---
name: research-readiness-advisor
description: Judge whether a benchmark-backed research candidate is a good project for this user to actually execute and turn into a short paper, given their goal, duration, and experience level. Rates benchmark fit, execution fit, original-question preservation, and short-paper readiness, recommends mechanism-preserving redesigns, and writes a full provisional pre-experiment paper draft (results TBD) for ready projects.
---

# Research Readiness Advisor

Answer, for each candidate:

"Given the user's current goal and experience level, is this a good
benchmark-centered research project to actually execute and turn into a
short paper?"

This skill advises; it does not replace other skills:

- benchmark-finder finds and verifies benchmarks, prior work, and the
  exact-benchmark / validity checks.
- prior-work-checker decides novelty (PASS / FAIL).
- compute-planner decides compute, duration, and difficulty at the user's
  experience level.
- research-planner owns final project design, comparison, ranking, and
  scheduling.

Never override their verdicts. A candidate that fails a hard gate from
those skills (exact benchmark, validity V1–V4, prior-work PASS, FITS
DURATION) cannot be made acceptable by a good readiness rating.

## Sources

Read before advising:

1. `references/mentorship_principles.md` (this skill's directory): the
   primary source for the criteria below.
2. `~/.claude/skills/benchmark-finder/references/research_advice.md`.

Both are mentorship guidance, not scientific evidence. Where
`research_advice.md` says a topic may be discarded for a more feasible
benchmark, apply it in this skill's sense: discard only when no
sufficiently aligned, feasible, benchmark-backed version of the original
question exists (see Preservation).

## Input

For each candidate (per slot RQk):

- Original research question (and seed direction, if any)
- Candidate research question and benchmark from benchmark-finder,
  including verification fields, validity V1–V4, and Benchmark Readiness
- prior-work-checker result, when available
- compute-planner result, when available
- User's goal (e.g. paper-writing practice), per-project duration D, and
  experience level L

## Workflow

### Step 1: Benchmark fit (HIGH / MEDIUM / LOW)

How well the benchmark represents the research question. Base it on
benchmark-finder's SAME-TASK, comparability, and validity (V1–V4) answers
and the benchmark-selection guidance: established task, clear metric,
published baseline numbers, public data and code, traceable literature,
room for a small method change. A benchmark is never rated HIGH merely
because it is easy.

### Step 2: Execution fit (HIGH / MEDIUM / LOW)

How feasible the benchmark is for the user's duration D, experience level
L, and compute. Before compute-planner has run, give a PRELIMINARY
execution fit from Benchmark Readiness (released outputs/predictions,
reproduction path, compute burden, experience-sensitive factors), D, and L.
After compute-planner has run, CONFIRM it: compute-planner's Duration
Feasibility is authoritative, and DOES NOT FIT DURATION means Execution fit
LOW.

Recommend a benchmark normally only when both Benchmark fit and Execution
fit are acceptable (MEDIUM or HIGH).

### Step 3: Original-question preservation

Rate how much of the original research motivation survives:

- HIGH: same mechanism and phenomenon, mapped onto an established
  benchmark.
- MEDIUM: core mechanism kept, but scope, setting, or measured outcome
  narrowed.
- LOW: only the broad theme survives.
- REPLACED: different research direction.

Preservation is a preference among candidates that pass every hard gate.
When several such candidates exist for a slot, prefer HIGH or MEDIUM
preservation. If the original question is too broad, first try to keep its
core mechanism while mapping it onto an established benchmark. Never
replace a direction merely because an unrelated benchmark project is
easier; replace only when no sufficiently aligned, feasible,
benchmark-backed version can be found. Preservation never overrides a hard
gate.

### Step 4: Research-question criteria

Check the ten research-question criteria in
`references/mentorship_principles.md` and record YES / NO for:

- Published baseline available
- Existing metric available
- New dataset required
- New evaluation task required
- Main table possible
- Ablation/control possible

and rate Prior-work traceability (HIGH / MEDIUM / LOW).

### Step 5: Project type

- Performance-oriented: primarily aims to improve benchmark performance.
  Beating, or being competitive with, a strong published baseline is the
  target.
- Scientific-diagnostic: primarily tests a hypothesis or mechanism using
  the benchmark. A well-designed negative result can be a valid outcome.

Never require SOTA for a result to count as meaningful.

### Step 6: Short-paper readiness

Check whether the project naturally supports this structure:

- Problem
- Benchmark
- Published baseline
- Proposed method/change
- Main experiment
- Main results table
- At least one ablation/control/sub-analysis
- Figure or framework diagram where appropriate
- Clear interpretation
- Related work traceable from the benchmark literature

Reference target: about four pages of main content plus references
(Abstract, Introduction, Related Work, Method, Experiment, Conclusion),
unless the user specifies another length. A literal conference submission
is not required.

Verdict:

- READY: every item above is supported, Benchmark fit and Execution fit
  are both acceptable, no new dataset or evaluation task is required
  (unless that is the explicit goal), and a main table plus an
  ablation/control are possible.
- NEEDS REDESIGN: the core mechanism is worth keeping but one or more items
  fail and a benchmark-centered redesign could fix them.
- NOT READY: no plausible benchmark-centered redesign of this candidate
  would fix it.

### Step 7: Recommended redesign (if NEEDS REDESIGN or NOT READY)

Propose, in order:

1. a benchmark-centered redesign that preserves the original research
   mechanism (same mechanism, established benchmark task and metric,
   published baseline, one isolated change);
2. a different established benchmark for the same mechanism;
3. only if neither yields a sufficiently aligned, feasible version:
   replacement of the direction.

Any redesign or replacement goes back through benchmark-finder's
validation, prior-work-checker, and compute-planner before it can be
accepted.

### Step 7b: Archive re-evaluation (research-pipeline Step 2c)

After benchmark-finder has built the benchmark-centered prior-work archive
for a provisionally confirmed benchmark and the overlap has been re-checked,
re-run the evaluation using the archive evidence (inventory, benchmark
history, baseline map, closest prior work, collision verdict, open gap).
Re-evaluate:

- Benchmark fit
- Original-question preservation
- Baseline choice (is the archive's selected baseline the appropriate
  comparison?)
- Main-table feasibility
- Ablation/control feasibility
- Prior-work traceability
- Remaining contribution (what the archive's open gap leaves for this
  project)
- Short-paper readiness

Report each as in the Output table, plus "Baseline choice" and "Remaining
contribution" with a one-line justification each, and state what changed
from the earlier evaluation. READY lets the pipeline mark the benchmark
FINAL CONFIRMED; NEEDS REDESIGN or NOT READY returns the slot to redesign
(Step 7).

### Step 8: Writing-first workflow (READY projects only)

Once the research question, benchmark, baseline, and proposed method have
been selected, write the FULL short-paper draft before running the main
experiment. Project order:

benchmark + baseline selection → method selection → full provisional paper
draft including Conclusion → experiment → fill results → revise
method/paper if necessary → final paper

#### Pre-experiment draft

The draft contains:

- Abstract
- Introduction
- Related Work
- Method
- Experiment design
- Conclusion
- Main results table
- Ablation/control table
- Planned figure(s)

Write the paper around the working research hypothesis that the proposed
method achieves the intended improvement, including outperforming the
target baseline or reaching SOTA when that is the stated project objective.
Write the Abstract, Introduction, and Conclusion as a provisional complete
paper narrative under that hypothesis. Do not leave the Conclusion
unwritten merely because the experiment has not yet been run. Mark the
draft as provisional.

Results before experiments: do NOT fabricate numerical results.

- Leave every unknown numerical cell in result tables as `TBD`.
- Clearly distinguish published baseline numbers (with their source) from
  unobserved proposed-method results.
- Never invent accuracy, standard deviation, p-values, effect sizes, or any
  other measurement, in tables or in the prose (the narrative may state the
  intended direction of the result, but any number stays TBD).

The narrative claim and conclusion are written provisionally under the
intended hypothesis; empirical values remain TBD.

#### After the experiment

If the intended result is achieved:

1. replace TBD cells with the actual measured results;
2. verify every numerical claim against the experiment outputs;
3. revise wording where necessary;
4. finalize the paper.

If the intended result is not achieved, do NOT keep the prewritten
conclusion as though it were true. Instead:

1. diagnose why the method underperformed;
2. preserve the core method concept when reasonable;
3. make small, justified methodological changes;
4. update the Method and planned claims;
5. rerun the experiment within the remaining time budget;
6. revise the paper accordingly.

If the method still does not achieve the intended result within the
project's stop/pivot budget, rewrite the Abstract, Results,
Discussion/interpretation, and Conclusion to match the actual evidence.

The pre-experiment conclusion is a working target for the research
process, not an empirical result that may stay unchanged regardless of
evidence.

#### Writing budget

Pre-experiment full-paper drafting and post-experiment result insertion
and revision are parts of the SAME writing budget estimated by
compute-planner; they are never double-counted. research-planner may
revise the draft when finalising the design.

### Step 9: Pivot guidance (for research-planner's stop/pivot criterion)

If the initial method underperforms during execution, follow the
"intended result is not achieved" sequence in Step 8, and:

- avoid repeatedly replacing the whole research direction;
- respect the user's duration and the stop/pivot criteria from
  compute-planner and research-planner.

Do not optimise indefinitely merely to beat a baseline.

## Output

For each candidate:

| Field | Result |
|---|---|
| Slot | RQk |
| Original research question | |
| Candidate benchmark | |
| Benchmark fit | HIGH / MEDIUM / LOW |
| Execution fit | HIGH / MEDIUM / LOW (PRELIMINARY / CONFIRMED) |
| Original-question preservation | HIGH / MEDIUM / LOW / REPLACED |
| Project type | Performance-oriented / Scientific-diagnostic |
| Published baseline available | YES / NO |
| Existing metric available | YES / NO |
| New dataset required | YES / NO |
| New evaluation task required | YES / NO |
| Main table possible | YES / NO |
| Ablation/control possible | YES / NO |
| Prior-work traceability | HIGH / MEDIUM / LOW |
| Short-paper readiness | READY / NEEDS REDESIGN / NOT READY |
| Main reason | |
| Recommended redesign if needed | |

For READY candidates, append the full provisional paper draft (Step 8).

## Rules

- Never invent papers, baselines, numbers, or URLs.
- Never fabricate experimental results; experimental cells stay TBD until
  actually measured.
- Do not claim novelty; that is prior-work-checker's job.
- Do not make compute or duration judgments beyond the preliminary
  execution fit; compute-planner is authoritative.
