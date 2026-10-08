# Mentorship Principles for Short Benchmark-Centered Projects

Primary source for `research-readiness-advisor`, together with
`~/.claude/skills/benchmark-finder/references/research_advice.md`.
These are project-selection and execution principles, not scientific
evidence: they never establish that a gap exists, a benchmark is
established, or a result is true.

## Core principle

For a beginner completing short research projects, prefer:

problem → established benchmark → published baseline → small method change
→ benchmark comparison → ablation/control → short paper

over:

interesting open-ended question → invent evaluation → create dataset →
build large experimental infrastructure

The goal is not merely to find novel questions. It is to find questions
that can be evaluated cleanly on an established benchmark and turned into a
complete research artifact.

## Research-question guidance

Prefer questions that:

1. map cleanly to an existing benchmark dataset;
2. use an existing benchmark task and metric rather than inventing a new
   evaluation task;
3. have published baseline results that can be directly compared against;
4. allow one small, clearly isolated method change;
5. can produce a main comparison table;
6. can support at least one meaningful ablation, control, or sub-analysis;
7. have an interpretable positive or negative result;
8. do not require creating a new dataset unless dataset creation is
   explicitly the research goal;
9. do not require changing the core research method repeatedly just to
   obtain a result;
10. are appropriately scoped for the user's stated duration and experience
    level.

If the original question is too broad, first try to preserve its core
mechanism while mapping it onto an established benchmark. Do not replace
the original question merely because another unrelated benchmark project is
easier.

## Benchmark-selection guidance

When several benchmarks could evaluate the same direction, prefer ones
with:

1. an established task;
2. a clearly defined evaluation metric;
3. published baseline numbers;
4. public dataset access;
5. public code when available;
6. released model outputs, predictions, probabilities, or intermediate
   results when these substantially reduce execution cost;
7. prior papers that make the relevant literature easy to trace;
8. manageable compute requirements;
9. a simple reproduction path;
10. enough room for a small method change to produce a meaningful
    comparison.

Do not choose a benchmark only because it is easy. It must still measure
the intended research problem.

## Paper target

Practice producing a submission-shaped research artifact, not necessarily
a literal submission. Reference shape: approximately four pages of main
content plus references (unless the user specifies another length):

Abstract · Introduction · Related Work · Method · Experiment · Conclusion

## Baseline and performance

Prefer projects whose method can be compared directly with an established
published baseline. Outperforming a strong baseline, or reaching
competitive performance, is a desirable target, especially for
paper-writing practice. SOTA is NOT required for a result to be
meaningful. For a scientific/diagnostic project, a well-designed negative
result can be useful if the benchmark, comparison, and interpretation are
strong.

## Writing first

Once the research question, benchmark, baseline, and method are selected,
write the full short-paper draft before the main experiment (Abstract,
Introduction, Related Work, Method, Experiment design, Conclusion, main
results table, ablation/control table, planned figures), written around the
working hypothesis that the method achieves the intended improvement
(including beating the target baseline or reaching SOTA when that is the
stated objective). The Conclusion is drafted too. Never fabricate numbers:
unmeasured cells stay TBD, and published baseline numbers are kept distinct
from unobserved proposed-method results. After the experiment, fill in real
results and verify them; if the intended result is not achieved, diagnose,
make small justified changes, rerun within the budget, and finally rewrite
the Abstract, Results, Discussion, and Conclusion to match the evidence.
The pre-experiment conclusion is a working target, not an empirical
result.

## Pivoting

If the initial method underperforms: preserve the core method concept when
reasonable, diagnose the failure, try small justified modifications, avoid
repeatedly replacing the whole direction, and respect the time budget and
stop/pivot criteria. Do not optimize indefinitely merely to beat a
baseline.
