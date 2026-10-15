---
name: experiment-runner
description: Manually invoked. Takes ONE completed pre-experiment paper from paper-writer (paper_RQk_vN.md), extracts its frozen experimental design, writes a bounded experiment plan, implements and runs only the pre-specified experiment, controls, ablations and statistical test, and saves results_RQk.md plus machine-readable outputs for paper-writer's post-experiment revision. Never adds experiments because a result is weak, null or surprising. Usage - /experiment-runner <paper_file> [RQk]
---

# Experiment Runner

Pipeline position:

RQ/design → paper-writer (pre-experiment) → **experiment-runner** →
paper-writer (post-experiment revision, `results:` = `results_RQk.md`)

One invocation = one paper = one RQ. This skill is invoked manually. It
runs experiments; it does not write or revise the paper, redesign the
project, select research questions, or search for benchmarks.

Governing goal:

> Run the smallest pre-specified experiment set that can answer the frozen
> research question credibly, following the mentor's research advice.

When unsure whether something should be added, do NOT add it unless the
research question cannot be answered validly without it.

## Invocation

```
/experiment-runner <paper_file> [RQ identifier]
```

- `paper_file` (required): a complete pre-experiment paper produced by
  paper-writer, e.g. `paper_RQ1_v1.md`.
- RQ identifier (optional): `RQk`. Needed only if the paper's RQ cannot be
  read unambiguously from its file name, title block or body. If the
  supplied identifier disagrees with the paper, stop and ask.

The supplied paper is authoritative. If it is missing, unreadable, not
supplied, or not a pre-experiment paper (e.g. it has no `TBD` results and
reads as already revised), ask the user. Never search for, or substitute,
an older paper, another version, or another RQ file.

## Sources and precedence

1. **The supplied paper**: authoritative for the frozen project-specific
   design (RQ, hypothesis, benchmark, dataset, split, labels, model or
   released outputs, method, baseline, metrics, controls, ablations,
   statistical test, success and stop/pivot criteria).
2. **The RQ/design file the paper derives from** (e.g. the
   `research_pipeline_report_vN.md` and `prior_work_*.md` archive it names
   or that sit in its folder and name the same RQk): read only to resolve
   provenance, to resolve a blocking TBD (Step 2), or to verify that the
   paper's design has not drifted from it. If you cannot tell which RQ file
   the paper derives from, do not guess; work from the paper alone and say
   so.
3. **Mentor references** (below): methodological guidance for scope,
   feasibility, minimum sufficient evidence, stop/pivot decisions and
   interpretation.
4. Benchmark conventions (official repo / paper of the benchmark, as cited
   in the paper or archive).
5. The simplest standard choice that preserves the research question.

Mentor advice is guidance, not evidence. It never establishes a result.

### Mentor references (read at run time, every run, before planning)

Read these completely before Step 1. Do not reconstruct or invent mentor
advice; use only what the files say.

- `~/.claude/skills/research-readiness-advisor/references/mentorship_principles.md`
  — especially "Core principle", "Research-question guidance" items 7 and
  9, "Baseline and performance", "Writing first", "Pivoting".
- `~/.claude/skills/research-readiness-advisor/SKILL.md` — Step 8
  ("Writing-first workflow", in particular "After the experiment") and
  Step 9 ("Pivot guidance").
- `~/.claude/skills/benchmark-finder/references/research_advice.md` —
  benchmark-first advice: reuse existing infrastructure, smallest
  meaningful extension, implementation simplicity.

On Windows, `~` is `C:\Users\<user>`. If a file is not found there, use
the copy in the project's own skills tree, if one exists (e.g.
`no-more-slops/tracks/auto-paper/skills/...`) and say which
copy was read. If no copy of a reference can be read, stop and tell the
user; do not proceed from memory.

### How mentor advice applies at execution time

The mentor files were written for the whole project lifecycle. This skill
applies them within the frozen design as follows:

- **"Writing first" / Step 8 "After the experiment" and "Pivoting"** say
  that if the intended result is not achieved, one should diagnose, make
  small justified changes, and rerun within budget. This skill keeps that
  advice but never runs the loop autonomously: it runs the frozen plan
  once, records the outcome, and, if the result is weak, null, surprising
  or negative, diagnoses it from the existing outputs and proposes ONE
  smallest justified change (Step 9). Nothing is rerun without the user's
  explicit approval in chat, and an approved change is written to the
  Deviation log before it executes. The paper's own stop/pivot criterion
  and the user's budget bound how many such cycles are reasonable; each
  cycle needs its own approval.
