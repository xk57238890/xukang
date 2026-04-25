from __future__ import annotations

from intel_ontology_demo.models import KnowledgeState


def render_ontology(state: KnowledgeState) -> str:
    classes = "\n".join(
        [f"- {c.name}: {c.description}" for c in state.ontology_classes.values()]
    ) or "(empty)"

    relations = "\n".join(
        [
            f"- {r.name} ({r.source_class} -> {r.target_class}): {r.description}"
            for r in state.relation_types.values()
        ]
    ) or "(empty)"

    return f"[Ontology Classes]\n{classes}\n\n[Ontology Relations]\n{relations}"


def render_instances(state: KnowledgeState) -> str:
    entities = "\n".join(
        [
            f"- {e.entity_id} ({e.class_name}) name={e.properties.get('name', '')}"
            for e in state.entities.values()
        ]
    ) or "(empty)"

    links = "\n".join(
        [
            f"- {r.source_id} -[{r.relation_type}/{r.confidence:.2f}]-> {r.target_id}"
            for r in state.relations
        ]
    ) or "(empty)"

    return f"[Entities]\n{entities}\n\n[Instance Relations]\n{links}"


def render_combined(state: KnowledgeState) -> str:
    return f"{render_ontology(state)}\n\n{'=' * 60}\n\n{render_instances(state)}"
