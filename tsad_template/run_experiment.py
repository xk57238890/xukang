from __future__ import annotations

import argparse
import json

from tsad_template.training.runner import MODEL_REGISTRY, run_once


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified SWaT + KDD experiment runner")
    parser.add_argument("--dataset", choices=["swat", "kdd", "kddcup99"], required=True)
    parser.add_argument("--model", choices=sorted(MODEL_REGISTRY.keys()), default="iforest")
    args = parser.parse_args()

    metrics = run_once(dataset=args.dataset, model=args.model)
    print(json.dumps({"dataset": args.dataset, "model": args.model, "metrics": metrics}, indent=2))


if __name__ == "__main__":
    main()
