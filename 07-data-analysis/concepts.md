# Concepts — data analysis

A plain-language companion to the four notebooks. It explains the ideas a regression workflow
rests on, with small examples.

## Exploratory data analysis

EDA is the conversation you have with a dataset before modelling. Start with structure — how many
rows, what type each column is, which values are missing — then look at how each variable is
distributed. A histogram and a set of quantiles describe a variable better than a mean alone,
because they expose skew and outliers.

```python
frame.describe(percentiles=[0.25, 0.5, 0.75])
frame["target"].hist(bins=30)
```

## Correlation is not causation

The **Pearson correlation** between two variables is their tendency to move together on a straight
line. It runs from -1 (perfect opposite) through 0 (no linear relationship) to +1 (perfect
agreement). It says nothing about cause: ice-cream sales correlate with drownings because both
rise in summer. It also misses non-linear patterns — a U-shaped relationship can have a
correlation near zero. Use it to screen features, not to conclude anything.

**Multicollinearity** is when predictors are highly correlated with each other. It does not usually
hurt predictions, but it inflates the variance of linear coefficients, so "the effect of feature
X" becomes unreliable.

## Feature engineering

Raw columns are not always the most informative. A ratio often generalises better than a count:

```python
frame["rooms_per_person"] = frame["AveRooms"] / frame["AveOccup"]
```

Every engineered feature is a hypothesis. Keep the ones that earn their place with evidence, and
document why you added them.

## Train, validation, and test

A model must be judged on data it did not learn from. Split the data into a **training set** (fit),
a **validation set** (choose hyperparameters), and a **test set** (final, one-time judgement).
Touching the test set during development turns it into a training set and inflates the score.

```python
from sklearn.model_selection import train_test_split
train, test = train_test_split(frame, test_size=0.2, random_state=42)
```

A fixed `random_state` makes the split reproducible, which matters when results are compared.

## Linear regression

Linear regression fits coefficients `w` and an intercept `b` to minimise squared error:

```
y_hat = b + w1*x1 + w2*x2 + ... + wn*xn
```

It is fast and interpretable, and it is a baseline every fancier model must beat. Its weakness is
that it can only represent straight-line relationships unless you give it non-linear inputs.

## Polynomial regression and the bias-variance trade-off

Adding `x²`, `x³`, and interaction terms lets a linear model bend. More flexibility reduces
**bias** (systematic error from too simple a model) but raises **variance** (sensitivity to the
particular training sample). The classic symptom is **overfitting**: training error falls while
test error rises. Choose complexity by validation performance, not training performance.

## Cross-validation

Instead of one split, K-fold cross-validation divides the training data into K folds, fits on K-1,
validates on the remaining one, and repeats. The mean score is more stable and the spread is a
useful warning.

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring="r2")
```

## Regularisation

Regularisation adds a penalty for large coefficients.

- **Ridge (L2)** shrinks coefficients smoothly and keeps all features.
- **Lasso (L1)** can set coefficients exactly to zero, selecting features.

```python
from sklearn.linear_model import Ridge
Ridge(alpha=0.1)   # larger alpha = stronger penalty
```

`alpha` is a hyperparameter tuned by cross-validation. Too small and the model overfits; too large
and it underfits.

## Error metrics

- **MAE** — mean absolute error, in the same units as the target.
- **RMSE** — root mean squared error; penalises large errors more than MAE.
- **R²** — proportion of variance explained; 0 is no better than predicting the mean, negative is
  worse. **Adjusted R²** discounts R² for the number of predictors, so adding useless columns does
  not raise it.

Always report at least one absolute error and R², always on held-out data, and always next to the
baseline.

## Learning curves

A learning curve plots training and validation score against the number of training rows. If both
are still rising, more data may help. If training is high and validation is low, the model is too
complex. If both are low, the model is too simple or the features are weak.
