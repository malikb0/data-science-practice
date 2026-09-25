# Skill → project map

This repository turns the nine skill areas of a standard data-science curriculum into nine
self-contained mini-projects. Each project uses a **different public dataset**, so the focus
stays on the technique rather than on any one dataset's quirks.

| # | Skill area | Original project | Dataset | Core techniques |
|---|---|---|---|---|
| 01 | What is data science | [`01-what-is-data-science`](../01-what-is-data-science/README.md) | — | Lifecycle, roles, a short applied walkthrough |
| 02 | Tools for data science | [`02-tools-for-data-science`](../02-tools-for-data-science/README.md) | — | Notebooks, Markdown, Git, reproducibility |
| 03 | Methodology | [`03-data-science-methodology`](../03-data-science-methodology/README.md) | Palmer Penguins | CRISP-DM end to end |
| 04 | Python for data science | [`04-python-for-data-science`](../04-python-for-data-science/README.md) | Palmer Penguins | Types, control flow, functions, classes, files, NumPy, pandas |
| 05 | Python project | [`05-python-project`](../05-python-project/README.md) | books.toscrape.com | Web scraping, cleaning, dashboard |
| 06 | Databases and SQL | [`06-databases-and-sql`](../06-databases-and-sql/README.md) | OpenFlights | Schema design, joins, aggregation, views, transactions |
| 07 | Data analysis | [`07-data-analysis`](../07-data-analysis/README.md) | California Housing | EDA, feature engineering, regression, evaluation |
| 08 | Data visualisation | [`08-data-visualization`](../08-data-visualization/README.md) | Gapminder, USGS quakes | Matplotlib/Seaborn, Plotly/Dash, Folium |
| 09 | Machine learning | [`09-machine-learning`](../09-machine-learning/README.md) | UCI Adult/Wine/Wholesale | Regression, classification, clustering, pipelines/tuning |
| Capstone | Applied capstone | [`falcon9-landing-analysis`](https://github.com/malikb0/falcon9-landing-analysis) | SpaceX launch records | Full applied workflow (separate repo) |

## How the skills build on each other

```
concepts ─▶ tooling ─▶ methodology
                │
                ▼
        python fundamentals
                │
                ▼
     data acquisition (scraping / SQL)
                │
                ▼
    exploratory analysis ─▶ visualisation
                │
                ▼
          machine learning
                │
                ▼
             capstone
```

The ordering is deliberate: each project can be attempted with only the skills from the
projects above it, and nothing depends on private or paid resources.
