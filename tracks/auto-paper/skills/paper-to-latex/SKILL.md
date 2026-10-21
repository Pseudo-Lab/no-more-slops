---
name: paper-to-latex
description: "Manually invoked. Converts ONE existing, completed research paper (.md, .tex, .docx, or text-extractable .pdf) into a fully editable, publication-quality, Overleaf-ready LaTeX project (main.tex, references.bib, figures/, tables/, README.md) plus an Overleaf upload ZIP, a compiled PDF, and a conversion/validation report. Preserves wording, numbers, equations, tables, figures, citations, footnotes and appendices verbatim; optionally integrates separately supplied visuals (tables as CSV/TSV/Markdown/LaTeX, plots and diagrams as PDF/SVG/EPS/PNG/JPG) into the manuscript's own figure/table slots without altering them, flagging ambiguity and manuscript contradictions; fits a configurable main-paper page limit (default 4 pages, references starting on page 5) using only legitimate typesetting. A document conversion and typesetting skill, NOT a paper-writing or revision skill. Usage - /paper-to-latex <paper_file> [output_directory] [--visuals <file|dir> ...] [pages:N|pages:none] [paper:letter|a4] [template:keep|default|<path>] [engine:pdflatex|xelatex|lualatex]"
argument-hint: "<paper_file> [output_directory] [--visuals <file|dir> ...] [pages:N] [paper:letter|a4] [template:keep|default|<path>] [engine:<name>]"
---

# Paper to LaTeX

Convert ONE finished paper into an editable LaTeX project that compiles,
imports into Overleaf, and says exactly what the source says.

This skill **typesets**; it never writes, rewrites, summarises, expands, or
"improves" the paper. When in doubt between changing content and reporting a
problem, report the problem.

