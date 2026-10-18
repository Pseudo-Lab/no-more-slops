# reuse_runs.py

Python 3.10+, standard library only. It reads records and writes only to a new
output directory (`derive`); the other commands print JSON. Exit code 0 means no
problem was found, 1 means a check reported errors, 2 means invalid input.

## Records

One JSON object per line (or a run directory holding `records.jsonl` and
optionally `manifest.json` with an integer `max_repairs`):

~~~json
{"id": "ex-1", "replicate": 0, "method": "loop", "correct": true,
 "trace": [{"proposal": {"calls": []}, "passed": false, "correct": true, "latency_s": 1.2},
           {"proposal": {"calls": [{"name": "f"}]}, "passed": true, "correct": false, "latency_s": 1.4}]}
~~~

`replicate` defaults to 0. Field paths are dotted and set with global options:
`--passed` (step, bool), `--correct` (step), `--proposal` (step, compared for
pairing and overlap; use `proposal.calls` to ignore latency or usage fields) and
`--row-correct` (row; the final correctness, empty to skip). For example, records
with `trace[].gate_pass`, `trace[].score.correct` and `score.correct` use
`--passed gate_pass --correct score.correct --row-correct score.correct`.

## Commands

| Command | Use | Output |
| --- | --- | --- |
| `derive SRC OUT --limit R [--rule last\|first] [--methods m] [--sum field]` | Cut stop-at-pass rows at `R` and choose the final attempt: the first pass, else the last or the first attempt. Other methods are copied. | `OUT/records.jsonl` with `final_attempt`, `passed`, `exhausted`, `final_proposal`, `derived`; `OUT/derived.json` with the source hash |
| `pairing RUN... [--expect shared\|new]` | Same first proposal for every method of an example; across runs, shared (rerun) or new (repeat) | per-run counts and errors |
| `overlap EXTENDED SOURCE [--limit R]` | A continued run reproduces the source up to `R` | errors |
| `paired RUN... --a M --b B [--exclude field=value]` | `M − B` correctness per example, averaged over runs, bootstrap over examples (seed 1729, 2,000 samples) | delta, 95% interval, counts |
| `plan RUN [--new-limit R]` | Rows that reached the limit (continuation) and rows whose first proposal was rejected (partial rerun) | counts per method |

`derive` refuses a larger limit than the source's and any trajectory that does
not follow stop-at-pass (a pass before the last attempt, or an unpassed
trajectory shorter than the limit). It never overwrites an existing output.

These are mechanical checks. They do not decide whether a route is valid for
your pipeline; the conditions in [the decision table](decision-table.md) do.
