# Concepts — databases and SQL

A plain-language companion to the five notebooks. Read it before notebook 01 if terms such as
*primary key*, *join*, or *transaction* are new.

## The relational model

A relational database stores data in **tables**: a fixed set of named **columns**, each holding one
**type** of value, and any number of **rows**. Where a spreadsheet repeats a customer's name on
every order, a database stores the customer once and refers to it by an id. Splitting repeated
data out like this is **normalisation**, and it is what keeps updates consistent: change the
customer name in one place and every order follows.

A **primary key** is the column (or columns) that uniquely identifies a row. An **id** generated
by the database is the usual choice because it never changes. A **foreign key** is a column that
points at a primary key in another table; it is how relationships are represented. A route does
not repeat an airport's name, it stores `source_airport_id` and `destination_airport_id`.

## Constraints are promises

A **constraint** is a rule the database enforces on every write:

- `NOT NULL` — the value must be present;
- `UNIQUE` — no two rows may share the value;
- `PRIMARY KEY` — unique and not null;
- `FOREIGN KEY` — the value must exist in the referenced table;
- `CHECK` — the value must satisfy an expression, such as a latitude between -90 and 90;
- `DEFAULT` — a value used when none is supplied.

Pushing rules into the schema means every program that writes to the database inherits them,
instead of each one re-implementing validation.

## Reading data: the order of a query

SQL is written `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT`, but it
is evaluated differently:

1. `FROM` picks the table (and joins);
2. `WHERE` filters individual rows;
3. `GROUP BY` collects rows into groups;
4. aggregate functions collapse each group to one value;
5. `HAVING` filters groups;
6. `SELECT` projects columns;
7. `ORDER BY` sorts the result;
8. `LIMIT` trims it.

Because `WHERE` runs before grouping, an aggregate condition such as `COUNT(*) > 5` must go in
`HAVING`. This one fact explains most beginner errors.

## Joins

A join combines rows from two tables on a condition, normally equality of a shared key.

```sql
SELECT al.name, COUNT(*) AS routes
FROM routes r
JOIN airlines al ON al.airline_id = r.airline_id
GROUP BY al.airline_id;
```

An `INNER JOIN` keeps only matching pairs. A `LEFT JOIN` keeps every row from the left table and
fills missing right-hand values with `NULL`, which is how you find rows that have no match:

```sql
SELECT a.name
FROM airports a
LEFT JOIN routes r ON r.source_airport_id = a.airport_id
WHERE r.route_id IS NULL;   -- airports that never depart a route
```

Joining a table to itself (a **self join**) compares rows within one table, such as pairing an
origin and a destination.

## Subqueries and CTEs

A **subquery** is a query used inside another. It can be a value (`WHERE x > (SELECT AVG(...))`),
a table in `FROM`, or a test (`WHERE x IN (SELECT ...)`). A **common table expression** (CTE) is a
named subquery introduced with `WITH`, which lets a long query read top to bottom:

```sql
WITH departures AS (
    SELECT source_airport_id AS airport_id, COUNT(*) AS n
    FROM routes GROUP BY source_airport_id
)
SELECT a.name, d.n
FROM departures d JOIN airports a ON a.airport_id = d.airport_id;
```

## Views, procedures, transactions

A **view** is a stored query that behaves like a table. It hides a complicated join and can limit
which columns a reader sees. A **stored procedure** is a named block of logic kept in the
database; SQLite lacks them, so this module writes Python functions that run several statements
inside one transaction.

A **transaction** groups writes so they either all happen or none do:

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;      -- or ROLLBACK to undo both
```

Databases advertise **ACID**: atomicity (all-or-nothing), consistency (constraints hold),
isolation (concurrent transactions do not corrupt each other), and durability (committed data
survives a crash). A **trigger** is SQL that fires automatically on a write, useful for keeping a
derived value in step.

## Window functions

A window function computes across related rows while keeping every row. `PARTITION BY` restarts
the calculation within each group; `ORDER BY` orders rows inside the group.

```sql
SELECT
    name,
    altitude,
    RANK() OVER (PARTITION BY country_id ORDER BY altitude DESC) AS altitude_rank
FROM airports;
```

`ROW_NUMBER` always produces 1, 2, 3; `RANK` leaves gaps after ties; `DENSE_RANK` does not.
Aggregate windows (`SUM(...) OVER (ORDER BY ...)`) produce running totals, and a frame such as
`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` produces a moving average.

## Indexes and query plans

An **index** is a sorted structure that lets the database find rows without reading every one.
Primary keys are indexed automatically; `CREATE INDEX` adds one for another column. Indexes speed
up `WHERE`, `JOIN`, and `ORDER BY`, but every insert must update them, so they are a deliberate
trade-off.

`EXPLAIN QUERY PLAN` shows the steps SQLite will take. `SCAN table` means a full read;
`SEARCH table USING INDEX` means the index was used. Read the plan before adding indexes and
measure before believing a change helped.
