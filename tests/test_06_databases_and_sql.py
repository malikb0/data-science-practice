"""Module 06 — schema/ETL smoke tests and the OpenFlights data contract."""
import sqlite3
from pathlib import Path

import pandas as pd

from helpers import load_module, require_file

ROOT = Path(__file__).resolve().parent.parent
sql_load = load_module("06-databases-and-sql/load.py", "sql_load")

AIRPORTS = (
    '1,"Keflavik","Reykjavik","Iceland","KEF","BIKF",63.985,-22.605,171,0,"N",'
    '"Atlantic/Reykjavik","airport","OurAirports"\n'
    '2,"Heathrow","London","United Kingdom","LHR","EGLL",51.470,-0.460,83,0,"E",'
    '"Europe/London","airport","OurAirports"\n'
    '3,"Charles de Gaulle","Paris","France","CDG","LFPG",49.010,2.550,392,1,"E",'
    '"Europe/Paris","airport","OurAirports"\n'
)
AIRLINES = (
    '1,"Icelandair",\\N,"FI","ICE","ICEAIR","Iceland","Y"\n'
    '2,"British Airways",\\N,"BA","BAW","SPEEDBIRD","United Kingdom","Y"\n'
)
ROUTES = (
    "FI,1,KEF,1,LHR,2,,0,757\n"
    "BA,2,LHR,2,CDG,3,,0,320\n"
)


def _write_sources(tmp_path: Path) -> None:
    (tmp_path / "airports.dat").write_text(AIRPORTS, encoding="utf-8")
    (tmp_path / "airlines.dat").write_text(AIRLINES, encoding="utf-8")
    (tmp_path / "routes.dat").write_text(ROUTES, encoding="utf-8")


def test_build_database_creates_normalised_tables(tmp_path):
    _write_sources(tmp_path)
    db_path = sql_load.build_database(db_path=tmp_path / "flights.db", data_dir=tmp_path)
    assert db_path.exists()

    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"countries", "cities", "airports", "airlines", "routes"}.issubset(tables)
    assert conn.execute("SELECT COUNT(*) FROM airports").fetchone()[0] == 3
    assert conn.execute("SELECT COUNT(*) FROM countries").fetchone()[0] == 3
    # only routes whose endpoints exist are kept
    assert conn.execute("SELECT COUNT(*) FROM routes").fetchone()[0] == 2
    conn.close()


def test_route_details_view_joins_names(tmp_path):
    _write_sources(tmp_path)
    db_path = sql_load.build_database(db_path=tmp_path / "flights.db", data_dir=tmp_path)
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT airline, source_iata, destination_iata FROM v_route_details").fetchall()
    assert ("Icelandair", "KEF", "LHR") in rows
    conn.close()


def test_schema_declares_constraints_and_indexes():
    text = (ROOT / "06-databases-and-sql" / "schema.sql").read_text(encoding="utf-8")
    for token in ["PRIMARY KEY", "REFERENCES", "UNIQUE", "CHECK", "CREATE INDEX", "CREATE VIEW"]:
        assert token in text


def test_openflights_data_contract():
    from ds_practice.data import AIRPORT_COLUMNS

    frame = pd.read_csv(
        require_file("airports.dat"), header=None, names=AIRPORT_COLUMNS, na_values=[r"\N"]
    )
    assert {"airport_id", "name", "country", "latitude", "longitude"}.issubset(frame.columns)
    assert len(frame) > 100
    assert frame["latitude"].between(-90, 90).all()
    assert frame["longitude"].between(-180, 180).all()
