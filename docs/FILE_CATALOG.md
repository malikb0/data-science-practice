# File catalogue

Every tracked file in the repository, with its type and purpose. Downloaded data under
`data/raw/`, the `.orchestrator/` scaffolding, and the virtual environment are intentionally
excluded (they are git-ignored). Notebooks are `.ipynb`; a per-notebook description is given in
the owning module's README.

## Root

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Hub: pitch, non-affiliation, skill-to-project map, Mermaid diagrams, quickstart |
| `NOTICE.md` | Markdown | Inspiration credit, non-affiliation, dataset attributions |
| `LICENSE` | Text | MIT licence for the owner's work |
| `CITATION.cff` | YAML | Citation metadata |
| `Makefile` | Make | `install`, `test`, `nb`, `data`, `clean` targets |
| `requirements.txt` | Text | Pinned Python dependencies |
| `pyproject.toml` | TOML | `src`-layout packaging for `ds_practice` |
| `.gitignore` | Text | Ignores venv, caches, downloaded data, scaffolding |
| `.github/workflows/ci.yml` | YAML | CI: install requirements and run offline-safe tests |

## `docs/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Documentation index and conventions |
| `course-map.md` | Markdown | Certificate skill area to original project map |
| `datasets.md` | Markdown | Source, licence, citation, and fetch command per dataset |
| `data-dictionary.md` | Markdown | Fields, types, units, and provenance per dataset |
| `methodology.md` | Markdown | How projects were built and kept reproducible |
| `erd-module-06.md` | Markdown | Entity-relationship diagram and key/constraint notes for module 06 |
| `glossary.md` | Markdown | Key terms defined |
| `learning-path.md` | Markdown | Suggested sequence, effort, and outcomes |
| `STRUCTURE.md` | Markdown | Directory tree and architecture hierarchy |
| `FILE_CATALOG.md` | Markdown | This file |

## `scripts/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Script inventory and usage |
| `download_data.py` | Python | Fetch and cache every dataset (`--module NN` / `--all`) |
| `run_notebooks.py` | Python | Execute offline-safe notebooks and report a summary |

## `src/ds_practice/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Package overview and API |
| `__init__.py` | Python | Public API re-exports |
| `data.py` | Python | Typed dataset loaders used by the notebooks |
| `metrics.py` | Python | Regression, classification, and adjusted-R² metrics |
| `paths.py` | Python | Repository-root and data-path resolution |
| `seeding.py` | Python | Deterministic random seeding |
| `sql.py` | Python | SQLite connection and query helpers |
| `viz.py` | Python | Shared plotting theme and figure helpers |

## `tests/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Test layout and how to run them |
| `conftest.py` | Python | Adds repository paths for imports |
| `helpers.py` | Python | `require_file`, `load_module`, notebook readers |
| `test_01_what_is_data_science.py` | Python | Module 01 content checks |
| `test_02_tools.py` | Python | Module 02 smoke tests |
| `test_03_methodology.py` | Python | Module 03 data contract and smoke test |
| `test_04_python_for_data_science.py` | Python | Packaged helpers and data contract |
| `test_05_python_project.py` | Python | Scraper parsing and dashboard builders |
| `test_06_databases_and_sql.py` | Python | Schema/ETL smoke tests and data contract |
| `test_07_data_analysis.py` | Python | Feature-engineering and model smoke tests |
| `test_08_data_visualization.py` | Python | Chart builders and app filters |
| `test_09_machine_learning.py` | Python | Model factories and pipeline smoke tests |

## `data/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Explains the cache layout; no data is committed |
| `raw/` | Directory | Downloaded datasets (git-ignored) |

## Module 01 — `01-what-is-data-science/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `case-study.md` | Markdown | A life-cycle example |
| `concepts.md` | Markdown | Plain-language explainer |
| `solutions.md` | Markdown | Worked answers |

## Module 02 — `02-tools-for-data-science/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | Notebooks, Git, reproducibility |
| `solutions.md` | Markdown | Worked answers |
| `notebooks/01-jupyter-and-git.ipynb` | Notebook | Notebook format, Markdown, Git workflow |

## Module 03 — `03-data-science-methodology/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | CRISP-DM phases explained |
| `solutions.md` | Markdown | Worked answers |
| `notebooks/01-crisp-dm-penguins.ipynb` | Notebook | CRISP-DM applied end to end |

