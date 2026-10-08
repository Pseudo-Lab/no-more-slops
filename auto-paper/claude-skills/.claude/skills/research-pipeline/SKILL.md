---
name: research-pipeline
description: Run the complete research planning pipeline from research-question extraction through benchmark research, prior-work checking, feasibility at a user-specified experience level against a user-specified project duration, experiment planning, and an easiest-to-hardest project schedule.
---

# Research Pipeline

Run the complete research planning workflow using the specialized research
skills.

This skill coordinates:

1. research-question-parser
2. benchmark-finder (candidate search; later, after a benchmark is
   provisionally confirmed, the benchmark-centered prior-work archive —
   Step 2c)
3. research-readiness-advisor (after benchmark-finder identifies candidate
   benchmarks, before slots are fixed; its execution fit is confirmed after
   compute-planner)
4. prior-work-checker (called after benchmark-finder and the advisor;
   loops back to benchmark-finder on FAIL)
5. compute-planner
6. research-planner

Do not replace the specialized responsibilities of these skills.
Use them in the order defined below.

## Core Goal

Optimize for benchmark-centered, experimentally executable research
directions, NOT for preserving the user's original ideas.

## Research Question Format Rule

Every research question the pipeline outputs (cleaned questions, seed
questions, replacement questions, and every "Final research question") must:

1. Be a single interrogative sentence that ends with "?".
2. Start with an interrogative form (Does / Do / Is / Are / Can / Will /
   Which / How much / To what extent ...).
3. Not be an imperative ("Evaluate whether ..."), a noun phrase or title
   ("Effect of X on Y"), a hypothesis statement, or a method description.
4. Contain exactly one question (no chained "... and does ...?", no second
   question mark).

A Final research question must additionally:

5. Name the proposed change, the comparison baseline, the benchmark, and
   the main metric, e.g. "Does <change> <increase / reduce> <metric> on
   <benchmark> compared with <baseline>?"
6. Be answerable directly from the main results table (yes / no, or which
   is better, on the established metric).

Hypotheses stay declarative and are labeled "Hypothesis", never presented
as the research question. Original wording from the input file is quoted
verbatim and labeled "Original", so it is exempt.

Before producing the final output, check every research-question field
against rules 1–6 and rewrite any that fail. The Comparison table must show
each slot's final research question.

## Cardinality Rule

The user may provide:

    Number of research directions: N

When N is provided, it is the authoritative output cardinality. If the user
does NOT provide N, fall back to N = m, the number of parsed research
questions/ideas (CLEAR and POSSIBLE together).

research-question-parser does NOT determine N. CLEAR / POSSIBLE
classifications are metadata only.

The pipeline must return exactly N output slots.

- If parsed ideas m > N: select the N most promising starting points, based
  primarily on exact benchmark availability and research feasibility, using
  research-readiness-advisor's benchmark fit, preliminary execution fit,
  and short-paper readiness to inform the choice.
  Report the unselected ideas (by RQ identifier) as "not selected".
- If parsed ideas m < N: generate additional candidate directions,
  preferably near the user's broad research themes, until N
  benchmark-backed candidates are available. Generated directions get the
  next unused identifiers (RQm+1, ...) and record which theme or RQ inspired
  them.

Original ideas do not need to be preserved.

Priority:

1. Exactly N output slots
2. Exact established benchmark
3. Established baseline and metric
4. Clear narrow literature gap
5. Feasible experiment
6. Similarity to the original ideas

Priorities 2–5 are hard gates (exact benchmark and validity, prior-work
PASS, FITS DURATION). Among candidates for a slot that pass every gate,
prefer HIGH or MEDIUM original-question preservation as rated by
research-readiness-advisor. Do not replace a direction merely because an
unrelated benchmark project is easier; replace it only when no
sufficiently aligned, feasible, benchmark-backed version can be found.
Preservation never overrides a hard gate. (Where `research_advice.md`
says a topic may be discarded for a more feasible benchmark, it is applied
in this sense.)

Never weaken the exact-benchmark standard merely to reach N. If exhaustive
search cannot find N valid benchmark-backed directions, keep all N output
slots but mark each remaining slot:

    UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND

Do not fabricate benchmarks.

