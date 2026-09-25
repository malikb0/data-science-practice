# 09 — Machine learning

Machine learning turns data into predictions. This module covers the core supervised and
unsupervised techniques — regression, classification, tree ensembles, clustering, dimensionality
reduction — and finishes with the evaluation discipline that makes results trustworthy, all on UCI
datasets and scikit-learn built-ins.

**Datasets:** UCI Adult Income, Wine Quality, and Wholesale Customers (all CC BY 4.0), plus
scikit-learn built-ins. Fetch with:

```bash
python scripts/download_data.py --module 09
```

## Learning objectives

By the end of this module you will be able to:

- split data into train and test sets, with stratification where the target is skewed;
- fit and interpret linear, multiple, and polynomial regression;
- classify with logistic regression, trees, SVMs, and KNN;
- explain bagging and boosting and fit random-forest and gradient-boosting models;
- segment unlabelled data with K-means and DBSCAN after standardising features;
- reduce dimensions with PCA and visualise with t-SNE (and optionally UMAP);
- build pipelines, tune with `GridSearchCV`, and evaluate with a confusion matrix and ROC/AUC.

## Prerequisites

- Module [`04-python-for-data-science`](../04-python-for-data-science/README.md) for NumPy/pandas.
- Module [`07-data-analysis`](../07-data-analysis/README.md) for train/test splits and regression.
- Module [`08-data-visualization`](../08-data-visualization/README.md) for reading embeddings and
  diagnostic plots.
- Comfort with high-school algebra and basic probability.

## Dataset

| Dataset | Rows | Target / use | License |
|---|---|---|---|
| Adult Income | ~32,500 | `income` (`>50K` vs `<=50K`) | CC BY 4.0 |
| Wine Quality (red) | ~1,600 | `quality` (ordinal 3–8) and chemistry | CC BY 4.0 |
| Wholesale Customers | 440 | spending by product category (clustering) | CC BY 4.0 |
| iris / digits / `make_moons` | built-in | classification and embedding demos | BSD 3-Clause |

Provenance and citations are in [`docs/datasets.md`](../docs/datasets.md); field definitions and
units are in [`docs/data-dictionary.md`](../docs/data-dictionary.md). The Adult table is sampled to
6,000 rows in the notebooks to keep runtime short; the sampling is seeded and stated each time.

## Topics covered

| Notebook | Topic |
|---|---|
| [`notebooks/01-regression.ipynb`](notebooks/01-regression.ipynb) | Simple, multiple, and polynomial regression |
| [`notebooks/02-classification.ipynb`](notebooks/02-classification.ipynb) | Logistic, tree, SVM, KNN; multi-class |
| [`notebooks/03-ensembles.ipynb`](notebooks/03-ensembles.ipynb) | Random forest, gradient boosting, importances |
| [`notebooks/04-clustering.ipynb`](notebooks/04-clustering.ipynb) | K-means, DBSCAN, optional HDBSCAN, elbow/silhouette |
| [`notebooks/05-dimensionality-reduction.ipynb`](notebooks/05-dimensionality-reduction.ipynb) | PCA, t-SNE, optional UMAP |
| [`notebooks/06-model-evaluation-and-pipelines.ipynb`](notebooks/06-model-evaluation-and-pipelines.ipynb) | Pipelines, CV, GridSearchCV, ROC/AUC |

Reusable model factories live in [`ml.py`](ml.py); the plain-language explainer is
[`concepts.md`](concepts.md); worked answers are in [`solutions.md`](solutions.md). Optional
libraries (`hdbscan`, `umap-learn`) are attempted and fall back gracefully if absent.

## How to run

```bash
make install
python scripts/download_data.py --module 09
jupyter lab 09-machine-learning/notebooks/
```

Every modelling notebook calls `set_seed(42)` and passes explicit `random_state` values, so splits
and stochastic models are reproducible. The notebooks run top to bottom once the UCI CSVs exist;
scikit-learn built-ins need no download.

## Exercises

1. **Regression.** Rank one-feature models by RMSE; add an interaction term; round predictions to
   the nearest integer and measure exact agreement.
2. **Classification.** Compare `class_weight="balanced"`; show why KNN needs scaling; sweep tree
   depth.
3. **Ensembles.** Sweep the boosting learning rate; add trees to the forest; compare impurity with
   permutation importance.
4. **Clustering.** Contrast scaled and unscaled K-means; plot silhouette against `k`; try optional
   HDBSCAN.
5. **Reduction.** Test accuracy using the first `n` PCA components; vary t-SNE perplexity; run PCA
   without standardising.
6. **Evaluation.** Swap logistic regression for a forest inside the pipeline and tune it; choose a
   threshold given asymmetric error costs; explain leakage.

## Limitations

Model results here are illustrative rather than tuned for deployment. Several datasets are small or
sampled, so scores are noisy. Adult contains historical and possibly sensitive attributes; the
income model is a teaching example, not a basis for decisions about people. Clustering has no
ground truth, so "good" segments are a judgement. Optional HDBSCAN and UMAP are not pinned
dependencies, so those sections degrade to alternatives. Finally, random train/test splits leak
group structure when rows are related, and none of the models is calibrated or monitored.
