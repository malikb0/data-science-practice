# 05 — Python project: scraping and analysing a book catalogue

**Skill area:** a complete, small, end-to-end project — acquire data from the web, clean it
into a tidy table, analyse it, and present it.

**Dataset:** [books.toscrape.com](http://books.toscrape.com/), a site built expressly for
practising web scraping. Source, license, and attribution are recorded in
[`docs/datasets.md`](../docs/datasets.md).

## Learning objectives

By the end of this module you can:

- Explain what ethical scraping means and apply its ground rules.
- Send an HTTP request with `requests` and read the response.
- Parse HTML with `BeautifulSoup` and pull fields out with CSS selectors.
- Turn repeated HTML blocks into rows of a tidy table.
- Follow pagination to collect more than one page of results.
- Save a scraped table as CSV and guard the parser with an offline test.
- Explore price, rating, and a defined "value" score with pandas and Matplotlib.
- State clearly what a small, fictional catalogue can and cannot support.

## Prerequisites

- Modules 01–04, or equivalent comfort with Python, pandas, and Matplotlib.
- A working install: `make install` creates `.venv` and installs the pinned packages.
- Internet access for notebook 01 and for the fetch command below. Notebook 02 runs offline.
- Basic familiarity with a terminal and with running Jupyter notebooks.

## Dataset

| Field | Value |
|---|---|
| Source | `http://books.toscrape.com/` |
| Kind | Public scraping sandbox (attribution requested) |
| Size | 1,000 books over 50 catalogue pages, 20 per page |
| Columns | `title`, `price_gbp`, `rating`, `in_stock`, `url` |
| Cache | `data/raw/books.csv` (git-ignored) |

Fetch it with:

```bash
python scripts/download_data.py --module 05
```

The fetch script sends a descriptive user agent and sleeps between requests. Notebook 01
performs the same steps by hand so you can see each one. The helper module
[`scrape.py`](scrape.py) packages the parsing functions (`parse_price`, `parse_card`,
`parse_page`) so they can be exercised against a static HTML fragment without any network
access.

## Topics covered

- **HTTP basics** — requests, responses, status codes, and headers.
- **Polite scraping** — an identifiable user agent, delays between requests, and a small scope.
- **HTML parsing** — tags, attributes, and CSS selectors.
- **Pagination** — walking `page-N.html` URLs until the list runs out.
- **Tidy data** — one row per book, one column per variable.
- **CSV persistence** — writing and reloading `data/raw/books.csv`.
- **Exploratory analysis** — distributions, grouped summaries, and a correlation.
- **Project habits** — acquire, clean, analyse, present, then state the limits.

## How to run

```bash
make install
python scripts/download_data.py --module 05     # or run notebook 01
jupyter lab 05-python-project/notebooks/
python 05-python-project/app/dashboard.py       # then open http://127.0.0.1:8050
```

Run the notebooks in order. Notebook 01 needs the network and writes `data/raw/books.csv`;
notebook 02 reads that file and runs offline. If the file is missing, notebook 02 prints a
clear message instead of failing obscurely. The dashboard in [`app/`](app/README.md) reads
the very same CSV.

| File | Purpose |
|---|---|
| [`notebooks/01-web-scraping.ipynb`](notebooks/01-web-scraping.ipynb) | Fetching, parsing, pagination, saving |
| [`notebooks/02-analysis.ipynb`](notebooks/02-analysis.ipynb) | Price, rating, and value |
| [`scrape.py`](scrape.py) | Reusable, testable parsing helpers |
| [`app/dashboard.py`](app/dashboard.py) | Dash dashboard over the scraped table |

## Exercises

Try these after working through both notebooks. Full worked answers are in
[`solutions.md`](solutions.md).

1. **Scrape the whole catalogue.** Extend the pagination loop to keep going until a page
   returns no product cards, with a hard cap of 60 pages so that a markup change cannot spin
   forever. How many rows do you collect?
2. **Add the category.** Each product page shows a breadcrumb that includes the category
   name. Fetch one product page and parse that category; then describe how you would add it
   to every row of the table.
3. **Price bands.** In notebook 02, split prices into quartiles and show the mean rating per
   band. Does the rating rise with price?
4. **Guard the parser offline.** Write a test for `parse_page` in `scrape.py` using a saved
   HTML snippet, following the pattern in `tests/test_05_python_project.py`. It must pass
   with no network connection.

## Limitations

The catalogue is a fixed teaching site, so its prices and ratings are fictional and are not
representative of any real market. Scraping also depends on the site's markup, which can
change without notice; the parser here is written against the current structure only. The
scrape is deliberately small, does not retry failed requests, and stores no history of past
fetches, so it cannot show how prices move over time.
