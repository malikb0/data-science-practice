# Solutions — data analysis

Worked answers to the exercises in [`README.md`](README.md) and at the end of each notebook. Start
from the same setup:

```python
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path.cwd().parent))
import analysis
from ds_practice import load_california, set_seed, regression_metrics, adjusted_r2
from sklearn.model_selection import train_test_split

set_seed(42)
housing = analysis.add_features(load_california())
train, test = train_test_split(housing, test_size=0.2, random_state=42)
X_train, y_train = analysis.split_xy(train)
X_test, y_test = analysis.split_xy(test)
```

## Notebook 01 — Data loading and wrangling

### 1. Range check on `AveRooms`

```python
high = housing[housing["AveRooms"] > 20]
print("count:", len(high), "share:", round(len(high) / len(housing), 4))
```

These rows are a tiny fraction and look like reporting artefacts (very few households with many
rooms). Dropping them removes noise, but because they are so few the effect on the model is small;
keeping them is also defensible. The important thing is to state the choice.

### 2. A new ratio

```python
housing = housing.assign(bedrooms_per_person=housing["AveBedrms"] / housing["AveOccup"])
print("AveBedrms corr          :", round(housing["AveBedrms"].corr(housing["MedHouseVal"]), 3))
print("bedrooms_per_person corr:", round(housing["bedrooms_per_person"].corr(housing["MedHouseVal"]), 3))
```

The per-person version usually correlates more strongly because it normalises away household size.

### 3. Split sizes

```python
train7, test7 = train_test_split(housing, test_size=0.3, random_state=7)
print(len(train7), len(test7))
```

Fixing the seed matters because a different split produces different scores; without it, two runs
are not comparable.

## Notebook 02 — Exploratory data analysis

### 1. Skew check

```python
for col in ["Population", "AveOccup"]:
    print(col, "mean", round(housing[col].mean(), 2), "median", round(housing[col].median(), 2),
          "skew", round(housing[col].skew(), 2))
```

A mean far above the median and a large positive skew means a few large values pull the mean up.
Models that assume symmetry (like ordinary least squares on unscaled features) can be dominated by
those rows.

### 2. Weak correlation, ordered means

```python
housing = housing.assign(age_band=pd.qcut(housing["HouseAge"], 4, labels=["new", "mid", "old", "oldest"]))
print(housing.groupby("age_band", observed=True)["MedHouseVal"].mean().round(3))
```

`HouseAge` often has a weak linear correlation with value yet shows ordered group means, because
the relationship is not a straight line. Correlation measures only the linear part.

### 3. Coastal effect

```python
coastal = housing.assign(north=housing["Latitude"] >= 37)
print(coastal.groupby("north")["MedHouseVal"].mean().round(3))
```

The south (coastal) half has a higher mean, but the split cuts through inland and coastal areas
alike, so it mixes very different places — a crude proxy at best.

## Notebook 03 — Model development

### 1. Feature subset

```python
subset = ["MedInc", "AveRooms", "bedrooms_per_room", "population_per_household", "rooms_per_person"]
small = analysis.fit_linear(X_train[subset], y_train)
print("subset test R2:", round(analysis.evaluate(small, X_test[subset], y_test)["r2"], 3))
print("full   test R2:", round(analysis.evaluate(analysis.fit_linear(X_train, y_train), X_test, y_test)["r2"], 3))
```

Income dominates, so the subset gets close to the full model; dropping geography costs the most.

### 2. Degree sweep to four

```python
for degree in (1, 2, 3, 4):
    model = analysis.fit_polynomial(X_train, y_train, degree=degree)
    print(degree, round(analysis.evaluate(model, X_test, y_test)["r2"], 3))
```

Stop at the first degree whose test R² drops below the previous one; beyond that the extra terms
fit noise.

### 3. Residuals by income quartile

```python
pred = analysis.fit_linear(X_train, y_train).predict(X_test)
residuals = pd.DataFrame({"resid": y_test - pred, "income_q": pd.qcut(X_test["MedInc"], 4)})
print(residuals.groupby("income_q", observed=True)["resid"].mean().round(3))
```

A systematic trend (for example large negative residuals in the top quartile) reveals the capped
target and the straight-line limitation.

## Notebook 04 — Evaluation and refinement

### 1. Lasso selection

```python
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

lasso = Pipeline([("scale", StandardScaler()), ("model", Lasso(alpha=0.001, max_iter=5000))]).fit(X_train, y_train)
kept = pd.Series(lasso.named_steps["model"].coef_, index=X_train.columns)
print(kept[kept != 0].round(3))
print("zeroed:", kept[kept == 0].index.tolist())
```

Lasso typically zeroes redundant ratios while keeping income and the main geographic signal.

### 2. Scoring choice

```python
from sklearn.model_selection import cross_val_score
for name, Model in (("ridge", Ridge), ("lasso", Lasso)):
    model = Pipeline([("scale", StandardScaler()), ("model", Model(alpha=0.1, max_iter=5000))])
    mae = -cross_val_score(model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error").mean()
    print(name, "MAE", round(mae, 3))
```

Ridge and Lasso usually rank the same way under both metrics; if the ranking flips, one model is
better at avoiding large errors (RMSE) while the other is better on average (MAE).

### 3. Learning curve reading

If the validation line is still climbing at the largest training size while the training line is
much higher, more data would likely help. If the two lines have converged near a low value, the
model is capacity-limited and more data will not help.
