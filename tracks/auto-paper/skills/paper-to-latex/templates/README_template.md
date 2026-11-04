# <<TITLE>> — LaTeX project

Converted from `<<SOURCE_FILE_NAME>>` by the `paper-to-latex` skill on <<DATE>>.
The wording, results, and references are those of the source paper; only the
typesetting was changed (see `conversion_report.md` in the output directory
for every deviation).

## Contents

| Path | Purpose |
| --- | --- |
| `main.tex` | Main document (compile this) |
| `references.bib` | Bibliography (BibTeX, style `<<BST>>`) |
| `figures/` | Figure files referenced by `\includegraphics` |
| `tables/` | One `.tex` file per table, pulled in with `\input` |

## Import into Overleaf

1. Overleaf → **New Project** → **Upload Project**.
2. Select `<<ZIP_NAME>>` (do not unzip it first).
3. Overleaf detects `main.tex` as the main document. If not: Menu → *Main document* → `main.tex`.
4. Menu → *Compiler*: **<<ENGINE_LABEL>>** (default on Overleaf). Click **Recompile**.

This project has **not** been uploaded to Overleaf by the conversion tool; the
ZIP is ready for you to upload.

## Compile locally

```bash
latexmk -pdf main.tex
```

or `pdflatex main && bibtex main && pdflatex main && pdflatex main`.

## Page layout

- Main paper: <<PAGES>> pages (pages 1–<<PAGES>>), including abstract, figures and tables.
- References start on page <<PAGES_PLUS_1>> (forced by `\clearpage` before the bibliography).
- <<APPENDIX_NOTE>>

The page-limit boundary is the `\label{pl:refsstart}` marker in `main.tex`.
When editing, keep the body at 10pt and the 0.75in margins; fit the limit by
editing the content itself, not by shrinking fonts or spacing.
