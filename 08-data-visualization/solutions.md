# Solutions — data visualisation

Worked answers to the exercises in [`README.md`](README.md) and at the end of each notebook. All
figures assume the setup below.

```python
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path.cwd().parent))
import charts
from ds_practice import load_gapminder, load_usgs_quakes, set_seed, set_theme

set_seed(42)
set_theme()
gap = load_gapminder()
latest = gap[gap["year"] == gap["year"].max()]
```

## Notebook 01 — Matplotlib fundamentals

### 1. GDP trend on a log axis

```python
world_gdp = gap.groupby("year")["gdpPercap"].mean().reset_index()
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(world_gdp["year"], world_gdp["gdpPercap"], marker="o")
ax.set_yscale("log")
ax.set_title("World mean GDP per capita (log scale)")
ax.set_xlabel("Year")
ax.set_ylabel("GDP per capita (USD, log)")
fig.tight_layout()
plt.show()
```

GDP grows multiplicatively, so equal *ratios* look equal on a log axis. On a linear axis the
recent growth dwarfs the early decades and hides the shape.

### 2. Distribution shift

```python
fig, ax = plt.subplots(figsize=(7, 4))
for year, colour in ((1952, "#4c72b0"), (2007, "#dd8452")):
    ax.hist(gap.loc[gap["year"] == year, "lifeExp"], bins=20, alpha=0.5,
            label=str(year), color=colour)
ax.set_title("Life expectancy in 1952 and 2007")
ax.set_xlabel("Life expectancy (years)")
ax.set_ylabel("Countries")
ax.legend()
fig.tight_layout()
plt.show()
```

The 2007 distribution has shifted right and become taller at the high end, with a thinning lower
tail.

### 3. Small multiples

```python
continents = sorted(gap["continent"].unique())
fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)
for ax, continent in zip(axes.ravel(), continents):
    subset = gap[gap["continent"] == continent].groupby("year")["lifeExp"].mean()
    ax.plot(subset.index, subset.values, marker="o")
    ax.set_title(continent)
    ax.set_xlabel("Year")
    ax.set_ylabel("Life expectancy")
fig.tight_layout()
plt.show()
```

Shared axes let the panels be compared directly; `zip(axes.ravel(), continents)` avoids indexing
arithmetic.

## Notebook 02 — Statistical and specialty plots

### 1. Pie versus waffle

```python
shares = latest.groupby("continent")["pop"].sum()
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(shares.values, labels=shares.index, autopct="%1.0f%%", startangle=90)
ax.set_title("Population share by continent (pie)")
plt.show()
```

The waffle makes the smallest share countable, while the pie forces the reader to compare angles.
For proportions below about 5%, the waffle is clearly easier.

### 2. Radius versus area

```python
sizes_radius = 30 + 600 * (latest["pop"] / latest["pop"].max()) ** 0.5   # radius grows with pop
# compare with sizes_radius_area = 30 + 600 * (pop / max) from the notebook
```

Encoding population in the radius makes the area grow as population squared, so large countries
look overwhelmingly bigger than they are. Area-proportional sizing is the fair choice.

### 3. Magnitude by `magType`

```python
quakes = load_usgs_quakes().dropna(subset=["mag", "magType"])
top_types = quakes["magType"].value_counts().head(5).index.tolist()
fig, ax = plt.subplots(figsize=(7, 4))
ax.boxplot([quakes.loc[quakes["magType"] == t, "mag"] for t in top_types],
           labels=top_types, showfliers=False)
ax.set_title("Magnitude by magnitude type")
ax.set_ylabel("Magnitude")
fig.tight_layout()
plt.show()
```

Small groups such as `mb` may have only a handful of events (check `value_counts()`), so their
boxes are unreliable.

## Notebook 03 — Interactive charts with Plotly

### 1. Hover budget

```python
fig = charts.bubble_chart(latest, x="gdpPercap", y="lifeExp", size="pop",
                          color="continent", hover="country",
                          title="GDP vs life expectancy")
fig.update_xaxes(type="log")
fig.show()
```

Limiting hover to the country name keeps the tooltip readable; extra fields are better shown in a
companion table.

### 2. Small multiples

```python
import plotly.express as px
fig = px.line(gap.groupby(["year", "continent"])["lifeExp"].mean().reset_index(),
              x="year", y="lifeExp", facet_col="continent", facet_col_wrap=3,
              title="Life expectancy by continent (faceted)")
fig.show()
```

Facets remove the overplotting of six lines but make a direct cross-continent comparison harder;
the multi-line chart is better when that comparison is the point.

### 3. Static alternative

For the animated bubble chart, the interactivity is essential to see change over time; a static
chart would need one panel per year. For the bar chart of means, interactivity adds little, since a
static bar already communicates the ranking.

## Notebook 04 — A Dash application

### 1. A country control

Add `dcc.Dropdown(id="country", options=...)` to the layout. The existing continent and year
components remain `Input`s, the new dropdown is a third `Input`, and the `dcc.Graph(id="bubble")`
stays the single `Output`. The callback gains a `country` parameter and filters `filter_data`
further.

### 2. Testing the pure functions

```python
assert len(dashboard.filter_data(gap, continent="All", year=2007)) == len(
    gap[gap["year"] == 2007]
)
assert dashboard.filter_data(gap, continent="Europe", year=1900).empty
```

`All` should keep every continent for the chosen year, and a year with no data should return an
empty frame rather than raising — the callback can then show an empty graph.

### 3. Default view

A sensible default is `continent="All"` and the latest year, which shows every country at the most
recent point. A single continent as the default would hide most of the world on first load.

## Notebook 05 — Geospatial visualisation

### 1. Magnitude as area

```python
strong = quakes.nlargest(50, "mag").copy()
strong["radius"] = (strong["mag"] - strong["mag"].min() + 1) ** 2
m = charts.folium_map(strong, popup="place", zoom_start=2)
m
```

`charts.folium_map` uses a fixed radius; to vary it, pass a radius column and draw the markers in a
short loop, scaling by the square root so area grows with magnitude.

### 2. Counts versus rates

Parsing the country from the `place` string and counting events gives more events in countries that
are large or near many faults. A rate (events per 100,000 km²) would be needed for a fair
comparison, and even then it ignores population exposure.

### 3. Proximity from home

```python
def nearest_to(lat, lon, frame, n=5):
    frame = frame.assign(distance_km=haversine_km(
        lat, lon, frame["latitude"].to_numpy(), frame["longitude"].to_numpy()))
    return frame.nsmallest(n, "distance_km")[["place", "mag", "distance_km"]]

display(nearest_to(51.5074, -0.1278, quakes))   # London
```

Distances depend on the 30-day window; rerunning tomorrow gives different nearest events.