Never merge two ideas into one output slot. Multiple directions may
originate from the same broad theme or original idea, but no two final
slots may contain the same research direction. Each output slot carries one RQ identifier, kept
even when its content is replaced (RQ3 original → RQ3 replacement).

Benchmark validity and experimental executability are primary. Preserving
the original topic is secondary.

## Priority Reference

`~/.claude/skills/benchmark-finder/references/research_advice.md`
(`C:\Users\elika\.claude\skills\benchmark-finder\references\research_advice.md`)
is the PRIMARY and HIGHEST-PRIORITY research-planning reference for this
project, and is the FIRST planning reference the pipeline reads.

Research-planning decisions must follow `research_advice.md` unless doing so
would conflict with an explicit current user instruction. Do not let
downstream skill defaults silently override it.

It is mentorship/project-selection guidance, not scientific evidence. It
must NOT be used as evidence that a literature gap exists, a contribution is
novel, a benchmark is established, or a scientific claim is true. Those
require verified literature or benchmark evidence.

Priority: (1) research_advice.md for strategy and project selection,
(2) verified benchmark/literature evidence, (3) user constraints such as
time and compute, (4) original research ideas as candidate interests unless
the user explicitly says a topic is fixed.

This priority holds in BOTH modes below.

## Benchmark Standard

Final recommended directions accept ONLY EXACT / DIRECT established
benchmarks, as defined in benchmark-finder (defined task, public dataset or
standardized evaluation set, defined protocol, established metric, and a
published baseline or prior result, directly evaluating the proposed
problem).

A PROXY BENCHMARK or RELATED DATASET is never sufficient. Phrases such as
"close benchmark", "closest benchmark", "reasonable proxy", "can be
adapted", "could construct a benchmark from...", or "we can derive a new
task from this dataset" are never evidence of benchmark support. A direction
that requires inventing a new task, dataset, evaluation protocol, or metric
does not satisfy the benchmark-first requirement.

Every final direction must pass benchmark-finder's SAME-TASK test: the main
experiment uses the benchmark's already-defined task, its existing
evaluation set, and its established metrics as the main metrics; it can be
compared directly with a published baseline on those metrics; and it does
not define a new target variable, derived task, custom main metric, or new
evaluation protocol (except as purely secondary analysis). A task derived
from a dataset (e.g. a new label predicted and scored with a newly
introduced AUROC) is a RELATED DATASET or PROXY BENCHMARK, never EXACT,
unless that task and metric already exist in the benchmark literature.

Every final direction must also pass the comparability check: this table
must be conceptually valid without inventing a new primary task or metric:

| Method | Established Benchmark Metric |
|---|---|
| Published baseline | reported score |
| Reproduced baseline | reproduced score |
| Proposed method | experimental score |

Otherwise reject the benchmark-direction pair.

Every final direction must also pass benchmark-finder's benchmark validity
check (V1–V4) on its FINAL question: the benchmark directly instantiates
the phenomenon, the metric directly measures the claimed outcome, positive
and negative results would each be evidence about the question, and there
is an established implementation (preferably with a published numerical
baseline). A benchmark that is merely related to the topic is not accepted;
on a mismatch, rewrite the question to match what the benchmark measures or
find a better benchmark.

## Modes

### Benchmark-First Mode (default)

Reasoning order:

1. Set N (see Cardinality Rule) and parse the broad themes of the input
   ideas.
2. For each parsed idea, search for established benchmark tasks; then
   select or generate starting points so there are exactly N slots.
3. Verify the benchmark itself.
4. Identify established baseline methods/results.
5. Identify a narrow gap in existing work.
6. Propose the smallest method/change that addresses that gap.
7. Run prior-work-checker on the resulting research question; on FAIL,
   return to benchmark-finder for a new question for the same slot and
   re-check, until the slot PASSES. The slot's benchmark is then
   PROVISIONALLY CONFIRMED; benchmark-finder builds or extends the
   benchmark-centered prior-work archive, the collision/gap is re-checked
   against it, and research-readiness-advisor re-evaluates the slot with
   the archive evidence. Only then is the benchmark FINAL CONFIRMED
   (Step 2c).
8. Define the controlled experiment using the benchmark's existing protocol.
9. Check compute feasibility, and whether a researcher at the
   user-specified experience level L can finish the full workflow within
   the user-specified per-project duration D, plus level-L
   difficulty (compute-planner).
