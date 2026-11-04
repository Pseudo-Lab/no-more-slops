# Worked Example: Execution (E) × Hidden-State Probe (P) × Chain-of-Thought (C) Monitoring

This file shows the procedure in
[prior_work_novelty_sota_review.md](prior_work_novelty_sota_review.md).
It is a **process demonstration, not a reusable verdict**:
- every classification below is dated;
- every number is a snapshot of a past review;
- a new project on this topic must redo Stages 2–3 and re-verify every
  number from the primary source.

Case record:
- Source: the PseudoLabs project review `prior_work_review_RQ1_execution_probe_cot.md`
  (2026-10-09).
- Bibliographic identities re-verified 2026-10-12 against the arXiv API,
  the NeurIPS virtual site and OpenReview.
- No experiments were run, and none are implied here.

---

## Step 0. Operational definitions (§3.1)

Define each component by **what is computed, from which information**,
before searching:

| Component | Operational definition (the benchmark here is APPS-ControlArena code backdoors) |
|---|---|
| E: execution | The trusted model writes reference solutions and inputs. The submitted code runs in a sandbox. A *witness* is an input on which the submitted code disagrees with the references |
| P: probe | A linear probe on the **trusted** model's hidden states while it reads the problem and code (the attacker is closed, so attacker-side probes are impossible) |
| C | Ambiguous, so it is split in two. **C-u**: the untrusted model's reasoning trace. **C-m**: the monitor's own reasoning before it scores |

**Lesson.** "C" names two different signals. Searching only "CoT
monitoring" would have mixed them up.

## Step 1. Stage 1 rapid screening (fatal checks first)

These checks are cheap, and each one can kill subsets before any deep
search:

- **Dataset schema check (Q7).** The benchmark's released fields contain
  no reasoning traces (HF dataset schema; review Fact 1). So **C-u cannot
  be computed** on the benchmark. Every subset containing C-u is
  `NOT EVALUATED: not computable` under §3.3, and it fails SAME-TASK if
  new trajectories are generated.
- **Baseline protocol check.** The benchmark's own baseline monitor
  already reasons before scoring (Koran et al., App. B). So **C-m is
  already present in the baseline**. It is not a new signal.
- **Affordance check.** The original AI-control game limits the blue
  team to running test cases for one submitted solution (Greenblatt et
  al., §2). E expands that affordance. It is legitimate, but it must be
  declared under S3 (comparable resources).

## Step 2. Stage 2 discovery: sources, strategies and what each found

| Strategy | Example queries | Key finds |
|---|---|---|
| Q1 exact names | "execution monitor AI control", "activation probe monitor backdoor" | ObserverBench; Koran et al. |
| Q2 synonyms | "differential testing", "behavioral comparison", "white-box monitor" | Hackathon behavioural-comparison repo; Differential Prompting |
| Q3 components | E / P / C separately | See closest-work table |
| Q4 pairs | "probe + black-box monitor", "CoT + action monitor" | Black-to-White boosts; CoT Red-Handed hybrid; Hua et al. |
| Q5 triple | E+P+C | Nothing found. **That is not evidence of novelty** |
| Q6 other fields | "LLM reference + differential test" (software engineering) | Differential Prompting; CodeHacker; TestCase-Eval |
| Q7 same benchmark | "APPS backdoor monitor pAUC", "ControlArena" | Koran et al.; ObserverBench; *Decorrelation Is Not Complementarity* |
| Q8 recent / concurrent | arXiv by date (2026-05 to 2026-10), OpenReview workshops | Caught in the Act (2026-10-08); Trusted Debate (NeurIPS 2025 workshop) |

**Search-log entries that had to be recorded as UNREACHABLE:**
- the Google Scholar and Semantic Scholar APIs were not directly
  queryable (2026-10-09), so coverage came from web search plus arXiv
  full text;
- OpenReview returned a bot challenge or 403 on the forum, note and PDF
  routes for the Trusted Debate paper (2026-10-12). It was first recorded
  as **UNREADABLE**. The fallback ladder later recovered the full text
  (Step 7), and the paper is now FULL-TEXT.

## Step 3. Bibliographic verification of the named papers (2026-10-12)

