# Which route a protocol change allows

Each route is valid only under its conditions. When a condition fails, take the
next, more expensive route; never approximate a route that does not hold.

## Exact recomputation (no requests)

**Smaller limit.** Valid for methods that stop at the first passing attempt and
never show the limit to a model: the run with limit `r` is the first `r + 1`
attempts of the run with any larger limit. Recompute time and cost from the kept
attempts only. Methods that always use every attempt (e.g. a fixed number of
self-review rounds) cannot be cut: their last round is told to finish.

**Final-answer rule.** When no attempt passes, the loop still ran every attempt;
only the returned proposal differs (last, first, abstain). Same requests, same
cost and time. Recompute every metric that reads "the final proposal": a summary
that takes `trace[-1]` silently reports the last attempt. Methods without a gate
(direct, fixed-round self-review) keep their own final proposal.

**Aggregates.** Means over runs, per-category tables, paired differences and
cuts of a continued run need only the records. Fix the example order before a
seeded bootstrap so the interval does not depend on file order.

## Continuation (requests only past the old limit)

Valid when no model sees the limit, nothing executes before the loop ends, and
the code, data, models, prompts and prices equal the source run's. Replay each
saved prefix through the same pipeline and assert that every replayed request
matches the record before sending a new one; then the result is exactly what an
uninterrupted run with the larger limit would have produced. Rows that passed
within the old limit stay as they are.

Traps: a prompt that mentions "attempt k of r", a history format that depends on
`r`, retries that resample, or a changed code hash. An API route may change (for
example a gateway stops serving a model) only if the model and questions stay the
same and the manifest records the route from each attempt on.

## Partial rerun from the shared first proposal

Needed when a model sees the changed setting: a verifier threshold quoted in the
feedback, a different feedback text, latest-only versus cumulative history, a new
system prompt. Keep each example's recorded first proposal (Direct rows are
copied, not regenerated), verify it again under the new setting, and generate the
rest. Every new row then pairs with the source rows of the same example.

Re-verification is itself a sample when the verifier is stochastic. Measure on
the reruns: the share of first proposals with identical scores, the spread of
score differences and the share of flipped verdicts.

## New run

More runs, another sample or another generator need new first proposals. Check
that each later run actually generated its own (digest of the first proposals
differs from run 1) and that everything else equals run 1. Report the mean and
spread across runs; average each example over runs before resampling examples.

## Choosing after seeing results

Reruns at several thresholds or a rule comparison on the evaluation examples are
post hoc selection. Keep all variants, report the chosen one as chosen after
seeing these examples, show the alternatives (a small table with paired
intervals is enough), and do not describe the choice as tuned on held-out data.
