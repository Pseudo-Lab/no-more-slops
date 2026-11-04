# paper-to-latex

Converts **one finished paper** (`.md`, `.tex`, `.docx`, or a `.pdf` with
extractable text) into an editable, **Overleaf-ready LaTeX project** that
compiles. It keeps wording, numbers, equations, tables, figures,
citations, footnotes and appendices **verbatim**, and fits a main-body page
limit (default 4 pages, with references starting on page 5) using
legitimate typesetting only.

It only typesets. It never rewrites, summarises or "improves" the content.
When in doubt it reports a problem instead of changing the text.

## How to use it

```
/paper-to-latex <paper_file> [output_directory] [--visuals <file|dir> ...] [pages:N|pages:none] [paper:letter|a4] [template:keep|default|<path>] [engine:pdflatex|xelatex|lualatex]
```

Examples:

```
/paper-to-latex paper.md
/paper-to-latex paper.md out_dir pages:6
/paper-to-latex paper.md --visuals figures/ tables/
/paper-to-latex paper.md paper_latex --visuals paper_figures/ pages:4
/paper-to-latex paper.docx paper:a4 template:my_venue.cls
```

| Option | Default | Meaning |
| --- | --- | --- |
| `output_directory` | `<source_dir>/<stem>_latex/` (or `_2`, `_3`… if it already exists) | Where the project is written. The source file is never touched. |
| `--visuals` | none | Tables (CSV/TSV/MD/LaTeX) and plots or diagrams (PDF/SVG/EPS/PNG/JPG) placed into the paper's own figure and table slots. Ambiguous matches and contradictions with the text are flagged. |
| `pages:N` / `pages:none` | `4` | Main-paper length. References are excluded and start on page N+1. |
| `paper:` | from the source, else `letter` | Paper size |
| `template:` | `keep` if the source names one, else `default` | Keep the venue class, use the bundled two-column template, or use your own `.cls`/`.sty`/`.tex` |
| `engine:` | `pdflatex` | Switches only if Unicode fonts are needed |

If the paper still contains `TBD` or `XX` placeholders, they are kept
as-is and flagged. Figure placeholders like `[Figure 2 here]` are filled
from `--visuals` when a match exists.

## Output

- `main.tex`, `references.bib`, `figures/`, `tables/`, and a `README.md`
  with Overleaf import steps
- A compiled PDF
- An Overleaf upload ZIP, re-verified from a clean extract
- `conversion_report.md`: what was converted, lint and compile results,
  page fit, a content comparison between source and PDF, and flags

## Requirements

A LaTeX distribution (pdflatex or another engine, plus bibtex or biber).
Pandoc, poppler tools and `pypdf` are used when available. Step 1 runs
`detect_tools.py` and reports anything missing.

## Scripts (`scripts/`)

| Script | Purpose |
| --- | --- |
| `detect_tools.py` | Finds compilers, pandoc, poppler, pypdf |
| `extract_source.py` | Extracts the source into `_conversion/` |
| `lint_project.py` | Paths, cite keys, labels, forbidden spacing or font hacks |
| `compile_and_check.py` | Compiles, parses logs, counts pages |
| `check_page_limit.py` | Venue-aware page-limit gate (exit codes 0–6). **Also used by paper-writer and the global Stop hook.** |
| `compare_content.py` | Checks the compiled PDF against the source for numbers and sentences |
| `visuals.py` | Inventory, conversion, tables and checks for supplied visuals |
| `make_overleaf_zip.py` | Builds and verifies the ZIP |

Templates are in `templates/` (`main_twocolumn.tex`,
`README_template.md`). The rules are in `references/conversion_rules.md`
and `references/report_template.md`.
