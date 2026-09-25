"""Module 09 — model factories, numeric selection, and data contracts."""
import numpy as np
import pandas as pd
import pytest

from helpers import load_module, require_file

ml = load_module("09-machine-learning/ml.py", "ml09")


def _classification_frame():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(60, 3))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    return pd.DataFrame(X, columns=["a", "b", "c"]).assign(target=y)


def test_make_classifier_fits_and_predicts():
    pytest.importorskip("sklearn")
    frame = _classification_frame()
    model = ml.make_classifier("tree", max_depth=3)
    model.fit(frame[["a", "b", "c"]], frame["target"])
    pred = model.predict(frame[["a", "b", "c"]])
    assert len(pred) == len(frame)
    assert set(pred).issubset({0, 1})


def test_make_regressor_fits():
    pytest.importorskip("sklearn")
    frame = _classification_frame()
    model = ml.make_regressor("linear")
    model.fit(frame[["a", "b", "c"]], frame["a"])
    assert model.predict(frame[["a", "b", "c"]]).shape == (len(frame),)


def test_make_cluster_assigns_labels():
    pytest.importorskip("sklearn")
    rng = np.random.default_rng(1)
    X = rng.normal(size=(40, 2))
    labels = ml.make_cluster("kmeans", n_clusters=2).fit_predict(X)
    assert set(np.unique(labels)).issubset({0, 1})


def test_unknown_kind_raises():
    pytest.importorskip("sklearn")
    with pytest.raises(ValueError):
        ml.make_classifier("nope")


def test_numeric_matrix_drops_target():
    frame = _classification_frame()
    X, y = ml.numeric_matrix(frame, target="target")
    assert "target" not in X.columns
    assert list(y) == list(frame["target"])


def test_uci_data_contracts():
    adult = pd.read_csv(require_file("adult.data"), header=None, skipinitialspace=True, na_values="?")
    assert adult.shape[1] == 15
    assert adult[14].dropna().isin(["<=50K", ">50K"]).all()

    wine = pd.read_csv(require_file("winequality-red.csv"), sep=";")
    assert {"alcohol", "volatile acidity", "quality"}.issubset(wine.columns)
    assert wine["quality"].between(0, 10).all()

    wholesale = pd.read_csv(require_file("wholesale_customers.csv"))
    assert {"Fresh", "Milk", "Grocery"}.issubset(wholesale.columns)
    assert len(wholesale) > 100
