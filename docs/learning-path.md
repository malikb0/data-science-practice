# Learning path

A suggested order for working through the portfolio, with the outcomes and an effort estimate for
each stage. The sequence is deliberate: each stage assumes only the skills from those before it.

## Before you start

```bash
make install                                   # build the virtual environment
python scripts/download_data.py --all          # fetch every dataset (~a few minutes)
make test                                      # confirm the offline tests pass
```

Read the root [`README.md`](../README.md) and [`methodology.md`](methodology.md) first.

## Stage 1 — Foundations (modules 01–03) · ~3–4 hours

| Order | Module | Outcome | Effort |
|---|---|---|---|
| 1 | [01 what-is-data-science](../01-what-is-data-science/README.md) | Describe the data-science lifecycle and roles | 45 min |
| 2 | [02 tools for data science](../02-tools-for-data-science/README.md) | Use notebooks, Markdown, and Git reproducibly | 1 h |
| 3 | [03 methodology](../03-data-science-methodology/README.md) | Run CRISP-DM end to end on one dataset | 1.5 h |

No coding background beyond basic computer literacy is required for stage 1; module 02 starts the
notebook habit.

## Stage 2 — Python core (modules 04–05) · ~6–8 hours

| Order | Module | Outcome | Effort |
|---|---|---|---|
| 4 | [04 python for data science](../04-python-for-data-science/README.md) | Use types, control flow, functions, classes, files, NumPy, pandas, and HTTP APIs | 4 h |
| 5 | [05 python project](../05-python-project/README.md) | Scrape, clean, and present a dataset as a dashboard | 2.5 h |

After this stage you can acquire and shape data yourself. The five notebooks in module 04 are
independent; do them in order.

## Stage 3 — Data handling (modules 06–07) · ~7–9 hours

| Order | Module | Outcome | Effort |
|---|---|---|---|
| 6 | [06 databases and SQL](../06-databases-and-sql/README.md) | Design a normalised schema and query it with joins, views, and windows | 4 h |
| 7 | [07 data analysis](../07-data-analysis/README.md) | Explore data and build and evaluate regression models | 3.5 h |

These can be done in either order, but the SQL module reinforces careful tabular thinking before
statistical modelling.

## Stage 4 — Communication and prediction (modules 08–09) · ~10–12 hours

| Order | Module | Outcome | Effort |
|---|---|---|---|
| 8 | [08 data visualisation](../08-data-visualization/README.md) | Build static, interactive, and geographic figures and a dashboard | 4.5 h |
| 9 | [09 machine learning](../09-machine-learning/README.md) | Fit supervised and unsupervised models and evaluate them honestly | 6 h |

Finish with the capstone in the separate
[`falcon9-landing-analysis`](https://github.com/malikb0/falcon9-landing-analysis) repository, which
combines acquisition, SQL, analysis, modelling, and visualisation into one project.

## How to study each module

1. Read the module `README.md` for objectives and the dataset.
2. Read `concepts.md` slowly; it explains the vocabulary before the code.
3. Work the notebooks top to bottom, predicting the output before running each cell.
4. Attempt the notebook exercises before opening `solutions.md`.
5. Re-derive one result independently — a different split, a different chart — to test your
   understanding.

## Progress checklist

- [ ] Stage 1 complete
- [ ] Module 04 notebooks all run
- [ ] Scraped or queried a dataset you did not download as a CSV
- [ ] Built and evaluated a regression model
- [ ] Built and evaluated a classifier with cross-validation
- [ ] Produced one map and one interactive chart
- [ ] Capstone attempted