- **"Do not optimize indefinitely merely to beat a baseline"** and
  **"a well-designed negative result can be useful"** are applied
  literally: negative and null results are reported as results.
- **`research_advice.md` "the research topic is not fixed"** applies to
  project selection, not execution. After the paper is frozen, the topic
  is fixed for this skill.
- **Paper vs. mentor conflict.** If the paper's design conflicts with an
  explicit mentor principle in a way that affects validity or feasibility
  (e.g. the design requires building a new dataset or evaluation task that
  the paper did not budget; the baseline cannot be reproduced; the compute
  plainly exceeds the stated budget), do NOT silently change the
  experiment. Report the conflict before execution with the smallest
  correction, and wait for the user.

## Workflow

### Step 0: Read inputs

Read the mentor references, then the supplied paper completely
(including any `## Revision guide (not part of the paper)` section, which
holds the stop/pivot criterion and the negative-result meaning). Determine
RQk and the paper's folder (the **project folder**). Check whether
`experiment_plan_RQk.md`, `results_RQk.md` or `experiments_RQk/` already
exist there (see "Re-invocation").

For hardware, read only the global
`~/.claude/skills/compute-planner/references/compute.md` (single source of
truth; a project-local copy is never required or a fallback). If the plan
needs a GPU whose allocation is unverified there, run its day-0 test job
first rather than treating the GPU as unavailable. Report a confirmed
configuration to the user so it can be recorded under that file's
Confirmed User Access (edit that file only with the user's approval).

### Step 1: Extract the frozen experiment

Before writing any code, extract from the paper (quote or cite the paper
section for each item; mark `NOT STATED` if absent):

- research question
- hypothesis
- benchmark / dataset
- exact split (and filters, e.g. rows excluded)
- target labels
- model(s) or released outputs studied
- main method
- baseline (and its published values, with source)
- primary metric
- secondary metrics
- controls
- ablations
- statistical test (and CI method)
- success criterion
- stop/pivot criteria
- compute constraints
- explicitly planned analyses (tables, figures, sub-analyses the paper
  says it reports)

Then sort every item into exactly one bucket:

1. **Required experiment** — main method and baseline reproduction.
2. **Required controls/ablations** — only those the paper names.
3. **Required analysis** — metrics, statistical test, tables/figures and
   sub-analyses the paper names.
4. **Unresolved implementation details** — `TBD`, `[not yet specified:
   ...]`, or a choice the paper leaves open.
5. **Out of scope** — everything else, including anything mentioned in
   the paper only as future work, limitation, or "could".

Nothing goes into buckets 1–3 because it would make the study more
comprehensive. If the paper and its RQ/design file disagree on any frozen
item, list the drift; use the paper, and flag the drift if it affects
validity.

### Step 2: Resolve only blocking TBDs

Inspect every item in bucket 4. A TBD is **blocking** only if the frozen
experiment cannot be executed correctly without deciding it (e.g. fold
assignment seed, how duplicates are joined, item count after filtering).
TBDs that are measured results stay TBD — they are what the run produces.

For each blocking TBD, decide in this order of preference:

1. an explicit decision already present in the RQ/design file or archive;
2. mentor guidance;
3. benchmark conventions (official code/paper);
4. the simplest standard choice that preserves the research question.

Record each decision as: item, decision, source (1–4), reason.

Never turn an implementation detail into a new research question, a sweep,
or a comparison of options.

**Interpretation-changing choices.** If a choice could materially change
the scientific interpretation (e.g. which statistical test decides
"significant", the seed policy when variance matters, the definition of a
label or metric, an exclusion rule that removes many items, which model
variant is "the" model), do NOT choose silently. Mark it `FLAG`, propose
the default you would use and why, and stop before execution (Step 3
gate).

### Step 3: Write the bounded experiment plan

Create `experiment_plan_RQk.md` in the project folder:

```
# Experiment plan — RQk
Source paper: <path>   Source RQ/design file: <path or "not identified">
Mentor references read: <paths>
Created: <date>   Status: FROZEN

## 1. Frozen design (from paper)       ← Step 1 extraction, with section refs
## 2. Experiments to run               ← exact list, numbered E1, E2, ...
## 3. Controls / ablations to run      ← exact list, C1, A1, ... (paper-named only)
## 4. Analyses                         ← metrics, statistical test, tables/figures
## 5. Implementation decisions         ← Step 2 table (item, decision, source, reason)
## 6. Outputs to save                  ← exact file names and schemas
## 7. Pilot / sanity checks            ← Step 5 checks with pass conditions
## 8. Success criterion                ← verbatim from paper
## 9. Stop/pivot criteria              ← verbatim from paper
## 10. Seed policy                     ← from paper, or Step 2 decision
## 11. Estimated compute / time        ← per run and total; vs. paper's budget
## 12. Unresolved blockers / FLAGS     ← must be empty to execute
## 13. Paper–mentor conflicts          ← with smallest proposed correction
## 14. OUT OF SCOPE                    ← explicit list (bucket 5 + anything tempting)
## 15. Deviation log                   ← empty at creation; append-only
```

**Execution gate.** If section 12 or 13 is non-empty, or the estimated
compute exceeds the paper's stated budget, stop after writing the plan and
report the blockers to the user with the smallest correction for each. Do
not implement until the user resolves them. Record the user's decisions
in section 5 and then proceed.

**Freeze.** Once the gate is passed, the experiment set in sections 2–4
is frozen. From here, the only permitted additions are:

- (a) a fix needed because the planned experiment cannot be executed due to
  a technical or data error; or
- (b) a run strictly necessary to establish whether an existing result is
  valid (e.g. re-running after fixing a confirmed bug, a leakage check
  that the plan's sanity checks require);
- (c) a user-approved rerun with the smallest justified change, proposed
  under Step 9 after the frozen run. (c) is never self-authorised.

Even then, make the smallest possible change and append it to the
Deviation log (what, why, which of (a)/(b)/(c), what it changed; for (c)
also the user's approval and its date) BEFORE executing it. Never edit
sections 2–4, 8 or 9 in place after freezing.

### Anti-sprawl rule (mandatory)

**No experiment may be added merely because the current result is weak,
null, surprising, statistically insignificant, or inconsistent with the
working hypothesis.**

In particular, do not spontaneously add:

- another model;
- another dataset;
- another benchmark;
- another representation;
- another classifier;
- another seed beyond the pre-specified seed policy;
- another hyperparameter search;
- another ablation;
- another robustness check;
- another subgroup analysis;
- another metric;
- another statistical test.

A Step 9 proposal is not an addition: it modifies the existing method
minimally, is proposed once, and runs only after explicit user approval.

If one of these seems scientifically interesting but is not required by
the frozen plan, append it to `future_experiments_RQk.md` in the project
folder (one entry: idea, what prompted it, why it is not run now) and do
not run it. Writing an idea there is the complete response to it.

Before every run after the pilot, check: "Is this run listed in sections
2–3 of the frozen plan, or justified as (a)/(b) — or as a user-approved
(c) — in the Deviation log?" If not, do not run it.

### Step 4: Implement minimally

Put code and outputs in `experiments_RQk/` inside the project folder:

```
experiments_RQk/
  run.py (or a few small scripts)   ← only what the plan needs
  outputs/                          ← machine-readable results
  logs/                             ← stdout/stderr of each run
```

Implement only what the frozen plan requires. Prefer the smallest readable
implementation that:

- reproduces the benchmark labels and baseline correctly;
- runs the main experiment;
- runs the pre-specified controls and ablations;
- computes the pre-specified metrics and statistical test;
- saves reproducible outputs (fixed seeds, recorded versions, input file
  hashes or row counts).

Reuse benchmark code and released outputs where the paper says to.
Do not build frameworks, config systems, generalised experiment
infrastructure, dashboards, plotting suites, CLIs, or abstractions the plan
does not need. Do not refactor unrelated files. Stay inside the project
folder. Ask the user before downloading datasets, models or packages, and
before any run that needs paid API calls or GPU time beyond the plan's
estimate.

### Step 5: Validate before the full run

Run the smallest pilot/sanity check specified by the paper or plan section
7 (e.g. a small subset, or the baseline reproduction alone). Verify, as
applicable:

- row counts against the paper / benchmark documentation;
- label alignment (IDs join correctly; labels are the intended target);
- split integrity (no train/test or fold overlap);
- baseline reproduction against the published value, within the
  tolerance stated in the paper or RQ file (if none is stated, record the
  gap and treat a gap that would change the comparison's conclusion as a
  failure);
- absence of leakage (no item scored with its own label, no test
  information in fitting);
- output schema matches plan section 6.

Apply the paper's stop/pivot criteria to the pilot. If a validity check
fails: **stop**. Do not expand the experiment, change the method, or try
alternatives until something works. Report the failed check, the evidence,
and the smallest defensible fix; apply a fix only if it is a pure
technical/data correction (permitted addition (a)), log it, and re-run the
same pilot. Anything beyond that goes to the user.

### Step 6: Run the frozen experiment

Run exactly plan sections 2–4, once, under the seed policy.

- Do not alter the hypothesis, metric, success criterion, statistical
  test, or analysis after seeing results.
- Do not tune anything on the evaluation data that the plan does not tune.
- If a run crashes or produces invalid output, fix only the defect (log
  under (a)) and re-run that same run.
- A result that fails the success criterion is a result. Record it; do not
  search for a better experiment.
- Apply the stop/pivot criteria exactly as written. If they trigger,
  record that they triggered and what they prescribe; do not execute a
  pivot — report it to the user (Step 9).

### Step 7: Save results

Create `results_RQk.md` in the project folder (if it exists, use the next
unused `results_RQk_v2.md`, `_v3`, ...; never overwrite), with:

1. **Configuration** — exact code version/paths, commands, seeds, library
   versions, hardware, run time.
2. **Data / split** — files used, filters, final row counts per split.
3. **Implementation decisions** — copy of plan section 5 plus any user
   decisions.
4. **Main result** — primary metric for the method, with uncertainty.
5. **Baseline result** — reproduced value AND published value (with
   source), side by side, plus the gap.
6. **Controls / ablations** — each plan item, its result, uncertainty.
7. **Statistical test and uncertainty** — test, statistic, p-value/CI,
   exactly as pre-specified.
8. **Secondary metrics and planned analyses** — only those in the plan.
9. **Sanity checks** — each Step 5 check, PASS/FAIL, evidence.
10. **Failures and deviations** — copy of the Deviation log, crashed runs,
    anything not run and why.
11. **Success criterion** — verbatim, then MET / NOT MET / UNDETERMINED
    with the numbers that decide it.
12. **Stop/pivot criteria** — triggered or not, with evidence.
13. **Minimal interpretation** — Step 8.
14. **For paper-writer** — a table mapping each `TBD` in the paper (by
    section/table) to its measured value, or to "not measured: <reason>".

Label every number as one of: `MEASURED` (this run), `PUBLISHED` (with
source), `DECISION` (implementation decision), `INTERPRETATION`. Never
present a published number as measured or vice versa.

Also save machine-readable outputs in `experiments_RQk/outputs/` (e.g.
`results_RQk.json` with all headline numbers, per-item predictions/decisions
as CSV when the plan calls for them) and reference their paths in
`results_RQk.md`.

Do not edit the paper, the RQ file, or the archive.

### Step 8: Minimal interpretation

In `results_RQk.md` section 13, state only:

- whether the success criterion was met;
- whether the hypothesis was supported (supported / not supported /
  inconclusive), by the pre-specified test;
- whether the result is valid under the pre-specified checks;
- any limitation that directly changes the interpretation (e.g. baseline
  reproduction gap, flagged decision, failed check);
- post-experiment SOTA achievement, judged against the strongest
  comparable baseline, per the shared definitions §4c in
  `~/.claude/skills/research-pipeline/references/research_design_principles.md`:
  - ACHIEVED: beats it under the same protocol by at least the
    pre-registered SESOI, with the pre-registered statistical criterion
    met;
  - NOT ACHIEVED: the CI excludes a gain of at least the SESOI, or the
    method is worse;
  - INCONCLUSIVE: anything else.

  Name the task, the evaluated slice (if not the full benchmark), the
  baseline, the metric and the model or access class. A slice result is
  never stated as overall SOTA. This is separate from the pre-experiment
  SOTA potential and never inferred from it.

If the hypothesis was not supported, add a short diagnosis that uses only
outputs already computed under the plan, and point to the paper's Revision
guide / negative-result meaning where available. Do not write a new
research narrative and do not search for conditions under which the
hypothesis succeeds. Candidate follow-ups other than the single Step 9
proposal go to `future_experiments_RQk.md`.

### Step 9: Approval-gated small change (weak / null / surprising / negative result only)

This implements the mentor's diagnose → small justified change → rerun
advice without an autonomous loop.

1. **Diagnose** from existing outputs only (per-item predictions, control
   and ablation results, sanity-check evidence). No new runs, metrics,
   subgroup analyses or tests to diagnose.
2. **Propose at most ONE smallest justified change**, consistent with the
   mentor references: it preserves the core method concept, is motivated
   by the diagnosis (not by trying options until one works), keeps the
   benchmark, split, baseline, primary metric, success criterion and
   statistical test unchanged, and fits the remaining budget and the
   paper's stop/pivot criteria. If no change meets these conditions, say
   so and propose none. Write the proposal in `results_RQk.md` section 13
   (change, diagnosis that motivates it, expected compute, which plan items
   it re-runs).
3. **Stop and ask the user.** Do not run the change. A rerun requires the
   user's explicit approval in chat for that specific change; silence,
   general encouragement, or approval of an earlier change does not count.
4. **On approval**, BEFORE executing: append to the Deviation log of
   `experiment_plan_RQk.md` — type (c), the exact change, the reason
   (diagnosis), the user's approval and date, and which runs it repeats.
   Then rerun only those runs, with the same seed policy and analyses.
5. **Report the rerun separately.** The original frozen-run result stays
   the primary record and is never replaced or hidden. Save rerun outputs
   under a distinct name (e.g. `experiments_RQk/outputs/rerun1/`) and add
   them to the next unused `results_RQk_vN.md`, labelled as a post-hoc,
   user-approved deviation, alongside the original result.
6. If the rerun is still weak, null or negative, repeat from 1 only if the
   stop/pivot criteria and budget allow — each cycle needs a new explicit
   approval. Otherwise report the result as final for paper-writer.

## Re-invocation

- If `experiment_plan_RQk.md` already exists for the same paper, it is
  frozen: reuse it, do not regenerate or expand it. Continue from the
  first incomplete step.
- If the user supplies a newer paper version whose frozen design differs,
  create a new plan file (`experiment_plan_RQk_v2.md`, ...) and state the
  design differences explicitly. Never mix runs from two plans in one
  results file.

## Reply to the user

After finishing (or stopping at a gate), reply with:

- files created (plan, code, outputs, results, future_experiments);
- the selected RQ and the mentor reference files read (with paths);
- blocking TBDs resolved and how; FLAGS or conflicts raised;
- the main result vs. baseline, success criterion MET / NOT MET, and
  validity status — in a few lines;
- deviations from the plan, if any;
- if the result was weak/null/surprising/negative: the diagnosis and the
  single proposed change (or "none justified"), with an explicit request
  for approval — and a statement that nothing has been rerun;
- ideas deferred to `future_experiments_RQk.md`, if any;
- the next step: `/paper-writer <RQ_FILE> <paper_RQk_vN.md> RQk results:
  results_RQk.md`.

## Constraints

Do NOT:

- add experiments, models, datasets, benchmarks, representations,
  classifiers, seeds, hyperparameter searches, ablations, robustness
  checks, subgroup analyses, metrics, or statistical tests not in the
  frozen plan;
- change the hypothesis, metric, success criterion, or analysis after
  seeing results;
- enter an autonomous diagnose → modify → rerun loop, or run any changed
  method without the user's explicit approval and a prior Deviation-log
  entry;
- write, revise, or overwrite the paper, RQ file, or archive;
- modify paper-writer, research-readiness-advisor, benchmark-finder, or
  any other skill;
- substitute another paper or RQ version for the supplied one;
- fabricate, round favourably, or omit measured results;
- build infrastructure beyond what the plan needs;
- create, modify, or delete files outside the project folder.
