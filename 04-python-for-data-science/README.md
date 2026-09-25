# 04 — Python for data science

**Skill area:** the Python language as it is actually used in data work — built-in types and
containers, control flow, functions and classes, file and data I/O, the NumPy and pandas stack,
and talking to a JSON API over HTTP.

This module is the bridge between general programming and the analysis, visualisation, and
machine-learning modules that follow. It uses the Palmer Penguins table throughout so the focus
stays on the language rather than on a new domain.

## Learning objectives

After working through this module you will be able to:

- use Python's built-in types and choose between a `list`, `tuple`, `set`, and `dict`;
- write branching and looping code, and handle expected errors with `try` / `except`;
- define reusable functions (including `lambda`) and small classes with methods and properties;
- read and write CSV and JSON with both the standard library and pandas;
- work with NumPy arrays and pandas DataFrames using selection, filtering, `groupby`, and `merge`;
- call a JSON HTTP API with `requests`, paginate results, and fail gracefully when offline.

## Prerequisites

- Module [`02-tools-for-data-science`](../02-tools-for-data-science/README.md) for the
  Jupyter and virtual-environment setup.
- A Python 3.10+ environment with the repository requirements installed:

  ```bash
  make install
  ```

  This installs NumPy, pandas, matplotlib, seaborn, `requests`, and the `ds_practice` package in
  editable mode.
- No prior pandas or NumPy experience is assumed; no network is required for notebooks 01–04.

## Dataset

**Palmer Penguins (CC0).** Body measurements — bill length and depth, flipper length, body mass,
sex, year — for three species across three islands. It was introduced in
[`03-data-science-methodology`](../03-data-science-methodology/README.md) and is reused here.

Notebook 05 does not use the penguins data. It calls the public, key-free JSON API
`https://jsonplaceholder.typicode.com/posts`, paging with the `_page` and `_limit` query
parameters.

## Topics covered

| Notebook | Topics |
|---|---|
| [`notebooks/01-language-basics.ipynb`](notebooks/01-language-basics.ipynb) | Types; `list` / `tuple` / `set` / `dict`; conditionals; `for` / `while`; `try` / `except` |
| [`notebooks/02-functions-and-classes.ipynb`](notebooks/02-functions-and-classes.ipynb) | Functions and defaults; `*args` / `**kwargs`; lambdas; classes, properties, `__repr__` |
| [`notebooks/03-files-and-data-io.ipynb`](notebooks/03-files-and-data-io.ipynb) | `pathlib`; context managers; `csv` and `json`; pandas CSV/JSON round trips |
| [`notebooks/04-numpy-and-pandas.ipynb`](notebooks/04-numpy-and-pandas.ipynb) | ndarrays and vectorisation; boolean masks; DataFrames; `groupby`; `merge`; `pivot_table` |
| [`notebooks/05-apis-and-http.ipynb`](notebooks/05-apis-and-http.ipynb) | `requests`; query parameters; JSON parsing; pagination; error handling |

The module also ships [`pyutils.py`](pyutils.py), a small packaged example that shows what
happens when a teaching function graduates into reuse. It defines `mass_band(grams)`,
`summarise(values)`, and `band_counts(rows, mass_key="mass_g")`; the notebooks define their own
versions inline so you can see the reasoning, and the tests exercise the packaged ones. The
shared `ds_practice` package (installed with the repo) provides `load_penguins` and the plotting
helpers, so no notebook copies data-loading or plotting code.

## How to run

```bash
make install
python scripts/download_data.py --module 04
jupyter lab 04-python-for-data-science/notebooks/
```

Notebooks 01–04 run offline once `data/raw/penguins.csv` exists. Notebook 05 needs a network
connection; if the request fails it prints a clear message and skips the network-dependent cells
instead of raising an error.

## Exercises

Each notebook ends with its own short exercise set. The full worked solutions are in
[`solutions.md`](solutions.md).

1. **Language basics.** Count penguins per island with a plain `for` loop and a `dict`; build a
   `set` of species and a `tuple` range for flipper length; write `safe_mean` that returns `None`
   for an empty sequence.
2. **Functions and classes.** Parameterise `mass_band` with overridable thresholds; find the five
   longest flippers with a `lambda` sort key; extend `Penguin` with `is_gentoo` and `summary`.
3. **Files and data I/O.** Round-trip ten rows through the `csv` module; save and reload an
   island-count dictionary as JSON; write a Gentoo subset with pandas and read it back.
4. **NumPy and pandas.** Add a per-species z-score with `groupby().transform()`; count long
   flippers with a boolean mask; merge an island-to-region lookup and pivot the result.
5. **APIs and HTTP.** Fetch page 2 of the posts endpoint; write a `fetch_page` helper that
   retries; collect ten posts and find the busiest user.

## Limitations

The notebooks teach the language, not the whole language. Generators, decorators, context-manager
protocols, and type hints appear only in passing, and async I/O is out of scope. The examples fit
in memory; larger-than-memory data needs chunking or another engine. Notebook 05 targets a mock
API without authentication, so the retry and pagination patterns are simplified. Finally, the
`ds_practice.load_penguins` loader expects the downloaded CSV — the notebooks fail with a clear
message rather than silently substituting a different source.
