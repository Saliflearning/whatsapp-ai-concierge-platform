from __future__ import annotations

from typing import Any

ALLOWED_AUDIT_KEYS = frozenset({"route", "reason_code", "knowledge_source_id", "handoff_id"})


def safe_audit_metadata(metadata: dict[str, Any]) -> dict[str, str | None]:
    """Keep audit records useful without persisting customer message content."""
    return {
        key: None if value is None else str(value)[:160]
        for key, value in metadata.items()
        if key in ALLOWED_AUDIT_KEYS
    }
