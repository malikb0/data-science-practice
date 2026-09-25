#!/usr/bin/env python3
"""Execute notebooks and (by default) save them back with outputs.

Network-dependent notebooks and notebooks whose dataset has not been downloaded
are skipped, so ``make nb`` is safe to run anywhere. Pass ``--all`` to attempt
every notebook (network notebooks will then fail without a connection).

By default a successful run is written back to disk so the notebooks ship with
visible outputs — this is a teaching repo. Use ``--no-save`` for a dry run, or
``--clear`` to strip outputs and reset execution counts.

Usage
-----
    python scripts/run_notebooks.py                 # execute + save offline-safe
    python scripts/run_notebooks.py --all           # include network notebooks
    python scripts/run_notebooks.py --no-save       # execute, do not write
    python scripts/run_notebooks.py --clear         # strip outputs, then stop
    python scripts/run_notebooks.py 04-python-for-data-science
"""
from __future__ import annotations

import argparse
import uuid
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


def ensure_cell_ids(nb) -> None:
    """Give any legacy cell a stable id so the notebook stays schema-valid."""
    for cell in nb.cells:
        if not cell.get("id"):
            cell["id"] = uuid.uuid4().hex[:8]


def execute(path: Path, timeout: int):
    """Execute a notebook in memory and return the executed node."""
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    return nb


def write_notebook(nb, path: Path) -> None:
    import nbformat

    ensure_cell_ids(nb)
    nbformat.validate(nb)
    nbformat.write(nb, str(path))


def clear_notebook(path: Path) -> None:
    """Remove outputs and reset execution counts, then save."""
    import nbformat

    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    write_notebook(nb, path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module", nargs="?", help="limit to one module directory")
    parser.add_argument("--all", action="store_true", help="include network notebooks")
    parser.add_argument("--timeout", type=int, default=300, help="per-notebook seconds")
    parser.add_argument(
        "--save",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="write executed notebooks back to disk (default: --save)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="clear outputs and execution counts instead of executing, then stop",
    )
    args = parser.parse_args(argv)

    notebooks = discover(args.module)
    if not notebooks:
        print("no notebooks found")
        return 1

    if args.clear:
        for path in notebooks:
            clear_notebook(path)
            print(f"  clear {path.relative_to(ROOT).as_posix()}")
        print(f"\n{len(notebooks)} notebook(s) cleared")
        return 0

    ran = skipped = failed = 0
    failures: list[tuple[Path, str]] = []
    skip_markers = ("FileNotFoundError", "ModuleNotFoundError", "ImportError")
    for path in notebooks:
        rel = path.relative_to(ROOT).as_posix()
        if rel in NETWORK_NOTEBOOKS and not args.all:
            print(f"  skip  {rel} (needs network)")
            skipped += 1
            continue
        try:
            nb = execute(path, args.timeout)
        except Exception as exc:  # noqa: BLE001 - report and continue
            detail = f"{type(exc).__name__}: {exc}"
            if any(marker in detail for marker in skip_markers):
                print(f"  skip  {rel} (missing data or dependency)")
                skipped += 1
            else:
                print(f"  FAIL  {rel}: {detail.splitlines()[0][:100]}")
                failures.append((path, detail))
                failed += 1
            continue

        if args.save:
            try:
                write_notebook(nb, path)
            except Exception as exc:  # noqa: BLE001
                print(f"  FAIL  {rel}: could not save ({type(exc).__name__}: {exc})")
                failures.append((path, str(exc)))
                failed += 1
                continue
            print(f"  ok    {rel} (saved)")
        else:
            print(f"  ok    {rel}")
        ran += 1

    print(f"\n{ran} executed, {skipped} skipped, {failed} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
