"""Module 03 — CRISP-DM on Palmer Penguins.

The data-contract test verifies the fetched file; the smoke test re-derives a
simple species classifier and checks it beats the majority baseline.
"""
import numpy as np
import pandas as pd
import pytest

from helpers import require_file

FEATURES = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]


@pytest.fixture(scope="module")
def penguins():
    return pd.read_csv(require_file("penguins.csv"))


def test_data_contract(penguins):
    assert len(penguins) >= 300
    for column in ("species", "island", *FEATURES):
        assert column in penguins.columns
    clean = penguins.dropna(subset=FEATURES)
    assert set(clean["species"]) == {"Adelie", "Chinstrap", "Gentoo"}
    assert clean["body_mass_g"].between(2500, 6500).all()
    assert clean["bill_length_mm"].between(30, 65).all()


def test_species_classifier_beats_baseline(penguins):
    sklearn = pytest.importorskip("sklearn")
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier

    clean = penguins.dropna(subset=FEATURES)
    X = clean[FEATURES].to_numpy()
    y = clean["species"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = DecisionTreeClassifier(max_depth=2, random_state=42).fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    baseline = accuracy_score(y_test, np.full_like(y_test, pd.Series(y).mode()[0]))
    assert accuracy > baseline
    assert accuracy > 0.9
    assert sklearn.__version__
