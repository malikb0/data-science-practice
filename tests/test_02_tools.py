"""Module 02 — the notebook should parse and genuinely mix prose and code."""
from helpers import notebook_source, read_notebook

NOTEBOOK = "02-tools-for-data-science/notebooks/01-jupyter-and-git.ipynb"


def test_notebook_parses_and_has_both_cell_types():
    nb = read_notebook(NOTEBOOK)
    kinds = {cell["cell_type"] for cell in nb["cells"]}
    assert kinds == {"code", "markdown"}


def test_notebook_covers_expected_topics():
    source = notebook_source(read_notebook(NOTEBOOK)).lower()
    for topic in ("markdown", "git", "reproducib", "seed"):
        assert topic in source


def test_git_demo_uses_a_temporary_directory():
    source = notebook_source(read_notebook(NOTEBOOK))
    assert "tempfile" in source and "mkdtemp" in source
