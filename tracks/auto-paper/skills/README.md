# Research-to-paper workflow

This guide explains which of these skills are meant to be used together and
how to run them. Every skill also has its own `README.md` and `SKILL.md`.

Scope: it covers only the 13 skills in the table below, contributed by the
research-pipeline project. Any other skills in the same folder are separate
contributions and are not part of this workflow.

| Group | Skills | Relationship |
| --- | --- | --- |
| **A. Research planning** (required workflow) | research-pipeline, research-question-parser, benchmark-finder, research-readiness-advisor, prior-work-checker, compute-planner, research-planner | Designed as one workflow. `research-pipeline` runs the other six in a fixed order, and they share reference files. |
| **B. Paper and experiment loop** (required workflow) | paper-writer, experiment-runner | `experiment-runner` only accepts a paper from `paper-writer`, and its results go back into `paper-writer`. Group B's input is group A's output. |
| **C. Finishing tools** (run independently; optional combinations) | paper-visuals, paper-to-latex, paper-results-reviser | Each is run by itself on any paper. They share some files with `paper-writer` (see Setup). |
| **Standalone** | [research-benchmark-advisor](research-benchmark-advisor/README.md) | Has no dependency on the other skills. See its own README. |

## Purpose

Groups A and B together take you from a file of rough research ideas to a
complete short paper (about 4 pages by default) backed by a real experiment:

1. Pick a project with an **exact public benchmark**, a **traced published
   baseline**, a **novelty check against prior work**, and a schedule that
   **fits your time budget and experience level** (group A).
2. Write the whole paper **before** the experiment, with unmeasured numbers
   marked `TBD`. Then run **only** the experiment the paper specifies, and
   rewrite the paper around the measured results (group B).

## Setup

The skills read each other's files from `~/.claude/skills/<name>/`, so
these folders must all be installed together:

| Folder | Why it is needed |
| --- | --- |
| Group A (all seven) | Shared references: `benchmark-finder/references/research_advice.md`, `research-pipeline/references/research_design_principles.md`, `compute-planner/references/compute.md` |
| `paper-writer` | Table standards, venue profiles, table templates and `scripts/check_tables.py`. Used by paper-writer, paper-visuals and paper-results-reviser. |
| `paper-to-latex` | `templates/main_twocolumn.tex`, `scripts/check_page_limit.py` and `scripts/compare_content.py`. **paper-writer always uses these to check the page limit on the compiled PDF**, even if you never run `/paper-to-latex`. |
| `research-readiness-advisor` | `references/mentorship_principles.md`, read by paper-writer and experiment-runner |

If you got these skills from a repository, copy all the skill folders into
`~/.claude/skills/`. Then edit
`~/.claude/skills/compute-planner/references/compute.md` to describe **your**
hardware. It is the only source the skills use to decide what compute you
have.

Optional: the skills also mention a Stop hook,
`~/.claude/hooks/page_limit_gate.py`, which stops Claude from ending its
turn while a compiled PDF is over the page limit. It is not part of these
folders, and the skills work without it.

## Workflow A: research planning

```
research-question-parser → benchmark-finder ⇄ prior-work-checker → compute-planner → research-planner
                                   ↘ research-readiness-advisor ↗
```

Run it with one command. `research-pipeline` calls each step in order:

```
/research-pipeline

File: ideas.md
Time budget: 2 weeks
Experience level: Beginner
Number of research directions: 3
```

The time budget is **per project**. If you leave out the file, the budget
or the experience level, the skill asks for it rather than guessing.

| Step | Skill | Needs | Produces |
| --- | --- | --- | --- |
| 1 | research-question-parser | Your idea file or notes | Numbered slots `RQ1`, `RQ2`, … (each slot keeps its ID through the whole run) |
| 2 | benchmark-finder | Each slot's question | An exact benchmark, the strongest baseline and its documented weaknesses, and a rewritten question; later `prior_work_<benchmark>.md` |
| 3 | research-readiness-advisor | Benchmark candidate, your goal, time budget and level | Readiness ratings, including the mechanism-validity gate; a redesign if needed; for READY projects a **provisional paper draft** (results `TBD`) |
| 4 | prior-work-checker | Question plus benchmark | PASS or FAIL, a novelty type, and `prior_work_evidence_<run-tag>_<RQk>.md`. **On FAIL, the slot goes back to step 2** for a new question under the same ID. |
| 5 | compute-planner | Experiment, time budget, level, `compute.md` | FITS DURATION / DOES NOT FIT, a phase-by-phase day estimate, and a difficulty rating |
| 6 | research-planner | All of the above | Final plans ordered **easiest to hardest**, each with hypothesis, benchmark, baseline, minimum experiment, and success and stop criteria |

