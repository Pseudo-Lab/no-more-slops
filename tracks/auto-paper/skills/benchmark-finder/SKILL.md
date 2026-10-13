---
name: benchmark-finder
description: Find established benchmarks, datasets, prior work, and literature gaps for one or more research questions, and build a persistent benchmark-centered prior-work archive (prior_work_<benchmark>.md) once a benchmark is provisionally confirmed.
---

# Benchmark Finder

## Reference Guidance

`references/research_advice.md` (in this skill's directory) is the PRIMARY
and HIGHEST-PRIORITY research-planning reference for this project.

Read it before benchmark search and selection.

When there is a conflict between preserving an original research idea, the
default behavior of this skill, or general project-planning heuristics, and
the guidance in `research_advice.md`, FOLLOW `research_advice.md`.

It is mentorship/project-selection guidance, not scientific evidence.
It must NOT be used as evidence that:
- a literature gap exists
- a contribution or research question is novel
- a benchmark is scientifically established
- a scientific claim is true

Those claims still require verified literature or benchmark evidence.

Priority order:
1. `research_advice.md` for research strategy and project-selection principles
2. Verified benchmark/literature evidence for scientific claims
3. User-provided constraints such as time and compute
4. Original research ideas as candidate interests, unless the user
   explicitly says a topic is fixed

## Strict Benchmark Definition

An established benchmark must normally have ALL of:

1. a clearly defined task/problem,
2. an existing public dataset or standardized evaluation set,
3. a defined evaluation protocol,
4. established evaluation metric(s),
5. at least one published baseline or prior result that can be reproduced
   or compared against.

A paper, framework, related dataset, or vaguely similar evaluation is NOT
automatically a benchmark. A benchmark must support the proposed experiment
directly.

Classify every candidate, relative to the question it is meant to support, as:

- EXACT / DIRECT BENCHMARK: meets the definition above AND directly evaluates
  the problem in the question, using its existing task, data, protocol and
  metric without inventing anything new.
- PROXY BENCHMARK: an established benchmark that evaluates a related but
  different problem.
- RELATED DATASET: data relevant to the topic that lacks a defined task,
  protocol, metric, or baseline (i.e. not a benchmark).
- NO BENCHMARK: none of the above found.

Only EXACT / DIRECT counts as benchmark support. PROXY BENCHMARK and RELATED
DATASET are reported for traceability only and never count as support.

Never describe a candidate as benchmark support using phrases such as
"close benchmark", "closest benchmark", "reasonable proxy", "can be adapted",
"could construct a benchmark from...", or "we can derive a new task from this
dataset". If supporting the question would require inventing a new task,
dataset, evaluation protocol, or metric, it is NOT an exact benchmark.

### SAME-TASK test (required for EXACT / DIRECT)

A benchmark may be classified as EXACT / DIRECT only if the proposed main
experiment uses the benchmark's established task and evaluation protocol
directly. Answer each question explicitly:

A. Is the proposed prediction/decision task already defined by the
   benchmark?
B. Is the benchmark's existing evaluation set used?
C. Are the benchmark's established metrics used as the MAIN metrics?
D. Can the proposed method be compared directly with an existing published
   baseline on those metrics?
E. Does the experiment avoid defining a new target variable, derived task,
   custom main metric, or new evaluation protocol?

If any of A-D is NO, the benchmark is not EXACT.
If E is NO, the benchmark is not EXACT unless the new component is purely
secondary analysis and the main benchmark comparison remains unchanged.

Derived tasks are never exact. A dataset whose observations allow a new
prediction problem to be created is NOT an exact benchmark for that new
problem. For example:

existing dataset
→ derive a new binary label
→ predict that label
→ introduce AUROC as the evaluation metric

must NOT be classified as EXACT unless that prediction task and metric
already exist in the benchmark literature. Classify such cases as RELATED
DATASET or PROXY BENCHMARK.

### Comparability check (required for EXACT / DIRECT)

Before classifying a benchmark-direction pair as EXACT, verify that this
table could be produced without inventing a new primary task or metric:

| Method | Established Benchmark Metric |
|---|---|
| Published baseline | reported score |
| Reproduced baseline | reproduced score |
| Proposed method | experimental score |

If this table is not conceptually valid, reject the benchmark-direction
pair.

### Benchmark validity check (required for EXACT / DIRECT)

Passing the SAME-TASK test is necessary but not sufficient. A benchmark that
is merely related to the topic is not accepted. For the candidate research
question, answer each explicitly (YES / NO / UNKNOWN, with a one-line
justification):

V1. Phenomenon: does the benchmark directly instantiate the phenomenon named
    in the research question (not a neighbouring phenomenon)?
V2. Metric: does the benchmark's main metric directly measure the outcome
    the research question claims (not a correlate of it)?
V3. Evidence: would a positive result AND a negative result each provide
    evidence about the research question, rather than being explainable by
    something else the benchmark happens to measure?
V4. Implementation: does the benchmark have an established, public
    implementation and, preferably, a published numerical baseline?

If any of V1–V3 is NO, there is a mismatch. Either:
- rewrite the research question so that it asks exactly what the benchmark
  and metric measure (then re-run SAME-TASK, comparability, and V1–V4), or
- find a better benchmark for the question.

Never keep a mismatched benchmark-question pair. If V4 is NO, the benchmark
is not EXACT. If V4 has an implementation but no published number, report
that so prior-work-checker can attempt to trace one.

Do not lower this standard to preserve topical similarity.

## Research Question Format Rule

Every research question this skill reports (the reformulated question for
an exact benchmark, and every replacement or generated question) must:

1. Be a single interrogative sentence that ends with "?".
2. Start with an interrogative form (Does / Do / Is / Are / Can / Will /
   Which / How much / To what extent ...).
3. Not be an imperative, a noun phrase or title, a hypothesis statement,
   or a method description.
4. Contain exactly one question.
5. Name the proposed change, the comparison baseline, the benchmark, and
   the main metric, e.g. "Does <change> <increase / reduce> <metric> on
   <benchmark> compared with <baseline>?"
6. Be answerable directly from the benchmark results table.

Check every reported question against rules 1–6 before output.

## Hand-off to prior-work-checker

Every slot with an EXACT / DIRECT benchmark is passed to prior-work-checker
immediately after this skill. It traces the prior work and baselines that
use the benchmark, and returns PASS or FAIL.

### Regeneration request (after a prior-work FAIL)

When prior-work-checker returns FAIL for a slot, it sends back:
- the failed research question,
- the FAIL reason (ALREADY-DONE / SUBSTANTIALLY-ANSWERED / NO-BASELINE /
  UNVERIFIED / FORMAT),
- the prior work that blocked it,
- all earlier failed questions for the slot.

Then:

1. Keep the same slot ID.
2. Generate ONE new research question in question format that excludes
   every failed question and every comparison already performed by the
   cited prior work. Cosmetic rewording of a failed question, renaming the
   same intervention, or changing only a minor protocol detail (seed,
   prompt wording, split, model size within the same family) does not
   count as new.
3. Prefer, in order:
   a. a different small change on the same exact benchmark, avoiding the
      blocking work;
   b. a different exact benchmark for the same target behaviour;
   c. progressively farther topics (same search order as Step 3b).
4. Re-run the SAME-TASK test, comparability check, and benchmark validity
   check (V1–V4) on the new pair.
5. Return it to prior-work-checker as the next iteration.

If the exhaustive replacement search has no remaining non-excluded exact
candidate, report this so the pipeline can mark the slot
"UNRESOLVED — NO DIRECTION PASSED THE PRIOR-WORK CHECK". Never weaken the
benchmark standard to escape the loop.

## Modes

### Fixed-Topic Mode

Use only when the user explicitly wants a particular research question
preserved. Search for an EXACT / DIRECT benchmark for that question. Do not
replace the question. If none exists, report "UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND" clearly; do
not substitute a proxy as support.

Fixed-topic cardinality conflict (K = number of user-designated fixed
topics, N = requested output cardinality):

- If K <= N: search fixed topics first; the remaining N - K slots are
  screened or generated normally.
- If K > N: do NOT silently discard fixed topics and do NOT increase N
  automatically. Report:

  "You requested N research directions, but marked K topics as fixed (K > N)."

  and ask the user to either (1) increase N to at least K, or (2) specify
  which fixed topics should be prioritized. Benchmark search on the fixed
  topics may be reported, but do not perform final selection until the
  conflict is resolved.

### Benchmark-First Mode (default)

The original question is a seed, not a commitment. Controlled topic drift,
including substantial drift, is explicitly allowed.

benchmark-finder does not set the output cardinality N; the pipeline does
(user-provided N, otherwise N = number of parsed ideas). benchmark-finder
supports it in two ways:

- Screening: evaluate every parsed idea (RQ1 ... RQm) so the pipeline can
  select the most promising starting points when m > N, primarily by exact
  benchmark availability and research feasibility.
- Generation: when the pipeline needs more directions (m < N), find
  additional benchmark-backed directions near the user's broad research
  themes, each with the next unused identifier (RQm+1, ...) and the theme
  or RQ that inspired it. Generated directions must pass the same
  exact-benchmark validation. Never weaken the standard to reach N.

For each idea or slot:

1. Search for an EXACT / DIRECT established benchmark for the original
   question (passing the SAME-TASK test, comparability check, and
   benchmark validity check V1–V4).
2. If one exists, report it so the question can be reformulated around it.
3. If only a PROXY BENCHMARK or RELATED DATASET exists, or the candidate
   fails the SAME-TASK test or comparability check, do NOT force the
   original question onto it. Keep the slot ID and report:
   "Original direction rejected: no exact established benchmark found."
4. Then search progressively farther from the original topic (nearby
   problem in the same target behavior → same broad research area →
   adjacent areas) until a direction passes exact-benchmark validation,
   with reproducible baselines, a clear metric, a plausible literature gap,
   and room for a small method modification or controlled experiment.
5. Report one best replacement benchmark per slot under the SAME slot ID
   (alternatives may be listed as backups), and the problem it directly
   evaluates.

Prioritize benchmarks with:
- public dataset
- public evaluation code
- established evaluation metric
- reproducible baseline
- minimal preprocessing
- minimal custom infrastructure
- accessible compute requirements
- short baseline reproduction time
- room for one small, interpretable modification
- interpretable positive AND negative results

Do not treat "closest conceptual match to the original question" as the
best benchmark. A benchmark that is EXACT for a nearby problem and highly
executable is preferable to a proxy for the original problem.

Explicitly distinguish:
- A. Scientific benchmark support (EXACT / DIRECT / PROXY BENCHMARK /
  RELATED DATASET / NO BENCHMARK; see Step 3)
- B. Benchmark readiness for a short project (see Benchmark Readiness in
  Step 4)

Benchmark readiness never upgrades the classification.

### Step 1: Define the task

For each research question (or seed direction, in benchmark-first mode),
identify:

- Input
- Output
- Target behavior
- Evaluation metric
- Research category


### Step 2: Find benchmark sources

Before searching for individual benchmarks, identify which benchmark
discovery sources are relevant to the research question.

Search sources in this order:

1. Benchmark sources explicitly provided by the user
2. Relevant resources in `references/benchmark_resources.md`
   (in this skill's directory, `benchmark-finder/references/`)
3. Broader web/literature search

The reference file is a prioritized search starting point, NOT an exhaustive
or exclusive list. Do not assume that a resource listed there is relevant:
select resources based on the research question, and skip the rest.
If the file contains no links yet, say so and continue with the other tiers.

Resources may include websites, benchmark collections, dataset repositories,
evaluation frameworks, leaderboards, survey papers, GitHub repositories,
papers, or other benchmark discovery resources.

Beyond provided and recommended resources, also consider:
- Benchmark/evaluation frameworks
- Benchmark leaderboards
- Dataset repositories (e.g. Papers With Code, Hugging Face Datasets)
- Benchmark survey or review papers
- Curated benchmark collections (e.g. Stanford HELM)
- Repositories from established research groups

Do not rely on any example list exclusively.
Search for sources specifically relevant to the research question.

Report:
- Source name
- Source type
- URL
- Why it is relevant
- Suggested search terms or categories to inspect

#### Follow links within benchmark resources

When a benchmark resource is an index, survey, collection, repository,
or resource hub, inspect relevant links contained within that resource.

Follow relevant links recursively when they are likely to lead to:
- benchmark descriptions
- benchmark papers
- datasets
- evaluation protocols
- leaderboards
- baseline implementations
- official code repositories
- closely related benchmark collections

Follow relevant links up to 2 levels deep by default. This means that if
a resource page links to another relevant page, inspect that page, and if
that page itself contains a relevant link, inspect that linked page as well.

Do not recursively explore unrelated links.

Do not treat a top-level resource page as the benchmark itself when it
only serves as an index, collection, or discovery hub.

For every benchmark ultimately reported, verify it using the most direct
available source, such as:
- the benchmark's original paper
- official benchmark page
- official dataset page
- official repository

Discovery resources may be used to find candidate benchmarks, but should
not replace direct-source verification when a direct source is available.

Search the relevant provided/recommended sources first for candidate
benchmarks.


### Step 3: Benchmark search

Apply the Strict Benchmark Definition and classification above.

#### 3a. Exact benchmark for the original question

Using the recommended benchmark sources first, search for established
benchmarks that are EXACT / DIRECT for the original question, i.e. that pass
the SAME-TASK test, comparability check, and benchmark validity check.

Prefer established benchmarks already used in published research.

Record any PROXY BENCHMARK or RELATED DATASET found, for traceability only.

#### 3b. Replacement search (Benchmark-First Mode, if 3a fails)

Keep the slot ID and report "Original direction rejected: no exact
established benchmark found."

Then search progressively farther from the original topic (same target
behavior → same broad research area → adjacent areas) until a benchmark
passes exact-benchmark validation (SAME-TASK test and comparability check)
for the replacement problem. Do not lower the benchmark standard to preserve
topical similarity. Prefer the benchmark-first priorities listed under
Modes.

For the chosen replacement report:
- The nearby problem it directly evaluates
- How far it moves from the original question
- Why it is EXACT for the nearby problem, not a proxy

A replacement benchmark is not evidence that the original question has been
studied.

#### 3c. No exact benchmark

Only return:

UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND

after the exact search (and, in Benchmark-First Mode, the exhaustive
replacement search) has failed. Still return an entry for the slot; never
drop it. Do not fabricate benchmarks.

#### 3d. Verify the benchmark

For every benchmark reported as EXACT / DIRECT, verify each field below from
the benchmark's original paper, official page, official dataset page, or
official repository. Do not infer them. Mark any field that cannot be
verified as UNKNOWN. If a critical property (task, dataset, protocol,
metric, or baseline) is UNKNOWN, say the benchmark is not verified as
established.

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
- SAME-TASK test answers (A-E, each YES / NO / UNKNOWN)
- Comparability check: the published-baseline / reproduced-baseline /
  proposed-method table on the established metric is conceptually valid
  (YES / NO)
- Benchmark validity answers (V1–V4, each YES / NO / UNKNOWN with a
  one-line justification), and any rewrite of the question made to remove
  a mismatch

benchmark-finder applies the SAME-TASK test to the candidate main comparison
implied by the benchmark and the identified gap. It does not design the
full experiment; research-planner re-applies the test to the final design.


### Step 4: Report

Return exactly one entry per parsed idea evaluated and per generated
direction. Never merge ideas or drop one.

For each entry, report:

- ID (RQk, unchanged even if the content is replaced; RQm+1, ... for
  generated directions)
- Original Research Question (or "Generated — inspired by <theme / RQ>")
- Original Question Status: EXACT BENCHMARK FOUND / REJECTED (no exact
  established benchmark found)
- Replacement Problem (if replaced)
- Candidate Research Question (question format, rules 1–6; sent to
  prior-work-checker)
- Regeneration iteration and excluded questions (if this entry answers a
  prior-work FAIL)
- Standard Task
- Research Category
- Recommended Benchmark Sources
- Suggested Search Terms
- Exact Benchmark (for the original question or the nearby problem)
- Rejected Candidates: proxy benchmarks / related datasets (traceability
  only, not support)
- Benchmark Type: EXACT / DIRECT / PROXY BENCHMARK / RELATED DATASET /
  NO BENCHMARK
- Benchmark Verification (all fields from Step 3d, including SAME-TASK
  test answers, comparability check, and benchmark validity V1–V4)
- What It Measures
- Relationship to Research Question
- Reusable Components
- Required Modification (to the method or condition only; never to the
  benchmark's task, data, protocol, or metric)
- Metric
- Dataset
- Original Benchmark Paper
- Code Repository
- Relevant Prior Work
- Representative Baseline
- Literature Relationship
- Main Evidence Gap
- Benchmark Readiness (see below)
- Candidate Small Gaps Around This Benchmark (verified against literature;
  no novelty claims)

Benchmark Readiness (a practical assessment, separate from the scientific
classification above; report factually from verified sources and do not
turn it into compute-feasibility judgments or experiment design):
- Dataset Availability
- Evaluation Code Availability
- Baseline Availability
- Setup Complexity
- Reproduction Risk
- Compute Burden (as documented by the benchmark/baseline, not a feasibility
  judgment)
- Modification Simplicity
- Short-Project Readiness
- Training Required? (none / fine-tuning / from scratch)
- Evaluation Type (automatic metric / LLM judge / human)
- External Dependencies (APIs, closed models, judge models, gated data)
- Repository Maturity (official, maintained, documented run command?)
- Typical Number of Conditions / Seeds in prior work
- Experience-sensitive factors present (YES / NO each, factual): multi-GPU
  or model-parallel execution; 70B-class models; activation hooks or
  mechanistic interpretability tooling; external judge / API pipeline;
  complicated output parsing; published effect reported as fragile or hard
  to reproduce; multiple interacting frameworks or repositories

These readiness fields are factual inputs for compute-planner's
duration-feasibility (against the user-specified D) and difficulty
estimate at the user-specified experience level L; benchmark-finder does
not make that judgment itself.

Also include a concise benchmark search trace:

1. User-provided sources checked
2. Reference resources checked
3. Exact benchmark search for the original question
4. Proxy benchmarks / related datasets found (rejected as support)
5. Replacement search for nearby problems (if needed)
6. Broader literature search
7. Final benchmark classification and verification status


### Step 5: Benchmark-centered prior-work archive (provisionally confirmed benchmarks only)

#### When to run

Do NOT build a full archive for every benchmark candidate. Run this step
only after a benchmark has become the PROVISIONALLY CONFIRMED benchmark for
a project slot, i.e. after:

research question → candidate benchmark search → readiness/validity checks
→ benchmark selection → benchmark provisionally confirmed

(In the pipeline, "provisionally confirmed" means: the benchmark passed the
exact-benchmark checks, research-readiness-advisor selected it for the
slot, and the slot's research question passed prior-work-checker. It
becomes FINAL CONFIRMED only after this archive search, the overlap
re-check, and the advisor's readiness re-evaluation all pass; see
research-pipeline Step 2c.)

If a slot's benchmark later changes, run this step for the newly
provisionally confirmed benchmark. Archives for benchmarks no longer used
are kept, not deleted.

#### File location, name, and de-duplication

- Write archives to the current project working directory (the directory
  where the pipeline report is written), never inside the skills directory.
- One Markdown file per benchmark, named from the benchmark's CANONICAL
  name: `prior_work_<benchmark_name>.md`, where `<benchmark_name>` is the
  canonical name lower-cased, with spaces and punctuation replaced by single
  underscores (e.g. `prior_work_truthfulqa.md`).
- Before creating a file, check the working directory for an existing
  `prior_work_*.md` whose canonical name or listed aliases match this
  benchmark (including different versions or capitalisations of the same
  name). If one exists, reuse and extend it: append new search passes to
  the Search log, add new papers to the inventory, and add or update the
  project-specific sections for this slot. Never create a second file for
  the same benchmark. Distinct benchmark versions that are evaluated
  separately in the literature (e.g. a v2 with a different test set) get
  their own file and cross-reference each other.

#### Search objective

Search as comprehensively as reasonably possible for prior work that:

- introduced the benchmark;
- used the benchmark;
- reported results on the benchmark;
- proposed methods evaluated on the benchmark;
- modified or extended the benchmark;
- analyzed weaknesses, biases, failure modes, or limitations of the
  benchmark;
- introduced relevant baselines;
- introduced strong or SOTA methods on the benchmark;
- performed ablations or analyses directly relevant to the user's proposed
  method;
- used substantially similar interventions or mechanisms on the same
  benchmark.

The archive is benchmark-centered, not only research-question-centered.
Include papers important for understanding benchmark history, major
methods, strong results, known limitations, or evaluation conventions even
if they are not directly relevant to the current method, and mark their
relevance to the current RQ. Do not stop after finding enough papers to
justify the project.

#### Search procedure

For every provisionally confirmed benchmark:

1. Find the original benchmark paper.
2. Identify the canonical name and aliases.
3. Trace papers that cite the benchmark paper (e.g. Semantic Scholar /
   Google Scholar "cited by").
4. Search the benchmark name and each alias directly.
5. Search combinations of the benchmark (and aliases) with: method,
   baseline, evaluation, improvement, analysis, ablation, robustness, bias,
   failure, and the proposed intervention/mechanism (and its synonyms).
6. Trace references and citations from the most relevant papers found.
7. Identify the strongest relevant published baseline found.
8. Specifically search whether the proposed research question or method
   has already been tested on this benchmark.

Suggested sources: Semantic Scholar, Google Scholar, arXiv, OpenReview,
ACL Anthology (where relevant), Papers with Code / leaderboards, Hugging
Face, and the official repository's issues and linked work. Record every
pass in the Search log.

Read the source for every numerical result recorded. Never infer a missing
number; write `NR` (not reported). Never invent papers, numbers, or URLs.

#### Archive schema

```markdown
# Prior Work Archive: <Canonical Benchmark Name>

Last updated: <YYYY-MM-DD>
Used by projects: <RQk (project / research question), ...>

## 1. Benchmark identity
- Benchmark name:
- Canonical paper:
- Authors:
- Year:
- Benchmark task:
- Dataset:
- Primary metric(s):
- Official repository / dataset:
- Important aliases:

## 2. Search log
| Pass | Date searched | Source / database | Query | Useful results (number / relevance) | Notes |
|---|---|---|---|---|---|

## 3. Prior-work inventory
| Paper | Year | Relationship to benchmark | Method | Model(s) | Dataset/split | Metric | Reported result | Code/data available | Relevance to current RQ |
|---|---|---|---|---|---|---|---|---|---|
(Relationship: introduced / used / reported results / method / modified or
extended / analysis or criticism / baseline / SOTA / relevant ablation /
similar intervention. Every number cites its source location, e.g.
"Table 2"; `NR` if not reported. Relevance: per RQk — DIRECT / PARTIAL /
BACKGROUND / NONE.)

## 4. Benchmark history
original benchmark → important baselines → major improvements → current
strong methods → relevant analyses / criticisms

## 5. Closest prior work — <RQk>
(one subsection per project using this benchmark)
| Paper | What they tested | How it differs from the proposed project | Proposed contribution still distinct? |
|---|---|---|---|

## 6. Baseline map — <RQk>
- Original benchmark baseline:
- Commonly used baseline:
- Strongest directly comparable baseline found:
- Strongest overall result found:
- Baseline selected for the user's experiment:
- Why the selected baseline is the appropriate comparison:
(The highest reported number is not automatically the appropriate
baseline; comparability of model, setting, split, and metric decides.)

## 7. Prior-work collision check — <RQk>
Question: Has the proposed method, intervention, or a substantially
equivalent research question already been tested on this benchmark?
Verdict: NO EVIDENCE FOUND / PARTIAL OVERLAP / STRONG OVERLAP / ALREADY TESTED
Supporting papers:

## 8. Open gap — <RQk>
(Stated only after sections 3 and 7.)
Gap type: genuinely untested mechanism / new method on an existing
benchmark / new analysis of existing outputs / new combination of known
methods / replication or robustness study / benchmark extension
Gap statement:

## 9. Search limitations
- What may still be missing, and why:
- Is additional prior work likely to exist?:
- Coverage statement: "Systematic benchmark-centered search found the
  following relevant prior work as of <date>."
```

Sections 1–4 and 9 describe the benchmark and are shared by all projects
using it. Sections 5–8 are per project (one subsection per RQk).

#### Collision verdict and gap rules

- ALREADY TESTED: a traced work performs the same comparison (or a trivially
  equivalent one) on this benchmark.
- STRONG OVERLAP: a functionally equivalent experiment, or one whose results
  already substantially answer the question.
- PARTIAL OVERLAP: related work on the same benchmark or mechanism, but the
  answer to the question still cannot be inferred.
- NO EVIDENCE FOUND: no overlapping work in the documented search.

These correspond to prior-work-checker's SAME COMPARISON, FUNCTIONALLY
EQUIVALENT / SUBSTANTIALLY ANSWERED, PARTIAL, and no overlap.

Do not call something a gap merely because the exact wording of the
question has not appeared in a paper.

If the verdict is ALREADY TESTED or STRONG OVERLAP, report it so the
pipeline returns the slot to research-question / benchmark selection or
redesign. Do not continue as though the project were unchanged.

#### Coverage language

Never claim the archive contains every paper on the benchmark, and never
write "all prior work has been found". Always report the search strategy,
sources, queries, dates, coverage limitations, and whether more prior work
is likely to exist, and use: "Systematic benchmark-centered search found
the following relevant prior work as of <date>."

#### Output to the pipeline

Return, per slot: the archive file path, provisionally confirmed benchmark, selected
baseline (with its source), closest prior work, collision verdict, and gap
type and statement. The full inventory stays in the archive file.


### Verification rules

- Never invent papers, benchmarks, datasets, scores, URLs, or repositories.
- Verify that cited benchmarks and papers actually exist.
- Do not claim novelty simply because no matching prior work was found.
- benchmark-finder does not make compute-feasibility judgments or design
  experiments.
