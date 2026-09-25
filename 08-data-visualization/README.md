# 08 — Data visualisation

A chart is an argument. This module practices the full visualisation stack — Matplotlib and
Seaborn for static figures, Plotly for interactive exploration, Dash for a dashboard, and Folium
for maps — on the Gapminder panel and the USGS earthquake feed.

**Datasets:** Gapminder (CC BY 4.0) and USGS all-month earthquakes (public domain). Fetch them
with:

```bash
python scripts/download_data.py --module 08
```

## Learning objectives

By the end of this module you will be able to:

- choose an appropriate chart type for a question and label it correctly;
- build line, area, histogram, bar, box, scatter, bubble, waffle, and word-frequency charts;
- add a fitted trend line while avoiding causal over-claiming;
- build interactive Plotly figures and export them to HTML;
- assemble a Dash dashboard from components and callbacks;
- map points and regions with Folium and compute proximity with the haversine formula;
- apply colour and accessibility judgement.

## Prerequisites

- Module [`04-python-for-data-science`](../04-python-for-data-science/README.md) for pandas.
- Module [`07-data-analysis`](../07-data-analysis/README.md) for exploratory habits.
- No design background; the module explains the reasoning behind each choice.

## Dataset

**Gapminder** tracks life expectancy, population, and GDP per capita for ~140 countries every five
years from 1952 to 2007. **USGS** publishes a rolling feed of earthquakes from the last 30 days,
including magnitude, depth, and location. Both are fetched by `scripts/download_data.py`; see
[`docs/datasets.md`](../docs/datasets.md) and [`docs/data-dictionary.md`](../docs/data-dictionary.md)
for provenance, licenses, and field definitions.

## Topics covered

| Notebook | Topic |
|---|---|
| [`notebooks/01-matplotlib-fundamentals.ipynb`](notebooks/01-matplotlib-fundamentals.ipynb) | Figure/Axes anatomy, line/area/histogram/bar |
| [`notebooks/02-statistical-and-specialty-plots.ipynb`](notebooks/02-statistical-and-specialty-plots.ipynb) | Box, scatter, bubble, regression, waffle, word frequency |
| [`notebooks/03-plotly-interactive.ipynb`](notebooks/03-plotly-interactive.ipynb) | Plotly Express, hover, log axes, animation, HTML export |
| [`notebooks/04-dash-app.ipynb`](notebooks/04-dash-app.ipynb) | Components, callbacks, and the [`app/`](app/README.md) dashboard |
| [`notebooks/05-geospatial-folium.ipynb`](notebooks/05-geospatial-folium.ipynb) | Markers, choropleth, proximity, map choices |

Reusable figure builders live in [`charts.py`](charts.py); the plain-language explainer is
[`concepts.md`](concepts.md); worked answers are in [`solutions.md`](solutions.md).

## How to run

```bash
make install
python scripts/download_data.py --module 08
jupyter lab 08-data-visualization/notebooks/
python 08-data-visualization/app/dashboard.py      # optional dashboard at :8050
```

Notebooks run top to bottom once the CSVs exist. Folium maps need network access **when displayed**
to fetch basemap tiles; building the map object is offline. The dashboard is best run from a
terminal rather than inside a notebook.

## Exercises

1. **Chart type.** Plot GDP over time on a log axis and explain the scale choice; overlay 1952 and
   2007 life-expectancy histograms; build a 2×3 grid of continent trends.
2. **Statistical plots.** Compare a pie with a waffle for population shares; re-encode bubble
   radius versus area; box-plot magnitude by `magType`.
3. **Interactive.** Limit hover fields and justify; compare faceted with multi-line charts; judge
   whether an interactive chart changes a decision.
4. **Dash.** Propose a country dropdown control and classify the callback's Input and Output; test
   `filter_data` edge cases.
5. **Maps.** Encode magnitude as area; compare earthquake counts with rates; find the nearest
   quakes to a city of your choice.

## Limitations

Interactive and map outputs require a browser and, for tiles, a network connection, so static PNGs
are still needed for reports. The Gapminder panel is five-yearly and ends in 2007. The USGS feed is
a 30-day rolling window, not a long historical record. Colour palettes are chosen for clarity but
checked only informally for accessibility; a production dashboard would test them against
colour-blind simulation and provide an alternative table view.
