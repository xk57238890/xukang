from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from intel_ontology_demo.models import (
    Entity,
    Event,
    KnowledgeState,
    OntologyChange,
    OntologyClass,
    OntologyVersion,
    Relation,
    RelationType,
)


@dataclass
class ExtractedFact:
    source: str
    relation: str
    target: str
    source_class: str
    target_class: str
    confidence: float = 0.85


@dataclass
class ExtractedEvent:
    subject: str
    subject_class: str
    action: str
    obj: str
    object_class: str
    timestamp: str
    location: str
    location_class: str
    result: str
    confidence: float = 0.8


class KAGOpenSPGAdapter:
    """Lightweight adapter that mimics KAG/OpenSPG responsibilities."""

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
            self._snapshot_version(state, "初始化本体")
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

    def ingest_events(self, state: KnowledgeState, events: Iterable[ExtractedEvent]) -> KnowledgeState:
        self._ensure_class(state, "Asset", "装备或平台")
        for item in events:
            self._ensure_class(state, item.subject_class, f"Auto evolved class: {item.subject_class}")
            self._ensure_class(state, item.object_class, f"Auto evolved class: {item.object_class}")
            self._ensure_class(state, item.location_class, f"Auto evolved class: {item.location_class}")

            self._ensure_relation(
                state,
                ExtractedFact(
                    source=item.subject,
                    relation=item.action,
                    target=item.obj,
                    source_class=item.subject_class,
                    target_class=item.object_class,
                    confidence=item.confidence,
                ),
            )

            subject_id = self._upsert_entity(state, item.subject, item.subject_class)
            object_id = self._upsert_entity(state, item.obj, item.object_class)
            location_id = self._upsert_entity(state, item.location, item.location_class)

            event_id = f"evt_{len(state.events) + 1}"
            state.events[event_id] = Event(
                event_id=event_id,
                subject_id=subject_id,
                action=item.action,
                object_id=object_id,
                time=item.timestamp,
                location_id=location_id,
                result=item.result,
            )
            state.relations.append(Relation("involved_in", subject_id, event_id, item.confidence))
            state.relations.append(Relation("targets", event_id, object_id, item.confidence))
            state.relations.append(Relation("happened_at", event_id, location_id, item.confidence))

            self._ensure_relation(
                state,
                ExtractedFact("Event", "targets", "Asset", "Event", "Asset", item.confidence),
            )
            self._ensure_relation(
                state,
                ExtractedFact("Event", "happened_at", "Location", "Event", item.location_class, item.confidence),
            )
        return state

    def _ensure_class(self, state: KnowledgeState, class_name: str, description: str) -> None:
        if class_name not in state.ontology_classes:
            state.ontology_classes[class_name] = OntologyClass(class_name, description)
            self._snapshot_version(state, f"新增类 {class_name}")

    def _ensure_relation(self, state: KnowledgeState, fact: ExtractedFact) -> None:
        if fact.relation not in state.relation_types:
            state.relation_types[fact.relation] = RelationType(
                name=fact.relation,
                source_class=fact.source_class,
                target_class=fact.target_class,
                description=f"Auto evolved relation: {fact.relation}",
            )
            self._snapshot_version(state, f"新增关系 {fact.relation}")

    def _upsert_entity(self, state: KnowledgeState, entity_name: str, class_name: str) -> str:
        entity_id = entity_name.strip().lower().replace(" ", "_")
        if entity_id not in state.entities:
            state.entities[entity_id] = Entity(
                entity_id=entity_id,
                class_name=class_name,
                properties={"name": entity_name},
            )
        return entity_id

    def _snapshot_version(self, state: KnowledgeState, detail: str) -> None:
        version = len(state.ontology_versions) + 1
        now = state.now_iso()
        state.ontology_versions.append(
            OntologyVersion(
                version=version,
                created_at=now,
                class_count=len(state.ontology_classes),
                relation_count=len(state.relation_types),
            )
        )
        state.ontology_changes.append(
            OntologyChange(
                version=version,
                change_type="schema_update",
                object_name=detail.split(" ")[-1],
                detail=detail,
                timestamp=now,
            )
        )
