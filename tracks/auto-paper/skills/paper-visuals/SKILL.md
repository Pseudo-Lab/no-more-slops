---
name: paper-visuals
description: "Manually invoked. Analyzes ONE completed or draft research paper (.md or .tex), independently selects the smallest set of scientifically justified visuals (tables, statistical plots, workflow/methodology/architecture/pipeline/algorithm diagrams), verifies every value and every arrow against the manuscript and any available project evidence (CSV/JSON results, analysis scripts, configs, logs), generates reproducible publication-quality figures (Matplotlib, Graphviz, Mermaid, hand-written SVG), visually inspects every render, integrates them into a copy of the paper in its native format, and writes a concise visualization audit. Never invents results, steps, or feedback loops; never runs experiments; never overwrites the original paper. Outputs <stem>_visuals.<ext>, <stem>_figures/, <stem>_visuals_audit.md. Usage - /paper-visuals <paper_file> [format:<venue/page limit>] [evidence:<dir>] [free-text instructions]"
argument-hint: "<paper_file> [format:<venue/page limit>] [evidence:<dir>] [instructions]"
---

# Paper Visuals

Add the smallest set of tables and figures that makes ONE paper clearer,
denser, and easier to verify, and prove that every visual says only what the
evidence says.

This is a **communication** skill, not a research skill. It does not run
experiments, change findings, add hypotheses, alter preregistered criteria,
or rewrite the science. It is generic: assume nothing about the project,
field, benchmark, model, metric, number of conditions, or venue beyond what
the inputs state. Scientific accuracy always outranks visual appearance.

The goal is **not** to maximize the number of visuals. A paper that needs
zero new visuals is a valid outcome; say so in the audit.

---

## 1. Inputs and argument handling

Raw arguments: `$ARGUMENTS`

Parse them as:

1. **First token** (required): `paper_file`, path to a `.md`, `.markdown`, or
   `.tex` file, relative to the current working directory or absolute.
2. Optional keyed tokens, in any order:
   - `format:<text>`: venue, column layout, and/or page limit
     (e.g. `format:"4-page two-column, refs excluded"`). Overrides anything
     inferred from the paper.
   - `evidence:<dir>`: an extra directory to search for result artifacts.
     May be repeated.
3. Everything else is free-text user instructions (e.g. "tables only",
   "no architecture figure", "appendix allowed"). User instructions override
   this skill's defaults but never override Section 15 (Restrictions).

### Input validation (stop on failure)

Before any analysis:

1. If `$ARGUMENTS` is empty: print the usage line
   `/paper-visuals <paper_file> [format:<...>] [evidence:<dir>] [instructions]`
   and stop.
2. Resolve `paper_file`. If it does not exist, search the working directory
   with Glob for a file of the same basename; if exactly one match exists,
   use it and say so; otherwise list candidates and stop.
3. Reject unsupported extensions (`.docx`, `.pdf`, etc.) with a message
   suggesting conversion to Markdown or LaTeX first. Stop.
4. Read the file. If it is empty or contains no section headings, stop and
   report.
5. Define:
   - `stem` = filename without extension; `ext` = original extension.
   - `paper_dir` = directory containing the paper.
   - `out_paper` = `<paper_dir>/<stem>_visuals.<ext>`
   - `fig_dir` = `<paper_dir>/<stem>_figures/`
   - `audit` = `<paper_dir>/<stem>_visuals_audit.md`
6. If any of these outputs already exist, do **not** overwrite silently:
   report it and either ask the user or write to a suffixed name
   (`_visuals_v2`, `_figures_v2`, ...). Never overwrite the original paper or
   any pre-existing figure asset unless the user explicitly authorizes it.
7. Respect any project instructions (CLAUDE.md) about where files may be
   written. All outputs go next to the paper, inside the project.

### Tooling check (once, up front)

Run quick, read-only probes and record results for the audit:

- `python --version` (or `python3`), and
  `python -c "import matplotlib, numpy; print(matplotlib.__version__)"`.
  Note whether `pandas` and `scipy` are importable (optional).
