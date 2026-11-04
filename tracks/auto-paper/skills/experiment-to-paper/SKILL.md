---
name: experiment-to-paper
description: Draft papers from completed results with checked evidence.
version: 0.2.1
license: MIT
metadata:
  hermes:
    tags: [research, paper, evidence]
---

# Experiment to Paper

## When to use

Use when saved experiment results need a manuscript, revision or evidence audit.

Inspect the requested format, evaluation code and completed result artifacts. Record the input revision and file hashes. Saved results do not prove the current revision generated them or that inference was reproduced. Preserve the user's language, venue and output choices.

## Connect results to claims

Create an evidence index with measurements, units, denominators, source files/selectors and missing values. The bundled [exporter script](scripts/export_evidence.py), used according to [evidence-schema.md](references/evidence-schema.md), transcribes explicitly selected values from any project's saved JSON and hashes the inputs; it does not recompute metrics. When item-level data is available, separately recompute aggregates using the actual evaluation rules.

Try the invented [example results](assets/example/results.json) with the [export specification](assets/example/export-spec.json) before adapting selectors to real results. These files demonstrate measured zero versus unavailable data.

For each main claim, record the sentence, measurement or original-source citation, comparator conditions, limitations and status (`observed`, `interpretation`, `unverified`). Keep missing values distinct from measured zero. Separate detection AP from supplied-box candidate-selection accuracy; shared boxes alone do not establish identical proposals or scoring.

Check backbone, training, proposal selection, crop/context, resolution, calibration, matching and metric before interpreting a comparison. Distinguish frozen pretrained encoders, newly trained heads or embeddings, checkpoint continuation and hyperparameter search. Training-seed variation and image-sampling uncertainty are different. Dependent queries from one image need an image-level sampling unit for a bootstrap; nonsignificance does not prove equivalence.

## Write and review

Draft from the evidence index. Verify substantive literature claims against original sections/tables; valid bibliography metadata does not establish support. Other writing or citation skills may help when available, but this workflow requires no particular agent host, profile or citation tool.

Use the requested format and include an experiment log, claim-evidence record and unresolved checks. Default names such as `manuscript.md` and `claim_evidence.md` may be adapted. Generate figures from identified measurements or qualitative inputs with scope and provenance. Follow repository acknowledgement requirements.

Read [internal-review.md](references/internal-review.md) for author-side content checks. The sibling `paper-review-local` skill supplies deterministic structure, hash, LaTeX, PDF and supplied-text overlap checks. If unavailable, record equivalent checks or their absence. Self-review, independent peer review and an editorial decision are separate outcomes.

Revise within the user's scope and use a bounded budget appropriate to the task (two rounds is a useful starting point). Record unresolved experiments or novelty questions instead of launching an indefinite loop. Delegation follows the user's authorization.

## Verification and handoff

When a PDF is requested, compile its actual sources, inspect page count and actual rendered pages, and report the chosen format. Successful compilation alone does not establish layout quality. Distinguish document rebuilds from experiment reproduction and static checks from scientific validation. Report missing authorship, rights, independent review or venue checks when relevant to submission.

Writing from saved artifacts does not itself authorize new experiments, provider uploads, bot assignments or submission. Existing user authorization remains applicable.

## Pitfalls

Snapshot hashes certify saved inputs, not scientific validity. Preserve null instead of reporting zero; distinguish provided-box selection from full detection; inspect original passages rather than trusting bibliography-key validation.

Version 0.2.1 declares the Hermes frontmatter version and directly links runtime files for URL installation.
