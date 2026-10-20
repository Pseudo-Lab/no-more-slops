---
name: research-readiness-advisor
description: Act as a proactive research advisor and designer. For each benchmark-backed candidate, diagnose the strongest comparable baseline's documented weaknesses, design and scope a technically meaningful intervention, and judge whether it is a good project for this user to execute and turn into a short paper within their duration and experience level. Rates benchmark fit, execution fit, technical depth, original-question preservation, pre-experiment SOTA potential (S1–S4) and novelty strength, negative-result interpretability (PASS / CONDITIONAL / FAIL), and short-paper readiness. Must attempt at least one meaningful redesign before rejecting a candidate, and writes a full provisional pre-experiment paper draft (results TBD) for ready projects.
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

0. `~/.claude/skills/research-pipeline/references/research_design_principles.md`.
   It holds the shared definitions of:
   - Beginner
   - technical depth
   - SOTA potential (pre-experiment) vs SOTA achievement (post-experiment)
   - D-day feasibility
   - research redesign
   - the mandatory gates

   When this skill's wording differs, that file wins, but no gate is ever
   weakened.
1. `references/mentorship_principles.md` (this skill's directory): the
   primary source for the criteria below.
2. `~/.claude/skills/benchmark-finder/references/research_advice.md`.
3. [prior_work_novelty_sota_review.md](../prior-work-checker/references/prior_work_novelty_sota_review.md)
   (owned by prior-work-checker). It defines the Prior-Work Evidence
   Report this skill consumes (§7) and how each field is used (§8).
   - The advisor reads the report.
   - It never re-runs the literature review.
   - It never re-classifies novelty.
   - It never issues a novelty verdict that conflicts with
     prior-work-checker's classification and gate.

Role: design, not only filter. Follow Discover → Diagnose → Design →
Scope → Evaluate → Refine → Select (shared definitions §1).

For every promising candidate:
1. Identify the strongest comparable baseline.
2. Diagnose its documented weaknesses.
3. Design an intervention that targets them.
4. Scope a minimal viable research design (MVRD).

"Beginner" never excludes GPU, fine-tuning, activation analysis,
mechanistic interpretability or white-box work; it only affects the
estimate (§2). GPU designs, including single-GPU 7B–8B experiments, are
considered by default; unverified GPU allocation is a RISK with a
mitigation, not a reason to prefer a CPU-only or API-only design.

Both are mentorship guidance, not scientific evidence. Where
`research_advice.md` says a topic may be discarded for a more feasible
benchmark, apply it in this skill's sense: discard only when no
sufficiently aligned, feasible, benchmark-backed version of the original
question exists (see Preservation).

## Input

For each candidate (per slot RQk):

- Original research question (and seed direction, if any)
- Candidate research question and benchmark from benchmark-finder,
  including verification fields, validity V1–V4, Benchmark Readiness, and
  the evaluation-set size and typical conditions/seeds (used by Step 5b)
- prior-work-checker result, when available, including its Prior-Work
  Evidence Report (`prior_work_evidence_<run-tag>_<RQk>.md`). The report
  supplies:
  - the novelty classification and gate;
  - the three closest prior works;
  - the combination analysis;
  - the strongest published baseline;
  - its known failure modes;
  - the open gap;
  - evidence quality, with DRAFT / FINAL status.
- compute-planner result, when available
- User's goal (e.g. paper-writing practice), per-project duration D, and
  experience level L

## Workflow

### Step 1: Benchmark fit (HIGH / MEDIUM / LOW)

How well the benchmark represents the research question. Base it on
benchmark-finder's SAME-TASK, comparability, and validity (V1–V4) answers
and the benchmark-selection guidance: established task, clear metric,
published baseline numbers, public data and code, traceable literature,
a strongest baseline with documented weaknesses, and room for a targeted,
technically meaningful intervention. A benchmark is never rated HIGH
merely because it is easy.

### Step 2: Execution fit (HIGH / MEDIUM / LOW)

How feasible the scoped design (MVRD) is for the user's duration D,
experience level L, and compute. Before compute-planner has run, give a
PRELIMINARY execution fit from:
- Benchmark Readiness (released outputs, predictions, models, adapters
  and activations; reproduction path; compute burden; experience-sensitive
  factors);
- D and L;
- the reuse actually verified in the repository.

Rate the scoped design, not the full benchmark programme. An
experience-sensitive factor (GPU, 24–70B models, activation hooks) lowers
execution fit only when the verified tooling does not cover it.
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

Preservation is the final tie-breaker among candidates that pass every
hard gate. It is the last criterion (7) of the topic-ranking order
(Step 5c; shared definitions §8). If the
original question is too broad, first try to keep its
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

### Step 5b: Negative-Result Interpretability Review (mandatory)

Purpose: prefer research questions that yield a meaningful scientific
finding even if the proposed method does not significantly beat the
baseline. This matters most for short projects with little time and
compute. It is a preference for interpretable outcomes, NOT a ban on
performance-improvement studies.

Scope boundary (to avoid duplicate checks):

- benchmark-finder's V3 already decides whether a positive and a negative
  benchmark result would each be *evidence about the question* (benchmark
  and question alignment). Take V3 as an input; do not re-judge it. If V3
  is NO, the pair goes back to benchmark-finder, not to this review.
- Novelty is decided by prior-work-checker and the prior-work archive.
  Item 6 below only reads their evidence; it never claims novelty itself.
- compute-planner decides whether any added control or seed fits D.

Answer each item with a one-line justification:

1. Positive outcome: what new scientific knowledge (not only a higher
   score) would a positive result provide?
2. Negative outcome: what specific, defensible conclusion could be stated
   if the hypothesis is not confirmed, *given that the result is
   sufficiently precise* (item 4)?
3. Independent contribution: can the study examine the underlying
   phenomenon or mechanism independently of whether performance improves
   (e.g. a manipulation check or a diagnostic sub-analysis on the same
   benchmark)?
4. Statistical interpretability: can the planned evaluation-set size,
   number of seeds/runs, and paired test distinguish a meaningful negative
   result from an inconclusive one? State:
   - the smallest effect of interest (SESOI) on the benchmark metric,
     justified (e.g. by the gaps between published methods or by a
     practically relevant difference);
   - an approximate minimum detectable effect, or the expected confidence
     interval width, from the evaluation-set size, seeds, and any
     published variance. If no variance estimate exists, mark it UNKNOWN
     and require a pilot-based check (CONDITIONAL), never a guessed number;
   - whether the design can bound the effect below the SESOI (e.g. a CI
     or equivalence test against ±SESOI), which is what a meaningful
     negative result needs.
5. Failure analysis: are there controls or diagnostics that can tell apart
   the plausible explanations for an unsuccessful intervention? At
   minimum consider: implementation did not take effect (manipulation or
   sanity check), baseline mis-reproduced, ceiling/floor effect, phenomenon
   absent, phenomenon present but not exploitable by this method.
6. Prior-work novelty: using prior-work-checker / archive evidence, would
   the positive OR the negative finding add knowledge beyond existing work
   (e.g. a negative result that is already known adds little)? Before the
   archive exists, mark this PRELIMINARY.
   - Read the answer from the Evidence Report's "Open research gap",
     "Closest prior work" and "Known failure modes".
   - A negative result counts as new knowledge only when the report shows
     the question is not already substantially answered, and no traced
     work has reported the same null.

Classify each possible outcome explicitly; never merge them:

- Meaningful positive finding: the effect is in the predicted direction,
  statistically supported, at least the SESOI, and the controls rule out
  the main artefact explanations.
- Meaningful negative finding: the CI (or equivalence test) excludes
  effects of at least the SESOI, the manipulation check shows the
  intervention took effect, and the baseline was reproduced.
- Inconclusive finding: anything else, in particular a non-significant
  result whose CI still includes the SESOI, or a failure the controls
  cannot attribute. A non-significant result alone never shows that no
  effect exists.

A negative result is never called publishable or a contribution unless
item 4 (precision) and item 6 (novelty) both support it.

Preferred question structure (where feasible, without adding scope):

- Phenomenon: does the underlying phenomenon exist?
- Method: can it be used to improve performance?
- Limits: under what conditions does it (or the method) fail?

The final research question stays the single Method question required by
research-pipeline's Research Question Format Rule. For short projects,
Phenomenon and Limits are covered by ONE minimal diagnostic analysis
(e.g. a manipulation check, or one split by a condition the benchmark
already annotates). They are never separate experiments and never the main
contribution. Do not invent extra research questions to satisfy this
structure.

Verdict (Negative-result readiness):

- PASS: both positive and negative outcomes can support meaningful,
  testable conclusions (items 1–6 are satisfied, item 6 at least
  PRELIMINARY).
- CONDITIONAL: interpretable once a specific, minimal addition is made:
  a named control or manipulation check, a power / MDE check (possibly via
  pilot), more seeds, or a narrower question. List each condition.
- FAIL: the study depends almost entirely on achieving a performance
  improvement, and an unsuccessful result would remain scientifically
  inconclusive.

For CONDITIONAL or FAIL, always propose a minimal redesign (Step 7) before
any rejection. Conditions must be the smallest that fix the problem and
must still fit D: any added control, seed, or run is passed to
compute-planner. If the conditions would break D, prefer narrowing the
question over adding experiments.

Effect on approval (applied in Step 6):

The review itself is mandatory: a candidate cannot be READY until it has
been completed and, for CONDITIONAL or FAIL, a minimal redesign (Step 7
a–d) has been attempted. The resulting rating is the SIXTH topic-ranking
criterion (Step 5c; shared definitions §8, criterion 6), not a gate:

- PASS: no restriction.
- CONDITIONAL: write the conditions into the design (main experiment,
  controls, statistical test) when they fit D, then re-rate (usually PASS).
  compute-planner confirms the design, conditions included, still fits D.
  If they cannot fit D, keep the rating CONDITIONAL and state why.
- FAIL (after the minimal redesign attempt): the candidate stays eligible
  and is labeled "Negative-result readiness: FAIL (performance-dependent)",
  with its inconclusive-result risk stated as a Main Risk. This rating
  decides between candidates only when they are comparable on every
  higher criterion of the shared ranking order (shared definitions §8:
  SOTA potential, feasibility margin, benchmark and evaluation strength,
  defensible contribution and depth, novelty strength). Never replace a
  direction only to improve this rating when a minimal redesign could fix
  it.

### Step 5c: Topic-ranking ratings (SOTA potential and novelty strength)

Mandatory gates are the full list in shared definitions §7. They are
never traded off against the ranking criteria:
- exact benchmark with SAME-TASK, comparability and validity V1–V4
  (benchmark-finder);
- no data leakage;
- fair baseline comparison;
- minimum novelty = prior-work-checker PASS;
- reproducibility;
- statistical rigor (a completed Step 5b review);
- research integrity;
- technical depth PASS (Step 5d);
- a credible SOTA path, meaning SOTA potential of at least MEDIUM
  (unless the user raised the bar to HIGH or waived it for an explicitly
  scientific-diagnostic goal);
- FITS DURATION (compute-planner).

Among candidates that pass every gate, rank in this order:

1. **Credible SOTA potential (PRIMARY):** an evidence-supported
   opportunity to outperform the strongest *existing* baseline (after the
   baseline-maturity audit) on the named task and metric. HIGH ranks above
   MEDIUM. Within a rating, rank by the strength of the S2 *cause*
   evidence, then by expected margin relative to the MDE (shared
   definitions §4d).
2. **Four-day feasibility margin, given the user's skills:** contingency
   left in D, critical-path slack, share of requirements VERIFIED
   (Execution fit).
3. **Benchmark and evaluation strength:** a public benchmark;
   reproducible baselines (released code, models or per-item outputs);
   reliable evaluation (automatic metric, adequate test size and power,
   low label noise, no contamination). Read this from Benchmark fit
   (Step 1) and benchmark-finder's Benchmark Readiness.
4. **Clear, measurable contribution and technical depth** (Step 5d,
   shared definitions §4e): a non-obvious finding in at least one
   outcome, and the strength of the reviewer pre-mortem answer.
5. **Novelty strength:** how much the contribution adds beyond prior
   work, mapped from prior-work-checker's Evidence Report and the archive
   evidence (the mapping table below). Modest novelty is acceptable when
   1–4 are strong. The advisor rates strength only; it never decides or
   claims novelty.
6. **Negative-result readiness** (Step 5b).
7. **Original-question preservation** (final tie-breaker; Step 3).

This list is the shared ranking order in shared definitions §8, with the
same criteria, numbers and order. If the two ever differ, §8 wins. Topic
area, AI safety or not, is never a criterion.

Each criterion is applied only when the candidates are comparable on all
higher ones. In particular, never rank a highly novel topic with weak SOTA
potential above a gate-passing topic with a credible path to SOTA.

Rate **pre-experiment** SOTA potential with the S1–S4 definitions in
shared definitions §4b. First identify the strongest comparable baseline
(§4a): same task, slice, metric, protocol and access class. Also name the
strongest method on the benchmark overall. Each criterion gets its
evidence and a strength (STRONG / PARTIAL / WEAK / UNVERIFIED):

- **S1. Documented weakness and headroom.**
  - The baseline's verified number on the named task and metric (with
    its source).
  - A documented weakness: a failure category, subset, error mode or
    stated limitation, taken from the paper, released results or released
    per-item outputs.
  - Realistic room to improve: not near ceiling or a label-noise bound,
    and not closable only by scale.
