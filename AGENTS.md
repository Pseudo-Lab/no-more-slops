# Repository instructions

Read CONTRIBUTING.md before adding or moving contributions.

- Use tracks/auto-paper, tracks/auto-application, or tracks/auto-post.
- Keep each reusable skill once at tracks/<track>/skills/<name>/SKILL.md. Its frontmatter name must match its directory and be unique across all tracks.
- Search existing skills and open PRs before adding another skill. Improve the existing implementation when its input, purpose, and output match. Document differences when keeping related implementations.
- Put project code and guides in tracks/<track>/projects/<project>. Put published results or external-result indexes in outputs/week-NN under that project.
- Preserve original content, attribution, licenses, historical verification records, and binary deliverables when reorganizing. Repair live references, tests, and workflow paths.
- Keep root README and docs for repository-wide guidance. Do not copy credentials or private source data.
- Run python3 scripts/check_repository.py and relevant existing tests. Distinguish rerun checks from contributor-reported results.
- Update the current PR for revisions. Record dependencies and preserve changes introduced by later PRs.
- Do not merge PRs without explicit maintainer authorization.
