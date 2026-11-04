---
name: compute-planner
description: Estimate compute requirements, hardware fit, and whether a researcher at the user-specified experience level can finish the full research workflow within the user-specified project duration, plus a difficulty estimate for ordering projects.
---

# Compute Planner

Evaluate the compute requirements and hardware feasibility of a proposed
ML/LLM experiment, and estimate whether a researcher at the user-specified
experience level L can complete the WHOLE project (not just the GPU runs)
within the user-specified per-project duration D, and how difficult it is
for that researcher relative to other projects.

## Input

The user provides:
- Proposed experiment
- Model(s)
- Training or inference setup, if known
- Per-project duration D (user-specified; never assumed)
- Experience level L: Beginner / Intermediate / Advanced (user-specified;
  never assumed)
- When available (from benchmark-finder / the pipeline): Benchmark
  Readiness, code repository, published baseline, number of experimental
  conditions and seeds, API or closed-model dependencies, LLM-judge calls,
  and whether evaluation is automatic

Read the global compute file
`~/.claude/skills/compute-planner/references/compute.md`
(`C:\Users\<user>\.claude\skills\compute-planner\references\compute.md`)
for available compute resources. It is the single authoritative source
(its "Source of Truth" section). A project-local `compute.md` is only a
mirror: never required, never a fallback, and its absence, emptiness or
template text never implies missing GPU access. If the global file cannot
be read, report compute as UNKNOWN (not UNAVAILABLE) and ask the user.

If newer compute information is provided in the current conversation,
use the newer information instead.

## Workflow

### Step 1: Identify experiment requirements

Determine:
- Model(s)
- Parameter count
- Inference or training
- Full fine-tuning, LoRA/QLoRA, or no training
- Precision or quantization, if relevant
- Number of models loaded simultaneously
- Dataset size
- Number of experimental conditions
- Number of seeds/runs

Mark missing critical information as UNKNOWN.

### Step 2: Estimate compute requirements

Estimate:
- VRAM per model
- Total VRAM requirement
- Number of GPUs required
- System RAM requirement, if relevant
- Storage requirement, if relevant
- Approximate runtime, if reasonably estimable

Distinguish between:
- Minimum compute
- Recommended compute

Do not give unsupported precise estimates.
Use ranges when appropriate.

### Step 3: Compare with available hardware

Compare requirements with the global `compute.md` (Feasibility Rules).

Distinguish:

Hardware Fit:
Could the experiment run on known cluster hardware?

Documented Access:
Is the required partition documented as open to the user's account
category?

User Feasibility (Allocation Status):
CONFIRMED if a successful user job is recorded; otherwise UNKNOWN
(allocation unverified). Queue / wait time is KNOWN or UNKNOWN.

Never assume unrestricted access or guaranteed scheduling. Equally, never
treat unverified allocation or unknown queue time as UNAVAILABLE.
UNAVAILABLE requires positive evidence (hardware absent, documented
partition limits exceeded, or a required account the user does not hold).
Evaluate GPU designs by default, including single-GPU 7B–8B experiments
on H100, H200, A40 or V100.

### Step 4: Assign feasibility

Use:

EASY
- Comfortable compute margin
- Multiple runs/debugging practical
- Requires CONFIRMED access (a DOCUMENTED-AVAILABLE GPU design is rated
  FEASIBLE or RISKY on its margin)

FEASIBLE
- Fits available resources
- May require careful memory management

RISKY
- Near memory/runtime/allocation limits
- Limited debugging margin

IMPOSSIBLE
- Exceeds confirmed hard constraints

UNKNOWN
- Critical information is missing (unverified allocation or unknown
  queue time alone is not missing critical information; rate the design
  on Hardware Fit and record User Feasibility separately)

### Step 5: Suggest compute reductions

If necessary, consider:
- Smaller model
- LoRA/QLoRA
- Quantization
- Smaller batch size
- Smaller dataset
- Fewer conditions
- Fewer seeds
- Inference-only evaluation
- Existing checkpoints

Do not change the research question unless necessary.

