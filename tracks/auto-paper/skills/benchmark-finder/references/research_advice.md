# Research Mentorship Advice

## Benchmark-first project selection

For short-term research projects:

- Start from an established benchmark rather than committing to a research topic first.
- Prefer modifying or extending an existing benchmark over creating a new task or dataset.
- Prefer projects with existing datasets, evaluation metrics, baselines, and code.
- For a one-week project, implementation simplicity and reuse of existing infrastructure are major selection criteria.
- The research topic is not fixed. It may be changed or discarded if another benchmark offers a substantially more feasible one-week research opportunity.
- Prefer the smallest meaningful extension of an established benchmark.

## Interpretation note (user instruction, 2026-10-09)

The mentor's advice above is unchanged. Apply it with the shared
definitions in
`~/.claude/skills/research-pipeline/references/research_design_principles.md`:

- **"Smallest meaningful extension"** means the smallest *scope* (one
  isolated intervention, a pre-specified slice, reused assets) that still
  delivers a technically meaningful contribution (technical depth, §3).
  It never means a trivial heuristic such as a threshold, vote or
  average.
- **"Implementation simplicity and reuse"** favour reusing code, models,
  outputs and activations. They do not exclude GPU, fine-tuning,
  white-box or interpretability work that is feasible with those assets.
- **"Discarding a topic for a more feasible benchmark"** happens only
  after the redesign levers in §6 have been tried.
- **"One-week"** stands for the user-specified duration D. The user's
  current standard sprint is 4 working days.