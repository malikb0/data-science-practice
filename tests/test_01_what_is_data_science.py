"""Module 01 — conceptual package: the written material should exist and be complete."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "01-what-is-data-science"


def test_module_files_exist():
    assert (MODULE / "README.md").is_file()
    assert (MODULE / "case-study.md").is_file()


def test_readme_covers_lifecycle_and_roles():
    text = (MODULE / "README.md").read_text(encoding="utf-8").lower()
    for topic in ("lifecycle", "roles", "limitations"):
        assert topic in text


def test_case_study_is_end_to_end():
    text = (MODULE / "case-study.md").read_text(encoding="utf-8").lower()
    for stage in ("frame the problem", "collect the data", "communicate"):
        assert stage in text
