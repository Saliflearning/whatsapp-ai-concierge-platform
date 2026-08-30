from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.messaging import FakeMessageTransport
from app.api.operator import router as operator_router
from app.api.routes import router
from app.core.config import Settings
from app.repositories.sqlite import SQLiteRepository
from app.services.conversation import ConversationService
from app.services.policy import PolicyEngine
from app.services.seed import seed_synthetic_demo


def create_app(settings: Settings | None = None) -> FastAPI:
    runtime_settings = settings or Settings.from_env()
    runtime_settings.validate()
    repository = SQLiteRepository(runtime_settings.database_path)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        repository.initialize()
        seed_synthetic_demo(repository, runtime_settings)
        yield

    application = FastAPI(
        title="WhatsApp AI Concierge Showcase API",
        version="0.1.0",
        description="Synthetic, privacy-safe reference implementation.",
        lifespan=lifespan,
    )
    application.state.settings = runtime_settings
    application.state.repository = repository
    application.state.conversation_service = ConversationService(
        repository=repository,
        policy=PolicyEngine(),
        transport=FakeMessageTransport(),
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(runtime_settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["content-type", "x-demo-business", "x-demo-token", "x-webhook-signature"],
    )
    application.include_router(router)
    application.include_router(operator_router)
    return application
