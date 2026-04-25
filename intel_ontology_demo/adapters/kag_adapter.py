from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from intel_ontology_demo.models import Entity, KnowledgeState, OntologyClass, Relation, RelationType


@dataclass
class ExtractedFact:
    source: str
    relation: str
    target: str
    source_class: str
    target_class: str
    confidence: float = 0.85


class KAGOpenSPGAdapter:
    """
    Lightweight adapter that mimics the responsibilities of KAG/OpenSPG:
    - Initialize domain ontology
    - Accept extracted facts
    - Auto-evolve ontology when unknown classes/relations appear

    In production this class can be replaced by a real KAG/OpenSPG SDK integration.
    """

    def initialize_ontology(self, domain: str) -> KnowledgeState:
        state = KnowledgeState()
        if domain.lower() in {"intel", "intelligence", "情报"}:
            state.ontology_classes = {
                "Person": OntologyClass("Person", "人物对象"),
                "Organization": OntologyClass("Organization", "组织对象"),
                "Location": OntologyClass("Location", "地理位置"),
                "Event": OntologyClass("Event", "事件对象"),
            }
            state.relation_types = {
                "member_of": RelationType("member_of", "Person", "Organization", "成员关系"),
                "located_in": RelationType("located_in", "Organization", "Location", "组织所在地"),
                "involved_in": RelationType("involved_in", "Person", "Event", "参与事件"),
            }
        return state

    def ingest_facts(self, state: KnowledgeState, facts: Iterable[ExtractedFact]) -> KnowledgeState:
        for fact in facts:
            self._ensure_class(state, fact.source_class, f"Auto evolved class: {fact.source_class}")
            self._ensure_class(state, fact.target_class, f"Auto evolved class: {fact.target_class}")
            self._ensure_relation(state, fact)

            source_id = self._upsert_entity(state, fact.source, fact.source_class)
            target_id = self._upsert_entity(state, fact.target, fact.target_class)
            state.relations.append(
                Relation(
                    relation_type=fact.relation,
                    source_id=source_id,
                    target_id=target_id,
                    confidence=fact.confidence,
                )
            )
        return state

    def _ensure_class(self, state: KnowledgeState, class_name: str, description: str) -> None:
        if class_name not in state.ontology_classes:
            state.ontology_classes[class_name] = OntologyClass(class_name, description)

    def _ensure_relation(self, state: KnowledgeState, fact: ExtractedFact) -> None:
        if fact.relation not in state.relation_types:
            state.relation_types[fact.relation] = RelationType(
                name=fact.relation,
                source_class=fact.source_class,
                target_class=fact.target_class,
                description=f"Auto evolved relation: {fact.relation}",
            )

    def _upsert_entity(self, state: KnowledgeState, entity_name: str, class_name: str) -> str:
        entity_id = entity_name.strip().lower().replace(" ", "_")
        if entity_id not in state.entities:
            state.entities[entity_id] = Entity(
                entity_id=entity_id,
                class_name=class_name,
                properties={"name": entity_name},
            )
        return entity_id
