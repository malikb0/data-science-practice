# Methodology

## Principles

1. **Original work.** Everything here is written from scratch. The datasets differ from any
   course dataset, and no third-party prose or code is copied.
2. **Every number is produced by code.** If a README quotes a figure, the notebook or test it
   refers to computes it. Nothing is estimated by hand.
3. **Reproducible.** Dependencies are pinned in `requirements.txt`; analysis and modelling
   notebooks seed their random generators; datasets are fetched by a single script.
4. **Offline-safe tests.** Tests that need downloaded data or the network *skip* rather than
   fail when it is unavailable, so CI stays green on a clean checkout.

## Project workflow

Each project follows the same lightweight workflow:

1. **Acquire** — `scripts/download_data.py` fetches the dataset and caches it under `data/raw/`.
2. **Inspect** — shape, dtypes, missing values, and basic ranges are checked before anything
   else.
3. **Transform** — only the transformations the question needs: type fixes, derived features,
   joins, or aggregation.
4. **Model / visualise** — the technique the project is about, with a held-out evaluation for
   anything predictive.
5. **Record limitations** — every module README ends with an honest limitations section.

## Reproducibility details

- **Versions** are pinned with `==` in `requirements.txt`; `make install` builds a virtualenv.
- **Seeds** — modelling and sampling code calls `numpy.random.default_rng(seed)` or sets
  `random_state=` explicitly. The value `42` is used consistently so runs are comparable.
- **Determinism** — notebooks run top to bottom with no hidden state; the tests re-derive the
  key quantities independently.
- **Data contracts** — each module ships a test asserting the schema and value ranges of its
  dataset. These act as change detectors if a publisher ever alters a file.

## Testing strategy

| Test type | Purpose | Offline behaviour |
|---|---|---|
| Data contract | Columns, shape, and value ranges of the fetched dataset | `pytest.skip` if data absent |
| Smoke | The module's core function or notebook logic runs end to end | `pytest.skip` if dependencies/data absent |
| Unit | Pure helper functions (parsing, scoring, cleaning) | Always runs |

`make test` is the single entry point, and `.github/workflows/ci.yml` runs the same command
after installing `requirements.txt`. Network-dependent paths are never required for CI.

## What this is not

This is a **portfolio of techniques on open data**, not a production system. Model results are
illustrative and are not tuned for deployment. See each module's *Limitations* section.
