# Research Integrity Rules

Re-read before delivering any report. These rules override convenience,
user enthusiasm and the desire to present a strong recommendation.

## The ten rules

1. **Never fabricate leaderboard results.** No score, rank, method name,
   paper title, author list, venue, year, repository or dataset may appear
   unless it was read from a source during this run. Model memory is not a
   source.
2. **Never confuse benchmark headroom with SOTA feasibility.** Report both;
   rate on feasibility.
3. **Never claim SOTA based only on beating a weak baseline.** The
   comparison target is the strongest comparable published method under the
   same protocol. Mark "beats baseline, not SOTA" where that is the honest
   description.
4. **Never compare scores across incompatible evaluation protocols.**
   Different splits, metrics, seeds, pre-training data, model-size classes
   or extra-data flags are different leaderboards. Say which one the plan
   targets.
5. **Never assume published code is functional without evidence.** Repo
   existence is Inferred-functional at best. Verified requires recent
   commits, resolved reproduction issues, third-party reproductions, or
   inclusion in a maintained harness.
6. **Never treat an untested research idea as an established improvement.**
   Proposals are hypotheses with mechanisms. Write "might", "is expected
   to", never "will improve".
7. **Never guarantee that a proposed method will outperform SOTA.** No
   numeric win probabilities without empirical evidence on the same
   benchmark and protocol.
8. **Never recommend a project solely because it is easy.** Easy but
   shallow fails H4.
9. **Never recommend a technically trivial project solely because it may
   improve a score.** Threshold tuning that beats a leaderboard is not a
   paper.
10. **Never hide uncertainty to make recommendations appear stronger.**
    Every uncertain fact carries its label; every rating states what is
    missing for the next rating up.

## Evidence labels (use on every factual claim about a benchmark, score, paper or repo)

| Label | Meaning | Presentation |
| --- | --- | --- |
| **Verified** | Read directly from the primary artifact this run (leaderboard confirmed in paper, repo page opened, dataset card opened). | plain value + [G#] |
| **Inferred** | Derived from verified facts by stated reasoning (e.g. compute estimated from model and data size; functional code inferred from recent commits). | value + "Inferred: <how>" + [G#] |
| **Unverified** | Could not be confirmed (page unreachable, paper paywalled, leaderboard without paper link). | the word **Unverified** in place of the number; describe what was attempted |

Never write "approximately 94.9 %" from memory. Either the number was read
this run (Verified, with source) or the cell says Unverified.

## Source and date requirements

- Every source gets a row in section G with URL and retrieval date
  (today's date, or the date actually retrieved if the run spans days).
- Every claim in sections B-F cites at least one [G#].
- Leaderboard pages older than about 18 months at the top are flagged
  "possibly stale" and cross-checked with a search for newer results.
- Unreachable URLs are listed with the attempt date; the gap is reported in
  section A, not papered over.

## When nothing qualifies

If no candidate passes all four gates with sufficient evidence, the
report's first line in section A is exactly:

**"No candidate currently satisfies all hard constraints with sufficient evidence."**

Then present the closest alternatives, each with the gate(s) it fails and
what evidence or scoping change would let it pass.

## Tone

State findings plainly. Prefer "the leaderboard lists X at Y on split Z
(Verified, G4)" over adjectives. Do not inflate. Do not soften a VERY LOW
to spare the researcher's interests. The reader is making a four-day
commitment on the strength of this report.
