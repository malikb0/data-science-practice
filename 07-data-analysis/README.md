# 07 — Data analysis

Analysis turns a dataset into evidence. This module walks a complete regression workflow on the
California Housing table: load and wrangle, explore, build linear and polynomial models, then
evaluate and refine them with cross-validation and regularisation.

**Dataset:** California Housing (public, StatLib via scikit-learn). Fetch it with:

```bash
python scripts/download_data.py --module 07
```

## Learning objectives

By the end of this module you will be able to:

- inspect a table's shape, types, missingness, and ranges before modelling;
- engineer ratio features and justify each one;
- read distributions, correlations, and binned group means during EDA;
- fit linear and polynomial regression and report MAE, RMSE, and R²;
- compare a model against a mean-prediction baseline;
- use K-fold cross-validation and Ridge/Lasso regularisation to refine a model;
- read a learning curve to judge whether more data or a simpler model is needed.

## Prerequisites

- Module [`04-python-for-data-science`](../04-python-for-data-science/README.md) for NumPy/pandas.
- Module [`03-data-science-methodology`](../03-data-science-methodology/README.md) for the idea of
  a lifecycle and held-out evaluation.
- Comfort with basic algebra and the notion of a straight line.

## Dataset

The California Housing table has one row per census block group, with nine numeric columns. Full
provenance and citation are in [`docs/datasets.md`](../docs/datasets.md); field definitions and
units are in [`docs/data-dictionary.md`](../docs/data-dictionary.md).

| Column | Meaning | Units |
|---|---|---|
| `MedInc` | median block-group income | tens of thousands of USD |
| `HouseAge` | median house age | years |
| `AveRooms`, `AveBedrms` | average rooms / bedrooms per household | rooms |
| `Population`, `AveOccup` | block-group population / occupancy | people |
| `Latitude`, `Longitude` | location | degrees |
| `MedHouseVal` | median house value (**target**) | hundreds of thousands of USD |

The target is capped at 5.0 (about $500k), a known artefact that limits all models.

## Topics covered

| Notebook | Topic |
|---|---|
| [`notebooks/01-data-loading-and-wrangling.ipynb`](notebooks/01-data-loading-and-wrangling.ipynb) | Inspection, ratio features, outliers, train/test split |
| [`notebooks/02-exploratory-data-analysis.ipynb`](notebooks/02-exploratory-data-analysis.ipynb) | Distributions, correlation, multicollinearity, geography |
| [`notebooks/03-model-development.ipynb`](notebooks/03-model-development.ipynb) | Baseline, linear regression, polynomial degrees |
| [`notebooks/04-model-evaluation-and-refinement.ipynb`](notebooks/04-model-evaluation-and-refinement.ipynb) | Cross-validation, Ridge/Lasso, learning curves |

The plain-language explainer is [`concepts.md`](concepts.md); worked answers are in
[`solutions.md`](solutions.md). Feature engineering and model factories live in
[`analysis.py`](analysis.py) and are imported by the notebooks.

## How to run

```bash
make install
python scripts/download_data.py --module 07
jupyter lab 07-data-analysis/notebooks/
```

The notebooks run top to bottom once `data/raw/california_housing.csv` exists. Every modelling
notebook calls `set_seed(42)` and uses fixed `random_state` values so results are reproducible.

## Exercises

1. **Wrangling.** Count and justify whether to drop block groups with extreme `AveRooms`; add a
   `bedrooms_per_person` ratio and compare its correlation with the target.
2. **EDA.** Compare skew in `Population`; find a pair with weak correlation but ordered binned
   means; compare house values by a rough coastal split.
3. **Modelling.** Fit a reduced-feature linear model; sweep polynomial degrees until test R²
   falls; examine residuals by income quartile.
4. **Evaluation.** Use Lasso to select features; compare RMSE and MAE rankings of Ridge vs Lasso;
   interpret the learning curve.

## Limitations

The target is censored, the rows are aggregates rather than individuals, and coordinates stand in
for unmeasured local factors. A random train/test split leaks geography because nearby block
groups are similar, so reported scores are optimistic relative to a spatial hold-out. Polynomial
degrees beyond two are hard to interpret. No causal claim is made anywhere in this module.
