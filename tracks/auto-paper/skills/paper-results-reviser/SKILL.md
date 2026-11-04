---
name: paper-results-reviser
description: "Revise an existing research paper draft (.md or .tex) against a directory of COMPLETED experimental results. Discovers and ranks result artifacts, audits their integrity, maps every paper claim to evidence, evaluates the original hypotheses (SUPPORTED / NOT SUPPORTED / INCONCLUSIVE / NOT EVALUABLE), revises the paper to match the actual findings (including negative and null results), and writes <stem>_revised.<ext> plus revision_audit.md. Post-experiment only; never runs experiments, redesigns the study, or modifies result artifacts. Use when a user has finished experiments and wants the paper updated to reflect the real results. Usage - /paper-results-reviser <paper_draft> <results_directory> [plan: <file>] [format: <venue/page limit>] [out: <dir>] [free-text instructions]"
argument-hint: "<paper_draft> <results_directory> [plan:<file>] [format:<text>] [out:<dir>] [instructions]"
allowed-tools: Read Grep Glob
---

# Paper Results Reviser

Revise ONE existing paper draft so it accurately reflects ONE set of
completed experimental results, and document every change in an audit.

This is a post-experiment revision skill. It does not redesign the study,
add experiments, change hypotheses, or regenerate results. It is generic:
assume nothing about the project, benchmark, model, metric, or number of
arms beyond what the inputs state.

## 1. Inputs and argument handling

Raw arguments: `$ARGUMENTS`

Parse the raw arguments with shell-style quoting (a quoted path may contain
spaces). Pre-parsed positional values:

- `paper_draft` (required) = `$0`
- `results_directory` (required) = `$1`

Everything after the second positional argument is optional and parsed
from the raw string:

