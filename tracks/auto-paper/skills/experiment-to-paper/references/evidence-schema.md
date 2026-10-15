# Saved JSON evidence export

Python 3.10+ and the standard library are sufficient. Copy this entire skill folder to your agent's skill directory, or call the repository copy. `--root` is the project containing the inputs; it need not be a Git checkout.

Create a specification:

```json
{"schema_version": 1, "measurements": [
  {"id": "selection_accuracy", "file": "results.json", "pointer": "/accuracy", "unit": "fraction", "denominator": 120}
]}
```

```sh
python /path/to/experiment-to-paper/scripts/export_evidence.py \
  --root /path/to/project --spec export-spec.json --out /tmp/paper-evidence-new
```

`file` and `--spec` are relative paths confined to `--root`, including resolved symlinks. `pointer` is an RFC 6901 JSON pointer: escape `/` in a key as `~1` and `~` as `~0`; array indices start at zero. An empty pointer selects the whole document. IDs must be unique. Values must be finite numbers or `null`; booleans and missing selectors are rejected. Null appears as `unavailable`, while zero remains zero. `unit` is required. A denominator is optional, positive when present, and caller-supplied rather than independently verified.

The new directory contains `evidence/measurements.json`, `evidence/manifest.json` and `tables/measurements.md`. The manifest hashes the specification and result bytes, records a Git snapshot revision when available, and leaves the experiment execution revision unknown. Existing output directories are preserved; inspect them and choose a fresh directory for another export. All inputs are validated before publishing output.

This checks transcription and hashes, not labels, aggregates, significance, novelty or scientific support. Use project-specific analysis for those checks.

## Invented example

From the repository root, this example needs no project data or third-party dependencies:

```sh
python3 tracks/auto-paper/skills/experiment-to-paper/scripts/export_evidence.py \
  --root tracks/auto-paper/skills/experiment-to-paper/assets/example --spec export-spec.json \
  --out /tmp/paper-evidence-demo-new
```

Expect three measurements: `0.75`, a measured `0`, and an unavailable `null`.
After copying the skill, replace the two `tracks/auto-paper/skills/experiment-to-paper` prefixes
with its installed directory. Use a fresh output path for another run.
