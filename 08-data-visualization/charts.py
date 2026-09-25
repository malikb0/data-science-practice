"""Reusable chart builders for the visualisation module.

Plotly figures are returned rather than shown, so notebooks and the Dash app can
share them. Folium is imported lazily.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px

THEME = "plotly_white"


def line_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    return px.line(df, x=x, y=y, color=color, title=title, template=THEME)


def area_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    return px.area(df, x=x, y=y, color=color, title=title, template=THEME)


def histogram(df: pd.DataFrame, x: str, color: str | None = None, nbins: int = 30, title: str = ""):
    return px.histogram(df, x=x, color=color, nbins=nbins, title=title, template=THEME)


def bar_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    return px.bar(df, x=x, y=y, color=color, title=title, template=THEME)


def box_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    return px.box(df, x=x, y=y, color=color, title=title, template=THEME)


def scatter_chart(df: pd.DataFrame, x: str, y: str, size: str | None = None,
                  color: str | None = None, hover: list[str] | None = None, title: str = ""):
    return px.scatter(
        df, x=x, y=y, size=size, color=color, hover_name=hover[0] if hover else None,
        title=title, template=THEME,
    )


def bubble_chart(df: pd.DataFrame, x: str, y: str, size: str, color: str,
                 hover: str | None = None, title: str = ""):
    return px.scatter(
        df, x=x, y=y, size=size, color=color, hover_name=hover,
        size_max=60, title=title, template=THEME,
    )


def choropleth(df: pd.DataFrame, locations: str, values: str, title: str = "",
               locationmode: str = "country names", color_continuous_scale: str = "Viridis"):
    return px.choropleth(
        df, locations=locations, color=values, locationmode=locationmode,
        title=title, template=THEME, color_continuous_scale=color_continuous_scale,
    )


def folium_map(df: pd.DataFrame, lat: str = "latitude", lon: str = "longitude",
               popup: str | None = None, zoom_start: int = 2, tiles: str = "OpenStreetMap"):
    """Return a folium Map with one marker per row."""
    import folium

    centre = [float(df[lat].mean()), float(df[lon].mean())]
    fmap = folium.Map(location=centre, zoom_start=zoom_start, tiles=tiles)
    for row in df.itertuples(index=False):
        label = getattr(row, popup) if popup else None
        folium.CircleMarker(
            location=[getattr(row, lat), getattr(row, lon)],
            radius=3, color="#c0392b", fill=True, fill_opacity=0.6,
            popup=str(label) if label is not None else None,
        ).add_to(fmap)
    return fmap
