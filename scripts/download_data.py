#!/usr/bin/env python3
"""Fetch and cache the datasets used across the portfolio.

Every function here is independent and writes into ``data/raw`` (git-ignored).
Use ``--module NN`` to fetch a single project's data, or ``--all`` for everything.

Examples
--------
    python scripts/download_data.py --list
    python scripts/download_data.py --module 03
    python scripts/download_data.py --all
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "data" / "raw"
USER_AGENT = "data-science-practice/1.0 (+https://github.com/malikb0/data-science-practice)"


def _fetch(url: str, dest: Path, force: bool = False, timeout: int = 60) -> Path:
    """Download ``url`` to ``dest`` unless it already exists."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        print(f"    cached  {dest.name}")
        return dest
    print(f"    get     {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = resp.read()
    dest.write_bytes(payload)
    print(f"    wrote   {dest.name} ({len(payload):,} bytes)")
    return dest


def download_penguins(out: Path = DEFAULT_OUT, force: bool = False) -> Path:
    """Palmer Penguins measurements (CC0). Used by modules 03 and 04."""
    url = (
        "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/"
        "main/inst/extdata/penguins.csv"
    )
    return _fetch(url, out / "penguins.csv", force)


def download_books(out: Path = DEFAULT_OUT, force: bool = False, pages: int = 5) -> Path:
    """Scrape books.toscrape.com (public scraping sandbox). Used by module 05."""
    dest = out / "books.csv"
    if dest.exists() and not force:
        print(f"    cached  {dest.name}")
        return dest

    import requests
    from bs4 import BeautifulSoup

    out.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    rating_words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    for page in range(1, pages + 1):
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        print(f"    get     {url}")
        resp = session.get(url, timeout=30)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("article.product_pod")
        if not cards:
            break
        for card in cards:
            title = card.h3.a["title"]
            price_text = card.select_one("p.price_color").get_text(strip=True)
            price = float(price_text.encode("ascii", "ignore").decode().lstrip("£"))
            rating_class = card.select_one("p.star-rating")["class"]
            rating = next((rating_words[c] for c in rating_class if c in rating_words), None)
            stock = card.select_one("p.instock.availability").get_text(strip=True)
            rel = card.h3.a["href"]
            rows.append(
                {
                    "title": title,
                    "price_gbp": price,
                    "rating": rating,
                    "in_stock": "In stock" in stock,
                    "url": "http://books.toscrape.com/catalogue/" + rel.replace("../", ""),
                }
            )
        time.sleep(0.5)

    with dest.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"    wrote   {dest.name} ({len(rows)} rows)")
    return dest


def download_openflights(out: Path = DEFAULT_OUT, force: bool = False) -> dict:
    """OpenFlights airport/airline/route tables (ODbL). Used by module 06."""
    base = "https://raw.githubusercontent.com/jpatokal/openflights/master/data"
    files = {}
    for name in ("airports", "airlines", "routes"):
        files[name] = _fetch(f"{base}/{name}.dat", out / f"{name}.dat", force)
    return files


def download_california(out: Path = DEFAULT_OUT, force: bool = False) -> Path:
    """California Housing via scikit-learn's fetcher. Used by module 07."""
    dest = out / "california_housing.csv"
    if dest.exists() and not force:
        print(f"    cached  {dest.name}")
        return dest
    from sklearn.datasets import fetch_california_housing

    print("    get     sklearn.datasets.fetch_california_housing")
    bunch = fetch_california_housing(as_frame=True)
    frame = bunch.frame
    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(dest, index=False)
    print(f"    wrote   {dest.name} ({len(frame)} rows)")
    return dest


def download_gapminder(out: Path = DEFAULT_OUT, force: bool = False) -> Path:
    """Gapminder five-year panel (CC BY 4.0). Used by module 08."""
    url = (
        "https://raw.githubusercontent.com/plotly/datasets/master/"
        "gapminderDataFiveYear.csv"
    )
    return _fetch(url, out / "gapminder.csv", force)


def download_usgs(out: Path = DEFAULT_OUT, force: bool = False) -> Path:
    """USGS all-month earthquake feed (public domain). Used by module 08."""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
    return _fetch(url, out / "usgs_quakes.csv", force)


def download_uci(out: Path = DEFAULT_OUT, force: bool = False) -> dict:
    """UCI Adult, Wine Quality, and Wholesale customers (CC BY 4.0). Module 09."""
    targets = {
        "adult.data": (
            "https://archive.ics.uci.edu/ml/machine-learning-databases/"
            "adult/adult.data"
        ),
        "winequality-red.csv": (
            "https://archive.ics.uci.edu/ml/machine-learning-databases/"
            "wine-quality/winequality-red.csv"
        ),
        "wholesale_customers.csv": (
            "https://archive.ics.uci.edu/ml/machine-learning-databases/"
            "00292/Wholesale%20customers%20data.csv"
        ),
    }
    return {name: _fetch(url, out / name, force) for name, url in targets.items()}


DATASETS = {
    "penguins": download_penguins,
    "books": download_books,
    "openflights": download_openflights,
    "california": download_california,
    "gapminder": download_gapminder,
    "usgs_quakes": download_usgs,
    "uci": download_uci,
}

MODULE_DATASETS = {
    "01": [],
    "02": [],
    "03": ["penguins"],
    "04": ["penguins"],
    "05": ["books"],
    "06": ["openflights"],
    "07": ["california"],
    "08": ["gapminder", "usgs_quakes"],
    "09": ["uci"],
}


def download_for_module(module: str, out: Path, force: bool = False) -> None:
    keys = MODULE_DATASETS.get(module)
    if keys is None:
        raise SystemExit(f"unknown module {module!r}; choose 01-09")
    for key in keys:
        print(f"  [{module}] {key}")
        DATASETS[key](out=out, force=force)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="fetch one module's dataset(s), e.g. 03")
    parser.add_argument("--all", action="store_true", help="fetch every dataset")
    parser.add_argument("--list", action="store_true", help="list dataset keys and stop")
    parser.add_argument("--force", action="store_true", help="re-download even if cached")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="cache directory")
    args = parser.parse_args(argv)

    if args.list:
        for key in DATASETS:
            print(key)
        return 0

    out = args.out.resolve()
    print(f"cache: {out}")
    try:
        if args.all:
            for key, fn in DATASETS.items():
                print(f"[{key}]")
                fn(out=out, force=args.force)
        elif args.module:
            download_for_module(args.module, out, args.force)
        else:
            parser.print_help()
            return 1
    except (urllib.error.URLError, OSError) as exc:
        print(f"download failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