Skill directory (`SKILL_DIR`): the directory containing this file, normally
`~/.claude/skills/paper-to-latex/` (on Windows
`C:\Users\<user>\.claude\skills\paper-to-latex\`). Resolve it to an absolute
path once and use it for every script call below.

| Path | Purpose |
| --- | --- |
| `scripts/detect_tools.py` | Detect compilers, bibtex/biber, pandoc, poppler tools, pypdf |
| `scripts/extract_source.py` | Extract source into `_conversion/` (plain text, pandoc draft, media, inventory) |
| `scripts/lint_project.py` | Static checks: paths, figures, cite keys, labels, forbidden spacing/font hacks |
| `scripts/compile_and_check.py` | Compile, parse log/blg, count pages, check main length and references start page |
| `scripts/check_page_limit.py` | Venue-aware page-limit gate on the compiled PDF (≤ N pages counted, formatting/template checks, required sections/labels, iteration cap; exit codes 0–6; used by paper-writer and the global Stop hook) |
| `scripts/compare_content.py` | Source vs compiled-PDF comparison: numbers, sentences, added sentences/text; `--visuals` treats included supplied visuals as an allowed source |
| `scripts/visuals.py` | Supplied visuals: `inventory` (classify, match to manuscript slots, conflicts), `convert` (vector-first, verified), `table` (CSV/TSV/MD → verbatim LaTeX table), `check` (placement, captions, refs, numbers, legibility, clipping risk, renders) |
| `scripts/make_overleaf_zip.py` | Build Overleaf ZIP; checks every included visual is inside; `--verify` re-lints and recompiles it from a clean extract |
| `templates/main_twocolumn.tex` | Default two-column template with page-limit markers |
| `templates/README_template.md` | Project README with Overleaf import steps |
| `references/conversion_rules.md` | Detailed rules: formatting vs content, per-format notes, bibliography, fitting ladder, integrity checklist |
| `references/report_template.md` | Required structure of `conversion_report.md` |

Read `references/conversion_rules.md` before Step 4 of every run (§6 too
when visuals are supplied).

## 1. Inputs and argument handling

Raw arguments: `$ARGUMENTS`

Parse with shell-style quoting (paths may contain spaces):

- `paper_file` (required) = `$0`
- `output_directory` (optional) = `$1` if present, not a `key:value` option,
  and not `--visuals`
- `visual_inputs` (optional): every path after `--visuals` up to the next
  option (`--...` or `key:value`). `--visuals` may appear more than once, and
  `visuals:<path>` is accepted as an alternative. Each path is a file or a
  directory (searched recursively). Without `--visuals` the skill behaves
  exactly as before (backward compatible).

Examples:

```
/paper-to-latex paper.md
/paper-to-latex paper.md out_dir pages:6
/paper-to-latex paper.md --visuals figures/ tables/
/paper-to-latex paper.md --visuals figure1.pdf workflow.svg results_table.tex
/paper-to-latex paper.md paper_latex --visuals paper_figures/ pages:4
```

The output of `/paper-visuals` (`<stem>_figures/`) is a valid `--visuals`
directory.

Options (anywhere after `paper_file`; natural-language equivalents such as
"6-page limit" or "A4" count the same):

| Option | Default | Meaning |
| --- | --- | --- |
| `pages:N` | `4` | Required main-paper length in pages (abstract, figures, tables count; references excluded). References start on page N+1. |
| `pages:none` | | No page limit; references still start on a new page. |
| `paper:letter\|a4` | from source if stated, else `letter` | Paper size of the default template. |
| `template:keep\|default\|<path>` | `keep` if the source uses/names a template, else `default` | `keep` preserves the source's venue class/style; `<path>` = a user-supplied .cls/.sty/template .tex. |
| `engine:pdflatex\|xelatex\|lualatex` | `pdflatex` (switch only if the source needs Unicode fonts/fontspec) | LaTeX engine. |

Validation, before anything else:

1. If `paper_file` is missing or looks like an unexpanded placeholder, ask.
   Never search the disk for a substitute paper.
2. The file must exist and end in `.md`, `.markdown`, `.tex`, `.docx`, or
   `.pdf`. Otherwise stop and ask.
3. Output directory:
   - omitted → `<source_dir>/<paper_stem>_latex/`; if that exists and is
     non-empty, use `<paper_stem>_latex_2`, `_3`, ... and say so;
   - given and exists non-empty → ask before writing into it;
   - it must never be the source file itself or contain the source such that
     `main.tex`/`references.bib` would overwrite an input file. The source
     is **read-only** for the entire run.
4. If the paper is clearly unfinished (TBD results, placeholders, `XX`),
   convert it as-is, keep placeholders verbatim, and flag them in the report.
   Do not fill them. (Figure/table placeholders such as `[Figure 2 here]`
   are the exception: they are replaced by the matching supplied visual.)
5. Every `visual_inputs` path must exist; a missing one is reported, never
   guessed. Supplied files are read-only like the paper.

## 2. Hard rules

Never:

- rewrite, paraphrase, summarise, shorten, expand, reorder, or reinterpret text;
- change any number, unit, sign, CI, p-value, effect size, significance
  wording, hedge, hypothesis, limitation, or negative/null finding;
- add or "complete" citations, reference fields (DOIs, pages, venues),
  authors, affiliations, venue/conference names, submission info, dates,
  acknowledgements, or captions that the source lacks;
- fix suspected errors in the source (report them in §6 of the report);
- drop figures, tables, footnotes, equations, appendices, or references;
- convert pages or text blocks into images; every word, table, and equation
  stays editable LaTeX (figures are image/PDF files only when they are
  figures in the source);
- shrink fonts, alter line spacing, margins, or text block, or use negative
  `\vspace` to meet the page limit;
- claim an Overleaf upload, a successful compile, a page count, or a
  validation that was not actually performed and observed;
- write outside the output directory (scratch work goes in
  `<out>/_conversion/` or the session scratchpad);
- silently omit a supplied visual: every supplied asset ends with a recorded
  decision (`include` / `exclude` with reason / `ask`) and appears in the report;
- redraw, re-plot, retype, crop, recolour, or otherwise edit a supplied figure
  when the file itself can be used; change data, axes, legends, error bars,
  or workflow boxes/arrows; retype a table from an image without approval;
- invent a caption, label text, or methodological detail for a visual: captions
  come verbatim from the manuscript, a caption sidecar, a caption inside the
  supplied file, or the user;
- choose silently between a supplied visual and the manuscript when they
  disagree (flag the discrepancy and ask).

Content changes of any kind need explicit user approval in chat, obtained
before they are made, and are listed in the report with the approval.

## 3. Workflow

Run every step in order. Use `python` (or `py -3`) to run scripts.

### Step 1 — Detect tools

```
python "<SKILL_DIR>/scripts/detect_tools.py"
```

Record the route. If no LaTeX compiler exists, continue the conversion but
mark compilation, page count, citation resolution, and PDF comparison as
**UNVERIFIED** in the report (lint still runs). If `pandoc` is missing,
`.docx` cannot be converted reliably: stop and report. For `.pdf`, `pdftotext`
is required.

### Step 2 — Extract and read the source

```
python "<SKILL_DIR>/scripts/extract_source.py" "<paper_file>" "<out>"
```

Then read the **whole** source (for `.docx` read
`_conversion/source_markdown.md`; for `.pdf` read the PDF pages themselves and
`source_layout.txt`). Build a content inventory: title, authors (verbatim,
only if present), affiliations, abstract, every heading and its level, every
equation, table (with caption and every cell), figure (file + caption),
footnote, in-text citation, reference-list entry, appendix, and anything the
source marks as not part of the paper. Note the venue template if the source
names or uses one.

Stop and report (do not invent) if: the PDF is scanned/not extractable,
figures referenced by the source are missing (and not supplied via
`--visuals`), or the source is not a paper.

### Step 2b — Inventory supplied visuals (only with `--visuals`)

```
python "<SKILL_DIR>/scripts/visuals.py" inventory "<paper_file>" "<out>" <visual_path> [<visual_path> ...]
```

It writes `<out>/_conversion/visuals_manifest.json` and prints:

- **slots**: the manuscript's figures/tables (number, caption, in-text
  mentions, own image/table body, `[Figure N here]` placeholders);
- **assets**: every supplied visual (format variants such as `fig1.pdf` +
  `fig1.png` are grouped, vector preferred), with metadata (vector/raster,
  size, DPI, extracted text, table cells, sidecar caption
  `<name>.caption.txt`), a proposed slot, a score and the reasons;
- **issues**: `ASK` (unmatched, ambiguous, competing assets, table supplied as
  an image, multi-page PDF, unsupported format, slot with no visual),
  `DISCREPANCY` (supplied table vs the manuscript's own table, cell by cell),
  `VERIFY` (supplied file differs from the manuscript's own image), `WARN`
  (low-resolution raster, fonts not embedded, SVG `<foreignObject>`), `INFO`;
- non-visual files (scripts, data, notes) — listed, never included.

Then Read every supplied figure (PDF/PNG directly; render others) and every
supplied table, and confirm each proposed match against the manuscript's
caption, the surrounding text, and the numbers it quotes. The scores are
evidence, not decisions.

### Step 3 — Plan the conversion

Decide and note for the report: template (keep vs default), paper size,
citation mode (numeric vs author-year; BibTeX+natbib by default; BibLaTeX
only if the source project already uses it), equation numbering, placement of
appendices (after references), and every planned exclusion of non-paper
material. If an exclusion is not unambiguous, ask.

With supplied visuals, record a decision for **every** asset in
`visuals_manifest.json` (`assets[i].decision`; edit the JSON with Write/Edit):

| Field | Value |
| --- | --- |
| `action` | `include`, `exclude` (needs `reason`, e.g. "duplicate of Figure 2 in PNG"), or `ask` (needs `reason`; becomes a question to the user) |
| `slot` | manuscript slot, e.g. `figure:2`, `table:1` |
| `project_path` | e.g. `figures/workflow.pdf`, `tables/tab_results.tex` |
| `label` | e.g. `fig:workflow`, `tab:results` |
| `caption_text` | the caption **verbatim** (plain text as in the source) |
| `caption_source` | `manuscript`, `sidecar`, `asset_file`, `user`, or `none` — never generated |
| `environment` | `figure`, `figure*`, `table`, `table*` |
| `placement` | `main` (default) or `appendix` (only if the manuscript puts it there) |
| `conversion` | the JSON record printed by `visuals.py convert` (figures) |

Ask the user (batch all questions in one message) before building when:
an asset matches no slot, matches several, competes with another asset,
contradicts the manuscript (`DISCREPANCY`), differs from the manuscript's own
image in content, has no caption anywhere, is a table supplied only as an
image, or including it would be redundant (same content as another visual or
a manuscript table) or would push the main paper over the page limit.
Unambiguous matches proceed without asking. If the user does not answer an
inclusion question, keep the asset as `ask` and report it — never drop it
silently and never include it unconfirmed.

Float numbering: LaTeX numbers floats in source order. If the manuscript's
numbering does not follow the order in which its figures/tables appear,
`visuals.py check` reports "printed number differs"; ask the user (keep
numbering by placing floats in numbering order within their sections, or
renumber with approval).

### Step 4 — Build the project

Layout (relative paths only):

```
<out>/
├── main.tex
├── references.bib
├── figures/        source images, ASCII names without spaces
├── tables/         tab_<short_name>.tex, one table per file, \input from main.tex
└── README.md
```

1. Start from `templates/main_twocolumn.tex` (default) or the preserved
   source template. Fill title, authors (or leave `\author{}` empty),
   abstract, sections. Delete every `<<...>>` placeholder line that does not
   apply. Keep the `\clearpage` + `\phantomsection\label{pl:refsstart}`
   before the bibliography in **every** template (also venue templates) so
   page accounting works; if appendices exist, put them after the
   bibliography behind `\clearpage\appendix\phantomsection\label{pl:appendixstart}`.
2. Transfer text **verbatim** paragraph by paragraph, applying only the
   markup translation in `references/conversion_rules.md` §1–2. Escape
   LaTeX specials. Copy from `pandoc_draft.tex` where it helps, but never ship
   pandoc wrappers (`\tightlist`, `\hypertarget`, `longtable`, `\pandocbounded`)
   or its image paths (they are absolute paths into `_conversion/media/`).
   Write `.tex`/`.bib` files with the Write/Edit tools, not shell heredocs or
   `python -c` one-liners: shells can silently collapse `\\` to `\`.
3. Equations → LaTeX math (`equation`/`align` for numbered or referenced
   ones, `\[...\]` otherwise). Keep the source's symbols and numbering.
4. Tables → `tables/tab_*.tex` using `table`/`table*` + `tabular` +
   `booktabs`; caption verbatim, `\label{tab:...}`. Copy every cell exactly
   (including bold/underline marks, ±, CI brackets, footnote markers).
5. Figures → copy files into `figures/`; `\includegraphics[width=...\columnwidth]{name}`;
   caption verbatim; `\label{fig:...}`.
6. Bibliography → `references.bib` per `conversion_rules.md` §3 (fields only
   from the reference text; verbatim `note` for the remainder; numbering
   preserved with `\nocite` in source order + `unsrtnat`).
7. Cross-references → `\ref`/`\eqref` only where the printed number stays
   identical to the source.
8. `README.md` from `templates/README_template.md` (fill every `<<...>>`).
9. Supplied visuals (decision `include`), per `conversion_rules.md` §6:
   - figures: `python "<SKILL_DIR>/scripts/visuals.py" convert <asset> "<out>/figures" [--name <stem>]`
     — PDF/PNG/JPG are copied byte-for-byte, EPS→PDF, SVG→PDF (vector),
     TIFF/GIF/BMP/WebP→PNG. Store the printed JSON as `decision.conversion`.
     Exit 3 = no converter (e.g. SVG without Inkscape/rsvg/cairosvg/svglib):
     ask the user for a PDF/PNG export or permission to install a converter;
   - tables from CSV/TSV/Markdown:
     `python "<SKILL_DIR>/scripts/visuals.py" table <asset> "<out>/tables/tab_<name>.tex" --caption-file <file> --label tab:<name> [--wide auto|yes|no]`
     (the caption file holds the verbatim caption as LaTeX: escape `% & _ #`).
     It refuses to finish if any number changed. A supplied `.tex` table is
     copied unchanged; wrap it in `table`/`table*` by hand only if it has no float;
   - place each float at the manuscript's placeholder or right after the
     paragraph that first mentions it; replace "Figure N"/"Table N" in the text
     with `Figure~\ref{...}` only when the printed number stays the same;
   - `figure`/`table` for column-width content; `figure*`/`table*` for wide
     diagrams/tables; widths relative to `\columnwidth`/`\textwidth`; never
     `trim`/`clip`/`viewport`, never `width`+`height` without `keepaspectratio`;
   - keep the template's `\typeout{PL-LAYOUT ...}` line (used by `visuals.py check`).

### Step 5 — Lint

```
python "<SKILL_DIR>/scripts/lint_project.py" "<out>"
```

Fix every ERROR (missing files, undefined keys/labels, absolute paths,
forbidden spacing/font commands). Explain any remaining WARN in the report.

### Step 6 — Compile and check layout

```
python "<SKILL_DIR>/scripts/compile_and_check.py" "<out>" --pages N [--engine E]
```

(`--pages 0` for `pages:none`.) Resolve all LaTeX errors, undefined
citations/references, missing files, BibTeX errors, and overfull boxes > 1pt
(fix via line-break-friendly markup such as `\allowbreak` in long URLs/
identifiers, table `p{}` columns, `\url` — never by rewording).

The script kills the whole build tree after `--timeout` seconds (default 600).
A timeout or a very slow first build usually means the TeX distribution is
installing a missing package on the fly or generating bitmap fonts (MiKTeX:
`miktex-makepk`/`gsf2pk` in the MiKTeX log directory). Re-run once after the
install completes; if it still stalls, report the package/font name to the
user. Never change system TeX configuration yourself.

Look at the PDF: render it with
`pdftoppm -r 60 -png "<out>/main.pdf" "<out>/_conversion/render/p"` (or
higher `-r` for detail) and Read pages 1 to N+1 at minimum. Check reading
order, float placement, table/figure legibility, equation rendering, column
overflow, and that the bibliography reproduces the source's reference text
(capitalisation, see `conversion_rules.md` §3).

### Step 6b — Check supplied visuals (only with `--visuals`)

```
python "<SKILL_DIR>/scripts/visuals.py" check "<out>"
```

Verifies, per asset: a decision exists; included files exist, are
`\includegraphics`'d / `\input`, and are byte-identical to the supplied file
or carry a verified conversion record (SVG text labels and aspect ratio kept);
the LaTeX caption equals the recorded verbatim caption; the label exists, is
`\ref`'d wherever the manuscript mentions the visual, and prints the
manuscript's number; the float lies inside the main paper; no
`trim`/`clip`/distortion; rendered width fits the column/text block;
effective in-figure font size (PDF figures, ERROR < 4pt, WARN < 5.5pt) and
effective raster DPI (WARN < 150); every table number equals the supplied
table's numbers; figure words still found on the page (clipping hint);
content touching the asset's own edge (already cropped in the source?).
It renders each page holding a visual (`visual_<label>_p<page>.png`) and each
supplied figure (`asset_<name>.png`) into `_conversion/render/`.
**Read every render** and compare each figure with its asset render: labels,
arrows, legends, tick labels and error bars must be complete and unclipped;
table cells must read correctly. Fix every ERROR; explain every WARN.

### Step 7 — Fit the page limit

Using `page_check` from Step 6, follow the fitting ladder in
`conversion_rules.md` §4, recompiling after each change and logging the
measurement. Requirements: main paper exactly N pages (last main page not
blank), references start on page N+1 (enforced by `\clearpage`), references
may take any number of pages.

- **Overflow after the ladder:** stop and ask the user with measured
  overflow and options. Do not cut or move content without approval. With
  supplied visuals, list each visual's page cost (e.g. "Figure 3 as
  `figure*` ≈ 0.3 page") so the user can decide which (if any) goes to an
  appendix; never drop or shrink a visual below the legibility limits to fit.
- **Underflow:** never pad. Report and ask whether the shorter main paper
  (references on page X+1) is acceptable.

**Programmatic verification (mandatory; added 2026-10-17).** After the
ladder, write `<out>/pagelimit.json` (`{"venue": "<profile>", "limit": N,
"main": "main.tex", "required_sections": [...], "required_labels":
[...]}`). Venue profiles live in
`~/.claude/skills/paper-writer/references/venue_profiles.json`; the
default is `default-4` = this skill's template. Then run:

```
python "<SKILL_DIR>/scripts/check_page_limit.py" "<out>" --reset
```

It compiles and counts pages from the actual PDF (via `pl:refsstart` or
`pl:bodyend`). It flags forbidden formatting and template mismatches
(exit 3), missing required sections or labels (exit 6), and overflow
(exit 1, with an overflow estimate in words and lines). Report its
status and counted pages in the conversion report.

This skill still never cuts content. On exit 1 after the ladder, ask the
user, as above. The global Stop hook
(`~/.claude/hooks/page_limit_gate.py`) will block the first attempt to
end the turn while the PDF is over the limit. Answer it by restating
that the overflow needs the user's decision; a second stop with an
unchanged source is allowed. The content cuts themselves belong to
paper-writer (Step 9b) or paper-results-reviser.

### Step 8 — Compare content against the source

```
python "<SKILL_DIR>/scripts/compare_content.py" "<out>/_conversion/source_plain.txt" "<out>/main.pdf" --out "<out>/_conversion/compare_report.json" [--visuals "<out>/_conversion/visuals_manifest.json"]
```

With `--visuals`, text, numbers and supplied captions of assets decided
`include` count as an allowed source (reported as "explained by supplied
visuals", not as added content), and `[Figure N here]` placeholders are
treated as replaced. Excluded/undecided assets are not allowed sources.

If non-paper material was excluded, compare against a copy of
`source_plain.txt` with exactly those parts removed (save it as
`_conversion/source_compare.txt` and say so). pandoc's plain text puts all
footnotes at the **end of the file**; keep that footnote block when cutting
a trailing section.

Output categories and how to act on them:

- **MISSING sentence** / **missing number** / **missing table cell** /
  **missing quoted reference title** → fix (restore verbatim) or explain.
  Known benign causes: a footnote mark fused with a preceding number in PDF
  text (`10^{-5}` + mark 1 → "10-5.1"), a math-only table cell (Δ, $p$),
  newtx math glyphs that `pdftotext` cannot extract. Each one must be
  confirmed by looking at the PDF, not assumed.
- **math (manual check)** → the prose around the math was found; verify the
  math itself symbol by symbol against the source.
- **near** → usually a float or page break inside the sentence; confirm.
- **references** → the bib style reformats entries (coverage < 1 is normal);
  titles must be present; check each entry's fields against the source.
- **added?** → must be explained (section numbers, "Figure 1:", headers,
  reference formatting) or removed.
- **ADDED sentence** / **decimal/% number only in PDF** → content that is in
  neither the source nor an included visual: remove it (these fail the run).

Then also:

- verify tables cell by cell, equations symbol by symbol, and each in-text
  citation → reference mapping manually against the source (the script does
  not see inside math or images);
- run the integrity checklist in `conversion_rules.md` §5.

Repeat Steps 5–8 until clean or until only issues that need the user remain.

### Step 9 — Package for Overleaf

```
python "<SKILL_DIR>/scripts/make_overleaf_zip.py" "<out>" --verify [--engine E]
```

The ZIP has `main.tex` at its root and only source files. It fails if an
included supplied visual is missing from the archive or any asset is
undecided. `--verify` proves it compiles from a clean extraction. Do **not** upload it anywhere; say it is
ready for Overleaf → New Project → Upload Project. If the engine is not
pdfLaTeX, the README must tell the user to switch the Overleaf compiler.

### Step 10 — Report

Write `<out>/conversion_report.md` following `references/report_template.md`.
It must include: source file, output directory, main paper page count,
references page count, compilation status, citation validation status,
missing or unresolved content, every deviation from the original, and (with
`--visuals`) the supplied-visuals table: every asset, its decision, slot,
label/number, page, conversion, caption source, and open questions. State
plainly what was verified and what is UNVERIFIED and why.

Final chat message (concise): output directory, ZIP path, PDF path (or why
none), page check result, compilation/citation status, content-comparison
result, deviations, and any question that needs the user's decision.

## 4. When to stop and ask

- Page limit cannot be met by legitimate typesetting (overflow) or the main
  paper is shorter than the limit (underflow).
- A venue template/class is referenced but not available.
- Source content is ambiguous or unreadable (equation symbols in PDFs,
  broken tables, missing figures, missing references for cited numbers).
- The source contains tracked changes, multiple versions, or material whose
  paper/non-paper status is unclear.
- Any change that would alter content.
- Supplied visuals: unmatched, ambiguous, competing, redundant, contradicting
  the manuscript, uncaptioned, table-as-image, unconvertible format, or
  inclusion that would exceed the page limit (see Step 3).
