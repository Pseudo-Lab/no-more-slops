# Week 2 case: Jev-Backed Function Calling

The study compared seven function-calling methods on 3,051 BFCL examples with
`gpt-5-nano` (and Direct and JBFC with `gpt-5.4-mini`): a generator proposes a
call, a verifier (Jev) checks it, and rejected calls are repaired with feedback.
The protocol changed several times after the first runs. Each change used the
cheapest valid route; costs are at list prices with eight workers.

| Change | Route | New requests | Time, cost |
| --- | --- | --- | --- |
| Repair limit 2 → 10 for the limit curve | Continuation (r=2 → 7 → 10); the verifier route changed at attempt 8 and was recorded | Rows that reached each limit | ≈30 min, $1.4 |
| Paper limit 2 → 3 | Exact cut of the r=10 continuation for JBFC; continuation of the other stop-at-pass methods; every fixed-round self-review row continued; JBFC added to the larger generator's Direct run from its first proposals | Rows at the old limit, plus the new arm | 26 min, $3.6 (both generators) |
| One run → three runs per generator | New runs (new first proposals), JBFC added from each run's first proposals | All rows of runs 2–3 | 47 min, $12 |
| Threshold 0.8 → 0.7 and 0.5 (stated in the feedback) | Partial reruns from each run's shared first proposals | Re-verification of every first proposal, regeneration after a rejection | 35 min, $8.7 (0.7); ≈28 min, $5.4 (0.5) |
| The other verifier methods and the limit curve at 0.5 | Partial reruns from the first run's first proposals; JBFC at 0.5 continued from r=3 to r=10 | Re-verification and regeneration; 476 rows continued | 32 min, $1.7 |
| Return the first instead of the last proposal when none passes | Exact, on the same trajectories (tables, figure and a comparison table) | None | none |

Checks that caught or ruled out problems:

- The 0.5 rerun stopped when the verifier returned HTTP 402 (billing). 759 rows
  were saved; after payment, resuming with the same route sent only the
  remaining 2,292. Resuming with another route would have changed the run's
  fingerprint and been refused.
- Re-verifying identical first proposals gave identical scores for only 34–37%
  of them; the 95th percentile of the score difference was 0.03 and about 1% of
  verdicts flipped. Small differences between reruns are partly the verifier's.
- A summary function read the last attempt as final. With the first-proposal
  rule it had to read the chosen attempt instead.
- The r=3 cut of the r=10 continuation reproduced every source row, and the
  figure's r=3 point equalled the table's JBFC cell.

What the rule comparison showed (mean of three runs, paired differences with
95% intervals): with `gpt-5.4-mini`, returning the last proposal made
unverified changes that fixed 10–14 calls per run and broke 53–55, so returning
the first proposal gained 1.37 points (0.93 to 1.82) and turned a loss against
Direct into a gain. With `gpt-5-nano` it cost 0.35 points (−0.68 to −0.03).
Both were reported, with the choice described as made after seeing these
examples.

`scripts/reuse_runs.py` reproduces the study's paired JBFC − Direct differences
from the raw records (`gpt-5-nano` +10.65, `gpt-5.4-mini` +0.96 points, same
intervals), confirms that all 3,051 first proposals are shared between a rerun
and its source, and confirms that the r=10 continuation reproduces the r=3 run.
