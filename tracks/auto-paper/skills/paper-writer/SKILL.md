---
name: paper-writer
description: Manually invoked. Turns ONE project's final RQ/research-plan markdown and its provisional paper draft into a complete ~4-page research paper written through the Conclusion (pre-experiment: full narrative written as if the working hypothesis is supported, with every unmeasured number TBD; post-experiment: whole-paper rewrite against the measured evidence). Usage - /paper-writer <RQ_FILE> <DRAFT_FILE> [Project p | RQk | "exact title"] [page limit N] [results: <file or values>]
---

# Paper Writer

Turn one research project's planning artifacts into a complete short
research paper.

One invocation = one project = one paper. This skill is invoked manually.
It is not part of research-pipeline, never runs automatically, and never
processes more than the one selected project.

This skill completes papers. It does not generate or select research
questions, redesign projects, search for new benchmarks, or run
experiments.

## Invocation

```
/paper-writer <RQ_FILE> <DRAFT_FILE> [project identifier] [page limit] [results: <file or pasted values>]
```

Example: `/paper-writer research_pipeline_report_v6.md provisional_paper_drafts_v6.md RQ4 4`
(RQ4, body limited to about 4 pages).

- `RQ_FILE` (required): the project's final RQ / research-plan markdown,
  e.g. a `research_pipeline_report_vN.md`.
- `DRAFT_FILE` (required): the provisional paper draft, e.g.
  `provisional_paper_drafts_vN.md`. For a revision, this may instead be the
  latest `paper_RQk_vN.md` produced by this skill.
- Project identifier: `Project p`, `RQk`, or an exact project title.
  Required only when a file contains several projects (see Step 2).
- Page limit (optional): a positive number N (integer or decimal), given
  as the argument immediately after the project identifier, or anywhere
  as `pages: N`. It sets the maximum length of the paper BODY to about N
  pages (see "Page limit" under Step 6). A bare number with no project
  identifier before it is ambiguous (it could be a project or RQ number):
  ask the user rather than guessing. If no page limit is supplied, the
  default length behaviour in Step 6 applies unchanged.
- `results:` (optional): actual experimental results, as a file path or
  pasted values. Supplying results switches the skill to post-experiment
  revision mode.

Paths may be absolute or relative to the current working directory.

The two supplied files are authoritative. If either is missing, unreadable,
or not supplied, ask the user for the path. Never search for, or substitute,
another RQ file or paper draft.

## Sources and precedence

Resolve information in this order:

1. The supplied RQ / research-plan file: authoritative for the research
   design.
2. The supplied paper draft: authoritative for paper framing and existing
   prose, wherever it does not conflict with (1).
3. Supporting prior-work / benchmark materials for the selected project
   (Step 3).
4. Mentor references (below).
5. General academic-writing conventions.

### Mentor references (read at run time, every run)

Read these completely before writing. Do not reconstruct or invent mentor
advice; use only what these files say.

- `~/.claude/skills/research-readiness-advisor/references/mentorship_principles.md`
  (`C:\Users\elika\.claude\skills\research-readiness-advisor\references\mentorship_principles.md`):
  the PRIMARY mentor reference for this skill. Its "Paper target",
  "Baseline and performance", "Writing first", and "Pivoting" sections
  govern paper shape, execution, experimental reasoning, result
  interpretation, and writing.
- `~/.claude/skills/research-readiness-advisor/SKILL.md`, Step 8
  ("Writing-first workflow"): the pre-experiment draft rules and the
  post-experiment revision sequence.
- `~/.claude/skills/benchmark-finder/references/research_advice.md`:
  benchmark-first project-selection advice; use it only for framing (why
  the paper is built around an established benchmark).

Mentor advice is guidance, not scientific evidence. It never establishes
that a gap exists, a contribution is novel, or a result is true.

Where the mentor reference and a general convention disagree, the mentor
reference wins. In particular, the pre-experiment paper is written as the
paper the project would be if the working hypothesis is supported, and every
unmeasured numerical result stays `TBD` (see "Pre-experiment narrative" and
Claim discipline).

## Workflow

### Step 1: Read the inputs

