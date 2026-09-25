# Glossary

Key terms used across the portfolio, defined in plain language. Cross-references point to the
module that teaches the idea.

## Data science practice

**CRISP-DM** — Cross-Industry Standard Process for Data Mining: a six-phase project lifecycle
(business understanding, data understanding, data preparation, modelling, evaluation, deployment).
See module 03.

**Data contract** — An explicit agreement about a dataset's columns, types, and value ranges,
encoded as a test that skips when the data is absent. See `tests/` and module 03.

**Reproducibility** — Being able to obtain the same result from the same inputs, achieved here with
pinned dependencies, fixed random seeds, and top-to-bottom notebooks. See module 02.

**Seed** — A number that initialises a random generator so runs are repeatable. This repository
uses `42` by default through `ds_practice.set_seed`.

## Python

**Container** — A value that holds other values: `list` (ordered, mutable), `tuple` (ordered,
fixed), `set` (unique), `dict` (key to value). See module 04.

**Exception** — Python's way of signalling an error; handled with `try` / `except` to recover from
expected failures. See module 04.

**Lambda** — A small anonymous function, often used as a `key` for sorting. See module 04.

**Class** — A blueprint for objects that bundles data with behaviour. See module 04.

**Context manager** — The `with` statement, which guarantees cleanup such as closing a file. See
module 04.

**NumPy ndarray** — A typed, contiguous array supporting fast vectorised operations. See module 04.

**pandas DataFrame** — A labelled table of typed columns with selection, filtering, grouping, and
joining. See modules 04 and 07.

**Vectorisation** — Applying an operation to a whole array at once instead of looping in Python.
See module 04.

## Data acquisition and storage

**Web scraping** — Reading HTML intended for browsers in order to build a dataset; performed
politely and within a site's rules. See module 05.

**REST API** — A service that exposes resources at URLs and is read with HTTP `GET`; responses are
usually JSON. See modules 04 and 05.

**JSON** — A text format for nested objects, arrays, strings, and numbers that maps onto Python
`dict` and `list`. See modules 04 and 05.

**Pagination** — Returning a long list in pages, commonly with `_page` and `_limit` parameters. See
module 05.

**Primary key** — The column that uniquely identifies a row. See module 06.

**Foreign key** — A column that references a primary key in another table, enforcing a relationship.
See module 06.

**Normalisation** — Splitting repeated data into separate tables referenced by keys. See module 06.

**Index** — A sorted structure that speeds lookups on a column at the cost of slower writes. See
module 06.

**View** — A saved query that behaves like a table. See module 06.

**Transaction / ACID** — A group of writes that all succeed or all fail; databases guarantee
atomicity, consistency, isolation, and durability. See module 06.

**Window function** — A calculation across related rows that keeps every row, such as a rank or
running total. See module 06.

## Analysis and visualisation

**Feature engineering** — Creating new columns, such as ratios, from existing ones. See module 07.

**Correlation** — A measure from -1 to +1 of linear co-movement; it is not causation. See module 07.

**Train / validation / test split** — Partitioning data so a model is fitted, tuned, and judged on
separate rows. See modules 07 and 09.

**Cross-validation** — Repeatedly splitting the training data into folds to estimate performance
more stably. See modules 07 and 09.

**Regularisation** — Penalising large coefficients (Ridge L2, Lasso L1) to reduce overfitting. See
modules 07 and 09.

**Bias and variance** — Systematic error from a model that is too simple versus sensitivity to the
training sample from one that is too flexible. See modules 07 and 09.

**MAE / RMSE / R²** — Mean absolute error, root mean squared error, and the proportion of variance
explained, all used to score regression. See module 07.

**Choropleth** — A map that shades regions by a value. See module 08.

**Waffle chart** — A grid of unit squares used to show proportions honestly. See module 08.

## Machine learning

**Supervised learning** — Learning from labelled examples to predict a number or category. See
module 09.

**Unsupervised learning** — Finding structure without labels, as in clustering. See module 09.

**Classification** — Predicting a category; scored with accuracy, precision, recall, and F1. See
module 09.

**Regression** — Predicting a number; scored with MAE, RMSE, and R². See modules 07 and 09.

**Bagging / random forest** — Averaging many decorrelated trees to reduce variance. See module 09.

**Boosting / gradient boosting** — Fitting trees in sequence, each correcting the previous errors.
See module 09.

**K-means** — Partitioning points into `k` clusters by distance to centroids. See module 09.

**DBSCAN** — Finding dense clusters and labelling sparse points as noise. See module 09.

**PCA** — A linear projection onto uncorrelated components ordered by variance. See module 09.

**t-SNE / UMAP** — Non-linear embeddings used mainly for visualisation. See module 09.

**Pipeline** — Bundling preprocessing with a model so they are fitted and applied together. See
module 09.

**GridSearchCV** — Exhaustive hyperparameter search with cross-validation. See module 09.

**ROC / AUC** — A threshold-free summary of a classifier's ranking quality. See module 09.

**Overfitting** — Fitting noise so training performance is better than test performance. See
modules 07, 09.
