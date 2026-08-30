from fastapi.testclient import TestClient


def create_handoff(client: TestClient, headers: dict[str, str]) -> dict[str, object]:
    response = client.post(
        "/api/demo/messages",
        headers=headers,
        json={
            "event_id": "operator-handoff-1",
            "customer_label": "Synthetic operator journey",
            "text": "Please guarantee this outcome",
            "locale": "en",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_operator_can_list_inspect_and_resolve_handoff_idempotently(
    client: TestClient, primary_headers: dict[str, str]
) -> None:
    created = create_handoff(client, primary_headers)
    listing = client.get("/api/conversations", headers=primary_headers)
    assert listing.status_code == 200
    assert listing.json()["conversations"][0]["status"] == "handoff"

    detail = client.get(f"/api/conversations/{created['conversation_id']}", headers=primary_headers)
    assert detail.status_code == 200
    assert detail.json()["messages"][0]["reason_code"] == "policy_boundary"

    first = client.post(f"/api/handoffs/{created['handoff_id']}/resolve", headers=primary_headers)
    second = client.post(f"/api/handoffs/{created['handoff_id']}/resolve", headers=primary_headers)
    assert first.status_code == second.status_code == 200
    assert first.json()["changed"] is True
    assert second.json()["changed"] is False


def test_cross_tenant_handoff_mutation_is_hidden(
    client: TestClient,
    primary_headers: dict[str, str],
    secondary_headers: dict[str, str],
) -> None:
    created = create_handoff(client, primary_headers)
    response = client.post(
        f"/api/handoffs/{created['handoff_id']}/resolve", headers=secondary_headers
    )
    assert response.status_code == 404


def test_conversation_listing_limit_is_bounded(
    client: TestClient, primary_headers: dict[str, str]
) -> None:
    assert client.get("/api/conversations?limit=101", headers=primary_headers).status_code == 422
