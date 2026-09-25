"""Reusable parsing helpers for the books.toscrape.com project.

The scraping notebook shows the same logic step by step; this module packages it
so it can be tested with a static HTML fragment, without touching the network.
"""
from __future__ import annotations

from bs4 import BeautifulSoup

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
CATALOGUE_BASE = "http://books.toscrape.com/catalogue/"


def parse_price(text: str) -> float:
    """Convert a price string such as '£51.77' or 'Â£51.77' to a float."""
    cleaned = text.encode("ascii", "ignore").decode().strip()
    return float(cleaned.lstrip("£").strip())


def parse_card(card) -> dict:
    """Extract one book record from a BeautifulSoup product card."""
    title = card.h3.a["title"]
    price = parse_price(card.select_one("p.price_color").get_text(strip=True))
    classes = card.select_one("p.star-rating")["class"]
    rating = next((RATING_WORDS[c] for c in classes if c in RATING_WORDS), None)
    stock = card.select_one("p.instock.availability").get_text(strip=True)
    href = card.h3.a["href"].replace("../", "")
    return {
        "title": title,
        "price_gbp": price,
        "rating": rating,
        "in_stock": "In stock" in stock,
        "url": CATALOGUE_BASE + href,
    }


def parse_page(html: str) -> list[dict]:
    """Parse every product card on a catalogue page."""
    soup = BeautifulSoup(html, "html.parser")
    return [parse_card(card) for card in soup.select("article.product_pod")]
