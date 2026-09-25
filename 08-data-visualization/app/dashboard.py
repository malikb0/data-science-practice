#!/usr/bin/env python3
"""Gapminder dashboard (Plotly Dash).

Run::

    python scripts/download_data.py --module 08
    python 08-data-visualization/app/dashboard.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px

from ds_practice.data import load_gapminder

DEFAULT_PORT = 8050


def filter_data(frame: pd.DataFrame, continent: str = "All", year: int | None = None) -> pd.DataFrame:
    """Filter by continent ('All' keeps everything) and by an exact year."""
    subset = frame
    if continent and continent != "All":
        subset = subset[subset["continent"] == continent]
    if year is not None:
        subset = subset[subset["year"] == year]
    return subset


def bubble_figure(frame: pd.DataFrame):
    """GDP per capita vs life expectancy, bubble size = population."""
    return px.scatter(
        frame,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        size_max=55,
        log_x=True,
        title="Life expectancy vs GDP per capita",
        labels={"gdpPercap": "GDP per capita (USD, log)", "lifeExp": "Life expectancy (years)"},
        template="plotly_white",
    )


def create_app(frame: pd.DataFrame):
    from dash import Dash, Input, Output, dcc, html

    app = Dash(__name__)
    years = sorted(frame["year"].unique().tolist())
    continents = ["All", *sorted(frame["continent"].unique().tolist())]

    app.layout = html.Div(
        style={"fontFamily": "system-ui, sans-serif", "maxWidth": "1000px", "margin": "auto"},
        children=[
            html.H1("Gapminder dashboard"),
            html.Label("Continent"),
            dcc.RadioItems(
                id="continent",
                options=[{"label": c, "value": c} for c in continents],
                value="All",
                inline=True,
            ),
            html.Label("Year"),
            dcc.Slider(
                id="year",
                min=years[0],
                max=years[-1],
                step=5,
                value=years[-1],
                marks={int(y): str(int(y)) for y in years[::2]},
            ),
            dcc.Graph(id="bubble"),
        ],
    )

    @app.callback(Output("bubble", "figure"), Input("continent", "value"), Input("year", "value"))
    def update(continent, year):
        return bubble_figure(filter_data(frame, continent, year))

    return app


def main() -> None:
    frame = load_gapminder()
    create_app(frame).run(debug=False, port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
