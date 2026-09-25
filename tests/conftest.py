"""Shared pytest configuration and path setup."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = Path(__file__).resolve().parent
SRC = ROOT / "src"

for entry in (str(ROOT), str(TESTS), str(SRC)):
    if entry not in sys.path:
        sys.path.insert(0, entry)
