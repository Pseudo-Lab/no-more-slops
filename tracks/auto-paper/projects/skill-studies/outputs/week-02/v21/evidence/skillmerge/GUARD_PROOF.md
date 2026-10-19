# Reference-blind prefix guard: exact conditional boundary

This is a new mathematical and finite-computation follow-up on the exposed bank. It is not an executable-skill experiment or a novelty claim about all safe composition methods.

## Objects and quantified statement

Fix ordered inputs A/B and cap k. Write X=set(V_k), Y=set(P_k); both have min(k,|A union B|) IDs. References form an arbitrary finite nonempty family of nonempty alternatives. The conditional class consists of families with at least one complete alternative inside A and at least one inside B, possibly different alternatives. This is annotation sufficiency of the two complete inputs, not a held-out Q gate, not the sufficiency of truncated inputs, and not semantic correctness of skills.

The policy reads A/B/k only. Its guard is G=(X=Y) or (set(A) subset Y) or (set(B) subset Y). It emits P_k on true and V_k otherwise. Gold is used only after construction for scoring and descriptive strata.

## Necessity and sufficiency

If X=Y, all containment scores coincide. If A is entirely in Y, the alternative witnessed in A is in Y; similarly for B. Thus G implies no baseline-success-to-promoted-failure transition for every conditionally admissible family. No-loss is weaker than success: X=Y can leave both outputs insufficient.

Conversely suppose G is false. Equal cardinality and X!=Y imply some x in X minus Y. Neither A nor B is entirely in Y, so choose an ID outside Y in each input. If x belongs to A, choose the A alternative {x}; otherwise choose {a_out}. If x belongs to B, choose its alternative {x}; otherwise choose {b_out}. At most two singleton alternatives result. Each complete input contains one, X completes {x}, and Y contains neither singleton. This family is a conditional loss countercertificate. Therefore G is necessary and sufficient for universal conditional containment no-loss. References outside the union and additional alternatives do not invalidate the forward proof; a two-alternative subfamily suffices for the reverse witness.

The theorem actually concerns any two equal-size output subsets of the same union; stable promotion supplies the concrete pair being tested. Without equal sizes, replace X=Y with X subset Y in this characterization. Empty-input cases make the conditional family class empty; for the current stable constructor an empty input also makes the two orders identical. No claim of a nonempty qualified population is created by this vacuous endpoint.

## Maximality is restricted

For a fixed A/B/k, a P-or-V switch that promises no-loss for every conditionally admissible reference family must fall back when G is false. Otherwise the reverse singleton family refutes it. G is maximal within that binary switch class and reference quantification, not a best policy for actual known annotations, arbitrary new outputs, semantic quality, token cost, or real skill deployment. A conservative false guard can discard a gain on the actual family, as the saved bank demonstrates.

## General input-length corollary and sharpness

Suppose each input length is at most d>=2. If the common set is empty, stable partition changes nothing. If at least two IDs are common, union size is at most 2d-2, so cap k>=2d-2 retains the union. If exactly one ID is common, union size is at most 2d-1, and at k>=2d-2 at most one noncommon ID is omitted. That ID belongs to only one input, so the other input is fully retained. In every case the structural guard is true. Conditional no-loss follows. For d=0 or1, the nonnegative-cap endpoints are treated directly; no negative cap is introduced.

The worst-case bound is sharp for each d>=2. Put d-1 private IDs in A and d-1 different private IDs in B, followed by the same common ID. RR alternates private IDs then ends with the common ID. At cap 2d-3 it contains A's last private ID but P, which promotes the common ID, omits both last private IDs. Choose the two last private singleton IDs as alternatives: both complete inputs are sufficient, RR passes, promotion fails, and G is false. At the next cap G is true. Code checks d=2..8 as authored illustrations; the argument, rather than those seven examples, establishes the general statement. The previous length-three/cap-four boundary is the d=3 special case.

## Why unconditional safety fails

The smallest authored failure under the declared finite ordering has two union IDs, total input length three, and cap one: A=(0,1), B=(1), reference family={{0}}. RR outputs (0); promotion and guard output (1), since all of B is retained. A is sufficient and B is not. G is true but the prerequisite for conditional safety is false. This is not a failure of the conditional theorem and not a new natural skill observation. The actual all-pair bank retains487 cap-one losses for the guarded policy.

## Endpoint and cost boundaries

At cap>=4 the guard may preserve full containment while first-three still ignores needed later IDs. Exact matching can also penalize a sufficient superset. These endpoints get separate raw rows and gains/losses, without inheriting the theorem. Cap counts IDs; measured token/call cost and qualified behavioral effects remain null. The same-author alternate verifier is not an independent scientific replication.

## Frozen computation

Canonical run: runs/research_advancement_v21_20261019_01/skillmerge/analysis_01. PLAN, both code files and six consumed sources are fixed before output generation in input_lock.json. Seven raw pair files each fit the8MB text limit. The alternate verifier reconstructs159,558 pair-capacity rows, exact aggregation and bitmask certificates, and rejects separately altered copies of one input and one output. The original run and earlier v19/v20 sources are not changed.
