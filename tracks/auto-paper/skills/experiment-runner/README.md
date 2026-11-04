# experiment-runner

Takes **one** completed pre-experiment paper from
[paper-writer](../paper-writer/README.md) (`paper_RQk_vN.md`), extracts its
**frozen experimental design**, writes a bounded experiment plan, and then
implements and runs **only** what the paper already specifies: the main
experiment, controls, ablations and statistical test. It saves the results
in a form that paper-writer can use for the post-experiment revision.

> Run the smallest pre-specified experiment set that can answer the frozen
> research question credibly.

It **never adds experiments because a result is weak, null or
surprising.** It is invoked manually only.

## How to use it

```
/experiment-runner paper_RQ1_v1.md
/experiment-runner drafts/paper_v1.md RQ3
```

- `paper_file` (required): a pre-experiment paper whose results are still
  `TBD`. If the paper looks already revised, the skill asks you.
- `RQk` (optional): needed only if the RQ can't be read from the file. If
  it disagrees with the paper, the skill stops and asks.

## Workflow

0. Reads the mentor references, the paper (including its *Revision guide*
   section) and `compute-planner/references/compute.md` for hardware.
1. Extracts the frozen design: RQ, hypothesis, benchmark, split, method,
   baseline, metrics, controls, statistical test, and success and
   stop/pivot criteria.
2. Resolves only the `TBD`s that block the run, recording each decision
   and its source.
3. Writes `experiment_plan_RQk.md`. Once written, this plan is **frozen**.
   Anything not in it goes to `future_experiments_RQk.md`.
4. Implements the minimum code in `experiments_RQk/`.
5. Runs pilot and sanity checks before the full run.
6. Runs the frozen experiment.
7. Saves `results_RQk.md` and machine-readable files in
   `experiments_RQk/outputs/`.
8. Writes a minimal interpretation.
9. **Approval-gated change** (only after a weak, null or negative result):
   diagnoses from existing outputs, proposes **at most one** small
   justified change, and **stops to ask you**. Nothing is re-run without
   your explicit approval of that specific change. Approved reruns are
   logged as deviations and reported *alongside* the original result,
   never in place of it.

## Output (in the paper's folder)

| File | Contents |
| --- | --- |
| `experiment_plan_RQk.md` | Frozen design, experiment list E1…, controls, analyses, implementation decisions, sanity checks, criteria, seed policy, compute estimate, out-of-scope list, deviation log |
| `experiments_RQk/` | Code and `outputs/` (reruns under `outputs/rerun1/`, ...) |
| `results_RQk.md` | Configuration, data, main result with uncertainty, baseline (reproduced next to published), controls, statistical test, sanity checks, failures and deviations |
| `future_experiments_RQk.md` | Ideas that were tempting but out of scope |

Existing files are never overwritten (`results_RQk_v2.md`, ...). If you
re-invoke on the same paper, it reuses the existing plan and continues from
the first incomplete step.

## Next step

```
/paper-writer <RQ_FILE> paper_RQk_vN.md RQk results: results_RQk.md
```
