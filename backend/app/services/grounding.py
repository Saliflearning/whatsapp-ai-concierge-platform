from __future__ import annotations

import re

from app.domain.models import KnowledgeSource


class GroundingService:
    def match(self, text: str, sources: list[KnowledgeSource]) -> KnowledgeSource | None:
        normalized = set(re.findall(r"[a-z0-9]+", text.lower()))
        ranked: list[tuple[int, KnowledgeSource]] = []
        for source in sources:
            if not source.approved:
                continue
            score = sum(1 for keyword in source.keywords if keyword.lower() in normalized)
            if score:
                ranked.append((score, source))
        if not ranked:
            return None
        ranked.sort(key=lambda item: (-item[0], item[1].label))
        return ranked[0][1]
