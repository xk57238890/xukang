from __future__ import annotations

import numpy as np
from sklearn.ensemble import IsolationForest

from .base import BaseModel


class IForestModel(BaseModel):
    def __init__(self, random_state: int = 42, contamination: str | float = "auto") -> None:
        self.model = IsolationForest(random_state=random_state, contamination=contamination)

    def fit(self, x_train: np.ndarray, y_train: np.ndarray | None = None) -> None:
        self.model.fit(x_train)

    def score_samples(self, x: np.ndarray) -> np.ndarray:
        # sklearn score_samples: higher is more normal, so negate.
        return -self.model.score_samples(x)
