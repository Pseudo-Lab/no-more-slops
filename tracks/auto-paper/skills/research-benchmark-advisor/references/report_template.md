# Report Template (sections A-G)

Reproduce this structure exactly. Replace angle-bracket placeholders.
Every score carries a label: **Verified**, **Inferred**, or **Unverified**.
Every fact cites a source number from section G.

---

# Research Benchmark Advisor Report

**Mode:** <Broad Discovery | Focused Analysis: subfield>
**Date of analysis:** <YYYY-MM-DD>
**Effective researcher profile:** <one paragraph; overridden fields marked>
**Constraint overrides:** <none | list>
**Coverage:** <N categories browsed, M subfields visited, K benchmarks screened, S shortlisted>

## A. Executive Summary

<If applicable, first line verbatim: **"No candidate currently satisfies all hard constraints with sufficient evidence."**>

- Strongest research opportunities: <2-3 sentences>
- Most promising subfields: <list>
- HIGH-SOTA opportunities identified: <Yes: names | No>
- Most important feasibility limitations: <GPU, reproduction risk, protocol issues>
- Evidence shortfalls this run: <sources unreachable, leaderboards stale, etc.>

## B. Ranked Research Subfields

| Rank | Subfield | Beginner Accessibility | SOTA Opportunity | Four-Day Feasibility | Overall |
| ---- | -------- | ---------------------- | ---------------- | -------------------- | ------- |
| 1 | | Easy/Moderate/Hard | HIGH/MEDIUM/LOW/VERY LOW | Fits/Tight/Fails | score |

<One or two sentences per subfield explaining its rank.>

## C. Ranked Subfield-Benchmark Combinations

| Rank | Subfield | Benchmark | Current SOTA | SOTA Opportunity | Technical Depth | Feasibility |
| ---- | -------- | --------- | ------------ | ---------------- | --------------- | ----------- |
| 1 | | | <metric value, method, year> [Verified/Inferred/Unverified] [G#] | | | |

Rubric audit:

| Rank | C1 | C2 | C3 | C4 (SOTA) | C5 | C6 | C7 | C8 | C9 | C10 | Total /90 |
| ---- | -- | -- | -- | --------- | -- | -- | -- | -- | -- | --- | --------- |

<Mark any row that "beats baseline, not SOTA". For C10, note which
extension path applies: multi-agent (MA), multimodal/robotics (MM), both,
or none; either MA or MM alone satisfies the preference.>

## D. Detailed Analysis of Top Candidates

Repeat for each top candidate (all shortlisted survivors, or top three if
`brief`).

### D.<n> <Subfield> / <Benchmark>

#### 1. Research Area
<Beginner-friendly explanation of the subfield, 3-5 sentences.>

#### 2. Benchmark
<What it measures; dataset; splits; metric; protocol variants; license; download size.> [G#]

#### 3. Existing SOTA
| Rank | Method | Score | Year | Protocol | Code | Label |
| ---- | ------ | ----- | ---- | -------- | ---- | ----- |
| 1 | | | | | URL | Verified/Inferred/Unverified |
| 2 | | | | | | |
| 3 | | | | | | |

Strongest *comparable* baseline the researcher will run: <method> [G#]

#### 4. Leading Papers
For each of at least three papers: Title (Year, venue) - method - reported
performance and protocol - code (URL, last commit) - compute - key
contribution - limitations - role (leader / reproducible baseline /
conceptual). Source links. [G#]

#### 5. Technical Opportunity
<The specific weakness or gap, with the evidence location.> [G#]

#### 6. Proposed Research Direction
1. What existing methods do:
2. Their limitation:
3. Why it matters:
4. Proposed technical modification (mechanism):
5. Why it might improve performance:
6. Experiment that tests it (baseline, intervention, ablation, metric, seeds, test):

#### 7. Required Knowledge
<Concepts the researcher must understand; mark which are already in the profile.>

#### 8. Implementation Difficulty
| Dimension | Rating | Why |
| --- | --- | --- |
| Coding | Easy/Moderate/Hard | |
| Mathematics | Easy/Moderate/Hard | |
| Infrastructure | Easy/Moderate/Hard | |

H1 sub-items: understand task <E/M/H>; understand baseline <E/M/H>; implement improvement <E/M/H>; validate <E/M/H>.

#### 9. Four-Day Experimental Plan
Assumed hardware: <one GPU type, memory>.

| Day | Blocks | Hours |
| --- | --- | --- |
| 1 | setup, data, baseline reproduction | |
| 2 | baseline verified; method implementation | |
| 3 | main runs, ablation | |
| 4 | statistics, analysis, writing tables | |
| | Debugging contingency | |
| | **Total** | **<h> / about 32** |

#### 10. Risks
<Main reasons the project might fail: reproduction, protocol mismatch, variance, compute, understanding.>

Extensibility (optional): <multi-agent systems: one sentence or "none" | multimodal learning / robotics: one sentence or "none">. Either one satisfies the preference.

#### 11. SOTA Feasibility Verdict
```
SOTA Feasibility Verdict: <rating>
Headroom: ...
Weakness evidence: ...
Mechanism: ...
Baseline reproducibility: ...
Protocol matched: ...
Schedule fit: ...
Why not higher: ...
```

## E. Final Recommendations

| Pick | Combination | Why |
| --- | --- | --- |
| Best overall | | |
| Best beginner-friendly | | |
| Best chance of outperforming SOTA | | |
| Best match for research interests | | |
| Best for a technically strong four-page paper | | |

<These may be different combinations. If a pick is unavailable (e.g. no HIGH candidate), say so instead of forcing one.>

## F. Rejected Candidates

| Subfield | Benchmark | Reason category | One-line reason | Source |
| --- | --- | --- | --- | --- |

Reason categories: Saturated benchmark / Excessive compute / Insufficient
technical depth / Poor reproducibility / Unrealistic four-day schedule /
Unclear SOTA opportunity / Fails H1 / Protocol or data issues.

## G. Sources and Verification

Retrieval date for all entries: <YYYY-MM-DD> unless noted.

| G# | Type | Title / description | URL | Retrieved | Tier | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Task index | Papers with Code tasks | https://paperswithcode.co/tasks | | primary | |
| 2 | Leaderboard | | | | | |
| 3 | Paper | | | | | |
| 4 | Repository | | | | | last commit, eval script present |
| 5 | Dataset | | | | | license, size |
| 6 | Eval script | | | | | |

Unretrievable or stale sources: <list URLs and what was attempted>.

Types: Task index / Task page / Leaderboard / Paper / Repository / Dataset
/ Eval script / Reproduction report / Other. Tier: primary / official repo
/ Hugging Face / GitHub / paper / secondary index.