- `dot -V` (Graphviz) and `python -c "import graphviz"` (optional).
- `mmdc --version` (Mermaid CLI, optional).
- For `.tex` inputs: `pdflatex --version` / `latexmk --version` (optional,
  only used for an optional compile check).

Do not install packages system-wide without asking. If a tool is missing,
pick a fallback from Section 8 and record the substitution. If Python with
Matplotlib is unavailable, ask the user before proceeding, because
quantitative plots cannot be produced reproducibly without it.

---

## 2. Phase A: Read and analyze the whole manuscript

Read the **entire** paper before deciding anything (use offset/limit reads
for long files; do not skim). Build an internal inventory:

| Item | What to record |
|---|---|
| Research questions / hypotheses | IDs, exact wording, preregistered criteria |
| Contributions | What the paper claims is new |
| Experimental design | Conditions/arms, factors, controls, randomization, seeds |
| Models / algorithms | Components, inputs, outputs, training vs inference |
| Data processing | Sources, filters, splits, subsets, sizes |
| Evaluation | Metrics (definitions), judges/oracles, execution environments |
| Statistics | Tests, effect sizes, CIs/SEs, n, corrections |
| Results | Every reported number, with its location (section/line) |
| Ablations / comparisons | Which baselines are directly comparable and which are not |
| Limitations / negative results | Every null, negative, or failed hypothesis |
| Existing visuals | Every table and figure, caption, numbering, references to it |
| Format | Venue, columns, page limit, appendix policy, refs counting |

Also note **where text alone struggles**: dense paragraphs of numbers,
multi-step procedures described in prose, factorial structure, multiple
interacting components, ordered trends, or comparisons spread across sections.

Do not assume every paper needs a workflow diagram, an architecture figure,
or a plot. Determine need from content.

---

## 3. Phase B: Locate and verify evidence

The manuscript is the primary input but **not** automatically authoritative
for numbers. Search for supporting evidence, starting from `paper_dir` and
walking up to the project root, plus any `evidence:` directories:

- Results: `*.csv`, `*.json`, `*.jsonl`, `*.parquet`, `*.tsv`, `results*.md`
- Analysis: `analysis*.py`, `stats*.py`, `*.ipynb`, statistical outputs
- Implementation: model/pipeline source referenced by the paper
- Configs: `*.yaml`, `*.yml`, `*.toml`, `config*.json`, hashes/IDs cited in the paper
- Logs, existing plots, preregistration / plan documents, benchmark docs

Use Glob/Grep; read only what is relevant. Prefer the artifact the paper
cites (by filename, config hash, run ID). If several versions exist, prefer
the one whose identifiers match the paper; record the choice. Never edit,
move, or "clean" source data. If you need derived data, compute it in a
script under `fig_dir/src/` that reads the originals read-only.

For every number you will visualize, record a provenance row:

`value | paper location | source file:field/row | match? | note`

Classify each visual's evidence as one of:

- **VERIFIED**: every value matches a project artifact (within stated rounding).
- **MANUSCRIPT-ONLY**: no artifact found; values taken from the paper text.
  Must be disclosed in the audit (and in the caption note if the user wants).
- **DISCREPANT**: paper and artifact disagree. Do **not** silently pick one.
  Report both in the audit. Default: plot the artifact value only if the
  artifact is clearly the source of the paper's claim and the paper is a
  transcription error; otherwise do not create that visual until resolved,
  and flag it to the user. Never change the paper's findings to match.

For diagrams, verify methodological fidelity: trace each step and each
arrow to a sentence in the paper or a code path in the implementation. If
the paper is ambiguous and the code resolves it, follow the code and note it;
if neither resolves it, report the ambiguity rather than guessing.

---

## 4. Phase C: Select visuals

### 4.1 Review existing visuals first

For each existing table/figure decide: **Preserve / Correct / Improve /
Merge / Replace / Remove**, with a one-line reason. Do not recreate an
accurate existing visual without a meaningful improvement. Never delete an
original image asset; a replaced figure simply stops being referenced in
`out_paper`, and the original file stays on disk.

### 4.2 Generate candidates

List candidate visuals from the inventory. Typical candidates (only where
the content exists):

