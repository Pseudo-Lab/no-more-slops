# Paper Standards: claims, sections, tables, statistics, page limit

Shared by paper-writer, paper-results-reviser, paper-visuals, paper-to-latex
(page-limit part) and experiment-runner (§5 output requirements). Read it
fully before writing or revising a paper.

Sources (2026-10-17):
- **[K]** S. Keshav, "How to Read a Paper", *ACM SIGCOMM CCR* 37(3), 2007.
  It is about reading papers. Its writing advice follows from how
  reviewers read.
- **[M]** The user's mentor's feedback on a submitted paper (tables,
  statistics presentation, page limit, causal justification).
- **[V]** Official venue guidelines and representative papers
  (`venue_profiles.md`).

This file sets presentation and claim rules. It never weakens a research
gate in `~/.claude/skills/research-pipeline/references/research_design_principles.md`.
Statistical **rigor** is still mandatory (§5). Only its **placement**
adapts to the venue.

---

## 1. The one-pass reader test [K]

Most reviewers make only one pass over a paper. They read the title,
abstract and introduction, the section headings and the conclusion, and
glance at the references [K §2.1]. If the gist is not clear after that
pass, the paper is likely to be rejected [K].

**Procedure (mandatory, after drafting and after every revision).**
Using ONLY the title, abstract, introduction, section and subsection
headings, and the conclusion, write a "five Cs card" in the run notes
(not in the paper):

| C | Must be answerable from the first-pass material |
|---|---|
| Category | What kind of paper is this: a new method, a measurement/diagnostic study, an analysis of an existing system, a reproduction? |
| Context | Which closest prior work and baseline does it build on, by name? |
| Correctness | Which assumptions does the method rest on, and are they stated? |
| Contributions | Two to four concrete contributions, each with its evidence type (§2) |
| Clarity | Do the headings alone tell the story? Is each heading informative ("Per-item fault exposure"), not generic ("Analysis 2")? |

If any C cannot be answered, revise the abstract, introduction or headings
until it can. Record the card in the reply or audit.

## 2. Claim–evidence ladder (mandatory)

Every claim in the abstract, introduction, results, discussion and
conclusion gets an evidence level. The wording may not exceed it.

| Level | Evidence actually produced | Allowed wording | Forbidden wording |
|---|---|---|---|
| L0 Hypothesis | none yet, or pre-experiment | "we hypothesize", "is designed to" | any outcome verb |
| L1 Difference observed | one comparison, same protocol | "achieves X vs Y", "outperforms B on <metric, split>" | "significantly", "consistently", "because" |
| L2 Reliable difference | L1 + the pre-registered test or variability criterion is met | "significantly / consistently outperforms (test, n)" | "due to", "the mechanism" |
| L3 Attributed to a component | L2 + an ablation or control that removes only that component | "the gain comes from component C (Table k)" | "proves the mechanism" |
| L4 Mechanism supported | L3 + a diagnostic that separates the proposed mechanism from the simplest alternative explanation (MDV Q8–Q9, shared definitions §9) | "evidence that M operates via ..." | "proves", "establishes in general" |

Rules:
- A performance difference never "proves", "demonstrates" or "confirms" a
  mechanism. Without L4, write "consistent with" or "suggests".
- A result on one benchmark or slice never supports a claim about a whole
  problem class. The scope must match the MDV Q10 answer.
- **SOTA claims** use the four claim levels in shared definitions §4f:
  overall SOTA / best reproducible baseline / selected baseline /
  restricted protocol. Never write "state of the art" for anything but
  the first, and only when its conditions hold.
- **Novelty claims** use the novelty type (prior-work resource §5a): a new
  application, modification, new mechanism, or implementation correction.
  Never call an application or correction "a novel method".
- Never write "first", "novel" or "unexplored" as a claim (existing
  prior-work rule).

## 3. Section-by-section quality checks

Each item is a pass/fail check for paper-writer Step 8 and
paper-results-reviser Step 10.

**Title.** Names the object and the finding or method. No claim above
the evidence level (no "solves", "proves").

**Abstract** (one paragraph, about 150–200 words for 4 pages):
1. context and problem (one sentence);
2. the specific gap or limitation of the strongest existing method;
3. what we do, naming the method or intervention;
4. the main result as a number, with the benchmark, the metric and the
   comparator, at its true claim level (§2, §4f);
