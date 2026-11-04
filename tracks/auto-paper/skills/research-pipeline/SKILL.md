---
name: research-pipeline
description: Run the complete research planning pipeline as a proactive research designer (Discover → Diagnose → Design → Scope → Evaluate → Refine → Select). It covers research-question extraction or broad discovery from user-named sources; benchmark research; diagnosing the strongest comparable baseline's documented weaknesses; designing and scoping technically meaningful interventions with at least one redesign before any rejection; prior-work checking; verified-requirements feasibility at a user-specified experience level against a user-specified duration; experiment planning; and an easiest-to-hardest project schedule.
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
   benchmarks, before slots are fixed; includes the mandatory
   Negative-Result Interpretability Review, confirmed before FINAL
   CONFIRMED in Step 2c; its execution fit is confirmed after
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

Act as a **research designer, not a feasibility filter**. Shared
definitions are in
`~/.claude/skills/research-pipeline/references/research_design_principles.md`.
Read it first: it defines Beginner, technical depth, SOTA potential vs
achievement, D-day feasibility, research redesign and the mandatory
gates. Every coordinated skill uses the same definitions.

The prior-work, novelty and SOTA-evidence procedure is
[prior_work_novelty_sota_review.md](../prior-work-checker/references/prior_work_novelty_sota_review.md),
owned by prior-work-checker. It defines:
- the three-stage literature investigation;
- the novelty classification and its mapping onto the PASS / FAIL gate;
- the Prior-Work Evidence Report that every downstream step reads.

This pipeline enforces that procedure through Step 2b and the
pre-implementation evidence gate (Step 5b). It never runs its own
novelty review.

Skills coordinated (workflow transitions, not recursive calls):
- [benchmark-finder](../benchmark-finder/SKILL.md)
- [prior-work-checker](../prior-work-checker/SKILL.md)
- [research-readiness-advisor](../research-readiness-advisor/SKILL.md)
- [compute-planner](../compute-planner/SKILL.md)
- [research-planner](../research-planner/SKILL.md)

Process every candidate through:

**Discover → Diagnose → Design → Scope → Evaluate → Refine → Select**

| Stage | What happens |
|---|---|
| Discover | Use the user's file and/or user-named sources (e.g. leaderboards, recent papers, public repositories; safety sources such as Shallow Review or Inspect Evals only when named). The scope is any area of AI/ML; technical AI safety is not required (shared definitions §1d). Screen at least 10–15 benchmarks across at least six subfields, then rank them and select three **before** any research question (benchmark-screening stage, §1c). Apply the anti-fixation rules (§1b). Output: a ranked benchmark screening table and three selected benchmarks. |
| Diagnose | Run the baseline-maturity audit (§4d.1). Then find the strongest existing baseline, its documented weaknesses and the benchmark's open questions. Write the research question and causal hypothesis **before naming any method** (§1a). |
| Design | Choose or design a method that tests that causal hypothesis and targets the cause of the weakness (§1a step 3, §4e). |
| Scope | Build a minimal viable research design. Separate essential from optional work. Reuse released code, models, outputs and activations. |
| Evaluate | Apply the mandatory gates. Rate SOTA potential (S1–S4), technical depth and verified-requirements feasibility. |
| Refine | Attempt at least one meaningful redesign before rejecting anything. |
| Select | Rank and select. |

The primary research objective is a **credible path to outperforming the
strongest comparable baseline** (SOTA), with meaningful technical depth.
Rules for that objective:
- Do not guarantee SOTA before the experiment.
- Do not reject a candidate because its outcome is uncertain.
- Never present a narrow-slice result as overall SOTA.
- Do not repeatedly recommend extending the deadline or lowering
  standards without first optimizing scope.

## Discovery Order and Anti-Fixation (mandatory)

**Discovery order: Benchmark → Research Question → Method**
(shared definitions §1a).
- benchmark-finder outputs benchmarks with their mature baseline map,
  documented failures and open questions.
- The research question and its causal hypothesis are then written from
  one documented failure.
- Only then is a method chosen (advisor Step 5).
- Every slot's report contains a three-line **Discovery record** that
  shows this order: Benchmark → Question + hypothesis → Method.
- A method-first candidate is sent back to the question step.

**Benchmark-screening stage** (shared definitions §1c; mandatory, in this
order):
1. Screen at least 10–15 diverse public benchmarks across AI/ML
   subfields.
2. For each, record the strongest existing methods and their published
   numbers.
