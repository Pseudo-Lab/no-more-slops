# paper-writer

Turns **one** project's final research plan and its provisional draft into
a **complete short paper written all the way through the Conclusion**
(about 4 pages by default). It then compiles the paper in a real venue
template and checks the page limit **on the compiled PDF**.

It has two modes:

- **Pre-experiment**: no results yet. The full narrative is written as if
  the working hypothesis holds, and every unmeasured number is `TBD`.
- **Post-experiment**: you supply `results:`. The whole paper is rewritten
  against the measured evidence, including null or negative results.

It is invoked manually only. It never picks research questions, redesigns
the project, or runs experiments.

## How to use it

```
/paper-writer <RQ_FILE> <DRAFT_FILE> [Project p | RQk | "exact title"] [page limit N] [venue: <profile>] [results: <file or values>]
```

Examples:

```
/paper-writer research_pipeline_report_v6.md provisional_paper_drafts_v6.md RQ4 4
/paper-writer report.md drafts.md RQ1 venue: neurips-workshop-4
/paper-writer report.md paper_RQ1_v1.md RQ1 results: results_RQ1.md
```

| Argument | Meaning |
| --- | --- |
| `RQ_FILE` | The final plan, e.g. `research_pipeline_report_vN.md`. Authoritative for the research design. |
| `DRAFT_FILE` | The provisional draft (from research-readiness-advisor), or the latest `paper_RQk_vN.md` when revising |
| project id | Needed only if a file contains several projects |
| page limit | A number right after the project id, or `pages: N`. A bare number with no project id is ambiguous, so the skill asks. |
| `venue:` | `default-4`, `neurips-workshop-4`, `neurips`, `icml`, `iclr`, `cvpr`, `iccv`, `eccv`, `aaai`, `aaai27`, `aistats`, `uai`, `ijcai`, `acl-long`, `acl-short`, `colm`, `tmlr` |
| `results:` | A results file or pasted values. Switches to post-experiment mode. |

If a file is missing it asks you. It never substitutes another file it finds
on disk.

## What it enforces

- **Venue-style tables**: established method names with citations,
  *published* vs *reproduced* values marked, and statistics in the text or
  appendix rather than in the main tables.
- **Claim discipline**: a claim–evidence ladder, so no claim goes beyond
  its evidence.
- A consistency check before saving.
- **The page limit on the actual PDF**, via
  `paper-to-latex/scripts/check_page_limit.py` (up to 6 revision rounds).

## Output

- `paper_RQk_v1.md` in the project folder (the folder of `RQ_FILE`). Each
  later revision goes to the next free version (`_v2`, `_v3`, ...). Nothing
  is ever overwritten.
- `paper_RQk_vN_latex/`: the compiled LaTeX version with `pagelimit.json`.
- A reply listing the mode, the sources used, inconsistencies and how they
  were resolved, remaining placeholders, the page-check result, a five-Cs
  card and the `check_tables.py` result.

## Files

- `references/paper_standards.md`, `references/venue_profiles.{md,json}`
- `scripts/check_tables.py`
- `templates/tables/*.tex`: main-results, ablation, diagnostic and
  statistics-appendix table templates, plus `table_macros.tex`
- `templates/venues/_downloads/`: bundled official author kits (AAAI, ACL,
  AISTATS, COLM, CVPR, ECCV, ICCV, ICLR, ICML, IJCAI, NeurIPS, TMLR, UAI),
  with their sources in `SOURCES.json`

## Where it sits

```
research-pipeline → paper-writer (pre) → experiment-runner → paper-writer (post, results:) → paper-visuals → paper-to-latex
```
