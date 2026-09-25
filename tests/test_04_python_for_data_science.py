"""Module 04 — Python fundamentals: smoke-test the packaged helpers and the data contract."""
import pytest

from helpers import load_module, require_file

pyutils = load_module("04-python-for-data-science/pyutils.py", "pyutils")

ROWS = [
    {"species": "Adelie", "mass_g": 3750},
    {"species": "Gentoo", "mass_g": 5000},
    {"species": "Chinstrap", "mass_g": 3200},
]


def test_mass_band_boundaries():
    assert pyutils.mass_band(3499) == "light"
    assert pyutils.mass_band(3500) == "medium"
    assert pyutils.mass_band(4499) == "medium"
    assert pyutils.mass_band(4500) == "heavy"


def test_summarise_returns_expected_shape():
    result = pyutils.summarise([1, 2, 3, 4])
    assert result == {"n": 4, "mean": 2.5, "min": 1, "max": 4}
    with pytest.raises(ValueError):
        pyutils.summarise([])


def test_band_counts():
    assert pyutils.band_counts(ROWS) == {"medium": 1, "heavy": 1, "light": 1}


def test_penguins_data_contract():
    import pandas as pd

    frame = pd.read_csv(require_file("penguins.csv"))
    assert {"species", "island", "body_mass_g"}.issubset(frame.columns)
    assert frame.shape[1] >= 7
    assert not frame["species"].isna().all()
