from __future__ import annotations

from tsad_template.data.datasets import UnifiedDatasetLoader
from tsad_template.evaluation.metrics import evaluate_scores
from tsad_template.models.iforest import IForestModel


MODEL_REGISTRY = {
    "iforest": IForestModel,
}


def run_once(dataset: str, model: str) -> dict[str, float]:
    loader = UnifiedDatasetLoader()
    split = loader.load(dataset)

    model_cls = MODEL_REGISTRY[model]
    estimator = model_cls()
    estimator.fit(split.x_train, split.y_train)
    scores = estimator.score_samples(split.x_test)
    return evaluate_scores(split.y_test, scores)
