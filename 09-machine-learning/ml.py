"""Model factories for the machine-learning module.

Each factory returns an unfitted scikit-learn estimator or pipeline so the
notebooks can share identical, seeded preprocessing.
"""
from __future__ import annotations

import pandas as pd

SEED = 42


def make_classifier(kind: str = "logistic", seed: int = SEED, **kwargs):
    """Return a classification pipeline (scaler + model)."""
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    models = {
        "logistic": LogisticRegression(max_iter=1000, random_state=seed),
        "tree": DecisionTreeClassifier(random_state=seed),
        "forest": RandomForestClassifier(n_estimators=200, random_state=seed),
        "boosting": GradientBoostingClassifier(random_state=seed),
        "svm": SVC(probability=True, random_state=seed),
        "knn": KNeighborsClassifier(),
    }
    if kind not in models:
        raise ValueError(f"unknown classifier {kind!r}; choose from {sorted(models)}")
    models[kind].set_params(**kwargs)
    return Pipeline([("scale", StandardScaler()), ("model", models[kind])])


def make_regressor(kind: str = "linear", seed: int = SEED, **kwargs):
    """Return a regression pipeline (scaler + model)."""
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    models = {
        "linear": Ridge(alpha=1.0, random_state=seed),
        "ridge": Ridge(alpha=1.0, random_state=seed),
        "forest": RandomForestRegressor(n_estimators=200, random_state=seed),
        "boosting": GradientBoostingRegressor(random_state=seed),
    }
    if kind not in models:
        raise ValueError(f"unknown regressor {kind!r}; choose from {sorted(models)}")
    models[kind].set_params(**kwargs)
    return Pipeline([("scale", StandardScaler()), ("model", models[kind])])


def make_cluster(kind: str = "kmeans", n_clusters: int = 3, seed: int = SEED, **kwargs):
    """Return an unfitted clustering estimator (no scaler; cluster plots use raw units)."""
    from sklearn.cluster import DBSCAN, KMeans

    if kind == "kmeans":
        return KMeans(n_clusters=n_clusters, random_state=seed, n_init=10, **kwargs)
    if kind == "dbscan":
        return DBSCAN(**kwargs)
    raise ValueError(f"unknown clusterer {kind!r}; choose 'kmeans' or 'dbscan'")


def numeric_matrix(frame: pd.DataFrame, target: str | None = None):
    """Select numeric columns, optionally dropping a target, and return (X, y|None)."""
    numeric = frame.select_dtypes("number")
    if target is None:
        return numeric, None
    return numeric.drop(columns=[target]), numeric[target]
