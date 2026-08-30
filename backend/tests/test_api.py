from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.core.security import sign_payload


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "synthetic-demo"}


def test_demo_message_returns_grounded_evidence(
    client: TestClient, primary_headers: dict[str, str]
) -> None:
    response = client.post(
        "/api/demo/messages",
        headers=primary_headers,
        json={
            "event_id": "synthetic-grounded-1",
            "customer_label": "Demo visitor",
            "text": "What are your weekend hours?",
            "locale": "en",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["route"] == "grounded"
    assert body["knowledge_source"]["label"] == "Synthetic service hours"


def test_duplicate_event_is_idempotent(client: TestClient, primary_headers: dict[str, str]) -> None:
    payload = {
        "event_id": "synthetic-duplicate-1",
        "customer_label": "Demo visitor",
        "text": "What are your weekend hours?",
        "locale": "en",
    }
    first = client.post("/api/demo/messages", headers=primary_headers, json=payload)
    second = client.post("/api/demo/messages", headers=primary_headers, json=payload)
    assert first.status_code == second.status_code == 200
    assert second.json()["duplicate"] is True
    assert second.json()["message_id"] == first.json()["message_id"]


def test_signed_webhook_rejects_invalid_signature(client: TestClient) -> None:
    response = client.post(
        "/webhooks/messages",
        headers={"x-demo-business": "northstar-demo", "x-webhook-signature": "sha256=bad"},
        json={
            "event_id": "synthetic-webhook-1",
            "customer_label": "Demo visitor",
            "text": "Hello",
            "locale": "en",
        },
    )
    assert response.status_code == 401


def test_signed_webhook_accepts_valid_signature(client: TestClient) -> None:
    payload = {
        "event_id": "synthetic-webhook-2",
        "customer_label": "Demo visitor",
        "text": "What are your weekend hours?",
        "locale": "en",
    }
    raw = json.dumps(payload, separators=(",", ":")).encode()
    response = client.post(
        "/webhooks/messages",
        headers={
            "content-type": "application/json",
            "x-demo-business": "northstar-demo",
            "x-webhook-signature": sign_payload(raw, "demo-northstar-webhook-secret"),
        },
        content=raw,
    )
    assert response.status_code == 200


def test_webhook_rejects_oversized_body_before_processing(client: TestClient) -> None:
    response = client.post(
        "/webhooks/messages",
        headers={
            "content-type": "application/json",
            "x-demo-business": "northstar-demo",
            "x-webhook-signature": "sha256=synthetic",
        },
        content=b"x" * 4097,
    )
    assert response.status_code == 413


def test_cross_tenant_conversation_is_not_disclosed(
    client: TestClient,
    primary_headers: dict[str, str],
    secondary_headers: dict[str, str],
) -> None:
    created = client.post(
        "/api/demo/messages",
        headers=primary_headers,
        json={
            "event_id": "synthetic-private-tenant",
            "customer_label": "Demo visitor",
            "text": "I need legal advice about a contract",
            "locale": "en",
        },
    ).json()
    response = client.get(
        f"/api/conversations/{created['conversation_id']}", headers=secondary_headers
    )
    assert response.status_code == 404
