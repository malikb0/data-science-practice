# `data/` — dataset cache

No data is committed to this repository. Datasets are downloaded on demand into `data/raw/`, which
is git-ignored, and loaded from there by `ds_practice`.

## Layout

| Path | Purpose |
|---|---|
| `raw/` | Downloaded source files (CSV and OpenFlights `.dat` files) |

`scripts/download_data.py` creates `raw/` and caches each file, reusing it unless `--force` is
passed. `data/raw/flights.db` (module 06) is built from the `.dat` files by
`06-databases-and-sql/load.py` and is also git-ignored.

## How to populate it

```bash
python scripts/download_data.py --all          # everything
python scripts/download_data.py --module 07    # just California Housing
```

## Files you should expect

| File | Dataset | Module |
|---|---|---|
| `penguins.csv` | Palmer Penguins | 03, 04 |
| `books.csv` | books.toscrape.com | 05 |
| `airports.dat`, `airlines.dat`, `routes.dat` | OpenFlights | 06 |
| `california_housing.csv` | California Housing | 07 |
| `gapminder.csv`, `usgs_quakes.csv` | Gapminder, USGS | 08 |
| `adult.data`, `winequality-red.csv`, `wholesale_customers.csv` | UCI | 09 |

Source URLs, licences, and citations are recorded in [`docs/datasets.md`](../docs/datasets.md) and
field definitions in [`docs/data-dictionary.md`](../docs/data-dictionary.md).

## How to read it

Open a file directly with pandas, or use the matching loader:

```python
from ds_practice import load_gapminder
frame = load_gapminder()
```
