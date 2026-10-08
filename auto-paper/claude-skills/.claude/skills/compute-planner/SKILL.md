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

Read `references/compute.md` for available compute resources.

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

Compare requirements with `references/compute.md`.

Distinguish:

Hardware Fit:
Could the experiment run on known cluster hardware?

User Feasibility:
Is the user confirmed to have access to the required hardware?

Never assume that cluster-wide hardware is accessible to the user.

### Step 4: Assign feasibility

Use:

EASY
- Comfortable compute margin
- Multiple runs/debugging practical

FEASIBLE
- Fits available resources
- May require careful memory management

RISKY
- Near memory/runtime/allocation limits
- Limited debugging margin

IMPOSSIBLE
- Exceeds confirmed hard constraints

UNKNOWN
- Critical information is missing

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
3. Not assume that a public repository runs successfully without
   modification.
4. Not assume baseline reproduction works on the first attempt; include at
   least one failed or mismatched reproduction attempt.
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
- **Writing a short paper**: about 1.0–1.5 working days by default, unless
  there is concrete project-specific evidence that less is sufficient.
  Writing covers the outline; Abstract, Introduction, Related Work, Method,
  Experiment, Conclusion; integrating real citations; checking references;
  turning results into tables; figure/table captions; revising claims to
  match the actual results; basic LaTeX formatting; and final consistency
  checking. AI may assist drafting, but AI-generated text does not
  eliminate these tasks, and an AI-assisted or auto-paper workflow does not
  make writing nearly automatic. If the user explicitly says only a
  research note (not a short paper) is required, a smaller writing estimate
  may be used. The default paper target is about four pages of main content
  plus references unless the user specifies another length.
- **Writing-first workflow**: if research-readiness-advisor recommends
  writing first, the estimate must include both the pre-experiment full
  provisional paper draft (all sections including the Conclusion, with
  result cells TBD) and the post-experiment result insertion and revision
  (including rewriting the Abstract, Results, Discussion, and Conclusion if
  the intended result is not achieved). Both are split from the SAME
  writing budget, estimated from the project, e.g. pre-experiment draft
  ~0.75 day + post-experiment results and revision ~0.5 day = 1.25 days
  total. Do not double-count writing. Numerical results are never
  fabricated.

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

At every level, increase the uncertainty (widen the range, and raise the
conservative upper bound) for projects involving:

- unfamiliar research repositories;
- multi-GPU / model-parallel execution;
- 70B-class models;
- activation hooks or mechanistic interpretability tooling;
- external judge / API pipelines;
- complicated output parsing;
- fragile or difficult-to-reproduce published effects;
- multiple interacting frameworks or repositories.

The increase is largest at Beginner, smaller at Intermediate, and smallest
at Advanced, but never zero for fragile effects or external APIs.

A project must fit D at the selected level L. A project that would fit for
a more experienced researcher but not at level L is DOES NOT FIT DURATION
for this run. Never use a more experienced level than L to estimate, and
never shrink an estimate merely to make a project fit D; if it does not
fit, propose redesign options (below).

The goal is realistic, not pessimistic, estimates. Do not inflate every
phase mechanically. A simple project using released outputs and standard
Python / scikit-learn may still fit comfortably within five working days at
Beginner. Projects involving unfamiliar repositories, GPU inference, model
serving, multi-GPU execution, activation hooks, external APIs, fragile
baseline reproduction, or complicated evaluation get appropriately wider
and higher estimates.

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
- Required contingency: reserve time for things going wrong, sized from the
  project's actual risks and the level-L uncertainty factors (no fixed
  percentage). At Beginner it must be enough to absorb at least one
  plausible failure, such as a baseline mismatch, a dependency issue, an
  incorrect metric implementation, an unexpected data format, a method
  implementation bug, or an experiment producing an uninterpretable result.
- Total budget required = conservative upper bound of estimated work +
  required contingency.

Contingency is not working time: never list it as a planned task and never
count unused contingency as research work.