- **S2. Mechanism targets the weakness.**
  - The intervention addresses the cause of the documented weakness.
  - There is a technically credible reason to expect improvement: either
    evidence from a closely related setting, or a principled argument a
    reviewer would accept (for example, information the baseline provably
    lacks, an objective mismatch, a documented inductive-bias failure).
  - No experimental proof on this benchmark is required. Speculation or
    "should help in principle" is WEAK.
- **S3. Fair, reproducible test.**
  - Same task, slice, metric and protocol.
  - The baseline number is released, reproducible, or recomputable from
    released outputs.
  - Resources are comparable, or the difference is declared.
  - Leakage is controlled.
- **S4. Feasible MVRD.** The scoped design fits D at level L under the
  verified-requirements estimate (§5). Compute is confirmed or has a
  concrete mitigation. This is preliminary before compute-planner;
  compute-planner is authoritative.
  - Compute comes only from the global
    `~/.claude/skills/compute-planner/references/compute.md` (§4b note).
    A DOCUMENTED-AVAILABLE GPU with a named day-0 test job, an
    alternative partition or GPU type, and a pre-download or fallback
    model is STRONG. Unverified allocation or UNKNOWN queue time alone
    never lowers S4 below STRONG and is never UNAVAILABLE.

**Evidence rules (shared definitions §4d; mandatory, stricter than the
criteria above):**
- **Discovery order check (§1a).**
  - Confirm the record shows Benchmark → Research Question + causal
    hypothesis → Method.
  - A method-first candidate is returned to the question step before
    rating.
