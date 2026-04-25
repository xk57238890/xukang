from __future__ import annotations

from intel_ontology_demo.adapters.extractors import KAGStyleExtractor, PureLLMExtractor
from intel_ontology_demo.adapters.kag_adapter import KAGOpenSPGAdapter
from intel_ontology_demo.models import KnowledgeState
from intel_ontology_demo.services.data_ingestion import DataIngestionService
from intel_ontology_demo.services.reasoning import ReasoningService


class IntelOntologyPipeline:
    def __init__(self) -> None:
        self.adapter = KAGOpenSPGAdapter()
        self.kag_extractor = KAGStyleExtractor()
        self.llm_extractor = PureLLMExtractor()
        self.ingestion = DataIngestionService()
        self.reasoner = ReasoningService()

    def bootstrap(self, domain: str = "intel") -> KnowledgeState:
        return self.adapter.initialize_ontology(domain)

    def ingest_multisource(self, state: KnowledgeState, source_payloads: dict[str, list[str]]) -> KnowledgeState:
        docs = self.ingestion.collect(source_payloads, state)
        for doc in docs:
            state = self.extract_and_merge(state, doc.content, mode="llm")
        return state

    def extract_and_merge(self, state: KnowledgeState, text: str, mode: str = "kag") -> KnowledgeState:
        if mode == "kag":
            extractor = self.kag_extractor
        elif mode == "llm":
            extractor = self.llm_extractor
        else:
            raise ValueError("mode must be either 'kag' or 'llm'")

        facts = extractor.extract(text)
        events = extractor.extract_events(text)

        state = self.adapter.ingest_facts(state, facts)
        state = self.adapter.ingest_events(state, events)
        return state
