# Conversion rules (paper-to-latex)

Detailed rules referenced from SKILL.md. The governing principle: **the LaTeX
output must say exactly what the source says.** Only typesetting changes.

## 1. What counts as "formatting" vs "content"

Allowed without asking (record each in the report under *Formatting changes*):

- Markup translation: Markdown/Word/PDF structure → `\section`, `\subsection`,
  `itemize`/`enumerate`, `\emph`, `\textbf`, `\footnote`, `\url`.
- Dropping manual heading numbers ("## 3 Method" → `\section{Method}`), because
  LaTeX numbers sections. Keep the same order and hierarchy, so the numbers
  stay the same. If the source numbering is irregular (skips, "3a"), keep it
  with `\section*{3a ...}` instead and say so.
- Replacing manual cross-references ("Table 2", "Eq. (3)", "Section 4") with
  `Table~\ref{tab:x}` only when the resulting number is identical. Verify it
  in the compiled PDF.
- Unicode → LaTeX (`α` → `$\alpha$`, `≤` → `$\le$`, `±` → `$\pm$`,
  `×` → `$\times$`, `–` → `--`, `—` → `---`, curly quotes → ``...'').
- Escaping LaTeX specials in text: `% & # _ $ { } ~ ^ \`.
- Float placement (`[t]`, `[!t]`, `[h]`), `figure` vs `figure*`, `table` vs
  `table*`, and moving a float a short distance in the source. Never move a float
  out of its section.
- Table typesetting with `booktabs` rules, column alignment (`l c r`,
  `S`-free), `\multicolumn` for spanning headers that exist in the source.
- Caption style handled by the `caption` package (`font=small` is part of the
  template and applies to all captions uniformly).
- Moving appendices after the references (standard venue convention). Report it.
- Removing material that the source itself marks as not part of the paper
  (e.g. "Revision guide (not part of the paper)", editor notes, TODO
  checklists). List every exclusion in the report. If in doubt, ask.

Requires explicit user approval (stop and ask):

- Any change to wording, claims, numbers, units, CIs, p-values, significance
  wording, hedges, limitations, hypotheses, or conclusions.
- Shortening, merging, or removing any paragraph, figure, table, footnote,
  equation, or reference to meet the page limit.
- Correcting apparent errors in the source (typos in numbers, inconsistent
  values between text and table, broken arithmetic). **Report them; do not fix.**
  Obvious spelling typos in prose may also be reported, not fixed.
- Converting a table into a figure or vice versa.
- Adding any citation, reference, author, affiliation, venue, date, funding,
  or acknowledgement that the source does not contain.

## 2. Format-specific notes

### Markdown (.md)
- `extract_source.py` writes `pandoc_draft.tex`: use it as a quarry for
  escaping, math, and tables, but assemble `main.tex` by hand from the
  template; pandoc's `longtable`, `\tightlist`, `\hypertarget` wrappers and
  `\pandocbounded` must not survive into the output.
- Inline math `$...$` and display `$$...$$` → keep TeX verbatim; display math
  becomes `equation` (numbered) when the source numbers it or refers to it,
  otherwise `equation*`/`\[ \]`. Do not number equations the source leaves
  unnumbered unless they are referenced.
- Pipe tables → `tables/tab_<n>.tex` (`tabular` inside `table`), caption text
  verbatim from the source caption line ("Table 2: ..." or the line before /
  after). If the source has no caption, use none (do not invent one); a label
  is fine.
- `![alt](path)` → copy the image to `figures/` (keep the file name, make it
  ASCII and space-free) and use the alt text/caption only if it is the source's
  caption.
- Text in code spans → `\texttt{...}` (escape `_`), fenced code →
  `verbatim` (or `lstlisting` if listings is loaded).

### LaTeX (.tex)
- If the source already uses a venue class/style (`neurips_2024.sty`,
  `acl.sty`, `IEEEtran`, `acmart`, `llncs`, ...): **keep it**. Copy the
  `.sty`/`.cls`/`.bst` files that are next to the source. If one is
  referenced but missing locally, do not fabricate it: report it and ask the
  user to provide it (Overleaf has some classes preinstalled; say which
  ones are standard on TeX Live: `IEEEtran`, `acmart`, `llncs`, `elsarticle`,
  `revtex4-2`).
- Flatten nothing unnecessarily: keep the author's macros (`\newcommand`).
  Only restructure into `figures/`, `tables/`, and `references.bib`.
- `thebibliography` environment in the source: convert entries to
  `references.bib` following §3, keeping keys = the original `\bibitem` keys.

### Word (.docx)
- Use pandoc's output for structure and OMML→LaTeX math, then verify every
  equation against `source_markdown.md`. Images come out in
  `_conversion/media/`; EMF/WMF images must be converted (e.g. via Inkscape
  if available) or reported — never dropped silently.
- Word fields for citations (Zotero/EndNote/Mendeley) appear as plain text:
  rebuild citations from the visible citation text and the reference list.
- Tracked changes / comments: pandoc accepts changes by default. If the
  document contains tracked changes, ask the user whether the accepted or
  original state is wanted.

### PDF (.pdf)
- Only proceed when the text is extractable (`extract_source.py` warns on
  scanned PDFs). Reading order in two-column PDFs must be checked against
  `source_layout.txt`.
- Equations: rebuild LaTeX from the visual PDF (render the page region with
  `pdftoppm -r 200 -f p -l p -x X -y Y -W W -H H -png` into `_conversion/` and
  Read the image). If a symbol is ambiguous, keep the most literal reading and
  list it under *Unresolved* in the report.
- Figures: raster images via `pdfimages`; vector figures by cropping the
  figure region only (`pdftoppm -r 300 ... -png` or `pdftocairo -pdf` with
  crop box). Never include a whole page as an image.
- Tables: rebuild as `tabular` from the PDF; verify every cell value against
  the PDF image.

## 3. Bibliography

- One `references.bib`; BibTeX + natbib by default (`unsrtnat` numeric,
  `plainnat` author-year). Use BibLaTeX only if the source project already
  does. Never mix.
- Every entry must come from the source's reference list. Fill only fields
  that are stated in the reference text. Do not look up, complete, or
  "correct" DOIs, pages, venues, years, or author lists.
- Parsing a reference string:
  - Clear structure → `@article`/`@inproceedings`/`@misc` with `author`,
    `title`, `journal`/`booktitle`/`howpublished`, `year`, `url`, `eprint`.
  - Any remainder that does not fit a field (e.g. "Code and data: <url>
    (released result files ...)") → `note = {...}` verbatim.
  - Unparseable → `@misc{key, note = {<entire reference text verbatim>}}`.
  - Author lists ending in "et al." → keep `and others`.
- Preserve the source's title capitalisation exactly: wrap every `title`
  (and `booktitle`) in double braces, `title = {{Compute-Efficient NLP}}`.
  Styles such as `unsrtnat`/`plainnat` otherwise lowercase titles
  ("Compute-efficient nlp"), which changes the reference text.
- The bibliography style re-orders/abbreviates name and field presentation
  (e.g. "Doe, J." → "J. Doe", added "In", "pages"). This is standard
  bibliography formatting; state it once in the report. The *content* of
  each field must match the source.
- Keys: `firstauthorYEARword` (ASCII), stable, unique.
- **Numbering:** numeric sources must keep their numbers. Use `unsrtnat` and
  put `\nocite{k1,...,kN}` (keys in the source's list order) immediately after
  `\begin{document}`; then [n] in the output equals [n] in the source. Verify
  in the compiled PDF that each in-text number points to the same work.
- Author-year sources: `\citep`/`\citet` must reproduce the source's
  parenthetical vs. narrative usage.
- References listed but never cited in the source must still be printed
  (`\nocite`). Citations to numbers absent from the list → report, do not
  create an entry.

## 4. Page-limit fitting ladder

Measure first (`compile_and_check.py`). Then, in this order, using only
legitimate typesetting moves, recompiling after each:

1. Float placement: `[t]` for most floats; `figure*`/`table*` for wide
   content at the top of a page; place each float right after the paragraph
   that first references it.
2. Figure sizing: width relative to `\columnwidth`/`\textwidth` so that
   the smallest text in the figure stays at roughly 7–8pt or larger
   (≥ 0.8\columnwidth for typical plots). Do not crop data out of figures.
   `visuals.py check` reports the effective in-figure font size
   (`effective_font_size_pt_p10`) of PDF figures: aim for ≥ 6pt; it errors
   below 4pt. A wide, short diagram scaled to `\textwidth` with in-figure
   text far above body size (> 11pt) can legitimately be narrowed
   (e.g. `0.85\textwidth`) to save vertical space. Choosing `figure` vs
   `figure*` for a diagram is a placement decision, not a content change.
3. Table layout: `booktabs`, `@{}` outer padding removal, `\tabcolsep` no
   lower than 4pt, line breaks inside long header cells, `p{}` columns.
   Table font may be `\small` (9pt) **uniformly for all tables** — record it.
   Never `\footnotesize` or smaller, `\resizebox`, or `\scalebox` without
   approval.
4. Long display equations: `split`/`multline`/`aligned` line breaks.
5. Widows/orphans and ragged float pages: reorder float placement, not text.
6. Lists: `enumitem` with `topsep=2pt, itemsep=1pt` at most (still
   readable); record it.

Forbidden at every step (lint_project.py flags them): body font < 10pt,
`\linespread`/`\baselinestretch`, `\fontsize`, geometry/margin/textheight
edits, `\enlargethispage`, negative `\vspace`, `\scriptsize`/`\tiny`,
removing or abbreviating content, deleting figures/tables, moving main-paper
content into an appendix.

**Overflow** (main paper > limit after the ladder): stop. Report the measured
overflow (e.g. "main text ends 0.4 columns into page 5"), what was tried, and
offer options — (a) user shortens/approves specific cuts, (b) move named
items to an appendix (content change: needs approval), (c) raise the page limit,
(d) accept overflow. Do not choose for the user.

**Underflow** (main paper < limit): do not pad with blank space, `\vfill`,
blank pages, or enlarged fonts. Allowed: restore figures/tables to their
natural size. If it is still short, report "main paper is X pages; the
requirement 'exactly N' cannot be met without adding content" and leave the
references starting on the page after the main text (page X+1). Ask the user
whether that is acceptable.

## 5. Scientific-integrity checklist (run before reporting)

- [ ] `compare_content.py` reports 0 missing numbers, or each one is explained
      (e.g. "0.5" rendered as `$\frac{1}{2}$` in the source too).
- [ ] Every MISSING sentence is resolved (restored) or explained (math
      rendering / approved exclusion).
- [ ] Every table cell checked against the source table (values, signs,
      bold/underline marking best results, ± and CI brackets, units, footnote marks).
- [ ] Hypotheses, limitations, negative/null findings, and hedging words
      ("may", "suggests", "not significant") are present verbatim.
- [ ] Each in-text citation points to the same reference as in the source.
- [ ] Figure captions verbatim; figure files are the source's own images.
- [ ] Nothing was added: no new citations, numbers, claims, affiliations,
      venue names, or acknowledgements.
- [ ] (With `--visuals`) every supplied asset has a decision; `visuals.py check`
      has 0 errors; every render was looked at; every DISCREPANCY and ASK went
      to the user; the report lists every asset.

## 6. Supplied visual materials (`--visuals`)

### 6.1 Matching assets to the manuscript
Evidence, strongest first: the manuscript's own image path; a figure/table
number in the file name (`fig2_*`, `table1.csv`); the caption sidecar
(`<name>.caption.txt|md|tex`) or a caption inside the file; overlap between
the manuscript caption and the file name / header row / figure text; for
tables, numbers shared with the manuscript's table or quoted in its text.
`visuals.py inventory` scores these; Claude confirms by reading both. A slot
with exactly one plausible asset proceeds. Everything else is a question.

### 6.2 Inclusion rules
- Include an asset only into a slot the manuscript already has (a caption,
  a mention, a placeholder, or its own image). An asset the manuscript never
  refers to is `ask` — adding a figure changes the paper.
- Redundancy: two assets with the same content (format variants, an identical
  hash, a PNG of a supplied PDF, a figure that shows exactly a manuscript
  table) → include one (vector first), mark the others `exclude` with the
  reason. If they differ in content, ask.
- The manuscript's own embedded image and a supplied file for the same slot:
  if they render identically (vector re-export of the same plot), prefer the
  vector file and say so; if anything differs (values, axes, legend, arrows,
  styling that changes meaning), it is a DISCREPANCY → ask.
- Manuscript tables vs supplied tables: `inventory` compares cell by cell
  (or by numbers if shapes differ). Any difference → DISCREPANCY → ask which
  is authoritative; never merge or "correct" either.
- Page budget: if including a supplied visual would overflow the page limit,
  report its page cost and ask; do not drop it, shrink it below the
  legibility limits, or move it to an appendix without approval.

### 6.3 Format handling (`visuals.py convert`)
| Supplied | In project | Notes |
| --- | --- | --- |
| PDF (1 page) | copied byte-for-byte | preferred; multi-page → ask which page |
| EPS | PDF via `epstopdf` | vector kept |
| SVG | PDF via Inkscape / rsvg-convert / cairosvg / svglib | text labels and aspect ratio verified; no converter → exit 3 → ask for a PDF export or permission to install one (`pip install svglib` is the lightest). The LaTeX `svg` package needs Inkscape + shell-escape (Overleaf: yes; local: usually no) |
| PNG / JPG | copied byte-for-byte | check effective DPI (≥ 300 ideal, < 150 warn) |
| TIFF / GIF / BMP / WebP | PNG via Pillow (lossless) | never JPEG re-encoding |
| CSV / TSV / Markdown table | `tables/tab_*.tex` via `visuals.py table` | cells verbatim; only LaTeX escaping and Unicode→math mapping (± → `$\pm$`, − → `$-$`, ≤, ×, Greek); **bold**/*italic* kept; numbers verified unchanged |
| LaTeX table | copied unchanged | wrap in a float by hand only if needed |
| XLSX | via openpyxl if installed, else ask for CSV | stored values may differ from displayed rounding → verify against the manuscript |
| Table as image | — | ask: retype (with approval, verify every cell) or include as a figure |

Never use Windows `convert.exe` (it is a disk utility, not ImageMagick).
Never screenshot, re-plot, or vectorise-by-tracing a figure.

### 6.4 Captions, labels, cross-references
- Caption text: verbatim from the manuscript (preferred), else the sidecar,
  else a caption inside the supplied `.tex`/`.md`, else the user. If none
  exists, ask; do not write one. If the manuscript caption and the sidecar
  differ, ask.
- Labels: `fig:<short_name>` / `tab:<short_name>`, ASCII, unique.
- In-text "Figure N"/"Table N" → `Figure~\ref{fig:...}` when the printed
  number equals N. If LaTeX's float order would change the manuscript's
  numbering, ask (see SKILL.md Step 3).
- Table captions above the table, figure captions below (template default).

### 6.5 What the checks cannot see
`visuals.py check` cannot judge whether a raster is visually clipped by its own
author, whether colours are distinguishable, or whether a diagram's arrows are
complete — only the renders can. Read `_conversion/render/visual_*` and
`asset_*` side by side for every visual before reporting.
