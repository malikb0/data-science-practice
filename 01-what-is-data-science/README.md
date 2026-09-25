# 01 — What is data science?

A short, code-free introduction to the field: what data science is, how a project moves from a
question to a decision, who does the work, and where the discipline sits inside an organisation.

**Dataset:** none. This module is conceptual on purpose so the ideas are not hidden behind code.

## Learning objectives

By the end of this module you should be able to:

- Give a working definition of data science and separate it from neighbouring roles such as data
  analysis, data engineering, and machine learning.
- Describe the stages of a typical data-science lifecycle and explain why it is iterative rather
  than a straight line.
- Name the common roles on a data team and state what each one contributes.
- Trace one applied question from a raw table to a decision, using [`case-study.md`](case-study.md).
- Explain why communication and provenance are part of the technical work, not extras.

## Prerequisites

- None. No programming, statistics, or tooling background is assumed.
- An interest in how organisations turn data into decisions.

## Topics covered

- A working definition of data science and the questions it answers.
- The data-science **lifecycle**: frame, collect, prepare, analyse, communicate, monitor.
- An alternative framing through **CRISP-DM**, used in
  [`03-data-science-methodology`](../03-data-science-methodology/README.md).
- The **roles** that appear on data teams and how they overlap.
- Where data science fits in an organisation and who it serves.
- An applied walk-through on the Palmer Penguins table, written out without code.

## How to run

There is nothing to execute. Read this file and [`case-study.md`](case-study.md). For the same
ideas applied in code, continue to module 03. The written explanations live in
[`concepts.md`](concepts.md), and worked answers to the exercises below are in
[`solutions.md`](solutions.md).

## Exercises

1. Pick a decision you make often — what to eat, which route to drive, which film to watch.
   Rewrite it as a measurable question a data team could answer, and state one thing that would
   count as a successful answer.
2. Using [`case-study.md`](case-study.md), list the six lifecycle stages and, for each, name the
   role most likely to lead it. Choose the stage where the reserve's domain knowledge matters most
   and explain your choice in two or three sentences.
3. Imagine a three-person team: one analyst, one engineer, and one modeller. Describe how they
   would divide the lifecycle stages, and identify one stage where two of them should work
   together. Justify the overlap.

## Limitations

- The lifecycle and the role lists are teaching abstractions. Real projects loop backwards, skip
  stages under time pressure, and are shaped by budgets and internal politics.
- Job titles vary a great deal between employers, so treat the role descriptions as shared
  vocabulary rather than a fixed org chart.
- With no code and no data, this module cannot show how messy real data actually is; the later
  modules supply that experience.
