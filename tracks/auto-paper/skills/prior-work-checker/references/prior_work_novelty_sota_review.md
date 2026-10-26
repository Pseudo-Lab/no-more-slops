# Prior-Work, Novelty and SOTA-Evidence Review (shared procedure)

**Owner:** prior-work-checker. Only prior-work-checker issues the novelty
classification and the novelty gate (PASS / FAIL). Other skills read this
file. They consume the Evidence Report it defines, but they do not run
their own literature reviews or issue novelty verdicts.

**Read by:**
- research-readiness-advisor: SOTA potential S1–S4, novelty strength,
  technical depth and negative-result item 6;
- research-planner: the comparison matrix and final selection;
- research-pipeline: the pre-implementation evidence gate;
- benchmark-finder: the archive collision verdict maps onto §6 below.

**Shared definitions:**
[research_design_principles.md](../../research-pipeline/references/research_design_principles.md)
defines technical depth (§3), SOTA potential S1–S4 and its evidence
rules (§4b, §4d), the defensible-contribution test (§4e), feasibility
(§5), redesign (§6), the mandatory gates (§7) and ranking (§8). If this
file and that one differ, that file wins, unless following it would
weaken a gate.

**Worked example:** [worked_example_epc_monitoring.md](worked_example_epc_monitoring.md)
(Execution × Probe × CoT monitoring). It shows the procedure. Its
conclusions are dated and are not reusable verdicts.

This procedure is planning methodology. It never counts as evidence for
a gap, a novelty claim or a result.

---

## 1. Staged investigation (fits the four-working-day constraint)

Literature work is part of the planning budget. Run the stages in order.
Stop early on any clearly fatal finding. Do not spend Stage 2 effort on
a candidate that has already failed Stage 1.

| Stage | Applies to | Goal | Typical effort (agent time) | Output |
|---|---|---|---|---|
| **1. Rapid screening** | Every candidate (benchmark-screening stage, shared definitions §1c "early kill check") | Find obvious collisions, a stronger existing method that already solves the problem, an untraceable baseline, or a fatal feasibility constraint | One pass of query strategies Q1, Q2 and Q7 (§2b); read abstracts and results tables only | KILL (with reason) / CONTINUE |
| **2. Focused investigation** | Shortlisted candidates (≤ 3 per run, plus regenerated ones) | Full discovery (§2), combination analysis (§3), the three closest papers (§4), strongest baseline and its failure modes | All Q1–Q9; open and read the closest papers | Evidence Report, status DRAFT (§7) |
| **3. Final verification** | The candidate(s) about to receive GO, and qualifying backups | Re-verify from primary sources: the strongest baseline number, the novelty classification, the improvement mechanism's cause evidence, and evaluation feasibility. Re-check for work posted since Stage 2 | Targeted re-reads; a recency search (Q8) | Evidence Report, status FINAL; novelty gate PASS / FAIL |

Rules:
- Never lower Stage 3 standards so that a promising candidate passes. If
  Stage 3 cannot be finished, the report stays DRAFT and the candidate
  cannot be GO.
- The human time for verifying the Evidence Report (reading the cited
  sections of the closest papers and checking the baseline number) is
  part of the project's "Understanding / reading" phase. compute-planner
  estimates it inside D. The report exists so that this reading stays
  small; it is never counted twice.

---

## 2. Mandatory literature discovery (Stages 2–3)

### 2a. Sources

Search each of these. Record every source in the search log, including
the ones you could not reach.

| Source | Typical use |
|---|---|
| arXiv (listing, full-text HTML/PDF, API) | Preprints, versions and dates |
| Google Scholar | "Cited by", variant titles |
| OpenReview | Venue submissions, workshop papers, reviews |
| Semantic Scholar | Citation graph, references, follow-ups |
| GitHub (official repos, issues, forks, hackathon repos) | Unpublished methods, released outputs, whether something was actually executed or only described |
| Published proceedings (ACL Anthology, PMLR, NeurIPS/ICLR/ICML pages) | Final versions and venues |
| Citation networks | Forward and backward citations of the closest papers, and of the benchmark paper |
| Field-specific venues (e.g. LessWrong / Alignment Forum for AI safety; leaderboards; Papers with Code) | Informal but often first reports |

**Inaccessible sources.** If a source cannot be reached (a bot challenge,
an API error, a paywall, missing full text), record it as `UNREACHABLE:
<source> — <reason>` in the log. If an affected paper is a closest-work
candidate, mark that paper UNREADABLE. A failed retrieval is **never**
evidence of novelty.

