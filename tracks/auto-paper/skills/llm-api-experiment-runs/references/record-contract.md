# Record contract

What a run must save so it can be resumed, checked, compared and later reused.

## Manifest (written before the first request)

| Field | Why |
| --- | --- |
| `code_sha256` (hash of the source files that build requests) | Continuations and reruns must use the code that produced the source run |
| `dataset_sha256`, data revision, `ids` | Same examples, same order of evidence |
| `replicates`, `methods`, `expected_records` | The grid that "complete" means |
| Every setting a request depends on: limit, thresholds, final-answer rule, prompts or prompt version, output-token limit, temperature, reasoning effort | A changed setting is a different run |
| Requested model, returned model id, provider, API style, endpoint or gateway | What actually answered |
| Prices per million tokens by kind | Costs can be recomputed |
| Route history (`first_attempt` and route) if a route changed during a run | Allowed only when recorded |
| `config_id`: a hash of all of the above | Resume refuses another configuration |

Leave operational fields (worker count, timestamps, local paths) out of the
fingerprint, and record them separately.

## Row (one per example × run × method, appended when finished)

- Keys: `id`, `replicate`, `method`, `config_id`; category or other labels used
  only for scoring.
- `trace`: one entry per attempt in order, with the proposal (parsed calls or
  answer, raw text, finish reason, an `incomplete` reason for unreadable outputs,
  usage, latency, returned model), the verifier's raw output (probabilities,
  verdicts, usage, latency, retry wait), the feedback actually shown next, the
  pass flag, and the score added after the loop.
- Final fields: final proposal, accepted or not, limit reached or not, repairs.
- Accounting: token totals by kind, estimated cost, and whether usage was
  complete.
- Whether the first proposal was shared with the other methods.

## Files

`manifest.json`, `records.jsonl` (append-only), `errors.jsonl` (sanitized error
events), `summary.json` (regenerated from records, never edited by hand) and a
run log. A derived or continued run records its source directory, the source's
fingerprint and the hash of the source records.