- Main results / baseline comparison table
- Hypothesis-test or preregistered-criteria table
- Effect-size CI / forest plot
- Interaction plot for factorial designs
- Grouped bar chart across conditions
- Ablation table or plot
- Dataset / subset statistics table
- Evaluation-validity / judge-agreement table
- Experimental workflow or evaluation pipeline diagram
- Model / system architecture diagram
- Algorithm illustration
- Calibration, ROC/PR, distribution (box/violin/histogram) plots
- Compute/efficiency table

### 4.3 Score each candidate

Score 0 to 2 on each criterion and write a one-line justification:

| Code | Criterion | Question |
|---|---|---|
| A | Scientific importance | Communicates a central contribution, method, or result? |
| B | Information gain | Conveys something hard to get from the text? |
| C | Non-redundancy | Avoids repeating another table/figure? (2 = no overlap) |
| D | Accuracy | Every element supportable by paper or evidence? |
| E | Space efficiency | Worth its space in the manuscript? |
| F | Publication suitability | Readable in the target format? |

Hard gates: **D = 0 rejects** the candidate (cannot be supported).
**C = 0 rejects** unless it replaces the redundant visual.

Select the **smallest set** that communicates the paper effectively. Rank by
total score, then by centrality to the main claim. Stop adding visuals when
the next one adds little information or breaks the page budget. Record all
rejected candidates with the reason for the audit.

### 4.4 Page budget

Use `format:` if given; otherwise infer from the paper (stated venue, page
limit, column layout). If unknown, assume a compact short paper and say so.

For short or two-column papers:

- Prefer compact, information-dense visuals; single-column width (about
  3.3 in / 8.5 cm) when readable; double-column (about 7 in / 17.8 cm) only
  when necessary.
- Avoid oversized workflow diagrams; a compact horizontal pipeline beats a
  tall flowchart.
- Prioritize central contributions; move secondary visuals to an appendix
  when the paper has or allows one.
- Never delete important evidence to make room. Never shrink fonts, margins,
  or spacing to force compliance.
- For Markdown, pagination cannot be verified; for LaTeX, it can only be
  verified by compiling. If you cannot verify page count, say so in the audit.

If the selection is not obvious (e.g. two equally strong figures competing
for one slot, or a page limit that forces cutting evidence), briefly present
the trade-off to the user and ask before generating.

---

## 5. Phase D: Tables

Create a table when exact numerical comparison matters.

Requirements:

- Every value verified (Section 3) or marked manuscript-only.
- Report n / denominators where a reader needs them (e.g. `42/120 (35.0%)`
  or an `n` column).
- Include uncertainty (CI, SE, SD) **only** if it was actually computed;
  state which kind and the level (e.g. "95% bootstrap CI").
- Preserve negative and null results in the same table as positive ones.
- Separate directly comparable from non-comparable baselines (a rule, a
  sub-header, or a dagger with a note). Do not rank non-comparable rows.
- Consistent units and precision within a column; state units in headers.
- Bold only by a stated rule (e.g. "best comparable value per column"), or
  not at all. No significance stars unless the note defines them.
- Keep columns few; split or transpose rather than cram.
- Concise caption above the table (LaTeX convention) stating what, on what
  data, with what metric; notes below for abbreviations, uncertainty type,
  and comparability.
- Never invent missing values. Use `n/a` or a plain hyphen `-` with a
  note explaining why.

Format:

- **Markdown**: GitHub-flavored pipe table, right-aligned numeric columns
  (`---:`), caption as a bold line above (`**Table N.** ...`), notes as an
  italic or plain line below.
- **LaTeX**: `table` (or `table*`) environment with `booktabs`
  (`\toprule`, `\midrule`, `\bottomrule`), no vertical rules, `\caption`
  above and `\label{tab:...}`. Use `\small` only if that matches existing
  tables in the paper. If `booktabs` is not loaded, add
  `\usepackage{booktabs}` to the preamble and note it in the audit.

Write tables directly in the manuscript. Optionally keep a generator script
in `fig_dir/src/` if the table is computed from data files.

---

## 6. Phase E: Statistical plots

Choose the plot from the scientific question, not habit:

