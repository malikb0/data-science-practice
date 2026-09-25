# Data dictionary

Every dataset used in this portfolio, with field names, types, units, and provenance. All files
are downloaded into `data/raw/` (git-ignored) by `scripts/download_data.py`. Licenses and
citations are in [`datasets.md`](datasets.md).

Legend: `int` = integer, `float` = decimal number, `str` = text, `bool` = true/false,
`category` = a small set of labels.

## 1. Palmer Penguins — `penguins.csv`

Source: [allisonhorst/palmerpenguins](https://github.com/allisonhorst/palmerpenguins) (CC0).
Used by modules 03 and 04. One row per measured penguin.

| Field | Type | Units | Description |
|---|---|---|---|
| `species` | category | — | Adelie, Chinstrap, or Gentoo |
| `island` | category | — | Island of the observation (Biscoe, Dream, Torgersen) |
| `bill_length_mm` | float | millimetres | Bill length |
| `bill_depth_mm` | float | millimetres | Bill depth |
| `flipper_length_mm` | int | millimetres | Flipper length |
| `body_mass_g` | int | grams | Body mass |
| `sex` | category | — | female / male (some missing) |
| `year` | int | year | Study year (2007–2009) |

Missing values occur in `bill_*`, `flipper_length_mm`, `body_mass_g`, and `sex`.

## 2. books.toscrape.com — `books.csv`

Source: [books.toscrape.com](http://books.toscrape.com/) (public scraping sandbox). Scraped by
module 05. One row per book on the first five catalogue pages.

| Field | Type | Units | Description |
|---|---|---|---|
| `title` | str | — | Book title |
| `price_gbp` | float | GBP (£) | Listed price |
| `rating` | int | stars (1–5) | Star rating |
| `in_stock` | bool | — | Whether the listing says "In stock" |
| `url` | str | — | Absolute product URL |

## 3. OpenFlights — `airports.dat`, `airlines.dat`, `routes.dat`

Source: [OpenFlights](https://openflights.org/data) (ODbL). Module 06. Three related tables; the
module normalises them into SQLite.

`airports.dat` — one row per airport.

| Field | Type | Units | Description |
|---|---|---|---|
| `airport_id` | int | — | OpenFlights primary key |
| `name` | str | — | Airport name |
| `city` | str | — | City served |
| `country` | str | — | Country |
| `iata` | str | — | 3-letter IATA code |
| `icao` | str | — | 4-letter ICAO code |
| `latitude` | float | degrees | Decimal latitude |
| `longitude` | float | degrees | Decimal longitude |
| `altitude` | float | feet | Altitude above sea level |
| `timezone_offset` | float | hours | UTC offset |
| `dst` | str | — | Daylight-saving rule |
| `tz_database` | str | — | Olson time-zone name |
| `type` | str | — | Airport type |
| `source` | str | — | Data source tag |

`airlines.dat` — one row per airline.

| Field | Type | Units | Description |
|---|---|---|---|
| `airline_id` | int | — | OpenFlights primary key |
| `name` | str | — | Airline name |
| `alias` | str | — | Alternative name |
| `iata` | str | — | 2-letter IATA code |
| `icao` | str | — | 3-letter ICAO code |
| `callsign` | str | — | Radio callsign |
| `country` | str | — | Country of registration |
| `active` | str | — | `Y`/`N` active status |

`routes.dat` — one row per route segment.

| Field | Type | Units | Description |
|---|---|---|---|
| `airline` | str | — | Airline IATA/ICAO code |
| `airline_id` | int | — | FK to `airlines.airline_id` |
| `source_airport` | str | — | Origin airport code |
| `source_airport_id` | int | — | FK to `airports.airport_id` |
| `destination_airport` | str | — | Destination airport code |
| `destination_airport_id` | int | — | FK to `airports.airport_id` |
| `codeshare` | str | — | Code-share flag |
| `stops` | int | — | Number of stops |
| `equipment` | str | — | Aircraft types |

## 4. California Housing — `california_housing.csv`

Source: scikit-learn `fetch_california_housing` (public / BSD-documented). Module 07. One row per
census block group.

| Field | Type | Units | Description |
|---|---|---|---|
| `MedInc` | float | tens of thousands of USD | Median block-group income |
| `HouseAge` | float | years | Median house age |
| `AveRooms` | float | rooms | Average rooms per household |
| `AveBedrms` | float | rooms | Average bedrooms per household |
| `Population` | float | people | Block-group population |
| `AveOccup` | float | people | Average household occupancy |
| `Latitude` | float | degrees | Block-group latitude |
| `Longitude` | float | degrees | Block-group longitude |
| `MedHouseVal` | float | hundreds of thousands of USD | Median house value (target) |

## 5. Gapminder — `gapminder.csv`

Source: [plotly datasets](https://github.com/plotly/datasets) (CC BY 4.0). Module 08. One row
per country per five-year period.

| Field | Type | Units | Description |
|---|---|---|---|
| `country` | str | — | Country name |
| `continent` | category | — | Continent |
| `year` | int | year | Observation year |
| `lifeExp` | float | years | Life expectancy at birth |
| `pop` | int | people | Population |
| `gdpPercap` | float | USD | GDP per capita |

## 6. USGS earthquakes — `usgs_quakes.csv`

Source: [earthquake.usgs.gov](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv)
(public domain). Module 08. One row per earthquake in the last 30 days.

| Field | Type | Units | Description |
|---|---|---|---|
| `time` | str (ISO 8601) | — | Origin time |
| `latitude`, `longitude` | float | degrees | Epicentre |
| `depth` | float | kilometres | Depth |
| `mag` | float | magnitude | Magnitude |
| `magType` | str | — | Magnitude scale |
| `place` | str | — | Human-readable location |
| `id` | str | — | Event identifier |
| `type` | str | — | Event type (mostly `earthquake`) |
| `status` | str | — | Review status |

Additional quality columns (`nst`, `gap`, `dmin`, `rms`, `net`, `updated`, errors, sources) are
retained in the raw file and documented on the USGS page.

## 7. UCI Adult Income — `adult.data`

Source: [UCI Adult](https://archive.ics.uci.edu/dataset/2/adult) (CC BY 4.0). Module 09. One row
per person. Columns are named on load by `ds_practice.load_uci_adult`.

| Field | Type | Units | Description |
|---|---|---|---|
| `age` | int | years | Age |
| `workclass` | category | — | Employment type |
| `fnlwgt` | int | — | Census sampling weight |
| `education` | category | — | Highest education level |
| `education_num` | int | — | Education as an ordinal number |
| `marital_status` | category | — | Marital status |
| `occupation` | category | — | Occupation |
| `relationship` | category | — | Household relationship |
| `race` | category | — | Race |
| `sex` | category | — | Sex |
| `capital_gain` | int | USD | Capital gains |
| `capital_loss` | int | USD | Capital losses |
| `hours_per_week` | int | hours | Weekly working hours |
| `native_country` | category | — | Country of origin |
| `income` | category | — | `<=50K` or `>50K` (target) |

## 8. UCI Wine Quality (red) — `winequality-red.csv`

Source: [UCI Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality) (CC BY 4.0).
Module 09. One row per wine sample (`;`-separated).

| Field | Type | Units | Description |
|---|---|---|---|
| `fixed acidity` | float | g/L | Non-volatile acids |
| `volatile acidity` | float | g/L | Acetic acid |
| `citric acid` | float | g/L | Citric acid |
| `residual sugar` | float | g/L | Sugar after fermentation |
| `chlorides` | float | g/L | Salt |
| `free sulfur dioxide` | float | mg/L | Free SO₂ |
| `total sulfur dioxide` | float | mg/L | Total SO₂ |
| `density` | float | g/mL | Density |
| `pH` | float | pH | Acidity |
| `sulphates` | float | g/L | Sulphates |
| `alcohol` | float | % vol | Alcohol content |
| `quality` | int | score (0–10) | Sensory quality (target) |

## 9. UCI Wholesale Customers — `wholesale_customers.csv`

Source: [UCI Wholesale customers](https://archive.ics.uci.edu/dataset/292/wholesale+customers)
(CC BY 4.0). Module 09. One row per customer; spend in monetary units.

| Field | Type | Units | Description |
|---|---|---|---|
| `Channel` | int | — | 1 = Horeca, 2 = Retail (semicolon-delimited in raw) |
| `Region` | int | — | 1 = Lisbon, 2 = Oporto, 3 = Other |
| `Fresh` | int | m.u. | Fresh products |
| `Milk` | int | m.u. | Milk products |
| `Grocery` | int | m.u. | Grocery products |
| `Frozen` | int | m.u. | Frozen products |
| `Detergents_Paper` | int | m.u. | Detergents and paper |
| `Delicassen` | int | m.u. | Delicatessen products |
