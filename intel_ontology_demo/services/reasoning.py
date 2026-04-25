from __future__ import annotations

from collections import defaultdict

from intel_ontology_demo.models import KnowledgeState


class ReasoningService:
    """Simple graph + event reasoning for demo outputs."""

    def find_key_person_network(self, state: KnowledgeState) -> dict[str, list[str]]:
        network: dict[str, list[str]] = defaultdict(list)
        for rel in state.relations:
            if rel.relation_type == "member_of":
                network[rel.source_id].append(rel.target_id)
        return dict(network)

    def infer_risk_paths(self, state: KnowledgeState) -> list[str]:
        paths: list[str] = []
        for event in state.events.values():
            if event.result and "disruption" in event.result.lower():
                paths.append(f"{event.subject_id} -> {event.action} -> {event.object_id} @ {event.location_id}")
        return paths

    def answer_recent_activities(self, state: KnowledgeState, org_name: str) -> str:
        org_id = org_name.strip().lower().replace(" ", "_")
        activities = [
            f"{event.time}: {event.subject_id} {event.action} {event.object_id} ({event.location_id})"
            for event in state.events.values()
            if event.subject_id == org_id
        ]
        if not activities:
            return f"未在事件图谱中发现组织 {org_name} 的近期活动。"
        return "\n".join(activities)