| Named in the task as | Verified identity | First version | Venue | Link | Status |
|---|---|---|---|---|---|
| ObserverBench | *ObserverBench: Testing Mechanistic Estimates for Intervention and Control*. Vijay Erramilli | 2026-09-02 | Preprint (28 pp.; frozen artifact on Zenodo) | [arXiv:2609.03026](https://arxiv.org/abs/2609.03026) | VERIFIED |
| CoT Red-Handed | *CoT Red-Handed: Stress Testing Chain-of-Thought Monitoring*. Benjamin Arnav, Pablo Bernabeu-Pérez, Nathan Helm-Burger, Tim Kostolansky, et al. | 2025-05-29 (v3 read) | NeurIPS 2025 | [arXiv:2505.23575](https://arxiv.org/abs/2505.23575) | VERIFIED |
| Evading CoT Monitoring Through Model Poisoning | *Evading Chain-of-Thought Monitoring Through Model Poisoning*. Giorgio Severi, Shujaat Mirza, Blake Bullwinkel, Amanda Minnich | 2026-08-03 | Preprint (15 pp.) | [arXiv:2608.02820](https://arxiv.org/abs/2608.02820) | VERIFIED |
| Enhancing Monitoring in AI Control | *Enhancing Monitoring in AI Control through Trusted Debate*. Ghassan Al Dahik, Ruize Xu, Satvik Singh, Leon Kiunga, Pablo Bernabeu-Perez | 2025 (exact date not shown on the page) | NeurIPS 2025 Workshop on Socially Responsible and Trustworthy Foundation Models ("ResponsibleFM"; per the PDF footer and the OpenReview search API) | [NeurIPS page](https://neurips.cc/virtual/2025/133159); [OpenReview](https://openreview.net/forum?id=v2vZmV9kHm); [author page](https://pbernabeup.github.io/projects/trusted-debate/) | IDENTITY VERIFIED. **FULL-TEXT** via a Wayback snapshot of the primary OpenReview PDF URL (Step 7) |
| APPS-ControlArena monitoring (benchmark split) | *Ensemble Monitoring for AI Control: Diverse Signals Outweigh More Compute*. Eugene Koran, Yejun Yun, Samantha Tetef, Benjamin Arnav, et al. | 2026-05-14 (v1; v2 read) | Recorded as ICML 2026 in the case record (not re-verified 2026-10-12) | [arXiv:2605.15377](https://arxiv.org/abs/2605.15377) | VERIFIED (identity). Venue: Partial |
| (AI-control game) | *AI Control: Improving Safety Despite Intentional Subversion*. Ryan Greenblatt, Buck Shlegeris, Kshitij Sachan, Fabien Roger | 2023-12-12 | ICML 2024 (version on OpenReview) | [arXiv:2312.06942](https://arxiv.org/abs/2312.06942) | VERIFIED |

**Bibliographic corrections:**
1. The case record dated Koran et al. "18 May 2026". The arXiv API gives
   the first version as **2026-05-14**.
2. The case record could not find "Enhancing Monitoring in AI Control".
   It is the Trusted Debate workshop paper above.

Both corrections are examples of what the "Bibliographic corrections"
section of an Evidence Report records.

**How the Trusted Debate paper affects the analysis:**
- Debate is a monitor-side reasoning protocol, so it belongs to the
  **C-m** family.
- Initially its full text was UNREADABLE. The C-m "debate" sub-claim was
  therefore held at UNCERTAIN, as the rules require, rather than assumed.
- Step 7 below shows how the regression test resolved it from the full
  text.

## Step 4. Combination analysis (§3), snapshot as of 2026-10-09/12

All numbers below are quoted from the case record. **Re-verify them
before reuse.**

| Subset | Three closest prior works | Equivalent method exists? | Comparable benchmark evaluation? | Strongest comparable baseline | Exact difference | Classification → gate | Decision |
|---|---|---|---|---|---|---|---|
| E | Koran et al. (Exploit-Finder / Reference-Compare, *by reading*); hackathon behavioural comparison (LLM-simulated, nothing executed); Differential Prompting / CodeHacker (software engineering) | The mechanism exists in software engineering. As a trusted control monitor, not found | No (reading-only analogues) | Same-model reader 0.228 pAUC@10%FPR (8B); overall 0.816 ensemble (Koran, Table 1) | Real execution as a ranking signal under an adversarial attacker on the standard split | PARTIAL OVERLAP → PASS only if P1–P5 hold *and* the "untested here" rule passes (adversarial attacker, affordance declared) | REVISE: secondary, scoped claim |
| P | ObserverBench (AUROC 0.979 / 0.983, Tables 12 and 18); Wiryadi code-security probes; Caught in the Act | **Yes** (ObserverBench, same dataset family) | Yes (same family); UNMEASURED on the held-out-attacker split | ObserverBench recipe | Split and attacker shift only | ALREADY STUDIED → FAIL-SUBSTANTIALLY-ANSWERED *as a contribution* | NO-GO as a contribution; **essential baseline** |
| C (C-u) | CoT Red-Handed (hybrid ROC-AUC 0.797, Fig. 8); Arike et al. EaE; Severi et al. poisoning | Yes (other benchmarks) | Not computable here (Step 1) | Hybrid 0.797 (BigCodeBench) | — | ALREADY STUDIED | NO-GO |
| C (C-m) | Koran baseline reasoning (App. B); Trusted Debate (FULL-TEXT: GPT-4o prosecutor, defendant and judge, all reading-only, on APPS Control Tax in ControlArena; §3–5); *Bootstrapped Monitoring* | Yes: monitor-side reasoning, both single-pass and multi-agent debate | Comparable family (APPS backdoors via ControlArena), but a different dataset, split and metric (detection rate at a 5% audit budget vs pAUC@10%FPR) | The Koran baseline on the split. Debate is UNMEASURED there | None for C-m alone | ALREADY STUDIED. The debate sub-claim moved from UNCERTAIN to verified (Step 7) | NO-GO |
| E+P | ObserverBench + Koran score ensembles + Hua et al. cost-constrained combination; *Decorrelation Is Not Complementarity* (gain shrinks as members strengthen, §3.5) | Not found | No | P on this split: UNMEASURED; 0.816 overall | A behavioural signal combined with a representational one, with a **complementarity argument**: E fails without a reference or trigger, P fails under representation or attacker shift | PARTIAL OVERLAP; S1 PARTIAL while P is UNMEASURED | REVISE; GO only after the P measurement gate |
| E+C | Hackathon interrogation; CoT Red-Handed hybrid; Severi et al. (trace–output consistency) | Not found | Not computable (C-u) | None comparable | — | UNCERTAIN → FAIL-UNVERIFIED (also fails SAME-TASK) | NO-GO |
| P+C | Black-to-White boosts (on its Backdoors set, the white-box-assisted monitor is *worse*: 0.776 vs 0.899); McKenzie et al. cascades; Hua et al. | Yes (deception settings) | Not computable (C-u); with C-m it reduces to probe + reader | 0.899 black-box (their Backdoors set) | — | ALREADY STUDIED | NO-GO |
| E+P+C | None found | — | Not computable | — | — | UNCERTAIN ("nothing found" ≠ NOVEL) | NO-GO (also infeasible in 4 days) |

## Step 5. What the downstream skills do with this

**research-readiness-advisor:**
- **S1:** the strongest *applicable* baseline for any E+P claim is P
  (ObserverBench recipe), and it is UNMEASURED on the split. So S1 is
  PARTIAL under the §4d.1 maturity audit, and SOTA potential is below
  MEDIUM until P is measured.
- **S2:** for E+P, *lever evidence* that each signal works separately is
  not enough. The S2 case rests on complementarity: the two signals have
  different documented failure causes. *Decorrelation Is Not
  Complementarity* is recorded as redundancy counter-evidence, which caps
  S2 at PARTIAL.
- **Expected margin vs MDE:** the case record estimates the MDE at about
  0.075 pAUC with 172 positives. The expected E+P gain over a strong P
  (about 0.02–0.08) is at or below the MDE, so S3 is at most PARTIAL
  (§4d.5).
- **Technical depth:** the E+P core is a new signal (execution
  witnesses) plus a complementarity hypothesis. It is not voting or
  averaging. It passes only if the combination rule is principled (e.g.
  witness-first ranking) and the design includes the per-item
  complementarity diagnostic.

**research-planner:**
- **Expected contribution:** B (combination benefit) if P lands below
  about 0.9; otherwise C/D. A is claimed only if E+P beats both 0.816 and
  P by at least the SESOI.
- **Decision:** REVISE, with a pre-registered P-measurement gate. The P
  measurement is an experiment and needs the user's permission.

**research-pipeline (evidence gate):**
- Checks 1–5 pass for E+P, provided the Evidence Report reaches FINAL.
- Check 7 (SOTA potential ≥ MEDIUM) **fails** until P is measured. No GO
  is issued, and the candidate is routed to redesign or to the
  measurement gate.

## Step 6. General lessons (these, not the verdicts, are what to reuse)

1. Define components operationally. One word can name two signals.
2. Check whether each signal is **computable on the benchmark** before
   doing deep literature work. The schema killed four subsets.
3. A combination counts only with a documented complementarity argument.
   Record redundancy counter-evidence explicitly.
4. The strongest *applicable* baseline may be a published method for one
   of your own components (here P). That can turn "novel combination"
   into "below MEDIUM until measured".
5. "Nothing found" for a higher-order combination is UNCERTAIN, never
   NOVEL.
6. Verify bibliographic identity. Two citations in the case record
   needed correction.
7. When the primary route is blocked, work down the full-text ladder
   before settling for UNCERTAIN, and keep UNCERTAIN until a legitimate
   route succeeds (Step 7).

## Step 7. Regression test of the fallback procedure (2026-10-12)

This step re-runs the access check (§2a-1) and the full-text ladder
(§2a-2) on the one paper that had stayed UNREADABLE.

**Source access table** (one known-answer probe per route, 2026-10-12).
This is a snapshot only; re-probe every session:

| Source / route | Status | Note |
|---|---|---|
| arXiv API | RATE-LIMITED, then WORKING | 429 on the first call; 200 on retry after backoff |
| arXiv abs / HTML full text | WORKING | |
| Semantic Scholar search and paper API | RATE-LIMITED | 429 persisted through 3 backoff retries (no API key). One citations call returned 200 |
| OpenAlex works search | WORKING | Returned the probe paper |
| Crossref | WORKING | Metadata only |
| DBLP | WORKING (HTTP 200) | Did not return the probe title; not relied on for discovery here |
| CORE (no key) | WORKING | Returned the probe paper |
| Google Scholar (web) | WORKING this session | Returned the paper; opportunistic only, never bulk-queried |
| OpenReview search API (`api2 …/notes/search`) | WORKING | Returned the paper's metadata, abstract and PDF path |
| OpenReview forum, notes-by-id, `pdf?id=`, hashed PDF path | BLOCKED | Challenge or 403 |
| NeurIPS virtual site | WORKING | Metadata and abstract |
| GitHub search API | WORKING | |
| Internet Archive (Wayback) | WORKING | Snapshot of the primary PDF URL available |

**Full-text ladder for "Enhancing Monitoring in AI Control through Trusted
Debate":**

| Rung | Result |
|---|---|
| arXiv (title search) | No arXiv version found |
| OpenReview PDF (`pdf?id=v2vZmV9kHm`, attachment route, hashed `/pdf/2b61…ecff.pdf`) | BLOCKED (403) |
| OpenAlex (title search, then open-access locations) | The paper was not among the top results of an exact-title search (the only match was the query echo), so there were no locations to follow |
| Author page ([pbernabeup.github.io](https://pbernabeup.github.io/projects/trusted-debate/)) | Abstract and BibTeX. Its "PDF" link points to the same hashed OpenReview PDF |
| Venue page (NeurIPS virtual) | Abstract only |
| Wayback snapshot of the hashed OpenReview PDF (timestamp 20260518055333) | **Success.** PDF 1.5, 3,495,777 bytes, sha256 prefix `949ac764f195fbcf`. Title, all five authors and the footer "NeurIPS 2025 Workshop: ResponsibleFM" match the verified identity |

**Claims verified from the full text (FULL-TEXT level):**

- **Method (§3.1).** Three trusted agents, all initialised from the same
  trusted model:
  - a prosecutor;
  - a defendant;
  - a judge, who reads the transcript and outputs a 0–100 suspicion
    score.

  There are R = 2 rounds. All agents **read** the code. Nothing is
  executed, there is no hidden-state probe, and the untrusted model's
  chain of thought is not used. The paper also tests a single-stance
  "trusted consultancy" variant (§3.2).
- **Setting (§4.1).** ControlArena, with APPS problems and backdoors from
  the APPS Control Tax dataset (Terekhov et al., 2025). The trusted model
  is GPT-4o. Attack trajectories come from an existing dataset; no
  adaptive attacker targets debate (§6.1).
- **Metric and results (§4.2, §5.2, Fig. 4).** "Safety" is the detection
  rate at an audit-budget threshold (5% FPR on honest samples):
  - debate 0.737 ± 0.017;
  - trusted monitoring 0.639 ± 0.019;
  - consultancy 0.220 ± 0.019.

  Debate scores are bimodal, and its advantage disappears at stricter
  budgets (§5.2, Fig. 5). It costs about 11.9k tokens per sample, against
  about 5.5k for monitoring (§6.1).

**Effect on the E/P/C classifications:**

| Item | Before | After | Decision change? |
|---|---|---|---|
| C-m debate sub-claim | UNCERTAIN (UNREADABLE) | Verified: multi-agent monitor-side reasoning is already studied on a comparable APPS-backdoor setting, with a different dataset, split and metric | No (C-m stays NO-GO) |
| E (execution) overlap | PARTIAL OVERLAP | Unchanged. Trusted Debate confirms that reading-only "argue about triggers" monitors exist, and that they do not execute code | No |
| E's strongest-baseline map (S1 maturity audit, §4d.1) | — | **New entry.** Debate is a stronger *reading* protocol than single trusted monitoring on APPS Control Tax with GPT-4o. It is UNMEASURED on the Koran split. It does not apply to a ≤ 13B open-model comparison class, but it must be listed in the mature baseline map for any claim made against GPT-4o-class readers | No (S1 for the label-free ≤ 13B class is unchanged) |

**What this test shows about the procedure:**
- The fallback ladder turned an UNCERTAIN item into a verified one by a
  legitimate route. The classification was held at UNCERTAIN until then.
- Verification also surfaced a baseline-map entry that the abstract
  alone did not reveal: a different dataset and metric, a stronger
  reading protocol, and a higher token cost.
- It does **not** show that coverage is complete. Semantic Scholar was
  rate-limited throughout, and OpenAlex did not return this workshop
  paper.
