"""Module 05 — parsing helpers, dashboard figure builders, and the data contract."""
import pandas as pd
import pytest

from helpers import load_module, require_file

CARD_HTML = """
<article class="product_pod">
  <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
  <p class="star-rating Three"></p>
  <p class="price_color">£51.77</p>
  <p class="instock availability">In stock</p>
</article>
"""


def test_parse_price_variants():
    pytest.importorskip("bs4")
    scrape = load_module("05-python-project/scrape.py", "books_scrape")
    assert scrape.parse_price("£51.77") == 51.77
    assert scrape.parse_price("Â£13.99") == 13.99


def test_parse_card_extracts_fields():
    pytest.importorskip("bs4")
    from bs4 import BeautifulSoup

    scrape = load_module("05-python-project/scrape.py", "books_scrape")
    card = BeautifulSoup(CARD_HTML, "html.parser").select_one("article.product_pod")
    row = scrape.parse_card(card)
    assert row["title"] == "A Light in the Attic"
    assert row["price_gbp"] == 51.77
    assert row["rating"] == 3
    assert row["in_stock"] is True
    assert row["url"].startswith("http://books.toscrape.com/catalogue/")


def test_dashboard_builds_figures_from_synthetic_data():
    pytest.importorskip("plotly")
    dashboard = load_module("05-python-project/app/dashboard.py", "books_dashboard")
    frame = pd.DataFrame(
        {"title": ["a", "b", "c"], "price_gbp": [10.0, 20.0, 30.0], "rating": [1, 3, 5]}
    )
    prepared = dashboard.prepare(frame)
    assert "value" in prepared.columns
    assert dashboard.price_histogram(prepared) is not None
    assert dashboard.rating_bar(prepared) is not None


def test_books_data_contract():
    frame = pd.read_csv(require_file("books.csv"))
    assert {"title", "price_gbp", "rating"}.issubset(frame.columns)
    assert len(frame) >= 20
    assert frame["price_gbp"].between(0, 100).all()
    assert frame["rating"].between(1, 5).all()
