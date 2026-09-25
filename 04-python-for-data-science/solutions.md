# Solutions — Python for data science

Worked solutions to the exercise sets in [`README.md`](README.md) and the notebooks. Each
solution states the idea first, then shows code you can paste into a notebook cell. The examples
assume:

```python
from ds_practice import load_penguins

penguins = load_penguins()
```

## Notebook 01 — Language basics

### 1. Count penguins per island with a loop

The idea is a **tally**: start with an empty `dict`, then for each island add one to whatever
count is already stored. `.get(island, 0)` supplies the zero on first sight.

```python
counts = {}
for island in penguins["island"]:
    counts[island] = counts.get(island, 0) + 1

print(counts)
```

You can check it against pandas: `penguins["island"].value_counts().to_dict()` should match.

### 2. Distinct species and the flipper range

`set` collapses duplicates; `min` and `max` over a tuple give a fixed record. Convert the column
to Python values with `.tolist()` so the result is a plain `set` / `tuple`, not a pandas object.

```python
species = set(penguins["species"])
flippers = penguins["flipper_length_mm"].dropna().tolist()
flipper_range = (min(flippers), max(flippers))

print(sorted(species))
print(flipper_range)
```

### 3. `safe_mean`

Returning `None` for an empty input is a deliberate contract. The docstring records it so callers
know to check.

```python
def safe_mean(values):
    """Return the arithmetic mean, or None for an empty sequence."""
    values = list(values)
    if not values:
        return None
    return sum(values) / len(values)

print(safe_mean([]))
print(round(safe_mean(penguins["body_mass_g"].dropna().tolist()[:10]), 1))
```

## Notebook 02 — Functions and classes

### 1. Parameterised `mass_band`

Defaults keep the common call short; keyword arguments let a caller move the boundaries.

```python
def mass_band(grams, light=3500, heavy=4500):
    if grams < light:
        return "light"
    if grams < heavy:
        return "medium"
    return "heavy"

print(mass_band(4000))                                  # medium
print(mass_band(4000, light=3000, heavy=3900))          # heavy
```

### 2. The five longest flippers

A `lambda` provides the comparison key. Sorting descending and slicing takes the top five.

```python
rows = penguins.dropna(subset=["flipper_length_mm"]).to_dict("records")
top_five = sorted(rows, key=lambda row: row["flipper_length_mm"], reverse=True)[:5]

for row in top_five:
    print(f"{row['species']:<10} {row['flipper_length_mm']} mm")
```

### 3. Extend the `Penguin` class

Methods reuse the stored data; `summary` returns a string instead of printing, which makes it
reusable.

```python
class Penguin:
    def __init__(self, species, island, body_mass_g, flipper_length_mm):
        self.species = species
        self.island = island
        self.body_mass_g = float(body_mass_g)
        self.flipper_length_mm = float(flipper_length_mm)

    def is_gentoo(self):
        return self.species == "Gentoo"

    def summary(self):
        return f"{self.species} on {self.island}: {self.body_mass_g:.0f} g, {self.flipper_length_mm:.0f} mm"

bird = Penguin("Gentoo", "Biscoe", 5000, 231)
print(bird.is_gentoo())
print(bird.summary())
```

## Notebook 03 — Files and data I/O

### 1. CSV round trip

`DictWriter` takes the header from `fieldnames`, and `to_dict("records")` gives one `dict` per
row. Read the file back and count the data rows (the header is not a row for `DictReader`).

```python
import csv
import tempfile
from pathlib import Path

workdir = Path(tempfile.mkdtemp(prefix="exercise_"))
columns = ["species", "island", "bill_length_mm", "body_mass_g"]
sample = penguins[columns].head(10)

with (workdir / "exercise.csv").open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=columns)
    writer.writeheader()
    writer.writerows(sample.to_dict("records"))

with (workdir / "exercise.csv").open(encoding="utf-8", newline="") as fh:
    recovered = list(csv.DictReader(fh))

print("rows recovered:", len(recovered))   # 10
```

### 2. Island counts as JSON

`to_dict()` turns the pandas result into a plain mapping, which `json.dump` can serialise. The
`assert` documents the round trip.

