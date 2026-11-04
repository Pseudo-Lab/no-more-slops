---
name: research-benchmark-advisor
description: Research subfield, public benchmark and SOTA-method advisor for beginner researchers. Browses Papers with Code task categories (with fallbacks to official benchmark repos, Hugging Face leaderboards, GitHub and original papers), retrieves current leaderboards and leading papers, verifies code, data and evaluation-script availability, and ranks subfield-benchmark combinations by the realistic chance of outperforming the strongest comparable published baseline within four working days, under hard gates for beginner accessibility, four-day feasibility, four-page-paper fit and technical depth. Broad Discovery Mode (default) explores many subfields; Focused Analysis Mode analyzes one named subfield. Never fabricates scores or papers; labels every claim Verified / Inferred / Unverified with source links and retrieval dates. Usage - /research-benchmark-advisor [free-text focus or instructions] [profile: <field>=<value>; ...]
---

# Research Benchmark Advisor

Find research directions where a relatively inexperienced researcher has a
realistic chance to **outperform the strongest comparable published baseline
within four working days**, and write them up as a four-page workshop paper.

This skill does **actual research** with live web evidence. It is not a
brainstorming prompt. Every leaderboard number, paper title and code claim
in the report must trace to a source retrieved during this run.

This skill is global and project-independent. It never needs the current
repository and must not read or modify project files except to save its own
report (see section 7).

## 0. Reference files (read before starting)

All in this skill's `references/` directory:

| File | Use it for |
| --- | --- |
| `researcher_profile.md` | Default researcher profile and the override syntax |
| `sources.md` | Primary source (Papers with Code tasks), fallback chain, category list to browse, tool guidance |
| `discovery_workflow.md` | Detailed Steps 1-7: browsing, benchmark screening, paper analysis, opportunity design, scheduling |
| `sota_feasibility.md` | The 10-point SOTA investigation and the HIGH / MEDIUM / LOW / VERY LOW rubric |
| `scoring_rubric.md` | Hard gates (H1-H4), weighted criteria, Ranking A and Ranking B procedure |
| `report_template.md` | Required output sections A-G with exact tables |
| `integrity_rules.md` | The 10 research-integrity rules, evidence labels, source and date requirements |

Read `researcher_profile.md`, `sources.md` and `integrity_rules.md` in full
at the start of every run. Read the others when the workflow reaches them.

## 1. Invocation and argument parsing

Arguments: `$ARGUMENTS`

Parse the arguments in this order.

1. **Profile overrides.** Any segment of the form
   `profile: field=value; field=value` (or a path to a markdown/YAML profile
   file) overrides the matching fields of the default profile in
   `researcher_profile.md`. Unlisted fields keep their defaults. Report the
   effective profile in section A of the report.
