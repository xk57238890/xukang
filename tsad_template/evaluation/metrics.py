from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_fscore_support


def evaluate_scores(y_true: np.ndarray, scores: np.ndarray, quantile: float = 0.95) -> dict[str, float]:
    threshold = float(np.quantile(scores, quantile))
    y_pred = (scores >= threshold).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
    ap = average_precision_score(y_true, scores)
    return {
        "threshold": threshold,
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
        "aupr": float(ap),
    }
