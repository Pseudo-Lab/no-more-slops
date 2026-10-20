# Portable local checks

Python 3.10+ is required. Install the PDF/string-comparison libraries:

```sh
python -m pip install -r /path/to/paper-review-local/scripts/requirements.txt
python /path/to/paper-review-local/scripts/review_mcp.py \
  --root /path/to/project --package paper --review-id initial-01
```

A package contains `shortpaper.md` or `manuscript.md`, the same-stem `.tex` and `.pdf`, `references.bib`, figures referred to by TeX, and optionally `sources/*.txt` and `renders/page-*.png`. The Markdown citation check recognizes Pandoc `@key` citations; verify other conventions separately. Text overlap is English-only. Optional `build_validation.json` plus `task_state.json` can bind a recorded `pdf_sha256` to the PDF; this is hash agreement, not a compilation test.

Install ChkTeX through your operating system's package manager (e.g. `apt install chktex` on Ubuntu). It is discovered on `PATH`; `PAPER_REVIEW_CHKTEX` overrides the binary. `PAPER_REVIEW_CHKTEX_RC` optionally names a configuration file. The report preserves command, diagnostics and stderr. Configuration warnings remain visible. TeX input traversal is disabled. Missing or broken lint execution remains `not_installed` or `tool_error` and prevents an editorial save through MCP.

Reports go to `paper/reviews/initial-01/local_checks.json`. Use a fresh ID after changing the input package or check environment. Reusing an ID with identical input hashes returns the immutable earlier report; it does not refresh dependency/linter results. Support files are hashed, excluding review outputs, caches and common TeX intermediates. New support files invalidate a subsequent editorial save. Keep the evidence package small and relevant.

`pypdf` and `RapidFuzz` are imported only for their checks. Missing libraries produce explicit unavailable results; the remaining checks still run. Successful CLI exit means a report was written, not that every check passed. Scientific content, actual layout, attribution and submission decisions need separate review.

## Optional MCP

Install `scripts/requirements-mcp.txt` in the agent host's Python environment and register this stdio command:

```sh
python /path/to/paper-review-local/scripts/review_mcp.py \
  --serve --root /path/to/project
```

`--root` applies to every tool; `PAPER_REVIEW_ROOT` or the current directory is the fallback. Tools: `run_local_review`, `read_local_review`, `read_review_input` (bounded text), `read_rendered_page` (existing PNG), `save_editorial_review`, `local_review_capabilities`. The server starts no models or render/build jobs. Editorial save requires matching current input hashes, valid fields and completed ChkTeX execution. Saved reviewer-provided content is not an automated acceptance decision.
