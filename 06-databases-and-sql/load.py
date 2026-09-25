#!/usr/bin/env python3
"""ETL the OpenFlights files into a normalised SQLite database.

Run directly::

    python scripts/download_data.py --module 06
    python 06-databases-and-sql/load.py

The loader is idempotent: it recreates the database from scratch each time.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from ds_practice.data import AIRLINE_COLUMNS, AIRPORT_COLUMNS, ROUTE_COLUMNS
from ds_practice.paths import repo_root

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEFAULT_DB = "flights.db"


def _read(path: Path, columns: list[str]) -> pd.DataFrame:
    return pd.read_csv(
        path, header=None, names=columns, na_values=[r"\N"], keep_default_na=True
    )


def _ids(conn: sqlite3.Connection, table: str, key: str, id_column: str) -> dict:
    """Return ``{key_value: id}`` for a lookup table."""
    return {
        row[0]: row[1]
        for row in conn.execute(f"SELECT {key}, {id_column} FROM {table}")
    }


def build_database(
    db_path: str | Path | None = None,
    data_dir: str | Path | None = None,
) -> Path:
    """(Re)build the SQLite database and return its path."""
    data_dir = Path(data_dir) if data_dir is not None else repo_root() / "data" / "raw"
    db_path = Path(db_path) if db_path is not None else data_dir / DEFAULT_DB
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.unlink(missing_ok=True)

    airports = _read(data_dir / "airports.dat", AIRPORT_COLUMNS)
    airlines = _read(data_dir / "airlines.dat", AIRLINE_COLUMNS)
    routes = _read(data_dir / "routes.dat", ROUTE_COLUMNS)

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        country_names = (
            pd.concat([airports["country"], airlines["country"]])
            .dropna().astype(str).str.strip()
            .replace("", pd.NA).dropna().drop_duplicates().sort_values()
        )
        conn.executemany(
            "INSERT INTO countries (name) VALUES (?)",
            [(name,) for name in country_names],
        )

        country_ids = _ids(conn, "countries", "name", "country_id")

        city_pairs = (
            airports[["city", "country"]].dropna()
            .assign(
                city=lambda d: d["city"].astype(str).str.strip(),
                country=lambda d: d["country"].astype(str).str.strip(),
            )
            .query("city != '' and country != ''")
            .drop_duplicates()
        )
        city_pairs["country_id"] = city_pairs["country"].map(country_ids)
        city_pairs = city_pairs.dropna(subset=["country_id"])
        conn.executemany(
            "INSERT INTO cities (name, country_id) VALUES (?, ?)",
            list(city_pairs[["city", "country_id"]].itertuples(index=False, name=None)),
        )
        city_ids = {
            (row[0], row[1]): row[2]
            for row in conn.execute(
                "SELECT c.name, co.name, c.city_id FROM cities c JOIN countries co USING (country_id)"
            )
        }

        airport_rows = []
        for row in airports.itertuples(index=False):
            city = None if pd.isna(row.city) else str(row.city).strip()
            country = None if pd.isna(row.country) else str(row.country).strip()
            airport_rows.append(
                (
                    int(row.airport_id), row.name,
                    city_ids.get((city, country)),
                    None if pd.isna(row.iata) else row.iata,
                    None if pd.isna(row.icao) else row.icao,
                    None if pd.isna(row.latitude) else float(row.latitude),
                    None if pd.isna(row.longitude) else float(row.longitude),
                    None if pd.isna(row.altitude) else float(row.altitude),
                    None if pd.isna(row.timezone_offset) else float(row.timezone_offset),
                    None if pd.isna(row.dst) else row.dst,
                    None if pd.isna(row.tz_database) else row.tz_database,
                    None if pd.isna(row.type) else row.type,
                    None if pd.isna(row.source) else row.source,
                )
            )
        conn.executemany(
            """INSERT INTO airports
               (airport_id, name, city_id, iata, icao, latitude, longitude, altitude,
                timezone_offset, dst, tz_database, type, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            airport_rows,
        )

        airline_rows = []
        for row in airlines.itertuples(index=False):
            country = None if pd.isna(row.country) else str(row.country).strip()
            airline_rows.append(
                (
                    int(row.airline_id), row.name,
                    None if pd.isna(row.alias) else row.alias,
                    None if pd.isna(row.iata) else row.iata,
                    None if pd.isna(row.icao) else row.icao,
                    None if pd.isna(row.callsign) else row.callsign,
                    country_ids.get(country),
                    None if pd.isna(row.active) else row.active,
                )
            )
        conn.executemany(
            """INSERT INTO airlines
               (airline_id, name, alias, iata, icao, callsign, country_id, active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            airline_rows,
        )

        valid_airports = {row[0] for row in conn.execute("SELECT airport_id FROM airports")}
        route_rows = []
        for row in routes.itertuples(index=False):
            if pd.isna(row.source_airport_id) or pd.isna(row.destination_airport_id):
                continue
            src, dst = int(row.source_airport_id), int(row.destination_airport_id)
            if src not in valid_airports or dst not in valid_airports:
                continue
            aid = None if pd.isna(row.airline_id) else int(row.airline_id)
            stops = 0 if pd.isna(row.stops) else int(row.stops)
            route_rows.append(
                (
                    aid, src, dst,
                    None if pd.isna(row.codeshare) else row.codeshare,
                    stops,
                    None if pd.isna(row.equipment) else row.equipment,
                )
            )
        conn.executemany(
            """INSERT OR IGNORE INTO routes
               (airline_id, source_airport_id, destination_airport_id, codeshare, stops, equipment)
               VALUES (?, ?, ?, ?, ?, ?)""",
            route_rows,
        )
        conn.commit()
    finally:
        conn.close()
    return db_path


def main() -> None:
    path = build_database()
    size = path.stat().st_size / 1_048_576
    print(f"built {path} ({size:.1f} MiB)")


if __name__ == "__main__":
    main()
