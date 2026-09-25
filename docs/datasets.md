# Datasets

No data is committed to this repository. Run `python scripts/download_data.py --all` (or a
single `--module NN`) to fetch and cache the files under `data/raw/`, which is git-ignored.
The table below records the source, license, and citation for each dataset.

| Key | File(s) under `data/raw/` | Source | License | Cite as |
|---|---|---|---|---|
| `penguins` | `penguins.csv` | https://allisonhorst.github.io/palmerpenguins/ | CC0 1.0 | Horst AM, Hill AP, Gorman KB (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin data.* R package v0.1.0. |
| `books` | `books.csv` | http://books.toscrape.com/ | Public scraping sandbox (attribution requested) | Zyte. *books.toscrape.com* — a demo site built for practising web scraping. |
| `openflights` | `airports.dat`, `airlines.dat`, `routes.dat` | https://openflights.org/data.html | ODbL 1.0 | OpenFlights. *Airport, airline and route data.* OpenFlights.org. |
| `california` | `california_housing.csv` | `sklearn.datasets.fetch_california_housing` | Public / BSD-compatible (StatLib) | Pace R.K., Barry R. (1997). *Sparse spatial autoregressions.* Statistics & Probability Letters 33(3), 291–297. |
| `gapminder` | `gapminder.csv` | https://github.com/plotly/datasets/blob/master/gapminderDataFiveYear.csv | CC BY 4.0 | Gapminder Foundation. *Gapminder Data.* gapminder.org. |
| `usgs_quakes` | `usgs_quakes.csv` | https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php | Public domain (U.S. Government work) | U.S. Geological Survey. *Earthquake Hazards Program — real-time feeds.* |
| `adult` | `adult.data` | https://archive.ics.uci.edu/dataset/2/adult | CC BY 4.0 | Becker B., Kohavi R. (1996). *Adult.* UCI Machine Learning Repository. |
| `wine` | `winequality-red.csv` | https://archive.ics.uci.edu/dataset/186/wine+quality | CC BY 4.0 | Cortez P. et al. (2009). *Wine Quality.* UCI Machine Learning Repository. |
| `wholesale` | `wholesale_customers.csv` | https://archive.ics.uci.edu/dataset/292/wholesale+customers | CC BY 4.0 | Cardoso M. (2013). *Wholesale customers.* UCI Machine Learning Repository. |
| `sklearn` | (fetched in-memory) | https://scikit-learn.org/stable/datasets.html | BSD 3-Clause | Pedregosa F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12, 2825–2830. |

## Fetch commands

```bash
python scripts/download_data.py --all          # everything
python scripts/download_data.py --module 03    # just the Penguins data
python scripts/download_data.py --module 06    # OpenFlights tables
python scripts/download_data.py --list         # show available keys
```

Options: `--force` re-downloads even if a cached file exists; `--out DIR` overrides the cache
directory (default `data/raw`). The scraper that builds `books.csv` sleeps between requests and
sends a descriptive user agent.

## Notes on licenses

- **CC0 1.0** — public-domain dedication; no conditions.
- **CC BY 4.0** — reuse permitted with attribution; attribute the original authors.
- **ODbL 1.0** — open database license; attribute OpenFlights and keep derived databases open.
- **Public domain / U.S. Government work** — no copyright restrictions.
- **BSD 3-Clause** — permissive software/data license; keep the copyright notice.

Dataset licenses apply to the data only. The code and prose in this repository are MIT-licensed
(see [`LICENSE`](../LICENSE)); attribution for the certificate that inspired the skill set is in
[`NOTICE.md`](../NOTICE.md).