10. Filter: re-check benchmark validity on the final question, reject
    duplicated directions across slots, and redesign any direction that
    does not fit D at level L (simplify → simpler benchmark/baseline →
    smaller reformulated question → replace) until it fits
    (research-planner).
11. Only after all slots are evaluated, order the projects that fit D at
    level L strictly from easiest/fastest to hardest/slowest for a
    researcher at level L and assign their schedule windows
    (research-planner).

i.e.

benchmark → task → metric → baseline → literature gap → proposed
modification → research question → prior-work check (loop) → experiment
→ user-specified duration D and experience level L → filter/redesign →
keep only projects that fit D at level L → order by level-L difficulty →
assign order/schedule windows

rather than: research question → search for something vaguely
benchmark-like.

For each slot:

A. Search for an exact established benchmark that directly evaluates the
   relevant problem.
B. If one exists, reformulate the research question around it.
C. If only a proxy/related benchmark exists, or the candidate fails the
   SAME-TASK test or comparability check, do NOT force the original
   question onto it. Keep the slot ID and state: "Original direction
   rejected: no exact established benchmark found."
D. First attempt a benchmark-centered redesign that preserves the original
   research mechanism (research-readiness-advisor Step 7). Only if no
   sufficiently aligned version passes, search progressively farther from
   the original topic and replace it,
   under the same slot ID, with a research problem that passes
   exact-benchmark validation: exact established benchmark, reproducible
   baselines, a clear metric, a plausible literature gap, and room for a
   small method modification or controlled experiment.
E. If necessary, move substantially away from the original topic. Do NOT
   lower the benchmark standard to preserve topical similarity.

Rules:

- Do not preserve an original research question merely because it appeared
  in the input file, and do not keep a weak direction for that reason.
- Exactly one final direction per output slot, and exactly N output slots.
  Two ideas may not be merged into one slot, and two slots may not hold the
  same direction.
- Do not force weak directions through the pipeline. It is acceptable to
  say: "This is an interesting research question, but it is a poor
  short-term benchmark-centered project."
- If no exact benchmark can be found even after exhaustive replacement
  search, still output the slot, label it "UNRESOLVED — NO EXACT
  ESTABLISHED BENCHMARK FOUND", and rank it last.
- Do not invent novelty. Verify literature gaps independently.
- The per-project duration D always comes from the user and is a hard
  feasibility constraint. Never hard-code or assume a default duration, and
  never extend D to make a project fit.
- The experience level L always comes from the user. Every feasibility,
  duration, and difficulty estimate is made at level L; never assume a
  level and never estimate at a more experienced level than L.
- Preserve compute-planner's UNKNOWN judgments when hardware access is
  genuinely unknown.
- Keep the benchmark classification separate from Benchmark Readiness.

For short durations, optimize for the probability of obtaining a
COMPLETE, INTERPRETABLE RESULT, not for maximizing conceptual novelty.

### Fixed-Topic Mode

Use only when the user explicitly asks to preserve a particular research
question. That question is not replaced, but the benchmark standard above
still applies: if it has no exact benchmark, state "Original direction
rejected: no exact established benchmark found." and do not attach a proxy.
The Cardinality Rule still holds.

Fixed-topic cardinality conflict (K = number of user-designated fixed
topics):

- If K <= N: fixed topics occupy output slots first; the remaining N - K
  slots are filled normally.
- If K > N: do NOT silently discard fixed topics and do NOT increase N
  automatically. Report:

  "You requested N research directions, but marked K topics as fixed (K > N)."

  and ask the user to either:
  1. increase N to at least K, or
  2. specify which fixed topics should be prioritized.

  Do not proceed with final selection until this conflict is resolved.

If N is not explicitly provided, N = m (all parsed ideas, CLEAR and
POSSIBLE), so K <= N always holds.

Mode selection:

Do NOT ask the user to choose a mode when the intent can reasonably be
inferred.

- Use Fixed-Topic Mode only when the user explicitly indicates that a
  particular research question/topic should be preserved.
- Use Benchmark-First Mode when the user asks for the most feasible
  project, prioritizes a short duration, asks to follow established
  benchmarks, allows the topic or research question to change, or asks for
  project/ranking recommendations without requiring preservation of the
  original topic.
