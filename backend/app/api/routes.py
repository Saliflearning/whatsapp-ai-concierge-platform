from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app.core.config import Settings
from app.core.security import require_operator, verify_signature
from app.domain.models import InboundMessage, MessageResult
from app.services.conversation import ConversationService

router = APIRouter()


def conversation_service(request: Request) -> ConversationService:
    return cast(ConversationService, request.app.state.conversation_service)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "synthetic-demo"}


@router.post("/webhooks/messages", response_model=MessageResult)
async def receive_webhook(
    request: Request,
    x_demo_business: str = Header(min_length=1, max_length=80),
    x_webhook_signature: str = Header(min_length=1, max_length=160),
) -> MessageResult:
    settings: Settings = request.app.state.settings
    credentials = settings.credentials_for(x_demo_business)
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown demo business.")
    payload = await request.body()
    if not verify_signature(payload, x_webhook_signature, credentials.webhook_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature.",
        )
    message = InboundMessage.model_validate_json(payload)
    return conversation_service(request).process(credentials.business, message)


@router.post("/api/demo/messages", response_model=MessageResult)
def submit_demo_message(
    message: InboundMessage,
    request: Request,
    business_id: str = Depends(require_operator),
) -> MessageResult:
    return conversation_service(request).process(business_id, message)
