# 06 — Databases and SQL

Relational databases are where most organisational data actually lives. This module designs a
**normalised schema** for the OpenFlights dataset, loads it into SQLite, and then teaches the SQL
needed to ask questions of it — from constraints and filtering through joins, views, transactions,
window functions, and query tuning.

**Dataset:** OpenFlights airports, airlines, and routes (ODbL). Fetch and build it with:

```bash
python scripts/download_data.py --module 06
python 06-databases-and-sql/load.py
```

The schema and the entity-relationship diagram are in [`schema.sql`](schema.sql) and
[`docs/erd-module-06.md`](../docs/erd-module-06.md).

## Learning objectives

By the end of this module you will be able to:

- model related tables with primary keys, foreign keys, and normalisation;
- write DDL that enforces uniqueness, required values, and valid ranges;
- filter, sort, and aggregate with `WHERE`, `GROUP BY`, and `HAVING`;
- combine tables with inner, left, and self joins, subqueries, and CTEs;
- wrap complex reads in views and multi-step writes in transactions;
- rank and accumulate with window functions;
- read `EXPLAIN QUERY PLAN` and justify an index.

## Prerequisites

- Module [`04-python-for-data-science`](../04-python-for-data-science/README.md) for Python and
  pandas basics.
- Module [`05-python-project`](../05-python-project/README.md) for turning raw files into a
  dataset you can trust.
- Basic familiarity with the idea of a table, a row, and a column; no prior SQL required.

## Dataset

OpenFlights publishes three pipe-and-comma separated files:

| File | Rows (approx.) | One row per |
|---|---|---|
| `airports.dat` | 7,700+ | airport |
| `airlines.dat` | 6,100+ | airline |
| `routes.dat` | 67,000+ | route segment between two airports |

The source is [openflights.org/data](https://openflights.org/data), released under the **Open
Database License (ODbL) 1.0**. Full provenance and citation are in
[`docs/datasets.md`](../docs/datasets.md) and field definitions in
[`docs/data-dictionary.md`](../docs/data-dictionary.md). The loader normalises the flat files into
`countries`, `cities`, `airports`, `airlines`, and `routes` inside `data/raw/flights.db`.

## Topics covered

| Notebook | Topic |
|---|---|
| [`notebooks/01-ddl-and-constraints.ipynb`](notebooks/01-ddl-and-constraints.ipynb) | `CREATE`/`ALTER`/`DROP`, keys, `UNIQUE`/`CHECK`/`NOT NULL`, indexes |
| [`notebooks/02-filtering-and-aggregation.ipynb`](notebooks/02-filtering-and-aggregation.ipynb) | `WHERE`, `LIKE`, `ORDER BY`, `GROUP BY`, `HAVING`, aggregates |
| [`notebooks/03-joins-and-subqueries.ipynb`](notebooks/03-joins-and-subqueries.ipynb) | inner/left/self joins, subqueries, CTEs |
| [`notebooks/04-views-procedures-transactions.ipynb`](notebooks/04-views-procedures-transactions.ipynb) | views, procedures, ACID, triggers |
| [`notebooks/05-window-functions-and-performance.ipynb`](notebooks/05-window-functions-and-performance.ipynb) | window functions, query plans, index tuning |

The plain-language explainer is [`concepts.md`](concepts.md); worked answers are in
[`solutions.md`](solutions.md).

## How to run

```bash
make install
python scripts/download_data.py --module 06
python 06-databases-and-sql/load.py
jupyter lab 06-databases-and-sql/notebooks/
```

The notebooks connect through `ds_practice.connect_sqlite()` and run top to bottom once
`data/raw/flights.db` exists. Notebook 01 works on an in-memory copy and needs no data; the loader
recreates the database from scratch on every run, so it is safe to repeat.

## Exercises

1. **DDL.** Add an index on `airports (name)`, then write a `measurements` table with a `CHECK`
   that rejects out-of-range flipper lengths and show which insert fails.
2. **Filtering.** Count active airlines per country with at least five active carriers; list the
   ten longest airport names containing "International".
3. **Joins.** Find the top ten countries by departing routes, five airports that never depart a
   route, and refactor a subquery into a CTE.
4. **Views and transactions.** Build a `v_routes_per_airline` view and an atomic Python procedure
   that rolls back a country if its city fails a foreign-key check.
5. **Windows and performance.** Return the two highest airports per country, compute a moving
   average of routes, and compare `EXPLAIN QUERY PLAN` before and after adding an index.

## Limitations

The module uses SQLite, which is wonderfully portable but weaker than a server database: it does
not enforce column types strictly, has no stored procedures, and cannot drop individual
constraints. The queries describe a published snapshot of schedules rather than live traffic, and
performance advice is measured on one machine. Normalisation is shown at a level appropriate for
learning; a production schema would add audit columns, foreign-key enforcement at the application
boundary, and careful handling of the many OpenFlights rows with missing IATA codes.
