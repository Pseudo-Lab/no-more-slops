---
name: research-planner
description: Turn benchmark-backed research questions into small, meaningful, time-bounded research plans and compare candidate directions.
---

# Research Planner

Design the smallest meaningful research plan for one or more
benchmark-backed research questions.

Use compute-feasibility results from compute-planner when available.
Do not independently invent detailed hardware requirements.

## Core Principle

Construct final recommended plans ONLY around EXACT / DIRECT established
benchmarks (as defined in benchmark-finder: defined task, public dataset or
standardized evaluation set, defined protocol, established metric, and a
published baseline or prior result) that pass the SAME-TASK test and
comparability check (see Step 1 and Step 4).

Reason in this order:

benchmark
→ task
→ metric
→ baseline
→ literature gap
→ proposed modification
→ experiment
→ research question

not:

research question
→ search for something vaguely benchmark-like

Never create a new benchmark, dataset, task, evaluation protocol, or metric
for the main experiment. A PROXY BENCHMARK or RELATED DATASET is never
sufficient support for a final recommended plan.

## Priority Reference

`~/.claude/skills/benchmark-finder/references/research_advice.md`
(`C:\Users\elika\.claude\skills\benchmark-finder\references\research_advice.md`)
is the PRIMARY and HIGHEST-PRIORITY research-planning reference for this
project. Read and follow it before constructing or ranking plans.

When it conflicts with preserving an original research idea, this skill's
default behavior, or general planning heuristics, FOLLOW it. It is
mentorship guidance, not scientific evidence: it must NOT be used as
evidence that a literature gap exists, a contribution is novel, a benchmark
is established, or a scientific claim is true. Those require verified
literature or benchmark evidence.

Priority: (1) research_advice.md for strategy and project selection,
(2) verified benchmark/literature evidence, (3) user constraints such as
time and compute, (4) original research ideas as candidate interests unless
the user says the topic is fixed.

## Modes

### Fixed-Topic Mode

Use only when the user explicitly wants a research question preserved. Plan
around the original question only if it has an EXACT / DIRECT benchmark. If
it does not, state "Original direction rejected: no exact established
benchmark found." and do not build a recommended plan on a proxy.

Fixed-topic cardinality conflict (K = number of user-designated fixed
topics):

- If K <= N: fixed topics occupy output slots first; the remaining N - K
  slots are filled normally.
- If K > N: do NOT silently discard fixed topics and do NOT increase N
  automatically. Report:

  "You requested N research directions, but marked K topics as fixed (K > N)."

  and ask the user to either (1) increase N to at least K, or (2) specify
  which fixed topics should be prioritized. Do not proceed with final
  selection or ranking until this conflict is resolved.

### Benchmark-First Mode (default)

Inputs are slots whose original questions may be preserved, modified, or
replaced. The final research question is derived only after benchmark and
literature analysis, and may move substantially away from the original
topic.

Do not ask "How can we make the original idea work?" Ask: "Given the
strongest available exact benchmark, what is the smallest meaningful
research question that can be answered within the user-specified
duration D?"

It is acceptable to conclude: "This is an interesting research question,
but it is a poor short-term benchmark-centered project." That is preferable
to attaching an unrelated proxy benchmark.

## Cardinality

N is set by the pipeline: the user-provided "Number of research
directions: N" if given, otherwise N = number of parsed research
questions/ideas. CLEAR / POSSIBLE is metadata only and does not determine N.
When the planner is used on its own, apply the same rule.

Return exactly N output directions, one per output slot. Never merge two
ideas into one slot, never drop a slot, never add extra directions.
Multiple directions may originate from the same broad theme or original
idea, but no two final slots may contain the same research direction. For each slot, state whether it is
Preserved, Modified, Replaced, Generated, or UNRESOLVED.

Priority: (1) exactly N output slots, (2) exact established benchmark,
(3) established baseline and metric, (4) clear narrow literature gap,
(5) feasible experiment, (6) similarity to the original ideas. Never weaken
the exact-benchmark standard merely to reach N; a slot with no valid exact
benchmark after exhaustive search is marked
"UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND".