- **S1 after the baseline-maturity audit.**
  - S1 cannot be STRONG while a plausibly stronger released system
    (published after the benchmark, or a standard method class the
    baseline set omits) is UNMEASURED on the benchmark. Such S1 is
    PARTIAL.
  - If the headroom exists only because the baseline set omits a
    standard method class, S1 is WEAK.
  - Author-only baselines on an IMMATURE benchmark cap S1 at PARTIAL
    until the audit is complete.
  - A poor baseline number is never by itself evidence of SOTA potential.
- **S2 needs cause evidence.**
  - Record separately: *cause evidence* (a documented diagnostic,
    ablation, error analysis or per-item output showing the baseline
    fails because of the factor the method changes) and *lever evidence*
    (the same kind of method helped elsewhere).
  - Lever evidence alone gives at most PARTIAL.
  - STRONG needs cause evidence plus closely related lever evidence, or a
    principled argument that the method uses information the baseline
    provably lacks.
- **Expected margin.**
  - State the expected effect size, the measured result it extrapolates
    from, and the planned test's MDE.
  - If the expected effect is below the MDE or the SESOI, S3 is at most
    PARTIAL.
- **No conditional HIGH.**
  - HIGH requires all four criteria STRONG on facts verified now.
  - "HIGH if X" is reported as the lower rating, with X named as the
    upgrade condition.
  - Unconfirmed GPU allocation is handled under S4 and is the only
    exception.