3. Record the documented failure modes and the realistic headroom.
4. Rank the benchmarks by SOTA-improvement potential, then by
   feasibility.
5. Select the three most promising benchmarks.
6. Only then formulate research questions.
7. Propose methods last, after checking prior work.

Apply the **early kill check**: before investing heavily in one idea,
verify that no stronger existing method already solves the problem and
that the method itself is not already published. This is prior-work-checker
**Stage 1 (rapid screening)**:
- run it on every candidate;
- KILL clearly unsuitable ones before any Stage 2 effort;
- run Stage 2 (focused investigation) only for shortlisted candidates;
- run Stage 3 (final verification) only for candidates about to receive
  GO, plus backups.

The literature stages are part of the planning budget. Promising
candidates are never verified less thoroughly to save time.

**Anti-fixation** (shared definitions §1b):
- Cover at least six AI/ML subfields (any area of AI/ML, not only AI
  safety), with at least two benchmark candidates each, before
  shortlisting. Include the coverage table and the screening table in
  the report.
- Concentration caps: at most one final slot per benchmark and per
  subfield, and no more than 40% of the shortlist from one subfield.
- **Before discovery**, read this user's previous two discovery reports
  in the working directory. List every benchmark, subfield and mechanism
  they selected or proposed as GO/REVISE as **previously explored**,
  with its recorded failure reason.
  - These are excluded by default.
  - One may return only with new verified evidence, dated after that
    report, that removes its failure reason.
  - Prior archives and memory notes are never seeds for new topics.
- Immature benchmarks (< 3 months old, or author-only baselines) hold at
  most one slot, and only after the maturity audit.

**Defensible contribution** (shared definitions §4e): every candidate
records the following, and confirmatory engineering fails the depth gate:
- the finding if positive;
- the finding if negative;
- the predictability test;
- the reviewer pre-mortem.

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

The pipeline reports exactly N output slots, but only slots that pass
every gate are **GO**. Never pad: a slot that does not pass is reported as
UNRESOLVED or NO-GO with its reason, never as a "GO (conditional)".
The only allowed GO condition is unconfirmed compute allocation.
Shortfalls are stated explicitly.

- If parsed ideas m > N: select the N most promising starting points, based
  primarily on exact benchmark availability and research feasibility, using
  research-readiness-advisor's benchmark fit, preliminary execution fit,
  negative-result readiness, and short-paper readiness to inform the
  choice.
  Report the unselected ideas (by RQ identifier) as "not selected".
- If parsed ideas m < N: generate additional candidate directions,
  preferably near the user's broad research themes, until N
  benchmark-backed candidates are available. Generated directions get the
  next unused identifiers (RQm+1, ...) and record which theme or RQ inspired
  them.

Original ideas do not need to be preserved.

Priority:

1. Exactly N output slots reported (GO only if every gate passes; never
   padded)
2. Exact established benchmark
3. Established baseline and metric
4. Clear narrow literature gap
5. Feasible experiment
6. Similarity to the original ideas

The mandatory gates are those in shared definitions §7. They are never
traded off against the ranking below:
1. exact benchmark and validity;
2. no data leakage;
3. fair baseline comparison;
4. prior-work PASS as the minimum novelty requirement;
5. reproducibility;
6. statistical rigor;
7. research integrity;
8. technical depth PASS, including the defensible-contribution test
   (§4e);
9. a credible SOTA path, meaning SOTA potential of at least MEDIUM,
   rated under the evidence rules (§4d);
10. FITS DURATION;
11. discovery process: the Benchmark → Question → Method order, and the
    anti-fixation rules (§1a, §1b).

On gate 9: the user may raise it to "HIGH required" or waive it for an
explicitly scientific-diagnostic goal.

A candidate that fails a gate is redesigned (shared definitions §6)
before it is rejected.

Topic-ranking order (among candidates for a slot that pass every gate;
defined in shared definitions §8 and research-readiness-advisor Step 5c,
and applied identically by research-planner):

1. **Credible SOTA potential (PRIMARY, pre-experiment):** an
   evidence-supported opportunity to outperform the strongest *existing*
   baseline on the named task and metric. It is rated with the S1–S4
   rubric (§4b) under the evidence rules (§4d):
   - S1 documented weakness and headroom, **after the baseline-maturity
     audit**; a weak or incomplete baseline set is not headroom;
   - S2 mechanism targeting that weakness, needing **cause evidence**, not
     only lever evidence;
   - S3 fair, reproducible test, with the expected margin ≥ the MDE;
   - S4 feasible minimal design.

   HIGH needs all four STRONG on facts verified now. There is no
   conditional HIGH. Speculation is never enough. HIGH ranks above
   MEDIUM.