Keep the slot identifier even when its content is replaced
(RQ3 original → RQ3 replacement).

## Input

The user provides:
- The N output slots (RQ identifiers), each from a parsed idea or generated
- Benchmark/prior-work findings, when available
- prior-work-checker results (PASS/FAIL, prior-work table, traced baseline
  number, gap statement, iteration history), when available
- Compute feasibility findings, when available
- research-readiness-advisor output (benchmark fit, execution fit,
  original-question preservation, project type, readiness checks,
  short-paper readiness, recommended redesign, provisional paper draft, pivot
  guidance), when available
- Per-project duration D (user-specified; hard constraint)
- Experience level L: Beginner / Intermediate / Advanced (user-specified;
  defined in compute-planner)
- Optional overall time budget

## Research Question Format Rule

Every "Final research question" must:

1. Be a single interrogative sentence that ends with "?".
2. Start with an interrogative form (Does / Do / Is / Are / Can / Will /
   Which / How much / To what extent ...).
3. Not be an imperative, a noun phrase or title, a hypothesis statement,
   or a method description.
4. Contain exactly one question.
5. Name the proposed change, the comparison baseline, the benchmark, and
   the main metric, e.g. "Does <change> <increase / reduce> <metric> on
   <benchmark> compared with <baseline>?"
6. Be answerable directly from the main results table.

The Hypothesis stays a declarative statement in its own field. Check every
Final research question against rules 1–6 before output, and rewrite any
that fail.

## Workflow

### Step 0: Require a prior-work PASS

Plan only slots whose research question has PASSED prior-work-checker. Use
the PASSED question verbatim as the Final research question. Take the
Literature gap from prior-work-checker's gap statement. Take the Published
baseline result from its baseline trace.

If the plan needs a different change, baseline, benchmark or metric than
the PASSED question, do not plan it. Send the revised question back
through prior-work-checker (and benchmark-finder on FAIL) first.

A slot marked "UNRESOLVED — NO DIRECTION PASSED THE PRIOR-WORK CHECK" is
output with that label and ranked last.

When the planner runs standalone without prior-work-checker results, mark
every slot "Prior-work check: NOT RUN" and do not rank any slot as a
strong recommendation.

### Step 1: Validate the benchmark foundation

Use benchmark-finder results when available.

For each slot, confirm the benchmark is EXACT / DIRECT and that these
verified fields are present:

- Benchmark name
- Benchmark paper/source
- Task
- Dataset / evaluation set
- Dataset size
- Input
- Output
- Metric(s)
- Established baseline(s)
- Existing reported result(s)
- Public data available?
- Public evaluation code available?
- Why this benchmark DIRECTLY evaluates the proposed problem

Do not infer these fields. If any critical property is UNKNOWN, keep it
UNKNOWN and do not rank the direction as a strong recommendation.

Re-apply benchmark-finder's SAME-TASK test (A-E) and comparability check to
the FINAL main experiment:

A. Is the proposed prediction/decision task already defined by the
   benchmark?
B. Is the benchmark's existing evaluation set used?
C. Are the benchmark's established metrics the MAIN metrics?
D. Can the proposed method be compared directly with an existing published
   baseline on those metrics?
E. Does the experiment avoid defining a new target variable, derived task,
   custom main metric, or new evaluation protocol? (A new component is
   allowed only as secondary analysis, with the main benchmark comparison
   unchanged.)

If any of A-D is NO, or E is NO for the main experiment, the direction is
not exact-benchmark-backed. A task derived from a dataset (e.g. a new label
predicted and scored with a newly introduced metric) is never EXACT unless
that task and metric already exist in the benchmark literature.

Re-apply benchmark-finder's benchmark validity check (V1–V4) to the FINAL
research question and main experiment:

V1. Does the benchmark directly instantiate the phenomenon in the final
    research question?
V2. Does the main metric directly measure the claimed outcome?
V3. Would a positive and a negative result each be evidence about the
    research question?