- **Calibration.**
  - Check the working directory for past designs with measured outcomes
    (`results_RQ*.md`). Example: v6/RQ4 was rated a credible path; TF-IDF
    then lost to BERT-PE by 2.43 pp.
  - When the current rationale resembles a past miss, state what differs.

Rating rules (§4b, subject to the evidence rules above):

- **HIGH:** all four are STRONG.
- **MEDIUM:** S1 and S3 STRONG, and S2 and S4 at least PARTIAL. This is a
  credible SOTA path.
- **LOW:** S1 or S2 WEAK, or S3 or S4 WEAK.
- **UNKNOWN:** S1 UNVERIFIED.

Further rules:
- Never assign STRONG from speculation alone, and never invent numbers.
- Do not withhold STRONG merely because the improvement is unproven
  before the experiment. Pre-experiment potential is not post-experiment
  achievement (§4c).
- Uncertainty about the outcome is never by itself a reason to reject.
- Before the prior-work archive exists, the rating is PRELIMINARY. If
  compute-planner's estimate weakens S4, re-rate.
- If S4 is the only criterion below STRONG, apply the §6 redesign levers
  before accepting MEDIUM or LOW.
- Every SOTA statement names the task, slice, baseline, metric and model
  or access class. A slice result is never presented as overall SOTA.

