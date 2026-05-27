from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class BaseModel(ABC):
    @abstractmethod
    def fit(self, x_train: np.ndarray, y_train: np.ndarray | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def score_samples(self, x: np.ndarray) -> np.ndarray:
        """Return anomaly scores where larger means more anomalous."""
        raise NotImplementedError
