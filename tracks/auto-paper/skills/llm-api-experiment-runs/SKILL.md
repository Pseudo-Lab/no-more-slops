---
name: llm-api-experiment-runs
description: Plan, run and verify paid LLM or verifier API experiments over many examples. Use before and after any benchmark run that spends money - configuration and key checks without printing secrets, a one-call preflight, cost and time estimates from recorded rows, resumable fingerprinted runs, a policy for truncated, filtered, billing and rate-limit failures, handing long runs to the user, and completion checks before reporting numbers.
---

# LLM API experiment runs

Every request costs money and every recorded row is evidence. Run so that a
stopped run can resume, a finished run can be checked, and later protocol changes
can reuse the records (see the `reuse-recorded-runs` skill when one is needed).

## Before spending

1. **Resolve the configuration.** Print what will be called: provider and API
   style, endpoint or gateway, deployment and model snapshot, reasoning effort,
   output-token limit, temperature, verifier model, prices. For keys print only
   `set` or `missing`; never print, log or commit their values.
2. **Preflight.** Send the smallest real request to each API with the run's
   settings. Check that the output parses, that the returned model is the one
   intended, and that usage is reported. Stop on authentication, billing, quota
   or deployment errors and tell the user which one (see
   [failures](references/failures.md)).
3. **Estimate.** From a pilot or an earlier run, measure tokens, attempts and
   seconds per row by method (`scripts/run_tools.py estimate`), multiply by the
   planned rows, and show cost and wall time with their assumptions. Wait for the
   user's go-ahead before a paid run.

## Run contract

Follow [the record contract](references/record-contract.md):

- Write the manifest before the first request: every setting that affects a
  request, code and data hashes, models, prompts, prices and routes, and a
  fingerprint of them. Operational options such as worker count stay out of it.
- Append one row per example × run × method as soon as it finishes, flushed to
  disk, with the full attempt trace. Score after the loop, never inside it, and
  never send labels to a model.
- Resume by skipping completed rows; refuse to resume into a directory whose
  fingerprint differs. A changed setting is a new run in a new directory.
- Methods compared on the same examples share one first proposal per example.
- An output cut off at the token limit, blocked by a content filter or refused
  is an attempt with no readable proposal: record it, score it wrong, repair it
  like any failed proposal, and count it. It is not "no call" and not a crash.
- Retry transport errors a bounded number of times with backoff, separately from
  the method's own repairs; keep retry waits out of latency.
- Stop on errors a retry cannot fix. Write a sanitized event (error type, HTTP
  status, request id, provider code; no payloads or keys). Saved rows stay.

## Long runs

Give long runs one command (a make target or script) that logs with timestamps
to a file, so the user can start it in their own terminal. Tell them the command,
the expected time and cost, and the log path. When a run stops, find the cause
from the log and the error events, fix it (payment, quota, a recorded route
change), and resume with the same settings. Ask for the end of the log when the
user reports it finished.

## Before reporting

Run `scripts/run_tools.py check RUN... --same <manifest keys>`:

- every expected row exists once, no foreign or other-configuration rows;
- error events are explained (and resumed rows did not repeat them);
- unreadable outputs and rows with unknown usage are counted, and costs say how
  unknown usage was handled;
- runs that will be compared share code, data, models, prompts and prices.

Regenerate summaries after the last row. Append a validation note: date, command,
wall time, cost, checks run, anomalies. Report results only from runs that pass.

## Hygiene

Keep results out of version control unless they are deliverables. Keep `.env`
out of the repository and credential fields in `.env.example` empty. A gateway
gets only its own subscription key; do not forward provider credentials through
it. State whether costs are list prices and whether gateway fees are included.

## Script

`scripts/run_tools.py` (Python 3.10+, standard library) reads run directories
(`manifest.json`, `records.jsonl`, `errors.jsonl`):

~~~sh
python3 scripts/run_tools.py check results/run1 results/run2 --same code_sha256 dataset_sha256 llm_model
python3 scripts/run_tools.py estimate results/pilot --rows 3051 --workers 8 \
  --usage input=proposal.usage.prompt_tokens --usage output=proposal.usage.completion_tokens \
  --usage 'verifier=verification.usage.input_tokens?' \
  --price input=0.05 --price output=0.40 --price verifier=0.042 \
  --latency proposal.latency_s --latency verification.latency_s
python3 -m unittest discover -s tests -v
~~~

A path ending in `?` counts as zero when absent (a verifier not called on every
attempt). When input tokens include cached tokens, price the cached count at
(cached price − input price) to avoid charging it twice.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.
