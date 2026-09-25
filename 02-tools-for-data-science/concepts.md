# Concepts — the data-science working environment

This note explains the tools behind the rest of the portfolio. The companion notebook,
[`01-jupyter-and-git.ipynb`](notebooks/01-jupyter-and-git.ipynb), puts each idea into a runnable
cell.

## Notebooks: prose and code in one document

A **Jupyter notebook** is an ordered list of *cells*. Each cell is one of two kinds:

- **Code cells** run in a language kernel (Python here) and share state with one another. The
  variables defined in an early cell are visible in a later one.
- **Markdown cells** hold formatted text and are not executed. They are where the explanation
  lives: what the next code does, what the output means, and what could go wrong.

Because code cells share one kernel, a notebook's meaning depends on **execution order**. If you
run cell 5 before cell 3, you may see a result that nobody else can reproduce. The habit that
fixes this is *Restart Kernel and Run All* before sharing or committing a notebook.

### A tiny example

A code cell can be as small as:

```python
masses = [3750, 3800, 5000]
print(sum(masses) / len(masses))
```

The Markdown cell above it should say *why* those three numbers are there — for example, "mean
body mass of one bird per species, in grams". Code with no prose is a script; prose with no code
is an essay. A notebook earns its name by combining them.

## Markdown essentials

Markdown is plain text with a light syntax. The same subset appears in every notebook here:

| Construct | Syntax | Use |
|---|---|---|
| Heading | `#`, `##`, `###` | Section structure |
| Bold / italic | `**text**`, `*text*` | Emphasis |
| Inline code | `` `text` `` | Names, commands, file paths |
| Fenced code | triple backticks | Multi-line code or commands |
| List | `-` or `1.` | Bullets and steps |
| Link | `[text](url)` | References |
| Table | pipes and dashes | Comparisons |
| Maths | `$...$`, `$$...$$` | Formulas |

Good technical writing uses headings to make a document skimmable, keeps paragraphs short, and
puts the *reason* before the *result*. Those rules hold whether the reader is a colleague, a
reviewer, or your future self.

## Git: snapshots, not save-as

**Git** records snapshots of a project so that every change is traceable and reversible. Each
snapshot is a **commit** with a message. The everyday loop is:

```bash
git status              # which files changed?
git add <files>         # choose what goes into the next snapshot
git commit -m "..."     # record the snapshot
git log --oneline       # review the history
```

A few concepts make the commands less mysterious:

- **Working tree** — the files as they currently are.
- **Staging area** — the changes selected for the next commit (`git add`).
- **Repository** — the full history of commits.
- **Branch** — a movable name pointing at the latest commit on a line of work.

Branches let you try something without disturbing the main line:

```bash
git switch -c experiment    # start a new line of work
# ... edit and commit ...
git switch main             # return to the main line
git merge experiment        # bring the work back when it is ready
```

Git is valuable in data work because analyses are explored, revised, and sometimes reverted. A
commit message such as "drop rows with missing bill length before modelling" is far more useful
than "update".

### A safety note

The notebook's Git demonstration runs inside a directory created by `tempfile.mkdtemp()`. It
initialises a *new* repository there, so your real project is never modified. Always be cautious
with commands such as `git reset --hard` and `git clean -fd`; they discard work.

## Reproducibility

A result is **reproducible** when another person, starting from the same code and data, obtains
the same answer. It is a property of the whole workflow, not a single line. Four habits carry
most of the weight:

1. **Fixed seeds.** Any code that samples, shuffles, or initialises randomly must be seeded.
   Python's `random` and NumPy both accept a seed; this repository uses `42` throughout.
2. **Pinned versions.** Dependencies are recorded with exact versions in
   [`requirements.txt`](../requirements.txt), so a library upgrade does not silently change a
   result.
3. **Deterministic ordering.** Sorting, grouping, and file iteration should have a defined order.
   Relying on the order in which a file system happens to return names is a hidden source of
   variation.
4. **Recorded provenance.** Where the data came from, when it was fetched, and its licence belong
   in the project. Here every dataset is fetched by `scripts/download_data.py` and cited in
   [`docs/datasets.md`](../docs/datasets.md).

### Why a seed is necessary but not sufficient

Seeding replaces one source of randomness with a fixed sequence, so *your* two runs agree. It
cannot guarantee that a different machine — with a different library version, a different CPU, or
a different data file — will agree too. That is why the checklist above has four items, not one.

## How the tools fit together

- **Markdown** explains the work.
- **Code cells** produce the numbers and figures.
- **Git** records how the work changed over time.
- **Seeds and pinned versions** make the work repeatable.

Used together, they turn a one-off calculation into something a colleague can read, rerun, and
trust.
