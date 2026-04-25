from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import List

from intel_ontology_demo.adapters.kag_adapter import ExtractedEvent, ExtractedFact


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> List[ExtractedFact]:
        raise NotImplementedError

    def extract_events(self, text: str) -> List[ExtractedEvent]:
        return []


class KAGStyleExtractor(BaseExtractor):
    """A rule-guided extractor that approximates KAG-style structured extraction."""

    def extract(self, text: str) -> List[ExtractedFact]:
        facts: List[ExtractedFact] = []
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

    def extract_events(self, text: str) -> List[ExtractedEvent]:
        events: List[ExtractedEvent] = []
        # Pattern: On 2026-04-20 Alice attacked Depot at Harbor resulting disruption
        event_pattern = (
            r"On\s+(\d{4}-\d{2}-\d{2})\s+([A-Z][a-zA-Z0-9]+)\s+([a-z_]+)\s+"
            r"([A-Z][a-zA-Z0-9]+)\s+at\s+([A-Z][a-zA-Z0-9\s]+)(?:\s+resulting\s+([a-zA-Z\s]+))?"
        )
        for m in re.finditer(event_pattern, text):
            events.append(
                ExtractedEvent(
                    subject=m.group(2),
                    subject_class="Organization" if m.group(2).isupper() else "Person",
                    action=m.group(3),
                    obj=m.group(4),
                    object_class="Asset",
                    timestamp=m.group(1),
                    location=m.group(5).strip(),
                    location_class="Location",
                    result=(m.group(6) or "unknown").strip(),
                )
            )
        return events


class PureLLMExtractor(BaseExtractor):
    """Placeholder for pure-LLM extraction pipeline."""

    def extract(self, text: str) -> List[ExtractedFact]:
        facts: List[ExtractedFact] = []
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

    def extract_events(self, text: str) -> List[ExtractedEvent]:
        events: List[ExtractedEvent] = []
        pattern = (
            r"(\d{4}-\d{2}-\d{2})\s*:\s*([A-Za-z0-9]+)\s+deployed\s+([A-Za-z0-9]+)\s+"
            r"to\s+([A-Za-z\s]+)"
        )
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            events.append(
                ExtractedEvent(
                    subject=m.group(2).title(),
                    subject_class="Organization",
                    action="deployed",
                    obj=m.group(3).title(),
                    object_class="Asset",
                    timestamp=m.group(1),
                    location=m.group(4).strip().title(),
                    location_class="StrategicArea",
                    result="presence_increase",
                    confidence=0.74,
                )
            )
        return events
