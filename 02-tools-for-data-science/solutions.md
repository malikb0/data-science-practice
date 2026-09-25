# Solutions — module 02 exercises

Worked answers to the [README](README.md) exercises. Where code is shown, it is the kind of code
you could add as a new notebook cell.

## Exercise 1 — A Markdown cell plus a working-directory cell

A Markdown cell like this satisfies the requirements:

```markdown
## Notes on paths

- the notebook remembers a working directory
- that directory is not guaranteed on another machine
- so we print it instead of hard-coding it

See `docs/datasets.md` for how data is fetched.
```

That cell has a level-2 heading, three bullets, an inline code span (`docs/datasets.md`), and a
link target. To make the link clickable in a notebook, use
`[datasets documentation](../../docs/datasets.md)` rather than bare text.

The companion code cell:

```python
from pathlib import Path

print(Path.cwd())
```

**Why the path can differ.** The kernel's working directory is set by the tool that launched it —
usually the folder containing the notebook, but that is configurable. A teammate may open the
notebook from a different folder or run it headlessly from a script, so the same `print` produces
a different string. Code should therefore locate files relative to the notebook (or via a known
project root) rather than assume the current directory.

## Exercise 2 — Branching in the temporary repository

Add these calls to the demonstration (they assume the helper `run` and the temporary `workdir`
already exist from the README notebook):

```python
run("switch", "-c", "experiment")
(workdir / "second.txt").write_text("only on the experiment branch\n")
run("add", "second.txt")
run("commit", "-q", "-m", "Add second file")

print("on experiment:")
print(run("log", "--oneline"))

run("switch", "main")
print("on main:")
print(run("log", "--oneline"))
```

**Why the second commit is absent from `main`.** A branch is just a name pointing at a commit.
When the `experiment` branch was created it pointed at the same commit as `main`. The new commit
moved the `experiment` name forward, leaving `main` where it was. The two branches therefore point
at different commits until they are merged. Running `git merge experiment` from `main` would move
`main` forward to include the new commit.

## Exercise 3 — Changing the seed

With the notebook's sampling cell, change:

```python
rng = random.Random(42)
```

to

```python
rng = random.Random(7)
```

and run the cell twice.

**What stays the same.** The two runs *within* the edited cell still agree with each other,
because both use the same new seed. The structure of the output is unchanged: the same number of
draws, the same set of possible species.

**What changes.** The actual sequence of sampled species differs from the seed-`42` version
(unless the two seeds happen to produce the same first draws, which is unlikely). This shows that
the seed *chooses* one sequence; it does not remove randomness, it fixes it.

**One sentence.** A fixed seed is necessary because it makes a single workflow repeatable, but it
is not sufficient because reproducibility also depends on the same library versions, the same
data, and a deterministic execution order.
