# Solutions — databases and SQL

Worked answers to the exercises in [`README.md`](README.md) and at the end of each notebook. SQL
is shown for SQLite; connect first with:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd().parent))
from load import build_database, DEFAULT_DB
from ds_practice import connect_sqlite, query
from ds_practice.paths import data_path

db_path = data_path(DEFAULT_DB)
if not db_path.exists():
    db_path = build_database()
conn = connect_sqlite(db_path)
```

## Notebook 01 — DDL, keys, and constraints

### 1. Add an index on `airports (name)`

```python
import sqlite3
from load import SCHEMA_PATH

scratch = sqlite3.connect(":memory:")
scratch.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
scratch.execute("CREATE INDEX idx_airports_name ON airports (name)")
print([row[1] for row in scratch.execute("PRAGMA index_list('airports')")])
```

The list includes `idx_airports_name` alongside the automatically created primary-key index.

### 2. A `CHECK` range

```python
scratch = sqlite3.connect(":memory:")
scratch.execute("""
    CREATE TABLE measurements (
        id INTEGER PRIMARY KEY,
        flipper_mm INTEGER NOT NULL CHECK (flipper_mm BETWEEN 100 AND 400)
    )
""")
for value in (190, 217, 999):
    try:
        scratch.execute("INSERT INTO measurements (flipper_mm) VALUES (?)", (value,))
        print("accepted", value)
    except sqlite3.IntegrityError as exc:
        print("rejected", value, "-", exc)
```

`190` and `217` are stored; `999` raises `IntegrityError` because it violates the `CHECK`.

### 3. `DROP TABLE` versus `DELETE FROM`

`DELETE FROM` removes rows but keeps the table, its columns, constraints, and indexes.
`DROP TABLE` removes the table itself. Both are shown below.

```python
scratch = sqlite3.connect(":memory:")
scratch.execute("CREATE TABLE demo (id INTEGER PRIMARY KEY, label TEXT)")
scratch.executemany("INSERT INTO demo (label) VALUES (?)", [("a",), ("b",)])
scratch.execute("DELETE FROM demo")
print("after DELETE, table still there:", scratch.execute(
    "SELECT COUNT(*) FROM sqlite_master WHERE name='demo'").fetchone()[0] == 1)
scratch.execute("DROP TABLE demo")
print("after DROP, table gone:", scratch.execute(
    "SELECT COUNT(*) FROM sqlite_master WHERE name='demo'").fetchone()[0] == 0)
