---
name: prior-work-checker
description: Check, for a benchmark-backed research question, whether prior work already answers it. Traces the papers and baselines that use the benchmark, identifies a verified research gap, and returns PASS or FAIL (FAIL sends the slot back to benchmark-finder for a new research question).
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
(`C:\Users\elika\.claude\skills\benchmark-finder\references\research_advice.md`)
is the PRIMARY and HIGHEST-PRIORITY research-planning reference. Read it
before checking. It is mentorship guidance, not scientific evidence: it must
NOT be used as evidence that a gap exists or that a contribution is novel.
Only traced literature counts as evidence here.

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

For each row, record which of N1–N5 found it.

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

### Step 6: Decide PASS / FAIL

PASS only if ALL hold:

- P1. The research question satisfies the Research Question Format Rule.
- P2. No traced work has a SAME COMPARISON, FUNCTIONALLY EQUIVALENT, or
  SUBSTANTIALLY ANSWERED overlap, and all of N1–N5 were searched.
- P3. The comparison baseline is traced, with an extracted published
  number (not UNTRACED).
- P4. All closest prior works were actually read (none UNREADABLE).
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
Result: PASS / FAIL-<reason>
If FAIL: prior work responsible, and what the next question must avoid

### Iteration History RQk

| Iteration | Research question | Benchmark | Result | Reason / blocking prior work |
|---|---|---|---|---|

## Verification Rules

- Never invent papers, results, numbers, or URLs.
- Do not claim novelty because nothing was found.
- Do not make compute or time judgments, and do not design experiments.
  Those belong to compute-planner and research-planner.
