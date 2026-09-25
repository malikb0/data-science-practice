#!/usr/bin/env python3
"""Interactive dashboard for the scraped book catalogue.

Run directly to serve locally::

    python 05-python-project/app/dashboard.py

The data-loading and figure-building functions are importable and tested without
starting a server.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px

DEFAULT_PORT = 8050


def find_repo_root(start: Path | None = None) -> Path:
    here = (start or Path.cwd()).resolve()
    for base in [here, *here.parents]:
        if (base / "scripts" / "download_data.py").exists():
            return base
    return here


def load_books(path: str | Path | None = None) -> pd.DataFrame:
    """Load the scraped catalogue, raising a helpful error if it is absent."""
    if path is None:
        path = find_repo_root() / "data" / "raw" / "books.csv"
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: python scripts/download_data.py --module 05"
        )
    frame = pd.read_csv(path)
    return prepare(frame)


def prepare(frame: pd.DataFrame) -> pd.DataFrame:
    """Add the derived ``value`` column (rating per pound)."""
    frame = frame.copy()
    if {"rating", "price_gbp"}.issubset(frame.columns):
        frame["value"] = frame["rating"] / frame["price_gbp"]
    return frame


def price_histogram(frame: pd.DataFrame):
    """Price distribution as a Plotly figure."""
    fig = px.histogram(
        frame,
        x="price_gbp",
        nbins=15,
        title="Distribution of book prices",
        labels={"price_gbp": "Price (GBP)"},
    )
    return fig


def rating_bar(frame: pd.DataFrame):
    """Mean price per star rating as a Plotly figure."""
    grouped = frame.groupby("rating", as_index=False)["price_gbp"].mean()
    fig = px.bar(
        grouped,
        x="rating",
        y="price_gbp",
        title="Mean price by star rating",
        labels={"rating": "Rating (stars)", "price_gbp": "Mean price (GBP)"},
    )
    return fig


def create_app(frame: pd.DataFrame):
    """Build the Dash application from an already-loaded frame."""
    from dash import Dash, Input, Output, dcc, html

    app = Dash(__name__)
    ratings = sorted(frame["rating"].dropna().unique().tolist())

    app.layout = html.Div(
        style={"fontFamily": "system-ui, sans-serif", "maxWidth": "1000px", "margin": "auto"},
        children=[
            html.H1("Book catalogue dashboard"),
            html.P(f"{len(frame)} titles scraped from books.toscrape.com."),
            html.Label("Minimum rating"),
            dcc.Slider(
                id="min-rating",
                min=min(ratings),
                max=max(ratings),
                value=min(ratings),
                step=1,
                marks={int(r): f"{int(r)}★" for r in ratings},
            ),
            dcc.Graph(id="price-hist"),
            dcc.Graph(id="rating-bar"),
        ],
    )

    @app.callback(
        Output("price-hist", "figure"),
        Output("rating-bar", "figure"),
        Input("min-rating", "value"),
    )
    def update(min_rating):
        subset = frame[frame["rating"] >= min_rating]
        return price_histogram(subset), rating_bar(subset)

    return app


def main() -> None:
    frame = load_books()
    app = create_app(frame)
    app.run(debug=False, port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
