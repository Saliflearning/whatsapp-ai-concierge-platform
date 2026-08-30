from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.domain.models import (
    HandoffStatus,
    InboundMessage,
    KnowledgeSource,
    MessageResult,
    PolicyDecision,
    ResolveResult,
    ResponseRoute,
)
from app.services.audit import safe_audit_metadata


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


class SQLiteRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS businesses (
                    id TEXT PRIMARY KEY,
                    slug TEXT NOT NULL UNIQUE,
                    display_name TEXT NOT NULL,
                    default_locale TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS knowledge_sources (
                    id TEXT PRIMARY KEY,
                    business_id TEXT NOT NULL REFERENCES businesses(id),
                    label TEXT NOT NULL,
                    content TEXT NOT NULL,
                    keywords_json TEXT NOT NULL,
                    approved INTEGER NOT NULL CHECK (approved IN (0, 1)),
                    updated_at TEXT NOT NULL,
                    UNIQUE (business_id, label)
                );
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    business_id TEXT NOT NULL REFERENCES businesses(id),
                    synthetic_customer_label TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('open', 'handoff', 'resolved')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_conversations_tenant
                    ON conversations (business_id, updated_at DESC);
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    business_id TEXT NOT NULL REFERENCES businesses(id),
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    parent_message_id TEXT REFERENCES messages(id),
                    provider_event_id TEXT,
                    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
                    body TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    response_route TEXT NOT NULL,
                    reason_code TEXT NOT NULL,
                    knowledge_source_id TEXT REFERENCES knowledge_sources(id),
                    created_at TEXT NOT NULL
                );
                CREATE UNIQUE INDEX IF NOT EXISTS idx_messages_event_tenant
                    ON messages (business_id, provider_event_id)
                    WHERE provider_event_id IS NOT NULL;
                CREATE TABLE IF NOT EXISTS handoffs (
                    id TEXT PRIMARY KEY,
                    business_id TEXT NOT NULL REFERENCES businesses(id),
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    message_id TEXT NOT NULL REFERENCES messages(id),
                    reason_code TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('open', 'resolved')),
                    created_at TEXT NOT NULL,
                    resolved_at TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_handoffs_tenant
                    ON handoffs (business_id, status, created_at DESC);
                CREATE TABLE IF NOT EXISTS audit_events (
                    id TEXT PRIMARY KEY,
                    business_id TEXT NOT NULL REFERENCES businesses(id),
                    conversation_id TEXT REFERENCES conversations(id),
                    event_type TEXT NOT NULL,
                    actor_type TEXT NOT NULL CHECK (actor_type IN ('system', 'operator')),
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_audit_tenant
                    ON audit_events (business_id, created_at DESC);
                """
            )

    def upsert_business(
        self, *, business_id: str, slug: str, display_name: str, default_locale: str
    ) -> None:
        with self.connection() as connection:
            connection.execute(
                """
                INSERT INTO businesses (id, slug, display_name, default_locale, created_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(slug) DO UPDATE SET display_name = excluded.display_name,
                    default_locale = excluded.default_locale
                """,
                (business_id, slug, display_name, default_locale, now_iso()),
            )

    def upsert_knowledge(self, source: KnowledgeSource) -> None:
        with self.connection() as connection:
            connection.execute(
                """
                INSERT INTO knowledge_sources
                    (id, business_id, label, content, keywords_json, approved, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(business_id, label) DO UPDATE SET
                    content = excluded.content,
                    keywords_json = excluded.keywords_json,
                    approved = excluded.approved,
                    updated_at = excluded.updated_at
                """,
                (
                    source.id,
                    source.business_id,
                    source.label,
                    source.content,
                    json.dumps(source.keywords),
                    int(source.approved),
                    now_iso(),
                ),
            )

    def business_exists(self, business_id: str) -> bool:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT 1 FROM businesses WHERE id = ?", (business_id,)
            ).fetchone()
        return row is not None

    def approved_knowledge(self, business_id: str) -> list[KnowledgeSource]:
        with self.connection() as connection:
            rows = connection.execute(
                """
                SELECT id, business_id, label, content, keywords_json, approved
                FROM knowledge_sources
                WHERE business_id = ? AND approved = 1
                ORDER BY label
                """,
                (business_id,),
            ).fetchall()
        return [
            KnowledgeSource(
                id=row["id"],
                business_id=row["business_id"],
                label=row["label"],
                content=row["content"],
                keywords=tuple(json.loads(row["keywords_json"])),
                approved=bool(row["approved"]),
            )
            for row in rows
        ]

    def result_for_event(self, business_id: str, event_id: str) -> MessageResult | None:
        with self.connection() as connection:
            return self._result_for_event(connection, business_id, event_id, duplicate=True)

    def _result_for_event(
        self,
        connection: sqlite3.Connection,
        business_id: str,
        event_id: str,
        *,
        duplicate: bool,
    ) -> MessageResult | None:
        row = connection.execute(
            """
            SELECT inbound.id AS message_id, inbound.conversation_id,
                   inbound.response_route, inbound.reason_code,
                   outbound.id AS outbound_message_id, outbound.body AS response_text,
                   handoffs.id AS handoff_id,
                   knowledge_sources.id AS source_id,
                   knowledge_sources.label AS source_label
            FROM messages AS inbound
            JOIN messages AS outbound ON outbound.parent_message_id = inbound.id
            LEFT JOIN handoffs ON handoffs.message_id = inbound.id
            LEFT JOIN knowledge_sources ON knowledge_sources.id = inbound.knowledge_source_id
            WHERE inbound.business_id = ? AND inbound.provider_event_id = ?
            """,
            (business_id, event_id),
        ).fetchone()
        if row is None:
            return None
        source = (
            {"id": row["source_id"], "label": row["source_label"]} if row["source_id"] else None
        )
        return MessageResult(
            conversation_id=row["conversation_id"],
            message_id=row["message_id"],
            outbound_message_id=row["outbound_message_id"],
            route=ResponseRoute(row["response_route"]),
            response_text=row["response_text"],
            reason_code=row["reason_code"],
            duplicate=duplicate,
            handoff_id=row["handoff_id"],
            knowledge_source=source,
        )

    def persist_decision(
        self,
        *,
        business_id: str,
        message: InboundMessage,
        decision: PolicyDecision,
    ) -> MessageResult:
        timestamp = now_iso()
        with self.connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            duplicate = self._result_for_event(
                connection, business_id, message.event_id, duplicate=True
            )
            if duplicate is not None:
                return duplicate

            conversation = connection.execute(
                """
                SELECT id FROM conversations
                WHERE business_id = ? AND synthetic_customer_label = ? AND status != 'resolved'
                ORDER BY updated_at DESC LIMIT 1
                """,
                (business_id, message.customer_label),
            ).fetchone()
            conversation_id = conversation["id"] if conversation else uuid4().hex
            if conversation is None:
                connection.execute(
                    """
                    INSERT INTO conversations
                        (id, business_id, synthetic_customer_label, locale, status,
                         created_at, updated_at)
                    VALUES (?, ?, ?, ?, 'open', ?, ?)
                    """,
                    (
                        conversation_id,
                        business_id,
                        message.customer_label,
                        message.locale.value,
                        timestamp,
                        timestamp,
                    ),
                )

            inbound_id = uuid4().hex
            outbound_id = uuid4().hex
            source_id = decision.knowledge_source.id if decision.knowledge_source else None
            connection.execute(
                """
                INSERT INTO messages
                    (id, business_id, conversation_id, provider_event_id, direction, body,
                     locale, response_route, reason_code, knowledge_source_id, created_at)
                VALUES (?, ?, ?, ?, 'inbound', ?, ?, ?, ?, ?, ?)
                """,
                (
                    inbound_id,
                    business_id,
                    conversation_id,
                    message.event_id,
                    message.text,
                    message.locale.value,
                    decision.route.value,
                    decision.reason_code,
                    source_id,
                    timestamp,
                ),
            )
            connection.execute(
                """
                INSERT INTO messages
                    (id, business_id, conversation_id, parent_message_id, direction, body,
                     locale, response_route, reason_code, knowledge_source_id, created_at)
                VALUES (?, ?, ?, ?, 'outbound', ?, ?, ?, ?, ?, ?)
                """,
                (
                    outbound_id,
                    business_id,
                    conversation_id,
                    inbound_id,
                    decision.response_text,
                    message.locale.value,
                    decision.route.value,
                    decision.reason_code,
                    source_id,
                    timestamp,
                ),
            )

            handoff_id: str | None = None
            status = "open"
            if decision.route is ResponseRoute.HANDOFF:
                handoff_id = uuid4().hex
                status = "handoff"
                connection.execute(
                    """
                    INSERT INTO handoffs
                        (id, business_id, conversation_id, message_id, reason_code,
                         status, created_at)
                    VALUES (?, ?, ?, ?, ?, 'open', ?)
                    """,
                    (
                        handoff_id,
                        business_id,
                        conversation_id,
                        inbound_id,
                        decision.reason_code,
                        timestamp,
                    ),
                )
            connection.execute(
                """
                UPDATE conversations SET locale = ?, status = ?, updated_at = ?
                WHERE id = ? AND business_id = ?
                """,
                (message.locale.value, status, timestamp, conversation_id, business_id),
            )
            self._append_audit(
                connection,
                business_id=business_id,
                conversation_id=conversation_id,
                event_type="message.processed",
                actor_type="system",
                metadata={
                    "route": decision.route.value,
                    "reason_code": decision.reason_code,
                    "knowledge_source_id": source_id,
                },
                timestamp=timestamp,
            )

        return MessageResult(
            conversation_id=conversation_id,
            message_id=inbound_id,
            outbound_message_id=outbound_id,
            route=decision.route,
            response_text=decision.response_text,
            reason_code=decision.reason_code,
            handoff_id=handoff_id,
            knowledge_source=(
                {"id": decision.knowledge_source.id, "label": decision.knowledge_source.label}
                if decision.knowledge_source
                else None
            ),
        )

    def list_conversations(self, business_id: str, limit: int = 50) -> list[dict[str, Any]]:
        bounded_limit = min(max(limit, 1), 100)
        with self.connection() as connection:
            rows = connection.execute(
                """
                SELECT c.id, c.synthetic_customer_label, c.locale, c.status,
                       c.created_at, c.updated_at,
                       (SELECT response_route FROM messages m
                        WHERE m.conversation_id = c.id AND m.direction = 'inbound'
                        ORDER BY m.created_at DESC LIMIT 1) AS response_route,
                       (SELECT reason_code FROM messages m
                        WHERE m.conversation_id = c.id AND m.direction = 'inbound'
                        ORDER BY m.created_at DESC LIMIT 1) AS reason_code
                FROM conversations c
                WHERE c.business_id = ?
                ORDER BY c.updated_at DESC
                LIMIT ?
                """,
                (business_id, bounded_limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def conversation_detail(self, business_id: str, conversation_id: str) -> dict[str, Any] | None:
        with self.connection() as connection:
            conversation = connection.execute(
                "SELECT * FROM conversations WHERE id = ? AND business_id = ?",
                (conversation_id, business_id),
            ).fetchone()
            if conversation is None:
                return None
            messages = connection.execute(
                """
                SELECT m.id, m.direction, m.body, m.locale, m.response_route,
                       m.reason_code, m.created_at, k.id AS source_id, k.label AS source_label
                FROM messages m
                LEFT JOIN knowledge_sources k ON k.id = m.knowledge_source_id
                WHERE m.conversation_id = ? AND m.business_id = ?
                ORDER BY m.created_at, m.direction
                LIMIT 200
                """,
                (conversation_id, business_id),
            ).fetchall()
            handoffs = connection.execute(
                """
                SELECT id, reason_code, status, created_at, resolved_at
                FROM handoffs WHERE conversation_id = ? AND business_id = ?
                ORDER BY created_at DESC
                LIMIT 100
                """,
                (conversation_id, business_id),
            ).fetchall()
            audits = connection.execute(
                """
                SELECT id, event_type, actor_type, metadata_json, created_at
                FROM audit_events WHERE conversation_id = ? AND business_id = ?
                ORDER BY created_at DESC
                LIMIT 200
                """,
                (conversation_id, business_id),
            ).fetchall()

        message_items = []
        for row in messages:
            item = dict(row)
            item["knowledge_source"] = (
                {"id": item.pop("source_id"), "label": item.pop("source_label")}
                if item["source_id"]
                else None
            )
            item.pop("source_id", None)
            item.pop("source_label", None)
            message_items.append(item)
        audit_items = []
        for row in audits:
            item = dict(row)
            item["metadata"] = json.loads(item.pop("metadata_json"))
            audit_items.append(item)
        return {
            "conversation": dict(conversation),
            "messages": message_items,
            "handoffs": [dict(row) for row in handoffs],
            "audit_events": audit_items,
        }

    def resolve_handoff(self, business_id: str, handoff_id: str) -> ResolveResult | None:
        timestamp = now_iso()
        with self.connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM handoffs WHERE id = ? AND business_id = ?",
                (handoff_id, business_id),
            ).fetchone()
            if row is None:
                return None
            changed = row["status"] == HandoffStatus.OPEN.value
            resolved_at = row["resolved_at"]
            if changed:
                resolved_at = timestamp
                connection.execute(
                    """
                    UPDATE handoffs SET status = 'resolved', resolved_at = ?
                    WHERE id = ? AND business_id = ? AND status = 'open'
                    """,
                    (timestamp, handoff_id, business_id),
                )
                connection.execute(
                    """
                    UPDATE conversations SET status = 'resolved', updated_at = ?
                    WHERE id = ? AND business_id = ?
                    """,
                    (timestamp, row["conversation_id"], business_id),
                )
                self._append_audit(
                    connection,
                    business_id=business_id,
                    conversation_id=row["conversation_id"],
                    event_type="handoff.resolved",
                    actor_type="operator",
                    metadata={"handoff_id": handoff_id},
                    timestamp=timestamp,
                )
        return ResolveResult(
            id=handoff_id,
            conversation_id=row["conversation_id"],
            status=HandoffStatus.RESOLVED,
            reason_code=row["reason_code"],
            resolved_at=resolved_at,
            changed=changed,
        )

    @staticmethod
    def _append_audit(
        connection: sqlite3.Connection,
        *,
        business_id: str,
        conversation_id: str | None,
        event_type: str,
        actor_type: str,
        metadata: dict[str, Any],
        timestamp: str,
    ) -> None:
        connection.execute(
            """
            INSERT INTO audit_events
                (id, business_id, conversation_id, event_type, actor_type,
                 metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                uuid4().hex,
                business_id,
                conversation_id,
                event_type,
                actor_type,
                json.dumps(safe_audit_metadata(metadata), sort_keys=True),
                timestamp,
            ),
        )
