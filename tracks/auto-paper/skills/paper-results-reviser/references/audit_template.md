# revision_audit.md template

Fill every section. Write "None" rather than omitting a section. Keep
entries factual and traceable (file path + field/row/line for every value).

```markdown
# Revision Audit - <paper title>

Status: COMPLETE | COMPLETE WITH UNRESOLVED ISSUES | BLOCKED
Date: <YYYY-MM-DD>
Revised paper: <path or "not produced (BLOCKED)">

## 1. Input files used
| Role | Path | Notes |
|---|---|---|
| paper_draft | ... | format, length |
| results_directory | ... | file count, top-level layout |
| experiment_plan | ... or "not supplied" | where hypotheses were taken from |
| target_format / instructions | ... | |

## 2. Authoritative result sources
| File | Category | Why authoritative (designation / config / validation) |
|---|---|---|

Excluded / non-authoritative files (and reason: superseded, partial,
debug, pilot, temporary, conflicting):
| File | Reason |
|---|---|

Provenance conflicts investigated and how each was resolved (or why not).

## 3. Integrity audit findings
| Check | Expected | Observed | Status (PASS / FAIL / NOT CHECKABLE) | Notes |
|---|---|---|---|---|
| Sample count per arm | | | | |
| Missing / duplicate / invalid / excluded | | | | |
| Arm coverage | | | | |
| Dataset / split / model identity | | | | |
| Metric definition | | | | |
| Statistical test / CI method | | | | |
| Multiple-testing correction | | | | |
| Baseline comparability | | | | |
| Completion status | | | | |
| Plan deviations | | | | |
| Summary vs raw consistency | | | | |

Recomputations: value, official value, recomputed value, difference,
explanation. Official values kept in the paper.

## 4. Hypothesis-by-hypothesis outcomes
| H | Original statement (verbatim) | Conditions | Metric | Effect (abs.) | 95% CI | p raw | p adj. (method) | Practical threshold | n | Evidence status | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|

Outcome in {SUPPORTED, NOT SUPPORTED, INCONCLUSIVE, NOT EVALUABLE};
evidence status in {VERIFIED, REPORTED, UNRESOLVED}. State the decision
rule used and where it came from. Exploratory analyses listed separately
and labelled exploratory.

## Evidence map
| # | Paper location | Claim (draft) | Source file : field/row | Value | Status | Verdict | Action |
|---|---|---|---|---|---|---|---|

Verdict in {CONSISTENT, UPDATE, CONTRADICTED, UNSUPPORTED, OVERSTATED}.
Action in {kept, updated, softened, removed, reframed, moved to limitations}.

## 5. Major changes made to the paper
Section-by-section list (title, abstract, introduction/contributions,
setup, results, tables, figures, discussion, limitations, conclusion),
each with a one-line rationale tied to evidence-map rows.

## 6. Unsupported claims removed or corrected
| Original text (short) | Problem | Replacement / removal |
|---|---|---|

Include every SOTA / "outperforms" claim with its baseline class (A-D).

## 7. Remaining limitations
Scientific limitations of the study now stated in the paper.

## 8. Unresolved issues
Conflicts, NOT CHECKABLE items, REPORTED-only values in key claims,
figures needing regeneration, questions for the user.

## 9. Final consistency checks
| Check | Result |
|---|---|
| Every number traces to evidence map | |
| Abstract / results / tables / discussion / conclusion agree | |
| Hypotheses unchanged from original | |
| No placeholders remain | |
| Figure/table references resolve | |
| pp vs % correct; CIs/p paired with comparisons | |
| No SOTA claim without class A/B comparison | |
| Exploratory analyses labelled | |
| Original draft untouched | |
| results_directory untouched | |
| Length within target_format (if given) | |
```
