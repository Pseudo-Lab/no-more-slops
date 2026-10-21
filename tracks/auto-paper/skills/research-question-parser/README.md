# research-question-parser

Pulls the distinct research questions and ideas out of your notes, PDFs or
idea files and gives each one a stable slot ID (`RQ1`, `RQ2`, ...). It is the
first step of [research-pipeline](../research-pipeline/README.md), and you can
also run it on its own.

## When to use it

- You have a messy idea dump (meeting notes, a brainstorm doc, a PDF of
  proposed experiments) and want a clean, numbered list of questions.
- You want to start the planning pipeline and need consistent `RQk` IDs that
  later skills will keep.

## How to use it

Name the skill and the file(s):

```
/research-question-parser ideas.md
```

or in plain language: *"Parse the research questions out of
notes/brainstorm.pdf."*

### Two modes (chosen automatically from what you say)

| Mode | When it is used | What you get |
| --- | --- | --- |
| **Benchmark-First** (default) | You care about feasibility, a short time budget, established benchmarks, or you say the topic may change | Each idea becomes a *seed direction*: research interest, seed question, broad area, target behaviour, reusable components, constraints. Later skills may replace the question but keep the `RQk` ID. |
| **Fixed-Topic** | You say a question must be kept as is | Original wording and meaning are kept; scope is not widened. |

To force a mode, say so: *"Keep RQ2 exactly as written"* (Fixed-Topic) or
*"Topics can change, I just want feasible projects"* (Benchmark-First).

## Output

Printed in chat:

- **Research Questions**: original and cleaned wording for each `RQk`.
- **Seed Directions** (Benchmark-First only).
- **Possible Research Questions**: ambiguous items marked `POSSIBLE`, with
  the reason.
- **Duplicates / Overlap**: overlapping ideas are listed, never merged.
- **Summary**: counts of clear, possible and total ideas (`m`).

## Notes

- Reads `~/.claude/skills/benchmark-finder/references/research_advice.md`
  first. That file is mentoring advice. It is never treated as proof that
  an idea is novel.
- It never invents novelty claims or benchmarks. That is the job of
  [benchmark-finder](../benchmark-finder/README.md) and
  [prior-work-checker](../prior-work-checker/README.md).

## Next step

Hand the `RQk` list to `/benchmark-finder`, or run the whole flow with
`/research-pipeline`.
