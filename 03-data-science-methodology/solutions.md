# Solutions — module 03 exercises

Worked answers to the [README](README.md) exercises. The figures below were produced by re-running
the notebook's preparation and model with the same seed (`42`); your machine may differ only in
the last digit from floating-point ordering.

## Exercise 1 — Switch the question to regression

A regression version of the question would be: *predict a penguin's body mass in grams from its
bill length, bill depth, and flipper length.* A business reason to care: body mass is costly to
measure accurately in the field, so a model that estimates it from measurements already taken
could fill gaps or flag implausible values.

**What changes.** The phase that changes most is **business understanding**, because "success" is
no longer "the right species" but "an estimate close enough to be useful". That ripples into
**evaluation**: accuracy and the majority-class baseline are replaced by error metrics such as
mean absolute error (MAE), root mean squared error (RMSE), and R². The modelling phase also
changes — a classifier is replaced by a regressor — while data understanding and preparation stay
largely the same, apart from the target column.

For illustration, a plain linear regression using the three measurement predictors gives roughly:

| Metric | Value |
|---|---|
| MAE | ≈ 278 g |
| RMSE | ≈ 344 g |
| R² | ≈ 0.79 |

So an average error of a few hundred grams is the price of not weighing the bird. Whether that is
acceptable is a business judgement, not a statistical one.

## Exercise 2 — Median imputation instead of dropping

The notebook drops the two rows with any missing measurement, keeping 342 of 344. If instead each
missing numeric value is filled with the median of its own species, all 344 rows survive. Re-running
the depth-2 tree gives:

| Preparation | Rows kept | Test accuracy |
|---|---:|---:|
| Drop rows with missing values | 342 | 0.988 |
| Impute species median | 344 | 0.977 |

**Argument against imputation here.** Only two rows are affected, so the benefit (two extra
training examples) is negligible, while the cost is that two fabricated values are treated as
real. Because the missingness is tiny and the model already performs well, dropping and
*recording* the loss is the more honest choice.

**Argument for imputation.** Imputation keeps the full sample and is valuable when missingness is
substantial or systematic. A species-specific median respects the fact that the three species have
genuinely different body sizes. The caveat is that imputation assumes values are missing at random;
if the largest birds were the ones not weighed, the imputed median understates them and biases the
model. On this dataset either choice is defensible, but the decision should be stated and
justified.

## Exercise 3 — Tree depth, overfitting, and readability

At `max_depth=2` the tree reaches **0.957 training accuracy** and **0.988 test accuracy**. At
`max_depth=8` it reaches **1.000 training** and **1.000 test** accuracy.

**What the gap means.** The gap between training and test accuracy is the usual sign of
overfitting: a model that has memorised the training rows does worse on new ones. On this dataset
there is essentially **no gap at either depth**, because the species separate cleanly on these
measurements — even a fully grown tree generalises. That is a property of an easy problem, not
proof that deep trees are safe in general. On noisier data the depth-8 tree would fit the noise and
the test score would fall.

**Which depth to hand to a field researcher.** Depth 2. It prints as a handful of readable `if`
rules, and the difference in accuracy (0.988 versus 1.000) is one penguin out of the test set. The
deeper tree's extra accuracy buys almost nothing here and costs interpretability, which is the whole
reason the tree was chosen. The right answer can change when errors are expensive — if a mistake
mattered a great deal, the extra accuracy might justify a larger tree or a different model.
