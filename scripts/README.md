# `scripts/` — repository tooling

Command-line helpers for fetching data and running notebooks.

## Inventory

| File | Purpose |
|---|---|
| `download_data.py` | Fetch and cache every dataset, or one module's dataset |
| `run_notebooks.py` | Execute offline-safe notebooks and print a pass/fail summary |

## `download_data.py`

```bash
python scripts/download_data.py --list          # show dataset keys
python scripts/download_data.py --module 06     # fetch one module's data
python scripts/download_data.py --all           # fetch everything
```

Each dataset has its own function, and files are cached under `data/raw/` (git-ignored) unless
`--force` is given. `--out DIR` overrides the cache location. Downloads are plain HTTP with a
descriptive user agent; the book scraper sleeps between requests.

## `run_notebooks.py`

```bash
python scripts/run_notebooks.py                 # offline-safe notebooks only
python scripts/run_notebooks.py 04-python-for-data-science
python scripts/run_notebooks.py --all           # include network notebooks
```

Notebooks whose dataset has not been downloaded, or that need the network, are skipped by default
so the command is safe on a clean checkout. This is the same entry point CI uses via `make nb`.

## How to read it

Both scripts are stdlib-first and avoid importing heavy libraries until needed. `download_data.py`
raises a helpful message and exits non-zero on a network failure rather than writing a partial
file.
