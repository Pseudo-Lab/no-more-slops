---
name: prior-work-checker
description: Check, for a benchmark-backed research question, whether prior work already answers it. Runs a staged (rapid screen → focused → final verification) multi-source literature investigation, including component and combination analysis for multi-component methods; identifies the three closest prior works and the strongest published baseline; classifies novelty (NOVEL / PARTIAL OVERLAP / ALREADY STUDIED / UNCERTAIN); maps that classification onto the existing PASS or FAIL gate (FAIL sends the slot back to benchmark-finder for a new research question); and writes a reusable Prior-Work Evidence Report that downstream skills consume.
---

# Prior Work Checker

Run immediately after benchmark-finder, on every slot that has an EXACT /
DIRECT benchmark. Its job is to make sure the proposed research question has
not already been answered, and that the baseline it will be compared against
is actually traced in the literature.

Workflow per slot:

    Research question
    → Find the relevant benchmark (from benchmark-finder)
    → Trace the prior work and baselines that use that benchmark
    → Identify a research gap
    → PASS / FAIL

A slot that FAILS goes back to benchmark-finder, which generates a new
research question for the same slot (same RQ identifier). The new question
comes back here for a fresh check. Repeat until the slot PASSES (see
Iteration Loop).

## Priority Reference

`~/.claude/skills/benchmark-finder/references/research_advice.md`
(`C:\Users\<user>\.claude\skills\benchmark-finder\references\research_advice.md`)
is the PRIMARY and HIGHEST-PRIORITY research-planning reference. Read it
before checking. It is mentorship guidance, not scientific evidence: it must
NOT be used as evidence that a gap exists or that a contribution is novel.
Only traced literature counts as evidence here.

## Procedure Resources (owned by this skill)

- [references/prior_work_novelty_sota_review.md](references/prior_work_novelty_sota_review.md)
  holds the mandatory investigation procedure:
  - the three stages (§1);
  - sources and query strategies Q1–Q9 (§2);
  - combination analysis (§3);
  - the three closest papers (§4);
  - the novelty classification (§5) and its mapping onto this skill's
    PASS / FAIL gate (§6);
  - the Prior-Work Evidence Report schema (§7);
  - how downstream skills consume the report (§8);
  - authority rules (§9).

  research-readiness-advisor, research-planner and research-pipeline
  link to this same file. Keep a single copy; never duplicate it.
- [references/worked_example_epc_monitoring.md](references/worked_example_epc_monitoring.md)
  works through the procedure for Execution × Probe × CoT monitoring. It
  demonstrates the process only. Its verdicts are dated and must not be
  reused.
- Shared definitions:
  [research_design_principles.md](../research-pipeline/references/research_design_principles.md)
  (technical depth §3, S1–S4 §4, mandatory gates §7). This skill applies
  gate 4 (prior-work verification). It does not rate SOTA potential,
  depth or feasibility.

This skill alone issues the novelty classification and the novelty gate.
No other skill re-classifies novelty.

## Research Question Format Rule

Every research question received or produced by this skill must:

1. Be a single interrogative sentence that ends with "?".
2. Start with an interrogative form (Does / Do / Is / Are / Can / Will /
   Which / How much / To what extent ...).
3. Not be an imperative ("Evaluate whether ..."), a noun phrase or title
   ("Effect of X on Y"), a hypothesis statement, or a method description.
4. Contain exactly one question (no chained "... and does ...?", no second
   question mark).
5. Name the proposed change, the comparison baseline, the benchmark, and
   the main metric, e.g. "Does <change> <increase / reduce> <metric> on
   <benchmark> compared with <baseline>?"
6. Be answerable directly from the main results table (yes / no, or which
   is better, on the established metric).

If an incoming question violates the rule, rewrite it into the required
form without changing its content, and record the rewrite. Do not check a
question until it is in question format.

## Input

For each slot:

- Slot identifier (RQk) and iteration number
- Research question (in question format)
- Exact benchmark and its verification fields (from benchmark-finder)
- Proposed change and comparison baseline
- Candidate model(s), if specified
- Previously failed questions for this slot and why they failed (from
  earlier iterations)

## Workflow

### Step 1: Confirm the benchmark

Restate the benchmark name, paper, task, evaluation set, and main metric
from benchmark-finder. Do not re-classify it here; if the benchmark is not
EXACT / DIRECT, or its benchmark validity check (V1–V4) has a NO, return the
slot to benchmark-finder without a prior-work check.

### Step 2: Trace prior work that uses the benchmark

Run the investigation in stages (resource §1):

- **Stage 1, rapid screening.** Run it on every candidate, including
  method ideas at the benchmark-screening stage (the "early kill check"
  in shared definitions §1c). It looks for:
  - obvious prior-work collisions;
  - a stronger existing method;
  - an untraceable baseline;
  - a fatal constraint.

  It returns KILL or CONTINUE.
