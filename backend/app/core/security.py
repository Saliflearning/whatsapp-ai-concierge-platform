from __future__ import annotations

import hashlib
import hmac

from fastapi import Header, HTTPException, Request, status

from app.core.config import Settings


def sign_payload(payload: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    if not signature.startswith("sha256="):
        return False
    return hmac.compare_digest(sign_payload(payload, secret), signature)


def require_operator(
    request: Request,
    x_demo_business: str = Header(min_length=1, max_length=80),
    x_demo_token: str = Header(min_length=1, max_length=160),
) -> str:
    settings: Settings = request.app.state.settings
    credentials = settings.credentials_for(x_demo_business)
    if credentials is None or not hmac.compare_digest(credentials.operator_token, x_demo_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid demo authorization.",
        )
    return credentials.business
