from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.security import require_operator
from app.repositories.sqlite import SQLiteRepository

router = APIRouter(prefix="/api")


def repository(request: Request) -> SQLiteRepository:
    return cast(SQLiteRepository, request.app.state.repository)


@router.get("/conversations")
def list_conversations(
    request: Request,
    business_id: str = Depends(require_operator),
) -> dict[str, object]:
    return {"conversations": repository(request).list_conversations(business_id)}


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: str,
    request: Request,
    business_id: str = Depends(require_operator),
) -> dict[str, object]:
    detail = repository(request).conversation_detail(business_id, conversation_id)
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    return detail


@router.post("/handoffs/{handoff_id}/resolve")
def resolve_handoff(
    handoff_id: str,
    request: Request,
    business_id: str = Depends(require_operator),
) -> object:
    result = repository(request).resolve_handoff(business_id, handoff_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Handoff not found.")
    return result
