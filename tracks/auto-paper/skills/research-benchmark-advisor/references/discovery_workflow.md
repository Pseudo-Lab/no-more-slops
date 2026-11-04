# Discovery Workflow (Steps 1-7, detailed)

Follow every step in order. Keep a running **evidence log** (URL, date,
what was read) that becomes section G of the report.

## Step 1 - Understand the researcher

Build the effective profile (see `researcher_profile.md`). Write a
five-line summary:

- Strengths (what the researcher can judge and implement unaided)
- Knowledge gaps (what must be learned or avoided)
- Compute constraints (assume one 48 GB GPU unless confirmed otherwise)
- Interests (ranked)
- Time limit and paper target

Ask the user a question only if an answer would change which candidates
survive the gates.

## Step 2 - Explore research subfields

1. Fetch the Papers with Code tasks index. List the top-level categories
   seen.
2. Choose at least five categories to open (Broad mode). At least two must
   lie outside the researcher's interests. In Focused mode open the named
   subfield plus one adjacent subfield if the named one yields fewer than
   three usable benchmarks.
3. For each category, list its subfields (tasks) with the number of
   benchmarks and papers shown, if displayed.
4. Pre-screen subfields on five quick signals:
   - Accessibility: can the task be explained in two sentences to a
     statistics graduate?
   - Benchmark availability: at least one public benchmark with a
     leaderboard.
   - Compute: do leading methods train on one GPU in under a day?
   - Technical opportunity: do recent papers disagree, show instability
     across seeds, or report failure modes?
   - SOTA potential: are top entries recent and close together, or is one
     method far ahead?
5. Keep 6-10 subfields for benchmark discovery (Broad mode).

Record all subfields visited, including rejected ones, with a one-line
reason.

## Step 3 - Discover benchmarks

For each kept subfield, open its task page and list benchmarks. Screen at
least ten benchmarks in total (Broad) or three (Focused). For each, fill
the screening table in `sources.md` section 4.

Exclude immediately (to section F) when any of these hold:
- Top score is 99-100 % with no justified alternative metric.
- Dataset not publicly downloadable, or license forbids research use.
- Splits undocumented and no community-standard split exists.
- Evaluation depends on a proprietary API with material cost, on live
  websites, or on extensive human evaluation.
- Leading methods need multi-GPU training measured in days.
- Scoring procedure cannot be reproduced from public artifacts.
- No leaderboard entry or paper newer than about 30 months and no sign of
  continued use (no citing papers in the last year).

Prefer benchmarks with: documented splits, public data, stable protocol,
public evaluation scripts, reproducible baselines, published leaderboard,
accessible implementations, manageable compute.

Keep several candidate benchmarks per subfield when possible. Shortlist
3-6 benchmarks overall (Broad) or 2-4 (Focused) for Steps 4-6.

## Step 4 - Analyze leading papers

For each shortlisted benchmark, identify **at least three** leading or
highly relevant papers. Include the leaderboard top-1 if it has a paper,
the strongest method with public code, and at least one method that is
simple enough for the researcher to understand fully.

Paper record (fill every row; write "not stated" rather than guessing):

| Field | Content |
| --- | --- |
| Title | exact |
| Year / venue | |
| Method | two-sentence description |
| Reported performance | metric, value, split; label Verified / Inferred / Unverified |
| Dataset and evaluation protocol | split, seeds, extra data, pre-training |
| Code availability | URL; last commit; eval script present?; checkpoints? |
| Computational requirements | GPU type, count, hours; or Inferred estimate |
| Key technical contribution | one sentence |
| Potential limitations | from the paper's own limitations section and from later papers that compare against it |

Label each paper as **leaderboard leader**, **strong reproducible
baseline**, or **conceptual reference**. Beating a reproducible baseline
that is not the leader is not SOTA; say so wherever it applies.

## Step 5 - Identify technical opportunities

Run the 10-point investigation in `sota_feasibility.md` for every
shortlisted benchmark. Then write **one** proposal per benchmark using
this six-part structure. Every part is mandatory.

1. **What existing methods do** (the strongest comparable method, in plain
   language).
2. **What their limitation is** (a specific weakness, with a source: a
   table, figure, ablation, or stated assumption).
3. **Why the limitation matters** (which inputs or conditions it hurts;
   how big the effect is, if measured).
4. **What technical modification could address it** (a loss term, an
   objective, a selection rule, a representation change, an architectural
   component, a principled combination). Name the mechanism.
5. **Why the modification might improve performance** (the causal story
   from mechanism to metric; cite any analogous published gain).
6. **What experiment would test the hypothesis** (baseline, intervention,
   ablation that removes the mechanism, metric, seeds, statistical test).

Reject proposals that fail H4 (see `scoring_rubric.md`) or that lack an
identifiable mechanism. Typical weakness families worth probing: poor
generalization under shift, inefficient optimization, label-noise
sensitivity, weak representations for a subpopulation, class or domain
imbalance, missing uncertainty modeling, unnecessary complexity, failure on
a specific input distribution, dependence on a tuned threshold that can be
replaced by a principled rule.

## Step 6 - Evaluate four-day feasibility

Estimate hours for each block, sum them, and compare with about 32 focused
hours. Include an explicit debugging contingency of at least 20 % of
implementation plus run time.

| Block | Typical range | Notes |
| --- | --- | --- |
| Environment setup | 1-4 h | conda/pip, CUDA, dependency pins |
| Dataset acquisition | 0.5-4 h | download size, preprocessing |
| Baseline verification | 2-8 h | must reproduce the strongest comparable baseline within tolerance |
| Method implementation | 3-8 h | with AI assistance; the researcher must be able to review it |
| Experiment execution | 2-12 h wall-clock | GPU time; can overlap with writing |
| Ablation | 1-4 h | at least one |
| Statistical evaluation | 1-2 h | seeds, CIs, paired tests |
| Result analysis | 2-4 h | tables, figures |
| Debugging contingency | 20 % or more | reproduction failures are the norm |

Produce a day-by-day plan (Day 1-4) with the hour estimates. If the total
exceeds about 32 h after one honest scoping pass (smaller model, fewer
seeds, a subset split that the benchmark itself defines), reject the
candidate for H2 and record it in section F.

Never assume unlimited or multi-GPU availability. Say which single GPU the
plan assumes.

## Step 7 - Rank candidates

Apply `scoring_rubric.md`:

1. Gate every candidate on H1-H4 and the saturation rule. Gated-out
   candidates go to section F with the failing gate named.
2. Score survivors on the weighted criteria.
3. **Ranking A (subfields):** rank each subfield by its *best surviving
   combination's* score, not by popularity or paper count.
4. **Ranking B (combinations):** rank by SOTA improvement potential first,
   then the remaining criteria in the rubric's order.
5. Assign the SOTA Opportunity rating to every combination in Ranking B.
6. If no combination is HIGH, write that sentence verbatim in section A.

Then produce the report per `report_template.md`.
