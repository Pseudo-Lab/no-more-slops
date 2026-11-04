---
name: research-planner
description: Turn benchmark-backed research questions into tightly scoped, technically meaningful, time-bounded research plans with a credible path to beating the strongest comparable baseline. Actively redesign failing directions (scope levers first) and compare candidate directions.
---

# Research Planner

Design the smallest-scope research plan that still delivers a technically
meaningful contribution with a credible SOTA path, for one or more
benchmark-backed research questions.

Shared definitions (Beginner, technical depth, SOTA potential vs
achievement, D-day feasibility, research redesign, mandatory gates) are
in `~/.claude/skills/research-pipeline/references/research_design_principles.md`.
They win over older wording here, but no gate is ever weakened. The
planner is a research designer, not only a filter: Discover → Diagnose →
Design → Scope → Evaluate → Refine → Select.

Use compute-feasibility results from compute-planner when available.
Do not independently invent detailed hardware requirements.

Upstream evidence this skill consumes, and never re-derives:
- [prior_work_novelty_sota_review.md](../prior-work-checker/references/prior_work_novelty_sota_review.md):
  the Prior-Work Evidence Report schema (§7) and its consumption rules
  (§8). Owned by prior-work-checker, which alone classifies novelty.
- [research-readiness-advisor](../research-readiness-advisor/SKILL.md)
  Steps 5b–5d: SOTA potential S1–S4, technical depth, novelty strength,
  signal complementarity and negative-result readiness. The advisor
  alone rates these.
- compute-planner: FITS DURATION. compute-planner alone decides it.

The planner combines these into the comparison matrix (Step 8b),
selects, and schedules.

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
(`C:\Users\<user>\.claude\skills\benchmark-finder\references\research_advice.md`)
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

Do not ask "How can we make the original idea work?" Ask:

"Given the strongest available exact benchmark, its strongest comparable
baseline and that baseline's documented weakness, what technically
meaningful intervention could beat it? What is the smallest-scope design
that tests it within the user-specified duration D?"

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
  number, gap statement, iteration history), when available, plus the
  Prior-Work Evidence Report (novelty classification, three closest
  prior works, combination analysis, strongest published baseline,
  known failure modes, evidence quality, DRAFT / FINAL)
- Compute feasibility findings, when available
- research-readiness-advisor output (benchmark fit, execution fit,
  original-question preservation, SOTA potential, novelty strength,
  project type, readiness checks, Negative-Result Interpretability Review (six fields, SESOI, required
  controls, PASS / CONDITIONAL / FAIL), short-paper readiness, recommended
  redesign, provisional paper draft, pivot guidance), when available
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

Take the "Closest prior work", "Novelty" and "Strongest comparable
baseline" fields from the Evidence Report, quoted as they appear there.
A slot whose report is still DRAFT can be planned, but it cannot be GO
(Step 8b).

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

"Existing benchmark + strongest comparable baseline + its documented
weakness + one targeted, technically meaningful intervention"

over "completely new phenomenon with no established evaluation."

Determine:

- What has already been evaluated on this benchmark?
- What is the strongest comparable baseline (shared definitions §4a), and
  what is its documented weakness (failure category, subset, error mode,
  stated limitation)?
- What specific, verified gap remains?
- What intervention targets the cause of that weakness? Does it pass
  technical depth (§3)? The entire contribution must not be a fixed
  threshold, vote, average, tuning, or recombination of existing outputs.
- What is the smallest scope (pre-specified slice, reused assets,
  essential experiments only) that tests it?

Modify ONE major variable while keeping the benchmark, metric, and baseline
fixed. "One variable" means isolated, not trivial.


### Step 3: Define the research contribution

Express the proposed project as:

Existing problem:
Established benchmark:
Strongest comparable baseline:
Documented weakness:
Specific gap:
Proposed intervention (mechanism):
Why it should work (causal chain, MDV Q3) and evidence level (E0–E3):
Assumptions and their validity on this benchmark (MDV Q4–Q5):
Simplest alternative explanation and the experiment that separates it
(MDV Q8–Q9; must be in the minimum experiment, Step 4):
Scope of the claim (problem classes where it should and should not
hold; MDV Q6, Q10):
Depth case (technical depth PASS):
Main comparison:
Targeted claim level (§4f: overall SOTA / best reproducible baseline /
selected baseline / restricted protocol):
Novelty type (NT-A application / NT-B modification / NT-C new mechanism
/ NT-D implementation correction; from the Evidence Report):
Expected contribution even if result is negative:
(Take this from research-readiness-advisor's Negative-Result
Interpretability Review, "Negative-result contribution"; do not re-derive
it. It holds only for a sufficiently precise negative result, not for an
inconclusive one.)