| Question | Plot |
|---|---|
| Effect sizes with uncertainty | CI / forest plot (point + interval, zero/null reference line) |
| Factorial design, interaction | Interaction plot (factor A on x, lines per level of B) |
| Few conditions, one metric | Dot plot with CIs, or bars starting at zero |
| Conditions x subgroups | Grouped bar chart (bars start at zero) |
| Ordered trend (size, step, budget) | Line plot with markers |
| Relationship between two continuous variables | Scatter (with fit only if the paper fits one) |
| Distributions | Histogram, box, or violin (show n) |
| Structured multi-dimensional comparison | Annotated heatmap |
| Classifier quality | ROC / PR curve, calibration plot |
| Ablations | Ablation bar/dot plot relative to full model |

Integrity rules:

- Bars encode magnitude and **must** start at zero. If differences are tiny
  relative to the scale, use a dot/CI plot instead of truncating bars.
- Axes for dot/line plots may be zoomed, but label ticks clearly and never
  imply a zero baseline that is not there.
- Error bars must represent exactly what the caption says (95% CI, SE, SD,
  min/max over seeds). If no uncertainty was computed, show none and do not
  imply any.
- Do not aggregate across subsets the paper keeps separate, or average
  metrics with different denominators.
- No significance stars unless the caption defines them and the tests
  exist in the paper.
- Show n per condition (in the legend, tick labels, or caption) when it
  differs across conditions.
- Use log scales only when the data span orders of magnitude, and label them.
- No dual y-axes unless unavoidable; prefer two panels.

### Matplotlib implementation

Write one script per figure (or one shared script with one function per
figure) in `fig_dir/src/`. Each script:

- Hard-codes the plotted data **in a clearly labeled block** with a
  provenance comment per value (source file and field, or paper section),
  OR reads the source files read-only and asserts the expected values.
- Contains an assertion block that checks plotted values against the
  provenance table (e.g. `assert abs(x - 0.352) < 5e-4`).
- Sets a shared style:
  ```python
  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt
  plt.rcParams.update({
      "font.family": "serif",          # match paper; "sans-serif" if paper uses it
      "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
      "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
      "axes.spines.top": False, "axes.spines.right": False,
      "axes.linewidth": 0.6, "lines.linewidth": 1.2,
      "pdf.fonttype": 42, "ps.fonttype": 42,   # embed TrueType, editable text
      "svg.fonttype": "none",                  # keep text as text in SVG
      "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
  })
  ```
- Sizes the figure to the final printed width (single column about
  3.3 x 2.2 in; double column about 7 x 2.5 in) so fonts render at true
  size (7 to 9 pt). Never rely on downscaling a large figure.
- Saves `fig_dir/figN_<slug>.pdf`, `.svg`, and `.png` (dpi=300).
- Uses no titles inside the figure when the caption carries the title.

Run the scripts with `python <script>`; keep them reproducible (no
randomness, or a fixed seed if jitter is used).

---

## 7. Phase F: Workflow, methodology, architecture, and algorithm diagrams

Create a diagram only when the procedure, system, or structure is complex
enough that prose is genuinely hard to follow.

### 7.1 Build a step table first

Before drawing, write (internally and in the audit) a step/edge table:

`node | type | evidence (paper section or code path)`
`edge | from -> to | meaning | evidence`

Node types to distinguish visually (shape and/or line style, not color
alone):

- Data / artifacts (inputs, datasets, generated test inputs, outputs)
- Processes / model calls (inference, training, transformation)
- Executable environments (sandboxes, interpreters, simulators)
- Evaluation / metrics / statistical analysis
- Shared components vs condition-specific components (e.g. dashed border
  or grouped cluster per condition)

Edge semantics: every arrow must have one clear meaning (data flow,
control flow, or dependency). Use one style per meaning and state it in the
caption or legend. Draw:

- Training separate from inference.
- Data preparation separate from evaluation.
- Model outputs (text) distinct from executed programs and their results.
- Independent branches (parallel conditions) as parallel lanes, not a chain.
- Feedback loops **only** if the method actually feeds outputs back. Never
  draw evaluation results flowing back into a generator, policy, or prompt
  unless the paper/code does that.

