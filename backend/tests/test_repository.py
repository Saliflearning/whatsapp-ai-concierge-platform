from pathlib import Path

from app.domain.models import InboundMessage, KnowledgeSource, Locale, PolicyDecision, ResponseRoute
from app.repositories.sqlite import SQLiteRepository


def make_repository(tmp_path: Path) -> SQLiteRepository:
    repository = SQLiteRepository(tmp_path / "repository.db")
    repository.initialize()
    for business in ("alpha-demo", "beta-demo"):
        repository.upsert_business(
            business_id=business,
            slug=business,
            display_name=f"{business} synthetic tenant",
            default_locale="en",
        )
    return repository


def test_knowledge_and_conversations_are_tenant_scoped(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    repository.upsert_knowledge(
        KnowledgeSource(
            id="alpha-hours",
            business_id="alpha-demo",
            label="Synthetic hours",
            content="Open weekdays.",
            keywords=("hours",),
            approved=True,
        )
    )
    assert [source.id for source in repository.approved_knowledge("alpha-demo")] == ["alpha-hours"]
    assert repository.approved_knowledge("beta-demo") == []


def test_persistence_is_idempotent_and_audited(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    message = InboundMessage(
        event_id="event-1", customer_label="Synthetic visitor", text="Unknown", locale=Locale.EN
    )
    decision = PolicyDecision(
        route=ResponseRoute.HANDOFF,
        response_text="A human operator should review this request.",
        reason_code="insufficient_evidence",
    )
    first = repository.persist_decision(
        business_id="alpha-demo", message=message, decision=decision
    )
    second = repository.persist_decision(
        business_id="alpha-demo", message=message, decision=decision
    )
    assert first.message_id == second.message_id
    assert second.duplicate is True
    detail = repository.conversation_detail("alpha-demo", first.conversation_id)
    assert detail is not None
    assert len(detail["messages"]) == 2
    assert [event["event_type"] for event in detail["audit_events"]] == ["message.processed"]
    assert repository.conversation_detail("beta-demo", first.conversation_id) is None