The contribution should look like:

existing benchmark
+ strongest comparable baseline
+ documented limitation/gap
+ one targeted, technically meaningful intervention
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
- The required controls, SESOI, and statistical test from
  research-readiness-advisor's Negative-Result Interpretability Review
  (keep them; do not add further controls beyond what it names)

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

Resolve compute only from the global
`~/.claude/skills/compute-planner/references/compute.md`; a project-local
`compute.md` is never required or used as a fallback, and its absence
never implies missing GPU access. Unverified allocation and unknown queue
time are UNKNOWN, never UNAVAILABLE, and alone never lower S4. GPU
directions, including single-GPU 7B–8B experiments, are considered by
default; never prefer a CPU-only or API-only direction solely because GPU
allocation is unverified.

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
short GPU runtime with fitting D.

FITS DURATION (shared definitions §5) means all of the following, so the
project can realistically and reliably be completed within D by a
researcher at level L:
- the STANDALONE total budget (expected active work for the complete
  workflow at level L, plus the separately stated contingency sized to
  the one or two most likely risks) is at most D;
- the conservative work bound is at most D;
- the critical-path wall-clock is at most D.

Further rules:
- Contingency is not planned work.
- Estimates use verified requirements (VERIFIED / ESTIMATE / RISK). They
  are never built from stacked pessimistic assumptions. A speculative
  failure is a RISK with a mitigation.
- Verified existing assets count toward the standalone estimate: public
  code, released models, outputs or activations, and the user's verified
  local environment or allocation. Setup from another *planned* project
  never makes a project fit.
- Beginner never makes GPU, fine-tuning, activation or white-box work
  ineligible (§2).
- For the user's standard D = 4 working days, expected work is about
  3–3.5 days plus 0.5–1 day of contingency.

A project that would fit D for a more experienced researcher but not at
level L is DOES NOT FIT DURATION for this run. Never shrink an estimate, or
evaluate at a more experienced level than L, to make a project fit; redesign
it instead.

- FITS DURATION: keep.
- DOES NOT FIT DURATION: do NOT mark it risky and keep it. Redesign it, in
  this order, until it fits:
  1. Optimise scope while keeping the mechanism and technical depth
     (shared definitions §6), in this order:
     - narrow to the pre-specified documented failure slice;
     - reuse published code and configs;
     - reuse released models, adapters, outputs or activations;
     - remove optional models, layers, seeds and conditions;
     - use a smaller intervention that keeps the mechanism.
  2. Use a more appropriate established benchmark, setting or baseline
     for the same mechanism.
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
annotation, large-scale training from scratch, many interacting
experimental variables, or uncertain evaluation design. Apply this only
after the scope levers have been tried.

Prefer designs that reuse existing repositories, released models,
outputs or activations, published baselines and automatic evaluation.
Fine-tuning (e.g. LoRA on a released model), activation extraction,
probing, and white-box or mechanistic analysis are acceptable, and are
never excluded because the user is a Beginner, when verified tooling and
a scoped design fit D. Technical depth is judged by the mechanism and
insight, not by implementation size.

If, after genuine redesign attempts, a strong design still does not fit,
report the binding bucket and the minimum verified additional time or
resource that would make it fit. Do not give generic advice to extend D.

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
  justify completing the paper or research report? Use the advisor's
  outcome classification: a meaningful negative result needs the effect
  bounded below the SESOI with the manipulation check passed; a
  non-significant but imprecise result is inconclusive, not negative.

These criteria should be compatible with the user-specified duration D
(Step 6).

For short projects, prefer early decision points that preserve enough time
for analysis and writing.

### Step 8: Final filtering and quality assessment

Before ordering, every direction in the portfolio must have:
- passed the SAME-TASK test, comparability check, and validity check V1–V4
  on its final question (Step 1),
- PASSED prior-work-checker on its final question (Step 0), backed by a
  FINAL Evidence Report whose evidence quality is not Unverified,
