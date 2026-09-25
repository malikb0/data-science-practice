# Solutions — module 01 exercises

Worked answers to the three exercises in the [README](README.md). These are model answers, not
the only correct ones; the reasoning matters more than the wording.

## Exercise 1 — Turn a decision into a measurable question

*Example decision:* which route to drive to work.

**Measurable question.** On weekday mornings between 07:00 and 09:00, which of my two usual routes
gets me to the office with the lower median travel time, and by how many minutes?

**What success looks like.** A clear answer with an honest range — for example "route A is about
six minutes faster on average, but the difference disappears when it rains". That is specific
enough to change behaviour and it admits uncertainty.

**Why this counts as data science.** The original wish ("avoid traffic") is not testable. The
rewritten question names the population (weekday mornings), the comparison (two routes), a metric
(travel time), and a summary (median). It could be answered by collecting trip records and
comparing them. Note that no model is required — this is a descriptive question.

## Exercise 2 — Map the lifecycle stages and roles

Using the case study:

| Stage | Most likely lead | Why |
|---|---|---|
| Frame the problem | Domain expert + data scientist | The reserve knows what decision is at stake; the data scientist makes it measurable |
| Collect the data | Data engineer | Three seasons of measurements must be assembled, labelled, and stored consistently |
| Prepare the data | Data engineer / analyst | Missing values, spelling of species and island, and unit checks |
| Analyse | Data analyst / data scientist | Group summaries and comparisons of body mass by species and island |
| Communicate | Data scientist + domain expert | A one-page brief that the reserve can trust and act on |
| Monitor | Data engineer / analyst | Recomputing the summaries each season to spot change |

**Where domain knowledge matters most.** The *frame the problem* stage. The reserve has to decide
what "planning monitoring effort" actually means before any data is touched. If the question were
framed as "which species is most numerous" the analysis would be different and possibly useless
for allocating effort. Domain knowledge also prevents nonsense later, when it can flag that a
measurement is implausible.

## Exercise 3 — Dividing work across a three-person team

A reasonable split:

- **Data engineer** — collect the data, build the pipeline, and own data quality. Responsible for
  stages 2 and 6, and supports stage 3 by making clean inputs available.
- **Analyst** — prepare and explore the data, produce the descriptive summaries, and draft the
  communication artefacts. Leads stages 3 and 5 with the domain expert.
- **Modeller (data scientist)** — frame the measurable question with the business, then fit and
  evaluate any predictive model in stage 4.

**The essential overlap: framing (stage 1).** All three should contribute. The modeller knows what
is technically feasible, the analyst knows what the data can support, and the engineer knows what
can be collected reliably. Framing alone or in a single role usually produces a question that is
either unanswerable or irrelevant.

A second, smaller overlap is **evaluation** (part of stage 4/5): the modeller quantifies
performance, but the analyst checks that the metric matches the original goal — a model can score
well on a metric that nobody in the business cares about.
