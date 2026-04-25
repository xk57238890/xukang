from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import List

from intel_ontology_demo.adapters.kag_adapter import ExtractedFact


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> List[ExtractedFact]:
        raise NotImplementedError


class KAGStyleExtractor(BaseExtractor):
    """A rule-guided extractor that approximates KAG-style structured extraction."""

    def extract(self, text: str) -> List[ExtractedFact]:
        facts: List[ExtractedFact] = []
        # Pattern: Alice joined ACME
        for m in re.finditer(r"([A-Z][a-z]+) joined ([A-Z][A-Za-z0-9]+)", text):
            facts.append(
                ExtractedFact(
                    source=m.group(1),
                    relation="member_of",
                    target=m.group(2),
                    source_class="Person",
                    target_class="Organization",
                )
            )

        # Pattern: ACME in Shanghai
        for m in re.finditer(r"([A-Z][A-Za-z0-9]+) in ([A-Z][a-zA-Z\s]+)", text):
            facts.append(
                ExtractedFact(
                    source=m.group(1),
                    relation="located_in",
                    target=m.group(2).strip(),
                    source_class="Organization",
                    target_class="Location",
                )
            )

        return facts


class PureLLMExtractor(BaseExtractor):
    """
    Placeholder for pure-LLM extraction pipeline.
    In practice this can call GPT/DeepSeek/Qwen etc and parse JSON output.
    """

    def extract(self, text: str) -> List[ExtractedFact]:
        facts: List[ExtractedFact] = []
        # Pattern: drone observed near harbor -> auto-evolve class/relation
        for m in re.finditer(r"([A-Za-z]+) observed near ([A-Za-z\s]+)", text, flags=re.IGNORECASE):
            facts.append(
                ExtractedFact(
                    source=m.group(1).title(),
                    relation="observed_near",
                    target=m.group(2).strip().title(),
                    source_class="Asset",
                    target_class="StrategicArea",
                    confidence=0.76,
                )
            )

        return facts