V4. Is there an established implementation and, preferably, a published
    numerical baseline?

A benchmark that is only related to the topic is not accepted. If V1–V3
reveals a mismatch, do not plan around it: send the slot back to
benchmark-finder to either rewrite the question to match what the benchmark
measures or find a better benchmark, and then back through
prior-work-checker. Never output a final direction with an unresolved
validity mismatch.

If the benchmark is only a PROXY BENCHMARK or RELATED DATASET, or fails the
SAME-TASK test or comparability check, do not plan on it. In Benchmark-First
Mode, keep the slot ID, mark the original direction rejected, and use the
replacement benchmark from benchmark-finder (or request a replacement
search progressively farther from the original topic). Do not lower the
benchmark standard to preserve topical similarity. If no exact benchmark
exists even after exhaustive replacement search, still output the slot,
mark it "UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND", and rank it
below every benchmark-backed direction.

When benchmark-finder provides Benchmark Readiness (dataset, evaluation
code, baseline, setup complexity, reproduction risk, compute burden,
modification simplicity, short-project readiness), use it. Keep scientific
benchmark support (the classification) separate from readiness for a short
project.


### Step 1b: Reject duplicated directions across slots

Compare all N slots with each other. Two slots are duplicates if they use
the same benchmark with the same or a functionally equivalent intervention
(same mechanism under different terminology, or differing only in a minor
protocol detail), or if one slot's result would substantially answer the
other's question.

Keep the slot that is easier to execute (per compute-planner), and send
the other back to benchmark-finder for a redesigned or replacement question
under its own slot ID, then through prior-work-checker. Multiple slots may
share a broad theme or benchmark as long as their questions are not
duplicates in this sense.


### Step 2: Identify the smallest benchmark-grounded gap

Do not search for completely unexplored problems. Prefer:

"Existing benchmark + strong baseline + one missing comparison/condition/
method modification"

over "completely new phenomenon with no established evaluation."

Determine:

- What has already been evaluated on this benchmark?
- What specific, verified gap remains?
- What is the smallest modification that tests it?

Modify ONE major variable while keeping the benchmark, metric, and baseline
fixed.


### Step 3: Define the research contribution

Express the proposed project as:

Existing problem:
Established benchmark:
Strong baseline:
Specific gap:
Smallest proposed change:
Main comparison:
Expected contribution even if result is negative:

The contribution should look like:

existing benchmark
+ established baseline
+ clearly identified limitation/gap
+ one small modification
+ controlled comparison

Do not recommend a direction whose primary contribution is only
correlation analysis, exploratory visualization, qualitative observation, a
new custom dataset, a new custom metric, a new evaluation protocol, "does
phenomenon X exist?", or an analysis that cannot be compared against an
established baseline. These may appear only as secondary analyses.


### Step 4: Design the minimum experiment

Specify:

- Hypothesis
- Baseline
- Main experimental condition
- Control
- Metric
- Minimum useful ablation

Use the benchmark's existing evaluation protocol.

Every direction must be able to produce a conventional benchmark results
table without inventing a new primary task or metric:

| Method | Established Benchmark Metric |
|---|---|
| Published baseline | reported score |
| Reproduced baseline | reproduced score |
| Proposed method | experimental score |

If this table is not conceptually valid, reject the benchmark-direction
pair (and, in Benchmark-First Mode, replace it under the same slot ID).

Avoid adding new datasets, metrics, models, or conditions unless they are necessary to answer the research question.

### Step 5: Incorporate compute feasibility

Use results from compute-planner when available.

Do not override compute-planner's feasibility assessment without
explicit evidence.

If compute feasibility is UNKNOWN, preserve it as UNKNOWN.

Report Hardware Fit separately from User Feasibility. Do not reject a
direction solely because user-specific GPU access is UNKNOWN.

If compute feasibility is RISKY or IMPOSSIBLE, determine whether the
research plan can be reduced in scope without destroying the core question.

### Step 6: Enforce the user-specified duration

