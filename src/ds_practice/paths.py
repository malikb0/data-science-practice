"""Locate the repository root and the downloaded data files."""
from __future__ import annotations

import os
from pathlib import Path

_MARKERS = (("scripts", "download_data.py"), ("src", "ds_practice"))


def repo_root(start: str | Path | None = None) -> Path:
    """Return the repository root, honouring ``DS_PRACTICE_ROOT`` if set."""
    override = os.environ.get("DS_PRACTICE_ROOT")
    if override:
        return Path(override).resolve()
    base = Path(start or Path.cwd()).resolve()
    for candidate in [base, *base.parents]:
        if all((candidate.joinpath(*parts)).exists() for parts in _MARKERS):
            return candidate
    raise FileNotFoundError(
        "could not find the repository root; run from inside the repo or set DS_PRACTICE_ROOT"
    )


def data_path(name: str) -> Path:
    """Path to a file under ``data/raw`` (whether or not it exists)."""
    return repo_root() / "data" / "raw" / name


def require_data(name: str) -> Path:
    """Return a downloaded data file, or raise a helpful error."""
    path = data_path(name)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Fetch the data first, e.g.\n"
            f"    python scripts/download_data.py --all"
        )
    return path