### Step 6: Full-workflow duration feasibility at experience level L

D is the per-project duration the user specified (e.g. 1 week, 4 weeks).
It is a hard constraint taken from the user; never assume a default, and
never extend D to make a project fit. If D is not available, report
DURATION FEASIBILITY: UNKNOWN (D not specified) instead of guessing.

L is the experience level the user specified. If L is not available,
report DURATION FEASIBILITY: UNKNOWN (experience level not specified)
instead of guessing; never silently assume a level.

Estimate the COMPLETE workflow, not just compute, for a researcher at
level L. Short GPU runtime does NOT imply that the project fits D. The
question is not whether the experiment could theoretically finish within D,
but whether the complete project can realistically and reliably be
completed within D by a researcher at level L.

#### Experience levels

**Beginner**
- Can program independently and has basic Python/ML knowledge.
- Has limited experience reproducing unfamiliar research repositories.
- Has limited experience modifying benchmark/evaluation pipelines.
- Has limited experience debugging model-serving, dependency, GPU, and
  evaluation infrastructure.
- Has limited experience conducting and writing up an end-to-end research
  experiment.

**Intermediate**
- Has reproduced and modified several research repositories and benchmark
  or evaluation pipelines.
- Can usually debug common dependency, GPU, and model-serving problems
  without outside help.
- Has completed and written up at least one end-to-end research experiment.
- Has limited experience with specialised tooling they have not used
  before (e.g. model-parallel serving, interpretability hooks).

**Advanced**
- Routinely reproduces, modifies, and debugs research code and evaluation
  infrastructure, including multi-GPU execution and specialised tooling.
- Has conducted and written up multiple end-to-end research experiments.

#### How L changes the estimate

The experience level must materially change the phase estimates, not just
appear as a label.

**Familiarity is project-specific (all levels).** Reduce setup or learning
overhead only when the user has relevant experience with the specific type
of task, library, benchmark, or experimental workflow in this project.
General Python/ML experience does not imply familiarity with, for example:
unfamiliar research repositories, benchmark reproduction, Hugging Face
model evaluation, vLLM, Slurm, activation hooks, mechanistic
interpretability, unusual benchmark metrics, or research-paper writing.

At **Beginner** (someone who can program and understands basic ML, but has
limited experience completing an unfamiliar research project from benchmark
reproduction through a finished short paper), the estimate must:

1. Include time to understand unfamiliar repositories, benchmark protocols,
   evaluation scripts, and the relevant paper sections.
2. Include realistic dependency/environment setup and debugging overhead.
3. Check the actual repository before assigning setup or adaptation
   overhead. Size the overhead from verified evidence: a documented run
   command, example configs, pinned dependencies, released checkpoints,
   outputs or activations. Neither assume it runs unchanged nor assume it
   fails. An unverified incompatibility is a RISK with a mitigation, not
   guaranteed work.
4. Budget baseline reproduction from what is verified. Recomputing from
   released outputs or released per-item scores is cheap. Rerunning
   released code costs more. Re-implementing from scratch costs the most.
   A reproduction mismatch is a RISK, covered by contingency with a stated
   mitigation (e.g. fall back to the released number plus recomputation
   from released outputs). Do not add a failed attempt as planned work
   unless the evidence makes it likely (e.g. known open issues,
   unreleased checkpoints).
5. Include time to understand unfamiliar libraries or infrastructure before
   modifying them.
6. Include realistic analysis, sanity-checking, figure/table creation,
   interpretation, and research write-up time.

Beginner phase guidance (defaults; adjust from the actual project, see
"Estimate each project individually"):

- **Baseline reproduction** is not merely running released code. Include
  time to understand the benchmark's evaluation protocol, locate the exact
  evaluation split, understand preprocessing, reproduce the published
  metric, investigate discrepancies, and verify that the reproduced number
  is sufficiently close to the published baseline. Released outputs or
  predictions can substantially reduce this time, but the estimate still
  includes validating them.