```python
import json

counts = penguins["island"].value_counts().to_dict()
(json_path := workdir / "islands.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")

loaded = json.loads(json_path.read_text(encoding="utf-8"))
assert loaded == counts
print(loaded)
```

### 3. A Gentoo subset with pandas

Filtering, selecting columns, and writing without the index is the whole job.

```python
gentoo = penguins.loc[penguins["species"] == "Gentoo", ["species", "island", "flipper_length_mm"]]
gentoo.to_csv(workdir / "gentoo.csv", index=False)

again = pd.read_csv(workdir / "gentoo.csv")
print("rows:", len(again), "| mean flipper:", round(again["flipper_length_mm"].mean(), 1))
```

## Notebook 04 — NumPy and pandas

### 1. Standardise within each species

`groupby(...).transform(...)` returns a series aligned to the original rows, so the z-score can be
assigned back as a column. Each species' mean z-score is then approximately zero by construction.

```python
clean = penguins.dropna(subset=["body_mass_g"]).copy()
clean["mass_z"] = clean.groupby("species")["body_mass_g"].transform(
    lambda values: (values - values.mean()) / values.std()
)

print(clean.groupby("species")["mass_z"].mean().round(6))
```

### 2. Count long flippers with a mask

`dropna().to_numpy()` gives a clean array; the mask both selects and counts.

```python
flippers = penguins["flipper_length_mm"].dropna().to_numpy()
long_flippers = flippers[flippers > 220]

print("count:", long_flippers.size)
print("share:", round(long_flippers.size / flippers.size, 3))
```

### 3. Merge an island lookup, then pivot

The lookup has one row per island, so the merge keeps the penguin row count. The pivot puts
species on the rows and region on the columns.

```python
island_region = pd.DataFrame(
    {"island": ["Biscoe", "Dream", "Torgersen"], "region": ["West", "West", "East"]}
)
merged = penguins.merge(island_region, on="island", how="left")
assert len(merged) == len(penguins)

grid = merged.pivot_table(index="species", columns="region", values="body_mass_g", aggfunc="mean")
print(grid.round(0))
```

## Notebook 05 — APIs and HTTP

The helper below is shared by all three solutions. It returns `(data, error)` so callers can
distinguish an empty page from a failed request.

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
TIMEOUT = 10


def fetch_page(page=1, limit=5, retries=3, base_url=BASE_URL, timeout=TIMEOUT):
    """Return (posts, error). Retries transient failures, then gives up cleanly."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                base_url,
                params={"_page": page, "_limit": limit},
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as exc:
            if attempt == retries:
                return [], type(exc).__name__
    return [], "unknown"
```

### 1. Fetch page 2

Page 1 and page 2 should not share ids, which confirms the pagination is moving.

```python
page_one, err_one = fetch_page(page=1, limit=5)
page_two, err_two = fetch_page(page=2, limit=5)

if err_one or err_two:
    print(f"offline or error: {err_one or err_two}")
else:
    ids_one = {post["id"] for post in page_one}
    ids_two = {post["id"] for post in page_two}
    print("overlap:", ids_one & ids_two)          # empty set
    for post in page_two:
        print(post["id"], post["title"][:50])
```

### 2. A retrying helper

The loop above is the solution: it attempts the request up to `retries` times and returns `[]`
with the error name only after the final failure. In a real job you would add a short back-off
between attempts (for example `time.sleep(2 ** attempt)`) and retry only on 5xx or connection
errors, not on a `404`.

### 3. Busiest user among the first ten posts

Collect ten posts with `_limit=10`, count `userId` with `Counter`, and take the maximum.

```python
from collections import Counter

posts, error = fetch_page(page=1, limit=10)
if error:
    print(f"skipped: {error}")
else:
    per_user = Counter(post["userId"] for post in posts)
    busiest = per_user.most_common(1)[0]
    print(per_user)
    print("busiest user:", busiest[0], "with", busiest[1], "posts")
```

## A note on checking your work

For notebooks 01–04 you can compare every hand-rolled result with the pandas equivalent — the
`dict` tally against `value_counts()`, the `safe_mean` against `Series.mean()`. When the two
agree, you understand both the language and the library. For notebook 05 the useful check is the
opposite: disconnect the network and confirm the notebook still finishes with clear messages
instead of a traceback.
