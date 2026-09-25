# Solutions — machine learning

Worked answers to the exercises in [`README.md`](README.md) and at the end of each notebook. The
shared setup imports the module's `ml.py` factories and `ds_practice`:

```python
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path.cwd().parent))
import ml
from ds_practice import set_seed, regression_metrics, classification_metrics

set_seed(42)
```

## Notebook 01 — Regression

### 1. One feature, three metrics

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

wine = __import__("ds_practice").load_wine()
rows = []
for feature in ["alcohol", "volatile acidity", "citric acid"]:
    X_train, X_test, y_train, y_test = train_test_split(
        wine[[feature]], wine["quality"], test_size=0.2, random_state=42
    )
    model = LinearRegression().fit(X_train, y_train)
    metrics = regression_metrics(y_test, model.predict(X_test))
    rows.append({"feature": feature, "slope": round(model.coef_[0], 3),
                 "rmse": round(metrics["rmse"], 3), "r2": round(metrics["r2"], 3)})
display(pd.DataFrame(rows).sort_values("rmse"))
```

Alcohol usually has the lowest RMSE and a positive slope; volatile acidity has a negative slope.

### 2. An interaction

```python
wine = wine.assign(alc_vol=wine["alcohol"] * wine["volatile acidity"])
features = [c for c in wine.columns if c != "quality"]
X_train, X_test, y_train, y_test = train_test_split(
    wine[features], wine["quality"], test_size=0.2, random_state=42
)
model = ml.make_regressor("linear").fit(X_train, y_train)
print(regression_metrics(y_test, model.predict(X_test)))
```

An interaction captures the idea that the effect of alcohol depends on acidity; it helps only if
that joint effect is real and not just noise.

### 3. Ordinal reality

```python
pred = model.predict(X_test)
rounded = np.rint(pred)
print("exact match:", round((rounded == y_test).mean(), 3))
```

Rounding to the nearest integer and measuring exact agreement asks the question a user actually
cares about ("can it name the score?"), and it avoids rewarding a model for being close on average
but never exactly right.

## Notebook 02 — Classification

### 1. Class weighting

```python
balanced = ml.make_classifier("logistic", class_weight="balanced")
```

`class_weight="balanced"` raises the weight of the minority `>50K` class, which usually increases
its recall at the cost of precision. This is the right move when missing a positive is expensive.

### 2. Scaling and KNN

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

knn = ml.make_classifier("knn", n_neighbors=5)
```

KNN measures distance, so without scaling `capital_gain` (thousands) swamps `age` (tens). The
pipeline in `ml.make_classifier` already includes `StandardScaler`; removing it drops accuracy
sharply.

### 3. Tree depth

```python
for depth in (2, 6, 12):
    model = ml.make_classifier("tree", max_depth=depth)
    model.fit(X_train, y_train)
    print(depth, round(model.score(X_train, y_train), 3), round(model.score(X_test, y_test), 3))
```

Training accuracy rises monotonically with depth while test accuracy peaks and then falls — the
textbook overfitting curve.

## Notebook 03 — Ensembles

### 1. Learning rate

```python
for lr in (0.01, 0.1, 0.5):
    model = ml.make_classifier("boosting", n_estimators=150, learning_rate=lr)
    model.fit(X_train, y_train)
    print(lr, classification_metrics(y_test, model.predict(X_test))["f1"])
```

Small learning rates need more trees for the same fit but generalise more gently; large rates fit
faster and can overshoot into overfitting.

### 2. More trees

```python
forest = ml.make_classifier("forest", n_estimators=500).fit(X_train, y_train)
```

Adding trees to a forest averages more independent votes, so variance falls and the score usually
plateaus rather than degrades. The cost is training time and memory.

### 3. Importance disagreement

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(forest, X_test, y_test, n_repeats=5, random_state=42)
```

One-hot columns for `occupation` often rank high on impurity importance but lower on permutation
importance, because impurity importance rewards features that create many small pure splits.

## Notebook 04 — Clustering

### 1. Scaling matters

```python
from sklearn.preprocessing import StandardScaler

raw_labels = ml.make_cluster("kmeans", n_clusters=2).fit_predict(wholesale[features])
scaled_labels = ml.make_cluster("kmeans", n_clusters=2).fit_predict(
    StandardScaler().fit_transform(wholesale[features])
)
print(pd.crosstab(raw_labels, scaled_labels))
```

Without scaling, `Fresh` (with the largest spread) dominates the distance and the clusters reflect
fresh-produce spend alone.

### 2. Silhouette by k

```python
from sklearn.metrics import silhouette_score

for k in range(2, 9):
    labels = ml.make_cluster("kmeans", n_clusters=k).fit_predict(X)
    print(k, round(silhouette_score(X, labels), 3))
```

The best silhouette often occurs at two clusters, agreeing with where the inertia elbow flattens.

### 3. Optional HDBSCAN

```python
try:
    import hdbscan

    labels = hdbscan.HDBSCAN(min_cluster_size=15).fit_predict(X)
    print("hdbscan noise:", (labels == -1).sum())
except ImportError:
    print("hdbscan not installed; using DBSCAN")
    labels = ml.make_cluster("dbscan", eps=1.5, min_samples=10).fit_predict(X)
```

HDBSCAN often finds one or two clusters with fewer noise points than DBSCAN at a fixed `eps`.

## Notebook 05 — Dimensionality reduction

### 1. Component count

```python
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

for n in (1, 2, 5, len(features)):
    reduced = PCA(n_components=n, random_state=42).fit_transform(X_scaled)
    score = cross_val_score(LogisticRegression(max_iter=1000), reduced, y, cv=5).mean()
    print(n, round(score, 3))
```

A handful of components often recover most of the accuracy, showing that the dropped directions
carried little class signal.

### 2. Perplexity sensitivity

```python
from sklearn.manifold import TSNE

for perplexity in (5, 50):
    coords = TSNE(n_components=2, perplexity=perplexity, random_state=42).fit_transform(X_scaled)
```

Low perplexity produces many small, tight clumps; high perplexity blends them into larger
structures. The "true" grouping is not identifiable from the picture alone.

### 3. Standardise or not

```python
unscaled = PCA(n_components=2, random_state=42).fit(X)   # X not standardised
print(unscaled.components_[0])
```

Without standardisation, the feature with the largest variance dominates the first component, so
the result describes measurement scale rather than structure.

## Notebook 06 — Evaluation and pipelines

### 1. Switch the model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

rf_pipe = Pipeline([("prep", preprocess), ("model", RandomForestClassifier(random_state=42))])
search = GridSearchCV(rf_pipe, {"model__n_estimators": [100, 300]}, cv=cv, scoring="f1")
search.fit(X_train, y_train)
print(search.best_params_, round(search.best_score_, 3))
```

The forest usually improves F1 over logistic regression but is slower to fit and less interpretable.

### 2. Threshold policy

```python
for threshold in (0.3, 0.5, 0.7):
    pred = (prob >= threshold).astype(int)
    print(threshold, classification_metrics(y_test, pred))
```

If a false negative costs five times a false positive, lower the threshold to catch more positives
(higher recall), because the expected cost of missing a positive outweighs the cost of extra false
alarms.

### 3. Leakage check

Scaling before splitting computes the mean and standard deviation using the test rows, so the test
statistics influence the training representation. The pipeline instead fits the scaler on the
training fold only and applies the learned parameters to the validation fold, keeping the test set
untouched.
