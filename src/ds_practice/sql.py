"""Small SQLite helpers used by the databases module."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from ds_practice.paths import repo_root

DEFAULT_DB = "flights.db"


def connect_sqlite(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open (creating if needed) the project SQLite database."""
    path = Path(db_path) if db_path is not None else repo_root() / "data" / "raw" / DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)


def query(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> pd.DataFrame:
    """Run a read-only query and return a DataFrame."""
    return pd.read_sql_query(sql, conn, params=params)
