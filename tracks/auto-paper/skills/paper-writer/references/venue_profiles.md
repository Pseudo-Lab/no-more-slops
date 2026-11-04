# Venue Profiles and Presentation Conventions

Used by paper-writer, paper-results-reviser, paper-visuals and
paper-to-latex. Machine-readable limits live in `venue_profiles.json`
(same folder). `check_page_limit.py` reads that file.

Checked 2026-10-17. Page rules change every year. Before a real
submission, re-check the official call for that year. Record the result in
the paper's `pagelimit.json` (`"venue_verified": "<date + URL>"`).

## 1. Page rules (submission version)

| Profile id | Main-content limit | References | Appendix | Template | Status |
|---|---|---|---|---|---|
| `default-4` (user default) | 4 | not counted | not counted | paper-to-latex `main_twocolumn.tex` (10pt, two-column, 0.75in) | user rule |
| `neurips-workshop-4` | 4 (typical; set per workshop) | not counted | not counted | `neurips_2026.sty` (kit) | confirm each workshop's CFP |
| `neurips` | 9 (+1 camera-ready) | not counted | not counted (checklist also excluded) | `neurips_2026.sty` (kit); editing the style can mean desk rejection | NeurIPS 2026 CFP + kit verified |
| `icml` | 8 (+1 camera-ready) | unlimited | unlimited | `icml2026.sty` (kit) | ICML 2026 verified |
| `iclr` | 9 (10 at rebuttal and camera-ready) | unlimited | unlimited, after bibliography | `iclr2026_conference.sty` (kit) | ICLR 2026 verified |
| `cvpr` | 8 incl. figures/tables | extra pages, references only | supplementary file | CVPR 2026 author kit | 2023–2025 official; 2026 kit |
| `iccv` | 8 | not counted | supplementary | ICCV 2025 author kit | 2025 official |
| `eccv` | 14 (LNCS) | not counted (kit text) | supplementary | `llncs.cls` + `eccv.sty` (2026 kit) | 2026 policy + kit |
| `aaai` | 7 | extra pages, references only (plus reproducibility checklist) | optional technical appendix | `aaai2026.sty` (kit) | AAAI-26 verified |
| `aaai27` | 7 (carried over; verify) | as AAAI-26 | as AAAI-26 | `aaai2027.sty` (kit) | AAAI-27 kit downloaded |
| `aistats` | 8 (9 camera-ready) | unlimited (also checklist) | unlimited | `aistats2026.sty` (kit) | AISTATS 2026 CFP verified |
| `uai` | 8 | unlimited | unlimited, from a new page | `uai2026.cls` (kit) | UAI 2026 instructions verified |
| `ijcai` | 7 | at most 2 extra pages (refs, acknowledgements, statements) | **counts** if inside the paper | `ijcai26.sty` (kit) | IJCAI-ECAI-26 kit text |
| `acl-long` / `acl-short` | 8 / 4 (9 / 5 final) | unlimited | Limitations section required, not counted | `acl.sty` (kit), 11pt | ACLPUB verified (ACL, EMNLP, NAACL via ARR) |
| `colm` | 9 | unlimited | not counted | `colm2026_conference.sty` (kit) | COLM 2026 kit text |
| `tmlr` | no hard limit (12 = soft target) | – | – | `tmlr.sty` (kit) | journal; over-length is advisory |

**Official kits are bundled** (downloaded 2026-10-17 with the user's
approval, unmodified) in
`~/.claude/skills/paper-writer/templates/venues/_downloads/<kit>/kit/`.
`SOURCES.json` there lists each official URL, the page it was linked
from, the sha256 and the style version. Each profile in
`venue_profiles.json` has `kit` (template folder) and `kit_main` (the
official example file). To start a paper: **copy** the kit folder into
the paper's LaTeX folder, replace the example's content, and never edit
the `.sty`/`.cls`. Re-download when a new year's kit is released.

Not bundled: WACV, BMVC, KDD/ACM (`acmart` from CTAN), ICRA/IROS (IEEE
`IEEEtran`), CoRL, ICASSP. Download them on request.

