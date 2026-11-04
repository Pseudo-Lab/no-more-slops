# prior-work-checker

Checks whether a benchmark-backed research question has **already been
answered** by published work, and whether the baseline you plan to beat can
be traced to a published number. It returns **PASS** or **FAIL** for each
slot and writes a reusable *Prior-Work Evidence Report*.

## When to use it

- Right after [benchmark-finder](../benchmark-finder/README.md), on every
  slot that has an EXACT or DIRECT benchmark.
- Any time you want an evidence-based novelty check on one specific
  question before investing days in it.

## How to use it

```
/prior-work-checker RQ3: Does <change> increase <metric> on <benchmark> compared with <baseline>?
```

Give it what you have: the slot ID, the question, the benchmark and its
verification fields, the proposed change and baseline, the candidate
models, and any earlier failed questions for this slot.

## How it works

1. **Staged literature search**: a quick screen, then a focused search,
   then a final full-text check across several sources. For methods with
   several components, it also checks each component and each combination.
2. Identifies the **three closest prior works** and the **strongest
   published baseline**.
3. Classifies novelty as **NOVEL / PARTIAL OVERLAP / ALREADY STUDIED /
   UNCERTAIN**.
4. Maps that label onto the gate:

| Classification | Gate |
| --- | --- |
| NOVEL | PASS if P1–P5 all hold |
| PARTIAL OVERLAP | PASS only if P1–P5 hold and the gap is "untested on this benchmark" |
| ALREADY STUDIED | FAIL (ALREADY-DONE or SUBSTANTIALLY-ANSWERED) |
| UNCERTAIN | FAIL-UNVERIFIED, never PASS |

P1–P5 cover the question format, no equivalent comparison existing, a
traced baseline number, full-text reading of the closest works (an abstract
alone is never enough), and a gap statement with no hedging.

## The FAIL loop

On FAIL, the slot goes back to `benchmark-finder` with the reason and the
blocking papers. benchmark-finder writes a genuinely new question under the
same `RQk`, and that question returns here as the next iteration. A reworded
version of a failed question does not count as new. If no candidates remain,
the slot is marked
`UNRESOLVED — NO DIRECTION PASSED THE PRIOR-WORK CHECK`.

## Output

- `Prior-Work Check RQk (iteration n)`: prior-work table, traced baseline,
  gap, classification, PASS/FAIL with a single reason.
- `Iteration History RQk`.
- The Prior-Work Evidence Report (`prior_work_evidence_<run-tag>_<RQk>.md`).
  [research-readiness-advisor](../research-readiness-advisor/README.md) and
  [research-planner](../research-planner/README.md) read this file and do
  not repeat the check.

## Files

- `references/prior_work_novelty_sota_review.md`: the full procedure and
  the Evidence Report schema. The pipeline treats this as the reference for
  novelty.
- `references/worked_example_epc_monitoring.md`: an end-to-end example.

A PASS settles **novelty only**. Whether the contribution is substantial
enough is decided by research-readiness-advisor.
