# Research Design Principles (shared definitions)

Shared by: research-pipeline, research-readiness-advisor, research-planner,
compute-planner, benchmark-finder, prior-work-checker, paper-writer,
experiment-runner, and `research-readiness-advisor/references/mentorship_principles.md`.

When a skill uses one of the terms defined below, it means exactly the
definition here. If a skill's older wording conflicts with this file, this
file wins, except where a mandatory gate (§7) would be weakened. Gates
are never weakened by anything in this file.

This file is planning methodology, not scientific evidence. It never
establishes that a gap exists, a benchmark is established, a method works,
or a result is true.

---

## 1. Role of the pipeline: research designer, not feasibility filter

The pipeline's job is to **design** promising, feasible, technically
meaningful projects. Rejecting weak ideas is only part of that job.
Process every candidate through:

**Discover → Diagnose → Design → Scope → Evaluate → Refine → Select**

| Stage | What happens |
|---|---|
| Discover | Screen at least 10–15 public benchmarks across at least six AI/ML subfields before any shortlist (§1b, §1c). The topic scope is any area of AI/ML; technical AI safety is optional, not required (§1d). Use user-named sources, recent papers, leaderboards and public repositories. Find benchmarks with strong, mature baselines. **Step 1 of §1a.** |
| Diagnose | Identify the strongest existing baseline after the maturity audit (§4a, §4d.1) and its documented weaknesses: failure categories, subsets, error modes, and the authors' own stated limitations. Prefer evidence from released results or per-item outputs. Formulate the research question and the causal hypothesis **before any method**. **Step 2 of §1a.** |
| Design | Propose an intervention that tests the causal hypothesis and directly targets the diagnosed weakness (§3, §4 S2, §4e). **Step 3 of §1a.** |
| Scope | Build the minimal viable research design (MVRD). Use the redesign levers in §6 and separate essential from optional work. |
| Evaluate | Apply the mandatory gates (§7), including the Mechanism and Domain-Validity Gate (§9). Then rate SOTA potential (§4, with the targeted claim level §4f), technical depth (§3) and feasibility (§5). Every estimate is labelled VERIFIED, ESTIMATE or RISK. |
| Refine | If a gate or rating fails, apply at least one meaningful redesign (§6) before rejecting. Re-evaluate after each redesign. |
| Select | Rank the designs that pass every gate (§8) and select. |

Uncertainty about the experimental outcome is **never** a reason to
reject on its own. Only failed gates, after genuine redesign attempts, are.

Do not repeatedly answer with "extend the deadline" or "lower the
standard". First optimise the scope (§6). If nothing qualifies after that,
report NO SUITABLE TOPIC FOUND, name the remaining unavoidable
constraints, and give the minimum verified change (extra time, compute or
scope) that would make the best design qualify.

### 1a. Mandatory discovery order: Benchmark → Research Question → Method

Every candidate is built in exactly this order. Each step is written down
before the next one starts.

1. **Benchmark.** Fix an established benchmark. Record:
   - its strongest existing baselines, after the baseline-maturity audit
     (§4d.1);
   - its documented failure modes;
   - its open questions, taken from the benchmark's limitations, future
     work and discussion sections and from follow-up papers.
2. **Research question.** Derive the question from one *documented*
   failure or open question of that benchmark. Attach a falsifiable
   causal hypothesis about **why** the strongest baseline fails. Write
   the question on the benchmark's own metric **before any method is
   named**.
3. **Method.** Choose or design the method that tests that causal
   hypothesis. The method follows from the hypothesis, never the reverse.

Forbidden starting points:
- a method or lever looking for a benchmark ("probe frozen activations",
  "LoRA a 7B model", "add hard negatives", "use a bigger model");
- a weak baseline looking for a method.

Every candidate record shows steps 1–3 in order. A candidate whose method
was fixed before its question goes back to step 2.

### 1b. Anti-fixation: exploration across AI/ML

1. **Subfield coverage before shortlisting.** Discovery screens at least
   **10–15** public benchmarks spread over at least **six** distinct
   AI/ML subfields before any shortlist is formed (§1c). Subfields may
   come from any area of AI/ML (§1d). Examples:
   - model evaluation and benchmark validity;
   - uncertainty estimation and calibration;
   - robustness and distribution shift;
   - data quality, label noise and data selection;
   - efficient inference (quantisation, pruning, speculative decoding,
     KV-cache compression);
   - classification (text, tabular, vision);
   - representation learning, embeddings and retrieval;
   - LLM reasoning, code and tool use;
   - time series, graphs and recommendation;
   - technical AI safety (safeguards, interpretability, honesty,
     control, unlearning, …), as one subfield among many.

   At least two benchmark candidates per subfield are recorded, each
   with its outcome. Every discovery report includes a coverage table:
   subfield → candidates → outcome and reason.