5. the implication or scope.
- No p-values or CIs unless the central claim is itself a statistical
  claim (e.g. "no interaction"). No undefined acronyms.
- Every number appears identically in the results.

**Introduction.**
- Motivation → precise problem → why the strongest existing method fails
  on it, with evidence (MDV Q1–Q2) → the idea and **why it should work**
  (MDV Q3, evidence level stated) → what we test → contributions.
- Contributions are a short list. Each one is backed by a named table,
  figure or section, and stays within its evidence level.
- No claim that a later section does not support.

**Related Work.**
- Organized by **mechanism or approach**, not as a paper-by-paper list.
  For each group: what it does, the closest paper, and the exact
  difference from this work.
- Includes the closest prior methods, the strongest comparable baselines,
  recent work (last 12–18 months), and mechanisms that resemble ours
  (prior-work resource §4a literature map).
- States the novelty type honestly. Partial overlap is described as
  partial overlap.
- Only verified references from the archive or Evidence Report.

**Method.**
- Notation is defined before use. Equations appear only where they add
  precision. The difference from the baseline is explicit (one sentence or
  a diff box).
- The assumptions the mechanism needs (MDV Q4) are stated.
- Enough detail to re-implement [K §2.3: a reader should be able to
  "virtually re-implement" the paper].

**Experimental setup.**
- Benchmark, split, metric(s) exactly as in the original protocol.
  Baseline sources: published, or reproduced with official code at commit
  X. Seeds, compute, hyperparameter selection (on validation, never test).
- The protocol-compatibility check (§4.2) is summarized in one sentence:
  "all rows use the official test split and scorer; rows marked ‡ differ
  in ...".
- The statistical procedure is named here, briefly (§5.4).

**Main results.**
- Follows §4 (table conventions). The prose interprets the table rather
  than repeating it. Give the headline comparison with its claim level.
- Negative and null results are reported in the same table.

**Ablations and analysis.**
- Each ablation removes or replaces one component. A Δ column against the
  full method is standard.
- Includes the experiment that separates the mechanism from the simplest
  alternative explanation (MDV Q9), when the paper claims the mechanism.
- Says which alternative explanations each control rules out.

**Limitations.**
- Specific to this study: problem classes where the assumptions fail
  (MDV Q5–Q6, Q10), protocol restrictions, reproduction gaps, statistical
  power. No generic filler.
- Never dropped to meet the page limit (§6).

**Conclusion.** What was tested, the answer at its claim level, and what
remains open. No new claims.

**Figures.** Axes labelled with units. Error bars are defined (what they
show, over what, and n). The figure is legible at print size [K §2.2:
check axes, error bars, statistical significance]. Bars start at zero.

**Citations.** Every baseline row and every borrowed component is cited.
Every citation is verified against its source (title, authors, venue,
year). Never fabricated. Published numbers are cited to the table they
come from.

## 4. Table conventions [M][V]

### 4.1 Method naming and provenance (mandatory)

1. Existing methods appear under their **established names**, with a
   citation: `PatchCore~\cite{roth2022patchcore}`. Never relabel a
   baseline with an experiment label ("Arm B", "Config-G", "Control").
2. Your own configurations appear in the main table only as the proposed
   method (one row, or a few named variants). Experimental arms, factor
   levels and descriptive configurations go in ablation or analysis
   tables, or are defined once in the text.
3. Every number has exactly one provenance class:

   | Class | Marker (default) | Meaning |
   |---|---|---|
   | PUBLISHED | `*` on the cell or row | copied from the cited paper (table and location in the source log) |
   | REPRODUCED | `†` | we ran the original method (official code or a faithful reimplementation) under our protocol |
   | OURS | none, or a shaded row | the proposed method, run by us |
   | INCOMPATIBLE | `‡` + separate block | different protocol: shown for context only, never bolded or ranked |

   The caption or a table note defines every marker used. If a row mixes
   published and reproduced cells, mark the individual cells.
4. Never present a PUBLISHED number as REPRODUCED, or the reverse. If you
   reproduced a method that also has a published number, show either the
   reproduced number (and note the gap to the published one in the text
   or appendix), or both rows (`Method*` and `Method†`).
5. Never fabricate a missing result. Use `–` and explain why in the note
   ("not reported for this split").
6. Never fabricate or guess a citation.