- **Analysis**: about 0.5–1.0 working day by default when the project
  requires interpreting a new experimental result. This covers sanity
  checks, checking the metric implementation, comparing against the
  baseline, examining unexpected results, checking obvious failure cases,
  producing the main result table and the required ablation/control, and
  deciding what the result actually supports. A very simple deterministic
  post-processing experiment may use less, only when justified.
- **Writing a short paper (AI-drafted, human-verified)**: the ~4-page
  paper is drafted primarily by AI (paper-writer), so do **not** budget
  human drafting time. Budget the human **review and verification** work,
  about **0.5 working day at Beginner (range 0.5–0.75)**:
  - tracing every number to an output file;
  - checking every citation against its source;
  - checking that each claim matches the evidence and the pre-registered
    success, stop and SOTA criteria;
  - correcting figures, tables and captions;
  - checking limitations and integrity;
  - a final read.

  Use the upper end when there are many tables or a negative result
  requires a rewrite. Verification time is mandatory and is never cut to
  make a project fit. Review can overlap with background compute (count
  active time once). The default paper target is about four pages of main
  content plus references unless the user specifies another length.
- **Writing-first workflow**: if research-readiness-advisor recommends
  writing first, the same 0.5–0.75 day covers both reviews:
  - about 0.25 day to review the AI's pre-experiment full provisional
    draft (all sections including the Conclusion, with result cells TBD);
  - about 0.25–0.5 day to verify the AI's post-experiment result
    insertion and revision, including the rewritten Abstract, Results,
    Discussion and Conclusion if the intended result is not achieved.

  Do not double-count writing. Numerical results are never fabricated.
- **Reallocation rule**: the time saved by AI drafting goes to the
  research: the diagnostic that tests the causal hypothesis, the controls
  and the reviewer pre-mortem experiment (shared definitions §4e). It
  never goes to extra optional scope.

At **Intermediate**, keep Beginner items 2–4 and 6 (repositories still
usually need fixes, reproduction may still need a retry, and analysis
includes the same checks), but reduce learning overhead (items 1 and 5),
and analysis or writing time, only for the specific kinds of task,
tooling, benchmark, and write-up the researcher has actually done before.
The Beginner analysis and writing defaults are not applied automatically;
estimate them from the project and the researcher's relevant experience.

At **Advanced**, learning and setup overhead apply mainly to genuinely
unfamiliar codebases and tooling; reproduction, analysis, and debugging
still carry their project-specific risk, and writing still requires real
time even if less than at Beginner.

Beginner describes experience, not the project's technical ceiling
(shared definitions §2). GPU, fine-tuning, activation analysis,
mechanistic interpretability and white-box projects are never excluded
because of L. They are estimated from verified tooling.

At every level, record the factors below as RISK entries, each with a
probability (low / medium / high) and a mitigation. Widen the range only
where verified evidence (missing configs, unreleased checkpoints, known
open issues) makes the extra work likely. A speculative failure is
covered by contingency, not added as work. Factors:

- unfamiliar research repositories;
- multi-GPU / model-parallel execution;
- 70B-class models;
- activation hooks or mechanistic interpretability tooling;
- external judge / API pipelines;
- complicated output parsing;
- fragile or difficult-to-reproduce published effects;
- multiple interacting frameworks or repositories.

Learning overhead for genuinely unfamiliar tools is largest at Beginner,
smaller at Intermediate, and smallest at Advanced. Count it once, in the
phase where it occurs. Fragile effects and external APIs always get a
RISK entry.

A project must fit D at the selected level L. A project that would fit for
a more experienced researcher but not at level L is DOES NOT FIT DURATION
for this run. Never use a more experienced level than L to estimate, and
never shrink an estimate merely to make a project fit D; if it does not
fit, propose redesign options (below).

The goal is realistic, not pessimistic, estimates. Do not inflate every
phase mechanically, and do not stack pessimistic assumptions. Do not
assume any of the following without verification:
- GPU setup takes a full day;
- baseline reproduction fails;
- every model must be downloaded from scratch;
- existing implementations cannot be reused;
- the full benchmark must be evaluated, when a pre-specified slice
  answers the question.

