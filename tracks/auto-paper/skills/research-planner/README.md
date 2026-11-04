# research-planner

Turns benchmark-backed research questions that have passed the prior-work
check into **tightly scoped, time-bounded research plans**, each with a
credible path to beating the strongest comparable baseline. It compares the
candidates side by side, redesigns weak directions (scope cuts first), and
orders the feasible projects **from easiest to hardest**.

## When to use it

- You have one or more slots with a prior-work **PASS** and want concrete,
  executable plans: hypothesis, minimum experiment, controls, success and
  stop criteria, and a schedule.
- You need to choose between several candidate directions.

It is the final stage of [research-pipeline](../research-pipeline/README.md),
and you can also call it directly if you already have the upstream outputs.

## How to use it

```
/research-planner
Slots: RQ1, RQ3 (prior-work PASS), RQ4
Duration per project: 1 week
Experience level: Intermediate
```

Attach or reference, when available: benchmark-finder findings,
prior-work-checker results and Evidence Reports, compute-planner results,
and research-readiness-advisor output. The per-project duration D is a
**hard constraint** and is never extended to make a project fit.

## What it does (Steps 0–9)

0. Requires a prior-work PASS for each slot.
1. Re-validates the benchmark and rejects duplicate directions across
   slots.
2. Finds the smallest gap grounded in the benchmark, and defines the
   contribution and the **minimum experiment**.
3. Incorporates compute-planner's feasibility verdict and enforces D.
4. Defines execution criteria (success, stop/pivot).
5. Filters, then builds a **candidate comparison matrix** for every
   shortlisted option.
6. Orders the feasible projects from easiest to hardest.

It combines verdicts from other skills and never re-derives them: novelty
comes from prior-work-checker, SOTA potential, depth and negative-result
readiness from research-readiness-advisor, and FITS DURATION from
compute-planner.

## Output

For each slot, `### Project p (schedule window) — Direction RQk` with: the
original question and whether it was Preserved, Modified, Replaced,
Generated or UNRESOLVED; the final research question (verbatim, ending in
"?"); hypothesis; problem; exact benchmark, dataset, metric and baseline;
the minimum experiment; controls; success and stop/pivot criteria; and the
schedule window. UNRESOLVED slots are listed last.

## Shared definitions

`~/.claude/skills/research-pipeline/references/research_design_principles.md`
(Beginner, technical depth, SOTA potential vs achievement, D-day
feasibility, redesign, mandatory gates).
