from __future__ import annotations

from intel_ontology_demo.models import KnowledgeState


def render_ontology(state: KnowledgeState) -> str:
    classes = "\n".join([f"- {c.name}: {c.description}" for c in state.ontology_classes.values()]) or "(empty)"

    relations = "\n".join(
        [f"- {r.name} ({r.source_class} -> {r.target_class}): {r.description}" for r in state.relation_types.values()]
    ) or "(empty)"

    return f"[Ontology Classes]\n{classes}\n\n[Ontology Relations]\n{relations}"


def render_instances(state: KnowledgeState) -> str:
    entities = "\n".join(
        [f"- {e.entity_id} ({e.class_name}) name={e.properties.get('name', '')}" for e in state.entities.values()]
    ) or "(empty)"

    links = "\n".join(
        [f"- {r.source_id} -[{r.relation_type}/{r.confidence:.2f}]-> {r.target_id}" for r in state.relations]
    ) or "(empty)"

    events = "\n".join(
        [
            f"- {evt.event_id}: {evt.time} {evt.subject_id} {evt.action} {evt.object_id} @ {evt.location_id}, result={evt.result}"
            for evt in state.events.values()
        ]
    ) or "(empty)"

    return f"[Entities]\n{entities}\n\n[Instance Relations]\n{links}\n\n[Events]\n{events}"


def render_ontology_timeline(state: KnowledgeState) -> str:
    lines = []
    for change in state.ontology_changes:
        lines.append(f"- v{change.version} | {change.timestamp} | {change.detail}")
    return "\n".join(lines) or "(no schema changes yet)"


def render_combined(state: KnowledgeState) -> str:
    return f"{render_ontology(state)}\n\n{'=' * 60}\n\n{render_instances(state)}"