- If the user's intent is genuinely ambiguous, default to Benchmark-First
  Mode, because `research_advice.md` is the highest-priority planning
  reference and favors benchmark-grounded project selection.

Only ask a clarification question when choosing the wrong mode would
materially change the task and the user's intent cannot reasonably be
inferred.

## Input

The user provides:

- A file containing research questions, research ideas, notes, or experiments
- A per-project duration D (how long the user has for EACH project)
- Experience level: Beginner / Intermediate / Advanced (required; levels
  are defined in compute-planner)
- Optional: Number of research directions: N
- Optional: an overall time budget across all projects

The input file, D, the experience level, N, and any overall budget are
user-controlled and must not be hard-coded.

Example:

/research-pipeline

File: experiments.pdf
Time budget: 4 weeks.
Experience level: Beginner
Number of research directions: 5

A single "Time budget" given without further qualification is the
per-project duration D (here, each project must fit in 4 weeks).

If no input file is provided, ask the user which file to analyze.

If no duration is provided, ask the user for one before performing any
duration-feasibility analysis. Never assume one.

If no experience level is provided, ask the user for one before performing
any duration-feasibility or difficulty analysis. Never assume one.

Use only the file specified by the user as the primary source of research questions and ideas unless the user explicitly asks to include other files.

## Workflow

### Step 1: Read the specified research file

Read the file specified by the user completely.

Do not automatically substitute or include other research files.

Use research-question-parser to extract:

- All parsed research questions/ideas RQ1 ... RQm, with CLEAR / POSSIBLE
  as metadata only
- Overlapping questions (reported, not merged)
- m, the number of parsed ideas

Then set N per the Cardinality Rule (user-provided N, otherwise N = m).

Preserve RQ identifiers throughout the rest of the pipeline, including when
a slot's content is replaced. The original questions are kept for
traceability only.

---

### Step 2: Find exact benchmark foundations and fix the N slots

Use benchmark-finder on each parsed idea (RQ1 ... RQm), then
research-readiness-advisor on each candidate (Step 2a), then fix exactly N
output slots:

- m > N: keep the N most promising starting points, chosen primarily by
  exact benchmark availability and research feasibility, informed by the
  advisor's benchmark fit, preliminary execution fit, short-paper
  readiness, and preservation; list the rest as "not selected".
- m < N: ask benchmark-finder for additional benchmark-backed directions
  near the user's broad research themes (identifiers RQm+1, ...) until N
  are available.
- m = N: use all parsed ideas as starting points.

If exhaustive search still leaves slots without a valid exact benchmark,
mark them "UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND". Never weaken
the benchmark standard to reach N.

For each of the N slots, obtain from benchmark-finder:

- Exact / direct benchmark (for the original question, or for a nearby
  replacement problem)
- Original question status: exact benchmark found, or rejected
- Rejected proxy benchmarks / related datasets (traceability only)
- Benchmark verification fields: name, paper/source, task, dataset /
  evaluation set, dataset size, input, output, metric(s), established
  baseline(s), existing reported result(s), public data available?, public
  evaluation code available?, why it DIRECTLY evaluates the proposed
  problem, SAME-TASK test answers (A-E), comparability check result,
  benchmark validity answers (V1–V4)
- Benchmark Readiness, including training required, evaluation type,
  external dependencies, repository maturity, and typical conditions/seeds
- Relevant prior work and literature coverage
- Candidate small gaps around the benchmark

Do not infer verification fields. If a critical benchmark property cannot be
verified, keep it UNKNOWN and do not let the direction be ranked as a strong
recommendation.

Require established benchmarks; never create new tasks, datasets, protocols
or metrics for the main experiment.

If no exact benchmark exists even after exhaustive replacement search, mark
the slot "UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND" rather than
inventing one.

benchmark-finder must express each slot's candidate as a research question
that follows the Research Question Format Rule (rules 1–6).

---

### Step 2a: Research readiness advice

After benchmark-finder has identified candidate benchmarks and before the
N slots are fixed, run research-readiness-advisor on each candidate with
the user's goal, D, and experience level L. Obtain: benchmark fit,
preliminary execution fit, original-question preservation, project type,
the YES/NO readiness checks, prior-work traceability, short-paper
readiness (READY / NEEDS REDESIGN / NOT READY), main reason, and
recommended redesign.

