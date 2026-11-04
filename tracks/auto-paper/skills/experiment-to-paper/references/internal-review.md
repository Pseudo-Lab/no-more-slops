# Internal manuscript review

This is an author-side review of the user's own draft. It is not a confidential third-party journal review, venue acceptance prediction or independent reviewer report.

Review the manuscript, claim table, generated tables, result metadata and relevant evaluation code. Do not review only the prose.

## Review lenses

- **Evidence and methods:** Are headline claims supported at the same unit and scope? Do comparison arms differ in proposals, training, crops, score selection, matching or evaluation exclusions? Are raw and balanced results distinguished?
- **Positioning:** What is already contributed by the cited prior work? Is the new observation distinguishable from their findings? A new application or result table does not by itself settle novelty.
- **Statistics and reproducibility:** Are denominators, units, strata, sampled images, checkpoints, settings, commands and missing uncertainty clear? Could per-image dependence or label noise alter the interpretation?
- **Presentation:** Do title, abstract, figures and conclusion match the bounded findings? Are comparisons understandable without reading the chat? Are references and limitations placed next to the claims they qualify?

Use a structured review record with `summary`, `strengths`, `major_issues`, `minor_issues`, `unresolved_checks` and `revision_actions`. For each issue, include its manuscript location, observation, evidence path/selector, impact and a concrete correction. Prefer narrowing a claim when the current data supports a narrower result.

Prioritize factual or methodological errors over presentation. Resolve each issue by correcting the draft, checking available artifacts, or recording the evidence that is still missing. An unresolved issue may limit submission readiness without preventing a useful working draft.

## Quality checklist

For each item record `supported`, `needs_revision`, or `not_available`, with the manuscript location:

1. Abstract and introduction state only observed contributions and bounded interpretations.
2. Methods distinguish pretrained components, new training and frozen parameters.
3. Data split, actual sample count and task construction are specified.
4. Comparison settings and protocol differences are disclosed.
5. Tables and figures have correct units and match source artifacts.
6. Uncertainty, sample dependence and unavailable statistics are described.
7. Original sources support the cited claims; metadata verification alone is insufficient.
8. Known limitations and plausible alternative explanations are included.
9. Reproduction instructions, versions and available artifacts are listed.
10. The repository acknowledgement is included; venue-specific requirements remain pending until a venue is chosen.

This checklist is adapted to an internal ML draft. It is not a completed NeurIPS submission checklist. If submitting to a venue later, retrieve its current instructions and template.
