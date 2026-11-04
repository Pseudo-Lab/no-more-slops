# research-benchmark-advisor

A standalone **live-web research advisor** for less experienced
researchers. It browses Papers with Code task categories (falling back to
official benchmark repos, Hugging Face leaderboards, GitHub and the
original papers), pulls current leaderboards and leading papers, checks
that the code, data and evaluation scripts actually exist, and ranks
subfield + benchmark combinations by **your realistic chance of beating
the strongest comparable published baseline within four working days**,
written up as a four-page paper.

Every number is labelled **Verified / Inferred / Unverified**, with the
source link and retrieval date. Nothing is invented.

## When to use it

- You don't have a topic yet and want to know where a quick SOTA result is
  realistic.
- You want to compare benchmarks within one subfield before committing.
- It is a lighter-weight alternative to the Discover stage of
  [research-pipeline](../research-pipeline/README.md).

## How to use it

```
/research-benchmark-advisor
/research-benchmark-advisor Find the best beginner-friendly SOTA opportunity within four days
/research-benchmark-advisor Focus on OOD detection
/research-benchmark-advisor Compare anomaly detection benchmarks profile: gpu=none; days=6
/research-benchmark-advisor must involve LLMs brief nosave
```

| Argument | Effect |
| --- | --- |
| *(nothing)* or a goal-style sentence | **Broad Discovery Mode** (default): explores many subfields |
| One subfield or benchmark family named | **Focused Analysis Mode** |
| `profile: field=value; ...` or a profile file path | Overrides fields of the default researcher profile |
| "six days", "eight-page", "CPU only", "must involve LLMs" | Replaces the matching default constraint (recorded in section A) |
| `brief` | Section D covers only the top 3 candidates |
| `nosave` | Don't write the report file |

## Hard gates (never traded off)

H1 accessible to a beginner · H2 feasible in four days · H3 fits a
four-page paper · H4 has technical depth. If nothing passes all four, the
report opens with *"No candidate currently satisfies all hard constraints
with sufficient evidence."* and lists the closest alternatives.

## Output

The report is printed in chat and, unless `nosave` is given, saved as
`research_benchmark_advisor_<YYYY-MM-DD>[_<slug>].md` in the current
directory. Sections:

A. Executive summary · B. Ranked subfields · C. Ranked subfield–benchmark
combinations · D. Detailed analysis of top candidates · E. Five final
recommendations · F. Rejected candidates · G. Sources and verification.

## Files (`references/`)

| File | Purpose |
| --- | --- |
| `researcher_profile.md` | Default profile and override syntax. Edit this to change your defaults. |
| `sources.md` | Primary source, fallback chain, categories to browse |
| `discovery_workflow.md` | Detailed Steps 1–7 |
| `sota_feasibility.md` | 10-point SOTA investigation and the HIGH…VERY LOW rubric |
| `scoring_rubric.md` | Gates H1–H4, weights, Rankings A and B |
| `report_template.md` | Exact report structure |
| `integrity_rules.md` | Evidence labels and sourcing rules |

It does not depend on any project and does not touch project files other
than its own report.