The advisor informs benchmark and research-question selection; it does
not override benchmark-finder's verification, prior-work-checker's
verdict, compute-planner's feasibility, or research-planner's final
design and ordering.

If the advisor rates a candidate NEEDS REDESIGN or NOT READY, first send it
back to benchmark-finder for a benchmark-centered redesign that preserves
the original research mechanism (advisor Step 7). Only replace the research
direction when no sufficiently aligned, feasible, benchmark-backed version
can be found. Every redesign or replacement goes back through
benchmark-finder's validation and this step.

Candidates regenerated later (after a prior-work FAIL or a duration
redesign) also pass through the advisor before being accepted.

---

### Step 2b: Prior-work check loop

After benchmark-finder and the advisor, run prior-work-checker on every slot
with an EXACT / DIRECT benchmark:

research question → relevant benchmark → trace prior work and baselines
that use that benchmark → identify the research gap → PASS / FAIL

- PASS: the slot proceeds to Step 3 with the traced prior-work table, the
  extracted published baseline number, the novelty search coverage
  (N1–N5), the closest prior work and what remains untested, and the gap
  statement.
- FAIL: send the slot back to benchmark-finder with the FAIL reason, the
  blocking prior work, and all previously failed questions for that slot.
  benchmark-finder generates a new research question for the SAME slot ID,
  and prior-work-checker checks it again. Repeat until the slot PASSES.

Do not move a slot to Step 3 until it has PASSED. Do not relax the check to
make a slot pass. A slot leaves the loop without passing only when
benchmark-finder's exhaustive replacement search has no further
non-excluded candidate; mark it
"UNRESOLVED — NO DIRECTION PASSED THE PRIOR-WORK CHECK" and rank it last.

Keep the full iteration history for each slot for the final report.

---

### Step 2c: Build the prior-work archive, re-check, re-evaluate readiness, final-confirm

Order:

research-question-parser → benchmark-finder finds candidate benchmarks →
research-readiness-advisor helps select the benchmark/RQ → prior-work-checker
PASS → benchmark PROVISIONALLY CONFIRMED → benchmark-finder comprehensive
benchmark-centered prior-work search (archive) → collision/gap re-checked →
research-readiness-advisor re-evaluates with the archive evidence →
benchmark FINAL CONFIRMED → compute-planner → research-planner

1. A slot's benchmark is PROVISIONALLY CONFIRMED once it passed the
   exact-benchmark checks, the advisor selected it, and the slot's question
   PASSED prior-work-checker. Do not build archives for candidates that are
   not provisionally confirmed.
2. Run benchmark-finder Step 5 for each provisionally confirmed benchmark:
   a comprehensive benchmark-centered prior-work search, saved to
   `prior_work_<benchmark_name>.md` in the project working directory.
   Slots sharing a benchmark reuse and extend the same file.
3. Re-check the collision and gap: re-run prior-work-checker on the slot's
   question with the archive's inventory as additional traced sources, and
   use the archive's collision verdict.
   - NO EVIDENCE FOUND or PARTIAL OVERLAP: continue to step 4 below, using
     the archive's selected baseline, closest prior work, and gap statement
     (PARTIAL overlaps are stated in the gap).
   - STRONG OVERLAP or ALREADY TESTED: do NOT continue as though the
     project were unchanged. Return the slot to research-question /
     benchmark selection or redesign (benchmark-finder regeneration, then
     Step 2a and Step 2b), keeping the slot ID and recording the blocking
     papers as excluded.
4. Readiness re-evaluation: run research-readiness-advisor again on the
   slot, using the archive evidence (advisor "Archive re-evaluation").
   Re-evaluate benchmark fit, original-question preservation, baseline
   choice, main-table feasibility, ablation/control feasibility, prior-work
   traceability, remaining contribution, and short-paper readiness.
   - READY: the benchmark becomes FINAL CONFIRMED; continue to Step 3 and
     then compute-planner.
   - NEEDS REDESIGN or NOT READY: the benchmark is not final confirmed.
     Handle it exactly as a Step 2a rejection (mechanism-preserving
     redesign first, replacement only if no aligned version exists), then
     repeat Steps 2b and 2c for the redesigned slot.
