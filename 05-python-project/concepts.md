# Concepts behind the book-catalogue project

This note explains the ideas the two notebooks rely on, in plain language. Read it before
notebook 01 if any of the words below are new.

## What web scraping is

Most websites are written for people: a browser asks a server for a page, the server sends
back HTML, and the browser draws it. Scraping means asking for that same page in code and
reading the HTML directly, so we can turn it into a table. It is worth doing when there is no
download link and no API offering the data in a structured form.

Scraping is not the same as hacking. We only request pages a normal visitor could open, we do
not defeat logins or paywalls, and we do not hammer the server.

## Ethical scraping

A scraper is a guest on someone else's machine. Good manners are simple:

1. **Identify yourself.** Send a `User-Agent` header that names your project, so the site owner
   can see who is calling and contact you if needed. A browser string that pretends to be a
   person is rude; `"data-science-practice/1.0"` is honest.
2. **Slow down.** Put a short delay (`time.sleep`) between requests. Servers are shared, and a
   tight loop looks like an attack.
3. **Take only what you need.** Request the pages the question requires, not the whole site,
   and store only the fields you will use.
4. **Respect the rules.** Check the site's terms and its `robots.txt`; if a site asks scrapers
   to stay away, stay away.
5. **Expect change.** Markup changes; a scraper that shouts "no data" is easier to maintain
   than one that quietly returns empty rows.

`books.toscrape.com` exists precisely so that people can practise these steps. It is a
sandbox, not a real shop, and it asks for attribution rather than forbidding access.

## HTTP in one page

HTTP is a request/response conversation:

- We send a **request**: a method (`GET` for "give me this page"), a URL, some headers, and
  sometimes a body.
- The server sends a **response**: a three-digit **status code** plus a body.
- `200` means "here is the page". `404` means "not found". `500` means "the server broke".
  `403` means "you are not allowed".

```python
import requests

response = requests.get(
    "http://books.toscrape.com/catalogue/page-1.html",
    headers={"User-Agent": "data-science-practice/1.0"},
    timeout=30,
)
response.raise_for_status()   # turn 4xx/5xx into an exception
html = response.text          # the page source as a string
```

`timeout` stops us waiting forever if the server does not answer. `raise_for_status()` makes a
bad status code fail loudly. Catching that exception is how the notebook degrades gracefully
when there is no network: it prints a clear message and skips the rest.

## HTML is a tree

HTML is text, but its structure is a tree of **elements**. Each element has a tag name
(`article`, `h3`, `p`), optional **attributes** (`class="product_pod"`, `href="..."`), and
children.

```html
<article class="product_pod">
  <h3><a href="page-2.html" title="A Light in the Attic">A Light in the Attic</a></h3>
  <p class="price_color">£51.77</p>
  <p class="star-rating Three"></p>
</article>
```

Reading this by hand breaks as soon as the page grows. A parser builds the tree in memory so
we can search it. **CSS selectors** are the query language browsers already use:

| Selector | Meaning |
|---|---|
| `article.product_pod` | every `<article>` whose class contains `product_pod` |
| `p.price_color` | every `<p>` with class `price_color` |
| `p.instock.availability` | every `<p>` carrying both classes |
| `h3 a` | every `<a>` inside an `<h3>` |

`BeautifulSoup` supports these directly through `.select(...)` and `.select_one(...)`.
`.select` returns all matches; `.select_one` returns the first (or `None`). From an element we
read text with `.get_text(strip=True)` and attributes like a dictionary,
`element["title"]`.

A subtle point from this dataset: the star rating is not stored as text. It hides in the
element's class list, `class="star-rating Three"`. We map the word to a number ourselves
(`"Three" -> 3`). Real pages often encode meaning in attributes this way.

## Pagination

A catalogue rarely fits on one page. The site splits it into `page-1.html`,
`page-2.html`, and so on. To collect everything we loop:

1. Fetch page `n`.
2. Parse its cards and add them to the list.
3. If the page has cards, increase `n`; otherwise stop.
4. Sleep briefly between pages.

A **safety cap** on `n` matters. If the site changes so our "is it empty?" check never fires,
an uncapped loop would run for a long time. A cap turns that into a clear, bounded failure.
Following a **"next page" link** found in the HTML is an alternative to guessing URL numbers,
but it depends more on the exact markup.

## The shape of a small end-to-end project

The value of this module is less about any single library and more about the arc:

1. **Acquire** — fetch raw pages and extract a tidy table (notebook 01).
2. **Persist** — write `data/raw/books.csv`, one row per book with named columns.
3. **Check** — inspect types, missing values, and ranges before trusting anything.
4. **Analyse** — ask a few concrete questions: how are prices spread, do ratings track
   price, what would "value" mean here?
5. **Present** — the same CSV feeds a small dashboard, so there is one source of truth.
6. **State limits** — say what the data is, where it came from, and what it cannot support.

Keeping these steps separate is what makes the project maintainable. Each one can be re-run,
tested, or replaced without disturbing the others. `scrape.py` exists for exactly this reason:
the parsing logic lives in one importable, testable place instead of being buried in a
notebook cell.

## A word on "value"

Notebook 02 defines `value = rating / price_gbp`. That is a choice, not a fact. Ratings here
are an **ordinal** scale (stars), so treating "4 stars" as twice "2 stars" is already a
simplification, and a cheap book can look like great value simply because its price is small.
Whenever you invent a score, write down its definition and check whether the ranking it
produces still makes sense.