2. **Concentration cap.**
   - At most **one** final slot per benchmark.
   - At most **one** final slot per subfield.
   - No subfield supplies more than 40% of the shortlist.

   The user may override these caps explicitly.
3. **No carry-over anchoring.** Benchmarks, subfields and mechanisms that
   were selected or proposed as GO/REVISE in this user's **previous two
   discovery runs** are excluded from a new run by default.
   - List them as "previously explored", each with its recorded failure
     reason.
   - One may return only if new verified evidence, dated after that
     run, removes its failure reason. Cite that evidence.
   - Earlier archives and memory notes are background. They are never
     seeds for new topics.
4. **Immature benchmarks.** A benchmark is **IMMATURE** if it was
   released less than 3 months ago, or if its only baselines come from
   its own authors.
   - It may hold at most one slot.
   - It needs the baseline-maturity audit (§4d.1) before S1 is rated.
5. **Search depth.** Every final candidate rests on primary sources:
   - the benchmark paper;
   - at least two follow-up or competing papers.

   Read them from downloaded HTML/PDF text, not from a summarised fetch.
   Every number used for S1 is quoted with its table or figure location.

### 1c. Benchmark-screening stage (mandatory, before any research question)

Discovery runs in this order. No research question is written before
step 6, and no method is proposed before step 7.

1. **Screen** at least 10–15 diverse public benchmarks across at least
   six AI/ML subfields (§1b).
2. **Strongest existing methods.** For each benchmark, record the
   strongest existing methods and their published numbers (source and
   table location), after a quick maturity audit (§4d.1). Mark
   unmeasured strong systems UNMEASURED.
3. **Failure modes and headroom.** Record the documented failure modes
   and the realistic room for improvement. Is the benchmark saturated,
   near its label-noise ceiling, or leaderboard-crowded? Is there a
   documented slice where the best method fails?
4. **Rank** the benchmarks by SOTA-improvement potential first, then by
   implementation feasibility within D at level L (§5).
5. **Select the three most promising benchmarks.**
6. **Only then** formulate research questions (§1a step 2).
7. **Propose methods last**, after a prior-work check of the method idea
   (prior-work-checker).

**Early kill check (budget discipline).** Before spending more than a
small share of the research budget developing any single idea, check:
- whether a stronger existing method already solves the problem on that
  benchmark;
- whether the closest prior work already proposed the method.

If either holds, drop or redesign the idea immediately. Do not polish it
first. This check is Stage 1 (rapid screening) of prior-work-checker's
staged investigation. Stage 2 (focused) and Stage 3 (final verification)
follow for shortlisted and selected candidates. See
[prior_work_novelty_sota_review.md](../../prior-work-checker/references/prior_work_novelty_sota_review.md)
§1. The screening table (benchmark → strongest method + number →
failure modes → headroom → feasibility → rank) is a required section of
every discovery report.

### 1d. Topic scope and priorities (user instruction, 2026-10-09)

- **Scope:** any area of AI or machine learning. Technical AI safety is
  **not** a requirement. Never reject a promising AI/ML topic because it
  is unrelated to AI safety.
- **Sources:** user-named safety sources (Shallow Review, Inspect Evals)
  are optional inputs, not the default scope. General sources include
  leaderboards, benchmark papers, recent method papers and public
  repositories.
- **The user's priorities, in order:**
  1. credible SOTA-improvement potential (highest priority);
  2. feasibility within D working days, given the user's skills;
  3. strong public benchmarks, reproducible baselines and reliable
     evaluation;
  4. a clear, measurable research contribution;
  5. novelty (important, but secondary to performance improvement).

  §8 encodes this order.

## 2. Beginner (experience level)

- "Beginner" describes the researcher's **experience**. It does not cap
  the technical difficulty of the project.
- Do not automatically exclude any of the following because the user is
  a Beginner:
  - GPU experiments
  - fine-tuning (including LoRA)
  - activation extraction or analysis
  - mechanistic interpretability
  - white-box methods
  - technically challenging algorithms
- Instead, check whether each is feasible with existing tools, pretrained
  or released models, public code, and a carefully scoped experiment.
- Beginner level affects the **estimate**, not eligibility.
  - Add learning time for tools that are genuinely unfamiliar. Size it
    from the verified quality of their code and documentation (a
    documented run command, an example config, released checkpoints).
  - Count this learning time once, in the phase where it occurs. Never
    count it as an extra cost on every phase.

## 3. Technical depth (mandatory gate)

A project has technical depth when its contribution is a **mechanism,
hypothesis, or scientific insight** that targets a diagnosed weakness.
Examples:
- a new signal, representation, objective, training signal or inference
  procedure;
- a principled use of information the baseline cannot access;
- a test of a mechanistic hypothesis whose result would change how the
  field builds or evaluates methods.

Technical depth is judged by the **significance of the mechanism and the
insight**, not by implementation complexity. A short implementation can
have depth; a large pipeline can lack it.