Do not invent steps, components, data access, or capabilities. Do not
convert an experimental workflow into a conceptual illustration that
implies more than was done. If the diagram is conceptual rather than
implemented, label it as such in the caption.

### 7.2 Tool choice

- **Graphviz (`dot`)**: default for pipelines, workflows, and architectures
  with real graph structure. Keep the `.dot` source in `fig_dir/src/`.
  Use `rankdir=LR` for compact single-column pipelines; `fontname` matching
  the paper's family; `fontsize=8` to `9`; `penwidth=0.8`; `nodesep`/`ranksep`
  tuned for compactness; `cluster` subgraphs for conditions/stages.
  Export: `dot -Tpdf`, `dot -Tsvg`, `dot -Tpng -Gdpi=300`.
- **Mermaid**: acceptable when the target is Markdown rendered on a
  platform that supports Mermaid, or when `mmdc` is installed for export.
  Still export PDF/SVG/PNG if `mmdc` exists; otherwise embed the Mermaid
  block **and** produce a Graphviz or SVG fallback for print.
- **Hand-written SVG**: for precise layouts (e.g. model architecture with
  aligned tensors/blocks) where Graphviz layout fights the structure. Keep
  the SVG as the editable source; convert to PDF/PNG with an available
  converter (`cairosvg`, `rsvg-convert`, `inkscape`) or redraw in Matplotlib.
- **Matplotlib patches**: fallback for diagrams when Graphviz is
  unavailable, and for algorithm illustrations that mix geometry and data.
- **TikZ**: only for `.tex` papers that already use TikZ, and only if a
  LaTeX engine is available to compile and inspect it.

Never use generative image models for quantitative charts or scientifically
precise diagrams. Every figure must come from explicit data or a structured
definition kept in `fig_dir/src/`.

---

## 8. Visual design standards

Apply to every figure:

- Clean, minimal layout; consistent typography across all figures (same
  family and sizes); consistent line weights.
- Colorblind-safe palette. Default (Okabe-Ito):
  `#0072B2` blue, `#E69F00` orange, `#009E73` green, `#D55E00` vermillion,
  `#CC79A7` purple, `#56B4E9` sky, `#F0E442` yellow (avoid yellow for thin
  lines/text), `#000000` black. For sequential heatmaps use `viridis` or
  `cividis`; for diverging use a perceptually uniform diverging map centered
  on the meaningful zero.
- Grayscale-compatible: pair color with marker shape, hatch, or line style
  so conditions remain distinguishable in black-and-white print.
- Use the same color for the same condition in every figure.
- Readable labels (no text below 6.5 pt at printed size); horizontal tick
  labels when possible; units in axis labels.
- Clear hierarchy; whitespace over boxes; light or no gridlines.
- Avoid decorative gradients, shadows, 3D, clip art, icons, excess colors,
  emphasis that exaggerates differences, and dense unreadable labels.
- Mathematical notation consistent with the paper (use mathtext `$...$` in
  Matplotlib; check that symbols render, not as boxes).

Missing-tool fallbacks (record any used): no Graphviz -> Matplotlib patches
or hand SVG; no SVG converter -> export PDF/SVG/PNG from Matplotlib; no
Mermaid CLI -> Graphviz.

---

## 9. Phase G: Render and inspect every figure

Do not trust successful file generation. For **every** figure:

1. Open the PNG with the Read tool and look at it.
2. Check: clipped text, overlapping labels or arrows, misaligned nodes,
   unreadable or overlapping legend, labels too small at printed size,
   inconsistent spacing, poor contrast, broken glyphs/symbols, wrong math
   notation, stray whitespace, wrong aspect ratio for the target column.
3. Check the PDF exists and is non-trivial in size; for Matplotlib PDFs,
   `pdf.fonttype=42` ensures embedded fonts. If a PDF inspection tool is
   available (`pdffonts`), confirm fonts are embedded.
4. Revise the source and re-render until clean. Record the number of
   revision rounds per figure in the audit.

---

## 10. Phase H: Scientific accuracy check per visual

After the final render, verify and record pass/fail for each item:

