# `tests/` — offline-safe test suite

Per-module tests that act as data contracts and smoke checks. They skip rather than fail when a
dataset or optional dependency is unavailable, so CI stays green on a clean checkout.

## Inventory

| File | Covers |
|---|---|
| `conftest.py` | Adds the repository, `tests/`, and `src/` to `sys.path` |
| `helpers.py` | `require_file` (skip if data absent), `load_module`, notebook readers |
| `test_01_what_is_data_science.py` | Module 01 content checks |
| `test_02_tools.py` | Module 02 smoke tests |
| `test_03_methodology.py` | Penguins data contract and tree smoke test |
| `test_04_python_for_data_science.py` | `pyutils` helpers and Penguins contract |
| `test_05_python_project.py` | Scraper parsing and dashboard builders |
| `test_06_databases_and_sql.py` | Schema/ETL smoke tests and OpenFlights contract |
| `test_07_data_analysis.py` | Feature engineering and model smoke tests |
| `test_08_data_visualization.py` | Chart builders and dashboard filters |
| `test_09_machine_learning.py` | Model factories and pipeline smoke tests |

## Two kinds of test

- **Data contract** — asserts columns, shape, and value ranges of a fetched dataset. It calls
  `require_file`, which `pytest.skip`s when the file is missing.
- **Smoke** — runs the module's core code path on small synthetic input, so it works offline. It
  uses `pytest.importorskip` for optional libraries such as Plotly or scikit-learn.

## How to run

```bash
make test                 # or: python -m pytest -q tests
python -m pytest -q tests/test_06_databases_and_sql.py
```

To exercise the data contracts, download the data first:
`python scripts/download_data.py --all`.
