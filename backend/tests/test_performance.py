from statistics import median
from time import perf_counter

from fastapi.testclient import TestClient


def test_one_hundred_local_requests_have_bounded_median_latency(
    client: TestClient, primary_headers: dict[str, str]
) -> None:
    durations_ms: list[float] = []
    for index in range(100):
        started = perf_counter()
        response = client.post(
            "/api/demo/messages",
            headers=primary_headers,
            json={
                "event_id": f"performance-{index}",
                "customer_label": f"Synthetic visitor {index}",
                "text": "What are your weekend hours?",
                "locale": "en",
            },
        )
        durations_ms.append((perf_counter() - started) * 1000)
        assert response.status_code == 200
    assert median(durations_ms) < 100