- **Stage 2, focused investigation.** Run it on shortlisted and
  regenerated candidates. It covers all of the searches below plus
  resource §2–§4, and it produces a DRAFT Evidence Report.
- **Stage 3, final verification.** Run it before any GO.
  - From primary sources, re-verify the strongest baseline, the novelty
    classification and the mechanism's cause evidence.
  - Run a recency search.
  - Mark the Evidence Report FINAL.

A PASS issued before Stage 3 is provisional. The pipeline's
pre-implementation evidence gate requires a FINAL report.

Search, in this order, and record every search in the trace:

1. The benchmark's original paper: its own baselines, ablations, and
   mitigation / method sections.
2. The benchmark's official repository and leaderboard (README results,
   issues, linked follow-ups).
3. Papers that cite or evaluate on the benchmark: citation listings
   (Semantic Scholar / Google Scholar "cited by"), Papers with Code /
   Hugging Face pages, and arXiv / web search on
   "<benchmark name> + <proposed change>" and
   "<benchmark name> + <method family>".
4. Papers on the proposed change itself (the method's original paper and its
   follow-ups), checked for evaluations on this benchmark or its metric.
5. Recent surveys of the area, if they exist.

Search at least once with each of: the benchmark name, the proposed method
name, and a plain-language description of the comparison.

Do not decide novelty from matching terminology. Explicitly search for, and
record in the trace, each of:

N1. The same intervention on the same benchmark.
N2. Functionally equivalent interventions under different terminology
    (synonyms, the underlying mechanism described in plain language, older
    or field-specific names for the same technique).
N3. The same method on closely related benchmarks or metrics.
N4. Prior experiments that effectively answer the research question even if
    they frame it differently (e.g. an ablation or analysis section of a
    larger paper).
N5. Papers that directly compare the proposed method with the named
    baseline, on any benchmark.

**Query strategies (in addition to N1–N5).** Apply Q1–Q9 from resource
§2b:
- exact method names;
- synonyms;
- each component on its own;
- pairwise and higher-order combinations;
- the same mechanism under other framings or in other fields;
- comparable benchmark evaluations;
- recent or concurrent work;
- backward and forward citation traces (Q9).

Tick off resource §2b's completeness checklist.

Cover arXiv, Google Scholar, OpenReview, Semantic Scholar, OpenAlex,
Crossref, GitHub, published proceedings, author or institutional pages
and citation networks (resource §2a).

**Source access and fallbacks (resource §2a-1, §2a-2).** At the start of
each Stage 2 or Stage 3 session:
- Probe each source with a known-answer query and record it WORKING /
  RATE-LIMITED / BLOCKED / NOT TESTED.
- Use the fallback ladders for discovery, identity, citations and full
  text. Never work around a block, captcha or paywall.
- Record unreachable sources as UNREACHABLE.

A failed retrieval is never evidence of novelty, and a higher hit count
is never evidence of coverage.

**Verification levels (resource §2a-3).** Record every paper as
FULL-TEXT, ABSTRACT-ONLY, METADATA-ONLY or SECONDARY.
- "Read" (P4) means FULL-TEXT.
- Never infer methodological difference or novelty from an abstract.

**Multi-component methods.** When the proposed change combines several
methodological components, run the combination analysis in resource §3:
1. Define each component operationally.
2. Enumerate the non-empty subsets.
3. Prune irrelevant subsets, recording the reason for each.
4. For every remaining subset, record:
   - the closest work;
   - whether it has been studied;
   - whether it is evaluable on this benchmark.

Combining components that are already studied is not novel by itself.
Without a documented complementarity argument, the combination is at
best PARTIAL OVERLAP, and the technical-depth flag goes to
research-readiness-advisor.

For the closest prior works (anything that might already perform the
comparison), open and read the paper itself (HTML, PDF, or official page).
A search snippet, abstract summary, or citation context alone is not enough
to rule a work in or out. If a closest prior work cannot be opened, record
it as UNREADABLE.

### Step 3: Build the prior-work table

| Paper | Uses this benchmark? | Method / condition evaluated | Model(s) | Metric | Reported result | Overlap with the RQ |
|---|---|---|---|---|---|---|

Overlap with the RQ is one of:

- SAME COMPARISON: same benchmark, same metric, same proposed change (or a
  trivially equivalent one) vs. the same kind of baseline.
- FUNCTIONALLY EQUIVALENT: the same experiment in substance under different
  terminology or framing, or one that differs only in a minor protocol
  detail (seed, prompt wording, split, decoding setting, model size within
  the same family). Treated exactly like SAME COMPARISON.