## Module 04 — `04-python-for-data-science/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | Language and data-stack explainer |
| `solutions.md` | Markdown | Worked answers |
| `pyutils.py` | Python | Packaged example helpers (`mass_band`, `summarise`, `band_counts`) |
| `notebooks/01-language-basics.ipynb` | Notebook | Types, containers, conditionals, loops, exceptions |
| `notebooks/02-functions-and-classes.ipynb` | Notebook | Functions, lambdas, OOP |
| `notebooks/03-files-and-data-io.ipynb` | Notebook | CSV/JSON and pandas I/O |
| `notebooks/04-numpy-and-pandas.ipynb` | Notebook | ndarrays, DataFrames, groupby/merge |
| `notebooks/05-apis-and-http.ipynb` | Notebook | requests, JSON APIs, pagination, errors |

## Module 05 — `05-python-project/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | Scraping, HTTP, and dashboards explained |
| `solutions.md` | Markdown | Worked answers |
| `scrape.py` | Python | Parsing helpers for the book catalogue |
| `notebooks/01-web-scraping.ipynb` | Notebook | Ethical scraping, parsing, pagination |
| `notebooks/02-analysis.ipynb` | Notebook | Cleaning, analysis, prepared data |
| `app/README.md` | Markdown | Dashboard run instructions |
| `app/dashboard.py` | Python | Plotly Dash book-catalogue dashboard |

## Module 06 — `06-databases-and-sql/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | Relational and SQL explainer |
| `solutions.md` | Markdown | Worked answers |
| `schema.sql` | SQL | Normalised schema, constraints, indexes, and a view |
| `load.py` | Python | ETL from OpenFlights files into SQLite |
| `notebooks/01-ddl-and-constraints.ipynb` | Notebook | DDL, keys, constraints, indexes |
| `notebooks/02-filtering-and-aggregation.ipynb` | Notebook | WHERE/LIKE/GROUP BY/HAVING and functions |
| `notebooks/03-joins-and-subqueries.ipynb` | Notebook | Inner/left/self joins, subqueries, CTEs |
| `notebooks/04-views-procedures-transactions.ipynb` | Notebook | Views, procedures, ACID, triggers |
| `notebooks/05-window-functions-and-performance.ipynb` | Notebook | Window functions, query plans, indexes |

## Module 07 — `07-data-analysis/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | EDA, regression, validation explainer |
| `solutions.md` | Markdown | Worked answers |
| `analysis.py` | Python | Feature engineering and model factories |
| `notebooks/01-data-loading-and-wrangling.ipynb` | Notebook | Inspection, features, split |
| `notebooks/02-exploratory-data-analysis.ipynb` | Notebook | Distributions, correlation, geography |
| `notebooks/03-model-development.ipynb` | Notebook | Linear and polynomial regression |
| `notebooks/04-model-evaluation-and-refinement.ipynb` | Notebook | Cross-validation and regularisation |

## Module 08 — `08-data-visualization/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | Chart grammar and tools explainer |
| `solutions.md` | Markdown | Worked answers |
| `charts.py` | Python | Plotly and Folium figure builders |
| `app/README.md` | Markdown | Dashboard run instructions |
| `app/dashboard.py` | Python | Gapminder Plotly Dash dashboard |
| `notebooks/01-matplotlib-fundamentals.ipynb` | Notebook | Figure anatomy, line/area/hist/bar |
| `notebooks/02-statistical-and-specialty-plots.ipynb` | Notebook | Box/scatter/bubble/waffle/word frequency |
| `notebooks/03-plotly-interactive.ipynb` | Notebook | Interactive charts and animation |
| `notebooks/04-dash-app.ipynb` | Notebook | Components and callbacks |
| `notebooks/05-geospatial-folium.ipynb` | Notebook | Markers, choropleth, proximity |

## Module 09 — `09-machine-learning/`

| File | Type | Purpose |
|---|---|---|
| `README.md` | Markdown | Module overview |
| `concepts.md` | Markdown | Supervised/unsupervised ML explainer |
| `solutions.md` | Markdown | Worked answers |
| `ml.py` | Python | Seeded classifier, regressor, and cluster factories |
| `notebooks/01-regression.ipynb` | Notebook | Simple, multiple, polynomial regression |
| `notebooks/02-classification.ipynb` | Notebook | Logistic, tree, SVM, KNN, multi-class |
| `notebooks/03-ensembles.ipynb` | Notebook | Random forest, gradient boosting, importances |
| `notebooks/04-clustering.ipynb` | Notebook | K-means, DBSCAN, elbow/silhouette |
| `notebooks/05-dimensionality-reduction.ipynb` | Notebook | PCA, t-SNE, optional UMAP |
| `notebooks/06-model-evaluation-and-pipelines.ipynb` | Notebook | Pipelines, CV, GridSearchCV, ROC/AUC |
