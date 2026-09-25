# Concepts — machine learning

A plain-language companion to the six notebooks. It explains the vocabulary a beginner meets in
every machine-learning project.

## Supervised versus unsupervised

In **supervised** learning every training row has a known answer (a label or a number), and the task
is to predict it for new rows. Regression predicts a number; classification predicts a category. In
**unsupervised** learning there is no answer key: clustering finds groups, and dimensionality
reduction finds structure. Supervised learning is judged against held-out labels; unsupervised
learning is judged by usefulness.

## Train, validation, test

A model must be measured on data it has not seen.

- the **training set** fits the model;
- the **validation set** (or cross-validation folds) chooses settings;
- the **test set** is used once, at the end.

If you tune against the test set, it becomes a training set and the score is optimistic. Splitting
must also respect structure: time series are split by time, and grouped data by group.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

## Bias and variance

**Bias** is error from a model that is too simple to capture the pattern; **variance** is error from
a model that is so flexible it fits noise. A single decision tree has low bias and high variance;
a straight line has high bias and low variance. **Regularisation** and **averaging many models**
reduce variance. The classic symptom of too much variance is training error far below test error.

## Why scale features

Distance-based methods (KNN, SVM, K-means) and regularised linear models treat all features by their
numeric magnitude. If one column ranges to thousands and another to single digits, the first
dominates. **Standardisation** subtracts the mean and divides by the standard deviation, giving
every feature equal weight. Fit the scaler on the training data only; a pipeline does this
automatically inside each fold.

## Regression

- **Linear**: `y = b + w1 x1 + ... + wn xn`, fitted by least squares.
- **Polynomial**: add `x²`, `x³`, and interactions so a linear model can curve.
- **Ridge (L2)**: penalises the sum of squared coefficients, shrinking them smoothly.
- **Lasso (L1)**: penalises absolute coefficients and can zero some out, selecting features.

Metrics: **MAE** (average absolute error), **RMSE** (penalises large errors), **R²** (variance
explained; 0 = no better than the mean).

## Classification

- **Logistic regression**: linear boundary in the log-odds; outputs probabilities.
- **Decision tree**: nested if/else splits; interpretable, overfits without depth control.
- **SVM**: maximum-margin boundary, kernels allow curves.
- **KNN**: vote of the nearest neighbours; simple, needs scaling and is slow to predict.

Metrics from a **confusion matrix**:

- **accuracy** = correct / total;
- **precision** = true positives / predicted positives;
- **recall** = true positives / actual positives;
- **F1** = harmonic mean of precision and recall.

**ROC/AUC** summarises every threshold: AUC is the chance a random positive outranks a random
negative. A high AUC does not guarantee well-calibrated probabilities.

## Tree ensembles

- **Bagging / random forest**: average many trees trained on bootstrap samples; reduces variance.
- **Boosting / gradient boosting**: fit trees in sequence, each correcting the previous errors;
  reduces bias, can overfit, and is slower.

Feature importance from trees measures impurity reduction; it favours high-cardinality features, so
**permutation importance** (shuffle a feature, measure the drop in score) is a useful cross-check.

## Clustering

- **K-means**: `k` centroids, minimise within-cluster squared distance; needs `k`, assumes
  spherical clusters.
- **DBSCAN**: grow clusters from dense regions; finds irregular shapes and labels sparse points as
  noise; sensitive to `eps`.
- **HDBSCAN**: varies the density threshold automatically (optional dependency).

Choose `k` with the **elbow** (inertia stops falling fast) and the **silhouette** (how well points
fit their cluster versus the next nearest). Always standardise first.

## Dimensionality reduction

- **PCA**: linear, fast, invertible; components are uncorrelated and ordered by variance. Read the
  **explained variance ratio** and the **loadings**.
- **t-SNE**: non-linear, stochastic, good for visualisation; cluster sizes and gaps are not
  meaningful.
- **UMAP**: non-linear, faster, often preserves more global structure (optional dependency).

Use PCA for model inputs; use t-SNE/UMAP only to look at data.

## Pipelines and tuning

A **pipeline** bundles preprocessing with a model so that fitting and predicting apply the same
steps and cross-validation refits them inside each fold, preventing leakage.

```python
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
search = GridSearchCV(pipeline, {"model__C": [0.1, 1.0, 10.0]}, cv=5, scoring="f1")
search.fit(X_train, y_train)
```

Nested parameters use double underscores (`model__C`). Report the chosen settings, the mean CV
score, and the one-time test score.
