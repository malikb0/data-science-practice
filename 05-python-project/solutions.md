# Worked solutions

Answers to the exercises in [`README.md`](README.md) and at the end of each notebook. Each
solution is code you can paste into a cell, followed by a short explanation of why it works.
For the scraping answers, network access is assumed; the parsing answers can all be tested
offline.

## README exercises

### 1. Scrape the whole catalogue

Keep requesting pages until one comes back empty, but stop no later than page 60.

```python
import time
from bs4 import BeautifulSoup

from scrape import parse_card  # or paste the notebook definition of parse_card

BASE = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "data-science-practice/1.0 (+portfolio scraping example)"}
MAX_PAGES = 60


def scrape_all(max_pages: int = MAX_PAGES, delay: float = 0.5) -> list[dict]:
    rows = []
    for page in range(1, max_pages + 1):
        response = requests.get(
            BASE.format(page), headers=HEADERS, timeout=30
        )
        if response.status_code != 200:
            break
        cards = BeautifulSoup(response.text, "html.parser").select(
            "article.product_pod"
        )
        if not cards:
            break
        rows.extend(parse_card(card) for card in cards)
        time.sleep(delay)
        print(f"page {page}: running total {len(rows)}")
    return rows


all_books = scrape_all()
print("total rows:", len(all_books))
```

The catalogue has 50 pages with 20 books each, so a complete run collects **1,000 rows**. The
loop stops early for two reasons: a non-200 status (for example 404 once the pages run out)
or a page with no product cards. `MAX_PAGES = 60` is the safety net — if the markup ever
changes so that a broken page still returns cards, the loop still ends after a bounded number
of requests instead of running forever.

### 2. Add the category

The product page carries a breadcrumb: `Home` → `Books` → the category → the title. The
category is the second-to-last list item.

```python
import requests
from bs4 import BeautifulSoup

product_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(
    product_url,
    headers={"User-Agent": "data-science-practice/1.0"},
    timeout=30,
)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

crumbs = soup.select("ul.breadcrumb li")
category = crumbs[-2].get_text(strip=True)
print("category:", category)  # -> Poetry
```

The `active` crumb is the book title, so the category sits immediately before it. To add this
to every row you would fetch each book's `url` once, parse this field, and merge it back:

```python
def category_for(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    crumbs = BeautifulSoup(resp.text, "html.parser").select("ul.breadcrumb li")
    return crumbs[-2].get_text(strip=True) if len(crumbs) >= 2 else ""


# For a small scrape:
for row in all_books:
    row["category"] = category_for(row["url"])
    time.sleep(0.5)
```

This doubles the number of requests (one per book plus one per list page), so it is a good
place to add a delay between calls and, ideally, a cache of pages already fetched.

### 3. Price bands

Split the prices into four equal-sized groups with `pandas.qcut`, then summarise the rating in
each band.

```python
import pandas as pd

from ds_practice import load_books

books = load_books()
books["price_band"] = pd.qcut(
    books["price_gbp"], q=4, labels=["Q1 (cheapest)", "Q2", "Q3", "Q4 (priciest)"]
)

summary = (
    books.groupby("price_band", observed=True)
    .agg(books=("title", "count"), mean_price=("price_gbp", "mean"),
         mean_rating=("rating", "mean"))
    .round(2)
)
print(summary)
print("correlation:", books["price_gbp"].corr(books["rating"]).round(3))
```

On this fictional catalogue the mean rating is roughly flat across the four bands and the
correlation is close to zero, so **rating does not rise with price** here. `observed=True`
keeps pandas from listing empty categories once the bands are cut. The exact numbers come
from the data, not from this text — always print the table before drawing a conclusion.

### 4. Guard the parser offline

`parse_page` takes an HTML string, so a small saved fragment is enough to test it with no
network. This mirrors `tests/test_05_python_project.py`.

```python
from bs4 import BeautifulSoup

from scrape import parse_page

PAGE_HTML = """
<div>
  <article class="product_pod">
    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html"
           title="A Light in the Attic">A Light in the Attic</a></h3>
    <p class="star-rating Three"></p>
    <p class="price_color">£51.77</p>
    <p class="instock availability">In stock</p>
  </article>
  <article class="product_pod">
    <h3><a href="catalogue/tipping-the-velvet_999/index.html"
           title="Tipping the Velvet">Tipping the Velvet</a></h3>
    <p class="star-rating One"></p>
    <p class="price_color">£53.74</p>
    <p class="instock availability">In stock</p>
  </article>
</div>
"""


def test_parse_page_reads_every_card():
    rows = parse_page(PAGE_HTML)
    assert len(rows) == 2
    assert rows[0]["title"] == "A Light in the Attic"
    assert rows[0]["price_gbp"] == 51.77
    assert rows[0]["rating"] == 3
    assert rows[1]["rating"] == 1
```

The test asserts facts about the fixture, so it stays green whether or not the live site is
reachable. Run it with `pytest`. Tests like this are how you protect the parser while you
experiment with selectors.

## Notebook 01 exercises

### 1. Scrape pages 1–3 with per-page counts

