#!/usr/bin/env python3
"""Execute the offline-runnable notebooks and report a summary.

Network-dependent notebooks and notebooks whose dataset has not been downloaded
are skipped, so ``make nb`` is safe to run anywhere. Pass ``--all`` to attempt
every notebook (network notebooks will then fail without a connection).

Usage
-----
    python scripts/run_notebooks.py            # offline-safe notebooks only
    python scripts/run_notebooks.py --all
    python scripts/run_notebooks.py 04-python-for-data-science
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Notebooks that require the network by design.
NETWORK_NOTEBOOKS = {
    "05-python-project/notebooks/01-web-scraping.ipynb",
    "04-python-for-data-science/notebooks/05-apis-and-http.ipynb",
}


def discover(module: str | None) -> list[Path]:
    pattern = f"{module}/**/*.ipynb" if module else "0*/**/*.ipynb"
    return sorted(p for p in ROOT.glob(pattern) if ".ipynb_checkpoints" not in p.parts)


def run(path: Path, timeout: int) -> tuple[bool, str]:
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        return False, "nbclient/nbformat not installed (pip install -r requirements.txt)"

    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    try:
        client.execute()
    except Exception as exc:  # noqa: BLE001 - report and continue
        return False, f"{type(exc).__name__}: {exc}"
    return True, "ok"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module", nargs="?", help="limit to one module directory")
    parser.add_argument("--all", action="store_true", help="include network notebooks")
    parser.add_argument("--timeout", type=int, default=300, help="per-notebook seconds")
    args = parser.parse_args(argv)

    notebooks = discover(args.module)
    if not notebooks:
        print("no notebooks found")
        return 1

    ran = skipped = failed = 0
    failures: list[tuple[Path, str]] = []
    skip_markers = ("FileNotFoundError", "ModuleNotFoundError", "ImportError")
    for path in notebooks:
        rel = path.relative_to(ROOT).as_posix()
        if rel in NETWORK_NOTEBOOKS and not args.all:
            print(f"  skip  {rel} (needs network)")
            skipped += 1
            continue
        ok, detail = run(path, args.timeout)
        if ok:
            print(f"  ok    {rel}")
            ran += 1
        elif any(marker in detail for marker in skip_markers):
            print(f"  skip  {rel} (missing data or dependency)")
            skipped += 1
        else:
            print(f"  FAIL  {rel}: {detail.splitlines()[0][:100]}")
            failures.append((path, detail))
            failed += 1

    print(f"\n{ran} executed, {skipped} skipped, {failed} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