5. If a slot's final confirmed benchmark changes at any later point
   (redesign or replacement), the new benchmark goes through this step from
   provisional confirmation onward. Old archives are kept.

Only FINAL CONFIRMED slots proceed to compute-planner.

The full paper inventory stays in the archive files, not in the main
report.

---

### Step 3: Define a minimal compute-evaluation configuration

Using the benchmark and prior-work findings, define only enough experimental
detail to allow compute-planner to estimate compute requirements.

This is NOT the final experiment design.
The final research design belongs to research-planner.

Specify only the minimum necessary information, such as:

- Candidate model or models
- Benchmark or dataset
- Approximate dataset size
- Training vs. inference
- Number of experimental conditions
- Approximate number of runs or seeds
- API / closed-model dependencies and LLM-judge calls, if any
- Whether evaluation is automatic
- Public repository and baseline code (from Benchmark Readiness)

Prefer reusing:

- Existing benchmark
- Existing dataset
- Existing evaluation infrastructure
- Existing checkpoints

Do not add experimental components merely for novelty.

This configuration exists only for compute estimation and may be revised by
research-planner when constructing the final research plan.

---

### Step 4: Evaluate compute feasibility

Use compute-planner on the smallest plausible experiment for each slot.

Pass all relevant information from the previous steps, including:

- Research question
- Benchmark
- Dataset
- Baseline
- Proposed modification
- Candidate model or models
- Experimental conditions

Always pass the user-specified per-project duration D and experience
level L, and the experience-sensitive factors from Benchmark Readiness.

For each direction, obtain:

- Estimated compute requirements
- Hardware fit
- User feasibility
- Compute feasibility
- Main compute bottleneck
- Recommended compute reduction, if necessary
- Standalone workflow estimate at level L (working days per phase, rounded
  to 0.25 or 0.5, estimated from the project rather than a template)
- Standalone expected work, standalone conservative work range, required
  contingency (stated separately, not as work), and total budget required
- Main uncertainty drivers, level-specific difficulty, learning overhead,
  setup/reproduction risk, and main reason for the estimate
- Duration Feasibility verdict against D at level L, based on the
  standalone total budget (FITS DURATION / DOES NOT FIT DURATION /
  UNKNOWN), limiting phase, and redesign options with re-estimated totals
- Optionally, duration with reused setup (information only)
- Difficulty estimate at level L (Standalone Expected Work, Execution Risk,
  External Dependencies, Difficulty Drivers)

If research-readiness-advisor recommends writing first, compute-planner's
estimate includes both the pre-experiment full provisional paper draft and
the post-experiment result insertion and revision, as parts of the same
writing budget; writing is not counted twice.

Do not independently override compute-planner's feasibility or difficulty
assessment.

Do not infer user-accessible GPUs from cluster-wide hardware. If exact user
GPU access is unknown, keep User Feasibility = UNKNOWN and state what
information is missing, but still evaluate Hardware Fit for the smallest
plausible experiment. Do not reject a direction solely because user-specific
GPU access is UNKNOWN.

After compute-planner, have research-readiness-advisor CONFIRM its
execution fit and short-paper readiness using compute-planner's verdict
(DOES NOT FIT DURATION means execution fit LOW). For READY projects, the
advisor writes the full provisional paper draft before the experiment
(advisor Step 8): all sections including the Conclusion, written under the
working hypothesis, with every unmeasured numerical cell TBD.

---

### Step 5: Build benchmark-centered research plans

Use research-planner to create exactly one final research plan per slot.

Provide research-planner with:

- Slot identifier and original question
- Exact benchmark and its verification fields
- Original question status (preserved / rejected and replaced)
- Benchmark Readiness
- Reusable benchmark components
- The PASSED research question (verbatim, in question format)
- Benchmark validity answers (V1–V4)
- research-readiness-advisor output (confirmed): benchmark fit, execution
  fit, original-question preservation, project type, readiness checks,
  short-paper readiness, recommended redesign, provisional paper draft,
  and pivot guidance
- prior-work-checker output: prior-work table, traced baseline number,
  novelty search coverage (N1–N5), closest prior work and what remains
  untested, gap statement, iteration history
- Prior-work archive summary (Step 2c): archive file path, selected
  baseline, closest prior work, collision verdict, and final gap
