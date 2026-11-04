# research-pipeline

Runs the **full research-planning workflow** from start to finish. You
supply an idea file (or name the sources to discover from), a per-project
time budget and your experience level. You get back a ranked, scheduled
set of benchmark-backed projects, each with a credible path to beating the
strongest comparable baseline.

```
Discover → Diagnose → Design → Scope → Evaluate → Refine → Select
```

## Skills it coordinates (in this order)

1. [research-question-parser](../research-question-parser/README.md): extract `RQk` slots
2. [benchmark-finder](../benchmark-finder/README.md): exact benchmarks, baselines and weaknesses, later the prior-work archive
3. [research-readiness-advisor](../research-readiness-advisor/README.md): design, rate, redesign, provisional draft
4. [prior-work-checker](../prior-work-checker/README.md): novelty PASS/FAIL, looping back to benchmark-finder on FAIL
5. [compute-planner](../compute-planner/README.md): compute and duration feasibility at your level
6. [research-planner](../research-planner/README.md): final plans, comparison and easiest-to-hardest schedule

The pipeline enforces these skills' verdicts and never replaces them.

## How to use it

```
/research-pipeline

File: experiments.pdf
Time budget: 4 weeks
Experience level: Beginner
Number of research directions: 5
```

| Input | Required? | Notes |
| --- | --- | --- |
| Idea file **or** named discovery sources | Yes | e.g. a notes file, or "recent literature", leaderboards, Inspect Evals. The scope is any area of AI/ML. |
| Per-project duration D | Yes | A single "time budget" is read as the budget **per project**. Asked if missing, never assumed. |
| Experience level | Yes | Beginner / Intermediate / Advanced. Asked if missing. |
| Number of directions N | No | Defaults to the number of parsed ideas. |
| Overall budget across projects | No | |

**Modes:** Benchmark-First (default; your ideas are seeds and the topics may
drift) or Fixed-Topic (say that a question must be preserved).

## Key steps

- **Step 1–2:** read the file, screen at least 10–15 benchmarks across at
  least 6 subfields, rank them and fix the N slots before writing any
  research question (anti-fixation).
- **Step 2a–2c:** readiness advice, then the prior-work check loop, then
  building the benchmark archive, re-checking, and final confirmation.
- **Step 3–4:** a minimal compute configuration and the feasibility
  verdict.
- **Step 5–5b:** plans built around the benchmark, then a mandatory
  evidence gate before implementation (prior work, novelty and SOTA).
- **Step 6:** filter, redesign at least once before any rejection, and
  order the projects.

## Output

- Input ideas and slots, and the directions found.
- For each project, `### Project p (schedule window) — Direction RQk`
  with the full plan.
- **Project Schedule** (easiest first) and a **Recommendation**.
- Along the way: `prior_work_<benchmark>.md` archives, Prior-Work Evidence
  Reports, and provisional paper drafts for READY projects.

## After the pipeline (manual skills)

```
/paper-writer <report.md> <provisional_drafts.md> RQk       # pre-experiment paper
/experiment-runner paper_RQk_v1.md                          # run the frozen experiment
/paper-writer <report.md> paper_RQk_v1.md RQk results: results_RQk.md
/paper-visuals paper_RQk_v2.md
/paper-to-latex paper_RQk_v2_visuals.md --visuals paper_RQk_v2_figures/
```

## Files

- `references/research_design_principles.md`: shared definitions used by
  every research skill (Beginner, technical depth, SOTA potential, D-day
  feasibility, redesign, gates).

## Tips

- The run is long and makes many web searches. Give it real sources and a
  realistic D.
- It will not guarantee SOTA, and it will not present a result on a narrow
  slice of the benchmark as overall SOTA.