- SUBSTANTIALLY ANSWERED: not the identical comparison, but its results
  (alone or together with other traced works) already let a reader predict
  the answer to the research question with reasonable confidence, e.g. the
  same method shown on several closely related benchmarks with consistent
  effects, or an ablation that isolates the same variable.
- PARTIAL: same benchmark but a different change, or the same change on a
  different benchmark/metric, or the same comparison on a substantially
  different model class, where the answer to the research question still
  cannot be inferred.
- BACKGROUND: related but does not perform the comparison.

For each row, record which of N1–N5 or Q1–Q9 found it.

**Three closest prior works.** For each serious candidate, also fill the
resource §4 closest-work table for the three closest papers. List fewer
only when fewer exist, and say why. Each row records:
- exact title, authors, date, venue and link;
- relevant sections;
- methodological similarity;
- benchmark and protocol;
- reported performance;
- exact differences;
- overlap degree: IDENTICAL / SUBSTANTIALLY EQUIVALENT / PARTIAL /
  RELATED-DIFFERENT (these map onto the overlap classes above);
- read status.

Verify each paper's bibliographic identity from the primary source.

**Reading depth and literature map (resource §2d, §4a; added
2026-10-17).**
- Read every ledger paper to pass 1 (five Cs). Read the three closest
  papers and the strongest baseline paper to pass 2. Read the strongest
  comparable baseline and the single closest paper to pass 3 ("virtual
  re-implementation": list their implicit assumptions and evaluation
  weaknesses).
- Grow the survey by snowballing: shared citations, repeated authors,
  recent top-venue proceedings.
- Fill the eight-field literature map, including **evidence against the
  hypothesis** and **potentially overlooked work**. Both searches are
  mandatory, and an empty result is recorded with its queries.

### Step 4: Trace the baselines

For the baseline named in the research question, extract from the source
itself:

- Published baseline result: the actual number(s), with the table/figure
  where they appear
- Model, setting, and split the number refers to
- Whether code or outputs to reproduce it are public

A baseline whose number cannot be extracted from a readable source is
UNTRACED.

Also list the strongest published results on this benchmark for the same
setting, so the proposed change is not compared only to a weak baseline.

Record the strongest published comparable baseline (method, metric,
number, source location, access class) and its documented failure modes,
each with its source. Keep cause evidence separate. These fill the
Evidence Report fields "Strongest published baseline" and "Known failure
modes", which research-readiness-advisor uses for S1 and S2 without
repeating the trace. benchmark-finder's mature baseline map remains the
authority for UNMEASURED systems.

### Step 5: Identify the research gap

State the gap in this form:

    Closest prior work: <citation(s)>, which evaluated <exactly what>.
    What remains untested: <proposed change> against <baseline> on
    <benchmark> (<metric>), because <the specific difference that the
    closest work did not test>.
    No directly equivalent experiment was found in the searched literature
    (search trace: Step 2, N1–N5).

The gap must be narrow and correspond exactly to the research question.
Never claim novelty or that "no prior work exists": write "No directly
equivalent experiment was found in the searched literature", not "novel",
"first", or "unexplored".

A minor protocol difference from the closest prior work (see FUNCTIONALLY
EQUIVALENT) is not a gap.

### Step 5b: Classify novelty (resource §5)

Classify the candidate's contribution as exactly one of:
- NOVEL
- PARTIAL OVERLAP
- ALREADY STUDIED
- UNCERTAIN

Give the six-point explanation:
1. closest work;
2. what has been studied;
3. what differs;
4. whether the difference is scientifically meaningful;
5. benchmark overlap;
6. the remaining uncertainty.

Rules:
- NOVEL needs a positive statement of what is methodologically new.
  "Nothing found" never earns NOVEL.
- An identical combination that is merely untested on this benchmark is
  a defensible gap only if you name the specific property of this
  benchmark or failure mode for which prior results do not predict the
  answer. Otherwise the gap is SUBSTANTIALLY ANSWERED.
- "NOVEL" is an internal label. The gap-statement wording rule in
  Step 5 still applies.
- Also assign the **novelty type** (resource §5a): NT-A new application /
  NT-B modification / NT-C new mechanism / NT-D implementation
  correction. Use the weakest type the evidence forces. NT-C requires a
  mechanism-level search of resembling mechanisms. The type caps novelty
  strength. It does not change PASS / FAIL.
- In the baseline trace (Step 4), keep the four performance-claim levels
  apart (shared definitions §4f): overall SOTA on the standard protocol;
  the best **reproducible** baseline; any selected baseline; results
  under restricted protocols. Record which published numbers are
  reproducible (code or outputs released) and which use incompatible
  protocols.

### Step 6: Decide PASS / FAIL

PASS only if ALL hold:

- P1. The research question satisfies the Research Question Format Rule.
- P2. No traced work has a SAME COMPARISON, FUNCTIONALLY EQUIVALENT, or
  SUBSTANTIALLY ANSWERED overlap, and all of N1–N5 were searched.
