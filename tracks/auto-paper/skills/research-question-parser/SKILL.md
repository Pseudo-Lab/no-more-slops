---
name: research-question-parser
description: Extract and organize research questions and research ideas from files or notes.
---

# Research Question Parser

Extract distinct research questions and research ideas from user-provided
files or notes.

## Input

The user provides:
- One or more files or notes containing research ideas

## Priority Reference

`~/.claude/skills/benchmark-finder/references/research_advice.md`
(`C:\Users\elika\.claude\skills\benchmark-finder\references\research_advice.md`)
is the PRIMARY and HIGHEST-PRIORITY research-planning reference for this
project. Read it before extracting. If it conflicts with the default behavior
of this skill, follow it. It is mentorship guidance, not scientific evidence,
and must not be used to claim novelty, a literature gap, or that a benchmark
is established.

## Modes

### Fixed-Topic Mode

Use when the user explicitly wants to preserve a research question.

- Preserve wording and meaning.
- Do not unnecessarily broaden scope.
- Downstream work should remain centered on the original question.

Follow Steps 1-6 and the Output below.

### Benchmark-First Mode

Use when the user prioritizes feasibility or explicitly allows topic changes.

Do NOT treat extracted research questions as commitments. Instead extract,
for each idea:

- Candidate Research Interest
- Seed Question
- Broad Research Area
- Target Behavior / Phenomenon
- Potentially Reusable Experimental Components
- Constraints implied by the idea

Label them clearly as SEED DIRECTIONS, using the same slot identifier as the
research question (RQ1, RQ2, ...). Downstream skills may replace them with
benchmark-derived final research questions, keeping the same identifier.

In this mode, do not interpret "preserve the original idea" or "do not
expand scope" (Step 3) as requiring preservation of the original research
question. Preserve what the user was interested in, without forcing the final
project to test exactly that question. Steps 1, 2, 4, 5 and 6 still apply
(extraction, ambiguity labeling, overlap reporting, identifier assignment), and the
original wording
should still be recorded. Do not invent novelty claims.

Mode selection:

Do NOT ask the user to choose a mode when the intent can reasonably be
inferred.

- Use Fixed-Topic Mode only when the user explicitly indicates that a
  particular research question/topic should be preserved.
- Use Benchmark-First Mode when the user asks for the most feasible
  project, prioritizes a short time budget, asks to follow established
  benchmarks, allows the topic or research question to change, or asks for
  project/ranking recommendations without requiring preservation of the
  original topic.
- If the user's intent is genuinely ambiguous, default to Benchmark-First
  Mode, because `research_advice.md` is the highest-priority planning
  reference and favors benchmark-grounded project selection.

Only ask a clarification question when choosing the wrong mode would
materially change the task and the user's intent cannot reasonably be
inferred.

## Workflow

### Step 1: Read the source

Read the provided files or notes completely before extracting questions.

### Step 2: Extract research questions

Identify:
- Explicit research questions
- Clearly stated hypotheses
- Research ideas that can reasonably be expressed as testable questions

Do not treat the following as research questions unless they clearly
propose a research direction:
- Background information
- Paper summaries
- Citations
- General observations
- TODO items

### Step 3: Preserve the original idea

(In Benchmark-First Mode, preserve the original wording and record the
interest, but see Modes above: the original question is a seed, not a
commitment.)

Preserve the user's original meaning and wording as much as possible.

For each question, provide:
- Original wording
- Cleaned research question

Question format (required for "Cleaned" and "Seed Question"): each must be
a single interrogative sentence that:
- ends with "?",
- starts with an interrogative form (Does / Do / Is / Are / Can / Will /
  Which / How much / To what extent ...),
- is not an imperative, a noun phrase or title, a hypothesis statement, or
  a method description, and
- contains exactly one question.

If the source states the idea as a topic, hypothesis, or experiment
description, convert it into question form without changing its meaning.
If one source item contains two questions, split them into separate
identifiers and report the overlap. Do not merge them. The "Original" field
stays verbatim and is exempt. Check every Cleaned and Seed Question
against this rule before output.

Do not:
- Invent new research ideas
- Expand the scope
- Claim novelty
- Merge ideas under a single identifier (report overlap instead; see Step 5)

### Step 4: Handle ambiguity

If something may be a research question but is ambiguous, label it:

POSSIBLE RESEARCH QUESTION

Do not silently discard it.

### Step 5: Deduplicate

Identify substantially overlapping questions.

Report the overlap, but do NOT merge them: each parsed idea keeps its own
identifier. Downstream skills decide which ideas become output slots.

### Step 6: Assign identifiers

Assign every parsed research question or idea, CLEAR or POSSIBLE, an
identifier RQ1, RQ2, ..., RQm (m = number of parsed ideas). CLEAR / POSSIBLE
is metadata only.

This skill does NOT determine the final output cardinality N. The pipeline
sets N: the user-provided "Number of research directions: N" if given,
otherwise N = m. Report m.

Identifiers are permanent: if downstream planning replaces an idea's
content, the identifier stays the same (RQ3 original → RQ3 replacement).
Downstream skills give any newly generated directions the next unused
identifiers (RQm+1, ...).

The original questions are preserved here for traceability only. Downstream
planning may substantially rewrite or replace them.

## Output

### Research Questions

RQ1

Original:
Cleaned:

RQ2

Original:
Cleaned:

### Seed Directions (Benchmark-First Mode only)

RQ1 (seed direction)

Original:
Candidate Research Interest:
Seed Question:
Broad Research Area:
Target Behavior / Phenomenon:
Potentially Reusable Experimental Components:
Constraints Implied:

### Possible Research Questions

RQk (POSSIBLE)

Original:
Why ambiguous:

### Duplicates / Overlap

List substantially overlapping questions here (not merged).

### Summary

Total clear research questions:
Total possible research questions:
Total parsed ideas (m = clear + possible):
(Final output cardinality N is set by the pipeline, not by this skill.)