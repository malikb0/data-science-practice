# Book dashboard

A small [Plotly Dash](https://dash.plotly.com/) app that explores the scraped
`books.toscrape.com` catalogue.

## Run

```bash
make install
python scripts/download_data.py --module 05      # creates data/raw/books.csv
python 05-python-project/app/dashboard.py       # serves http://127.0.0.1:8050
```

## What it shows

- A histogram of book prices.
- Mean price per star rating.
- A slider that filters the catalogue by minimum rating.

## Design notes

`load_books()` and the two figure builders are plain functions, so they can be tested without
starting a server (see `tests/test_05_python_project.py`). The app reads the raw CSV and derives
the `value` column at load time, keeping one source of truth.

## Limitations

The catalogue is static and fictional. The app is single-user and does not cache; for larger
data a real deployment would add an application server, caching, and tests of the callbacks.
