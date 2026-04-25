from __future__ import annotations

from intel_ontology_demo.models import KnowledgeState, OntologyClass, RelationType


class OntologyEditor:
    """Manual ontology editing capability."""

    def add_class(self, state: KnowledgeState, class_name: str, description: str) -> None:
        state.ontology_classes[class_name] = OntologyClass(class_name, description)

    def add_relation(
        self,
        state: KnowledgeState,
        relation_name: str,
        source_class: str,
        target_class: str,
        description: str,
    ) -> None:
        state.relation_types[relation_name] = RelationType(
            relation_name,
            source_class,
            target_class,
            description,
        )
