# Conversion and Validation Report

- **Source file:** `<path>` (format: md / tex / docx / pdf; never modified)
- **Output directory:** `<path>`
- **Date:** YYYY-MM-DD
- **Template:** default two-column (article, 10pt, Times, 0.75in margins) | preserved source template `<name>`
- **Page limit requested:** N main pages, references from page N+1

## 1. Summary

| Item | Result |
| --- | --- |
| Compilation | SUCCESS / FAILED / UNVERIFIED (no compiler) — engine, route |
| Main paper page count | X pages (required N) — PASS/FAIL/UNVERIFIED |
| References start page | page R (required N+1) — PASS/FAIL/UNVERIFIED |
| References page count | Y pages |
| Appendix | none / Z pages after references (pages a–b) |
| Total PDF pages | T |
| Citation validation | all K cited keys resolved / list problems; numbering preserved: yes/no |
| Cross-references | all resolved / list |
| Missing figures | none / list |
| Overfull boxes > 1pt | count (list the largest) |
| Content comparison | S sentences: E exact, N near, M missing; numbers: P source tokens, Q missing |
| Supplied visuals | V assets: I included, E excluded (reasons), A awaiting the user; visuals check errors: 0 |
| Overleaf ZIP | `<path>` — lint OK, all included visuals inside, clean recompile from extracted ZIP: OK/FAILED/NOT RUN |
| Overleaf upload | **Not uploaded** (ZIP ready for Overleaf → New Project → Upload Project) |

## 2. Deliverables

- `main.tex`, `references.bib`, `figures/` (n files), `tables/` (m files), `README.md`
- `<name>_overleaf.zip`
- `main.pdf` (compiled) — or "not produced"
- this report

## 3. Content inventory (source → output)

| Element | Source | Output | Notes |
| --- | --- | --- | --- |
| Sections / subsections | | | |
| Equations (display) | | | |
| Tables | | | |
| Figures | | | |
| Footnotes | | | |
| References (list entries) | | | |
| In-text citations | | | |
| Appendices | | | |

## 3b. Supplied visual materials (only with `--visuals`)

Supplied paths: `...` — N files: V visual assets (after grouping format
variants), O other files (scripts/data/notes, not included).

| Asset (variants) | Decision | Slot → printed no. | Label | Page | File in project | Conversion / identity | Caption source | Checks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fig1_accuracy_ci.pdf (+ .png) | include | figure:1 → Figure 1 | fig:accuracy | 2 | figures/fig1_accuracy_ci.pdf | byte-identical copy | manuscript | font ≥ 7.2pt, scale 1.03, no clipping |
| results_table.csv | include | table:1 → Table 1 | tab:results | 3 | tables/tab_results.tex | csv → booktabs table*, 20/20 numbers unchanged | manuscript | — |
| extra_ablation.png | ask | — | — | — | — | — | — | unreferenced by manuscript |

- Discrepancies with the manuscript (cell / value / which file) — none or list, with the user's answer
- Open questions for the user — list
- Renders inspected: `_conversion/render/...` (list)

## 4. Deviations from the original

### 4a. Formatting changes (no effect on content)
- e.g. manual section numbers replaced by LaTeX numbering (same numbers)
- e.g. tables typeset at \small uniformly; appendix moved after references

### 4b. Excluded material
- e.g. "Revision guide (not part of the paper)" — marked as non-paper in source

### 4c. Content changes approved by the user
- none / list with the approval quote

## 5. Missing or unresolved content
- e.g. reference [7] cited in text but absent from the reference list (not created)
- e.g. equation 3 symbol ambiguous in PDF source; literal reading kept
- e.g. near-match sentences caused by math rendering (listed in `_conversion/compare_report.json`)

## 6. Issues found in the source (reported, NOT fixed)
- e.g. Table 2 reports 0.81 while §5 text says 0.18

## 7. Page-limit fitting log
- measurements after each step of the fitting ladder; final state; any conflict and the options offered

## 8. Validation commands run
```
python detect_tools.py
python extract_source.py ...
python lint_project.py ...
python compile_and_check.py ... --pages N
python visuals.py inventory ... / convert ... / table ... / check ...   (with --visuals)
python compare_content.py ... [--visuals ...]
python make_overleaf_zip.py ... --verify
```
Anything not run is listed here as UNVERIFIED with the reason.
