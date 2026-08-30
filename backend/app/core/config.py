from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TenantCredentials:
    business: str
    operator_token: str
    webhook_secret: str


@dataclass(frozen=True)
class Settings:
    demo_mode: bool
    database_path: Path
    primary_business: str
    primary_token: str
    primary_webhook_secret: str
    secondary_business: str
    secondary_token: str
    secondary_webhook_secret: str
    cors_origins: tuple[str, ...]

    @classmethod
    def from_env(cls) -> Settings:
        demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
        settings = cls(
            demo_mode=demo_mode,
            database_path=Path(os.getenv("DATABASE_PATH", ".data/demo.db")),
            primary_business=os.getenv("DEMO_PRIMARY_BUSINESS", ""),
            primary_token=os.getenv("DEMO_PRIMARY_TOKEN", ""),
            primary_webhook_secret=os.getenv("DEMO_PRIMARY_WEBHOOK_SECRET", ""),
            secondary_business=os.getenv("DEMO_SECONDARY_BUSINESS", ""),
            secondary_token=os.getenv("DEMO_SECONDARY_TOKEN", ""),
            secondary_webhook_secret=os.getenv("DEMO_SECONDARY_WEBHOOK_SECRET", ""),
            cors_origins=tuple(
                origin.strip()
                for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
                if origin.strip()
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        values = (
            self.primary_business,
            self.primary_token,
            self.primary_webhook_secret,
            self.secondary_business,
            self.secondary_token,
            self.secondary_webhook_secret,
        )
        if not self.demo_mode:
            raise RuntimeError(
                "This public reference implementation starts only in explicit DEMO_MODE."
            )
        if any(not value for value in values):
            raise RuntimeError("Synthetic demo credentials are required.")
        if self.primary_business == self.secondary_business:
            raise RuntimeError("Demo businesses must be distinct.")

    @property
    def tenants(self) -> tuple[TenantCredentials, TenantCredentials]:
        return (
            TenantCredentials(
                self.primary_business, self.primary_token, self.primary_webhook_secret
            ),
            TenantCredentials(
                self.secondary_business, self.secondary_token, self.secondary_webhook_secret
            ),
        )

    def credentials_for(self, business: str) -> TenantCredentials | None:
        return next((tenant for tenant in self.tenants if tenant.business == business), None)