- Compute-planner findings at level L, including the workflow estimate,
  the experience-level fields, Duration Feasibility verdict, redesign
  options, and difficulty estimate
- The user-specified per-project duration D (and any overall budget)
- The user-specified experience level L

research-planner must keep the PASSED research question's change,
baseline, benchmark and metric. If planning requires changing any of
these, the new question goes back through Step 2b.

The plan should follow:

existing benchmark
+ established baseline
+ clearly identified limitation/gap
+ one small modification
+ controlled comparison

and be able to produce a conventional benchmark results table (published
baseline, reproduced baseline, proposed method). Modify ONE major variable
while keeping the benchmark, metric, and baseline fixed.

Do not recommend a direction whose main contribution is only correlation
analysis, exploratory visualization, qualitative observation, a new custom
dataset, a new custom metric, a new evaluation protocol, "does phenomenon X
exist?", or an analysis that cannot be compared against an established
baseline. These may only be secondary analyses.

Do not expand the experiment merely to make the project appear more novel.

Prefer the smallest experiment capable of producing a meaningful and
interpretable result.

---

### Step 6: Filter, redesign, and order

Use research-planner's final filtering and redesign (its Steps 1, 1b, 6
and 8) and its mandatory ordering (its Step 9). Do not re-rank or re-order
here.

This guarantees that, before output:

1. Every final benchmark/question pair has passed the benchmark validity
   check (V1–V4) on its FINAL question; mismatches were repaired (question
   rewritten to match the benchmark) or the benchmark was replaced.
2. No final question is already done, functionally equivalent to, or
   substantially answered by prior work (prior-work-checker), and no two
   slots are duplicates of each other (research-planner Step 1b).
3. Every project in the final portfolio FITS the user-specified duration D
   for a researcher at the user-specified experience level L across the
   FULL workflow (compute-planner): its standalone total budget
   (conservative work + separately stated contingency) fits D, without
   counting setup reused from another project. Projects that did not fit were
   redesigned in order (simplify → simpler established benchmark/baseline →
   smaller reformulated question → replacement by an actively searched,
   different benchmark-centered question), never kept as "risky" and never
   fitted by extending D. Every replacement passed Benchmark Validity, the
   prior-work check, and FITS DURATION.
4. Feasible projects are ordered Project 1 ... strictly from
   easiest/fastest to hardest/slowest for a researcher at level L (not a
   generic researcher), only after all slots were evaluated, each with its
   schedule window of length D.

The pipeline must actively try to return N valid projects. A slot is never
left UNRESOLVED merely because the original question or its nearby
variants fail; it is first redesigned and then replaced through an active
search for alternative research questions (research-planner Step 6). Only
when that reasonable replacement search has also failed does a slot keep
its place (cardinality) with an UNRESOLVED label, outside the feasible
portfolio, listed after the ordered projects, with the steps and search
scopes that were tried.

---

## Duration Rules

The per-project duration D always comes from the user and is a HARD
feasibility constraint. Never hard-code or assume a default, and never
extend D to make a project fit. Examples: D = 1 week → propose only
projects a researcher at level L can realistically finish end-to-end in
1 week; D = 4 weeks → evaluate against 4 weeks; any other D → use that D.

D covers the FULL workflow: understanding the benchmark and relevant prior
work, reproducing the baseline, implementation, debugging, experiments,
analysis, figures/tables, and writing the required paper.

All feasibility and time estimates are made at the user-specified
experience level L (Beginner / Intermediate / Advanced, defined in
compute-planner). The level materially changes the estimate (learning
overhead, setup and reproduction overhead, uncertainty for
experience-sensitive factors). A project that would fit for a more
experienced researcher but not at level L is DOES NOT FIT DURATION for
this run. Never shrink an estimate to make a project fit.

A project FITS DURATION only if its STANDALONE total budget required — the
conservative upper bound of estimated work for the complete workflow at
level L, plus a separately stated required contingency sized to the
project's risks — fits within D, i.e. it can realistically and reliably be
completed within D, not merely theoretically finished. No fixed percentage
or fixed buffer is used. Contingency is never counted as planned work, and
setup reused from another project never makes a project fit (a reuse
estimate may be shown as information only). D is in working days (1 week =
5 working days unless the user states otherwise). When D is 5 working days,
a Beginner project's expected work should normally be at most about 3.5–4
days; a conservative workload of about 5 days is normally DOES NOT FIT
DURATION unless unusually low execution risk is explicitly justified.
Estimates are realistic, project-specific, and rounded to 0.25 or 0.5 day;
compute-planner holds the detailed phase rules (including Beginner defaults
for reproduction, analysis, and writing).