- P3. The comparison baseline is traced, with an extracted published
  number (not UNTRACED).
- P4. All closest prior works were actually read (none UNREADABLE).
  "Read" means FULL-TEXT verification (resource §2a-3), from a primary
  copy or a verified archived copy of the primary URL. ABSTRACT-ONLY
  never satisfies P4.
- P5. The gap statement in Step 5 can be written without hedges such as
  "verify", "may already exist", "to be checked", or "reportedly".

Otherwise FAIL, with exactly one primary reason:

- FAIL-ALREADY-DONE: a traced work performs the same comparison, or a
  functionally equivalent one (cite it).
- FAIL-SUBSTANTIALLY-ANSWERED: traced work already substantially answers
  the question (cite it and explain why the answer is predictable). The
  slot must be redesigned or replaced, not passed on a minor protocol
  difference.
- FAIL-NO-BASELINE: the baseline cannot be traced to a published number.
- FAIL-UNVERIFIED: a closest prior work could not be read, or the gap
  depends on unchecked claims.
- FAIL-FORMAT: the question cannot be put into the required form without
  changing its content.

PARTIAL overlaps do not cause a FAIL, but they must be listed and the gap
must be stated relative to them.

**Classification → gate mapping (resource §6; the stricter rule always
wins):**

| Classification | Gate |
|---|---|
| NOVEL | PASS only if P1–P5 hold |
| PARTIAL OVERLAP | PASS only if P1–P5 hold and the gap passes the "untested on this benchmark" rule (Step 5b) |
| ALREADY STUDIED | FAIL-ALREADY-DONE or FAIL-SUBSTANTIALLY-ANSWERED |
| UNCERTAIN | FAIL-UNVERIFIED, never PASS. If the uncertainty can be resolved within the stage budget, resolve it first and reclassify |

The classification and the gate must agree with this table. If they
disagree, the gate is wrong.

A PASS settles novelty only. Whether the contribution is meaningful
(technical depth, §4e) is decided by research-readiness-advisor.

## Iteration Loop

On FAIL:

1. Return the slot to benchmark-finder with: the failed research question,
   the FAIL reason, the prior works that caused it, and every earlier
   failed question for this slot.
2. benchmark-finder generates a NEW research question for the same slot ID
   (a different proposed change on the same benchmark, or a different
   exact benchmark), in question format, and excluding everything already
   failed or already covered by the cited prior work.
3. The new question comes back to this skill as iteration n+1.
4. Repeat until the slot PASSES.

Never pass a slot by relaxing P1–P5. Never reuse a failed question with
cosmetic rewording.

The loop ends without a PASS only when benchmark-finder reports that its
exhaustive replacement search can produce no further exact-benchmark
candidate for the slot that is not excluded. Then mark the slot:

    UNRESOLVED — NO DIRECTION PASSED THE PRIOR-WORK CHECK

and rank it last.

## Output

For each slot:

### Prior-Work Check RQk (iteration n)

Research question:
Benchmark:
Search trace: (sources and queries from Step 2)
Prior-work table: (Step 3)
Baseline trace: (Step 4)
Novelty search coverage: N1–N5, each with the queries used and what was
found
Closest prior work and what remains untested: (Step 5)
Research gap: (Step 5)
Novelty classification: NOVEL / PARTIAL OVERLAP / ALREADY STUDIED /
UNCERTAIN, with the six-point explanation (Step 5b)
Combination analysis: (multi-component methods only; resource §3)
Three closest prior works: (resource §4 table)
Result: PASS / FAIL-<reason> (consistent with the Step 6 mapping);
provisional until Stage 3
If FAIL: the prior work responsible, and what the next question must
avoid
Evidence Report: `prior_work_evidence_<run-tag>_<RQk>.md` in the project
working directory (resource §7), with status DRAFT / FINAL and evidence
quality Verified / Partial / Unverified

The Evidence Report is the reusable hand-off. Downstream skills cite its
fields instead of repeating the literature review.

### Iteration History RQk

| Iteration | Research question | Benchmark | Result | Reason / blocking prior work |
|---|---|---|---|---|

## Verification Rules

- Never invent papers, results, numbers, or URLs.
- Do not claim novelty because nothing was found.
- Do not make compute or time judgments, and do not design experiments.
  Those belong to compute-planner and research-planner.
- Do not rate SOTA potential, technical depth or novelty *strength*.
  Those belong to research-readiness-advisor, which reads the Evidence
  Report.
- Record unreachable sources and unreadable papers explicitly. They push
  the classification toward UNCERTAIN, never toward NOVEL.
- Never hard-code conclusions from a past review, including the worked
  example, into a new check. Re-verify everything.
