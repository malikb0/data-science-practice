"""Shared helpers for the data-science-practice portfolio.

Notebooks import from this package so that data loading, the plotting theme, and
the metric definitions live in exactly one place.
"""
from ds_practice.paths import data_path, repo_root, require_data
from ds_practice.data import (
    load_airlines,
    load_airports,
    load_books,
    load_california,
    load_gapminder,
    load_penguins,
    load_routes,
    load_uci_adult,
    load_usgs_quakes,
    load_wholesale,
    load_wine,
)
from ds_practice.metrics import (
    adjusted_r2,
    classification_metrics,
    regression_metrics,
)
from ds_practice.seeding import set_seed
from ds_practice.sql import connect_sqlite, query
from ds_practice.viz import (
    barplot,
    boxplot,
    histogram,
    lineplot,
    scatterplot,
    set_theme,
)

__version__ = "1.0.0"

__all__ = [
    "data_path",
    "repo_root",
    "require_data",
    "load_penguins",
    "load_books",
    "load_airports",
    "load_airlines",
    "load_routes",
    "load_california",
    "load_gapminder",
    "load_usgs_quakes",
    "load_uci_adult",
    "load_wine",
    "load_wholesale",
    "regression_metrics",
    "classification_metrics",
    "adjusted_r2",
    "set_seed",
    "connect_sqlite",
    "query",
    "set_theme",
    "histogram",
    "barplot",
    "scatterplot",
    "lineplot",
    "boxplot",
]