**Technical depth: FAIL** when the **entire** contribution is one of:
- a fixed threshold on an existing score;
- simple voting;
- weighted or unweighted averaging of existing scores;
- hyperparameter tuning;
- re-running an existing method on the same setting;
- a new combination of existing outputs with no new signal or hypothesis;
- a **standard engineering lever** applied without a falsifiable causal
  hypothesis about the baseline's failure. Such levers include:
  - more, other or distribution-matched training data, including standard
    augmentation and hard-negative mining;
  - a larger or different backbone;
  - standard fine-tuning, LoRA or distillation;
  - swapping a frozen probe for a fine-tuned head, or the reverse;
  - prompt engineering;
  - more inference compute;
  - re-applying a published recipe unchanged to a new benchmark.

A lever passes only when all three hold:
- (a) the project states a causal hypothesis for **why** the strongest
  baseline fails;
- (b) it includes a diagnostic or control whose outcome could falsify
  that hypothesis;
- (c) the outcome passes the predictability test (§4e).

"It is a new training signal" or "it is a new setting" is never
sufficient on its own.

Such components are allowed **inside** a project whose core contribution
passes (for example, a threshold applied to a new, principled signal,
where the signal is the contribution).

Every candidate must state its depth case in one or two sentences: what
the mechanism is, and what insight a positive or negative result gives.

## 4. SOTA potential (pre-experiment) vs SOTA achievement (post-experiment)

These are two different ratings and are never merged.

### 4a. Strongest comparable baseline

The strongest published or reproducible method that meets all of these:
- same task, evaluation set or slice, metric and protocol;
- the same class of model access (black-box vs white-box) and comparable
  resources (model size, training data, inference budget) — or the
  difference is stated and justified;
- it is reported (with a number and its source) or can be reproduced from
  released code or outputs.

Always also name the strongest method on the benchmark overall, even when
it is not comparable.

### 4b. Pre-experiment SOTA potential (S1–S4)

Rate each criterion STRONG / PARTIAL / WEAK / UNVERIFIED. No
experimental proof of improvement is required. Speculation alone never
earns STRONG.

| Criterion | STRONG when | PARTIAL when | WEAK when |
|---|---|---|---|
| **S1 Documented weakness and headroom** | The strongest comparable baseline has a verified number on the named task and metric, plus a **documented weakness** with verified room to improve. The weakness can be a failure category, a subset, an error mode, or a gap to a ceiling or reference. The headroom is not something only a much larger model or budget could close. | The baseline is verified, but the weakness or its size is only partly documented. | Near ceiling, label-noise bound, or no documented weakness. |
| **S2 Mechanism targets the weakness** | The intervention directly addresses the **cause** of the documented weakness, **and** there is a technically credible reason to expect improvement. That reason is either evidence from a closely related setting, or a principled argument a reviewer would accept (for example: access to information the baseline provably lacks, an objective mismatch, a documented inductive-bias failure). | It targets the weakness, but the reason is plausible rather than principled or evidenced. | "Should help in principle", or it does not target a diagnosed weakness. |
| **S3 Fair, reproducible test** | Same task, split or slice, metric and protocol as the baseline. The baseline number is released, reproducible, or recomputable from released outputs. Resources are comparable, or the difference is declared. Leakage is controlled. | A protocol detail or the baseline reproduction is not yet verified, but a concrete plan exists. | No fair comparison is possible. |
| **S4 Feasible MVRD** | The scoped design fits D at level L under §5, with verified code, models and data. Compute is either confirmed or has a concrete mitigation (an access check on day 0, a pre-download, a smaller fallback model already named). A GPU that is DOCUMENTED-AVAILABLE in the global `compute.md` (Hardware Fit and Documented Access on an all-account partition) with these mitigations counts as STRONG; unverified allocation or UNKNOWN queue time alone never lowers S4. | It fits only if one unverified requirement holds, and that requirement has no mitigation yet. | It does not fit D after scope optimisation. |

- **HIGH:** all four STRONG, on verified facts, under the evidence rules
  in §4d (no conditional HIGH).
- **MEDIUM:** S1 and S3 STRONG, and S2 and S4 at least PARTIAL. This is
  a **credible path to SOTA**.
- The §4d rules take precedence over the table above wherever they are
  stricter.
- **LOW:** S1 or S2 WEAK, or S3 or S4 WEAK.
- **UNKNOWN:** S1 UNVERIFIED (no verified baseline number).

Compute for S4 and for every feasibility estimate is resolved only from
the global `~/.claude/skills/compute-planner/references/compute.md`
(single source of truth; its Feasibility Rules). A project-local
`compute.md` is a mirror, never a required input or fallback; a missing
or empty local copy never means no GPU. Unverified allocation and
unknown queue time are UNKNOWN, never UNAVAILABLE. GPU designs, including
single-GPU 7B–8B experiments on H100, H200, A40 or V100, are considered
by default, and a CPU-only or API-only design is never preferred solely
because GPU allocation is unverified. This does not assume unrestricted
access or guaranteed scheduling: allocation stays UNKNOWN until a user
job confirms it, and is carried as a RISK with a mitigation.