Read the supplied RQ file and paper draft completely. Read the mentor
references listed above.

### Step 2: Select exactly one project

- Match the identifier against the paper draft's project headings (e.g.
  `## Project p (RQk): Title`) and the RQ file's project headings (e.g.
  `### Project p (...) — Direction RQk`). Accept `Project p`, `RQk`, or an
  exact title.
- The identifier must resolve to the SAME RQk in both files. If it does
  not, report the mismatch and ask the user.
- If both files clearly contain exactly one matching project, proceed
  without asking for an identifier.
- Ask the user when the identifier is missing and several projects exist,
  when it is ambiguous (e.g. a bare number such as `1`, which could mean
  Project 1 or RQ1, and Project p need not be RQp), or when it matches
  nothing. List the projects available in the supplied files.
- Use ONLY the selected project's section of each file. Do not expand,
  rewrite, or summarise other projects.

### Step 3: Locate supporting materials for the selected project

These support the paper; they never replace the supplied inputs.

1. Prior-work archive: the file named on the RQ file's "Prior-work
   archive:" line for this project, resolved relative to the RQ file's
   folder. If none is named, a `prior_work_*.md` in that folder whose
   "Used by projects" line lists the selected RQk. Use its sections 1–4 and
   9 (benchmark identity, search log, inventory, benchmark history, search
   limitations) and the selected RQk's sections 5–8 (closest prior work,
   baseline map, collision check, open gap).
2. Benchmark, validity, and readiness details: the selected project's
   fields in the RQ file (benchmark verification fields, SAME-TASK and
   V1–V4 answers, readiness ratings, stop/pivot criterion, what a negative
   result would mean), plus the archive's section 1.
3. If no matching archive can be found, say so in the reply and write
   Related Work only from the literature named in the supplied files. Never
   fill gaps from memory.

### Step 4: Reconcile and freeze the research design

Extract from the RQ file and keep fixed: final research question,
hypothesis, benchmark, dataset/split, model, baseline, published baseline
values (with sources), metric, intervention, controls, ablations,
statistical testing, collision verdict, gap, and intended contribution.

Do not silently change any of them. If the paper draft conflicts with the
RQ file, use the RQ file for the design, keep the draft's prose wherever it
is compatible, and list every inconsistency in the reply.

If a detail needed for the paper (e.g. a hyperparameter or seed count) is
not decided in the inputs, do not invent it; write an explicit placeholder
such as `[not yet specified: number of seeds]`.

### Step 5: Determine the mode

- Pre-experiment: no actual results supplied. Write the complete paper
  under the working assumption that the hypothesis is supported (see
  "Pre-experiment narrative" below).
- Post-experiment: actual results supplied. Revise the whole latest paper
  (or the draft) against the measured evidence (Step 7).

### Step 6: Write the complete paper

Target about four pages of main content plus references, unless the RQ
file specifies another length. Expand the selected draft into a credible
short research paper; do not replace it with an unrelated paper, and do
not merely lengthen bullet points.

#### Page limit (only when the user supplies one)

A user-supplied page limit N replaces the default target above and any
length in the RQ file, and is a hard writing constraint, not a target to
fill.

- **What counts (the body):** everything from the Abstract through the
  end of the Conclusion, including section headings, tables, table
  captions, equations, and figure placeholders/captions.
- **What does not count:** the title, author/status line(s) under the
  title, the References / bibliography, any source-listing or provenance
  material (e.g. lists of input files, data/code links blocks placed after
  the Conclusion), and the `## Revision guide (not part of the paper)`.
  Keep these after the Conclusion so the boundary is unambiguous.
- **Conversion (fixed, used every time):** 1 page = 650 words of body
  text. Count words as whitespace-separated tokens in the body, with
  Markdown syntax (`#`, `|`, `---`, `**`) not counted as words. Each
  figure placeholder additionally counts as 160 words (one quarter page)
  for the space the figure would occupy. Approximate body pages =
  (body words + 160 × figures) / 650. Budget for N pages = 650 × N
  word-equivalents.
- **Tolerance:** the body may be up to 5% over budget. More than that
  "materially exceeds" the limit and must be revised before saving.