Verify the available resources and code first. Label every phase
estimate:
- **VERIFIED:** checked against the repository, dataset, model card,
  released outputs or compute documentation.
- **ESTIMATE:** reasoned from verified facts.
- **RISK:** speculative, with a probability and a mitigation.

See shared definitions §5
(`~/.claude/skills/research-pipeline/references/research_design_principles.md`).

#### Estimate each project individually

- Estimate every phase from the actual project. Do not reuse a fixed
  template of near-identical phase values across unrelated projects just
  because they share an experience level.
- State the main project-specific sources of uncertainty.
- Use working days, and convert D to working days (1 week = 5 working days
  unless the user states otherwise).
- Round to meaningful units (0.25 or 0.5 working day). Report e.g.
  "Expected work: ~3.5 days" and "Conservative range: 3–4 days", never
  false precision such as "3.475 days".

#### Work, contingency, and total budget are separate

- Estimated work: the range of planned working time across all phases.
  Expected work is its central value; the conservative upper bound is its
  upper end.
- Required contingency: reserve time sized to the one or two most likely
  RISK entries (no fixed percentage, and not the sum of every conceivable
  failure). At Beginner it must absorb at least the single most likely
  plausible failure, such as a baseline mismatch, a dependency issue, an
  incorrect metric implementation, an unexpected data format, a method
  implementation bug, or an uninterpretable result. Each risk has a stated
  mitigation.
- Total budget required = expected work (active time, buckets 1–4) +
  required contingency. The conservative upper bound of work is reported
  separately, and must itself be at most D (the contingency is what
  absorbs the gap between expected and conservative work; do not count
  that gap twice).

Report the estimate in the five buckets of shared definitions §5:
1. essential implementation;
2. compute (active work vs wall-clock; background compute overlapping
   with writing or analysis is not counted twice);
3. evaluation and statistics;
4. paper writing;
5. contingency.

These buckets are in addition to the phase table below.

Contingency is not working time: never list it as a planned task and never
count unused contingency as research work.

#### Standalone first