| Key | Meaning |
| --- | --- |
| `plan: <path>` | Original experiment plan / preregistration (`experiment_plan`). |
| `format: <text>` | Target venue, page/word limit, style (`target_format`). |
| `out: <dir>` | Output directory (default: the draft's directory). |
| `overwrite-original` | Only if present: the user explicitly allows writing over the draft. |
| any other text | `revision_instructions` (preferences, scientific constraints). |

Values after a key may be quoted. Natural-language equivalents ("the plan
is in X", "4-page limit") count as the same keys.

Validation, before anything else:

1. If either required value is missing, empty, or still looks like an
   unexpanded placeholder, ask the user for it. Never search the disk for
   a substitute draft or results directory.
2. Resolve paths relative to the current working directory; accept
   absolute paths, forward or back slashes, and spaces.
3. `paper_draft` must exist and end in `.md` or `.tex` (for `.tex` with
   `\input`/`\include`, also read the included files). Otherwise stop and
   ask.
4. `results_directory` must exist and be a directory. Otherwise stop and
   ask.
5. If the user gave the arguments in the wrong order (a directory first),
   swap only when unambiguous and say so.

The skill must work with only the two required inputs. If the original
hypotheses, primary metric, conditions, or analysis plan cannot be
reliably reconstructed from the draft plus the results directory (e.g. a
plan/preregistration/config inside it), ask for the experiment plan.
Never invent them.

## 2. Hard constraints (read-only on everything except the outputs)

Allowed writes: the revised paper and `revision_audit.md` in the output
directory, plus throwaway helper scripts/outputs in the session scratchpad
(or system temp) directory, never inside `results_directory`.

Never:

- run new experiments, training, inference, or evaluation jobs; submit HPC
  or cluster jobs; call model APIs to produce new results;
- regenerate, edit, move, rename, or delete any file in
  `results_directory`, any raw result, frozen config, or preregistration;
- change the original research questions, hypotheses, primary metric,
  analysis plan, or experimental design;
- overwrite the original draft (unless `overwrite-original` was given);
- overwrite an existing `*_revised.*` or `revision_audit.md` - use the next
  free suffix (`_revised_2`, `revision_audit_2.md`, ...) and report it;
- fabricate citations, experiments, data, metrics, CIs, p-values,
  significance, baselines, or SOTA claims;
- present a REPORTED value as VERIFIED.

Read-only analysis (Read/Grep/Glob, `python -I` or similar on copies of
values, read-only pandas/json loading) is allowed for verification and
recomputation.

## 3. Workflow

Follow every step in order. Steps 5-7 are mandatory; do not skip the
evidence map.

### Step 1 - Read the paper draft

Read it completely. Record: title, RQs, hypotheses (verbatim, with their
exact operational definitions), conditions/arms, datasets/splits, models,
metrics, statistical tests, correction method, practical-significance
thresholds, baselines, planned sample sizes, every quantitative statement,
every table/figure and where each is referenced, every SOTA/"outperforms"
claim, and placeholders (`TBD`, `XX`, `??`, `\todo`, "expected").

### Step 2 - Discover the results directory

List the full tree (Glob `**/*`), with sizes and modification times where
available. Do not read huge raw files whole; sample heads, schemas, and
row counts. Classify every relevant file into:

- primary analysis outputs; secondary/exploratory analyses;
- raw item-level results; statistical tests; confidence intervals;
- baseline comparisons; ablations; figures; tables;
- completion status / execution summaries / logs;
- validation and integrity reports; manifests, configs, metadata, hashes;
- documented deviations and known limitations;
- non-authoritative: intermediate, debug, smoke/pilot, partial, superseded,
  old-version, backup, temporary.

### Step 3 - Read the experiment plan (if given)

Also look for a plan, preregistration, frozen config, or design document
inside `results_directory`. Where the plan and the draft disagree on a
design element, the plan (frozen earlier) wins for what was intended; the
results show what was run. Record every disagreement.

### Step 4 - Identify authoritative outputs

Rank sources by explicit designation, not recency:

1. Files explicitly marked final/authoritative by a manifest, README,
   audit/validation report, or completion summary.
2. Outputs whose config/hash/version matches the frozen design and that
   passed validation.
3. Complete runs over partial ones; validated over unvalidated.

Do not assume the newest file is authoritative. When two candidates
conflict, investigate provenance (config IDs, hashes, timestamps vs. logs,
manifests, sample counts, which file later reports cite). If the conflict
cannot be resolved from the evidence, STOP, list the candidates and the
conflict, and ask the user which is authoritative.

### Step 5 - Scientific integrity audit

Check every item the available data supports; mark the rest "not
checkable" with the reason:

- expected vs actual sample counts per arm/condition/seed; missing,
  duplicate, invalid, or excluded observations (and whether exclusions
  follow a pre-stated rule);
- arm/condition coverage; dataset, split, and model identity vs the paper;
- metric and statistical-test definitions as implemented vs as described;
- CI method and level; multiple-testing correction (family, method);
- baseline comparability (classes A-D, Step 9 "Baselines and SOTA");
- completion status, crashes, retries, reruns;
- deviations from the plan;
- summary statistics vs raw results (recompute means/rates/counts from
  item-level data when feasible).

Recompute only when necessary and feasible from existing data. If a
recomputed value disagrees with the official one, keep the official value
in the paper, document both in the audit, and investigate the cause
(rounding, filtering, different denominator, bug). Never silently swap
in the recomputed number. If the disagreement changes a conclusion, it is
a blocking issue.

Label each quantitative result:

- `VERIFIED` - checked directly against underlying data;
- `REPORTED` - present in the results but not independently checked;
- `UNRESOLVED` - conflicting or insufficient evidence.

### Step 6 - Evidence map

Build a table linking every major claim in the draft (abstract,
contributions, results, discussion, conclusion, captions) to: the
supporting file and field/row, the value, its status
(VERIFIED/REPORTED/UNRESOLVED), and a verdict: `CONSISTENT`, `UPDATE`
(placeholder or wrong number), `CONTRADICTED`, `UNSUPPORTED`, or
`OVERSTATED`. Use the format in
[references/audit_template.md](references/audit_template.md).

### Step 7 - Hypothesis evaluation and inconsistencies

For each original hypothesis (definition unchanged), record: conditions
compared, metric, effect size (absolute and, if useful, relative), 95% CI,
raw p, adjusted p and correction, practical-significance threshold, n,
and the outcome:

- `SUPPORTED` - meets the pre-stated criterion (significance and/or CI
  and/or practical threshold, as defined in the draft/plan);
- `NOT SUPPORTED` - the evidence contradicts it, or a sufficiently precise
  estimate excludes the hypothesized effect / practical threshold;
- `INCONCLUSIVE` - the criterion is not met but the CI is too wide to rule
  out a meaningful effect;
- `NOT EVALUABLE` - required data missing, failed, or invalid.

Use the decision rule stated in the draft or plan. If none is stated,
say so and apply the conventional reading (two-sided alpha = 0.05 after
the stated correction) labelled as such. A nonsignificant result is not
evidence of no effect unless an equivalence/precision criterion supports
that. Do not create post-hoc hypotheses; label any additional analysis
`exploratory`.

Then list every inconsistency between draft and results (Step 6 verdicts
other than CONSISTENT, plus design/plan deviations).

**Blocking issues** - stop before writing a revised paper if any of these
hold: authoritative source unresolved; primary-outcome data missing or
invalid; recomputation contradicts the official primary result in a way
that flips a conclusion; the run used a different dataset/model/metric
than the paper describes and the paper cannot be truthfully revised
without the user's decision; hypotheses cannot be reconstructed and no
plan was supplied. In that case write only `revision_audit.md` with
status `BLOCKED`, the blocking items, and the questions for the user.

### Step 8 - Revision strategy

Decide, and record in the audit, the minimal set of changes that makes the
paper truthful: which claims to update, soften, remove, or reframe; whether
the title or headline contribution must change; what moves to limitations;
what is labelled exploratory. Emphasizing the strongest supported finding
is fine; hiding contradictory evidence is not. The design described in the
paper must stay the design that was run - disclose deviations instead of
rewriting the design to match.

### Step 9 - Revise the paper

Edit the existing text; do not rewrite from scratch. Preserve RQs,
hypotheses, design, methodological commitments, valid citations, correct
background, technical contributions, section structure, and voice.

Update as needed: title (only if the old one is now false or misleading),
abstract, introduction/contributions, experimental setup (actual n,
exclusions, deviations), results, tables, figure captions/references,
discussion, limitations, conclusion. Replace all result placeholders with
authoritative values or, where none exists, state that the result is not
available - never leave a guessed number.

Format rules:

- `.md`: keep heading hierarchy, table syntax, image links, citation style.
- `.tex`: keep preamble, packages, macros, `\label`/`\ref`/`\cite` keys,
  bibliography commands; do not add `.bib` entries; keep it compilable
  (balanced environments/braces, no undefined macros introduced).

Statistical reporting:

- absolute values for each condition, then effect size, 95% CI, test,
  p (raw and adjusted, with method), n;
- percentage points (pp) for differences of percentages; % only for
  relative change, and never relative change alone;
- rounding consistent across the paper and never changing a conclusion
  (e.g. do not round p = 0.052 to 0.05, or a CI bound across zero);
- identical numbers in abstract, results, tables, discussion, conclusion.

Baselines and SOTA - classify every comparison:

- A. directly comparable within-study baseline;
- B. reproduced external baseline (state reproduction gap vs published);
- C. cross-paper reference only (different protocol/compute/scorer);
- D. not comparable.

Check same benchmark and split, metric definition, evaluation protocol,
scorer implementation, model/compute class. "State of the art" requires
a comparison in A or B on the standard benchmark protocol; never claim it
from C or D, and never from beating a weak baseline. Disclose failed or
divergent reproductions.

Figures and tables:

- check plotted/tabled values, metric names, axes, units, error bars (what
  they represent: SD, SE, 95% CI) against the authoritative data;
- reuse valid figures; do not create or modify figure image files and do
  not generate data; fix a caption when only the caption is wrong;
- flag an incorrect figure in the audit (and with a visible author note in
  the paper only if it cannot be fixed in text) for the user to regenerate;
- keep figure/table numbering and every in-text reference consistent.

Length and quality: keep the original scope. If `format` gives a limit,
prioritize methods, quantitative results, honest negatives, and concise
limitations over background. The paper must read as a coherent academic
paper in academic English (unless instructed otherwise), not as an audit
log - audit detail belongs in `revision_audit.md`.

### Step 10 - Verification pass

Re-read the revised paper end to end and check:

- every number traces to the evidence map (no orphan numbers);
- no REPORTED/UNRESOLVED value is described as verified or certain;
- abstract, results, tables, discussion, and conclusion agree;
- hypothesis statements are verbatim-equivalent to the originals;
- each hypothesis outcome in prose matches Step 7;
- no remaining placeholders; every figure/table reference resolves;
- no SOTA or "outperforms" claim without an A/B comparison;
- pp vs % used correctly; CIs and p-values paired with their comparison;
- exploratory analyses labelled; deviations and exclusions disclosed;
- citations unchanged except removals of claims they no longer support;
- original draft and results directory untouched (compare to Step 2 list).

Fix failures before saving.

### Step 11 - Deliverables

Write to the output directory (default: the draft's directory):

- A. `<original_stem>_revised.<original_extension>` - the revised paper.
- B. `revision_audit.md` - using
  [references/audit_template.md](references/audit_template.md), with all
  nine required sections.

Then reply to the user briefly: output paths, authoritative sources used,
hypothesis outcomes (one line each), the most important changes, blocking
or unresolved issues and questions, and any figures needing regeneration.

## 4. When to ask instead of proceeding

Ask (and do not guess) when: required paths are missing/invalid;
authoritative results conflict irreconcilably; hypotheses or the primary
metric cannot be reconstructed; the draft and the results describe
different studies; or a revision instruction would require violating the
constraints in Section 2 (explain which and why).
