---
name: paper-review-local
description: Check local manuscripts, PDFs and supplied-text overlap.
version: 0.4.1
license: MIT
metadata:
  hermes:
    tags: [research, paper, review]
---

# Local Manuscript Review

## When to use

Use for a completed manuscript package or revision needing local checks and input-bound findings.

Read the manuscript and original evidence before the author's self-review. For revisions, prior findings and the author's response provide useful context. Automated output is not peer-review approval.

## Run the checks

Runtime files: [review_mcp.py](scripts/review_mcp.py), [CLI dependencies](scripts/requirements.txt), [optional MCP dependencies](scripts/requirements-mcp.txt). Install dependencies for the requested mode.

Read [local-tools.md](references/local-tools.md) for installation, CLI and optional MCP use. The bundled script takes an explicit repository root and package path; it needs no agent profile, GPU, provider credentials or network access. It writes reports under `reviews/<review-id>/` and keeps manuscript inputs unchanged.

Inspect sections, bibliography keys, figures, readable PDF pages, author placeholders and ChkTeX execution. Missing dependencies and failed checks remain explicit. Missing ChkTeX blocks a completed LaTeX-review claim. Reports bind supporting package files to input hashes and reject reuse after inputs change.

Only provided `sources/*.txt` are compared for English word sequences and sentence-string overlap. Examine matches with their citation and quotation context. Short technical phrases and the author's earlier drafts require different treatment. No supplied sources or no matches do not establish originality. The tool produces no global plagiarism percentage or AI-authorship verdict.

## Review content and layout

Inspect actual PDF page images for clipping, spacing, units, captions and typography. Mark visual inspection unverified when actual pixels are unavailable. Check claims against source artifacts and exact comparison protocols. Verify literature support against original cited passages.

Record location, evidence, impact and a correction for each finding. The optional `save_editorial_review` MCP tool requires strings for all values and fields `id`, `location`, `evidence`, `priority` (`required`, `recommended`, `minor`), `explanation`, `confidence` (`high`, `medium`, `low`), `suggested_correction`. Save findings with the matching digest; changed inputs need a fresh review.

Distinguish author-side review, independent review and venue decisions. Bound revisions to the user's task and record unresolved issues. Author identities, rights, venue rules and upload readiness remain separate from static checks. Consult current official submission instructions when submission preparation is requested.

The bundled workflow performs no external upload or submission. Provider comparisons need a supported connection and applicable user authorization; a score alone cannot certify or reject a manuscript.

## Pitfalls and verification

Successful CLI exit means a report was saved, not that every check passed. Read statuses and unresolved findings. Same-ID reports are immutable; changed inputs or check environments need a fresh ID. PDF readability is separate from layout inspection, and overlap candidates are separate from plagiarism findings.

Version 0.4.1 declares the Hermes frontmatter version and directly links runtime files for URL installation. The check engine remains 0.4.0.
