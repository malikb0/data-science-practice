"""Feature engineering and model helpers for the California Housing analysis."""
from __future__ import annotations

import pandas as pd

from ds_practice.metrics import regression_metrics

TARGET = "MedHouseVal"
BASE_FEATURES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude",
]


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Add three ratio features derived from the base columns."""
    frame = frame.copy()
    frame["bedrooms_per_room"] = frame["AveBedrms"] / frame["AveRooms"]
    frame["population_per_household"] = frame["Population"] / frame["AveOccup"]
    frame["rooms_per_person"] = frame["AveRooms"] / frame["AveOccup"]
    return frame


def split_xy(frame: pd.DataFrame, target: str = TARGET):
    """Return (X, y) with the target excluded from the features."""
    y = frame[target]
    X = frame.drop(columns=[target])
    return X, y


def fit_linear(X, y, scale: bool = True):
    """Fit a (optionally standardised) linear regression and return the pipeline."""
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    steps = [("scale", StandardScaler())] if scale else []
    model = Pipeline(steps + [("model", LinearRegression())])
    return model.fit(X, y)


def fit_polynomial(X, y, degree: int = 2):
    """Fit polynomial regression as scaler -> polynomial -> linear."""
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler

    model = Pipeline([
        ("scale", StandardScaler()),
        ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
        ("model", LinearRegression()),
    ])
    return model.fit(X, y)


def evaluate(model, X, y) -> dict:
    """Return MAE/RMSE/R2 for a fitted model."""
    return regression_metrics(y, model.predict(X))
