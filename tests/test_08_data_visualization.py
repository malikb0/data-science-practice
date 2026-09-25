"""Module 08 — chart builders, dashboard filters, and data contracts."""
import pandas as pd
import pytest

from helpers import load_module, require_file

GAP = pd.DataFrame(
    {
        "country": ["A", "B", "C", "D"],
        "continent": ["Europe", "Asia", "Asia", "Africa"],
        "year": [2007, 2007, 2002, 2007],
        "lifeExp": [80.0, 70.0, 65.0, 55.0],
        "pop": [10, 100, 50, 20],
        "gdpPercap": [40000, 8000, 3000, 1500],
    }
)


def test_chart_builders_return_figures():
    pytest.importorskip("plotly")
    charts = load_module("08-data-visualization/charts.py", "charts08")
    assert charts.line_chart(GAP, "year", "lifeExp") is not None
    assert charts.bar_chart(GAP, "country", "pop") is not None
    assert charts.box_chart(GAP, "continent", "lifeExp") is not None
    assert charts.bubble_chart(GAP, "gdpPercap", "lifeExp", "pop", "continent") is not None
    assert charts.choropleth(GAP, "country", "lifeExp") is not None


def test_dashboard_filters_and_figure():
    pytest.importorskip("plotly")
    dashboard = load_module("08-data-visualization/app/dashboard.py", "dash08")
    euro = dashboard.filter_data(GAP, continent="Europe", year=2007)
    assert len(euro) == 1
    assert len(dashboard.filter_data(GAP, continent="All", year=None)) == len(GAP)
    assert dashboard.bubble_figure(euro) is not None


def test_create_app_builds_layout():
    pytest.importorskip("dash")
    dashboard = load_module("08-data-visualization/app/dashboard.py", "dash08_app")
    app = dashboard.create_app(GAP)
    assert app.layout is not None


def test_visualisation_data_contracts():
    gapminder = pd.read_csv(require_file("gapminder.csv"))
    assert {"country", "continent", "year", "lifeExp", "pop", "gdpPercap"}.issubset(gapminder.columns)
    assert gapminder["lifeExp"].between(20, 90).all()

    quakes = pd.read_csv(require_file("usgs_quakes.csv"))
    assert {"latitude", "longitude", "mag", "place"}.issubset(quakes.columns)
    assert quakes["latitude"].between(-90, 90).all()
    assert quakes["longitude"].between(-180, 180).all()
