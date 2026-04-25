from __future__ import annotations

import argparse

from intel_ontology_demo.services.ontology_editor import OntologyEditor
from intel_ontology_demo.services.pipeline import IntelOntologyPipeline
from intel_ontology_demo.ui.console_view import render_combined, render_instances, render_ontology


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dynamic ontology demo for intelligence system")
    parser.add_argument(
        "--mode",
        choices=["kag", "llm"],
        default="kag",
        help="Extraction mode: KAG-style or pure LLM",
    )
    parser.add_argument(
        "--view",
        choices=["combined", "split"],
        default="combined",
        help="Display ontology+instances together or separately",
    )
    parser.add_argument(
        "--text",
        default="Alice joined ACME. ACME in Shanghai.",
        help="Input intelligence text",
    )
    parser.add_argument(
        "--edit-demo",
        action="store_true",
        help="Apply manual ontology editing before extraction",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pipeline = IntelOntologyPipeline()
    editor = OntologyEditor()

    state = pipeline.bootstrap("intel")

    if args.edit_demo:
        editor.add_class(state, "Operation", "人工添加：行动对象")
        editor.add_relation(state, "targets", "Organization", "Operation", "组织指向行动")

    state = pipeline.extract_and_merge(state, args.text, mode=args.mode)

    if args.view == "combined":
        print(render_combined(state))
    else:
        print(render_ontology(state))
        print("\n" + "=" * 60 + "\n")
        print(render_instances(state))


if __name__ == "__main__":
    main()