```python
import time
import requests
from bs4 import BeautifulSoup

BASE = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "data-science-practice/1.0 (+portfolio scraping example)"}

per_page = {}
for page in range(1, 4):
    response = requests.get(BASE.format(page), headers=HEADERS, timeout=30)
    if response.status_code != 200:
        per_page[page] = 0
        continue
    cards = BeautifulSoup(response.text, "html.parser").select("article.product_pod")
    per_page[page] = len(cards)
    time.sleep(0.5)

print(per_page, "total:", sum(per_page.values()))
```

Each full catalogue page holds 20 cards, so expect `{1: 20, 2: 20, 3: 20}` and a total of 60.
A page can return fewer than 20 when it is the **last** page (the remainder does not divide
evenly), when the request failed (status other than 200), or when the site's markup changed
so that the card selector no longer matches. That is why we count what we actually parsed
rather than assuming 20.

### 2. Retry a failing request

```python
import time
import requests

HEADERS = {"User-Agent": "data-science-practice/1.0 (+portfolio scraping example)"}


def fetch_with_retries(url: str, attempts: int = 3, timeout: int = 30) -> str:
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            last_error = exc
            print(f"attempt {attempt} failed: {exc}")
            if attempt < attempts:
                time.sleep(attempt)  # 1 s, then 2 s
    raise last_error


good = fetch_with_retries("http://books.toscrape.com/catalogue/page-1.html")
print("good page chars:", len(good))

try:
    fetch_with_retries("http://books.toscrape.com/catalogue/page-9999.html")
except requests.RequestException as exc:
    print("gave up cleanly:", exc)
```

Wait one second longer on each attempt (`time.sleep(attempt)`) to give a struggling server
room to recover. Re-raising the final error keeps the failure visible; swallowing it would
hide a real outage.

### 3. Parse from a saved file

```python
from pathlib import Path

from bs4 import BeautifulSoup

out_dir = Path("data/raw")
out_dir.mkdir(parents=True, exist_ok=True)
page_file = out_dir / "page-1.html"

# Save the HTML we already downloaded.
if html:
    page_file.write_text(html, encoding="utf-8")

# Read it back and parse with no network involved.
saved = page_file.read_text(encoding="utf-8")
offline_cards = BeautifulSoup(saved, "html.parser").select("article.product_pod")
print("cards from disk:", len(offline_cards))
assert len(offline_cards) == 20
```

Because the parser only ever sees a string, once the HTML is on disk the rest of the pipeline
works without a connection. This is the same idea behind the test in `tests/`: keep the
network at the edge and make everything downstream a pure function of saved input.

## Notebook 02 exercises

### 1. Price spread and a boxplot

```python
from ds_practice import load_books, set_theme, boxplot
import pandas as pd

set_theme()
books = load_books()
price = books["price_gbp"]

q1, q3 = price.quantile([0.25, 0.75])
print("count:", price.count())
print("mean:", round(price.mean(), 2))
print("median:", round(price.median(), 2))
print("IQR:", round(q3 - q1, 2))
threshold = price.quantile(0.90)
print("books above 90th percentile:", int((price > threshold).sum()))
print("90th percentile:", round(threshold, 2))

fig, ax = boxplot(price, title="Spread of book prices", ylabel="Price (GBP)")
```

The median and the mean answer slightly different questions: the mean is sensitive to a few
expensive books, the median is not. The IQR (the middle 50% of prices) describes the typical
spread, and the 90th-percentile count says how many books sit in the expensive tail. A boxplot
draws the same story: the box is the IQR, the line inside is the median, and the whiskers and
dots show the rest.

### 2. Price by rating

```python
from ds_practice import load_books
import pandas as pd

books = load_books()
by_rating = (
    books.groupby("rating")["price_gbp"]
    .agg(count="count", mean="mean", median="median")
    .round(2)
)
print(by_rating)

cheapest = by_rating["mean"].idxmin()
priciest = by_rating["mean"].idxmax()
gap = by_rating.loc[priciest, "mean"] - by_rating.loc[cheapest, "mean"]
print(f"most expensive rating: {priciest}; gap to cheapest: {gap:.2f} GBP")
```

Read the table rather than assuming a pattern. On this sandbox the mean and median prices are
close across ratings and the gap between the most and least expensive rating is small
relative to the overall spread, which is consistent with the near-zero correlation the
notebook reports. A large difference in `count` between ratings would also be a warning that
a mean is being driven by very few books.

### 3. Rethinking value

```python
from ds_practice import load_books
import pandas as pd

books = load_books()
books["value"] = books["rating"] / books["price_gbp"]
books["value_norm"] = (books["rating"] / 5) / books["price_gbp"]

top_raw = books.nlargest(5, "value")["title"].tolist()
top_norm = books.nlargest(5, "value_norm")["title"].tolist()

print("top by rating/price:     ", top_raw)
print("top by (rating/5)/price: ", top_norm)
print("same set:", set(top_raw) == set(top_norm))
```

Dividing every rating by the same constant (5) cannot change the **order** of the scores, only
their scale, so the two `nlargest` lists are identical. That is a useful check: any transform
that is a positive constant multiple cannot reorder a ranking. What *would* change the
ranking is a different definition of value — for example subtracting the price, capping the
rating, or dividing by the price rank instead of the price itself. The lesson is that "best
value" is a statement about your scoring rule as much as about the books.
