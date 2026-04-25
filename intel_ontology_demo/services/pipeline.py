from __future__ import annotations

from intel_ontology_demo.adapters.extractors import KAGStyleExtractor, PureLLMExtractor
from intel_ontology_demo.adapters.kag_adapter import KAGOpenSPGAdapter
from intel_ontology_demo.models import KnowledgeState


class IntelOntologyPipeline:
    def __init__(self) -> None:
        self.adapter = KAGOpenSPGAdapter()
        self.kag_extractor = KAGStyleExtractor()
        self.llm_extractor = PureLLMExtractor()

    def bootstrap(self, domain: str = "intel") -> KnowledgeState:
        return self.adapter.initialize_ontology(domain)

    def extract_and_merge(self, state: KnowledgeState, text: str, mode: str = "kag") -> KnowledgeState:
        if mode == "kag":
            facts = self.kag_extractor.extract(text)
        elif mode == "llm":
            facts = self.llm_extractor.extract(text)
        else:
            raise ValueError("mode must be either 'kag' or 'llm'")

        return self.adapter.ingest_facts(state, facts)
