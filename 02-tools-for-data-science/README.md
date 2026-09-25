# 02 — Tools for data science

The working environment behind every other project in this repository: interactive notebooks,
Markdown for explanation, Git for version control, and the habits that make an analysis
reproducible.

**Dataset:** none. The notebook builds a tiny example in memory so it runs completely offline.

## Learning objectives

By the end of this module you should be able to:

- Describe the structure of a notebook and the difference between code cells and Markdown cells,
  including why cell execution order matters.
- Write the handful of Markdown constructs — headings, lists, links, tables, code, and maths —
  that carry most technical writing.
- Use a minimal Git workflow: `init`, `status`, `add`, `commit`, `log`, and a short-lived branch.
- Explain what makes a result reproducible: a fixed seed, pinned dependency versions, a clean
  top-to-bottom run, and recorded data provenance.
- Run the notebook's Git demonstration safely inside a throwaway directory.

## Prerequisites

- Python 3.10 or newer and the packages in [`requirements.txt`](../requirements.txt).
- Git installed (the notebook still runs and explains itself if Git is missing).
- No prior experience with notebooks, Markdown, or Git is assumed.

## Topics covered

- Notebook format: code cells, Markdown cells, and kernel state.
- Markdown essentials used throughout the portfolio.
- The Git loop from an empty folder to a first commit, plus branching.
- Reproducibility as a set of concrete habits rather than a vague goal.
- A short worked example that mixes prose, computation, and version control.

## How to run

```bash
make install
jupyter lab 02-tools-for-data-science/notebooks/01-jupyter-and-git.ipynb
```

The notebook has no external data requirement. The Git section creates a temporary directory with
`tempfile.mkdtemp()` and never touches this repository. The written explanation is in
[`concepts.md`](concepts.md), with answers in [`solutions.md`](solutions.md).

## Exercises

1. Add a Markdown cell to the notebook containing a level-2 heading, a three-item bulleted list,
   one inline code span, and a link to the repository's `docs/datasets.md`. Then add a code cell
   that prints the current working directory, and explain in one sentence why that path can differ
   between machines.
2. In the notebook's temporary Git repository, create a branch named `experiment`, add a second
   file, commit it there, switch back to the default branch, and print `git log --oneline` for
   both branches. Explain in a short Markdown cell why the second commit does not appear on the
   default branch.
3. The notebook samples species names with a fixed seed. Change the seed from `42` to `7`, run the
   cell twice, and note what stays the same and what changes. Write one sentence on why a fixed
   seed is necessary but not sufficient for reproducibility.

## Limitations

- The Git demonstration covers the everyday loop only; remotes, rebasing, and merge conflicts are
  deliberately out of scope and belong in Git's own documentation.
- Notebook interfaces differ between JupyterLab, Jupyter Notebook, VS Code, and other editors, so
  menu names and keyboard shortcuts may vary.
- The reproducibility checklist is a strong default, not a formal guarantee across operating
  systems, hardware, or floating-point libraries.