2. **Four-day feasibility margin, given the user's skills:** contingency
   left; verified rather than estimated requirements.
3. **Benchmark and evaluation strength:** public benchmark,
   reproducible baselines, reliable evaluation (§8 item 3).
4. **Clear, measurable contribution (§4e):** a non-obvious finding in
   at least one outcome, the strength of the pre-mortem answer, and
   technical depth.
5. **Novelty strength.** Important but secondary. Modest novelty is
   acceptable when 1–4 are strong.
6. **Negative-result readiness.**
7. **Original-question preservation** (final tie-breaker).

Topic area is never a ranking criterion. AI/ML topics unrelated to AI
safety compete on equal terms (§1d).

Each criterion applies only when candidates are comparable on the higher
ones. Never prefer a highly novel topic with weak SOTA potential over a
topic with a credible path to SOTA when both pass every gate. This
ranking selects candidates and drives the Recommendation; it never sets
project order (that is research-planner's difficulty ordering).

Do not replace a direction merely because an
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
(`C:\Users\<user>\.claude\skills\benchmark-finder\references\research_advice.md`)
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
4. Identify established baseline methods/results, and determine the
   strongest comparable baseline (shared definitions §4a).
5. Diagnose that baseline's documented weaknesses: failure categories,
   subsets, error modes, and the authors' own stated limitations. Prefer
   evidence from released results or per-item outputs. Identify the
   narrow, verified gap in existing work.
6. Design a technically meaningful intervention that targets the cause of
   the diagnosed weakness (technical depth, §3). Scope it into a minimal
   viable research design: one isolated intervention, a pre-specified
   slice if justified, reused assets, and essential vs optional work
   separated.
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
10. Refine and filter (research-planner):
    - re-check benchmark validity on the final question;
    - reject duplicated directions across slots;
    - redesign any direction that fails a gate (feasibility, depth or
      SOTA path) with the scope levers (§6) first: narrow to the
      documented failure slice → reuse code → reuse models, outputs or
      activations → cut optional scope → smaller intervention that keeps
      the mechanism → better benchmark or setting. Only then
      reformulate, and only then replace, until the direction passes.
11. Only after all slots are evaluated, order the projects that fit D at
    level L strictly from easiest/fastest to hardest/slowest for a
    researcher at level L and assign their schedule windows
    (research-planner).

i.e.

benchmark → task → metric → strongest comparable baseline → diagnosed
weakness → literature gap → designed intervention → scoped MVRD →
research question → prior-work check (loop) → experiment → user-specified
duration D and experience level L (verified-requirements estimate) →
refine/redesign → keep only projects that pass every gate → order by
level-L difficulty → assign order/schedule windows

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
   targeted, technically meaningful intervention or controlled experiment.
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
- Every stage resolves compute only from the global
  `~/.claude/skills/compute-planner/references/compute.md` (single source
  of truth). A project-local `compute.md` is never required and never a
  fallback; a missing or empty local copy never implies missing GPU
  access.
- Keep the benchmark classification separate from Benchmark Readiness.

For short durations, optimize for the probability of obtaining a
COMPLETE, INTERPRETABLE RESULT from a technically meaningful intervention
with a credible SOTA path, not for maximizing conceptual novelty. Do this
by scoping (shared definitions §6), not by lowering technical depth.
Beginner never excludes GPU, fine-tuning, activation analysis,
mechanistic interpretability or white-box work (§2). Those approaches
are judged on verified tooling and a scoped design.
- Unconfirmed GPU access is recorded as a RISK with a mitigation, not as
  a rejection, and never by itself lowers S4 or SOTA potential.
- Unverified allocation and unknown queue time are UNKNOWN, never
  UNAVAILABLE. Do not assume unrestricted access or guaranteed
  scheduling either.
- GPU-based research, including single-GPU 7B–8B experiments on H100,
  H200, A40 or V100, is considered by default. Never prefer a CPU-only or
  API-only design solely because GPU allocation is unverified.
- The "UNKNOWN" judgments above stay UNKNOWN; they are never treated as
  a FAIL.

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

If no input file and no discovery sources are provided, ask the user
which file or sources to use.

If no duration is provided, ask the user for one before performing any
duration-feasibility analysis. Never assume one.

If no experience level is provided, ask the user for one before performing
any duration-feasibility or difficulty analysis. Never assume one.

Use only the file specified by the user as the primary source of research
questions and ideas, unless the user explicitly asks to include other
files or names other discovery sources. Examples of such sources:
- URLs such as Shallow Review or Inspect Evals;
- "recent literature";
- "any area of AI/ML" (the default scope; technical AI safety is
  optional, not required).

When discovery sources are named, run the Discover stage across them. Turn
the strongest benchmark-backed opportunities into candidate slots
(identifiers RQ1, RQ2, ...), each recording its source. The input file
is then optional.

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

- m > N: among starting points with exact benchmark availability that
  plausibly pass the gates (after the advisor's design and scoping), keep
  the N best by the topic-ranking order (shared definitions §8),
  applied to the advisor's preliminary ratings:
  1. SOTA potential;
  2. feasibility margin;
  3. benchmark and evaluation strength;
  4. defensible contribution and technical depth;
  5. novelty strength;
  6. negative-result readiness;
  7. preservation.

  Check short-paper readiness, and list the rest as "not selected".
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
- Candidate gaps around the benchmark
- The strongest comparable baseline, with its number, source, task, slice,
  metric and access class
- That baseline's documented weaknesses (failure categories, subsets,
  error modes, stated limitations), with their sources
- Reusable assets, VERIFIED in the actual repository or model hub:
  - code and configs;
  - released models and adapters;
  - released outputs, per-item scores and activations

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
the user's goal, D, and experience level L. The advisor acts as a
designer first: it diagnoses the strongest comparable baseline's
weakness, and designs and scopes the intervention. Obtain:
- strongest comparable baseline;
- documented weakness;
- proposed mechanism;
- technical depth PASS / FAIL with the depth case (advisor Step 5d);
- refinement history (advisor Step 7);
- benchmark fit;
- preliminary execution fit;
- original-question preservation;
- pre-experiment SOTA potential S1–S4 and novelty strength (advisor
  Step 5c, PRELIMINARY);
- project type;
the YES/NO readiness checks, prior-work traceability, the
Negative-Result Interpretability Review (advisor Step 5b: positive-result
contribution, negative-result contribution, inconclusive-result risk,
independent scientific value, required controls, and negative-result
readiness PASS / CONDITIONAL / FAIL, PRELIMINARY at this stage),
short-paper readiness (READY / NEEDS REDESIGN / NOT READY), main reason,
and recommended redesign.

The review is mandatory for every candidate, including regenerated ones.
It does not re-check benchmark validity V3 (benchmark-finder) or decide
novelty (prior-work-checker); it consumes their outputs. For CONDITIONAL
or FAIL, apply the advisor's minimal negative-result fixes (Step 7 a–d)
before considering replacement. The review is mandatory, but its rating
is the sixth ranking criterion (shared definitions §8, criterion 6), not
a gate; a FAIL remains eligible
(labeled performance-dependent, with its inconclusive-result risk stated).

The advisor informs benchmark and research-question selection; it does
not override benchmark-finder's verification, prior-work-checker's
verdict, compute-planner's feasibility, or research-planner's final
design and ordering.

No candidate is rejected (NOT READY, or dropped for feasibility, depth or
SOTA potential) until the advisor has recorded at least one meaningful
redesign attempt using the scope levers (advisor Step 7; shared
definitions §6) and re-evaluated it.

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

This is prior-work-checker **Stage 2 (focused investigation)**. Besides
the benchmark-centered trace, it runs:
- the multi-source, multi-strategy search (Q1–Q9);
- the combination analysis for multi-component methods;
- the three-closest-papers table;
- the novelty classification, mapped onto PASS / FAIL.

It writes the Prior-Work Evidence Report
(`prior_work_evidence_<run-tag>_<RQk>.md`, status DRAFT). Downstream
steps read that report instead of repeating the review.

- PASS: the slot proceeds to Step 3 with the traced prior-work table, the
  extracted published baseline number, the novelty search coverage
  (N1–N5 and Q1–Q9), the closest prior work and what remains untested,
  the gap statement, the novelty classification and the Evidence Report
  path.
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
   traceability, remaining contribution, SOTA potential and novelty
   strength (re-rated with the archive's baseline map, current best
   result, collision verdict and gap), negative-result readiness (item 6,
   novelty of the positive and negative finding, confirmed against the
   archive), and short-paper readiness.
   This is the final topic-confirmation point: a slot is not FINAL
   CONFIRMED until the Negative-Result Interpretability Review is
   completed (with any CONDITIONAL conditions written into the design and
   a minimal redesign attempted for FAIL) and SOTA potential and novelty
   strength have been re-rated. If a gate-passing alternative for the slot
   ranks higher by the topic-ranking order, prefer it.
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
- Any minimal controls, pilot power check, or extra seeds required by the
  Negative-Result Interpretability Review (CONDITIONAL conditions)
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

The paper is drafted primarily by AI (paper-writer). The writing bucket
therefore budgets only human review and verification, about 0.5 day at
Beginner (range 0.5–0.75; shared definitions §5):
- checking numbers against output files;
- checking citations against sources;
- checking that claims match the evidence and the pre-registered
  criteria;
- figures, captions and limitations;
- a final read.

Verification time is never cut to make a project fit.

Do not independently override compute-planner's feasibility or difficulty
assessment.

Do not infer confirmed user allocations from cluster-wide hardware. If exact
user GPU access is unknown, keep User Feasibility = UNKNOWN and state what
information is missing, but still evaluate Hardware Fit and Documented
Access (global `compute.md`) for the smallest plausible experiment. Do not
reject a direction, lower S4, or prefer a CPU-only design solely because
user-specific GPU access or queue time is UNKNOWN; record it as a RISK with
the mitigations in the global `compute.md`.

After compute-planner, have research-readiness-advisor CONFIRM its
execution fit, SOTA potential criterion S4 (feasibility), and
short-paper readiness using compute-planner's verdict (DOES NOT FIT
DURATION means execution fit LOW; a weakened S4 means SOTA potential is
re-rated). If the review's required
controls make the project not fit D, the advisor narrows the question
(Step 7 d) rather than dropping the controls or extending D; a CONDITIONAL
whose conditions cannot fit D stays CONDITIONAL (§8 ranking criterion 6). For READY projects, the
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
  Negative-Result Interpretability Review (all six fields, SESOI and
  outcome classification), short-paper readiness, recommended redesign,
  provisional paper draft, and pivot guidance
