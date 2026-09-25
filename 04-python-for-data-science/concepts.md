# Concepts — Python for data science

A plain-language companion to the five notebooks. Each section states the idea first, then shows
the smallest example that makes it concrete.

## 1. Values, types, and the four containers

Every value in Python has a **type**. The common ones in data work are `int`, `float`, `str`,
`bool`, and `None`. You rarely need to declare a type; you check it when it matters:

```python
value = 3750
print(type(value).__name__)   # int
print(float(value))           # 3750.0
```

A **container** holds other values. The four built-ins differ along three axes: order, whether
they can change, and whether duplicates are allowed.

- `list` — ordered and changeable; the default sequence.
  `[3750, 3800, 5000]`
- `tuple` — ordered and fixed; good for a record such as `(min, max)`.
- `set` — unordered, unique; perfect for "which distinct species are there?".
- `dict` — maps a key to a value; the natural structure for a tally.

```python
species = ["Adelie", "Gentoo", "Adelie"]
print(sorted(set(species)))          # ['Adelie', 'Gentoo']

counts = {}
for name in species:
    counts[name] = counts.get(name, 0) + 1
print(counts)                        # {'Adelie': 2, 'Gentoo': 1}
```

`counts.get(name, 0)` is the idiom to remember: it returns `0` for a key that is not there yet,
so the first occurrence is not a special case.

## 2. Conditionals, loops, and errors

An `if` / `elif` / `else` chain chooses one branch:

```python
def band(grams):
    if grams < 3500:
        return "light"
    elif grams < 4500:
        return "medium"
    else:
        return "heavy"
```

A `for` loop walks the items of a container. `enumerate` adds an index; `zip` walks two
containers together.

```python
for i, grams in enumerate([3200, 5000]):
    print(i, grams)
```

An **exception** is how Python reports something it cannot do. Instead of guarding every line,
try the operation and catch the specific error you can recover from:

```python
def safe_mean(values):
    values = list(values)
    if not values:
        return None            # a deliberate choice, not a crash
    return sum(values) / len(values)
```

Catch the narrow exception (`ZeroDivisionError`, `KeyError`, `ValueError`) rather than a blanket
`Exception`, so genuine bugs are not hidden. Remember that `float("nan")` — a common "missing
number" marker — silently spreads through arithmetic, so use it only on purpose.

## 3. Functions and lambdas

A **function** names a reusable job. Give it a docstring, sensible defaults, and a clear return:

```python
def mean(values, round_to=1):
    values = list(values)
    return round(sum(values) / len(values), round_to)

print(mean([1, 2, 3]))        # 2.0
print(mean([1, 2, 3], 3))     # 2.0
```

A **lambda** is a one-expression function for throwaway jobs, usually as a `key`:

```python
rows = [{"mass": 3750}, {"mass": 5000}, {"mass": 3400}]
heaviest = sorted(rows, key=lambda row: row["mass"], reverse=True)
```

Prefer a named `def` when the logic has a name worth saying out loud or needs a test.

## 4. Classes

A **class** bundles data with the behaviour that belongs to it. `__init__` sets up an instance,
methods act on it, a `@property` looks like an attribute but is computed, and `__repr__` gives a
readable description.

```python
class Penguin:
    def __init__(self, species, mass_g):
        self.species = species
        self.mass_g = float(mass_g)

    @property
    def band(self):
        return band(self.mass_g)

    def __repr__(self):
        return f"Penguin({self.species!r}, {self.mass_g:.0f} g)"

print(Penguin("Gentoo", 5000))        # Penguin('Gentoo', 5000 g)
```

Reach for a class when several values travel together and the same small rules keep being
applied to them. If you only need one function, write one function.

## 5. Files, CSV, and JSON

Use a **context manager** (`with`) so the file always closes, and pass an encoding so the bytes
are unambiguous:

```python
from pathlib import Path
import json

path = Path("summary.json")
with path.open("w", encoding="utf-8") as fh:
    json.dump({"Adelie": 152, "Gentoo": 123}, fh, indent=2)

data = json.loads(path.read_text(encoding="utf-8"))
```

**CSV** is a text table: simple and universal, but types are not stored, so everything comes back
as a string unless something parses it. **JSON** is text for nested structures (objects, arrays,
numbers) and maps onto `dict` and `list`, which is why APIs speak it. pandas wraps both:

```python
import pandas as pd
df = pd.read_csv("penguins.csv")          # types inferred
df.to_csv("out.csv", index=False)          # no index column
```

Always think about where a file lives. Using a temporary directory for scratch output keeps the
repository clean; `tempfile.mkdtemp()` gives you one.

## 6. NumPy arrays and pandas DataFrames

A NumPy **ndarray** is a typed block of values. Because the block is uniform, arithmetic happens
to the whole thing at once:

```python
import numpy as np
mass = np.array([3750.0, 3800.0, 5000.0])
standardised = (mass - mass.mean()) / mass.std()
print(mass[mass > 4000])          # boolean mask selects elements
```

A pandas **DataFrame** is a table with named, typed columns. The core operations are selection
(`df[["species"]]`), filtering (`df[df["body_mass_g"] > 4000]`), deriving
(`df.assign(mass_kg=df["body_mass_g"] / 1000)`), grouping
(`df.groupby("species")["body_mass_g"].mean()`), and joining
(`df.merge(lookup, on="island", how="left")`).

The mental shift is from "loop over rows and update a total" to "describe the operation on whole
columns". That is what makes pandas and NumPy both faster and shorter.

```python
by_species = df.groupby("species")["body_mass_g"].agg(["count", "mean", "std"])
grid = df.pivot_table(index="species", columns="island", values="body_mass_g")
```

Watch for two silent traps: `groupby` drops missing values, so a mean is computed only over the
rows that have a value; and a `merge` on a non-unique key can multiply rows. Check the row count
after joining.

## 7. Calling a JSON API

An **API** is an agreed way to ask another program for data. A REST API exposes URLs; a `GET`
request reads a resource and returns a status code plus a body, usually JSON.

```python
import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"_page": 1, "_limit": 5},     # requests builds the query string
    timeout=10,                            # never wait forever
)
response.raise_for_status()                # turn 4xx/5xx into an exception
posts = response.json()                    # -> list of dicts
```

**Pagination** is how an API returns long lists in pieces; `_page` and `_limit` are one common
scheme. Keep asking until a page comes back empty.

Network code must assume failure. Catch `requests.RequestException` (the base class for timeouts,
connection errors, and bad statuses) and return something safe such as an empty list, so the rest
of the notebook can print a clear "skipped" message rather than crashing.
