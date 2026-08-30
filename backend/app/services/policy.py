from __future__ import annotations

from app.domain.models import KnowledgeSource, Locale, PolicyDecision, ResponseRoute
from app.services.grounding import GroundingService

SENSITIVE_TERMS = (
    "safe neighborhood",
    "good neighborhood",
    "bad neighborhood",
    "good school",
    "best school",
    "legal advice",
    "guarantee",
)

HANDOFF_COPY = {
    Locale.EN: (
        "I cannot verify that from approved demo information. "
        "A human operator should review this request."
    ),
    Locale.FR: (
        "Je ne peux pas le vérifier avec les informations de démonstration approuvées. "
        "Un opérateur humain doit examiner cette demande."
    ),
    Locale.ES: (
        "No puedo verificarlo con la información de demostración aprobada. "
        "Un operador humano debe revisar esta solicitud."
    ),
}

GROUNDED_PREFIX = {
    Locale.EN: "Based on the approved demo source",
    Locale.FR: "Selon la source de démonstration approuvée",
    Locale.ES: "Según la fuente de demostración aprobada",
}


class PolicyEngine:
    def __init__(self, grounding: GroundingService | None = None) -> None:
        self.grounding = grounding or GroundingService()

    def decide(
        self, *, text: str, locale: Locale, knowledge_sources: list[KnowledgeSource]
    ) -> PolicyDecision:
        lowered = " ".join(text.lower().split())
        if any(term in lowered for term in SENSITIVE_TERMS):
            return PolicyDecision(
                route=ResponseRoute.HANDOFF,
                response_text=HANDOFF_COPY[locale],
                reason_code="policy_boundary",
            )

        source = self.grounding.match(text, knowledge_sources)
        if source is None:
            return PolicyDecision(
                route=ResponseRoute.HANDOFF,
                response_text=HANDOFF_COPY[locale],
                reason_code="insufficient_evidence",
            )

        return PolicyDecision(
            route=ResponseRoute.GROUNDED,
            response_text=f"{GROUNDED_PREFIX[locale]} “{source.label}”: {source.content}",
            reason_code="approved_knowledge",
            knowledge_source=source,
        )
