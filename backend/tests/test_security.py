import hashlib
import hmac

from app.core.config import Settings
from app.core.security import sign_payload, verify_signature


def test_hmac_signature_round_trip(settings: Settings) -> None:
    payload = b'{"event_id":"synthetic-event-1"}'
    signature = sign_payload(payload, settings.primary_webhook_secret)
    assert verify_signature(payload, signature, settings.primary_webhook_secret)


def test_hmac_rejects_tampering(settings: Settings) -> None:
    payload = b'{"event_id":"synthetic-event-1"}'
    signature = (
        "sha256="
        + hmac.new(settings.primary_webhook_secret.encode(), payload, hashlib.sha256).hexdigest()
    )
    assert not verify_signature(payload + b" ", signature, settings.primary_webhook_secret)