- prior-work-checker output: prior-work table, traced baseline number,
  novelty search coverage (N1–N5, Q1–Q9), closest prior work and what
  remains untested, gap statement, iteration history, novelty
  classification and the Prior-Work Evidence Report path
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
+ strongest comparable baseline
+ documented limitation/gap
+ one targeted, technically meaningful intervention
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

Prefer the smallest experiment capable of producing a meaningful,
interpretable and technically deep result. Separate the essential
experiments from optional extensions, and schedule only the essential
ones inside D.

research-planner also returns its candidate comparison matrix (planner
Step 8b), which feeds Step 5b.

---

### Step 5b: Pre-implementation prior-work, novelty and SOTA evidence gate (mandatory)

**When it runs.** After the research question and candidates have been
formulated, designed and costed (Steps 2–5), and **before** any
implementation, any expensive experiment, or any hand-off to paper-writer
or experiment-runner. It respects the discovery order (Benchmark →
Question → Method). It never runs before the method has been proposed and
checked.

**What it does first.** It triggers prior-work-checker **Stage 3 (final
verification)** for every candidate proposed for GO, and for its backups.
This turns the Evidence Report from DRAFT into FINAL.

**How it checks.** It does not re-judge anything. For each check it reads
the authoritative output and verifies that the output exists, is final,
and passes:

