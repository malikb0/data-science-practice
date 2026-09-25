"""Helpers shared by the test modules."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"


def require_file(name: str) -> Path:
    """Return a downloaded file, or skip the test if it is absent."""
    path = RAW / name
    if not path.exists():
        pytest.skip(f"data file {name!r} not found; run scripts/download_data.py")
    return path


def load_module(relative_path: str, name: str):
    """Import a module from a path whose folder name is not a valid identifier."""
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_notebook(relative_path: str) -> dict:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def notebook_source(nb: dict) -> str:
    return "\n".join("".join(cell.get("source", [])) for cell in nb["cells"])
