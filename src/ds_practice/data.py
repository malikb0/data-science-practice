"""Typed loaders for every dataset used in the portfolio.

Each loader raises ``FileNotFoundError`` with a fetch hint when the raw file is
missing, so notebooks fail clearly instead of silently.
"""
from __future__ import annotations

import pandas as pd

from ds_practice.paths import require_data

AIRPORT_COLUMNS = [
    "airport_id", "name", "city", "country", "iata", "icao",
    "latitude", "longitude", "altitude", "timezone_offset", "dst",
    "tz_database", "type", "source",
]

AIRLINE_COLUMNS = [
    "airline_id", "name", "alias", "iata", "icao", "callsign",
    "country", "active",
]

ROUTE_COLUMNS = [
    "airline", "airline_id", "source_airport", "source_airport_id",
    "destination_airport", "destination_airport_id", "codeshare", "stops",
    "equipment", "price",
]

ADULT_COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country",
    "income",
]


def load_penguins() -> pd.DataFrame:
    """Palmer Penguins measurements (CC0). Modules 03 and 04."""
    return pd.read_csv(require_data("penguins.csv"))


def load_books() -> pd.DataFrame:
    """Scraped books.toscrape.com catalogue. Module 05."""
    return pd.read_csv(require_data("books.csv"))


def load_airports() -> pd.DataFrame:
    """OpenFlights airports (ODbL). Module 06."""
    return pd.read_csv(
        require_data("airports.dat"), header=None, names=AIRPORT_COLUMNS,
        na_values=[r"\N"], keep_default_na=True,
    )


def load_airlines() -> pd.DataFrame:
    """OpenFlights airlines (ODbL). Module 06."""
    return pd.read_csv(
        require_data("airlines.dat"), header=None, names=AIRLINE_COLUMNS,
        na_values=[r"\N"], keep_default_na=True,
    )


def load_routes() -> pd.DataFrame:
    """OpenFlights routes (ODbL). Module 06."""
    return pd.read_csv(
        require_data("routes.dat"), header=None, names=ROUTE_COLUMNS,
        na_values=[r"\N"], keep_default_na=True,
    )


def load_california() -> pd.DataFrame:
    """California Housing (public, via scikit-learn). Module 07."""
    return pd.read_csv(require_data("california_housing.csv"))


def load_gapminder() -> pd.DataFrame:
    """Gapminder five-year panel (CC BY 4.0). Module 08."""
    return pd.read_csv(require_data("gapminder.csv"))


def load_usgs_quakes() -> pd.DataFrame:
    """USGS all-month earthquakes (public domain). Module 08."""
    return pd.read_csv(require_data("usgs_quakes.csv"))


def load_uci_adult() -> pd.DataFrame:
    """UCI Adult income (CC BY 4.0). Module 09."""
    return pd.read_csv(
        require_data("adult.data"), header=None, names=ADULT_COLUMNS,
        skipinitialspace=True, na_values="?",
    )


def load_wine() -> pd.DataFrame:
    """UCI red wine quality (CC BY 4.0). Module 09."""
    return pd.read_csv(require_data("winequality-red.csv"), sep=";")


def load_wholesale() -> pd.DataFrame:
    """UCI wholesale customers (CC BY 4.0). Module 09."""
    return pd.read_csv(require_data("wholesale_customers.csv"))