### 4c. Post-experiment SOTA achievement

Recorded only after the experiment, by experiment-runner and paper-writer:
- **ACHIEVED:** the method beats the strongest comparable baseline under
  the same protocol, by at least the pre-registered SESOI, with the
  pre-registered statistical criterion met.
- **NOT ACHIEVED:** the CI excludes an improvement of at least the SESOI,
  or the method is worse.
- **INCONCLUSIVE:** anything else.

**Claim level (mandatory label; added 2026-10-17, see §4f).** Every
ACHIEVED result is also labelled with its claim level. Overall SOTA is
level 1 only.

**Scope rule.** Every SOTA claim, before or after the experiment, names:
- the task;
- the evaluation slice (if not the full benchmark);
- the baseline;
- the metric;
- the model or access class.

A result on a narrow slice is reported as "SOTA on <slice> of <benchmark>
for <metric> against <baseline>". It is never reported as overall SOTA
on the benchmark.

### 4d. Evidence rules for SOTA potential (mandatory; stricter than 4b and override it)

**1. Baseline-maturity audit before S1.** The strongest comparable
baseline is the strongest *existing* applicable method, not merely the
strongest one the benchmark paper reported.
- Search for methods, models and detectors released after the
  benchmark: follow-up papers, open guard/detector models, strong open
  LLMs.
- Record each one's published number on the benchmark, or mark it
  **UNMEASURED**.
- **S1 cannot be STRONG while a plausibly stronger released system is
  UNMEASURED on the benchmark.** It is PARTIAL.
- A cheap measurement (≤ 30 min on CPU or one GPU) can settle this, but
  it is an experiment and needs the user's permission.

**2. A weak baseline is not headroom.**
- A poor baseline number is never, by itself, evidence of SOTA potential.
- If the headroom exists only because the baseline set omits a standard
  method class, S1 is **WEAK**. Examples of omitted classes: input
  moderation, a modern guard model, a strong open LLM, a published
  follow-up method.
- If the only baselines are the benchmark authors' own, S1 is at most
  PARTIAL until the audit is done.

**3. S2 needs cause evidence, not only lever evidence.**
- *Lever evidence* ("this kind of method helped elsewhere") alone gives at
  most PARTIAL.
- *Cause evidence* means a documented diagnostic, ablation, error
  analysis or per-item output showing the baseline fails *because of*
  the factor the method changes.
- S2 is STRONG only with cause evidence **plus** either lever evidence
  from a closely related setting or a principled argument that the method
  uses information the baseline provably lacks.
- **Combinations of signals or methods.** Evidence that each component
  works on its own is lever evidence only. S2 above WEAK for a
  combination requires two things:
  - a **complementarity argument**: the components fail on different,
    documented causes, so the combination targets a failure that neither
    addresses alone;
  - the specific failure mode of the strongest baseline that the
    combination addresses.

  Published redundancy evidence (correlated errors, or combination gains
  that shrink as the components get stronger) caps S2 at PARTIAL until
  the design includes a diagnostic that could show complementarity. The
  component and combination evidence comes from prior-work-checker's
  Evidence Report (combination analysis).

**4. No conditional HIGH.**
- HIGH requires all four criteria STRONG on facts verified **now**.
- "HIGH if X holds" is reported as the lower rating, with X named as the
  upgrade condition.
- Unconfirmed GPU allocation is the only exception, and is handled under
  S4.

**5. Expected-margin check.**
- Every HIGH or MEDIUM states an expected effect size with its basis: the
  measured result it extrapolates from, and why.
- It also states the planned test's minimum detectable effect (MDE).
- If the expected effect is below the MDE, or below the SESOI, S3 is at
  most PARTIAL.

**6. Calibration record.**
- When a post-experiment outcome (§4c) exists for a past design, compare
  it with that design's pre-experiment rating.
- Cite past misses when rating similar designs. Example: v6/RQ4 on
  PromptSET (TF-IDF vs BERT-PE) was rated a credible path, then measured
  ΔAcc −2.43 pp, CI [−3.05, −1.81].
- A rating rationale that resembles a past miss must say what is
  different this time.

### 4e. Defensible contribution: publishable finding vs routine engineering

Every candidate states, in one sentence each:
- **Finding if positive:** what the field learns, beyond "method M scored
  higher".