2. **Mode detection.**
   - **Focused Analysis Mode** when the arguments name one subfield or
     benchmark family ("Focus on data-centric AI", "Compare anomaly detection
     benchmarks", "Analyze OOD detection", a benchmark name).
   - **Broad Discovery Mode** otherwise (empty arguments, or goal-style text
     such as "Find the best beginner-friendly SOTA opportunity within four
     days"). **Default to Broad Discovery Mode.**
3. **Constraint overrides.** Phrases like "six days", "eight-page", "CPU
   only", "no GPU", "must involve LLMs" replace the corresponding default
   constraint. Record every override explicitly in section A.
4. **Output options.** `nosave` suppresses writing the report file
   (section 7). `brief` limits section D to the top three candidates.

Ask a clarifying question **only** when a missing fact would materially
change the recommendation (for example, the user forbids GPU use but names a
GPU-only subfield). Otherwise state the assumption in section A and proceed.

## 2. Tools and evidence gathering

Use the web tools available in the session. Preferred order:

1. `WebFetch` on the exact page (task page, benchmark leaderboard page,
   arXiv abstract, GitHub repo, Hugging Face dataset or Space).
2. `WebSearch` to locate pages, recent papers, and third-party
   reproductions. Use "extended" mode for leaderboard-specific or recent
   queries if the standard mode returns thin results.
3. Browser tools (built-in browser or Claude in Chrome) when a leaderboard
   renders client-side and `WebFetch` returns no table. Prefer
   `get_page_text` / `read_page` over screenshots.

If a tool is deferred, load it first with `ToolSearch`
(e.g. `select:WebFetch,WebSearch`). If no web tool is available at all,
stop and tell the user the skill cannot run without live evidence; do not
produce a report from memory.

Record for every retrieved fact: URL, retrieval date (today), and what was
read there. Model memory is **never** an acceptable source for a score, a
rank, a paper's existence, or a repo's existence. Memory may only suggest
where to look.

## 3. Hard constraints (gates, never traded off)

Full definitions in `scoring_rubric.md` and `sota_feasibility.md`.

- **H1 Beginner accessibility.** Evaluate separately: understanding the
  task, understanding the baseline, implementing an improvement, validating
  it. "AI can write the code" does not satisfy H1.
- **H2 Four-day feasibility.** Setup, data, baseline verification, method,
  runs, ablation, statistics, analysis, debugging contingency; realistic GPU
  availability, never assumed unlimited.
- **H3 Four-page paper feasibility.** One clear RQ, one meaningful technical
  contribution, reproducible setup, strong baselines, at least one ablation,
  quantitative results, defensible conclusion.
- **H4 Technical depth.** New loss / objective / data-selection algorithm /
  representation / architecture component / principled combination.
  Reject: threshold tuning, majority voting, trivial prompt edits, arbitrary
  heuristic stacking, cosmetic changes, unprincipled hyperparameter search.

Also gate out any benchmark whose current best score is **99-100 %** unless a
justified alternative metric has substantial headroom.

**Extensibility (Preferred, optional, criterion 10).** Satisfied by
*either* extensibility to multi-agent systems *or* extensibility to
multimodal learning / robotics. One is sufficient; it is a tie-breaker,
never a gate.

## 4. Workflow (summary; details in `discovery_workflow.md`)

**Step 1 - Understand the researcher.** Build the effective profile.
List strengths, gaps, compute constraints, interests, time limit.

**Step 2 - Explore subfields.** Open `https://paperswithcode.co/tasks`.
Browse **at least five distinct top-level categories** in Broad mode, not
only the researcher's interest areas; record every subfield visited.
Apply the fallback chain in `sources.md` if the site is down or stale.

**Step 3 - Discover benchmarks.** Screen **at least ten benchmarks** across
the explored subfields (Broad mode) or **at least three** within the named
subfield (Focused mode). For each: leaderboard retrieved?, top methods,
metric, last-update recency, dataset and eval-script availability,
saturation check. Drop saturated or impractical ones with a one-line reason
(they go to section F).

**Step 4 - Analyze leading papers.** For each shortlisted benchmark
(target 3-6 shortlisted in Broad mode), identify at least three leading or
highly relevant papers and fill the paper record in
`discovery_workflow.md` (title, year, method, reported score, protocol,
code, compute, contribution, limitations). Separate *leaderboard leaders*
from *strong reproducible baselines*.

**Step 5 - Identify technical opportunities.** For each shortlisted
benchmark, run the 10-point SOTA investigation in `sota_feasibility.md` and
write one proposal using the six-part structure (what methods do, their
limitation, why it matters, the modification, why it should help, the
test). No proposal without an identifiable mechanism.

**Step 6 - Four-day feasibility.** Produce a day-by-day schedule with
hour estimates and a debugging contingency. Reject anything that does not
fit after one honest scoping pass.

**Step 7 - Rank.** Apply gates first, then the weighted rubric in
`scoring_rubric.md`. Produce Ranking A (subfields) and Ranking B
(subfield-benchmark combinations). Assign a SOTA Opportunity rating
(HIGH / MEDIUM / LOW / VERY LOW) to each surviving combination. **If no
HIGH exists, say so plainly.**

## 5. SOTA feasibility: the central judgment

Headroom (distance from the metric's maximum) is **not** opportunity.
Opportunity requires a *specific, evidenced weakness* in the strongest
comparable method, a *mechanism* that addresses it, a *reproducible or
directly comparable* baseline, and *experiments that fit in four days*.

A combination earns HIGH only when all of those are documented with
sources. When evidence is partial, it is MEDIUM at best. When the credible
path is unclear, LOW. Saturated, prohibitively expensive, irreproducible
or far beyond the researcher's level: VERY LOW. Never round up.

Never present a numeric probability of beating SOTA unless there is
empirical evidence (e.g. a published ablation showing the mechanism's gain
on the same benchmark and protocol).

## 6. Output

Produce the report exactly in the structure of `report_template.md`:

A. Executive Summary / B. Ranked Research Subfields / C. Ranked
Subfield-Benchmark Combinations / D. Detailed Analysis of Top Candidates
(11 subsections each) / E. Final Recommendations (five named picks) /
F. Rejected Candidates / G. Sources and Verification.

Every SOTA score in sections C and D carries one of three labels:
**Verified** (read on a leaderboard or in the paper this run),
**Inferred** (derived from verified facts; say how),
**Unverified** (could not be confirmed; shown as "Unverified", never as a
number presented as fact).

If no candidate passes all four gates with sufficient evidence, the first
line of section A must be exactly:

> **"No candidate currently satisfies all hard constraints with sufficient evidence."**

followed by the closest alternatives and the gate(s) each fails.

## 7. Saving the report

Print the full report in the response. Unless `nosave` is given, also
write it to the current working directory as
`research_benchmark_advisor_<YYYY-MM-DD>[_<slug>].md`, where `<slug>` is
a short lowercase tag of the focus (Focused mode only). Do not write any
other file. If the working directory is not writable or the user's project
rules forbid new files there, print the report only and say so.

## 8. Minimum breadth and effort

| Mode | Categories browsed | Benchmarks screened | Shortlisted for section D | Papers per shortlisted benchmark |
| --- | --- | --- | --- | --- |
| Broad Discovery | 5 or more | 10 or more | 3-6 | 3 or more |
| Focused Analysis | the named one (plus adjacent if thin) | 3 or more | 2-4 | 3 or more |

If a source is unreachable and the fallback chain yields fewer items than
the minimum, report the shortfall in sections A and G rather than padding
with unverified entries.

## 9. Pre-delivery checklist

Before printing the report confirm each item; fix or label anything that
fails.

- [ ] Every score, rank, paper and repo in sections B-F has a URL in
      section G with today's retrieval date.
- [ ] No score is quoted across incompatible protocols (different split,
      metric, model size class, or extra training data) without saying so.
- [ ] Each section D candidate has all 11 subsections and a day-by-day
      schedule.
- [ ] Each proposal states a mechanism, not just an intention.
- [ ] No candidate rated HIGH lacks a sourced weakness *and* a reproducible
      or directly comparable baseline.
- [ ] Section A states explicitly whether any HIGH candidate exists.
- [ ] Section F lists every benchmark screened but not shortlisted, with
      its rejection reason.
- [ ] Effective profile and every override are stated in section A.
- [ ] No fabricated, remembered, or "approximately" scores anywhere.
- [ ] The 10 integrity rules in `integrity_rules.md` were re-read and hold.
