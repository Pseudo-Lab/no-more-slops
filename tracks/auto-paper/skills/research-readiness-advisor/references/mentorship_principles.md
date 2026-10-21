# Mentorship Principles for Short Benchmark-Centered Projects

Primary source for `research-readiness-advisor`, together with
`~/.claude/skills/benchmark-finder/references/research_advice.md`.
These are project-selection and execution principles, not scientific
evidence: they never establish that a gap exists, a benchmark is
established, or a result is true.

## Shared definitions

These terms are defined in
`~/.claude/skills/research-pipeline/references/research_design_principles.md`:
- Beginner
- Technical depth
- SOTA potential vs SOTA achievement
- D-day feasibility
- Research redesign
- Mandatory gates

Use those definitions; this file never redefines them.

The advisor's role is to **design** strong projects (Discover → Diagnose →
Design → Scope → Evaluate → Refine → Select), not only to filter them.
"Beginner" describes the researcher's experience, not a limit on the
project's technical difficulty.

## Core principle

For a beginner completing short research projects, prefer:

problem → established benchmark → strongest comparable baseline and its
documented weakness → targeted, technically meaningful intervention →
benchmark comparison → ablation/control → short paper

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
4. allow one clearly isolated intervention whose mechanism targets a
   documented weakness of the strongest baseline. Isolated means small
   in scope; it does not mean technically trivial. A fixed threshold,
   vote or average is not enough as the whole contribution (technical
   depth, shared definitions §3);
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
8. manageable compute requirements (judged against the global
   `~/.claude/skills/compute-planner/references/compute.md`; a GPU that
   is documented as available but not yet allocated is manageable, not
   missing);
9. a simple reproduction path;
10. enough documented headroom for a targeted intervention to produce a
    meaningful comparison.
11. released models, checkpoints, adapters, transcripts or activations
    that make white-box, fine-tuning or GPU work feasible within D. These
    are enablers; their absence is not by itself a reason to exclude such
    work.

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

## Mentor advice: Minhyeong Yu

Recommendations from the user's research mentor. They refine the sections
above; they are not universal publication requirements and do not override
hard gates or the Negative-Result Interpretability Review
(`research-readiness-advisor` Step 5b).

1. Topic priorities. Achieving SOTA, or a clear improvement over strong
   existing baselines, is a HIGH PRIORITY in topic selection. Before
   approving a topic, evaluate BOTH experimental performance potential
   and novelty. Among topics that pass the mandatory gates (experimental
   validity, feasibility within D, and minimum novelty = prior-work-checker
   PASS; never traded off), rank in this order:
   1. SOTA potential (PRIMARY): a credible, realistic path to beating the
      strongest comparable baseline, ideally reaching SOTA.
      Pre-experiment potential (S1–S4, shared definitions §4b) is a
      different thing from post-experiment achievement (§4c):
      - Pre-experiment HIGH needs no experimental proof. It needs:
        - a documented weakness and headroom (S1), with verified facts;
        - a mechanism that targets the cause of that weakness, with a
          technically credible reason to expect improvement (S2);
        - a fair, reproducible test (S3);
        - a feasible minimal design (S4). Unverified GPU allocation or
          unknown queue time alone never weakens S4 (§4b note).
      - A method being novel, promising, or theoretically capable of
        improving is never enough for HIGH. Speculation never counts as
        STRONG.
      - SOTA potential is rated under the evidence rules of shared
        definitions §4d:
        - a baseline-maturity audit;
        - weak baselines are not headroom;
        - cause evidence is required for S2;
        - no conditional HIGH;
        - an expected margin vs the MDE;
        - calibration against past outcomes.
   2. Four-day feasibility margin (contingency, verified requirements).
   3. Defensible contribution (shared definitions §4e): a non-obvious
      finding in at least one outcome, and a reviewer pre-mortem answered
      inside D. Confirmatory engineering does not qualify.
   4. Novelty: contribution beyond prior work, as verified by
      prior-work-checker (never asserted by the advisor). Modest novelty
      is acceptable when 1–3 are strong.
   5. Negative-result interpretability.
   Do not prefer a highly novel topic with weak performance potential over
   a topic with a credible path to SOTA when both pass the gates. This is
   the topic-ranking order in `research-readiness-advisor` Step 5c.
