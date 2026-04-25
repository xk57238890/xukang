from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Iterable, List

from intel_ontology_demo.models import CollectedDocument, KnowledgeState


class DataIngestionService:
    """Simulated multi-source ingestion with incremental update + dedup."""

    def collect(self, source_payloads: dict[str, Iterable[str]], state: KnowledgeState) -> List[CollectedDocument]:
        new_docs: List[CollectedDocument] = []
        for source, payloads in source_payloads.items():
            for text in payloads:
                doc_id = self._build_doc_id(source, text)
                if doc_id in state.processed_doc_ids:
                    continue
                doc = CollectedDocument(
                    doc_id=doc_id,
                    source=source,
                    content=text,
                    collected_at=datetime.now(timezone.utc).isoformat(),
                )
                state.documents[doc_id] = doc
                state.processed_doc_ids.add(doc_id)
                new_docs.append(doc)
        return new_docs

    def _build_doc_id(self, source: str, content: str) -> str:
        key = f"{source}:{content.strip()}".encode("utf-8")
        digest = hashlib.md5(key).hexdigest()[:12]
        return f"{source.lower()}_{digest}"