### 4.2 Protocol-compatibility check (before any published number enters a comparison)

For each PUBLISHED number, record in the source log (not in the paper):
dataset version, split, metric definition and scorer, input resolution or
context length, backbone/model size, training data, extra data, inference
budget, number of seeds. Same on all of them → comparable. Different on
any of them → INCOMPATIBLE (`‡` block, no ranking), or reproduce the
method under your protocol (REPRODUCED). A published number from an
incompatible protocol is **never** used for a direct comparison or a SOTA
claim.

### 4.3 Venue adaptation

Choose the layout from `venue_profiles.md` §2: ML method layout, CV
multi-dataset layout, or diagnostic-arms layout. Templates:
`~/.claude/skills/paper-writer/templates/tables/`:

| File | Use |
|---|---|
| `table_macros.tex` | `\pub`, `\repro`, `\incompat`, `\best`, `\second`, `\ours` macros (add to the preamble) |
| `main_results_ml.tex` | NeurIPS/ICML/ICLR/AAAI main comparison (published / reproduced / ours blocks, mean ± std over seeds) |
| `main_results_cv.tex` | CVPR/ICCV/ECCV multi-dataset `table*` |
| `ablation.tex` | component ablation with check marks and Δ |
| `diagnostic_arms.tex` | factorial or arm-based study (condition labels allowed) |
| `stats_appendix.tex` | full statistical table for the appendix or supplement |
| `tables_demo.tex` | compilable demo of all of the above |

Common rules: `booktabs` (`\toprule/\midrule/\bottomrule`), no vertical
rules; caption above; metric direction in the header (↑/↓); units and
precision consistent within a column; bold/underline by a stated rule
within the comparable block only.

### 4.4 Executable check

`python ~/.claude/skills/paper-writer/scripts/check_tables.py <paper.tex|paper.md|dir>`
flags: undefined provenance markers, baseline rows without a citation,
configuration labels in a main-results table, p-values or CIs in a
main-results table without `% stats-ok: <reason>`, and bolding inside an
incompatible block. ERRORs must be fixed. WARNs are fixed or justified in
the reply.

## 5. Statistics: rigor vs presentation [M][K][V]

### 5.1 Rigor is not optional

The pre-registered statistical analysis (shared definitions §7 gate 6) is
always run and always saved (experiment-runner). This holds even when the
paper shows no p-values. **Never** remove an analysis to make the paper
look conventional. Never report a significance result whose test was not
run.

### 5.2 Choose the test from the design

| Design | Default analysis |
|---|---|
| Two methods, same test items, binary per-item outcome | McNemar exact test, or paired bootstrap over items for Δaccuracy (CI) |
| Two methods, same items, continuous per-item score | paired bootstrap CI for the mean difference; Wilcoxon signed-rank |
| k ≥ 3 seeds per method, one test set | mean ± std over seeds; Welch t / paired-by-seed test if n ≥ 5, else report the spread and do not claim significance |
| Several datasets or tasks, two methods | Wilcoxon signed-rank across datasets |
| Several methods × several datasets | Friedman test + Nemenyi / Holm post-hoc (Demšar 2006) |
| Factorial (A × B) | regression or ANOVA with an interaction term (logistic or mixed-effects for per-item binary outcomes) |
| Many comparisons | Holm (FWER) or Benjamini–Hochberg (FDR), declared in advance |
| Costly single run (no repetition possible) | item-level bootstrap over the test set; state that seed variance is unmeasured |

Always report an effect size (absolute difference in the metric's units,
in pp for percentages). A non-significant result is never evidence of no
effect; use the SESOI or an equivalence test for "no meaningful
difference".

### 5.3 Where statistics go (presentation)

Defaults (the venue profile can tighten them):
- **Main results table:** point estimates. Add `± std` (or s.e., labelled)
  over seeds for your own runs where the venue family reports it (ML
  venues: common; CV: usually not). **No p-value or CI columns.**
- **Text, next to the table:** one sentence per headline claim, e.g.
  "Ours improves on PatchCore† by 1.2 pp (paired bootstrap 95% CI [0.6,
  1.8]; Appendix B)."
- **Appendix or supplement:** the full table (effect, CI, test, statistic,
  p raw / adjusted, n, correction). Use `stats_appendix.tex`.

Statistics move **into** the main table or figure when one of these holds
(record the reason as `% stats-ok: <reason>` in the table source):
1. the gain is within about 2× the seed std or near the SESOI (reviewers
   could attribute it to chance);