```

## Notebook 02 — Filtering and aggregation

### 1. Active European airlines

```sql
SELECT co.name AS country, COUNT(*) AS active_airlines
FROM airlines al
JOIN countries co ON co.country_id = al.country_id
WHERE al.active = 'Y'
GROUP BY co.country_id
HAVING COUNT(*) >= 5
ORDER BY active_airlines DESC;
```

### 2. Ten longest names containing "International"

```sql
SELECT name, LENGTH(name) AS len
FROM airports
WHERE name LIKE '%International%'
ORDER BY len DESC
LIMIT 10;
```

### 3. Services per airport

```sql
SELECT a.name, COUNT(*) AS departures, COUNT(DISTINCT r.destination_airport_id) AS destinations
FROM routes r
JOIN airports a ON a.airport_id = r.source_airport_id
GROUP BY a.airport_id
ORDER BY departures DESC
LIMIT 5;
```

`COUNT(*)` counts route rows, and the same destination can be served by several airlines, so it is
usually larger than `COUNT(DISTINCT destination_airport_id)`, which counts unique places reached.

## Notebook 03 — Joins, subqueries, and CTEs

### 1. Top countries by departing routes

```sql
SELECT co.name AS country, COUNT(*) AS departures
FROM routes r
JOIN airports a   ON a.airport_id = r.source_airport_id
JOIN cities c     ON c.city_id = a.city_id
JOIN countries co ON co.country_id = c.country_id
GROUP BY co.country_id
ORDER BY departures DESC
LIMIT 10;
```

### 2. Airports with no departing route

```sql
SELECT a.name
FROM airports a
LEFT JOIN routes r ON r.source_airport_id = a.airport_id
WHERE r.route_id IS NULL
LIMIT 5;
```

The filter must be in `WHERE`, not `ON`; putting it in `ON` would stop the left join from keeping
the unmatched airports.

### 3. CTE refactor

```sql
WITH departures AS (
    SELECT source_airport_id AS airport_id, COUNT(*) AS n
    FROM routes GROUP BY source_airport_id
)
SELECT a.name, d.n
FROM departures d JOIN airports a ON a.airport_id = d.airport_id
WHERE d.n > (SELECT AVG(n) FROM departures)
ORDER BY d.n DESC
LIMIT 5;
```

The CTE names the per-airport count once, so the threshold subquery and the final join both refer
to `departures` instead of repeating the aggregation.

## Notebook 04 — Views, procedures, and transactions

### 1. `v_routes_per_airline`

```python
conn.execute("DROP VIEW IF EXISTS v_routes_per_airline")
conn.execute("""
    CREATE VIEW v_routes_per_airline AS
    SELECT al.name AS airline, COUNT(*) AS routes
    FROM routes r
    JOIN airlines al ON al.airline_id = r.airline_id
    GROUP BY al.airline_id
""")
conn.commit()
display(query(conn, "SELECT * FROM v_routes_per_airline ORDER BY routes DESC LIMIT 5"))
```

### 2. Atomic country + city insert

```python
def add_country_with_city(db, country_id, country_name, city_name, bad_country_id=None):
    try:
        db.execute("BEGIN")
        db.execute("INSERT INTO countries (country_id, name) VALUES (?, ?)",
                   (country_id, country_name))
        # deliberately point at a country that does not exist
        taken = bad_country_id if bad_country_id is not None else country_id
        db.execute("INSERT INTO cities (name, country_id) VALUES (?, ?)", (city_name, taken))
        db.commit()
        print("committed")
    except Exception as exc:  # noqa: BLE001 - demonstration
        db.rollback()
        print("rolled back:", type(exc).__name__)

add_country_with_city(conn, 9100, "Neverland", "Capital", bad_country_id=424242)
print(query(conn, "SELECT COUNT(*) AS n FROM countries WHERE name='Neverland'").iloc[0, 0])
```

Because the city insert fails the foreign key, `rollback()` removes the country too; the final
count is `0`.

### 3. Trigger guard

```python
conn.executescript("""
    DROP TRIGGER IF EXISTS trg_altitude_guard;
    CREATE TRIGGER trg_altitude_guard BEFORE INSERT ON airports
    WHEN NEW.altitude < 0
    BEGIN
        SELECT RAISE(ABORT, 'altitude cannot be negative');
    END;
""")
```

Any insert with a negative altitude now aborts with the message instead of storing bad data.

## Notebook 05 — Window functions and performance

### 1. Top two airports per country

```sql
WITH ranked AS (
    SELECT
        a.name,
        co.name AS country,
        a.altitude,
        ROW_NUMBER() OVER (PARTITION BY co.country_id ORDER BY a.altitude DESC) AS rn
    FROM airports a
    JOIN cities c     ON c.city_id = a.city_id
    JOIN countries co ON co.country_id = c.country_id
)
SELECT country, name, altitude
FROM ranked
WHERE rn <= 2
ORDER BY country, rn;
```

### 2. Moving average of routes

```sql
WITH counts AS (
    SELECT al.name AS airline, COUNT(*) AS routes
    FROM routes r JOIN airlines al ON al.airline_id = r.airline_id
    GROUP BY al.airline_id
)
SELECT airline, routes,
       AVG(routes) OVER (ORDER BY routes DESC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS moving_avg
FROM counts
ORDER BY routes DESC
LIMIT 5;
```

### 3. Plan comparison

```sql
EXPLAIN QUERY PLAN
SELECT * FROM routes WHERE source_airport_id = 1234;
```

Before the index the plan reports a full scan of `routes`; after
`CREATE INDEX idx_routes_source ON routes (source_airport_id)` (already present in the schema) the
plan switches to an index search. An index is justified here because routes are looked up by
origin constantly, while the table is written only by the loader.
