# research-readiness-advisor

Acts as a research mentor and designer for each benchmark-backed
candidate. It answers one question:

> *Given my goal and experience level, is this a good project to actually
> run and turn into a short paper?*

It diagnoses the strongest baseline's documented weaknesses, designs a
targeted intervention, rates the candidate on several axes, **tries at
least one redesign before rejecting anything**, and writes a full
provisional paper draft (results marked TBD) for projects that are ready.

## When to use it

- After [benchmark-finder](../benchmark-finder/README.md) (and ideally
  [prior-work-checker](../prior-work-checker/README.md) and
  [compute-planner](../compute-planner/README.md)) have produced a
  candidate.
- When you want an honest go/no-go on a project idea, including what a
  *negative* result would still teach you.

## How to use it

```
/research-readiness-advisor
Candidate: RQ2 — <question>, benchmark <name>, baseline <name>
Goal: practice writing a 4-page workshop paper
Duration: 4 working days
Experience level: Beginner
```

The more upstream output you provide, the better the result: benchmark
verification and validity (V1–V4), the Prior-Work Evidence Report
(`prior_work_evidence_*_RQk.md`), and compute-planner's result.

## What it rates

| Axis | Values |
| --- | --- |
| Benchmark fit / Execution fit | HIGH / MEDIUM / LOW |
| Original-question preservation | HIGH / MEDIUM / LOW / REPLACED |
| SOTA potential (pre-experiment), from S1 weakness and headroom, S2 mechanism, S3 fair test, S4 feasible design | HIGH / MEDIUM / LOW / UNKNOWN |
| Technical depth (hard gate) | PASS / FAIL |
| Mechanism and domain validity | PASS / PASS-EXPLORATORY / FLAG / FAIL |
| Novelty strength (taken from the Evidence Report, not re-judged) | HIGH / MEDIUM / LOW |
| Negative-result interpretability | PASS / CONDITIONAL / FAIL |
| **Short-paper readiness** | **READY / NEEDS REDESIGN / NOT READY** |

It also lists the required controls, the expected effect against the
minimum detectable effect, and what a positive, negative or inconclusive
result would mean.

## Output

- One table per candidate with all of the fields above, the redesign
  history, and the recommended redesign.
- For **READY** candidates, a full provisional paper draft: abstract,
  introduction, related work, method, experiment design, conclusion, and
  planned tables and figures. It is written as if the hypothesis holds,
  with **no invented numbers**. This draft is the `DRAFT_FILE` input for
  [paper-writer](../paper-writer/README.md).
- Pivot guidance that research-planner uses for stop/pivot criteria.

## Boundaries

It advises and never overrides another skill's verdict. A candidate that
fails a hard gate (no exact benchmark, failed V1–V4, prior-work FAIL, does
not fit duration) cannot be rescued by good readiness ratings.

## Files

- `references/mentorship_principles.md`
