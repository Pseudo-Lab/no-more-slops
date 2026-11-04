---
name: paper-code-audit
description: Audit an empirical paper against the code, data and run records that produce it. Use when asked whether a manuscript matches its implementation and results - before submission, after a protocol change or new runs - to inventory claims and settings, trace each to code or records, recompute every number, run the tests and build, re-verify findings, and fix only within the agreed scope.
---

# Paper–code audit

A paper can build, pass its tests and still describe a different method, data
set or number than the code produced. Check what the paper says against what the
code does and what the records contain. Read only, unless fixes are requested.

## Ground rules

- The manuscript, the code path the paper's runs used and the run records are the
  evidence. A summary file, a log line or the author's memory is a lead to check.
- Sections the author froze or approved change only with explicit approval;
  propose exact replacement wording instead.
- Report what was verified separately from what could not be; never mark an item
  verified because nothing contradicted it.
- Do not edit results, records or expected outputs to make a check pass.

## 1. Inventory the paper

Read the whole manuscript, including captions, footnotes, the algorithm and the
abstract. List each checkable item with its location, using
[the checklist](references/checklist.md):

- method steps, equations, defaults and limits as stated;
- data: source, revision, counts, categories, splits, filters, exclusions;
- metrics: definitions, denominators, excluded cases, rounding;
- models and settings: snapshots, prompts, decoding, thresholds, routes;
- statistics: runs, seeds, resamples, pairing, interval type;
- costs and times: what is included, prices;
- every number (`scripts/extract_numbers.py paper.tex`), and every qualitative
  claim ("highest", "in every run", "mostly by", "never").

## 2. Trace each item to the implementation

Follow the entry point the paper's runs used (command, config, defaults,
overrides) to the code that does the work. Check the run manifests record the
value the paper states. Watch for a default that differs from the run's flag,
an ablation whose prompt or feedback differs from the main method in more than
the ablated part, a metric whose code excludes or includes cases the text does
not mention, and dead code that matches the text while another path ran.

## 3. Recompute the numbers

Recompute from records, not from cached summaries when possible, with the
paper's denominators and rounding. Check text against tables, the abstract
against the body, overlapping cells across tables and figures, per-run claims
run by run, and decomposition claims ("mostly by X") with counts. Recheck
companion documents (README, slides) the same way: `extract_numbers.py
README.md --compare paper.tex` lists numbers the paper does not state.

## 4. Run what exists

Run the test suite, linters, the data check and the paper build with the
project's own commands. Record each command and its result. Check page budget
and rendered pages if the venue has limits.

## 5. Re-verify, then report

Before reporting a finding, try to refute it: reread the code path, rerun the
recomputation, check the record. Then report with
[the template](references/report-template.md): severity, location, what the
paper says, what the evidence shows, the proposed fix. Close with what was run
and what remains unverified. Order by severity: wrong numbers and method
mismatches first, then undocumented deviations, ambiguities and style.

## 6. Fix when asked

Make the smallest change that resolves each finding. Add or update a test for
each code fix. Rebuild the paper, rerun the checks that failed, and record the
change in the project's validation log. If a fix changes what a run would do,
earlier runs no longer match the code: say which results need a rerun.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.