#### Consuming the Prior-Work Evidence Report (mandatory input to S1–S4 and novelty strength)

Take every literature fact from prior-work-checker's Evidence Report and
benchmark-finder's mature baseline map. Do not re-search. If a fact you
need is missing, return the slot to prior-work-checker; do not fill the
gap yourself. If the report is still DRAFT, every rating stays
PRELIMINARY.

Assess, and record each item in the Output:

1. **Novelty strength.** Map it from the report's classification and gate
   using resource §8:

   | Classification and gate | Novelty strength |
   |---|---|
   | NOVEL + PASS, evidence Verified | HIGH |
   | PARTIAL OVERLAP + PASS with a narrow, defensible gap, or NOVEL with Partial evidence | MEDIUM |
   | PARTIAL OVERLAP + PASS whose gap is only a new benchmark or setting, or a new combination of known methods | LOW |
   | ALREADY STUDIED / UNCERTAIN | Not rated: gate 4 has failed |

   Archive verdicts translate via resource §6 (NO EVIDENCE FOUND or
   PARTIAL OVERLAP → as classified; STRONG OVERLAP or ALREADY TESTED →
   gate failed). Never raise novelty strength above what the
   classification supports, and never use it to raise SOTA potential.
2. **The strongest baseline's documented weaknesses (S1).** Use the
   report's "Strongest published baseline" and "Known failure modes",
   after the maturity audit. A weakness without a source is not
   documented.
3. **Does the mechanism address those weaknesses (S2)?** Name the
   specific failure mode the mechanism targets and the cause evidence for
   it. Report cause evidence and lever evidence separately (§4d.3).