**Save the pipeline's final report and the provisional drafts as Markdown
files** in a project folder. They are the inputs to workflow B
(paper-writer's examples name them `research_pipeline_report_vN.md` and
`provisional_paper_drafts_vN.md`).

You can call any group A skill on its own, for example
`/compute-planner` for a quick feasibility check. Only `research-pipeline`
enforces the full order and the FAIL loop.

## Workflow B: paper and experiment loop

These skills are **manual**: each runs only when you type its command, and
each handles **one project (one `RQk`) at a time**.

```
paper-writer (pre-experiment) → experiment-runner → paper-writer (post-experiment)
```

```
/paper-writer research_pipeline_report_v1.md provisional_paper_drafts_v1.md RQ1 venue: default-4
/experiment-runner paper_RQ1_v1.md
/paper-writer research_pipeline_report_v1.md paper_RQ1_v1.md RQ1 results: results_RQ1.md
```

| Step | Skill | Needs | Produces (in the project folder) |
| --- | --- | --- | --- |
| 1 | paper-writer | Plan file, provisional draft, project ID; optional `venue:` or page limit | `paper_RQ1_v1.md` (a complete paper through the Conclusion, numbers `TBD`) and `paper_RQ1_v1_latex/`, compiled and checked against the page limit |
| 2 | experiment-runner | `paper_RQ1_v1.md` | `experiment_plan_RQ1.md` (frozen), code and outputs in `experiments_RQ1/`, `results_RQ1.md`, and `future_experiments_RQ1.md` for ideas that are out of scope |
| 3 | paper-writer | The same plan file, the latest paper, `results: results_RQ1.md` | `paper_RQ1_v2.md` (and its LaTeX folder): the whole paper rewritten to match the measured results, including null or negative ones |

Rules worth knowing:

- No file is overwritten. New versions are saved as `_v2`, `_v3`, and so
  on.
- `experiment-runner` runs **only** what the paper already specifies. If a
  result is weak or negative, it proposes at most one small change and
  **waits for your approval** before rerunning anything.
- Venue options for `venue:`: `default-4`, `neurips-workshop-4`, `neurips`,
  `icml`, `iclr`, `cvpr`, `iccv`, `eccv`, `aaai`, `aaai27`, `aistats`,
  `uai`, `ijcai`, `acl-long`, `acl-short`, `colm`, `tmlr`.

## Group C: optional finishing tools

You run each of these on its own, on any paper file, after workflow B or on
a paper from somewhere else.

| Skill | Use it to | Command |
| --- | --- | --- |
| [paper-visuals](paper-visuals/README.md) | Add the minimum set of verified tables and figures | `/paper-visuals paper_RQ1_v2.md` → `paper_RQ1_v2_visuals.md`, `paper_RQ1_v2_figures/` |
| [paper-to-latex](paper-to-latex/README.md) | Convert a finished paper into an Overleaf-ready LaTeX project, ZIP and PDF | `/paper-to-latex paper_RQ1_v2.md` |
| [paper-results-reviser](paper-results-reviser/README.md) | Revise **any** draft against a folder of finished results, with an audit file | `/paper-results-reviser paper.md results/` |

Two useful combinations, both optional:

- **Figures, then LaTeX.** `paper-to-latex` accepts the figure folder from
  `paper-visuals` directly:
  ```
  /paper-visuals paper_RQ1_v2.md
  /paper-to-latex paper_RQ1_v2_visuals.md --visuals paper_RQ1_v2_figures/
  ```
- **Results that didn't come from experiment-runner.** Use
  `paper-results-reviser` instead of step 3 of workflow B.

## Full example

```
/research-pipeline   File: ideas.md  Time budget: 2 weeks  Experience level: Beginner
/paper-writer research_pipeline_report_v1.md provisional_paper_drafts_v1.md RQ1
/experiment-runner paper_RQ1_v1.md
/paper-writer research_pipeline_report_v1.md paper_RQ1_v1.md RQ1 results: results_RQ1.md
/paper-visuals paper_RQ1_v2.md                                            # optional
/paper-to-latex paper_RQ1_v2_visuals.md --visuals paper_RQ1_v2_figures/   # optional
```
