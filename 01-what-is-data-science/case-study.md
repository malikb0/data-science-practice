# Case study: from a raw table to a decision

This short walk-through uses no code. Its purpose is to show how the vocabulary from this
module fits together on a single concrete question. The data involved is the Palmer Penguins
table used later in the repository, but the reasoning applies to any dataset.

## The question

> *A nature reserve wants to know whether the size of its penguin population differs by
> species and island, so it can plan where to focus monitoring effort.*

A data-science project starts with a decision, not a dataset. Everything below is in service of
that decision.

## Stage 1 — Frame the problem

The vague wish ("understand the penguins") is turned into a measurable question: *do body mass
and bill dimensions differ by species, and is the difference explained by island?* Success is
defined in advance: a clear, defensible summary that can be shown to a non-technical audience.
Framing is cheap here and expensive to skip — a project aimed at the wrong question wastes every
stage that follows.

## Stage 2 — Collect the data

The reserve already has three seasons of measurements. The relevant columns are species, island,
bill length, bill depth, flipper length, and body mass. We record where the data came from, when
it was collected, and how missing values were encoded. Provenance is part of the data.

## Stage 3 — Prepare the data

Rows with missing measurements are counted (not silently dropped). Species and island are text,
so they are checked for spelling consistency. Units are confirmed — millimetres for bill
measurements, grams for mass. Only after this do we trust any summary.

## Stage 4 — Analyse

We compute group summaries (mean and spread) of body mass by species, then split by island to
see whether island adds information. A visual comparison is usually clearer than a table of
summary statistics. The analysis is descriptive: we are summarising what is there, not yet
predicting anything.

## Stage 5 — Communicate

The output is a one-page brief: two charts, a short paragraph, and an explicit statement of
uncertainty. It answers the original question and notes what the data cannot say. The reserve
can now decide where to place monitoring effort.

## Stage 6 — Decide and monitor

The plan is put into action, and the same summaries are recomputed each season so that change is
visible. If a new question arises ("is body mass changing over time?"), the cycle repeats.

## Where the roles appear

| Stage | Usually led by |
|---|---|
| Frame the problem | Domain expert + data scientist |
| Collect | Data engineer |
| Prepare | Data engineer / analyst |
| Analyse | Data analyst / data scientist |
| Communicate | Data scientist + domain expert |
| Monitor | Data engineer / analyst |

In a small team one person wears several of these hats; the stages still happen.

## What this example deliberately omits

No model is trained, because the question does not require one. Jumping to machine learning
before the descriptive question is answered is a common and avoidable mistake. The remaining
projects in this repository add those techniques in turn.
