from __future__ import annotations

from dataclasses import dataclass, field
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
class KnowledgeState:
    ontology_classes: Dict[str, OntologyClass] = field(default_factory=dict)
    relation_types: Dict[str, RelationType] = field(default_factory=dict)
    entities: Dict[str, Entity] = field(default_factory=dict)
    relations: List[Relation] = field(default_factory=list)