Per-project feasibility is estimated by compute-planner (Step 6 of that
skill) and enforced by research-planner (its Step 6). Do not re-estimate it
here. Short GPU runtime never implies that a project fits D.

If the user also gives an overall time budget shorter than N × D, report
the conflict instead of shortening D.

Prefer the smallest meaningful experiment that fits comfortably within D.

---

## Final Output

### Input Ideas and Slots

List all m parsed ideas (RQ1 ... RQm, with CLEAR / POSSIBLE metadata).
State N and its source (user-provided, or N = m). List which ideas were
selected as starting points, which were not selected, and which slots were
generated (RQm+1, ...).

---

### Directions

State the user-specified duration D. List the feasible projects in order
(Project 1 = easiest/fastest first), then any UNRESOLVED slots, one entry
per output slot, using the slot's identifier. Use the same fields as
research-planner's Final Output, except that prior work is condensed to
the concise block below with a reference to the archive file:

### Project p (schedule window) — Direction RQk

Original question: (or "Generated — inspired by <theme / RQ>")
Preserved / Modified / Replaced / Generated / UNRESOLVED:
(If rejected: "Original direction rejected: no exact established benchmark found.")

Final research question:
(One interrogative sentence ending with "?", naming the change, baseline,
benchmark and metric; see Research Question Format Rule.)

Hypothesis:

Problem:

Exact established benchmark:
Benchmark source:
Dataset/evaluation set:
Metric:
Baseline:
Published baseline result:
(The extracted number and its table/figure, from prior-work-checker.)

Why this is an EXACT benchmark rather than a proxy:
(include SAME-TASK test answers A-E)

Benchmark validity:
(V1–V4 for the final question; note any rewrite made to fix a mismatch.)

Prior work (concise; the full inventory is in the archive file):
- Final confirmed benchmark:
- Selected baseline: (with its source)
- Closest prior work: (1–3 papers, and how each differs)
- Collision verdict: NO EVIDENCE FOUND / PARTIAL OVERLAP (STRONG OVERLAP
  and ALREADY TESTED never reach the final report; they send the slot back
  to selection)
- Final research gap: (gap type and statement, from the archive)
- Prior-work archive: `prior_work_<benchmark_name>.md`
- Prior-work check: PASS at iteration n (earlier failed questions listed
  only by question and FAIL reason)

Do not reproduce the full prior-work inventory, search log, or benchmark
history in the main report.

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

Project plan order:
benchmark + baseline selection → method selection → full provisional paper
draft including Conclusion → experiment → fill results → revise
method/paper if necessary → final paper
(If the intended result is not achieved: diagnose, keep the core method
where reasonable, make small justified changes, rerun within the remaining
budget; if it still fails within the stop/pivot budget, rewrite the
Abstract, Results, Discussion, and Conclusion to match the evidence.)

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

---

### Project Schedule

| Project | Schedule Window | Slot (RQk) | Final Research Question | Preserved / Modified / Replaced / Generated / UNRESOLVED | Exact Benchmark | Baseline | Metric | Validity (V1–V4) | Collision Verdict | Gap | Prior-Work Archive | Proposed Change | Short-Paper Readiness | Preservation | Experience Level | Standalone Expected Work | Conservative Work Range | Contingency | Total Budget Required | Execution Risk | Duration Feasibility (standalone, vs. D, at L) | Hardware Fit | User Compute Feasibility |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

The table must contain exactly N rows, one per output slot: feasible
projects sorted by Project order (easiest/fastest first), then UNRESOLVED
slots. Order comes only from research-planner's Step 9 difficulty
ordering, never from importance, novelty, or the original question order.

---

### Recommendation

Answer: "Which benchmark-grounded project should the user actually execute
within the user-specified duration D?" rather than "Which of the user's
original ideas is best?"

Explain briefly why each recommended direction is stronger than the
alternatives. The recommendation does not change the project order.

Do not recommend a direction solely because it appears novel.
