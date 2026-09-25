# 03 — Data science methodology

Running a project through a structured lifecycle. This module applies the six phases of
**CRISP-DM** (the Cross-Industry Standard Process for Data Mining) end to end on one small,
real dataset.

**Dataset:** Palmer Penguins (CC0). Fetch it with:

```bash
python scripts/download_data.py --module 03
```

## Learning objectives

By the end of this module you should be able to:

- Name the six CRISP-DM phases and explain, in one sentence each, why the phase exists.
- Translate a vague request into a measurable question with an explicit success criterion.
- Inspect a dataset for shape, types, missingness, and plausible ranges before modelling.
- Prepare only the columns a question needs, and account for every row that is dropped.
- Fit and evaluate a small, interpretable decision tree against a majority-class baseline.
- Describe what "deployment" means for a model whose output informs a human decision.

## Prerequisites

- Module [`01`](../01-what-is-data-science/README.md) for the lifecycle vocabulary.
- Module [`02`](../02-tools-for-data-science/README.md) for notebooks and reproducibility habits.
- Basic Python and comfort with `pandas`; the shared `ds_practice` package supplies the loader
  and evaluation helpers.

## Topics covered

- The six CRISP-DM phases: business understanding, data understanding, data preparation,
  modelling, evaluation, and deployment.
- Exploratory inspection before modelling, including missing values and ranges.
- A train/test split with a fixed seed and stratification.
- An interpretable tree (`max_depth=2`) chosen for explanation, not for maximum accuracy.
- Honest evaluation: held-out accuracy, a baseline comparison, and a confusion matrix.
- A deployment discussion: confidence, human review, logging, and retraining.

## How to run

```bash
make install
python scripts/download_data.py --module 03
jupyter lab 03-data-science-methodology/notebooks/01-crisp-dm-penguins.ipynb
```

The notebook runs top to bottom once `data/raw/penguins.csv` is present. The plain-language
explanation of CRISP-DM is in [`concepts.md`](concepts.md); worked answers are in
[`solutions.md`](solutions.md).

## Exercises

1. Restate the modelling question as a *regression* problem by predicting `body_mass_g` from the
   other measurements, and write down a business reason someone might care about that number.
   Which CRISP-DM phase changes the most when you switch from classification to regression?
2. In the preparation phase, instead of dropping rows with missing measurements, impute each
   missing value with the **median of its species**. Re-run the model and report whether held-out
   accuracy changes. In two or three sentences, argue for or against imputation on this dataset.
3. The tree uses `max_depth=2`. Increase the depth to `8`, evaluate it, and explain what the gap
   between training and test accuracy is telling you. Which depth would you choose to hand to a
   field researcher, and why?

## Limitations

- The dataset is small, balanced, and unusually clean, so it under-states the effort that data
  preparation takes on real projects.
- A single train/test split is noisy; a careful study would cross-validate and report a range.
- The model is chosen for interpretability, so it is not the most accurate model that could be
  fitted to this table.
- "Deployment" is discussed rather than implemented; no service, API, or monitoring system is
  built here.