2. the main claim is itself statistical (an interaction, equivalence, a
   null result);
3. the venue or subfield's main tables routinely show it (e.g. RL or
   small-data benchmarks with CIs over seeds);
4. the paper reports a single costly run per method. Then the item-level
   CI is the only uncertainty available.

Error bars in **figures** stay expected [K §2.2]. Define them in the
caption.

**Conflict note.** [K] asks whether results come with error bars "so that
conclusions are statistically significant". [M] says p-values and CIs
are not routine in main tables. Resolution: uncertainty is always
computed and shown somewhere a reviewer will look. In figures, as error
bars. In tables, as ± over seeds where conventional. In the text, as a
one-line test result. Full statistics go to the appendix. The rigor
requirement wins; the placement follows the venue.

### 5.4 Setup sentence (always)

The experimental setup names the number of seeds or runs, what ±
denotes, the test used, and the correction method, in one or two
sentences. This answers the NeurIPS and AAAI checklist questions.

## 6. Page-limit protocol (programmatic) [M]

Prompts alone did not keep papers within four pages. The limit is enforced
on the compiled PDF:

1. **Venue and template first.** Resolve the venue profile
   (`venue_profiles.json`; default `default-4`). Write `pagelimit.json` in
   the LaTeX project folder:
   ```json
   {"venue": "default-4", "limit": 4, "main": "main.tex",
    "references_count": false, "appendix_counts": false,
    "max_iterations": 6,
    "required_sections": ["Introduction", "Method", "Experiment|Results",
                          "Limitation", "Conclusion"],
    "required_labels": ["tab:main"]}
   ```
   Put `\label{pl:bodyend}` right after the last line of the Conclusion,
   or keep paper-to-latex's `\clearpage` + `\label{pl:refsstart}` marker.
   The marker is **required**. Without one, the checker can only estimate
   from a "References" heading. That estimate can undercount, so it never
   PASSes. A marker after a page break, or after `\end{document}`, is
   rejected.
2. **Compile and count.**
   `python ~/.claude/skills/paper-to-latex/scripts/check_page_limit.py <latex_dir>`
   compiles with latexmk, counts the **actual PDF pages** up to the body
   marker, and checks forbidden formatting, the template, required
   sections and labels. It writes `_pagecheck/report.json` and appends to
   `_pagecheck/history.jsonl`.
   Exit codes: 0 PASS · 1 OVER LIMIT · 2 COMPILE FAILURE · 3 FORMAT OR
   TEMPLATE VIOLATION · 4 CONFIG ERROR · 5 MAX ITERATIONS (failure
   condition) · 6 ESSENTIAL CONTENT MISSING.
3. **Revise if over.** The report gives the overflow in lines and words.
   Cut in this order, recompiling after each round:
   1. repetition across the abstract, introduction and conclusion;
   2. background and generic motivation;
   3. related work → closest work + difference per mechanism group;
   4. prose that restates table contents;
   5. secondary analyses → one sentence + appendix (if the venue has an
      uncounted appendix);
   6. implementation details not needed to interpret results → appendix;
   7. merge short sections; tighten captions.
4. **Never cut** the research question, the method and its difference
   from the baseline, the setup needed to judge the comparison, the main
   results table, the required ablation or control, the statistical
   sentence (§5.4), the validity-critical limitations, or the conclusion.
   Never shrink fonts, change margins or line spacing, use negative
   `\vspace`, `\resizebox` tables below legibility, or switch to a
   denser template (the checker flags these, exit 3).
5. **Repeat** until exit 0, or until a failure condition: exit 5 (more
   than `max_iterations` failed rounds), or only protected content remains
   to cut. Then **stop and report**: the measured overflow, what was cut,
   and what remains and why it is essential. Never silently remove
   essential content.
6. **Automatic backstop.** A global Claude Code Stop hook
   (`~/.claude/hooks/page_limit_gate.py`) re-runs the checker on every
   LaTeX project with a `pagelimit.json` that was edited in the session.
   It blocks the agent from finishing while the PDF is over the limit,
   until exit 5. Set `"enforce": false` in `pagelimit.json` to opt out
   for a project.

The Markdown word-count estimate (650 words/page) is only a pre-check.
The compiled-PDF count is authoritative.
