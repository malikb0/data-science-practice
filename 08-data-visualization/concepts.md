# Concepts — data visualisation

A plain-language companion to the five notebooks, covering the grammar of charts and the tools used
to build them.

## Start from the question

Every chart answers a question, and the question determines the chart:

- "How has this changed over time?" → **line**.
- "How is this value distributed?" → **histogram** or **box**.
- "How do two variables relate?" → **scatter** (add a fitted line if useful).
- "How do categories compare?" → **bar**.
- "How do parts make a whole?" → **stacked bar** or **waffle** (pie only for two or three parts).
- "Where is this?" → **marker map** or **choropleth**.

If you cannot state the question, the chart will not help.

## Matplotlib anatomy

Matplotlib has two objects. The **Figure** is the whole canvas; the **Axes** is one plot area with
its own x and y axes, ticks, and labels. A figure can hold several axes (a grid of panels).

```python
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, y)
ax.set_title("Title")
ax.set_xlabel("Time (years)")
ax.set_ylabel("Value (units)")
ax.legend(frameon=False)
fig.tight_layout()
```

`fig.tight_layout()` stops labels overlapping. Always include units in axis labels, because a
number without units is not information.

## Aggregation before plotting

Raw rows rarely make a readable chart. Decide the unit of analysis first:

```python
by_year = frame.groupby("year")["value"].mean()
```

Plotting one line per country when the question is about the world mean produces a hairball. The
aggregation *is* the analysis; the chart only shows it.

## Seaborn adds statistics

Seaborn builds on Matplotlib and makes statistical layers short: `sns.boxplot`, `sns.regplot`,
`sns.scatterplot`, and themes via `sns.set_theme()`. The `ds_practice.set_theme()` helper applies a
consistent theme and falls back to a built-in Matplotlib style if Seaborn is absent.

## Interactive versus static

Plotly figures are JavaScript objects described in Python. Interactivity helps when data is dense
or multi-dimensional: hovering reveals exact values and the legend filters series. It is overkill
for a single number, and it cannot be embedded in a PDF or read by a screen reader. A sound
approach is to explore interactively and publish a static figure, with a data table for
accessibility.

```python
import plotly.express as px
fig = px.scatter(frame, x="gdp", y="life", size="pop", color="continent", log_x=True)
fig.show()
```

## Dash in three parts

A Dash app is:

1. a **layout** — a tree of components (`html.Div`, `dcc.Graph`, `dcc.Slider`);
2. **callbacks** — functions that take `Input` values and return an `Output`;
3. a **server** — usually started with `app.run_server()`.

Keeping filtering and figure building in plain functions makes them testable without a browser.

## Maps

- **Marker maps** place one symbol per observation.
- **Choropleths** shade regions by a value and require joining the data to region boundaries.
- **Proximity** uses the haversine formula for great-circle distance between two coordinates.

Pitfalls: a choropleth hides within-region variation; raw counts favour large regions while rates
do not; every projection distorts area or shape. Folium maps fetch basemap tiles from the network
when displayed, so they are not fully offline.

## Colour and accessibility

Encode magnitude with a perceptually uniform, colour-blind-safe palette (for example Viridis)
rather than a rainbow. Do not rely on colour alone to carry meaning; use shape, labels, or
annotations as well. Ensure text has sufficient contrast, and prefer direct labels over legends
when a chart is small. Accessibility is part of correctness, not decoration.