- **How to compress (in this order):** remove repetition across sections
  (Abstract/Introduction/Conclusion restating the same sentences);
  shorten background and motivation; shorten Related Work to the closest
  prior work, the collision verdict and the gap; cut nonessential
  implementation detail and secondary discussion; merge sections where the
  section list allows it; tighten table captions and prose that repeats
  table contents.
- **Never cut to meet the limit:** the research question, hypothesis,
  method (including how it differs from the baseline), experimental design
  (benchmark, dataset/split, model, metrics, statistical test), the
  baseline and its published values with sources, the required controls
  and ablations, the results (main table and the measured or `TBD` values),
  the analysis essential to interpret them, the validity-critical
  limitations, and a substantive Conclusion. All other Step 6 and Step 8
  requirements still apply. If these alone cannot fit within N pages, keep
  them, save the shortest compliant version, and report the overrun and
  why.
- **Before saving:** compute the body word count and page estimate; if
  over tolerance, compress and recount until within it.

Sections (combine where appropriate for space, but never omit Results,
interpretation/Discussion, or Conclusion):

Title · Abstract · Introduction · Related Work · Method · Experimental
Setup · Results · Analysis / Ablations · Discussion · Limitations / Threats
to Validity · Conclusion · References

THE PAPER MUST ALWAYS BE COMPLETED THROUGH THE CONCLUSION. Never stop at an
outline, a skeleton, section notes, a plan, TODOs, or "results will be added
after the experiment".

#### Pre-experiment narrative (writing-first, applied literally)

Before experiments, write the strongest coherent full-paper narrative under
the working assumption that the hypothesis is supported. The Abstract,
Introduction, Results, Analysis, Discussion, and Conclusion read as if the
hypothesised qualitative result is the paper's result:

