# Audit checklist

Mismatches found in real audits of LLM-pipeline papers, by area. Use it to plan
the inventory; not every item applies to every paper.

## Method

- A check defined in the Method (for example a schema check `S(c)`) has a
  different scope in code (readability only, or also types and required fields).
- An ablation differs from the main method in more than the ablated part: other
  feedback wording, field order, or instructions.
- Edge cases the text does not cover: no tools available, an empty or unreadable
  output, a missing argument, a "no call" decision.
- The algorithm's return value or stopping rule differs from the code's.
- Thresholds, limits or defaults in the text differ from the run's manifest.

## Data and labels

- Counts per category differ from the prepared data, or the revision is not pinned.
- Reference answers contain conflicts or errors that some methods cannot satisfy;
  document them rather than silently dropping cases.
- Labels or category names reach a model's prompt.

## Metrics and statistics

- A total excludes a category (for example presence-only labels) without saying so.
- Percentages over different denominators (examples, records, attempts) are compared.
- Retry waits are counted as latency; a shared first call is charged to one method only.
- Intervals ignore pairing or treat repeated runs as independent examples.
- "In every run", "highest" or "mostly by" claims are not checked per run or decomposed.

## Results

- A table and the text round the same value differently.
- The same quantity differs across tables, figures, abstract and README.
- Results come from runs with different code, data, prompts or prices.
- A result was produced by a code path that has since changed.

## Reporting

- Costs omit gateway fees or cached-token pricing without saying so.
- Model names in text differ from the snapshot the API returned.
- Post hoc choices (limits, thresholds, rules chosen after seeing results) are
  presented as fixed in advance.