| # | Check | Authoritative source | Passes when |
|---|---|---|---|
| 1 | Literature search sufficiently complete | Evidence Report search log and coverage report | Every source in resource §2a was probed this session and is WORKING or covered by another rung of the fallback ladder (§2a-1, §2a-2); the completeness checklist (§2b) is all DONE; Q1–Q9 and N1–N5 were used; the Stage 3 recency search was done. Hit or query counts never satisfy this check |
| 2 | Closest prior work identified | Evidence Report §4 table and paper ledger | Three closest papers (or fewer, with the reason), every one READ at FULL-TEXT level (§2a-3), bibliographic identity verified; "Remaining uncertainty affecting GO / NO-GO" lists no open item that could flip the classification or the gate |
| 3 | Novelty verdict evidence-supported | Evidence Report | The classification has its six-point explanation; evidence quality is not Unverified; the report is FINAL |
| 4 | Existing novelty PASS requirement satisfied | prior-work-checker gate + archive re-check (Step 2c) | PASS, consistent with the classification → gate mapping; the archive verdict is not STRONG OVERLAP or ALREADY TESTED |
| 5 | Strongest comparable baseline identified | Evidence Report + mature baseline map (benchmark-finder) | Number, source location and access class are recorded; UNMEASURED systems are listed |
| 6 | Expected improvement mechanism credible | Advisor Step 5c items 2–4 | S2 at least PARTIAL, with cause evidence named; for combinations, a complementarity argument |
| 7 | SOTA potential meets the user's threshold | Advisor Step 5c | At least MEDIUM by default; HIGH if the user required it; waived only by an explicit scientific-diagnostic instruction (gate 9) |
| 8 | Technical depth passes | Advisor Step 5d | PASS, including the defensible-contribution test and the multi-signal rule |
| 9 | Benchmark validity passes | benchmark-finder; planner Step 1 | EXACT / DIRECT, SAME-TASK, comparability, and V1–V4 on the final question |
| 10 | Fits four working days (or the user's D) | compute-planner | FITS DURATION at level L |
| 11 | Evaluation supports a meaningful scientific conclusion | Advisor Step 5b; advisor Step 5c item 7; planner Step 8b | Required controls, SESOI and MDE are in the design; the expected effect is at least the MDE (or S3 is rated accordingly); the expected contribution type (A–D) is supported by its evidence |
| 12 | Mechanism and domain validity (gate 12) | Advisor Step 5c item 8 (shared definitions §9) | Q1–Q10 answered with sources; verdict PASS, or PASS-EXPLORATORY with all four §9c conditions; E-level consistent with S2; the Q9 discriminating experiment is in the MVRD; claims scoped to the Q10 problem classes |
| 13 | Literature review complete beyond a list | Evidence Report (resource §2d, §4a, §5a) | Eight-field literature map present, including evidence against the hypothesis and potentially overlooked work; closest papers read to pass 2, strongest baseline and closest paper to pass 3; novelty type assigned; the targeted performance-claim level (§4f) is consistent with the baseline trace |

**Outcome.**
- **All 13 pass:** the candidate may be GO. The only permitted condition
  is unconfirmed compute allocation.
- **Any check fails:** the candidate is **not GO**. A positive readiness
  rating, high novelty strength, or a favourable matrix row never
  overrides a failed check. Route the candidate by the check that
  failed:
  - checks 1–5 → prior-work-checker. Resolve it in Stage 3 if possible;
    otherwise FAIL, then benchmark-finder regeneration (Step 2b loop);
  - checks 6–8, 11 and 12 → research-readiness-advisor redesign (advisor
    Step 7; shared definitions §6);
  - check 13 → prior-work-checker (Stage 2/3 completion);
  - check 9 → benchmark-finder;
  - check 10 → the planner Step 6 redesign sequence.

  Every redesign re-enters the normal flow (Steps 2a–5) and comes back to
  this gate.
- **Redesign cannot resolve it:** the candidate is NO-GO. The slot follows
  the existing replacement search. If that also fails, the slot is
  UNRESOLVED. Never force a GO, and never pad (Cardinality Rule).

**Budget.** Stage 3 verification is part of the planning budget. It is
run only for GO candidates and backups (see the early kill check). The
human reading that verifying the Evidence Report needs during the project
counts in compute-planner's "Understanding / reading" phase, inside D.

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
   FULL workflow (compute-planner; shared definitions §5):
   - expected active work plus contingency is at most D;
   - the conservative work bound is at most D;
   - the critical-path wall-clock is at most D;
   - every line is labelled VERIFIED, ESTIMATE or RISK;
   - no setup from another planned project is counted.

   Projects that did not fit were redesigned in this order, never kept as
   "risky" and never fitted by extending D:
   - the scope levers: narrow to the documented failure slice → reuse
     code → reuse models, outputs or activations → cut optional scope →
     smaller intervention that keeps the mechanism → better benchmark or
     setting;
   - then a smaller reformulated question;
   - then replacement by an actively searched, different
     benchmark-centered question.

   Every replacement passed every mandatory gate.
3b. Every project in the final portfolio passes technical depth (§3) and
   has a credible SOTA path (pre-experiment SOTA potential of at least
   MEDIUM, or HIGH if the user required it), unless the user waived that
   gate. Every SOTA statement names the task, slice, baseline, metric and
   access class, and a slice result is never presented as overall SOTA.
4. Feasible projects are ordered Project 1 ... strictly from
   easiest/fastest to hardest/slowest for a researcher at level L (not a
   generic researcher), only after all slots were evaluated, each with its
   schedule window of length D.

The pipeline must actively try to return N valid projects, but it never
pads: a slot that fails any gate is reported as NO-GO or UNRESOLVED,
never as a conditional GO (except for unconfirmed compute allocation).
Replacement search obeys the anti-fixation rules (§1b): no second slot on
the same benchmark or subfield, and no previously explored direction
without new evidence. A slot is never
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
compute-planner).
- The level changes the estimate through learning overhead for genuinely
  unfamiliar tools, sized from verified documentation.
