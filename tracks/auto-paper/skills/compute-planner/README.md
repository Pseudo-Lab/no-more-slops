# compute-planner

Estimates what a proposed experiment needs in compute (VRAM, GPUs,
runtime), checks it against the hardware you actually have, and judges
whether **you, at your experience level, can finish the whole project**
(reading, setup, baseline reproduction, implementation, experiments,
analysis and writing) within your time budget. It also gives a difficulty
rating that is used to order projects from easiest to hardest.

## When to use it

- Before you commit to a project: *"Can I do this in 1 week as a
  Beginner?"*
- To see which phase (setup, compute, writing...) limits the schedule, and
  which scope cuts would make the project fit.

## How to use it

```
/compute-planner
Experiment: LoRA fine-tune Llama-3-8B on <benchmark>, 3 seeds, 2 conditions
Duration: 5 working days
Experience level: Beginner
```

Required: the proposed experiment and models, a **per-project duration D**
and an **experience level L** (Beginner / Intermediate / Advanced). The
skill never assumes D or L and asks if they are missing. The training or
inference setup, benchmark readiness, number of seeds and conditions, API or
LLM-judge dependencies and the repo link improve the estimate when you have
them.

## Your hardware: `references/compute.md`

`references/compute.md` in this folder is the **single source of truth**
for available compute. It is also read by benchmark-finder and
experiment-runner. Keep it current: partitions, GPU types, allocation
status, confirmed access. A project-local `compute.md` is never used as a
fallback. If this file can't be read, compute is reported as UNKNOWN rather
than unavailable. Newer information you give in chat overrides the file.

## Output

1. A **compute table**: model size, workload, precision, estimated VRAM,
   GPUs, runtime, minimum and recommended compute, hardware fit, documented
   access, queue time, main bottleneck, recommended change.
2. A **phase-by-phase workflow estimate** in working days at level L, with
   each row labelled VERIFIED / ESTIMATE / RISK, plus a five-bucket summary
   (implementation, compute, evaluation, writing, contingency) and a risk
   table.
3. A **verdict**: `FITS DURATION / DOES NOT FIT DURATION / UNKNOWN`, the
   limiting phase, a LOW/MEDIUM/HIGH difficulty, execution risk, and ordered
   redesign options with re-estimated totals if it doesn't fit.

## Notes

- Experience level changes the *estimate* through learning overhead. It
  never decides eligibility on its own.
- The verdict is always for the project done standalone. "Faster if reused
  after Project X" is listed for information only.
- Within the pipeline, compute-planner alone decides FITS DURATION. No
  other skill overrides it.
