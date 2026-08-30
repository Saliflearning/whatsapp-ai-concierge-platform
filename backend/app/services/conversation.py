from __future__ import annotations

from app.adapters.messaging import MessageTransport
from app.domain.models import InboundMessage, MessageResult
from app.repositories.sqlite import SQLiteRepository
from app.services.policy import PolicyEngine


class ConversationService:
    def __init__(
        self,
        repository: SQLiteRepository,
        policy: PolicyEngine,
        transport: MessageTransport,
    ) -> None:
        self.repository = repository
        self.policy = policy
        self.transport = transport

    def process(self, business_id: str, message: InboundMessage) -> MessageResult:
        existing = self.repository.result_for_event(business_id, message.event_id)
        if existing is not None:
            return existing

        sources = self.repository.approved_knowledge(business_id)
        decision = self.policy.decide(
            text=message.text,
            locale=message.locale,
            knowledge_sources=sources,
        )
        result = self.repository.persist_decision(
            business_id=business_id,
            message=message,
            decision=decision,
        )
        if not result.duplicate:
            self.transport.send(
                business_id=business_id,
                conversation_id=result.conversation_id,
                text=result.response_text,
            )
        return result