- The level never decides eligibility. Beginner describes experience, not
  the technical ceiling (shared definitions §2).
- A project that would fit for a more experienced researcher but not at
  level L is DOES NOT FIT DURATION for this run.
- Never shrink an estimate to make a project fit, and never inflate one
  by stacking pessimistic assumptions.

A project FITS DURATION (shared definitions §5) when all three hold:
- its STANDALONE total budget (expected active work for the complete
  workflow at level L, plus a separately stated contingency sized to the
  one or two most likely risks) is at most D;
- its conservative work bound is at most D;
- its critical-path wall-clock is at most D.

Further rules:
- Contingency is never counted as planned work.
- Estimates use five buckets: essential implementation, compute (active
  vs wall-clock), evaluation and statistics, paper writing, contingency.
  Every line is labelled VERIFIED, ESTIMATE or RISK.
- A speculative failure is a RISK with a mitigation, not added work.
- Verified existing assets (public code, released models, outputs or
  activations; the user's verified local environment, caches or compute
  allocation) count toward the standalone estimate. Setup from another
  *planned* project never makes a project fit.
- D is in working days (1 week = 5 working days unless the user states
  otherwise). The user's current standard sprint is D = 4 working days:
  expected work of about 3–3.5 days plus 0.5–1 day of contingency.
