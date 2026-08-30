from __future__ import annotations

from app.core.config import Settings
from app.domain.models import KnowledgeSource
from app.repositories.sqlite import SQLiteRepository

SYNTHETIC_BUSINESSES = {
    "northstar-demo": ("Northstar Demo Realty", "en"),
    "harbor-demo": ("Harbor Demo Homes", "fr"),
}

SYNTHETIC_KNOWLEDGE = {
    "northstar-demo": (
        KnowledgeSource(
            id="knowledge-northstar-hours",
            business_id="northstar-demo",
            label="Synthetic service hours",
            content=(
                "Demo appointments are available weekdays 09:00–17:00 and Saturday 10:00–14:00."
            ),
            keywords=("hours", "weekend", "saturday", "appointment", "open"),
            approved=True,
        ),
        KnowledgeSource(
            id="knowledge-northstar-process",
            business_id="northstar-demo",
            label="Synthetic consultation process",
            content=(
                "The demo process begins with a needs review before any next-step recommendation."
            ),
            keywords=("process", "consultation", "start", "steps"),
            approved=True,
        ),
    ),
    "harbor-demo": (
        KnowledgeSource(
            id="knowledge-harbor-hours",
            business_id="harbor-demo",
            label="Horaires synthétiques",
            content=(
                "Les rendez-vous de démonstration sont disponibles du lundi "
                "au vendredi, de 10 h à 16 h."
            ),
            keywords=("horaires", "heures", "rendez", "hours", "appointment"),
            approved=True,
        ),
    ),
}


def seed_synthetic_demo(repository: SQLiteRepository, settings: Settings) -> None:
    for credentials in settings.tenants:
        display_name, locale = SYNTHETIC_BUSINESSES.get(
            credentials.business, (f"{credentials.business} synthetic tenant", "en")
        )
        repository.upsert_business(
            business_id=credentials.business,
            slug=credentials.business,
            display_name=display_name,
            default_locale=locale,
        )
        for source in SYNTHETIC_KNOWLEDGE.get(credentials.business, ()):
            repository.upsert_knowledge(source)
