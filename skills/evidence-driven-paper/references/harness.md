# Paper checks harness

Python 3.10+; the paired-record and hash checks use only the standard library.
PDF page checks additionally require pypdf (tested with the version in CI).
The script never edits inputs or runs experiments. Its JSON report describes
mechanical checks, not a scientific or independent audit.

From the repository root:

~~~sh
python3 skills/evidence-driven-paper/scripts/paper_checks.py \
  skills/evidence-driven-paper/assets/example/checks.json
python3 -m unittest discover -s tests -v
~~~

The bundled example is invented: Candidate has one lower-score win, Baseline
has one, and one is an exact tie. It includes a frozen input hash.

Copy the example configuration into your paper directory and adapt it.
All input paths are relative to the configuration's directory, must stay inside
that directory (including symlinks), and must identify files. Place the manifest
at the project root if data and submission files are in different subdirectories.

## Configuration

~~~json
{
  "schema_version": 1,
  "comparisons": [
    {
      "id": "candidate-v-baseline",
      "candidate": {"name": "Candidate", "path": "results/candidate.jsonl"},
      "baseline": {"name": "Baseline", "path": "results/baseline.jsonl"},
      "keys": ["dataset", "model", "seed"],
      "metric": "brier",
      "direction": "lower",
      "roster": "exact",
      "expected_pairs": 3,
      "expect": {"candidate_wins": 1, "baseline_wins": 1, "ties": 1}
    }
  ],
  "artifacts": [
    {"path": "paper.pdf", "pages": 4},
    {"path": "supplement.pdf", "max_pages": 30},
    {"path": "code.zip"},
    {"path": "results/candidate.jsonl", "sha256": "REPLACE_WITH_SAVED_SHA256"}
  ]
}
~~~

These illustrative numbers show the schema, not evidence of a new result.
An unedited placeholder hash is rejected. The runnable example has only small,
invented records and a real hash.

Top-level fields:
- schema_version: integer 1.
- comparisons and artifacts: arrays, either may be omitted, but at least one
  check must be present. Unknown fields are rejected.

Each comparison requires:
- id: unique nonempty identifier.
- candidate and baseline: distinct nonempty names and relative file paths.
  Each JSONL file contains only that method's records.
- keys: nonempty list of unique field names defining a matched observation.
  Key values must be strings or integers; types are significant.
- metric: a numeric, finite field. Booleans and numeric strings are rejected.
  Records may contain other fields; duplicate JSON object keys are rejected.
- direction: lower or higher. Output always reports candidate minus baseline
  in the original metric, regardless of which direction is better.
- roster: exact requires identical key sets; intersection permits different
  sets and explicitly reports every unmatched key. Choose intersection only
  for a justified, declared evaluation roster, not to discard missing results.
- expected_pairs: positive integer matched count. A mismatch fails the check.
- expect: optional subset of candidate_wins, baseline_wins, ties, each a
  nonnegative integer. This guards a stated count against the actual records.

Records are paired by keys, never file order. Duplicate observation keys,
missing fields, empty files, and nonfinite values fail. Exact floating-point
equality defines a tie; it is not practical equivalence. A file must not mix
methods or experimental settings omitted from the keys.

The report includes source SHA-256 hashes, means, signed mean difference,
named winner counts, exact ties, matched denominator, unmatched keys, and an
unambiguous sentence. Extra records are validated even under intersection.
It deliberately computes no confidence intervals or significance judgments.
Define dependencies, aggregation weights, and bootstrap units in the analysis
code appropriate to the experiment.

Each artifact requires path and may include:
- sha256: previously saved 64-digit hex digest, to detect unintended changes.
- pages: exact positive PDF page count.
- max_pages: positive PDF page limit.
  If either is supplied, the file must parse as a PDF and pypdf must be installed.
  Missing pypdf is a failure, never a skipped successful check.

All artifacts are checked for existence and hashed. PDF contents, ZIP members,
embedded attachments, hyperlink destinations, and semantic agreement between
prose and data are outside this harness. Inspect them using project-specific
build and PDF tools. Include every promised companion in the manifest.

## Baselines, output, and failure behavior

Save input hashes before an editorial revision, preferably in version control.
Compare the final inputs against those saved values. A hash computed only after
editing establishes the identity of the current file, not that it was unchanged.
After an intentional experimental change, review why the expected data and
counts changed before updating the manifest.

~~~sh
python3 skills/evidence-driven-paper/scripts/paper_checks.py \
  /path/to/paper/checks.json --output /path/to/paper/check-report.json
~~~

Standard output is JSON. The optional output file is created exclusively;
an existing path is refused to avoid overwriting evidence. Use a new report
filename for each revision. Exit status is 0 when all declared checks pass,
1 for a failed comparison or artifact check, and 2 for invalid configuration
or a report-writing failure. Errors include context and never silently pass.

A passing report means only that the supplied manifest and supplied files
satisfy these checks. It cannot establish that the manifest is complete, that
the right baseline was supplied, that the paper says what the records show,
or that a reviewer should accept the paper.
