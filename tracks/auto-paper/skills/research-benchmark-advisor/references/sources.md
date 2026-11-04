# Sources, Fallback Chain and Browsing Guide

## 1. Primary discovery source

**Papers with Code tasks index:** `https://paperswithcode.co/tasks`

Use it to:
1. Enumerate top-level task categories and the subfields (tasks) under them.
2. Open individual task pages to list their benchmarks (dataset + metric).
3. Open benchmark pages to read the leaderboard: method, score, year,
   paper link, code link.
4. Follow paper and code links to the original source.

Read leaderboards as *data*: note the metric name, the split, whether extra
training data is flagged, and the date of the top entries. Record the
retrieval date for every page.

Caveats to check every run:
- Papers with Code mirrors have at times gone stale or offline. If the top
  entries are more than about 18 months old, cross-check with a web search
  for "<benchmark> state of the art <current year>" and with the official
  benchmark repository before quoting the leaderboard as current.
- A leaderboard entry is a *claim by the submitter*. Confirm the number in
  the linked paper before labeling it **Verified**.

## 2. Fallback chain (use in order when the primary is unavailable or thin)

1. **Official benchmark repositories and websites** (the dataset's own
   GitHub organization or project page; usually hosts the canonical
   leaderboard and evaluation script).
2. **Hugging Face**: `https://huggingface.co/datasets/<name>` for data and
   splits; `https://huggingface.co/spaces?search=leaderboard` and the Open
   LLM / MTEB / other community leaderboards for live rankings;
   `https://huggingface.co/papers` for recent papers with code.
3. **GitHub**: the baseline's official repo (check last commit, open issues
   about reproduction, presence of eval scripts, pretrained checkpoints).
   Also awesome-lists ("awesome-<subfield>") to enumerate methods.
4. **Original papers**: arXiv abstract pages and the PDF for tables;
   OpenReview for venue reviews that often discuss reproducibility.
5. **Secondary indexes**: Semantic Scholar, Google Scholar "cited by" on
   the benchmark paper (finds the latest methods), ACL Anthology, CVF
   Open Access, PMLR.
6. **Curated resource lists** (starting points, not exhaustive):
   - `https://huggingface.co/papers/trending`
   - `https://huggingface.co/spaces/mteb/leaderboard` (embeddings)
   - `https://www.openml.org` (tabular suites)
   - `https://robustbench.github.io` (robustness)
   - `https://wilds.stanford.edu` (distribution shift)
   - `https://github.com/Jingkang50/OpenOOD` (OOD detection)
   - `https://crfm.stanford.edu/helm` (holistic LLM eval)
   - `https://github.com/EleutherAI/lm-evaluation-harness`
   - `https://github.com/UKGovernmentBEIS/inspect_evals`

Report in section G which tier each fact came from.

## 3. Category list to browse (Broad Discovery Mode)

Browse at least five distinct categories. Pick them to cover accessibility,
compute range and the researcher's interests, but always include at least
two categories *outside* the stated interests. Examples (not a mandatory
shortlist; discover others on the site):

- Anomaly detection (industrial, time-series, graph, video)
- Data-centric AI: dataset pruning / selection, label-noise learning,
  data valuation, dataset distillation
- Representation learning / self-supervised learning (small-scale)
- Weakly supervised, semi-supervised, few-shot learning
- Dataset quality assessment, label-error detection
- Model calibration and uncertainty estimation
- Robustness: corruption, adversarial, spurious correlation
- Domain adaptation / domain generalization / test-time adaptation
- Out-of-distribution detection / open-set recognition
- Multi-agent learning, cooperative and communication benchmarks
- Multimodal learning (small VLM-free tasks where feasible)
- Tabular learning, time-series forecasting and classification
- Graph learning (node / graph classification, link prediction)
- Mechanistic interpretability benchmarks (circuit discovery, probing,
  SAE evaluation suites)
- AI safety evaluations: jailbreak / over-refusal, prompt-injection
  detection, deception probes, unlearning benchmarks
- Efficient inference: KV-cache compression, quantization, pruning
- Code generation and test generation
- Molecular property prediction, activity cliffs, materials
- Medical imaging small benchmarks (segmentation, classification)
- Audio / sound event detection, speech small tasks
- Continual learning, model merging, parameter-efficient fine-tuning

Record every category and task page visited, even those yielding nothing.

## 4. Benchmark screening fields (collect for every screened benchmark)

| Field | Where to find it |
| --- | --- |
| Benchmark name, task, metric(s) | PwC benchmark page / official site |
| Train/val/test splits documented? | dataset card, repo README |
| Dataset download: public? size? license? | HF dataset card, project page |
| Evaluation script public and maintained? | official repo |
| Top-1, top-2, top-3 method and score | leaderboard, confirmed in paper |
| Date of top entries; entries per year | leaderboard |
| Code for top methods? checkpoints? | repo links, HF hub |
| Compute of top methods (GPU type, hours) | paper experimental section |
| Saturation: top score within 1 point of max, or 99-100 %? | leaderboard |
| Protocol stability: multiple variants, extra-data flags, metric changes | leaderboard notes, benchmark paper |
| Proprietary API dependency? Live-web dependency? Human eval? | papers |

## 5. Tool guidance

- `WebFetch` first on exact URLs. Ask it for the leaderboard table rows
  (method, score, year, code link) explicitly in the prompt.
- `WebSearch` to find the official benchmark site, the newest papers
  ("<benchmark> 2026", "<benchmark> state of the art"), reproduction
  reports and GitHub issues ("<repo> reproduce results issue").
- Browser tools when a page is JavaScript-rendered (many leaderboard
  Spaces). Use `get_page_text`; take a screenshot only if text extraction
  fails.
- Batch independent fetches in one turn.
- If a page cannot be retrieved after two attempts, record the URL as
  "unretrievable on <date>" in section G and continue down the chain.

## 6. What "verified" means for each fact type

| Fact | Verified when |
| --- | --- |
| SOTA score | Read on the leaderboard **and** found in the paper's table (or the official repo README) under the same protocol. |
| Paper exists | arXiv / venue page opened; title, authors, year read. |
| Code available | Repo page opened; README describes training/eval for this benchmark; last commit date read. |
| Code functional | At least one of: recent commits; closed reproduction issues; third-party reproduction; a maintained harness includes it. "Repo exists" alone is **Inferred: functional**, not Verified. |
| Dataset available | Download page or HF card opened; license and size read. |
| Compute requirement | Stated in paper or README (GPU type, count, hours). Otherwise Inferred from model size and dataset size, stated as such. |
