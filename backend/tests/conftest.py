from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        demo_mode=True,
        database_path=tmp_path / "demo.db",
        primary_business="northstar-demo",
        primary_token="demo-northstar-operator-token",
        primary_webhook_secret="demo-northstar-webhook-secret",
        secondary_business="harbor-demo",
        secondary_token="demo-harbor-operator-token",
        secondary_webhook_secret="demo-harbor-webhook-secret",
        cors_origins=("http://localhost:3000",),
    )


@pytest.fixture
def client(settings: Settings) -> TestClient:
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def primary_headers() -> dict[str, str]:
    return {
        "x-demo-business": "northstar-demo",
        "x-demo-token": "demo-northstar-operator-token",
    }


@pytest.fixture
def secondary_headers() -> dict[str, str]:
    return {
        "x-demo-business": "harbor-demo",
        "x-demo-token": "demo-harbor-operator-token",
    }
