# paper-results-reviser

Revises **an existing paper draft** (`.md` or `.tex`) so that it matches
**a directory of completed experimental results**. It finds and ranks the
result files, audits their integrity, maps every claim in the paper to
evidence, evaluates each original hypothesis, rewrites the paper to match
what actually happened (including null and negative results), and
documents every change.

It is generic: it works on any project, not only papers from
paper-writer. It is post-experiment only. It never runs experiments,
redesigns the study, or edits result files.

## When to use it

- Experiments are done and the draft still contains `TBD`s or hoped-for
  claims.
- You have a paper and results that didn't come from experiment-runner
  (otherwise `/paper-writer ... results:` is the matching tool).

## How to use it

```
/paper-results-reviser <paper_draft> <results_directory> [plan: <file>] [format: <venue/page limit>] [out: <dir>] [free-text instructions]
```

Examples:

```
/paper-results-reviser paper.md results/
/paper-results-reviser "drafts/my paper.tex" runs/final plan: prereg.md format: "4-page workshop"
/paper-results-reviser paper.md results/ out: revised/ keep the related work untouched
```

| Option | Meaning |
| --- | --- |
| `plan:` | Original experiment plan or preregistration. Strongly recommended. Without it, the skill asks if the hypotheses can't be reconstructed. |
| `format:` | Target venue or page limit |
| `out:` | Output directory (default: the draft's folder) |
| `overwrite-original` | Only if you explicitly want the draft replaced |
| other text | Revision instructions |

## Hypothesis outcomes

Each hypothesis is marked **SUPPORTED / NOT SUPPORTED / INCONCLUSIVE / NOT
EVALUABLE**, and the paper's framing is adjusted to match.

## Output

- `<stem>_revised.<ext>`: the revised paper. The original is untouched.
- `revision_audit.md` (from `references/audit_template.md`, nine
  sections): sources used, integrity findings, evidence map, hypothesis
  outcomes, and each change with the reason for it.
- A short reply covering the outputs, hypothesis outcomes, key changes,
  open issues and figures that need regenerating.

## It stops and asks when

Required paths are missing, results conflict in ways that can't be
reconciled, the hypotheses or primary metric can't be reconstructed, the
draft and the results describe different studies, or an instruction would
require breaking its constraints.
