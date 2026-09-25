"""Small functions from the Python fundamentals notebooks, packaged for reuse."""
from __future__ import annotations

from collections import Counter
from typing import Iterable


def mass_band(grams: float) -> str:
    """Bucket a mass in grams into light / medium / heavy."""
    if grams < 3500:
        return "light"
    if grams < 4500:
        return "medium"
    return "heavy"


def summarise(values: Iterable[float], round_to: int = 1) -> dict:
    """Return n / mean / min / max for a non-empty sequence."""
    values = list(values)
    if not values:
        raise ValueError("cannot summarise an empty sequence")
    return {
        "n": len(values),
        "mean": round(sum(values) / len(values), round_to),
        "min": min(values),
        "max": max(values),
    }


def band_counts(rows: Iterable[dict], mass_key: str = "mass_g") -> dict:
    """Count how many rows fall in each mass band."""
    bands = (mass_band(row[mass_key]) for row in rows)
    return dict(Counter(bands))