2. Benchmark-first. Already the core principle above and in
   `research_advice.md`; the mentor's reason is that established
   benchmarks make experiments easier to execute, compare, and evaluate.
3. Headroom. Prioritize problems with substantial, realistic room for
   performance improvement over the published baseline (not near ceiling,
   and not a gap that only a much larger model or budget could close),
   with a clear numerical baseline the experiment is designed to beat.
   This strengthens benchmark-selection item 10. Treat weak expected
   performance relative to existing methods as a significant publication
   risk and state it as such.
4. Iteration. If initial experiments do not improve performance, explore
   alternative approaches and iterate, within the time and compute budget
   and the stop/pivot criteria (see Pivoting). Iteration refines the method
   for the same question; it never means adding experiments because a
   result is weak.
5. Statistical significance. Keep three things separate:
   - Statistical significance: rigorous validation generally improves
     research quality, but it is not universally required in computer
     science, e.g. when runs are too expensive to repeat.
   - Practical significance: whether the improvement is large enough to
     matter. Significance matters most when the gain over prior results is
     small enough that reviewers could reasonably attribute it to chance.
   - Computational feasibility: when repetition is affordable, use
     repeated runs/seeds, confidence intervals, or an appropriate
     statistical test to show the improvement is reliable; when it is not,
     state the limitation instead of implying reliability.
   A non-significant result is never evidence of no effect (Step 5b).
6. Publication strategy. Weak experimental evidence gives reviewers
   grounds for rejection, so strong empirical prospects and novelty are
   prioritized during topic selection. After a small (pilot) experiment
   establishes feasibility, start drafting the paper early and fill in
   result tables as experiments progress, consistent with Writing first.

SOTA improvement is the primary research objective. By default, a
**credible SOTA path** is a mandatory gate: SOTA potential of at least
MEDIUM, with HIGH preferred (shared definitions §7, gate 9). The user may
instead:
- raise the bar to "HIGH required"; or
- waive the gate for an explicitly scientific-diagnostic goal.

Uncertainty about the experimental outcome is never a reason to reject
on its own. These preferences never override the other hard gates, and
never skip the mandatory Negative-Result Interpretability Review. A
precise negative result remains a legitimate, publishable outcome of a
project selected for its SOTA potential.

## Mentor feedback on a submitted paper (recorded 2026-10-17)

This feedback comes from the user's mentor, on one of the user's papers.
It refines the sections above and is operationalised in the files named
below. Read those files; do not paraphrase this section into new rules.

1. **Tables should look like major-CS-conference tables.**
   - Existing methods appear under their established names, with
     citations.
   - Published results from the original papers are used where
     appropriate, and are visibly distinguished from results reproduced
     in our own experiments.
   - Our experimental configurations do not replace standard method names
     in the main comparison table.

   → `~/.claude/skills/paper-writer/references/paper_standards.md` §4;
   templates in `paper-writer/templates/tables/`; checker
   `paper-writer/scripts/check_tables.py`.
2. **p-values and CIs are not routine in main tables.** Statistical
   validity stays required. Placement follows the venue: point estimates
   (± std) in the table, the test result in the text, full statistics in
   the appendix. → `paper_standards.md` §5 (rigor vs presentation).
3. **Page limits need programmatic enforcement, not instructions.** →
   `paper_standards.md` §6; `paper-to-latex/scripts/check_page_limit.py`
   (compiled-PDF count); the global Stop hook
   `~/.claude/hooks/page_limit_gate.py`.
4. **Ideas need causal, domain-specific justification.** The test-case
   generation proposal assumed that an LLM generator struggles with
   extreme inputs, without explaining why the intervention should
   improve fault exposure. Programs differ in behaviour and execution
   cost, and more cases are not necessarily better. → the Mechanism and
   Domain-Validity Gate, shared definitions §9 (gate 12).

## Active research design

Before rejecting a promising candidate, attempt at least one meaningful
redesign (shared definitions §6). The levers, in order:
1. Narrow to the documented failure category.
2. Reuse code.
3. Reuse models, adapters, outputs or activations.
4. Cut optional scope.
5. Use a smaller intervention that keeps the mechanism.
6. Move to a better benchmark or setting.

Replace the direction only after these levers have been tried. Estimate
feasibility from verified requirements, not stacked pessimistic
assumptions. A speculative failure is a risk with a mitigation, not
guaranteed extra work.