Every feasibility verdict is based on the STANDALONE estimate, assuming no
setup carried over from another *planned* project in this portfolio. A
shared-setup estimate (e.g. "duration if run after Project X with
reusable setup") may be reported afterwards as additional information,
but a project is never labeled as fitting D solely because another
planned project would be completed first.

Standalone does **not** exclude assets that already exist and are
VERIFIED. These count toward the standalone estimate:
- public code, released models, adapters, outputs and activations;
- the user's existing local code, environments, cached weights or
  confirmed compute allocations, when they are verified to exist now.

Estimate time (in working days, as a range) for each phase, at level L:

| Phase | What drives it |
|---|---|
| Understanding the benchmark and relevant prior work | paper length and clarity, protocol complexity, amount of related work. When prior-work-checker's Evidence Report exists, size this phase by human verification of that report (the cited sections of the three closest papers and the baseline number). Do not size it as a fresh literature review. The agent-run literature stages belong to the planning budget, not to D, and are not counted twice |
| Environment setup | repo quality, dependency pinning, infrastructure / cluster setup |
| Baseline reproduction | evaluation protocol, exact split, preprocessing, reproducing and validating the published metric, investigating discrepancies; released outputs reduce but do not remove validation |
| Implementation of the change | lines of code touched, number of components modified |
| Debugging and failed runs | engineering complexity, number of interacting parts |
| Experiments | runtime × conditions × seeds, training vs. inference, queue time |
| External dependencies | API access, rate limits and cost, closed models, LLM-judge calls |
| Analysis / sanity checks | sanity checks, metric-implementation checks, baseline comparison, unexpected results, failure cases, main table, ablation/control, deciding what the result supports |
| Figures and tables | number of results tables and plots |
| Writing / revision | AI-drafted ~4-page paper; human time covers only review and verification: number tracing, citation checks, claims vs evidence and pre-registered criteria, captions, limitations, final read (≈ 0.5 day at Beginner) |

Explicitly account for: reproduction risk, engineering complexity, training
requirements, number of experimental conditions and seeds, API dependencies,
judge calls, infrastructure setup, likely debugging time, and the
level-L learning overhead and uncertainty factors above. Mark any phase
whose inputs are missing as UNKNOWN rather than guessing.

Classify against D:

- FITS DURATION, when all three hold (evaluated at level L):
  - the STANDALONE total budget (expected active work for the complete
    workflow plus the required contingency) is at most D. The complete
    workflow is: understanding what the design needs, setup, baseline
    reproduction on the evaluated slice, implementation, debugging,
    experiments, evaluation and statistics, figures/tables, and writing
    the required paper;
  - the conservative work bound is at most D;
  - the critical-path wall-clock (including compute that cannot overlap
    with other work) is at most D.
- DOES NOT FIT DURATION: anything else, including projects that fit only
  if every RISK fails to materialise (i.e. no contingency left), projects
  that fit only with setup from another planned project, and projects that
  would fit only for a more experienced researcher than L. Before this
  verdict is final, apply the scope levers (shared definitions §6) and
  re-estimate.

Short-sprint rule: expected active work should leave the contingency the
top risks need.
- **D = 4 working days:** expected work of about 3–3.5 days, with
  0.5–1 day of contingency.
- **D = 5:** about 3.5–4 days of expected work.

A worked 4-day profile is in shared definitions §5. Estimate each project
from its own verified requirements, not from the profile.
- UNKNOWN: critical inputs (or D, or L) are missing. State exactly what is
  missing.

User Feasibility = UNKNOWN (unconfirmed GPU access) does not by itself make
Duration Feasibility UNKNOWN, and is not by itself a reason to reject.
Estimate runtime on the configuration that has Hardware Fit, record the
access as a RISK, and give a concrete mitigation:
- a day-0 test job on a documented all-account partition;
- an alternative partition or GPU type (share, ampere, dgxh, dgx2,
  preempt);
- pre-downloading weights while other work proceeds;
- a named smaller fallback model or quantised variant that keeps the
  mechanism.

Favour projects that reuse existing repositories, released models,
outputs or activations, published baselines and automatic evaluation.
Fine-tuning (e.g. LoRA), activation extraction and white-box analysis are
acceptable when the verified tooling and a scoped design fit D.

If the verdict is DOES NOT FIT DURATION, name the limiting phase(s) and
propose redesign options in this order, each with its re-estimated total:

1. Optimise scope while keeping the mechanism and a meaningful,
   technically deep contribution (shared definitions §6):
   - narrow to the pre-specified documented failure slice;
   - reuse released code, models, adapters, outputs or activations;
   - cut optional models, layers, seeds and conditions;
   - choose a smaller intervention that keeps the mechanism (e.g. a probe
     on frozen activations instead of fine-tuning);
   - use existing checkpoints, an automatic metric instead of a judge, or
     drop an API dependency.
2. Use a more appropriate established benchmark, setting or baseline for
   the same mechanism.
3. Reformulate the question around a smaller experiment.
4. Replace it with a different benchmark-centered research question.

For every option, state the binding bucket it relieves and give the
re-estimated total. If even the best option does not fit, state the
**minimum verified additional time or resource** that would make it fit.

compute-planner proposes and re-estimates options 1–3 and flags when only
option 4 remains; research-planner decides and routes changed or
replacement questions back through benchmark-finder and prior-work-checker.
compute-planner re-estimates every replacement candidate against D at
level L.

### Step 7: Difficulty estimate at level L (for ordering)

Produce a difficulty estimate, for a researcher at level L, that downstream
skills use to order projects from easiest/fastest to hardest/slowest:

- Experience Level Used: L
- Standalone Expected Work: central value of the level-L standalone work
  estimate from Step 6 (rounded, e.g. ~3.5 days)
- Standalone Conservative Range: the level-L standalone work range. Its
  upper end must be ≤ D. Expected work plus the required contingency is
  the total budget used for FITS DURATION (Step 6).
- Level-Specific Difficulty: LOW / MEDIUM / HIGH for a researcher at
  level L, with a one-line reason
- Learning Overhead: days spent understanding unfamiliar repositories,
  protocols, scripts, libraries, infrastructure, and paper sections at
  level L
- Setup / Reproduction Risk: LOW / MEDIUM / HIGH at level L, with the
  driving factor (e.g. unpinned dependencies, multi-GPU serving, fragile
  published effect)
- Execution Risk: LOW / MEDIUM / HIGH (driven by reproduction risk,
  debugging exposure, external dependencies, and the level-L uncertainty
  factors)
- External Dependencies: count of APIs, closed models, judge models, or
  non-public resources required
- Difficulty Drivers / Main Reason for the Estimate: the 1–3 phases or
  factors that dominate the estimate at level L

The same project may have a different difficulty and a different order at
different experience levels; always use level L.

Base difficulty only on execution effort and completion time. Never base it
on research importance, novelty, conceptual interest, or the original order
of the questions.

## Output

| Field | Result |
|---|---|
| Model | |
| Model Size | |
| Workload | |
| Training Method | |
| Precision | |
| Estimated VRAM | |
| GPUs Required | |
| Estimated Runtime | |
| Minimum Compute | |
| Recommended Compute | |
| Hardware Fit | |
| Documented Access | |
| User Feasibility (Allocation Status) | |
| Queue / Wait Time | |
| Main Bottleneck | |
| Recommended Modification | |

Standalone workflow estimate at experience level L (working days, rounded
to 0.25 or 0.5; estimated from this project, not a template):

| Phase | Estimated work (range) | Project-specific notes / uncertainty |
|---|---|---|
| Understanding / reading | | |
| Setup | | |
| Baseline reproduction | | |
| Implementation | | |
| Debugging | | |
| Experiments | | |
| Analysis / sanity checks | | |
| Figures / tables | | |
| Writing / revision | | (if writing-first: full provisional draft + post-experiment results/revision, split of the same budget) |
| External dependencies (API / judge) | | |
| **Estimated work (total)** | | |
| Required contingency (not work) | | (which plausible failure(s) it covers) |
| **Total budget required** | up to … | (expected active work + contingency; the conservative work bound must also be ≤ D) |

Label each phase row VERIFIED / ESTIMATE / RISK. Also give the five-bucket
summary (shared definitions §5):

| Bucket | Active work | Wall-clock | Label | Notes |
|---|---|---|---|---|
| 1. Essential implementation | | | | |
| 2. Compute | | | | (background compute overlapping other work counted once) |
| 3. Evaluation and statistics | | | | |
| 4. Paper writing | | | | |
| 5. Contingency | | | | (top 1–2 risks, each with its mitigation) |

| Risk | Probability | Mitigation | Covered by |
|---|---|---|---|

| Field | Result |
|---|---|
| Experience Level | (L, as specified by the user) |
| Per-Project Duration (D, working days) | (as specified by the user) |
| Standalone Expected Duration | e.g. ~3.5 days of work |
| Standalone Conservative Duration Range | e.g. 3–4 days of work |
| Required Contingency | e.g. 1 day |
| Total Budget Required | e.g. up to 5 days |
| Main Uncertainty Drivers | |
| Level-Specific Difficulty | LOW / MEDIUM / HIGH, with reason |
| Learning Overhead | (days) |
| Setup / Reproduction Risk | LOW / MEDIUM / HIGH, with driver |
| Main Reason for the Estimate | |
| Duration Feasibility | FITS DURATION / DOES NOT FIT DURATION / UNKNOWN (standalone, at level L) |
| Duration With Reused Setup (optional) | e.g. "after Project X: ~3 days of work" (information only; never the basis of the verdict) |
| Limiting Phase | |
| Redesign Options (if DOES NOT FIT) | (in order 1–4, each with re-estimated total at level L) |
| Execution Risk | LOW / MEDIUM / HIGH |
| External Dependencies | |
| Difficulty Drivers | |