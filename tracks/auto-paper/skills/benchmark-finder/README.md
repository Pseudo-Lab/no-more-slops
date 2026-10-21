# benchmark-finder

Finds an **exact, established benchmark** for each research question, along
with the strongest comparable baseline, that baseline's documented
weaknesses, and the assets you can reuse (code, released models, per-item
outputs). Once a benchmark is provisionally confirmed, it also builds a
lasting prior-work archive for it: `prior_work_<benchmark>.md`.

It covers the *Discover* and *Diagnose* stages of
[research-pipeline](../research-pipeline/README.md).

## When to use it

- You have a research question and need to know whether a real benchmark
  measures exactly that, and not a loose proxy.
- You want the strongest baseline and its known failure modes before you
  design a method.
- [prior-work-checker](../prior-work-checker/README.md) returned FAIL and the
  slot needs a new question (the regeneration loop).

## How to use it

```
/benchmark-finder RQ1: Does <change> improve <metric> on <task> compared with <baseline>?
```

or pass the output of `/research-question-parser`. Plain language works
too: *"Find an exact benchmark for these three ideas; topics may drift."*

### Modes

| Mode | Behaviour |
| --- | --- |
| **Benchmark-First** (default) | The question is a seed. If no exact benchmark exists, the original direction is rejected and the skill searches progressively farther (nearby problem, then the same area, then adjacent areas) until a direction passes validation. The slot ID stays the same. |
| **Fixed-Topic** | Only used when you say the question must be kept. If no exact benchmark exists, it reports `UNRESOLVED — NO EXACT ESTABLISHED BENCHMARK FOUND` and does not substitute a proxy. |

If you mark more fixed topics (K) than requested directions (N), it stops
and asks you to raise N or choose which topics come first.

## What "exact benchmark" means here

A candidate must pass the **SAME-TASK test**, the **comparability check**
and the **validity check (V1–V4)**. Each candidate is labelled EXACT / DIRECT
/ PROXY BENCHMARK / RELATED DATASET / NO BENCHMARK. Only EXACT or DIRECT
counts as support. Ease of execution only breaks ties between benchmarks
that already have a credible, evidence-based path to SOTA.

Every reported question must be a single question ending in "?" that names
the change, the baseline, the benchmark and the metric, for example:
*"Does X reduce error rate on Y compared with Z?"*

## Output

- One report entry per idea or slot: status, candidate question, benchmark
  verification fields, metric, dataset, original paper, code repo,
  representative baseline, reusable components, main evidence gap,
  benchmark readiness, and rejected proxies (for traceability).
- For provisionally confirmed benchmarks, `prior_work_<benchmark>.md`, with
  sections for benchmark identity, search log, prior-work inventory,
  benchmark history, closest work, baseline map, collision check, open gap
  and limitations.

## Files

- `references/research_advice.md`: the main mentoring reference, also
  read by the other research skills.
- `references/benchmark_resources.md`: where to search for benchmarks.
- Compute accessibility is judged against
  `~/.claude/skills/compute-planner/references/compute.md`.

## Next step

Every EXACT or DIRECT slot goes to `/prior-work-checker`.
