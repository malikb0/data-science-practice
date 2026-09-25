# `src/ds_practice/` — shared helpers

The one place shared data-science code lives. Notebooks and scripts import this package so that
data loading, metric definitions, the plotting theme, and SQL access are defined once. Install it
in editable mode with `pip install -e .` (or `make install`).

## Inventory

| File | Contents |
|---|---|
| `__init__.py` | Re-exports the public API listed below |
| `paths.py` | `repo_root()`, `data_path()`, `require_data()` |
| `data.py` | Typed loaders for every dataset |
| `metrics.py` | `regression_metrics`, `classification_metrics`, `adjusted_r2` |
| `seeding.py` | `set_seed(seed=42)` |
| `sql.py` | `connect_sqlite()`, `query()` |
| `viz.py` | `set_theme()` and `histogram`/`barplot`/`scatterplot`/`lineplot`/`boxplot` |

## Public API

```python
from ds_practice import (
    # data
    load_penguins, load_books, load_airports, load_airlines, load_routes,
    load_california, load_gapminder, load_usgs_quakes,
    load_uci_adult, load_wine, load_wholesale,
    # metrics
    regression_metrics, classification_metrics, adjusted_r2,
    # utilities
    set_seed, connect_sqlite, query, set_theme,
    histogram, barplot, scatterplot, lineplot, boxplot,
)
```

## How to read it

Start with `paths.py`, which decides where the repository root and `data/raw/` are. `data.py`
builds on it with one function per dataset; each raises a clear `FileNotFoundError` naming the
download command if the file is absent. `metrics.py` and `viz.py` are deliberately small so their
definitions are easy to audit.

## How to run it

```bash
make install
python scripts/download_data.py --module 03
python -c "from ds_practice import load_penguins; print(load_penguins().shape)"
```

The package never downloads data and never imports a notebook, so it is safe to import in tests.
