from app.domain.models import Locale, ResponseRoute
from app.services.policy import PolicyEngine


def test_policy_handoffs_sensitive_area_characterization() -> None:
    decision = PolicyEngine().decide(
        text="Is this a safe neighborhood?",
        locale=Locale.EN,
        knowledge_sources=[],
    )
    assert decision.route is ResponseRoute.HANDOFF
    assert decision.reason_code == "policy_boundary"
    assert "review" in decision.response_text.lower()
    assert "will" not in decision.response_text.lower()


def test_policy_handoffs_without_approved_evidence() -> None:
    decision = PolicyEngine().decide(
        text="Do you offer weekend appointments?",
        locale=Locale.EN,
        knowledge_sources=[],
    )
    assert decision.route is ResponseRoute.HANDOFF
    assert decision.reason_code == "insufficient_evidence"