- Paper writing is AI-drafted; budget about 0.5 day of human review and
  verification (shared definitions §5), not human drafting. The time
  freed goes to the diagnostic, controls and pre-mortem experiment
  (§4e).
- Estimates are realistic, project-specific, and rounded to 0.25 or
  0.5 day. compute-planner holds the detailed phase rules.

Per-project feasibility is estimated by compute-planner (Step 6 of that
skill) and enforced by research-planner (its Step 6). Do not re-estimate it
here. Short GPU runtime never implies that a project fits D.

If the user also gives an overall time budget shorter than N × D, report
the conflict instead of shortening D.

Prefer the smallest **scope** that still delivers a technically
meaningful contribution and fits comfortably within D. Before concluding
DOES NOT FIT, apply the scope levers (shared definitions §6). If a design
still does not fit, report the minimum verified additional time or
resource rather than generic advice to extend D.

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

Discovery record (shared definitions §1a; the order must be visible):
1. Benchmark: (with its mature baseline map and its documented failures
   and open questions)
2. Research question + causal hypothesis: (written before the method;
   which documented failure it comes from)
3. Method: (how it tests that hypothesis)

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
- Novelty classification: NOVEL / PARTIAL OVERLAP (from the Evidence
  Report; ALREADY STUDIED and UNCERTAIN never reach the final report as GO)
- Prior-Work Evidence Report: `prior_work_evidence_<run-tag>_<RQk>.md`
  (FINAL; evidence quality)
- Expected contribution type: A / B / C / D, with its supporting evidence
  (research-planner Step 8b)
- Novelty type: NT-A / NT-B / NT-C / NT-D (resource §5a)
- Pre-implementation evidence gate (Step 5b): 13/13 PASS, or the failed
  check and its routing

Mechanism and domain validity (gate 12, shared definitions §9):
- Verdict and evidence level (E0–E3):
- Q1 problem / Q2 evidence / Q3 causal chain:
- Q4 assumptions → Q5 validity on this benchmark:
- Q6 failure conditions / Q7 alternative explanations:
- Q8 simplest equivalent method → Q9 discriminating experiment:
- Q10 generalization / claim scope:
- Targeted performance-claim level (§4f):

Do not reproduce the full prior-work inventory, search log, or benchmark
history in the main report.

Strongest comparable baseline:
(Name, number, source, task, slice, metric, access class; also the
strongest method on the benchmark overall.)

Documented weakness of that baseline:
(Failure category, subset or error mode, with its source.)

Proposed method/change:
(The mechanism, and why it targets the cause of the documented weakness.)

Technical depth:
(PASS, with a one- or two-sentence depth case: the mechanism or
hypothesis, and the insight a positive or negative result gives.)

Defensible contribution (shared definitions §4e):
- Finding if positive:
- Finding if negative:
- Predictability test: (would an expert predict the outcome? If success
  is predictable, explain why the negative outcome is informative, or
  the depth gate fails)
