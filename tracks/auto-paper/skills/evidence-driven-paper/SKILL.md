---
name: evidence-driven-paper
description: Draft or revise empirical research papers from results and reviewer feedback, especially when component attribution, tuning fairness, tiny effects, short-paper limits, or submission consistency matter. Use to connect claims to evidence, choose discriminating controls, and prepare a reviewable manuscript and companion files.
---

# Evidence-driven paper

Turn evidence into a paper whose main argument a reviewer can assess without
running the code. Improve the evidence or narrow the claim when a review exposes
a gap; acceptance is not an outcome this skill can guarantee.

## Establish the revision contract

Inspect the manuscript source, result files, build instructions, and current
review before editing. Reuse the user's existing decisions about language,
venue, page budget, and deliverables. Do not assume a four-page limit, LaTeX,
a supplement, or formal proofs. Use existing authorization and resource
constraints for experiment runs.

Separate requested work into:

- Editorial corrections supported by existing evidence.
- Reanalysis of existing outputs.
- New experiments needed to distinguish explanations.

Complete independent, authorized work while clarifying genuinely missing
constraints. Use the smallest scope that answers the review. A wording fix
normally needs a source/PDF check, not another benchmark run.

## Build the claim-to-evidence chain

For each central claim, record its exact wording, population, comparison,
metric and direction, independent sampling unit, effect size and uncertainty,
source artifact, analysis timing (prespecified or post hoc), and limitation.
Keep this in the project's existing notes, or use the compact ledger example
in [the review playbook](references/review-playbook.md).

Start with the question each comparison can answer:

- Whole procedure versus a strong baseline: overall performance.
- A matched function family with independently tuned penalties: regularization.
- The same objective in different coordinates: numerical optimization.
- The same method under different selection rules: tuning procedure.

These are examples, not mandatory experiments for every paper. Read
[the review playbook](references/review-playbook.md) when selecting controls,
interpreting uncertainty, or handling numerical/formal verification.
If existing evidence cannot support a stronger contribution, say what additional
observation would change that assessment. Do not invent results or disguise
post hoc choices as predictions.

## Write the main paper around the finding

Lead with the research question, evidence, and resulting knowledge. For a short
paper, retain the model, assumptions, central relation and its meaning, a short
proof where needed, experimental design, key results, and limitations. Move
routine algebra or diagnostic detail to identified companion sections only
when companions are part of the agreed submission.

Make the main argument self-contained; optional derivations may remain outside
it. A request for one PDF concerns packaging and does not automatically change
the main-text page limit.

Use a table to connect questions to controls, tuning budgets, effects, and
uncertainty. Separate different evaluation populations. If the proposed
mechanism depends on a variable, show results by that variable and disclose
confounded changes, averaging, and duplicated conditions. Use a figure only
when it helps the reader see those results.

Name the winner and comparator explicitly: “Candidate outperforms Baseline on
X of N matched pairs.” State the metric and direction nearby. For lower-is-better
metrics, a more negative difference means a larger benefit. Condition percentages on their actual setting, including
synthetic experiments. End with the research conclusion and its boundary.

## Verify and deliver

Use [the harness guide](references/harness.md) for the bundled, read-only
comparison and artifact checks. It checks supplied records and declarations;
it does not establish statistical significance or evaluate prose truth.

Before editing experimental artifacts, record a baseline manifest of relevant
inputs. For editorial revisions, compare against that earlier manifest.
Never regenerate expected hashes merely to make an unexpected change pass.

Build with the project's existing commands. Check page limits, extracted PDF
text, rendered pages, readable figures/tables, winner wording, and actual links
to supplied companions. Check the final assembled PDF too when requested:
component order, page count, internal links, and embedded files if used.
File existence and matching hashes do not establish that a hyperlink works.

Report what changed, which checks actually ran, the resulting deliverable paths,
and any unresolved evidence gap. Distinguish your execution from an independent
audit. Keep original data, proofs, and reported results intact unless the
authorized revision requires changing them.