#### Standalone first

Every feasibility verdict is based on the STANDALONE estimate, assuming no
setup carried over from any other project. A shared-setup estimate (e.g.
"duration if run after Project X with reusable setup") may be reported
afterwards as additional information, but a project is never labeled as
fitting D solely because another project was completed first.

Estimate time (in working days, as a range) for each phase, at level L:

| Phase | What drives it |
|---|---|
| Understanding the benchmark and relevant prior work | paper length and clarity, protocol complexity, amount of related work |
| Environment setup | repo quality, dependency pinning, infrastructure / cluster setup |
| Baseline reproduction | evaluation protocol, exact split, preprocessing, reproducing and validating the published metric, investigating discrepancies; released outputs reduce but do not remove validation |
| Implementation of the change | lines of code touched, number of components modified |
| Debugging and failed runs | engineering complexity, number of interacting parts |
| Experiments | runtime × conditions × seeds, training vs. inference, queue time |
| External dependencies | API access, rate limits and cost, closed models, LLM-judge calls |
| Analysis / sanity checks | sanity checks, metric-implementation checks, baseline comparison, unexpected results, failure cases, main table, ablation/control, deciding what the result supports |
| Figures and tables | number of results tables and plots |
| Writing / revision | the required paper (default ~4 pages + references); outline, all sections, real citations, reference checks, captions, revising claims to match results, LaTeX, consistency check |

Explicitly account for: reproduction risk, engineering complexity, training
requirements, number of experimental conditions and seeds, API dependencies,
judge calls, infrastructure setup, likely debugging time, and the
level-L learning overhead and uncertainty factors above. Mark any phase
whose inputs are missing as UNKNOWN rather than guessing.

Classify against D:

- FITS DURATION: the STANDALONE total budget required (conservative upper
  bound of estimated work for the complete workflow — understanding the
  benchmark and relevant prior work, reproducing the baseline,
  implementation, debugging, experiments, analysis, figures/tables, and
  writing the required paper — plus the required contingency) fits within
  D. All of this is evaluated at the selected experience level L.
- DOES NOT FIT DURATION: anything else, including projects that fit only if
  reproduction and debugging go smoothly, projects that fit only with setup
  reused from another project, and projects that would fit only for a more
  experienced researcher than L. "Risky but possible" counts as DOES NOT
  FIT.

Five-day rule: when D is 1 week = 5 working days, do not plan about five
full days of expected work. At Beginner, expected work should normally be
at most about 3.5–4 working days, leaving the rest for uncertainty and
recovery. A Beginner project whose realistic conservative workload reaches
about 5 days is normally DOES NOT FIT DURATION; an exception requires
explicit justification from unusually low execution risk. For other values
of D apply the same principle: conservative work plus required contingency
must fit D.
- UNKNOWN: critical inputs (or D, or L) are missing. State exactly what is
  missing.

User Feasibility = UNKNOWN (unconfirmed GPU access) does not by itself make
Duration Feasibility UNKNOWN: estimate runtime on the configuration that has
Hardware Fit, and note the access assumption.

Strongly favor projects that are simple benchmark extensions with existing
repositories, published baselines, automatic evaluation, minimal code
modification, and inference-only experiments.

If the verdict is DOES NOT FIT DURATION, name the limiting phase(s) and
propose redesign options in this order, each with its re-estimated total:

1. Simplify the experiment while keeping a meaningful contribution (fewer
   conditions or seeds, smaller model, inference-only, existing
   checkpoints, automatic metric instead of a judge, dropping an API
   dependency).
2. Use a simpler established benchmark or baseline for the same question.
3. Reformulate the question around a smaller experiment.
4. Replace it with a different benchmark-centered research question.

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
- Standalone Conservative Range: the level-L standalone work range, whose
  upper end plus the required contingency is the total budget used for
  FITS DURATION
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
| User Feasibility | |
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
| **Total budget required** | up to … | (conservative work + contingency) |

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