- State the qualitative result and its interpretation as the paper's
  working conclusion, in plain declarative prose (e.g. "TF-IDF LR
  outperforms BERT-PE (published 65.9%, Table 2); accuracy TBD").
- Do NOT repeatedly qualify the narrative with "expected", "provisional",
  "would", "if the hypothesis holds", "under our working hypothesis", or
  similar hedges, and do not write parallel branches for each possible
  outcome in the paper body.
- Mark the file's pre-experiment status ONCE, in a single short status line
  directly under the title (e.g. "Pre-experiment version: written under the
  working hypothesis; every `TBD` is unmeasured."). Do not repeat it in
  section headings or prose.
- After References, append a short `## Revision guide (not part of the
  paper)` that records, from the RQ file, the stop/pivot criterion, what a
  negative or null result would mean, and which claims the measured numbers
  must support. Step 7 uses it and then deletes it.

The working narrative never authorises quantitative evidence. Every
unmeasured number stays `TBD`, and the prose must not fabricate or imply
measurements: no invented accuracies, margins ("by N points", "a large
margin"), confidence intervals, p-values, statistical significance
("significantly outperforms"), effect sizes, or rankings that depend on an
unmeasured number. Where such a value belongs, write `TBD` (e.g. "ΔAcc
TBD, 95% CI TBD"). Published numbers are stated normally with their
sources. Citations and prior-work findings are never invented.

Limitations / Threats to Validity and "what cannot be concluded" are part
of a real paper and stay in it; write them as the limitations of the
working result, not as hedges on whether the result occurred.

Section requirements:

- Introduction: motivation → problem → closest prior work → precise gap →
  research question → proposed test → contribution. Do not exaggerate
  novelty beyond the prior-work check and archive.
- Related Work: from the archive and RQ file. Explain what the closest work
  tested, how this project differs, what gap remains, and why it is worth
  testing. Respect the collision verdict: PARTIAL OVERLAP must be described
  as partial overlap, never as an absence of related work. Use the archive's
  coverage wording ("systematic benchmark-centered search found ... as of
  <date>"); never claim exhaustive coverage. Never fabricate literature.
- Method: clear enough for a technical reader, with the difference from
  the baseline explicit. Use equations where they add precision. Do not
  invent implementation details.
- Experimental Setup: benchmark, dataset/split, model, baseline,
  preprocessing, hyperparameters, metrics, controls, ablations, statistical
  testing, released outputs/checkpoints, and implementation details, only
  as supported by the inputs; placeholders for undecided details.
- Results: construct the intended final results table(s) and figure
  placeholders. Visibly distinguish published baseline values (with
  source), measured project results, and `TBD` cells. Pre-experiment,
  write substantive prose that reports the hypothesised qualitative result
  as the paper's result and compares it with the relevant baseline, with
  every unmeasured number `TBD`. The negative/null-result meaning goes in
  the Revision guide, not in the Results prose.
- Analysis / Ablations: what each control and ablation tests, which
  competing explanations it separates, and how it affects interpretation of
  the main result. Pre-experiment, state the hypothesised outcome of each
  control as its finding (numbers `TBD`).
- Discussion: what the result means, why the method works (or, after
  experiments, why it did not), alternative explanations, relationship to
  prior work, and what cannot be concluded. Post-experiment, also what a
  negative or null result implies when one was observed. Prefer the
  narrowest defensible interpretation.
- Limitations / Threats to Validity: use the project's own validity
  analysis from the RQ file and archive (e.g. benchmark, model, or domain
  specificity, threshold dependence, released-output limitations,
  calibration or reproduction uncertainty, external validity). No generic
  filler limitations.
- Conclusion (mandatory, substantive): what question was tested; the
  answer (pre-experiment: the working conclusion, stated plainly, with
  numbers `TBD`); the contribution; what the result implies; what remains
  uncertain. Do not add a "provisional" label here; the single status line
  under the title covers it.
- References: only works named in the supplied files and archive, with the
  details given there. Never invent a reference or a reference detail.

### Step 7: Post-experiment revision (when results are supplied)

The pre-experiment paper states the working conclusion as if it held, so
every one of its qualitative claims must be re-checked against the evidence.
Revise the entire paper, not only the `TBD` cells:

1. Replace every relevant `TBD` (and any `EXPECTED` / `HYPOTHETICAL`
   value) with the actual measured results.
2. Verify every numerical claim against the supplied results and sources.
3. Re-check every qualitative claim written under the working hypothesis
   (e.g. "outperforms", "bigrams add accuracy", "the coefficients show ...")
   against the measured numbers; keep it only if the evidence supports it,
   including any significance or CI criterion the design specifies.
4. Update tables and figure descriptions.
5. Rewrite the Abstract.
6. Rewrite Results.
7. Rewrite Analysis.
8. Rewrite Discussion.
9. Revise Limitations where necessary.
10. Rewrite the Conclusion.
11. Revise the title, Introduction contribution list, and any other claim
    or section the evidence affects.
12. Remove the pre-experiment status line and the Revision guide.
13. Check every SOTA or "outperforms" claim against the post-experiment
    SOTA achievement classification (shared definitions §4c in
    `~/.claude/skills/research-pipeline/references/research_design_principles.md`:
    ACHIEVED / NOT ACHIEVED / INCONCLUSIVE). A SOTA claim may stay only
    if it is ACHIEVED. It must name the task, the evaluated slice (if not
    the full benchmark), the baseline, the metric and the model or access
    class. A slice result is never phrased as overall SOTA on the
    benchmark.

If the results differ from the working hypothesis, rewrite the Abstract,
Results, Analysis, Discussion, Conclusion, title and claims as needed, and
any other affected section, so the final paper reflects the measured
evidence rather than preserving the original narrative. Use the Revision
guide's negative/null-result meaning as the starting point. Never
manipulate interpretation to preserve the working conclusion. Negative and
null results are valid outcomes, and the pre-experiment conclusion is a
working target, not a result (mentor reference, "Writing first").

### Step 8: Consistency check (before saving)

Verify, and fix anything that fails:

- the selected project is the correct one;
- the final RQ matches the supplied RQ file;
- the hypothesis matches;
- the benchmark matches;
- the dataset/split matches;
- the model matches;
- the baseline matches;
- the metric matches;
- published numbers are preserved exactly, with sources;
- the method matches the confirmed intervention;
- controls and ablations match;
- prior-work positioning is supported by the archive and matches the
  collision verdict;
- published numbers and this project's numbers remain distinguishable
  (source column or label for every published value; `TBD` or measured for
  every project value);
- pre-experiment: no unmeasured number, margin, CI, p-value, significance
  claim, or effect size appears anywhere, in tables or prose; the narrative
  is not hedged with repeated "expected / provisional / would / if the
  hypothesis holds" language; the single status line and the Revision
  guide are present;
- post-experiment: every qualitative claim is supported by the measured
  results; the status line and Revision guide are removed;
- Results and Discussion are consistent;
- the Abstract and Conclusion are consistent with Results;
- the Conclusion exists and is substantive;
- if a page limit was supplied: the body (Abstract through Conclusion)
  estimate is within the limit plus 5% under the Step 6 "Page limit"
  conversion, with References, source-listing material and the Revision
  guide excluded from the count.

### Step 9: Save the paper

- Destination: the project folder, i.e. the folder containing the supplied
  RQ file. If the RQ file and paper draft are in different folders, or the
  destination is otherwise unclear, ask the user before writing.
- File name: `paper_RQk_v1.md` for the first complete pre-experiment paper.
  For every later revision (after results or other updates), use the next
  unused version number: `paper_RQk_v2.md`, `paper_RQk_v3.md`, and so on.
  Check which versions already exist first.
- Never overwrite an existing paper file.

## Claim discipline

Internally keep every claim in one category, and never confuse them:

- `PUBLISHED`: supported by the benchmark / prior-work sources.
- `MEASURED`: supported by this project's actual results.
- `WORKING`: a qualitative claim written before measurement under the
  working hypothesis.
- `INTERPRETATION`: an inference from published, measured, or working
  findings.

The categories are tracked internally; the prose need not label them.
Pre-experiment, `WORKING` claims are written as plain declarative prose (see
"Pre-experiment narrative"). What keeps them distinguishable from measured
findings is: every unmeasured number is `TBD`; the single status line under
the title; and the Revision guide. Step 7 re-checks every `WORKING` claim
against the evidence.

Pre-experiment numbers (mentor reference takes precedence):

- Keep every unmeasured numerical result as `TBD`.
- Qualitative direction may be stated as the working result, e.g. "TF-IDF
  LR outperforms BERT-PE (published 65.9%, Table 2); accuracy TBD", but
  never with an invented magnitude, CI, p-value, significance claim, or
  effect size.
- Do NOT invent illustrative numbers, marked `EXPECTED` / `HYPOTHETICAL` or
  otherwise, unless the user explicitly requests them in that specific run.
  If requested, label every such value unmistakably as `EXPECTED` or
  `HYPOTHETICAL`.

Never:

- fabricate citations or reference details;
- fabricate prior-work findings;
- fabricate measured results, or any quantitative evidence (margins,
  confidence intervals, p-values, significance, effect sizes);
- strengthen novelty beyond the prior-work evidence;
- keep a pre-experiment `WORKING` claim in a post-experiment paper without
  verifying it against the measured results;
- invent mentor advice.

## Reply to the user

After saving, reply with:

- the saved file path;
- the mode (pre-experiment / post-experiment) and the selected project;
- the supporting sources used (archive file, mentor references);
- any inconsistencies found between the supplied files, and how each was
  resolved;
- placeholders left for undecided details;
- the consistency-check result;
- if a page limit was supplied: the requested page limit; the approximate
  body word count (and figure placeholders counted); the approximate
  body-page estimate (at 650 words/page); confirmation that References,
  bibliography, source-listing material and the Revision guide were
  excluded from the count; and, if the limit could not be met, the overrun
  and why.

The paper itself goes in the file. Do not reply with only an outline,
suggestions, section summaries, TODOs, or writing advice.

## Constraints

Do NOT:

- run experiments;
- generate or select new research questions, or redesign the project;
- search for a new benchmark unless the user explicitly asks;
- modify research-pipeline or any other research skill;
- process more than the one selected project;
- replace the supplied input files with versions found elsewhere;
- invent mentor advice, citations, or measured results;
- stop writing because experimental results are unavailable.