- Reviewer pre-mortem: (the most likely rejection reason, and the
  experiment inside D that answers it)

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

Topic ranking (advisor Step 5c, confirmed; criteria and numbering from
shared definitions §8; S1–S4 from §4b):
- Pre-experiment SOTA potential (§8 criterion 1): HIGH / MEDIUM / LOW /
  UNKNOWN.
  Rate each criterion STRONG / PARTIAL / WEAK / UNVERIFIED, with its
  evidence:
  - S1 documented weakness and headroom (baseline number, sourced, with
    its table/figure). Include the **baseline-maturity audit**: systems
    released after the benchmark, and which are UNMEASURED (§4d.1–2).
  - S2 mechanism targeting the weakness. Give the **cause evidence**
    (diagnostic or error analysis) and the lever evidence separately
    (§4d.3).
  - S3 fair, reproducible test. Give the **expected effect size, its
    basis, and the MDE** (§4d.5).
  - S4 feasible MVRD.
  - Calibration note: any similar past design and its measured outcome
    (§4d.6).

  HIGH only if all four are STRONG on facts verified now; there is no
  conditional HIGH. This is never a claim of achieved SOTA; that is
  classified only after the experiment (§4c).
- Four-day feasibility margin (§8 criterion 2).
- Benchmark and evaluation strength (§8 criterion 3): public benchmark,
  reproducible baselines, reliable evaluation.
- Clear, measurable contribution and technical depth (§8 criterion 4):
  PASS (gate), the significance of the finding, and the contribution
  type A–D (research-planner Step 8b).
- Novelty strength (§8 criterion 5): HIGH / MEDIUM / LOW. Modest is
  acceptable.
- Negative-result readiness (§8 criterion 6): see the review table
  below.
- Original-question preservation (§8 criterion 7, tie-breaker).

Negative-Result Interpretability Review (from research-readiness-advisor
Step 5b, confirmed):

| Field | Result |
|---|---|
| Positive-result contribution | What a successful result would establish |
| Negative-result contribution | What a sufficiently precise negative result would establish |
| Inconclusive-result risk | Why the experiment might fail to support either conclusion |
| Independent scientific value | Findings beyond benchmark improvement |
| Required controls | Minimum controls (incl. SESOI and power / MDE check) needed for interpretation |
| Negative-result readiness (§8 criterion 6) | PASS / CONDITIONAL (conditions adopted) / FAIL (performance-dependent) |

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
- Writing/revision time: (AI-drafted paper; human review and verification
  only, about 0.5 day at Beginner; if writing-first, the split of the
  same budget)
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

Minimum Result Worth Writing Up:

What a negative result would mean:
(Consistent with the review above; distinguish a meaningful negative from
an inconclusive result.)

Main Risk:

Recommended Scope:

---

### Project Schedule

| Project | Schedule Window | Slot (RQk) | Final Research Question | Preserved / Modified / Replaced / Generated / UNRESOLVED | Exact Benchmark | Baseline | Metric | Validity (V1–V4) | Collision Verdict | Gap | Prior-Work Archive | Proposed Change | SOTA Potential | Novelty Strength | Negative-Result Readiness | Short-Paper Readiness | Preservation | Experience Level | Standalone Expected Work | Conservative Work Range | Contingency | Total Budget Required | Execution Risk | Duration Feasibility (standalone, vs. D, at L) | Hardware Fit | User Compute Feasibility |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

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
alternatives, using the topic-ranking order (shared definitions §8):
1. SOTA potential;
2. feasibility margin;
3. benchmark and evaluation strength;
4. defensible contribution and technical depth (credible A/B above C/D);
5. novelty strength;
6. negative-result readiness;
7. preservation.

Include research-planner's candidate comparison matrix. The
recommendation does not change the project order. Only candidates that
passed the Step 5b evidence gate may be recommended as GO.

For the selected primary project and each backup, explain:
- the technical contribution;
- the strongest baseline;
- the documented performance gap;
- the proposed mechanism and why it could improve performance;
- SOTA potential (S1–S4);
- the D-day execution plan, with VERIFIED / ESTIMATE / RISK labels and
  the five buckets;
- the risks with their mitigations.

If no project qualifies after genuine redesign attempts, report NO
SUITABLE TOPIC FOUND. Name the remaining unavoidable constraints and the
minimum verified change (time, compute or scope) that would make the best
design qualify. Do not simply recommend extending D or lowering the
standards.

Do not recommend a direction solely because it appears novel.
