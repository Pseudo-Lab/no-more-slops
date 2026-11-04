# SOTA Feasibility Assessment

This is the most important judgment the skill makes. A low leaderboard
score does **not** mean a benchmark is easy to improve. Separate two
concepts and report both:

- **Benchmark headroom:** distance between the top score and the metric's
  maximum (or human performance, if published).
- **Practical improvement opportunity:** whether a credible technical route
  exists to beat the strongest comparable method, given this researcher,
  four days, and one GPU.

A benchmark at 70 % may be far harder to improve than one at 95 %.

## The 10-point investigation (run for every shortlisted benchmark)

Answer each item with evidence and a label (Verified / Inferred /
Unverified).

1. **Current best reported performance.** Method, score, year, protocol.
2. **Second- and third-best methods.** Scores and the gaps between ranks 1,
   2 and 3. Tight clustering suggests many routes to a marginal gain; a
   large gap suggests one dominant idea that must be matched first.
3. **Recent improvement trend.** Score change over the last 1-3 years.
   Flat trends with active submissions signal difficulty; rapid gains
   signal an immature benchmark where new ideas still land.
4. **Strength of existing methods.** Are leaders large pretrained models,
   ensembles, or heavily tuned pipelines? Are they simple ideas that leave
   obvious extensions?
5. **Code and checkpoints.** Is the strongest comparable method runnable?
   Evidence of functionality (recent commits, closed reproduction issues,
   third-party reproduction, inclusion in a maintained harness)?
6. **Computational requirements.** GPU type, count, hours for the leader
   and for the comparable baseline the researcher will actually run.
7. **Protocol comparability.** Same split, metric, seeds, pre-training data,
   model-size class? List every protocol variant on the leaderboard and pick
   the one the researcher can match.
8. **Remaining technical weaknesses.** Documented failure modes (from
   ablations, error analyses, later papers, GitHub issues). Each with a
   source location.
9. **Can this researcher exploit them?** Does the fix require knowledge or
   engineering beyond the effective profile?
10. **Validation in four days.** Can the improvement be shown with
    statistical support (seeds, CIs, paired test) inside the schedule?

## Rating rubric

Assign exactly one rating per combination. Each condition must hold with
cited evidence; "sounds promising" never qualifies.

### HIGH
All of:
- A specific, evidence-supported technical weakness in the strongest
  comparable method (item 8 with a source).
- A plausible improvement method with a named mechanism (Step 5 proposal
  complete).
- The strongest comparable baseline can be reproduced or compared directly
  under the same protocol (items 5 and 7 Verified).
- Required experiments fit within four working days (Step 6 schedule under
  about 32 h including contingency).
- A credible path to outperforming the strongest comparable method, e.g. a
  published analogous gain of the mechanism on a related benchmark, or a
  measured error mode large enough that fixing a fraction of it would move
  the metric past the leader.

### MEDIUM
- A plausible improvement exists with a mechanism.
- Some uncertainty remains about performance, protocol comparability or
  implementation (one of items 5, 7, 8 is Inferred rather than Verified).
- Experiments appear feasible within four days.

### LOW
- Benchmark is accessible, but no credible path to beating the leader is
  identified; or the leaders are large, heavily tuned, or ensemble systems
  the researcher cannot match; or expected gains are within seed variance.

### VERY LOW
Any of: saturated (99-100 % or within noise of the maximum);
computationally prohibitive on one GPU; poorly reproducible (no code, no
protocol, no eval script); unsuitable for the researcher's level even with
AI assistance.

## Anti-inflation rules

- Do not assign HIGH because a mechanism sounds elegant. HIGH needs a
  sourced weakness **and** a reproducible baseline **and** a fitted
  schedule.
- Do not upgrade a MEDIUM because the researcher is interested in the area.
- Do not treat beating a reproducible baseline that is not the leader as a
  SOTA path; label such candidates "beats baseline, not SOTA" in section C.
- Do not present numeric win probabilities unless a published result
  quantifies the mechanism's effect on the same benchmark and protocol.
- If no combination reaches HIGH, say so in section A, first paragraph.

## Reporting format for the verdict (section D, item 11)

```
SOTA Feasibility Verdict: <HIGH | MEDIUM | LOW | VERY LOW>
Headroom: <top score> vs <max/human>; <N> points
Weakness evidence: <source, table/figure, one sentence>
Mechanism: <one sentence>
Baseline reproducibility: <Verified | Inferred | Unverified>, <evidence>
Protocol matched: <split / metric / model class>
Schedule fit: <hours> of about 32 h
Why not higher: <the missing condition, if any>
```