Sources: neurips.cc/Conferences/2025/CallForPapers;
icml.cc/Conferences/2026/CallForPapers and /AuthorInstructions;
iclr.cc/Conferences/2026/AuthorGuide;
cvpr.thecvf.com/Conferences/2025/AuthorGuidelines;
iccv.thecvf.com/Conferences/2025/AuthorGuidelines;
eccv2024.ecva.net/Conferences/2026/SubmissionPolicies;
aaai.org/conference/aaai/aaai-26/submission-instructions/ and
/reproducibility-checklist/; neurips.cc/public/guides/PaperChecklist.

**Template rule.** A paper is checked against the template of its target
venue. Two-column 10pt (CVPR, AAAI, `default-4`) holds about 1.5–1.8 times
as much text per page as a single-column NeurIPS, ICML or ICLR page. A
4-page paper written for one template does not fit the other. Fix the
venue **before** drafting. Use the bundled official kit (above). For a
venue or year that is not bundled, ask the user for the file, or ask
permission to download it from the official author kit. Never imitate a
venue style by hand-editing margins.

## 2. Main-results tables by research family

These patterns were checked in representative papers. Examples: LoRA
(ICLR 2022), Tables 2–3, and PatchCore (CVPR 2022), Table 1. They also
follow the NeurIPS and AAAI checklists. Adapt them; do not copy one
universal format.

### ML venues (NeurIPS, ICML, ICLR, AAAI): methods, LLMs, learning

- Rows are methods under their **established names** with a citation:
  `LoRA~\cite{hu2022lora}`. Variants are distinguished by a superscript
  or an extra column, such as parameter count, backbone or budget.
- Rows are grouped with `\midrule`: (i) published baselines, (ii) baselines
  reproduced by the authors, (iii) the proposed method. Ours goes last,
  often named `Ours` or the method's name, optionally shaded.
- Provenance markers are standard and are always defined in the caption.
  LoRA uses `*` for "numbers published in prior works" and `†` for runs
  set up for a fair comparison. These skills use `*` = published and
  `†` = reproduced by us (see `paper_standards.md` §4).
- The authors' own runs commonly show `mean ± std` over seeds. The number
  of seeds and the meaning of ± (std or s.e.) go in the caption or
  appendix. Published rows usually show no ± because the original paper
  did not report one.
- Bold = best per column, underline = second best. State the rule if it
  is not obvious.
- **p-values and CIs are almost never columns of the main table.** The
  NeurIPS checklist asks for error bars, CIs or tests for the main claims.
  It accepts them in tables or plots, explained in the text. The AAAI
  checklist asks for variation measures and appropriate tests, and allows
  them in a referenced appendix.

### CV venues (CVPR, ICCV, ECCV): detection, segmentation, anomaly detection

- Wide `table*` with datasets, categories or splits as columns. Usually
  there is also a backbone or extra-data column, plus an average column.
- `Method [n]` with bracketed numeric citations. Mark a published number
  that used a different protocol (PatchCore: `PaDiM*` = "result from [14]
  with problem-specific backbone selection").
- Single point values are the norm in main tables. Variation goes in
  ablations, the supplement or plots. Missing values are `–`, with the
  reason in the note.
- Ablations: compact tables with check marks per component, or line plots
  over a hyper-parameter.

### Diagnostic and empirical-analysis papers

- Main table = conditions or arms × metrics. Condition labels are allowed
  **here** because there is no established method to name. Still give
  each arm a short, descriptive, defined name, and cite the method each
  arm is built on.
- Interaction or factorial claims are statistical claims. The test result
  belongs in the text next to the table, or in a small dedicated table
  (`paper_standards.md` §5.3).

## 3. Statistical presentation by venue (summary)

| Venue family | Main table | Text | Appendix |
|---|---|---|---|
| NeurIPS / ICML / ICLR | point estimate, `± std` over seeds for own runs where the field reports it | one sentence on the test and its result for each headline claim | full test table (effect, CI, test, p, n, correction) |
| AAAI | as above; run count stated | as above | reproducibility-checklist answers + test table |
| CVPR / ICCV / ECCV | point estimates | variance or test sentence when the gain is small | seed variance and tests |
| Workshop 4-page | as the parent venue | as the parent venue; mandatory if the gain is within noise | appendix if allowed, otherwise a short sentence |