- All plotted/tabulated values match their sources (independently re-read
  the source; do not just rerun the script's own assertions).
- Axes, units, legends, and labels correct.
- Error bars represent the stated uncertainty, with the stated n.
- Denominators and subsets match the paper's.
- Diagram: walk the step table node by node and edge by edge against the
  methodology; every arrow corresponds to a real flow; no nonexistent
  feedback loops; no implied capabilities or data access.
- Architecture matches the implementation (or is labeled conceptual).
- No causal interpretation the design does not support.
- Caption describes exactly what is shown.
- The manuscript's interpretation of the visual remains correct.

---

## 11. Phase I: Integrate into the manuscript

Copy the original paper to `out_paper` and edit only the copy.

For every visual:

1. Assign consistent numbering in order of first reference. Renumber
   existing figures/tables and all their in-text references if insertion
   changes order. Search the whole document for every `Figure N`/`Table N`/
   `\ref{}` to update them.
2. Write a concise, informative caption: what is shown, on what data/subset,
   metric and uncertainty definition, and n where relevant. End with the
   takeaway only if it is a direct, verified reading of the visual.
3. Insert it near its first substantive discussion.
4. Reference it naturally in the text ("Table 2 reports...", "as Figure 1
   shows...").
5. State the scientific takeaway in the surrounding text, consistent with
   the paper's existing findings.
6. Remove only redundant repetition the visual now carries (e.g. a sentence
   listing every number now in the table). Keep all essential methodological
   explanation and all interpretive claims; a diagram never replaces a
   necessary methods sentence.

Format rules:

- **Markdown**: relative image links,
  `![Figure N: short alt text](<stem>_figures/figN_<slug>.png)`, followed by
  a caption line `**Figure N.** ...`. Use PNG for broad renderer support;
  PDF/SVG remain in `fig_dir` for typesetting. Use relative paths from
  `out_paper`'s directory.
- **LaTeX**: `figure`/`figure*` environment, `\centering`,
  `\includegraphics[width=\columnwidth]{<stem>_figures/figN_<slug>.pdf}`,
  `\caption{...}`, `\label{fig:...}`. Add `\usepackage{graphicx}` only if
  missing (note in audit). Use `[t]` placement unless the paper's convention
  differs.

Do not convert Markdown to LaTeX (or vice versa) unless the user asks.
Do not change findings, numbers, hypotheses, criteria, citations, or the
conclusion to fit a visual. Do not introduce em dashes (the character U+2014)
into manuscript text you write; use commas, colons, parentheses, or
semicolons. Do not remove em dashes already present in unchanged original
text unless the user asks.

---

## 12. Phase J: Final independent review of the whole manuscript

Re-read `out_paper` start to finish as a fresh reviewer and check:

1. Figures, tables, and text agree (numbers, names, condition labels).
2. Scientific claims unchanged and still accurate.
3. Numbering is sequential; every visual is referenced; every reference
   resolves; no dangling `\ref` or "Figure N" pointing to nothing.
4. No redundant visuals (two visuals carrying the same information).
5. Terminology consistent between captions, labels, and text.
6. Negative and null findings preserved and not visually de-emphasized.
7. Statistical interpretations accurate (no CI read as a test unless
   defined, no unsupported significance language).
8. Methodological flow remains clear without relying on a diagram alone.
9. No invented experimental steps or feedback loops.
10. Publication constraints respected; for `.tex`, compile once with the
    available engine (in a temp copy or `fig_dir/src/build/`, then delete
    build intermediates) if possible and report page count; otherwise state
    pagination is unverified.
11. `grep` the new/edited text for U+2014 em dashes; fix any introduced.

Fix issues found, then repeat the affected checks.

---

## 13. Deliverables and naming

All paths relative to `paper_dir`:

```
<stem>_visuals.<ext>          # updated manuscript (original untouched)
<stem>_figures/
    fig1_<slug>.pdf           # vector, for typesetting
    fig1_<slug>.svg           # editable vector
    fig1_<slug>.png           # 300 dpi preview / Markdown embedding
    ...
    src/
        fig1_<slug>.py | .dot | .mmd | .svg   # editable, reproducible sources
        (optional) tables_<slug>.py           # if a table is computed from data
        README.md             # one line per figure: source file -> outputs, how to regenerate
<stem>_visuals_audit.md       # concise audit
```

Slugs are short, lowercase, hyphen- or underscore-separated, and describe
content (`fig2_effect-ci`, `fig1_eval-pipeline`). Do not leave intermediate
files (temp data dumps, scratch renders, LaTeX build files) in the outputs;
put scratch work in the session scratchpad if one exists.

### Audit file template (`<stem>_visuals_audit.md`)

Keep it concise (aim for 1 to 2 screens).

```markdown
# Visualization audit: <paper filename>

Date: <YYYY-MM-DD> | Input: <path> | Output: <path> | Format assumed: <...>
Tooling: Python <v>, Matplotlib <v>, Graphviz <v or "absent">, ...

## Existing visuals
| Item | Decision | Reason |

## Selected visuals
| # | Type | Purpose | Scores A-F | Evidence status | Placement |

## Considered but rejected
| Candidate | Reason |

## Data sources and provenance
| Visual | Source file(s) | Fields / rows | Notes |

## Discrepancies
(paper vs artifact, with both values and how handled; or "None found")

## Unresolved uncertainties
(ambiguous methodology, manuscript-only values, unverified pagination)

## Quality control
| Visual | Values verified | Axes/legend | Uncertainty | Diagram fidelity | Visual inspection (rounds) | Caption |
Final manuscript review: <pass/fail per Section 12 item, short>
```

---

## 14. Final quality-control checklist

Do not report completion until every item is true or explicitly explained:

- [ ] Whole paper read before selection.
- [ ] Evidence search done; every visualized value has provenance or is
      marked manuscript-only.
- [ ] Discrepancies reported, not silently resolved.
- [ ] Each selected visual passed gates D and C and justified by A-F scores.
- [ ] Rejected candidates recorded.
- [ ] Existing visuals reviewed (preserve/correct/improve/merge/replace/remove);
      original assets untouched.
- [ ] Bars start at zero; no truncated or exaggerating axes.
- [ ] Uncertainty shown only if computed, and defined in caption.
- [ ] No undefined significance stars.
- [ ] Every diagram node and edge traced to paper or code; no invented
      steps or feedback loops; conceptual diagrams labeled.
- [ ] Colorblind-safe and grayscale-distinguishable.
- [ ] Every figure rendered and visually inspected (PNG read); no clipping,
      overlap, tiny text, or broken glyphs.
- [ ] PDF, SVG, PNG and editable source exist for every figure.
- [ ] Integrated in native format; numbering and references consistent.
- [ ] Findings, hypotheses, criteria, citations unchanged; negative results
      preserved.
- [ ] No em dashes introduced into manuscript text.
- [ ] Page-budget compliance verified or limitation stated.
- [ ] Original manuscript unchanged; outputs named per Section 13.
- [ ] Audit written.

Final chat report (short): output paths, list of visuals added/changed with
one-line purpose each, evidence status counts (verified / manuscript-only /
discrepant), any open issues requiring the user's decision.

---

## 15. Restrictions (never violate)

- Do not invent, estimate, interpolate, or "fill in" experimental results.
- Do not modify, move, or delete original data or result files.
- Do not run new scientific experiments or re-run analyses to obtain new
  numbers (re-reading existing outputs and recomputing simple displayed
  derivations such as a percentage from a reported count is allowed and
  must be noted).
- Do not introduce new hypotheses or alter preregistered criteria.
- Do not fabricate or add citations.
- Do not hide, shrink, or omit negative or null findings.
- Do not make or imply unsupported SOTA claims (e.g. by bolding a
  non-comparable baseline comparison).
- Do not invent workflow steps, components, or data access.
- Do not imply feedback where none exists.
- Do not use decorative illustrations as scientific evidence.
- Do not use generative image models for figures.
- Do not introduce em dashes into manuscript text.
- Do not convert Markdown to LaTeX (or the reverse) unless requested.
- Do not overwrite the original manuscript or existing figure assets
  without explicit authorization.
- Do not manipulate fonts, margins, or spacing to fake page compliance.

Scientific accuracy takes priority over visual appearance.
