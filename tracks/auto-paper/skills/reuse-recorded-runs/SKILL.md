---
name: reuse-recorded-runs
description: Change the protocol of finished LLM or agent experiments (repair or step limit, number of runs, verifier threshold, final-answer rule, added arm) by reusing recorded trajectories instead of rerunning everything. Use when results are in and a setting must change; classifies each change as exact recomputation, continuation, partial rerun from shared first proposals, or new run, then checks pairing, provenance and disclosure.
---

# Reuse recorded runs

A paid run is evidence. When a setting changes after the results are in, rerun
only what the change can affect, recompute the rest exactly from the records, and
say in the paper which choices were made after seeing these examples.

## What the records must hold

Reuse is possible only if each run saved, per example × run × method, the full
attempt trace: every proposal, the verifier's raw output and pass flag, the
feedback actually shown to the generator, the score of each attempt, and usage
and latency. The run's manifest must hold the code hash, data hash, model
snapshots, prompts, every setting (limit, thresholds, final rule), prices and
API routes, plus a fingerprint of all of them. All methods of an example must
start from one shared first proposal. If a run lacks this, say which changes
can no longer be derived and plan a new run instead of approximating.

## Classify the change before touching an API

Ask two questions: does the generator or verifier ever *see* the setting, and
does anything execute before the loop ends? Then pick the cheapest valid route.
[The decision table](references/decision-table.md) has conditions and traps.

| Change | Route | New requests |
| --- | --- | --- |
| Smaller repair/step limit | Exact: cut each trajectory at the new limit | None |
| Which proposal is final when none passes (last, first, abstain) | Exact: choose among recorded attempts; same cost and time | None |
| Larger limit, limit not shown to any model, nothing executed | Continuation: replay the saved prefix, assert it matches, generate only past the old limit, only for rows that reached it | Rows that reached the limit |
| Threshold, feedback text, history format, prompt — anything a model sees | Partial rerun from each example's shared first proposal | Rows whose first proposal was rejected, re-verified |
| Another sample, more runs, another generator | New run with new first proposals (check they are new) | Everything |
| Added comparison arm on the same examples | New method from the saved first proposals | That arm |

A verifier that is not deterministic changes some verdicts even on the same
proposal. Before attributing a rerun's difference to the setting, measure how
often repeated verification of identical proposals flips.

## Procedure

1. Write the change as a decision with date and reason in the project's decision
   log. Note whether it was chosen after seeing results on the same examples.
2. Estimate the cost: `scripts/reuse_runs.py plan RUN --new-limit R` counts
   rows that reached the limit and rows whose first proposal was rejected. Multiply
   by the tokens per attempt of the recorded rows and the prices in the manifest.
   Share the estimate before spending.
3. Freeze the code that produced the source runs. Continuations and reruns must
   refuse a source with another code hash, data hash or model; route changes
   (gateway vs direct) are allowed only when recorded attempt by attempt.
4. Run or derive into a new directory. Never edit or overwrite source records;
   a derived run records its parts (paths, fingerprints, record hashes).
5. Check before reporting:
   - `pairing`: within a run, every method shares each example's first proposal;
     a rerun shares the source's; a repeat does not copy run 1.
   - `overlap`: a continued run cut at the source limit reproduces every source row.
   - Overlapping numbers agree: the curve at the default limit equals the table.
   - Summaries that read "the final proposal" use the chosen attempt, not the last.
6. Compare on the same trajectories. For a rule change, report both rules on the
   same records with a paired interval (`paired`): what each fixes and breaks,
   including where the preferred rule loses.
7. Keep every run. Do not drop or replace a run after seeing its result; report
   means and spread across runs and average each example over runs before
   resampling examples.

## Disclose

In Methods, say how the reported runs were made (continued, rerun from shared
first proposals, derived). In Limitations, list each setting chosen after seeing
these examples. In the repository, keep the decision log and a validation note
per change: commands, time, cost, checks run, and anomalies.

## Script

`scripts/reuse_runs.py` (Python 3.10+, standard library) works on JSON Lines
records with configurable dotted field paths; see [the script guide](references/script.md).

~~~sh
python3 scripts/reuse_runs.py --passed gate_pass --correct score.correct --row-correct score.correct \
  derive results/run1 results/run1_first --limit 3 --rule first --methods jbfc
python3 scripts/reuse_runs.py pairing results/run1 results/run1_rerun --expect shared
python3 -m unittest discover -s tests -v
~~~

[The week-2 case](references/case-jbfc.md) shows each route on a real study: a
limit raised from 2 to 3, three repeated runs, thresholds 0.8/0.7/0.5 and a
final-answer rule, with what each cost.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.