- no duplicate among the other slots (Step 1b),
- a FITS DURATION verdict against D (Step 6),
- a confirmed short-paper readiness of READY from
  research-readiness-advisor (NEEDS REDESIGN or NOT READY triggers the
  advisor's mechanism-preserving redesign first, then the Step 6 sequence),
- technical depth PASS (advisor Step 5d; shared definitions §3),
- a credible SOTA path: pre-experiment SOTA potential of at least MEDIUM,
  or HIGH if the user required it, unless the user waived this for an
  explicitly scientific-diagnostic goal (§7, gate 9),
- the remaining gates in §7: no data leakage, fair comparison,
  reproducibility, statistical rigor and research integrity.

There is no "risky but kept" category. A slot that cannot meet all of these is
redesigned and, if needed, replaced through the active search in Step 6.
Only if that replacement search also fails does it remain in its slot with
an UNRESOLVED label, outside the feasible portfolio.

The quality criteria below are used to choose between candidate directions
(e.g. when m > N, or when deciding which duplicate to redesign) and for the
Recommendation. They NEVER determine project order. The hard gates above
(validity, prior-work PASS as the minimum novelty requirement, FITS
DURATION, READY) are mandatory and never traded off. Among directions
that pass them, rank strictly in this order (the same topic-ranking order
as research-readiness-advisor Step 5c), applying each criterion only when
directions are comparable on the higher ones:

1. **Credible SOTA potential (PRIMARY, pre-experiment):** an
   evidence-supported opportunity to outperform the strongest *existing*
   baseline on the named task and metric. This is the advisor rating
   from the S1–S4 rubric (§4b), under the evidence rules (§4d):
   - S1 documented weakness and headroom, after the baseline-maturity
     audit (a weak or incomplete baseline set is not headroom);
   - S2 mechanism targeting it, with cause evidence and not only lever
     evidence;
   - S3 fair, reproducible test, with the expected margin ≥ the MDE;
   - S4 feasible MVRD.

   HIGH needs all four STRONG on facts verified now. There is no
   conditional HIGH. Novelty, promise or speculation alone never count.
   HIGH ranks above MEDIUM.
2. **Four-day feasibility margin, given the user's skills:** contingency
   left within D, critical-path slack, share of requirements VERIFIED,
   hardware fit.
3. **Benchmark and evaluation strength:** a public benchmark;
   reproducible baselines (released code, models or per-item outputs);
   a clear metric and a conventional results table; reliable evaluation
   (automatic metric, adequate test size and power, low label noise, no
   contamination).
4. **Clear, measurable contribution (§4e) and technical depth:** a
   non-obvious finding in at least one outcome, plus the strength of the
   pre-mortem answer. Within this criterion, a credible contribution of
   type A or B ranks above C or D (Step 8b). Confirmatory engineering
   (more data, a bigger model or standard fine-tuning with a predictable
   outcome) fails the depth gate.
5. **Novelty strength:** narrow, defensible gap and contribution beyond
   prior work (advisor rating mapped from prior-work-checker's Evidence
   Report). Modest novelty is acceptable when 1–4 are strong.
6. **Negative-result interpretability** (advisor's negative-result
   readiness: PASS > resolved CONDITIONAL > FAIL).
7. **Original-question preservation** and relevance to the user's broad
   interests (final tie-breakers).

This list is the shared ranking order in shared definitions §8, with the
same criteria, numbers and order. If the two ever differ, §8 wins. Topic
area, AI safety or not, is never a ranking criterion (§1d).

Never rank a highly novel direction with weak SOTA potential above a
direction with a credible path to SOTA when both pass every gate.
Scientific-diagnostic directions are eligible only when the user waived
the credible-SOTA-path gate; they are then ranked by the same order.

Never replace a direction merely because an unrelated benchmark project
is easier. Preservation never
overrides a hard gate: a direction loosely related to the original question
but with an excellent exact benchmark still ranks above one that preserves
the original idea but has only a proxy.

Directions without an exact benchmark, or with critical benchmark fields
UNKNOWN, are never ranked alongside benchmark-backed directions as equally
valid candidates; rank them last and label them. The same applies to slots
that did not PASS prior-work-checker.

Compliance with `research_advice.md` overrides this quality assessment
where they conflict, except for the topic-ranking order above, which the
user set explicitly.

### Step 8b: Candidate comparison matrix (mandatory for every shortlisted candidate)

Build one row per shortlisted candidate. This includes candidates
compared for a slot when m > N, duplicates being resolved, and
redesigned or replacement versions. Every column is **copied from its
authoritative source**. The planner judges only the last two columns.

| Field | Content | Source (authority) |
|---|---|---|
| Candidate | The proposed method (one line) | Planner |
| Closest prior work | Three closest papers, where available | Evidence Report (prior-work-checker) |
| Novelty | Classification (NOVEL / PARTIAL OVERLAP / ALREADY STUDIED / UNCERTAIN) **and** the existing gate (PASS / FAIL-<reason> / unresolved) | Evidence Report (prior-work-checker) |
| Strongest comparable baseline | Method, metric, number, source | Evidence Report + mature baseline map (benchmark-finder) |
| SOTA potential | HIGH / MEDIUM / LOW / UNKNOWN, with S1–S4 | research-readiness-advisor Step 5c |
| Improvement mechanism | The evidence-supported explanation: targeted failure mode, cause evidence, and complementarity for combinations | research-readiness-advisor Step 5c items 2–4 |
| Technical depth | PASS / FAIL | research-readiness-advisor Step 5d |
| Mechanism and domain validity | PASS / PASS-EXPLORATORY / FLAG / FAIL, E-level, and whether the Q9 discriminating experiment is in the design | research-readiness-advisor Step 5c item 8 (shared definitions §9) |
| Novelty type | NT-A / NT-B / NT-C / NT-D | Evidence Report (prior-work-checker, resource §5a) |
| Four-day feasibility | FITS DURATION / DOES NOT FIT DURATION / UNKNOWN at D and L | compute-planner (authoritative) |
| Negative-result readiness | PASS / CONDITIONAL / FAIL | research-readiness-advisor Step 5b |
| Expected contribution | A / B / C / D (below) | Planner, from the evidence above |
| Final decision | GO / REVISE / NO-GO (below) | Planner, subject to every gate |

**Contribution types.** Assign the strongest type the evidence supports,
not the type you hope for.

- **A. SOTA improvement.** The method is expected to outperform the
  strongest comparable baseline (§4a) under the same protocol. Claim A
  only if all of these hold:
  - SOTA potential is at least MEDIUM;
  - the S2 mechanism targets a documented failure mode;
  - the expected margin is at least the MDE.
- **B. Significant combination benefit.** A combination is expected to
  give a statistically supported improvement over each individual
  component *and* over the relevant strong baselines. Claim B only if
  all of these hold:
  - the design includes every component-alone arm and the strong
    baselines;
  - there is a pre-registered paired test;
  - the advisor rated signal complementarity COMPLEMENTARY;
  - the expected gain over the best single component is at least the
    MDE.
- **C. Complementary failure-mode evidence.** Evidence that different
  methods detect distinct failure modes, for example from a per-item
  cross-tabulation.
- **D. Mechanistic or diagnostic understanding.** New evidence on when
  and why the methods succeed or fail.

How the types interact with ranking and gates:
- **Contribution type is not a new ranking criterion.** It describes the
  §4e defensible contribution inside the existing order (Step 8 /
  shared definitions §8, criterion 4). Within that criterion, a credible
  A or B ranks above C or D.
- A candidate whose only credible contribution is C or D usually has
  SOTA potential below MEDIUM. It is then eligible only if the user
  waived gate 9 for an explicitly scientific-diagnostic goal.
- Never claim A or B without the supporting evidence listed above. When
  in doubt, record the lower type and name the upgrade condition.

**Final decision:**

| Decision | Meaning |
|---|---|
| **GO** | Every Step 8 gate passes, including MDV (gate 12) PASS or PASS-EXPLORATORY. The Evidence Report is FINAL, and the research-pipeline evidence gate passes. The only allowed condition is unconfirmed compute allocation. A FLAG on MDV is REVISE, never GO |
| **REVISE** | A gate or rating fails, but a redesign lever (shared definitions §6; advisor Step 7) or a named, permitted measurement could fix it. REVISE is a working state. It never appears in the final portfolio as GO and is never a "conditional GO" |
| **NO-GO** | It fails a gate after at least one meaningful redesign attempt, or it is ALREADY STUDIED with no different question available. The slot then follows the existing replacement search (Step 6). If that also fails, the slot is labelled UNRESOLVED |

A positive rating never overrides a failed gate. In particular:
- high novelty strength never compensates for LOW SOTA potential;
- a good readiness rating never compensates for a novelty FAIL or for
  DOES NOT FIT DURATION.

The matrix is used for selection and the Recommendation only. It never
sets project order; Step 9 does.

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
Novelty classification: (from the Evidence Report; quoted, not re-judged)
Evidence Report: `prior_work_evidence_<run-tag>_<RQk>.md` (FINAL; evidence
quality)
Expected contribution: A / B / C / D (Step 8b), with its supporting
evidence
Final decision: GO / REVISE / NO-GO (Step 8b)

Closest prior work and what remains untested:
(From prior-work-checker. "No directly equivalent experiment was found in
the searched literature" — never "no prior work exists".)

Literature gap:
(The gap statement from prior-work-checker.)

Strongest comparable baseline:
(Name, number, source, task, slice, metric, access class; also the
strongest method on the benchmark overall.)

Documented weakness of that baseline:
(Failure category, subset or error mode, with its source.)

Proposed method/change:
(The mechanism, and why it targets the cause of the documented weakness.)

Technical depth:
(PASS, with a one- or two-sentence depth case.)

Main experiment:

Main results table:
Describe exactly what rows and columns would appear.

Minimum ablation/control:

Smallest viable experiment:
(The MVRD. Mark each experiment ESSENTIAL or OPTIONAL. Only ESSENTIAL
experiments are scheduled inside D.)

Refinement history:
(Each redesign attempt: the lever used, what changed, and the
re-evaluated ratings.)

Research readiness (from research-readiness-advisor, confirmed):
(Benchmark fit, Execution fit, Original-question preservation, Project type
(Performance-oriented / Scientific-diagnostic), Short-paper readiness, and
the full provisional paper draft with all unmeasured numerical cells TBD.)

Topic ranking (advisor Step 5c, confirmed; shared definitions §4b):
- Pre-experiment SOTA potential (§8 criterion 1): HIGH / MEDIUM / LOW /
  UNKNOWN.
  Rate each criterion STRONG / PARTIAL / WEAK / UNVERIFIED, with its
  evidence:
  - S1 documented weakness and headroom (baseline number, sourced, with
    its table/figure), plus the mature baseline map with UNMEASURED
    systems (§4d.1–2);
  - S2 mechanism targeting the weakness: cause evidence and lever
    evidence, listed separately (§4d.3);
  - S3 fair, reproducible test: expected effect, its basis, and the MDE
    (§4d.5);
  - S4 feasible MVRD.

  HIGH only if all four are STRONG on facts verified now (no conditional
  HIGH). This is never a claim of achieved SOTA (§4c).
- Four-day feasibility margin (§8 criterion 2).
- Benchmark and evaluation strength (§8 criterion 3): public benchmark,
  reproducible baselines, reliable evaluation.
- Clear, measurable contribution and technical depth (§8 criterion 4):
  the finding if positive, the finding if negative, the predictability
  test, the reviewer pre-mortem (§4e), and the contribution type A–D
  (Step 8b).
- Novelty strength (§8 criterion 5): HIGH / MEDIUM / LOW.
- Negative-result readiness (§8 criterion 6): see the review table below.
- Original-question preservation (§8 criterion 7, tie-breaker).

Discovery record (§1a): Benchmark → Research Question + causal hypothesis
→ Method, in that order.

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
- Total budget required: (expected active work + contingency, e.g. "up to 4 days";
  the conservative work bound and the critical-path wall-clock must also be <= D)
- Five-bucket summary (shared definitions §5): essential implementation /
  compute (active vs wall-clock) / evaluation and statistics / paper writing /
  contingency. Label each line VERIFIED, ESTIMATE or RISK.
- Risks: each with its probability and mitigation (a speculative failure is a
  RISK, not added work)
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

Negative-Result Interpretability Review (from research-readiness-advisor):
| Field | Result |
|---|---|
| Positive-result contribution | |
| Negative-result contribution | |
| Inconclusive-result risk | |
| Independent scientific value | |
| Required controls | |
| Negative-result readiness (§8 criterion 6) | PASS / CONDITIONAL (conditions adopted) / FAIL (performance-dependent) |

Minimum Result Worth Writing Up:

What a negative result would mean:
(Consistent with the review; distinguish meaningful negative from
inconclusive.)

Main Risk:

Recommended Scope:

Then provide the candidate comparison matrix (Step 8b), with one row per
shortlisted candidate, including those not selected.

Then provide the final schedule table (exactly N rows, one per output slot,
sorted by Project order, UNRESOLVED slots last):

| Project | Schedule Window | Slot (RQk) | Final Research Question | Preserved / Modified / Replaced / Generated / UNRESOLVED | Exact Benchmark | Baseline | Metric | Validity (V1–V4) | Prior-Work Check (iteration) | Gap | Proposed Change | SOTA Potential | Novelty Strength | Negative-Result Readiness | Short-Paper Readiness | Preservation | Experience Level | Standalone Expected Work | Conservative Work Range | Contingency | Total Budget Required | Execution Risk | Duration Feasibility (standalone, vs. D, at L) | Hardware Fit | User Compute Feasibility |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