4. **Complementary or redundant signals (S2, depth).** For any method
   that combines several signals or components, use the report's
   combination analysis:
   - Are the components' documented failure causes different
     (complementary)?
   - Is there published redundancy evidence?

   A combination of existing signals is **never** sufficient for S2 by
   itself. S2 above WEAK needs a credible complementarity argument plus
   the baseline failure mode it addresses. Redundancy evidence caps S2 at
   PARTIAL until the design includes a complementarity diagnostic (shared
   definitions §4d.3).
5. **Is a positive result a meaningful contribution?** It must exceed
   what the closest prior work already shows (Step 5d "finding if
   positive").
6. **Is a negative result new knowledge?** See Step 5b item 6.
7. **Is the expected improvement detectable?** State the expected effect
   size, the basis it extrapolates from (a number in the report or the
   archive), and the planned test's MDE. If the expected effect is below
   the MDE or the SESOI, S3 is at most PARTIAL (§4d.5).

By default, a credible SOTA path (at least MEDIUM) is a mandatory gate
(shared definitions §7, gate 9). Scientific-diagnostic
(phenomenon-oriented) candidates are eligible only when the user waives
that gate for an explicitly scientific-diagnostic goal. They are then
ranked by the same order.

### Step 5d: Technical depth (mandatory gate)

Apply shared definitions §3. State the depth case in one or two
sentences:
- the mechanism or hypothesis;
- the scientific insight that a positive result gives;
- the scientific insight that a negative result gives.

- **PASS:** the core contribution is a mechanism, a new signal or
  objective, a principled use of information the baseline lacks, or a
  test of a mechanistic hypothesis.
- **FAIL:** the entire contribution is one of:
  - a fixed threshold on existing scores;
  - simple voting;
  - weighted or unweighted averaging;
  - hyperparameter tuning;
  - re-running an existing method;
  - a recombination of existing outputs with no new signal;
  - a standard engineering lever with no falsifiable causal hypothesis
    about the baseline's failure. Such levers include:
    - more, other or distribution-matched training data, or standard
      augmentation and hard-negative mining;
    - a larger or different backbone;
    - standard fine-tuning, LoRA or distillation;
    - swapping a probe for a fine-tuned head;
    - prompt engineering or more inference compute;
    - re-applying a published recipe to a new benchmark.

    "New training signal" or "new setting" alone is not sufficient.

  Such components are allowed inside a project whose core contribution
  passes. Judge depth by the significance of the mechanism and insight,
  not by implementation size.
- **Multi-signal methods.** Simple voting, thresholding, averaging, or
  unprincipled recombination of existing signals is never, by itself, a
  meaningful methodological contribution. A combination PASSES only when
  all of these hold:
  - at least one component is a new signal, or the combination rule
    encodes a stated mechanism (for example, evidence-type precedence
    justified by the components' different failure causes);
  - there is a complementarity hypothesis, taken from the Evidence
    Report's combination analysis;
  - the design includes a diagnostic that could falsify that hypothesis,
    such as a per-item cross-tabulation of which component catches which
    failure.
- **Defensible-contribution test (shared definitions §4e), mandatory for
  PASS.** Record one sentence each:
  - **Finding if positive.**
  - **Finding if negative.**
  - **Predictability test.** Would an expert, shown only the design,
    confidently predict the outcome?
    - If success is predictable, the project is confirmatory
      engineering. It FAILS unless a surprising negative outcome would be
      informative and the design can detect it.
    - If failure is predictable, S2 is WEAK.
  - **Reviewer pre-mortem.** The single most likely rejection reason,
    plus the experiment inside D that answers it. That experiment is
    ESSENTIAL.
- On FAIL, attempt a depth-restoring redesign (Step 7) before rejecting.
  The redesign must change the *research question or causal
  hypothesis*, not only the lever.

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
  (unless that is the explicit goal), a main table plus an
  ablation/control are possible, and the Step 5b review has been
  completed with any minimal redesign attempted (its rating ranks
  candidates; it does not block READY). In addition, technical depth
  (Step 5d) is PASS, and SOTA potential meets the credible-SOTA-path gate
  (Step 5c), unless the user waived that gate.
- NEEDS REDESIGN: the core mechanism is worth keeping but one or more items
  fail and a benchmark-centered redesign could fix them.
- NOT READY: no plausible benchmark-centered redesign of this candidate
  would fix it. This verdict is allowed only after at least one
  meaningful redesign attempt (Step 7) has been recorded and evaluated.

### Step 7: Active redesign (mandatory before any rejection)

Before any candidate is rated NOT READY or rejected (for feasibility,
technical depth, or SOTA potential), attempt **at least one meaningful
redesign** and re-evaluate it.

**Redesign levers** (shared definitions §6), in this order:

1. Narrow the question to the documented failure category or subset. The
   slice must be pre-specified and justified by the diagnosed weakness.
2. Reuse published implementations, configs and evaluation scripts.
3. Reuse pretrained or fine-tuned models, adapters, released outputs,
   cached activations and intermediate results.
4. Remove scope the main claim does not need, separating essential
   experiments from optional extensions.
5. Design a smaller intervention that keeps the mechanism.
6. Choose a more appropriate benchmark or evaluation setting.

Each redesign must still pass technical depth (Step 5d) and must never
weaken a mandatory gate. Record every attempt in a "Refinement history"
field: lever used, what changed, and the re-evaluated ratings.

Then, only if no lever yields an acceptable design, propose in order:

1. a benchmark-centered redesign that preserves the original research
   mechanism (same mechanism, established benchmark task and metric,
   published baseline, one isolated intervention);
2. a different established benchmark for the same mechanism;
3. only if neither yields a sufficiently aligned, feasible version:
   replacement of the direction.

Do not answer with "extend D" or "lower the standard" until the levers
have been tried. If a design still fails, state the remaining unavoidable
constraint and the minimum verified change that would resolve it.

When the problem is negative-result readiness (Step 5b CONDITIONAL or
FAIL), try these minimal fixes first, inside option 1 and in this order,
keeping the same benchmark, baseline, metric, and single change:

a. add a manipulation check or sanity control showing the change took
   effect;
b. state the SESOI and add a power / MDE check (via pilot if variance is
   unknown), adding seeds only if that fits D;
c. add one diagnostic sub-analysis on an existing benchmark split or
   annotation (the Phenomenon / Limits element of Step 5b);
d. narrow the question to the sub-setting where a precise result is
   achievable.

Any redesign or replacement goes back through benchmark-finder's
validation, prior-work-checker, and compute-planner before it can be
accepted.

### Step 7b: Archive re-evaluation (research-pipeline Step 2c)

After benchmark-finder has built the benchmark-centered prior-work archive
for a provisionally confirmed benchmark and the overlap has been re-checked,
re-run the evaluation using the archive evidence (inventory, benchmark
history, baseline map, closest prior work, collision verdict, open gap)
and the updated Prior-Work Evidence Report.
- Where the archive verdict and the report disagree, use the stricter
  one (resource §6).
- Removing PRELIMINARY from SOTA potential and novelty strength requires
  the report to be FINAL (Stage 3).
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
- SOTA potential and Novelty strength (Step 5c): re-rate with the
  archive's baseline map, benchmark history (current best result),
  collision verdict, and gap, removing PRELIMINARY
- Negative-result readiness (Step 5b): confirm item 6 (prior-work
  novelty of both the positive and the negative finding) against the
  archive, removing PRELIMINARY, and re-check items 1–5 if the baseline or
  question changed
- Short-paper readiness

Report each as in the Output table, plus "Baseline choice" and "Remaining
contribution" with a one-line justification each, and state what changed
from the earlier evaluation. READY (which includes the Step 5b condition)
lets the pipeline mark the benchmark FINAL CONFIRMED; NEEDS REDESIGN or NOT
READY returns the slot to redesign (Step 7).

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
Classify the outcome with Step 5b's categories (meaningful positive /
meaningful negative / inconclusive) using the pre-specified SESOI and
controls. Report an inconclusive result as inconclusive; never present a
non-significant result as evidence of no effect.

Classify **post-experiment SOTA achievement** separately from the
pre-experiment potential (shared definitions §4c):
- **ACHIEVED:** beats the strongest comparable baseline under the same
  protocol, by at least the SESOI, with the pre-registered statistical
  criterion met.
- **NOT ACHIEVED:** the CI excludes a gain of at least the SESOI, or the
  method is worse.
- **INCONCLUSIVE:** anything else.

Every SOTA claim names the task, slice, baseline, metric and model or
access class. A slice result is never stated as overall SOTA.

The pre-experiment conclusion is a working target for the research
process, not an empirical result that may stay unchanged regardless of
evidence.

#### Writing budget

The paper is drafted primarily by AI. Pre-experiment drafting and
post-experiment result insertion and revision are done by AI
(paper-writer), and they are parts of the SAME writing budget estimated
by compute-planner. That budget covers only human review and
verification, about 0.5 day at Beginner (range 0.5–0.75):
- trace every number to output files;
- check citations against sources;
- check that claims match the evidence and the pre-registered criteria;
- review captions and limitations;
- do a final read.

These are never double-counted, and verification is never cut to make a
project fit. research-planner may revise the draft when finalising the
design.

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
| Strongest comparable baseline | Name, number, source, task, slice, metric, access class; plus the strongest method overall (Step 5c, §4a) |
| Documented weakness | The failure category, subset or error mode, with its source |
| Proposed mechanism | The intervention and why it targets the weakness's cause |
| SOTA potential (pre-experiment; §8 criterion 1) | HIGH / MEDIUM / LOW / UNKNOWN, with S1 documented weakness and headroom, S2 mechanism, S3 fair reproducible test, S4 feasible MVRD, each STRONG / PARTIAL / WEAK / UNVERIFIED (Step 5c, §4b) |
| Technical depth | PASS / FAIL, with the depth case (Step 5d) |
| Refinement history | Each redesign attempt: lever, change, re-evaluated ratings (Step 7) |
| Novelty strength (§8 criterion 5) | HIGH / MEDIUM / LOW, mapped from the Evidence Report's classification and gate (Step 5c); never a novelty verdict of its own |
| Prior-work evidence used | Evidence Report path, DRAFT / FINAL, evidence quality; novelty classification and gate (quoted, not re-judged) |
| Signal complementarity | Multi-component methods only: COMPLEMENTARY (documented different failure causes) / REDUNDANT / UNKNOWN, with sources and the diagnostic that tests it |
| Expected effect vs MDE | Expected effect, its basis, the MDE and the SESOI (Step 5c item 7) |
| Positive-result contribution | What a successful result would establish (Step 5b item 1) |
| Negative-result contribution | What a sufficiently precise negative result would establish (item 2, conditioned on item 4) |
| Inconclusive-result risk | Why the experiment might support neither conclusion (items 4–5) |
| Independent scientific value | Findings beyond benchmark improvement (item 3) |
| Required controls | Minimum controls, SESOI, and power / MDE check needed for interpretation (items 4–5) |
| Negative-result readiness (§8 criterion 6) | PASS / CONDITIONAL (conditions listed) / FAIL (performance-dependent) (PRELIMINARY until archive re-evaluation) |
| Short-paper readiness | READY / NEEDS REDESIGN / NOT READY |
| Main reason | |
| Recommended redesign if needed | |

For READY candidates, append the full provisional paper draft (Step 8).

## Rules

- Never invent papers, baselines, numbers, or URLs.
- Never fabricate experimental results; experimental cells stay TBD until
  actually measured.
- Do not claim novelty; that is prior-work-checker's job.
- Never treat statistical non-significance as evidence of no effect, and
  never call a negative result publishable without supporting precision
  (Step 5b item 4) and novelty (item 6) evidence.
- The Negative-Result Interpretability Review never adds experiments
  beyond the minimal controls it names, and never expands scope beyond D.
- Do not make compute or duration judgments beyond the preliminary
  execution fit; compute-planner is authoritative.
