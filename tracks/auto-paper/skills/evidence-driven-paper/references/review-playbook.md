# Review playbook

Use the sections relevant to the actual claim. These lessons come from iterative
review of a short empirical calibration paper; they are not universal demands
for all research. No private manuscript, result, or reviewer identity is bundled.

## A compact evidence ledger

Use one row per claim; a small Markdown table is enough.

| Claim | Comparison / population | Evidence and uncertainty | Status / boundary |
| --- | --- | --- | --- |
| Candidate improves score | Candidate vs Baseline; named dataset roster; lower is better | Result path and paired keys; absolute and relative effect; interval method and independent unit | Prespecified or post hoc; practical value still untested |
| Sharing causes the improvement | Same function family, penalties tuned independently with equal opportunity | Matched control outputs, not just an additive ablation | Supported, unresolved, or contradicted |
| Numerical ranking is resolved | Same objective or named comparator; fixed diagnostic subset | Observed gap and both error bounds | Conditional assumptions; subset does not explain the entire benchmark |

Replace example entries with actual evidence. “Unresolved” is a useful result.
A filled ledger is not evidence that its contents are correct.

## Controls that answer different questions

An added shared term can sometimes be absorbed into existing coefficients.
Check the represented function family before attributing an improvement to
expressiveness. If the family is unchanged, derive the induced regularizer and
compare against an appropriate same-family control.

A frozen-hyperparameter ablation measures removal under one setting. An
independently tuned ablation measures the competing procedure after selection.
Report which question each answers. Equal numbers of candidates alone do not
ensure fairness: also describe candidate ranges, split, selection metric,
optimizer budget, and data used to design those choices.

A same-objective reparameterization is a useful numerical control when the
reported effects are near solver tolerances. It does not replace a different-
regularizer control. Projection, parameter count, and sharing need not each
deserve a new experiment unless they support a central claim.

## Interpret uncertainty and magnitude separately

- A significant estimate and a nonsignificant estimate are not evidence that
  the two effects differ. Estimate their paired difference directly when the
  claim concerns a change in effect.
- Failure to detect an advantage is not equivalence or proof of no effect.
  Equivalence needs a justified margin and a suitable analysis.
- A small confidence interval can support a small effect without establishing
  practical utility. Report the scale, baseline, relative change when meaningful,
  and relevant training/inference costs.
- Resample independent units. Models, calibration splits, and seeds belonging
  to the same dataset need not be independent datasets. State the unit, number
  of independent groups, weighting, and sensitivity to dependencies.
- Brier or log-loss improvement alone does not isolate calibration quality.
  Use appropriate calibration diagnostics when making a calibration claim.
- Declare pointwise versus simultaneous intervals, selection among analyses,
  and post hoc analyses. A local timestamp or frozen file is not independent
  preregistration.

Do not add confidence intervals mechanically to a comparison from the bundled
harness: it has no model of the experiment's sampling hierarchy.

## Turn a mechanism into a testable prediction

State what an equation changes, the assumptions that link it to risk, and what
could falsify that prediction. Separate parameter shrinkage from predictive
performance; a surrogate-risk calculation may not survive a nonlinear link.

For controlled experiments, document the generator, sampled labels, fitting
and selection data, and evaluation targets. If oracle probabilities are used,
keep them out of fitting/selection unless an explicitly named oracle comparison
is intended. Stratify effects by the variables central to the prediction.
Disclose when changing one variable also changes sample size or difficulty.

Averaging across class counts, generators, or signal types can hide reversals.
A mean coefficient of zero does not by itself eliminate common behavior in
nonlinear predictions. Plausible interactions are hypotheses until separated
by intervention; describe an unexplained residual benefit as such.

## Numerical and formal verification boundaries

For a same-objective control, compare objective values, residuals, predictions,
and the reported evaluation metric after adequate refinement. Agreement between
two implementations alone does not prove proximity to the optimum.

If using error bounds, a signed gap is certified only when its comparison
interval excludes zero. An unresolved sign can reflect a conservative bound;
it does not mean a wrong ranking. Report the size of actual reversals and their
effect on the research conclusion. A tiny sign change is not automatically an
important model-selection failure.

Say which models a maximum bound aggregates over, and report exceptions instead
of mixing their populations. A float-computed bound is not an interval-arithmetic
rounding certificate.

When formal verification is requested or useful, distinguish:
1. Definitions, assumptions, and algebra checked by the prover.
2. Analytic inequalities supplied as hypotheses versus proved from definitions.
3. Numerical implementation, floating-point arithmetic, data, statistics, and
   empirical claims outside the formalization.

Rebuild the actual proof source with pinned versions if claiming execution.
Check admitted proofs and unexpected axioms. Count auxiliary lemmas honestly;
a theorem count is not a count of research contributions. Hashes and execution
logs establish provenance relative to saved files, not independent replication.