The per-project duration D is specified by the user (e.g. 1 week, 4 weeks,
or any other duration). It is a hard feasibility constraint. Never assume a
default, never hard-code a value, and never extend D to make a project
fit. If D is not specified, ask the user for it before this step.

D must cover the COMPLETE workflow: understanding the benchmark and
relevant prior work, reproducing the baseline, implementation, debugging,
experiments, analysis, figures/tables, and writing the required paper.

All estimates are made at the user-specified experience level L (Beginner /
Intermediate / Advanced, defined in compute-planner). If L is not
specified, ask the user for it before this step; never silently assume a
level.

Use compute-planner's level-L workflow estimate and Duration Feasibility
verdict against D. Do not re-estimate it independently, and do not equate
short GPU runtime with fitting D. FITS DURATION means the STANDALONE total
budget required, i.e. the conservative upper bound of estimated work for
the complete workflow at level L plus the separately stated required
contingency, fits within D, so the project can realistically and reliably
be completed within D by a researcher at level L, not merely theoretically
finished. Contingency is not planned work. Setup reused from another
project never makes a project fit. When D is 5 working days, a Beginner
project's expected work should normally be at most about 3.5–4 days, and a
conservative workload of about 5 days is normally DOES NOT FIT DURATION
(compute-planner's five-day rule).

A project that would fit D for a more experienced researcher but not at
level L is DOES NOT FIT DURATION for this run. Never shrink an estimate, or
evaluate at a more experienced level than L, to make a project fit; redesign
it instead.

- FITS DURATION: keep.
- DOES NOT FIT DURATION: do NOT mark it risky and keep it. Redesign it, in
  this order, until it fits:
  1. Simplify the experiment while preserving a meaningful research
     contribution.
  2. Use a simpler established benchmark or baseline.
  3. Reformulate the research question around a smaller experiment.
  4. Replace it with a different benchmark-centered research question that
     satisfies the constraints (same slot ID), only after steps 1–3 (and
     research-readiness-advisor's mechanism-preserving redesign) found no
     sufficiently aligned version that fits.
  After each attempt, re-run compute-planner against D. Any change to the
  question, benchmark, baseline, or metric goes back through
  benchmark-finder's validation (SAME-TASK, comparability, V1–V4) and
  prior-work-checker before it can be kept.
- UNKNOWN: resolve the missing inputs if possible. A direction whose fit to
  D cannot be established is not kept; redesign or replace it as above.

Step 4 is an active search, not a formality. When step 4 is reached, ask
benchmark-finder to search for alternative research questions without
staying anchored to the original idea or its nearby variants: other
benchmarks and gaps in the same theme, then the user's other broad themes,
then adjacent areas. Prefer candidates whose benchmark readiness suggests
they fit D comfortably. Every replacement must pass all three gates before
it is kept:

- Benchmark Validity (SAME-TASK, comparability, V1–V4),
- Novelty / prior-work check (prior-work-checker PASS),
- FITS DURATION against D (compute-planner).

A slot must never be marked UNRESOLVED merely because the original research
question, or its nearby variants, cannot fit D. The final portfolio
contains ONLY directions with FITS DURATION, and the planner must actively
try to return N valid projects. Only after a reasonable replacement search
across these widening scopes has also failed, keep the slot (cardinality)
and mark it, as a last resort:

    UNRESOLVED — NO PROJECT FITS THE SPECIFIED DURATION

State which redesign steps and which replacement scopes were tried. Such
slots are not part of the feasible portfolio.

Reject (in Benchmark-First Mode, replace) or heavily penalize directions that
require collecting a new dataset, designing a benchmark, extensive human
annotation, large-scale training from scratch, complicated infrastructure,
many interacting experimental variables, or uncertain evaluation design.

Prefer simple benchmark extensions with existing repositories, published
baselines, automatic evaluation, minimal code modification, and
inference-only experiments.

If the user also gives an overall time budget shorter than N × D, report
the conflict instead of shortening D.

### Step 7: Define execution criteria

For each research plan, define:

- Pilot Success Criterion:
  What minimum observation would justify proceeding to the full experiment?

- Stop/Pivot Criterion:
  What result, implementation failure, or time threshold should trigger
  stopping or changing the experiment? Follow research-readiness-advisor's
  pivot guidance: preserve the core method concept when reasonable,
  diagnose the failure, try small justified modifications, avoid
  repeatedly replacing the whole direction, and do not optimise
  indefinitely merely to beat a baseline.

- Minimum Result Worth Writing Up:
  What is the smallest interpretable positive or negative result that would
  justify completing the paper or research report?

These criteria should be compatible with the user-specified duration D
(Step 6).

For short projects, prefer early decision points that preserve enough time
for analysis and writing.

### Step 8: Final filtering and quality assessment

Before ordering, every direction in the portfolio must have:
- passed the SAME-TASK test, comparability check, and validity check V1–V4
  on its final question (Step 1),
- PASSED prior-work-checker on its final question (Step 0),
- no duplicate among the other slots (Step 1b),
- a FITS DURATION verdict against D (Step 6),
- a confirmed short-paper readiness of READY from
  research-readiness-advisor (NEEDS REDESIGN or NOT READY triggers the
  advisor's mechanism-preserving redesign first, then the Step 6 sequence).

There is no "risky but kept" category. A slot that cannot meet all five is
redesigned and, if needed, replaced through the active search in Step 6.
Only if that replacement search also fails does it remain in its slot with
an UNRESOLVED label, outside the feasible portfolio.

The quality criteria below are used to choose between candidate directions
(e.g. when m > N, or when deciding which duplicate to redesign) and for the
Recommendation. They NEVER determine project order. Assess quality by:

1. Exact established benchmark availability
2. Reproducible baseline availability
3. Clarity of evaluation metric
4. Narrow and defensible literature gap
5. Simplicity of proposed modification
6. Ability to produce a conventional benchmark results table
7. Contingency remaining within the duration D
8. Hardware fit
9. Interpretability of negative results
10. Relevance to the user's broad interests

Original-question preservation is a preference among candidates that pass
every hard gate (exact benchmark and validity, prior-work PASS, FITS
DURATION): when several such candidates exist for a slot, prefer HIGH or
MEDIUM preservation (research-readiness-advisor). Never replace a direction
merely because an unrelated benchmark project is easier. Preservation never
overrides a hard gate: a direction loosely related to the original question
but with an excellent exact benchmark still ranks above one that preserves
the original idea but has only a proxy.

Directions without an exact benchmark, or with critical benchmark fields
UNKNOWN, are never ranked alongside benchmark-backed directions as equally
valid candidates; rank them last and label them. The same applies to slots
that did not PASS prior-work-checker.

Compliance with `research_advice.md` overrides this quality assessment
where they conflict.

### Step 9: Order feasible projects from easiest to hardest (mandatory)

Pipeline: user-specified duration D and experience level L → filter/redesign
projects → keep only projects that fit D at level L → order them by
level-L difficulty → assign order.

Only after every slot has completed Steps 0–8, order the feasible projects
from easiest/fastest to hardest/slowest for a researcher at the selected
experience level L (not for a generic researcher) and assign Project 1,
Project 2, ... in that order. Project 1 is always the
easiest and lowest-risk project. Each project occupies one period of length
D; give its schedule window (e.g. with D = 1 week: Project 1 = Week 1,
Project 2 = Week 2; with D = 4 weeks: Project 1 = Weeks 1–4, Project 2 =
Weeks 5–8).

Order by compute-planner's level-L difficulty estimate, which covers the
whole workflow (understanding the benchmark/paper, baseline reproduction,
implementation, debugging, compute/runtime, external dependencies or APIs,
analysis, figures/tables, and writing the required paper) including level-L
learning overhead and uncertainty:

1. Standalone Expected Work at level L (ascending)
2. Execution Risk at level L (LOW, then MEDIUM, then HIGH)
3. External Dependencies (fewer first)
4. Slot identifier (only as the final tie-break)

Order strictly by execution difficulty and expected completion time. Never
order by research importance, novelty, conceptual interest, quality
assessment, or the original order of the questions.

UNRESOLVED slots are not ordered or scheduled; list them after all
scheduled projects.

Before output, verify the order: for every consecutive pair, Project p must
not have more Standalone Expected Work at level L than Project p+1 (ties
broken by the
keys above). Fix any violation.

## Final Output

List the feasible projects in order (Project 1 = easiest first), then any
UNRESOLVED slots, one entry per output slot, using the slot's identifier:

### Project p (schedule window) — Direction RQk

Original question: (or "Generated — inspired by <theme / RQ>")
Preserved / Modified / Replaced / Generated / UNRESOLVED:
(If rejected: "Original direction rejected: no exact established benchmark found.")

Final research question:
(The PASSED question, verbatim. One interrogative sentence ending with "?".)

Hypothesis:

Problem:

Exact established benchmark:
Benchmark source:
Dataset/evaluation set:
Metric:
Baseline:
Published baseline result:

Why this is an EXACT benchmark rather than a proxy:
(include SAME-TASK test answers A-E)

Benchmark validity:
(V1–V4 answers for the final question: phenomenon, metric, evidence,
implementation / published baseline. Note any rewrite made to fix a
mismatch.)

Prior-work check:
PASS at iteration n, with the earlier failed questions and their reasons.

Closest prior work and what remains untested:
(From prior-work-checker. "No directly equivalent experiment was found in
the searched literature" — never "no prior work exists".)

Literature gap:
(The gap statement from prior-work-checker.)

Proposed method/change:

Main experiment:

Main results table:
Describe exactly what rows and columns would appear.

Minimum ablation/control:

Smallest viable experiment:

Research readiness (from research-readiness-advisor, confirmed):
(Benchmark fit, Execution fit, Original-question preservation, Project type
(Performance-oriented / Scientific-diagnostic), Short-paper readiness, and
the full provisional paper draft with all unmeasured numerical cells TBD.)

Duration estimate (from compute-planner; standalone, working days, rounded
to 0.25 or 0.5, estimated from this project rather than a template):
- Experience level:
- Standalone expected duration: (e.g. "Expected work: ~3.5 days")
- Standalone conservative duration range: (e.g. "3–4 days")
- Understanding/reading time:
- Setup time:
- Baseline reproduction time:
- Implementation time:
- Debugging time:
- Experiment time:
- Analysis/sanity-check time:
- Figure/table time:
- Writing/revision time: (if writing-first, the split of the same budget)
- External dependency time:
- Required contingency: (not work time; which plausible failure it covers)
- Total budget required: (e.g. "up to 5 days")
- Main uncertainty drivers:
- Level-specific difficulty, learning overhead, setup/reproduction risk,
  main reason for the estimate:
- Duration feasibility: FITS DURATION / DOES NOT FIT DURATION (standalone,
  vs. D, at level L). If the direction was redesigned or replaced to fit,
  list each step taken (1–4) and why. UNRESOLVED slots state which
  redesign steps and replacement scopes were tried.
- Duration with reused setup (optional, information only):

Difficulty:
(Standalone Expected Work at level L, Execution Risk, External
Dependencies, Difficulty Drivers.)

Hardware fit:

User compute feasibility:

Pilot Success Criterion:

Stop/Pivot Criterion:

Minimum Result Worth Writing Up:

What a negative result would mean:

Main Risk:

Recommended Scope:

Then provide the final schedule table (exactly N rows, one per output slot,
sorted by Project order, UNRESOLVED slots last):

| Project | Schedule Window | Slot (RQk) | Final Research Question | Preserved / Modified / Replaced / Generated / UNRESOLVED | Exact Benchmark | Baseline | Metric | Validity (V1–V4) | Prior-Work Check (iteration) | Gap | Proposed Change | Short-Paper Readiness | Preservation | Experience Level | Standalone Expected Work | Conservative Work Range | Contingency | Total Budget Required | Execution Risk | Duration Feasibility (standalone, vs. D, at L) | Hardware Fit | User Compute Feasibility |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
