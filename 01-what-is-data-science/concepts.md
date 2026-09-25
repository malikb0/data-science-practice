# Concepts — what data science is

This note explains the ideas behind module 01 in plain language. It is written to be read once
from top to bottom; the [case study](case-study.md) then shows the same ideas on a single question.

## A working definition

**Data science is the practice of turning data into decisions that are defensible.** The word
"defensible" matters: an answer drawn from data should survive the question "how do you know?".
That means the data's source is recorded, the steps are repeatable, and the uncertainty is stated.

Data science borrows from three traditions:

- **Statistics**, for reasoning about uncertainty and variation.
- **Computer science**, for handling data at scale and writing reproducible code.
- **Domain knowledge**, for knowing which questions are worth asking and which answers are
  plausible.

A model without domain knowledge can be technically correct and practically useless. A careful
analyst without statistics can be fooled by randomness. A brilliant method that nobody can rerun
is not evidence.

### A small example

A café owner notices sales dip on Tuesdays. "Sales are lower on Tuesdays" is an observation.
A data question is sharper: *by how much, compared with other days, after accounting for weather
and holidays?* The answer may be "about 120 fewer cups, mostly between 2pm and 4pm". That
difference — vague impression versus measured effect — is the value data science adds.

## The lifecycle

Most teams describe their work as a cycle of stages. Names differ, but the content is stable.

1. **Frame the problem.** Convert a wish into a measurable question and define success in advance.
   *Example:* "reduce customer churn" becomes "predict which subscribers will cancel in the next
   30 days, so that retention offers can be targeted".
2. **Collect the data.** Find or gather the relevant data and record where it came from, when it
   was captured, and how it is licensed.
3. **Prepare the data.** Clean types, handle missing values, deal with duplicates, and build the
   features the question needs. This is usually the largest stage.
4. **Analyse or model.** Summarise, test hypotheses, or fit a model. Descriptive work comes before
   predictive work; jumping straight to machine learning is a common mistake.
5. **Communicate.** Turn the result into something a decision-maker can act on: a chart, a short
   brief, a dashboard. State what the data cannot tell you.
6. **Monitor.** Put the result into use and watch it. If the world changes, the analysis is
   repeated or the model is retrained.

### The lifecycle is a loop, not a line

Stages feed back into each other. During preparation you may discover the question was ambiguous
and return to framing. During evaluation you may find a feature that was mis-scaled and return to
preparation. Treat the numbered list as a checklist of concerns, not a waterfall.

## Roles on a data team

Titles overlap and differ between employers, but most teams need four kinds of work done.

| Role | Core question | Typical output |
|---|---|---|
| Data analyst | "What happened, and why?" | Reports, dashboards, experiments |
| Data engineer | "Is the data available, correct, and on time?" | Pipelines, tables, data quality checks |
| Data scientist | "What should we expect, and how sure are we?" | Analyses, models, written recommendations |
| Machine-learning engineer | "Does the model work reliably in production?" | Deployed services, monitoring, retraining |

A fifth and often decisive role is the **domain expert** — the person who knows the penguins, the
customers, or the machines. They help frame the question and sanity-check the answer. In small
teams one person wears several hats; the work still has to happen.

### A small example of overlap

A hospital wants to reduce missed appointments. A data engineer assembles appointment records, an
analyst measures how often people miss them and by how much, and a data scientist builds a model
that scores each booking. The scheduling team, as domain experts, decide which interventions are
ethical and practical. None of these people can deliver the change alone.

## Where data science fits in an organisation

Data science rarely sits on its own. It usually connects:

- the **business side**, which owns the decision and the budget;
- the **engineering side**, which owns the systems where data is created and used;
- **risk, legal, and ethics**, which care about privacy, fairness, and compliance.

The most successful projects start from a decision someone actually needs to make, not from a
dataset that happens to be available. That is why framing is the first stage.

## Common misunderstandings

- **"It is mostly modelling."** In practice, framing and preparation dominate; modelling is
  often the smaller part.
- **"More data always helps."** Badly labelled or biased data makes things worse, not better.
- **"A model is the answer."** A model is an input to a decision. Someone still has to act.
- **"Once it is built, it is done."** Data drifts, behaviour changes, and results need monitoring.

## What comes next

The rest of the repository makes these ideas concrete. Module 02 covers the tools; module 03
applies the CRISP-DM lifecycle end to end on a small dataset; the remaining modules build the
individual skills — programming, databases, analysis, visualisation, and machine learning.
