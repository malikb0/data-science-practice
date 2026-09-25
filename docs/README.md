# Documentation

Supplementary notes for the **Data Science Practice** portfolio. Start with the root
[`README.md`](../README.md) for the project overview and quickstart.

| Document | What it covers |
|---|---|
| [`course-map.md`](course-map.md) | The certificate skill areas mapped to the original projects in this repo |
| [`datasets.md`](datasets.md) | Every dataset: source URL, license, citation, and fetch command |
| [`methodology.md`](methodology.md) | How the projects were built and how results are kept reproducible |

## Conventions used across the repo

- One folder per skill area (`01-…` … `09-…`), each with a `README.md`, a `notebooks/`
  directory, and an entry in `tests/`.
- Datasets are **never committed**. `scripts/download_data.py` fetches and caches them.
- Notebooks that need data load it from `data/raw/` and fail with a clear message pointing at
  the download command rather than silently inventing values.
- Every number quoted in a README is produced by the notebook or test it refers to.
