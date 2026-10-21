# Scoring Rubric: Gates, Criteria and Rankings

Hard constraints are **gates**: a candidate failing any one is removed
before scoring, whatever its other merits. Weighted criteria order the
survivors.

## Part 1 - Gates (pass / fail, evidence required)

### H1 Beginner accessibility (Mandatory)
Rate each sub-item Easy / Moderate / Hard for the effective profile, with
one sentence each:
1. Understanding the task
2. Understanding the strongest comparable baseline
3. Implementing the proposed improvement
4. Validating the improvement (metrics, statistics, pitfalls)

Also note: required math, required ML/DL knowledge, complexity of existing
methods, difficulty of interpreting results, implementation complexity.

**Fail** when any sub-item is Hard, or when two or more are Moderate *and*
the baseline's correctness depends on theory the researcher cannot check.
"AI can generate the code" never converts Hard to Moderate: H1 is about
understanding and judging, not typing.

### H2 Four-day feasibility (Mandatory)
Use the Step 6 schedule. **Fail** when the total exceeds about 32 focused
hours after one honest scoping pass, when the plan needs more than one
GPU without confirmed access, when baseline reproduction has a documented
history of failure, or when any single run exceeds about 12 h wall-clock
without a cheaper defined variant.

### H3 Four-page paper feasibility (Mandatory)
**Pass** only if all of these can be written from the planned experiments:
one clear research question; one meaningful technical contribution; a
reproducible setup; comparison with the strongest comparable baseline and
at least one more; at least one ablation; quantitative results with
uncertainty; a defensible conclusion even if the result is negative.
**Fail** when the contribution needs a large framework, a new benchmark,
or many experimental axes to be convincing.

### H4 Technical depth (Mandatory)
**Pass** when the contribution is one of: new loss function; novel
optimization objective; principled data-selection algorithm; new
representation-learning approach; mathematically motivated training
method; new architectural component; theoretically motivated combination
of existing methods; a new analysis technique that yields a measurable
intervention.
**Fail** when the contribution is only: threshold tuning; majority voting
or plain ensembling; trivial prompt modifications; arbitrary heuristic
combinations; cosmetic changes; unprincipled hyperparameter search.

### Saturation gate
**Fail** when the top score is 99-100 % (or within seed noise of the
maximum) unless a justified alternative metric on the same benchmark has
substantial headroom and published results exist for it.

## Part 2 - Weighted criteria (survivors only)

Score each 0-5 with a one-line justification. Weights reflect the stated
priorities.

| # | Criterion | Priority | Weight |
| --- | --- | --- | --- |
| 1 | Beginner accessibility (degree, beyond the gate) | Mandatory gate + | 2 |
| 2 | Four-day feasibility (margin under 32 h) | Mandatory gate + | 2 |
| 3 | Four-page paper suitability | Mandatory gate + | 1 |
| 4 | **Probability of surpassing existing SOTA** | **Highest** | **4** |
| 5 | Technical depth (degree) | Mandatory gate + | 2 |
| 6 | Fit with statistics / CS / ML background | Important | 2 |
| 7 | Alignment with research interests | Important | 1.5 |
| 8 | Reproducible public benchmark quality | Important | 2 |
| 9 | Opportunity for GPU experiments | Optional | 0.5 |
| 10 | Extensibility: to multi-agent systems **or** to multimodal learning / robotics | Preferred (optional) | 1 |

Criterion 4 scoring anchors (map from the SOTA rating):
HIGH = 5, MEDIUM = 3, LOW = 1, VERY LOW = 0 (VERY LOW is normally gated
out already).

Criterion 10 scoring anchors: the preference is satisfied by **either**
(a) extensibility to multi-agent systems or (b) extensibility to
multimodal learning or robotics; a candidate need not satisfy both.
Score 5 when a concrete extension path exists for at least one of the two
(name it in one sentence); 2-3 when an extension is plausible but not
concrete; 0 when neither applies. Satisfying both earns no extra credit
beyond 5. This criterion never gates a candidate and never outranks
criteria 1-8.

Total = sum(weight x score); maximum 90. Report the total and the
criterion-4 score separately so the reader can see the SOTA driver.

## Part 3 - Ranking A (research subfields)

Rank each explored subfield by the **best surviving combination's total
score**, not by popularity, paper count, or interest alignment. Subfields
with no surviving combination rank below all others and show "no gated
candidate". Give one sentence per subfield explaining its position.

Table columns: Rank | Subfield | Beginner Accessibility | SOTA Opportunity
| Four-Day Feasibility | Overall.

## Part 4 - Ranking B (subfield-benchmark combinations)

Order by, in sequence:
1. SOTA improvement potential (rating, then criterion-4 evidence quality)
2. Satisfaction margin on the hard constraints
3. Reproducibility (criterion 8)
4. Technical depth (criterion 5)
5. Compatibility with researcher background (criterion 6)
6. Research interest alignment (criterion 7)
7. Computational feasibility (margin and GPU need)
8. Extensibility (criterion 10: multi-agent systems or multimodal/robotics, either suffices)

Ties within a step are broken by the next step. Table columns: Rank |
Subfield | Benchmark | Current SOTA (with label) | SOTA Opportunity |
Technical Depth | Feasibility.

## Part 5 - Transparency

Show the rubric scores for every ranked combination in a compact table in
section C (or an appendix to section C), so the ranking can be audited.
Never present numeric SOTA probabilities; present the rating and its
evidence.