### 2a-1. Source access check (start of each Stage 2 or Stage 3 session)

Do not assume any service is reachable. Before relying on a source, send
it one known-answer probe: a search for a paper you know exists (e.g.
the benchmark paper's exact title). Record the result in the Evidence
Report's Source access table (§7):

| Status | Meaning | Action |
|---|---|---|
| WORKING | HTTP 200 and the known paper is returned | Use the source |
| RATE-LIMITED | HTTP 429 or a quota message | Retry with backoff (≥ 3 s between calls; about 10 s, 20 s, 30 s on retries; at most 3 retries). If it still fails, use the fallback |
| BLOCKED | Bot challenge, captcha, or HTTP 403 on this route | Do not try to get around the block. Use another route from §2a-2 |
| NOT TESTED | Not probed in this session | Must not be listed as "searched" |

Access status changes over time and between routes on the same host.
For example, on 2026-10-12 OpenReview's search API worked while its
forum, note and PDF routes returned 403. Re-probe every session. Never
copy access status from an earlier report.

### 2a-2. Fallback ladders (by function)

For each function, go down the ladder until one route works. Log every
rung you try. Use legitimate routes only: never shadow libraries,
paywall circumvention, captcha solving or credential use. The routes are
API or web endpoints reached with the agent's web tools or `curl`. The
web-search tool is a discovery aid only, never a verification source.

| Function | Ladder (in order) |
|---|---|
| **Keyword discovery** | OpenAlex works search (no key) → arXiv API → Semantic Scholar API (often rate-limited without a key) → OpenReview search API (`api2.openreview.net/notes/search`) → DBLP → Crossref (metadata) → CORE → GitHub search API → web-search tool → Google Scholar (when it returns results; never bulk-queried) |
| **Identity and metadata** (title, authors, first-version date, venue) | arXiv API or abs page → OpenReview search API → publisher or proceedings page (NeurIPS / PMLR / ACL Anthology / journal) → Crossref / DBLP → OpenAlex → author or institutional page |
| **Backward citations** | The paper's own reference list (from the full text) → OpenAlex `referenced_works` → Semantic Scholar references |
| **Forward citations** | OpenAlex `filter=cites:<id>` → Semantic Scholar citations endpoint → Google Scholar "Cited by" (when accessible) → web search for the arXiv ID or exact title |
| **Full text** | arXiv HTML / PDF → venue PDF (OpenReview / proceedings / publisher) → the open-access locations OpenAlex lists → the author's or institution's page and its links → CORE → an Internet Archive (Wayback) snapshot of the **same** primary URL → the official code repository (README or paper copy) |

If every rung of the full-text ladder fails, the paper is UNREADABLE.
Stop there; do not keep searching indefinitely (§1 budget). Unpaywall
needs a contact email. Use it only if the user supplies one for that
purpose.

**Archived copies.** A Wayback snapshot counts as full text only if all
three hold:
- the snapshot URL is the primary source's own URL, for example the
  OpenReview PDF path linked from the venue or the author's page;
- the title, authors and venue footer match the verified identity;
- you record the snapshot timestamp and a hash of the file.

An archived copy may be an older version. If a newer version exists,
record that too.

### 2a-3. Verification levels (for every paper in the ledger)

| Level | Basis | What it can support |
|---|---|---|
| **FULL-TEXT** | Methods, setup and results sections read from a primary copy, or from a verified archived copy of the primary URL | Every judgement: overlap degree, methodological difference, numbers |
| **ABSTRACT-ONLY** | Abstract or project-page summary only | That the paper is *related* and must be read. RELATED-DIFFERENT only when the abstract shows a different task or signal outright. **Never** "methodologically different", NOVEL, or the absence of overlap |
| **METADATA-ONLY** | Title, authors, venue, date | Identity, and that it exists. Nothing about the method |
| **SECONDARY** | A blog, survey, citation context or search snippet | A lead only |

Rules:
- Every one of the three closest papers, every paper whose abstract
  suggests IDENTICAL or SUBSTANTIALLY EQUIVALENT overlap, and the source
  of the strongest baseline number must be FULL-TEXT. Otherwise the paper
  is UNREADABLE, P4 fails, the result is FAIL-UNVERIFIED and the
  classification is UNCERTAIN. The existing gate is unchanged.
- Never infer methodological novelty from an abstract.
- For each paper below FULL-TEXT, list the specific claims that remain
  unverified, e.g. "uses execution? unknown", "evaluated on split X?
  unknown".

### 2a-4. Budget (keeps the four-working-day constraint)

Spend reading effort where it can change the decision:

| Stage | Full-text reading | Fallback ladder |
|---|---|---|
| 1 | None, unless an abstract suggests a collision; then read only that paper | Discovery rungs only |
| 2 | The three closest papers, the strongest-baseline source, and any suspected IDENTICAL or SUBSTANTIALLY EQUIVALENT paper. Every other paper may stay ABSTRACT-ONLY if its relevance is recorded as RELATED-DIFFERENT or BACKGROUND | All full-text rungs, each tried once (plus one backoff retry), for the papers listed |
| 3 | Re-check only the decision-critical facts, and search for new papers | Only for facts that are still unverified |

Never cut the Stage 3 checks for a GO candidate to save time.

### 2b. Query strategies

Use every strategy and log the exact queries.

| ID | Strategy | Example (E/P/C case) |
|---|---|---|
| Q1 | Exact method names | "execution-based monitor", "activation probe monitor" |
| Q2 | Synonyms and alternative terminology | "differential testing", "behavioral comparison", "white-box monitor", "linear probe" |
| Q3 | Each methodological component on its own | E; P; C |
| Q4 | Pairwise combinations | E+P, E+C, P+C |
| Q5 | Higher-order combinations | E+P+C |
| Q6 | The same mechanism under different framing, including other fields (e.g. software engineering, security, classical ML) | "LLM-generated reference + differential test" in software engineering |
| Q7 | Comparable benchmark evaluations: the same benchmark, its family, or the same metric | "APPS backdoor" + monitor; "ControlArena" + pAUC |
| Q8 | Recent and concurrent work (last ~6 months, including workshops and preprints posted after the benchmark) | Date-sorted arXiv listing; OpenReview for the current cycle |
| Q9 | Citation trace: backward (references) and forward (citing works) of the benchmark paper and of each of the three closest papers, via the §2a-2 ladders | The references and citing works of ObserverBench and of Koran et al. |

These extend prior-work-checker's existing N1–N5 searches. They do not
replace them: N1–N5 stay mandatory and are still recorded separately.

**Completeness checklist.** Each required search maps to one existing
strategy, so nothing is duplicated. The Evidence Report records each row
as DONE, or NOT DONE with the reason:

| Required search | Covered by |
|---|---|
| Exact paper titles (identity check for every cited paper) | Q1 + §2c |
| Methodological synonyms | Q2, N2 |
| Equivalent experimental designs | N4 (an experiment that answers the question under another framing) + Q6 |
| Individual components | Q3 |
| Previously studied combinations | Q4, Q5 (§3) |
| Closest competing methods | N5, Q7 |
| Backward citations | Q9 |
| Forward citations | Q9 |
| Recent preprints and concurrent work | Q8 |

**Hit counts are not coverage.** The number of results, sources or
queries never shows that a search was complete. Coverage is supported
only by the checklist above, the Source access table, and the
verification levels of the decision-relevant papers.

### 2c. Primary-source verification

- Open and read every closest-work candidate and every paper that
  supplies a number. A snippet, abstract summary or citation context is
  not enough. This is prior-work-checker P4. "Read" means verification
  level FULL-TEXT (§2a-3), obtained through the §2a-2 full-text ladder.
- Quote every number with its table, figure or section, and its version
  (e.g. arXiv v2).
- Verify bibliographic identity: exact title, authors, first-version date,
  venue, and a working link. Record any correction to an earlier citation
  (wrong date, wrong title).

---

## 3. Systematic combination analysis

When a proposal combines k methodological components:

1. **List the components.** Define each one operationally, in terms of
   what is computed and from which information. This matters because
   two papers can use the same word for different signals. Example: "C"
   might mean the untrusted model's chain of thought or the monitor's own
   reasoning.
2. **Enumerate the 2^k − 1 non-empty subsets.** For each subset, record
   the closest prior work, whether it has been studied, and whether it
   can be evaluated on the proposed benchmark.
3. **Prune scientifically irrelevant subsets, and show your reasons.** A
   subset may be marked `NOT EVALUATED — <reason>` without a search when
   it:
   - cannot be computed on the benchmark (e.g. the benchmark lacks the
     required inputs; cite the dataset schema);
   - is strictly dominated by a superset already established; or
   - is outside the research question.

   For k ≥ 4, search all singletons and pairs. Search higher-order
   subsets only when the proposal uses them.
4. **Studied components do not make a novel combination.** Combining
   studied components counts as a contribution only if a
   **complementarity argument** is present: the components fail on
   different, documented causes, so their combination targets a failure
   that neither addresses alone. Without that argument, the combination
   is classified at best PARTIAL OVERLAP. Its gap is then of type "new
   combination of known methods", and the technical-depth gate
   (shared definitions §3: "a new combination of existing outputs with
   no new signal or hypothesis") is flagged for the advisor.
5. **Record redundancy evidence.** Record any published evidence that
   the signals are correlated, or that combination gains shrink as the
   components get stronger. That evidence feeds S2 (§8).

---

## 4. Closest prior work (three per serious candidate)

For each of the three closest papers (fewer only when fewer exist, with
the reason stated), record:

| Field | Content |
|---|---|
| Title | Exact title |
| Authors | Full list, or the first author plus "et al." with the count |
| Date | Date of the first public version, plus the version read |
| Venue | Conference, workshop, journal or "preprint" |
| Link | A direct link to the source that was read |
| Relevant location | Sections, tables or figures |
| Methodological similarity | What is the same, operationally |
| Benchmark and protocol | Dataset, split, metric, threat model and access class |
| Reported performance | Numbers with their location; `NR` if not reported |
| Exact differences | What the proposal does that this paper does not, and the reverse |
| Overlap degree | IDENTICAL / SUBSTANTIALLY EQUIVALENT / PARTIAL / RELATED-DIFFERENT |
| Read status | READ (= FULL-TEXT, §2a-3; give the route used) / UNREADABLE (with the ladder rungs tried and the claims that remain unverified) |

The overlap degrees map one-to-one onto prior-work-checker's existing
overlap classes:

| Overlap degree (this file) | prior-work-checker Step 3 class |
|---|---|
| IDENTICAL | SAME COMPARISON |
| SUBSTANTIALLY EQUIVALENT | FUNCTIONALLY EQUIVALENT or SUBSTANTIALLY ANSWERED |
| PARTIAL | PARTIAL |
| RELATED-DIFFERENT | BACKGROUND |

Never fabricate a reference, a number or a methodological detail. If a
detail cannot be verified, write `UNVERIFIED`.

---

## 5. Novelty classification

Assign exactly one classification to the candidate's **contribution**,
meaning the method on its question and setting, not just the method's
name.

| Classification | Definition |
|---|---|
| **NOVEL** | The Stage 2–3 search was complete, with every closest paper READ. A meaningful methodological contribution is identified: a mechanism, signal or hypothesis that is not present in prior work. No IDENTICAL or SUBSTANTIALLY EQUIVALENT work was found. "Nothing found" alone never earns NOVEL. A positive description of what is new is required |
| **PARTIAL OVERLAP** | Related work exists (PARTIAL rows), but a specific, defensible gap remains. Prior results do **not** let a reader predict the answer |
| **ALREADY STUDIED** | At least one IDENTICAL or SUBSTANTIALLY EQUIVALENT work exists, including a substantially equivalent method on another benchmark whose results predict the answer here |
| **UNCERTAIN** | The evidence is insufficient: a closest paper is UNREADABLE, a key source is UNREACHABLE, the search is incomplete, or the remaining gap depends on an unchecked claim |

For every classification, explain these six points:
1. the closest prior work;
2. what has already been studied;
3. what is methodologically different;
4. whether that difference is scientifically meaningful (would it
   change the field's methods or understanding?);
5. whether the same or a comparable benchmark has been used;
6. what uncertainty remains.

**The "untested on this benchmark" rule.** That an identical
combination has not been tested on the proposed benchmark does not, by
itself, make the work novel. Such a gap is defensible (PARTIAL OVERLAP)
only if the checker names a specific property of this benchmark or its
documented failure mode for which the prior results do **not** predict
the answer. Otherwise the gap is SUBSTANTIALLY ANSWERED, and the
classification is ALREADY STUDIED.

**Wording.** "NOVEL" is an internal classification label. In any
report, gap statement or paper text, keep prior-work-checker's existing
wording: "No directly equivalent experiment was found in the searched
literature". Never write "novel", "first" or "unexplored" as a claim.

---

## 6. Mapping to the existing novelty gate (PASS / FAIL)

The four-way classification does **not** replace prior-work-checker's
PASS / FAIL gate (P1–P5, Step 6). It is mapped onto that gate. The gate
still requires every one of P1–P5, so the stricter rule always applies.

| Classification | Existing gate result | Notes |
|---|---|---|
| NOVEL | **PASS** only if P1–P5 all hold | A PASS is a novelty pass only. Whether the contribution is meaningful (technical depth, §4e) is the advisor's gate, not this one |
| PARTIAL OVERLAP | **PASS** only if P1–P5 all hold **and** the gap passes the "untested on this benchmark" rule (§5) | PARTIAL rows are listed and the gap is stated relative to them (existing rule) |
| ALREADY STUDIED | **FAIL**: FAIL-ALREADY-DONE (IDENTICAL) or FAIL-SUBSTANTIALLY-ANSWERED (SUBSTANTIALLY EQUIVALENT) | A genuinely different contribution is a *new question*. It returns through benchmark-finder regeneration and is classified afresh; it never upgrades this verdict |
| UNCERTAIN | **FAIL-UNVERIFIED** (existing reason; never PASS) | If the uncertainty can be resolved within the stage budget (an alternative route to an UNREADABLE paper, a re-query), resolve it and reclassify before returning the slot. Otherwise the FAIL stands and the slot follows the existing iteration loop |

**Archive collision verdicts** (benchmark-finder Step 5, research-pipeline
Step 2c) map as follows:

| Archive verdict | Consistent classification | Pipeline effect (unchanged) |
|---|---|---|
| NO EVIDENCE FOUND | NOVEL or PARTIAL OVERLAP, depending on whether a positive methodological contribution is identified | Continue |
| PARTIAL OVERLAP | PARTIAL OVERLAP | Continue; the gap is stated relative to the overlap |
| STRONG OVERLAP | ALREADY STUDIED (substantially equivalent) | Back to selection or redesign |
| ALREADY TESTED | ALREADY STUDIED (identical) | Back to selection or redesign |

If the archive verdict and the Evidence Report disagree, the **stricter**
one applies, and prior-work-checker re-runs the Step 2c re-check.

---

## 7. Prior-Work Evidence Report (reusable output)

Every candidate that reaches Stage 2 gets one report. Save it in the
project working directory, never inside the skills directory, as:

`prior_work_evidence_<run-tag>_<RQk>.md`

For example, `prior_work_evidence_v22_RQ1.md`. The run tag stops reused
RQ identifiers from colliding across discovery runs. The
benchmark-centered archive (`prior_work_<benchmark>.md`, benchmark-finder
Step 5) links to it from its §5 "Closest prior work — RQk", and the
report links back to the archive. Neither file duplicates the other's
inventory.

```markdown
# Prior-Work Evidence Report — <run-tag> <RQk>

Status: DRAFT (Stage 2) / FINAL (Stage 3)   Last verified: <YYYY-MM-DD>
Archive: prior_work_<benchmark>.md (if it exists)

| Field | Content |
|---|---|
| Research question | Exact question (Research Question Format Rule) |
| Proposed method | Components, each operationally defined (§3.1) |
| Closest prior work | Three papers (§4 table, below) |
| Existing combinations | Per-subset table (§3, below) |
| Novelty classification | NOVEL / PARTIAL OVERLAP / ALREADY STUDIED / UNCERTAIN, plus the six-point explanation (§5) |
| Existing novelty gate | PASS / FAIL-<reason> per §6; or "unresolved: Stage 3 pending" while DRAFT |
| Methodological difference | The exact difference from the closest work |
| Benchmark overlap | Same benchmark / comparable benchmark / different setting, for each closest paper |
| Strongest published baseline | Method, metric, number, source location, access class; plus the mature-baseline-map pointer and any UNMEASURED systems |
| Known failure modes | Documented limitations of that baseline, each with its source (and cause evidence, if any, kept separate) |
| Open research gap | Gap statement in prior-work-checker Step 5 form |
| Evidence quality | Verified / Partial / Unverified (definitions below) |
| Supporting references | Direct links plus the sections, tables or figures used |

## Closest prior work
(§4 table, one row per paper)

## Combination analysis
| Subset | Closest work | Studied? | Evaluable on the benchmark? | Overlap degree | Notes / pruning reason |

## Search log
| Stage | Date | Source / route | Query (Q1–Q9 / N1–N5) | Results | Notes (incl. UNREACHABLE) |

## Coverage report
### Source access table (probed this session; §2a-1)
| Source / route | Probe date | Status (WORKING / RATE-LIMITED / BLOCKED / NOT TESTED) | Used for |

### Completeness checklist (§2b)
| Required search | Strategy | DONE / NOT DONE (reason) |

### Paper ledger
| Paper | Identified via | Verification level (FULL-TEXT / ABSTRACT-ONLY / METADATA-ONLY / SECONDARY) | Full-text route (or rungs tried) | Role (closest / baseline source / related / background) | Claims still unverified |

Counts (identified / FULL-TEXT / ABSTRACT-ONLY / METADATA-ONLY): these
describe effort, not coverage.

### Unresolved methodological overlaps
| Paper | Possible overlap | Why unresolved (level, inaccessible section) | What would resolve it |

### Remaining uncertainty affecting GO / NO-GO
(Each open item, and the decision it could flip: classification, gate,
S1 baseline, or S2 mechanism. Write "none" only when every
decision-critical paper is FULL-TEXT.)

## Bibliographic corrections
(Any earlier citation found to have a wrong title, date or ID.)
```

**Evidence quality:**
- **Verified**: every closest paper READ at FULL-TEXT level; the
  baseline number quoted from the source with its location; no
  UNREACHABLE source in the critical path; completeness checklist all
  DONE (or NOT DONE only for a source that is BLOCKED, with its function
  covered by another rung of the ladder); "Remaining uncertainty
  affecting GO / NO-GO" = none.
- **Partial**: the critical facts are verified, but a non-closest source
  is unread or unreachable.
- **Unverified**: a critical fact (a closest paper, the baseline number,
  or the gap) rests on a snippet, an abstract or an assumption. A report
  with Unverified evidence cannot support a PASS. That is P4/P5.

---

## 8. How downstream skills use the report (no re-derivation)

| Report field | Consumer | Used for |
|---|---|---|
| Novelty classification + gate | research-readiness-advisor | **Novelty strength** (mapped below). The advisor never reclassifies |
| Strongest published baseline + known failure modes | Advisor (S1); benchmark-finder's mature baseline map is the S1 maturity source | S1 documented weakness and headroom |
| Known failure modes (cause evidence) + methodological difference + combination analysis | Advisor (S2, technical depth) | Does the mechanism target the documented cause? Are the combined signals complementary or redundant? |
| Benchmark overlap + strongest baseline protocol | Advisor (S3) | Is there a fair, comparable test? |
| Open research gap + classification | Advisor (Step 5b item 6) | Would the positive and the negative finding add knowledge? |
| All of the above | research-planner | Comparison matrix columns "Closest prior work", "Novelty" and "Strongest comparable baseline" |
| Gate + evidence quality + status | research-pipeline | Pre-implementation evidence gate |

**Novelty strength** (an advisor rating, read from the report):

| Classification + gate | Novelty strength |
|---|---|
| NOVEL + PASS, evidence Verified | HIGH |
| PARTIAL OVERLAP + PASS with a narrow but clearly defensible gap, or NOVEL with Partial evidence | MEDIUM |
| PARTIAL OVERLAP + PASS whose gap is only a new benchmark or setting, or a new combination of known methods | LOW |
| ALREADY STUDIED / UNCERTAIN | Not rated: the gate has FAILED |

Novelty strength stays a secondary ranking criterion (shared definitions
§8, criterion 5). It never raises SOTA potential.

---

## 9. Authority and conflict rules

| Decision | Sole authority |
|---|---|
| Benchmark validity, SAME-TASK, V1–V4, mature baseline map, archive | benchmark-finder |
| Novelty classification, novelty gate PASS / FAIL, Evidence Report | prior-work-checker |
| SOTA potential S1–S4, technical depth, novelty *strength*, negative-result readiness, short-paper readiness | research-readiness-advisor |
| Compute, duration, FITS DURATION, difficulty | compute-planner |
| Final design, comparison matrix, ranking, selection, scheduling, stop/pivot | research-planner |
| Orchestration and enforcement of every mandatory gate | research-pipeline |

- A good rating in one skill never overrides a failed gate in another.
- These are workflow transitions, not recursive calls. A skill that
  finds a problem returns the slot to the owning skill's step, through
  the existing loops (prior-work FAIL → benchmark-finder regeneration;
  redesign → shared definitions §6). It never re-runs another skill's
  judgment itself.
