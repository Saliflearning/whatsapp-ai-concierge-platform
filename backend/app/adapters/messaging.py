from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4


class MessageTransport(Protocol):
    def send(self, *, business_id: str, conversation_id: str, text: str) -> str: ...


@dataclass
class FakeMessageTransport:
    """Local-only provider seam. It performs no network access."""

    def send(self, *, business_id: str, conversation_id: str, text: str) -> str:
        del business_id, conversation_id, text
        return f"fake-delivery-{uuid4().hex}"
