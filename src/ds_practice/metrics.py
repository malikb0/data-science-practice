"""Metric helpers so definitions are identical in notebooks and tests."""
from __future__ import annotations

import math

import numpy as np


def regression_metrics(y_true, y_pred) -> dict:
    """MAE, RMSE, and R^2 for a regression model."""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    y_true = np.asarray(y_true, dtype=float).ravel()
    y_pred = np.asarray(y_pred, dtype=float).ravel()
    mse = mean_squared_error(y_true, y_pred)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(math.sqrt(mse)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def adjusted_r2(r2: float, n: int, p: int) -> float:
    """R^2 adjusted for the number of predictors ``p`` and samples ``n``."""
    if n <= p + 1:
        raise ValueError("need more samples than predictors")
    return 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1)


def classification_metrics(y_true, y_pred, average: str = "weighted") -> dict:
    """Accuracy, precision, recall, and F1 for a classifier."""
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
    )

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
    }