- **Finding if negative:** what the field learns if M fails.
- **Predictability test:** would an expert reviewer, shown only the
  design, confidently predict the outcome?
  - If they would predict success (for example, "distribution-matched
    training data helps on the matched test distribution", "a 7B model
    beats a 184M model"), the project is **confirmatory engineering**.
    Technical depth FAILS unless the *negative* outcome would be
    surprising and informative, and the design can detect it.
  - If they would predict failure, the SOTA path is not credible (S2 WEAK).
- **Reviewer pre-mortem:** the single most likely rejection reason, plus
  the specific experiment or control inside D that answers it.

A defensible contribution needs a non-obvious finding in at least one
outcome, and a pre-mortem answer that fits inside D.

### 4f. Four performance-claim levels (never merged; added 2026-10-17)

Every planned or reported improvement is tagged with exactly one level.
Planning documents and papers use the level's wording, never a stronger
one.

| Level | Definition | Allowed wording |
|---|---|---|
| **1. Overall SOTA** | Beats the best published result on the benchmark's **standard** full protocol, after the baseline-maturity audit (§4d.1). No stronger released system is UNMEASURED. | "state of the art on <benchmark> (<metric>)" |
| **2. Best reproducible baseline** | Beats the strongest method we could reproduce (or that is reproducible from released outputs) under the standard protocol. Stronger published but non-reproducible results may exist and are named. | "outperforms the strongest reproducible baseline, <name>" |
| **3. Selected baseline** | Beats a specific chosen baseline that is **not** the strongest comparable one. | "improves over <baseline>" (never "SOTA") |
| **4. Restricted protocol** | Improvement holds only under a restricted setting: a slice, a smaller model class, a reduced budget, a modified metric or a subset. | "on <slice/setting>, improves over <baseline>" + the restriction in the same sentence |

- The pre-experiment SOTA-potential rating (§4b) states which level the
  project **targets**. HIGH or MEDIUM SOTA potential means a credible
  path to level 1 or 2. A project that can reach only level 3 or 4 has
  SOTA potential at most LOW, unless the user waived gate 9.
- Post-experiment, ACHIEVED (§4c) is reported together with its level.
  A level-4 result is never described as overall SOTA (existing scope
  rule).

## 5. Feasibility estimation (D-day sprint; 4-day profile)

D is always the user-specified duration (in working days). The worked
profile below is for D = 4, which is the user's current standard sprint.

Estimate **actual work**. Do not stack pessimistic assumptions. Report
five separate buckets:

| Bucket | Contents |
|---|---|
| 1. Essential implementation | Reading only what the design needs; setup; adapting released code; reproducing the baseline on the evaluated slice; implementing the intervention; debugging |
| 2. Compute | GPU or CPU wall-clock, queue time (UNKNOWN unless observed; covered by the mitigation and contingency, never a reason to exclude GPU), downloads. Report **active work** and **wall-clock** separately. Compute that runs in the background overlaps with writing or analysis and is not counted twice. |
| 3. Evaluation and statistics | Metrics, controls, ablation, CIs or tests, sanity checks, tables and figures |
| 4. Paper writing (AI-drafted, human-verified) | The ~4-page paper is **drafted primarily by AI** (paper-writer). The human budget is review and verification: <ul><li>check every number against output files;</li><li>check every citation against its source;</li><li>check that claims match the evidence and the pre-registered criteria;</li><li>edit figures, captions and limitations;</li><li>do a final read.</li></ul> **Budget 0.5 day total at Beginner (range 0.5–0.75):** about 0.25 for the pre-experiment draft review and about 0.25–0.5 for the post-experiment verification and revision. Do not budget human drafting time. Verification time is mandatory and never cut to make a project fit. |
| 5. Contingency | Sized to the **one or two most likely** risks, each with its mitigation. Not a fixed percentage, and not the sum of every conceivable failure. |

Label every line:
- **VERIFIED:** checked against the actual repository, dataset, model
  card, released outputs or compute documentation.
- **ESTIMATE:** reasoned from verified facts.
- **RISK:** a speculative failure. It gets a probability (low / medium /
  high) and a mitigation. It adds work only if it is high-probability,
  otherwise it is covered by contingency.

**Do not assume** any of the following without verification:
- GPUs are unavailable because allocation is unverified, queue time is
  unknown, or a project-local `compute.md` is missing or empty;
- GPU setup takes a full day;
- the baseline reproduction will fail;
- every model must be downloaded from scratch (check released
  checkpoints, adapters, cached activations and outputs);
- existing implementations cannot be reused;
- the full benchmark must be evaluated, when a pre-specified,
  scientifically justified slice answers the question.

A slice must be fixed **before** the results are seen. It must be
justified by the diagnosed weakness. It must be reported with its full
definition.

**Verdict.**
- **FITS DURATION:** expected work (buckets 1–4, active time) plus
  contingency is at most D, and the critical-path wall-clock (including
  compute that cannot overlap) is at most D.
- Otherwise **DOES NOT FIT**: name the binding bucket and apply §6
  before rejecting.

**4-day profile** (a guide, not a template; estimate each project from
its own verified requirements):

| Day | Work |
|---|---|
| 0.5 | Setup, verified assets, baseline reproduction on the slice; launch long compute early |
| 1.75 | Implement the intervention, the diagnostic that tests the causal hypothesis, and controls. AI drafts the paper while compute runs; review the draft (≈ 0.25) |
| 1.0 | Evaluation, statistics, figures |
| 0.25–0.5 | Human verification of the AI-revised paper: numbers, citations, claims vs evidence |

The remainder (≈ 0.5) is contingency. Compute runs in the background where
possible. The day saved on writing goes to the research itself (the
diagnostic, controls and the pre-mortem experiment), never to scope
creep.

## 6. Research redesign (mandatory before any rejection)

Before rejecting a promising candidate for feasibility, depth or SOTA
potential, attempt **at least one meaningful redesign**. Apply levers in
this order and re-evaluate after each:

1. Narrow the research question to the documented failure category or
   subset (the slice must be pre-specified; see §5).
2. Reuse published implementations, configs and evaluation scripts.
3. Reuse pretrained or fine-tuned models, adapters, released outputs,
   cached activations and intermediate results.
4. Reduce scope that the main claim does not need: fewer models, layers
   or seeds; one setting. Separate essential experiments from optional
   extensions.
5. Design a smaller intervention that keeps the mechanism (for example,
   a probe on frozen activations instead of fine-tuning the model).
6. Choose a more appropriate benchmark or evaluation setting for the same
   mechanism.
7. Only then replace the direction.

A redesign must keep a genuine research contribution, which means it
still passes the technical-depth gate (§3) and the defensible-contribution
test (§4e). It must never weaken a mandatory gate (§7). Record each
redesign attempt and its outcome.

Two further rules apply:
- **Depth or SOTA failures.** A redesign triggered by a depth or SOTA
  failure must change the research question or the causal hypothesis
  (§1a step 2). Swapping one standard lever for another (probe ↔
  fine-tune, small ↔ large model, curated ↔ matched data) is not a
  meaningful redesign.
- **Replacements.** A replacement direction obeys the anti-fixation rules
  (§1b): it does not move to a second slot on the same benchmark or
  subfield.

Example:
- Original: "Train a large deception detector."
- Redesign: "Reuse a released model and its released transcripts, and
  test a targeted activation-based mechanism on the documented failure
  category where every transcript-based detector fails."

## 7. Mandatory gates (never weakened)

1. **Benchmark validity:** exact or direct benchmark, SAME-TASK test,
   comparability check, V1–V4 (benchmark-finder).
2. **No data leakage:** train, calibration and test separation;
   thresholds and slices fixed before the test results are seen; no
   training on the test labels or on their construction procedure.
3. **Fair baseline comparison:** same protocol (§4a, S3).
4. **Prior-work verification:** prior-work-checker PASS, plus the
   archive re-check. The PASS must be backed by a FINAL Prior-Work
   Evidence Report (Stage 3, evidence quality not Unverified). Its novelty
   classification maps onto the gate as follows:
   - NOVEL or PARTIAL OVERLAP can PASS only if P1–P5 hold;
   - ALREADY STUDIED is a FAIL;
   - UNCERTAIN is FAIL-UNVERIFIED, never PASS.

   Details are in
   [prior_work_novelty_sota_review.md](../../prior-work-checker/references/prior_work_novelty_sota_review.md)
   §5–§7. Only prior-work-checker issues this verdict.
5. **Reproducibility:** public or released code, data, models and seeds,
   documented commands.
6. **Statistical rigor:** pre-registered SESOI, CI or test, power or MDE
   note, controls that distinguish the explanations
   (Negative-Result Interpretability Review).
7. **Research integrity:** no fabricated numbers; results stay TBD until
   measured; no post-hoc changes to slice, threshold or metric; honest
   reporting of negative and inconclusive results.
8. **Technical depth:** PASS (§3), including the defensible-contribution
   test (§4e).
9. **Credible SOTA path:** SOTA potential at least MEDIUM (§4b), rated
   under the evidence rules (§4d). The user
   may raise this to "HIGH required" or, for an explicitly
   scientific-diagnostic goal, waive it. Without such an instruction,
   MEDIUM is the minimum and HIGH is preferred.
10. **Feasibility:** FITS DURATION (§5) at level L.
11. **Discovery process:** the candidate was built in the order Benchmark
    → Research Question → Method (§1a), and the run satisfied the
    anti-fixation rules (§1b).
12. **Mechanism and domain validity (MDV):** verdict PASS, or
    PASS-EXPLORATORY under the conditions in §9. A FLAG must be resolved;
    FAIL rejects the candidate after redesign.

A project that cannot satisfy every gate after redesign is not selected.

## 8. Selection and ranking

Among designs that pass every gate, rank by:

1. **Credible SOTA potential** under §4d (HIGH > MEDIUM). Within a rating,
   rank by the strength of the S2 *cause* evidence, then by expected
   margin relative to the MDE.
2. **Four-day feasibility margin, given the user's skills:** contingency
   left; verified rather than estimated requirements; critical-path
   slack.
3. **Benchmark and evaluation strength:** a public benchmark;
   reproducible baselines (released code, models or per-item outputs);
   reliable evaluation (automatic metric, adequate test size and power,
   low label noise, no contamination).
4. **Clear, measurable contribution (§4e):** a non-obvious finding in at
   least one outcome; strength of the pre-mortem answer; technical depth.
5. **Novelty strength.** Important but secondary. Modest novelty is
   acceptable when 1–4 are strong. The advisor reads it from the
   Evidence Report's classification, using the mapping in
   prior_work_novelty_sota_review.md §8. It never raises SOTA potential.
6. Negative-result interpretability.
7. Original-question preservation (tie-breaker).

This order follows the user's stated priorities (§1d). Topic area
(AI safety or not) is never a ranking criterion.

**No padding.**
- Return only the candidates that pass every gate, up to the requested
  number.
- If fewer qualify, report the shortfall. Never fill a slot with a
  "GO (conditional)" whose condition is anything other than unconfirmed
  compute allocation.

Select one primary and the qualifying ranked backups. For each, report:
- the strongest baseline and its documented weakness;
- the mechanism and why it should help;
- the MVRD (essential vs optional);
- S1–S4 with evidence, including the baseline-maturity audit, the cause
  evidence, and the expected margin vs the MDE (§4d);
- the depth case, findings if positive and negative, the predictability
  test, and the reviewer pre-mortem (§4e);
- the Benchmark → Question → Method record (§1a);
- the D-day plan with VERIFIED / ESTIMATE / RISK labels;
- risks with mitigations;
- the refinement history;
- the MDV record and verdict (§9), and the performance-claim level
  targeted (§4f).

## 9. Mechanism and Domain-Validity Gate (MDV; mandatory gate 12; added 2026-10-17)

**Why this exists.** A past proposal (test-case generation to expose
program faults) assumed that an LLM generator "struggles to produce
sufficiently extreme inputs". It never explained **why** the intervention
should improve fault exposure for the programs in the benchmark. Programs
differ greatly in behaviour and execution cost. Some process huge inputs.
Some run for hours or longer. More generated cases do not mean better
testing, and a few well-designed cases can beat many generic ones. An
intervention that helps one program class can fail on another. The MDV
gate makes this reasoning explicit before approval.

**When.** Written by research-readiness-advisor during Design (Step 5c,
with S2). Re-checked by research-planner (Step 8b) and by the
research-pipeline Step 5b evidence gate. Updated after every redesign.
paper-writer uses it for the Introduction's "why it should work", for
Limitations and for claim levels.

### 9a. The ten questions (each answered in 1–4 sentences, with sources)

| # | Question | What a sufficient answer contains |
|---|---|---|
| Q1 | What precise problem does the existing method fail to solve? | The failing method by name, the task, the metric and the failure category, on the benchmark's own terms |
| Q2 | What evidence shows this limitation actually exists? | Per-item outputs, error analysis, tables in the source paper (location), or our own measured diagnostic. "It is plausible that" is not evidence |
| Q3 | Why should the proposed mechanism address that limitation? | The causal chain intervention → changed intermediate quantity → target metric, step by step |
| Q4 | What assumptions must hold for the mechanism to work? | An explicit list (data properties, model capabilities, compute or execution-cost properties, scorer properties) |
| Q5 | Are those assumptions valid for the benchmark's actual data and tasks? | Each assumption checked against the benchmark: VERIFIED (inspected data, cited statistics), PLAUSIBLE, or VIOLATED for some subset (name it and estimate its share) |
| Q6 | Under what conditions would the method fail? | Concrete problem classes or regimes (e.g. programs whose cost is dominated by I/O; tasks where the baseline is already at ceiling) |
| Q7 | What alternative explanations could account for an observed improvement? | At least two (e.g. more samples or compute; leakage; a scorer artefact; prompt length; selection on test; regression to the mean) |
| Q8 | What is the simplest existing method that could produce the same benefit? | A named method or trivial baseline (more samples at matched budget, best-of-k, a fixed heuristic, the published recipe) |
| Q9 | What experiment would distinguish the proposed mechanism from that simpler explanation? | A matched-budget control or diagnostic, with its predicted outcome under each explanation. It must be inside the MVRD and fit D |
| Q10 | Does the hypothesis generalize across the relevant problem classes, or only a narrow subset? | The problem classes in the benchmark and the expected effect for each. If only a subset, the paper's claims are scoped to it (and any slice is pre-specified, §5) |

### 9b. Evidence level of the mechanism (label exactly one)

| Level | Name | Meaning |
|---|---|---|
| E0 | Intuitive idea | A reason that sounds right; no specific causal chain, or an unsupported assumption in it |
| E1 | Plausible mechanism | A complete causal chain (Q3) with explicit assumptions (Q4) that pass Q5 against the benchmark, but no external support |
| E2 | Supported by prior research or theory | E1 plus published evidence (an ablation, an analysis or a theorem) that the same causal link holds in a closely related setting. Cite the location |
| E3 | Supported by direct experimental evidence | E2 or E1 plus our own measured diagnostic, or released per-item outputs, on this benchmark showing the causal link |

E-levels and S2 (§4b, §4d.3): S2 STRONG requires cause evidence, so E3,
or E2 with a documented diagnostic of the baseline failure. S2 PARTIAL
requires at least E1. E0 means S2 is WEAK.

### 9c. Verdict

- **PASS:** Q1–Q10 answered with sources. E1 or higher. No assumption is
  VIOLATED for the main evaluation set without a pre-specified scope
  restriction. Q9 names a feasible discriminating experiment that is
  part of the design.
- **PASS-EXPLORATORY:** the mechanism is E0–E1 with real uncertainty, and
  **all** of the following hold:
  1. the hypothesis is falsifiable (a stated result would refute it);
  2. the Q9 experiment is in the design;
  3. the uncertainty is stated explicitly in the plan and in the paper;
  4. the negative result is informative (Negative-Result
     Interpretability Review PASS).

  Exploratory candidates still need every other gate. Gate 9 (SOTA
  path) usually needs the user's waiver for a scientific-diagnostic goal.
  They rank below PASS candidates with equal SOTA potential.
- **FLAG (must be resolved before GO):** one or more questions unanswered;
  an assumption VIOLATED for a large, unscoped share of the benchmark; or
  no feasible Q9 experiment. Route to research-readiness-advisor
  redesign (Step 7). A redesign changes the hypothesis or scopes the
  claim (§6).
- **FAIL:** no coherent causal explanation of why the intervention should
  improve the target metric (Q3 missing or self-contradictory). Or Q8's
  simpler method is expected to produce the whole benefit, and no Q9
  experiment can separate them. Or the core assumption is VIOLATED for
  the benchmark. This holds even after redesign.

### 9d. Wording rules (planning documents and papers)

- Speculative mechanisms are never stated as fact. E0/E1 → "we
  hypothesize", "is designed to". E2 → "prior work suggests [cite]".
  E3 → "our diagnostic shows (Table k)".
- "X struggles with Y" or "the generator cannot produce Z" are claims.
  They need Q2 evidence, or they are written as hypotheses.
- A measured performance difference never upgrades the mechanism's level
  by itself. Only the Q9 discriminating experiment does
  (paper_standards.md §2, L4).

### 9e. Worked example (the motivating case)

Proposal: "LLM test generators miss extreme numerical inputs, so add a
boundary-value generator to raise fault exposure (TLE/MLE) on
TestCase-Eval."
- Q2: Is there evidence that missed faults are caused by insufficiently
  extreme values? This needs per-fault analysis, not intuition.
- Q4/Q5: The mechanism assumes faults are triggered by input magnitude.
  For programs whose fault depends on structure (e.g. an adversarial
  graph shape, a hash collision pattern, a worst-case ordering), magnitude
  alone does not help. Q5 must estimate the share of such programs.
- Q6: It fails where execution cost makes large inputs infeasible, or
  where faults are logical rather than resource-related.
- Q7/Q8: The gain could come from simply generating more cases. The
  simplest equivalent is best-of-k sampling at a matched case budget.
- Q9: Compare at a matched number of cases and matched execution budget,
  and stratify by fault class (magnitude-triggered vs structure-triggered).
- Q10: Claims are scoped to the fault classes where the assumption holds.

Without Q2 evidence and a Q9 control, the verdict is FLAG. It is not
PASS.

## 10. Configurable researcher defaults (added 2026-10-17)

The researcher profile and default constraints live in one file:
`~/.claude/skills/research-benchmark-advisor/references/researcher_profile.md`.
Every research and paper skill reads its **Default constraints** and
**Preferences** sections and applies per-project overrides. Overrides
are given in the invocation, the RQ file, or a project
`research_profile.md`. Nothing in this section is hard-coded into a
project. Record the effective values in each report.

| Default | Value | Used by |
|---|---|---|
| Duration D | 4 working days | §5, compute-planner |
| Paper length | 4 pages (`default-4` venue profile, references excluded) | paper-writer, paper-to-latex, page-limit gate |
| Priority | defensible overall SOTA (§4f level 1–2) > novelty | §8 |
| Depth | meaningful technical depth (§3) | gate 8 |
| Experience | beginner research/implementation; statistics + CS background | §2, §5 |
| Compute | OSU HPC GPUs (global `compute.md`) | §4b S4, §5 |
| Assets | prefer public code and pretrained checkpoints | §6 levers 2–3 |
| Interests (tie-breaker) | underlying AI mechanisms, model interactions, anomaly detection | §8 tie-breaks |
| Extensibility (preferred, not mandatory) | multi-agent systems **or** multimodal learning/robotics (either suffices) | §8 tie-breaks |
