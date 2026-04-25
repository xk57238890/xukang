from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class OntologyClass:
    name: str
    description: str


@dataclass
class RelationType:
    name: str
    source_class: str
    target_class: str
    description: str


@dataclass
class Entity:
    entity_id: str
    class_name: str
    properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class Relation:
    relation_type: str
    source_id: str
    target_id: str
    confidence: float = 1.0


@dataclass
class Event:
    event_id: str
    subject_id: str
    action: str
    object_id: str
    time: str
    location_id: str | None = None
    result: str | None = None


@dataclass
class CollectedDocument:
    doc_id: str
    source: str
    content: str
    collected_at: str


@dataclass
class OntologyChange:
    version: int
    change_type: str
    object_name: str
    detail: str
    timestamp: str


@dataclass
class OntologyVersion:
    version: int
    created_at: str
    class_count: int
    relation_count: int


@dataclass
class KnowledgeState:
    ontology_classes: Dict[str, OntologyClass] = field(default_factory=dict)
    relation_types: Dict[str, RelationType] = field(default_factory=dict)
    entities: Dict[str, Entity] = field(default_factory=dict)
    relations: List[Relation] = field(default_factory=list)

    events: Dict[str, Event] = field(default_factory=dict)
    documents: Dict[str, CollectedDocument] = field(default_factory=dict)
    processed_doc_ids: set[str] = field(default_factory=set)

    ontology_versions: List[OntologyVersion] = field(default_factory=list)
    ontology_changes: List[OntologyChange] = field(default_factory=list)

    def now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()
