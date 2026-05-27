from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dataclass
class DatasetSplit:
    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray


class UnifiedDatasetLoader:
    def __init__(self, data_root: str | Path = "tsad_template/data") -> None:
        self.data_root = Path(data_root)

    def load(self, dataset_name: str, test_size: float = 0.3, random_state: int = 42) -> DatasetSplit:
        dataset_name = dataset_name.lower()
        if dataset_name == "swat":
            x, y = self._load_swat()
        elif dataset_name in {"kdd", "kddcup99"}:
            x, y = self._load_kdd()
        else:
            raise ValueError(f"Unsupported dataset: {dataset_name}")

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=random_state, stratify=y
        )

        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        return DatasetSplit(x_train, y_train, x_test, y_test)

    def _load_swat(self) -> tuple[np.ndarray, np.ndarray]:
        path = self.data_root / "swat.csv"
        df = pd.read_csv(path)
        y = (df["label"].astype(str).str.lower().isin(["attack", "1", "true"]).astype(int)).to_numpy()
        x = df.drop(columns=["label"]).to_numpy(dtype=float)
        return x, y

    def _load_kdd(self) -> tuple[np.ndarray, np.ndarray]:
        path = self.data_root / "kdd.csv"
        df = pd.read_csv(path)
        if "label" not in df.columns:
            raise ValueError("kdd.csv must include 'label' column.")
        # Minimal baseline: numeric-only features for quick reproducibility.
        numeric_df = df.select_dtypes(include=["number"]).copy()
        y = (df["label"].astype(str) != "normal").astype(int).to_numpy()
        x = numeric_df.drop(columns=["label"], errors="ignore").to_numpy(dtype=float)
        return x, y
