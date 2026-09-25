-- Normalised schema for the OpenFlights data (SQLite dialect).
-- Keys, constraints, and indexes are intentional; see docs/erd-module-06.md.

PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS v_route_details;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS airports;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    country_id  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE
);

CREATE TABLE cities (
    city_id     INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    country_id  INTEGER NOT NULL REFERENCES countries (country_id),
    UNIQUE (name, country_id)
);

CREATE TABLE airports (
    airport_id       INTEGER PRIMARY KEY,           -- from the source file
    name             TEXT    NOT NULL,
    city_id          INTEGER REFERENCES cities (city_id),
    iata             TEXT,
    icao             TEXT,
    latitude         REAL    CHECK (latitude  BETWEEN -90  AND 90),
    longitude        REAL    CHECK (longitude BETWEEN -180 AND 180),
    altitude         REAL,
    timezone_offset  REAL,
    dst              TEXT,
    tz_database      TEXT,
    type             TEXT,
    source           TEXT
);

CREATE TABLE airlines (
    airline_id  INTEGER PRIMARY KEY,                 -- from the source file
    name        TEXT    NOT NULL,
    alias       TEXT,
    iata        TEXT,
    icao        TEXT,
    callsign    TEXT,
    country_id  INTEGER REFERENCES countries (country_id),
    active      TEXT    CHECK (active IN ('Y', 'N') OR active IS NULL)
);

CREATE TABLE routes (
    route_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    airline_id              INTEGER REFERENCES airlines (airline_id),
    source_airport_id       INTEGER NOT NULL REFERENCES airports (airport_id),
    destination_airport_id  INTEGER NOT NULL REFERENCES airports (airport_id),
    codeshare               TEXT,
    stops                   INTEGER NOT NULL DEFAULT 0 CHECK (stops >= 0),
    equipment               TEXT,
    UNIQUE (airline_id, source_airport_id, destination_airport_id)
);

CREATE INDEX idx_airports_iata        ON airports (iata);
CREATE INDEX idx_airports_city        ON airports (city_id);
CREATE INDEX idx_cities_country       ON cities (country_id);
CREATE INDEX idx_airlines_country     ON airlines (country_id);
CREATE INDEX idx_routes_airline       ON routes (airline_id);
CREATE INDEX idx_routes_source        ON routes (source_airport_id);
CREATE INDEX idx_routes_destination   ON routes (destination_airport_id);

CREATE VIEW v_route_details AS
SELECT
    r.route_id,
    al.name            AS airline,
    src.name           AS source_airport,
    src.iata           AS source_iata,
    dst.name           AS destination_airport,
    dst.iata           AS destination_iata,
    r.stops,
    r.equipment
FROM routes r
LEFT JOIN airlines al ON al.airline_id = r.airline_id
LEFT JOIN airports src ON src.airport_id = r.source_airport_id
LEFT JOIN airports dst ON dst.airport_id = r.destination_airport_id;
