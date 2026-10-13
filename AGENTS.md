# Repository instructions

Read CONTRIBUTING.md before adding or moving contributions.

- Use tracks/auto-paper, tracks/auto-application, or tracks/auto-post.
- Keep each reusable skill once at tracks/<track>/skills/<name>/SKILL.md. Its frontmatter name must match its directory and be unique across all tracks.
- Search existing skills and open PRs before adding another skill. Improve the existing implementation when its input, purpose, and output match. Document differences when keeping related implementations.
- Put project code and guides in tracks/<track>/projects/<project>. Put published results or external-result indexes in outputs/week-NN under that project.
- Preserve original content, attribution, licenses, historical verification records, and binary deliverables when reorganizing. Repair live references, tests, and workflow paths.
- Keep root README and docs for repository-wide guidance. Do not copy credentials or private source data.
- Run python3 scripts/check_repository.py and relevant existing tests. Distinguish rerun checks from contributor-reported results.
- Update the current PR for revisions. After the common rules PR #16, contribution PRs must be mergeable in any order against main. Do not stack them on another open PR or assume another unmerged contribution is present.
- Preserve the contributions of related PRs. If open PRs share files, keep their final contents identical or separate their changes; verify both merge orders and retain a distinct contribution in each PR.
- Supported GitHub merge methods are merge commit and squash. Rebase-and-merge is disabled because replaying pre-migration commits can conflict; do not rewrite contributor history to work around this.
- Do not merge PRs without explicit maintainer authorization.
