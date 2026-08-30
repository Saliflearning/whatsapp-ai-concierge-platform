from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field


class Locale(StrEnum):
    EN = "en"
    FR = "fr"
    ES = "es"


class ResponseRoute(StrEnum):
    GROUNDED = "grounded"
    HANDOFF = "handoff"
    DUPLICATE = "duplicate"


class HandoffStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"


BoundedId = Annotated[str, Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9._:-]+$")]


class InboundMessage(BaseModel):
    event_id: BoundedId
    customer_label: Annotated[str, Field(min_length=1, max_length=80)]
    text: Annotated[str, Field(min_length=1, max_length=1000)]
    locale: Locale


class KnowledgeSource(BaseModel):
    id: str
    business_id: str
    label: str
    content: str
    keywords: tuple[str, ...]
    approved: bool


class PolicyDecision(BaseModel):
    route: ResponseRoute
    response_text: str
    reason_code: str
    knowledge_source: KnowledgeSource | None = None


class MessageResult(BaseModel):
    conversation_id: str
    message_id: str
    outbound_message_id: str
    route: ResponseRoute
    response_text: str
    reason_code: str
    duplicate: bool = False
    handoff_id: str | None = None
    knowledge_source: dict[str, str] | None = None


class ResolveResult(BaseModel):
    id: str
    conversation_id: str
    status: HandoffStatus
    reason_code: str
    resolved_at: str | None
    changed: bool
