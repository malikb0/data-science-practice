"""Module 07 — feature engineering, model smoke tests, and the data contract."""
import numpy as np
import pandas as pd
import pytest

from helpers import load_module, require_file

analysis = load_module("07-data-analysis/analysis.py", "analysis07")

FRAME = pd.DataFrame(
    {
        "MedInc": [2.0, 4.0, 6.0, 8.0],
        "HouseAge": [10, 20, 30, 40],
        "AveRooms": [4.0, 5.0, 6.0, 7.0],
        "AveBedrms": [1.0, 1.2, 1.4, 1.6],
        "Population": [500, 800, 1200, 1500],
        "AveOccup": [2.5, 3.0, 3.5, 4.0],
        "Latitude": [34.0, 35.0, 36.0, 37.0],
        "Longitude": [-118.0, -119.0, -120.0, -121.0],
        "MedHouseVal": [1.5, 2.0, 2.5, 3.0],
    }
)


def test_add_features_creates_ratios():
    result = analysis.add_features(FRAME)
    for column in ["bedrooms_per_room", "population_per_household", "rooms_per_person"]:
        assert column in result.columns
    row = result.iloc[0]
    assert np.isclose(row["bedrooms_per_room"], 1.0 / 4.0)


def test_split_xy_excludes_target():
    X, y = analysis.split_xy(FRAME)
    assert analysis.TARGET not in X.columns
    assert list(y) == list(FRAME[analysis.TARGET])


def test_models_fit_and_evaluate():
    pytest.importorskip("sklearn")
    X, y = analysis.split_xy(FRAME)
    linear = analysis.fit_linear(X, y)
    metrics = analysis.evaluate(linear, X, y)
    assert set(metrics) == {"mae", "rmse", "r2"}
    assert metrics["rmse"] >= 0

    poly = analysis.fit_polynomial(X, y, degree=2)
    assert analysis.evaluate(poly, X, y)["r2"] is not None


def test_california_data_contract():
    frame = pd.read_csv(require_file("california_housing.csv"))
    expected = set(analysis.BASE_FEATURES) | {analysis.TARGET}
    assert expected.issubset(frame.columns)
    assert len(frame) > 1000
    assert frame["MedHouseVal"].between(0, 6).all()
