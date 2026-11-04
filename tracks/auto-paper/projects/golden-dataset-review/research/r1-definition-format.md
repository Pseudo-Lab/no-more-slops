# R1 — Definition and criteria of "golden" datasets, plus Mini Review format

Researcher notes, compiled 2026-10-25. Each source was opened (abstract page, publisher page, or full PDF) unless a claim is marked **UNVERIFIED**. "Verified" means the claim was read on the page listed; for several papers only the abstract or landing page was read, and this is noted where it matters. Grey literature (vendor docs, blogs) is marked **[GREY]**.

---

## Part A. What makes a dataset "golden"

### A1. Origins: test collections and assessor disagreement

**1. Voorhees, E. M. (2000).** Variations in relevance judgments and the measurement of retrieval effectiveness. *Information Processing & Management*, 36(5), 697–716. DOI: 10.1016/S0306-4573(00)00010-8. NIST record: https://www.nist.gov/node/710491 (earlier version: SIGIR 1998, DOI 10.1145/290941.291017, pp. 315–323).
- Verified (NIST abstract): relevance assessments by humans vary considerably, yet "very high correlations were found among the rankings of systems produced using different relevance judgment sets," which supports using TREC collections as laboratory tools.
- Implication for the review: in the Cranfield/TREC tradition a "gold" label does not have to be the one true label. It has to be stable enough that system rankings hold up when assessors disagree. That makes it a *relative-ranking* criterion, not an absolute-correctness criterion.
- UNVERIFIED: specific assessor-overlap figures (about 0.3–0.5 overlap is often cited). The full text was not read. Page range 697–716 also comes from memory.

**2. Rebholz-Schuhmann, D. et al. (2010).** CALBC silver standard corpus. *Journal of Bioinformatics and Computational Biology*, 8(1), 163–179. DOI: 10.1142/S0219720010004562. Companion paper at LREC 2010: https://aclanthology.org/L10-1609/
- Verified (repository record and LREC companion, via search snippets): a "silver standard" corpus was built by harmonizing the output of several automatic named-entity taggers (EMBL-EBI, EMC Rotterdam, NLM, JULIE Lab, Linguamatics) through a voting scheme. The corpus has about 630k sentences and about 16M tokens.
- Verified (LREC companion): agreement with the harmonized set was lower for proteins/genes than for diseases/species.
- Use: a canonical early definition of **silver** (machine-consensus) versus **gold** (expert human) labels. It maps directly onto today's LLM-generated "silver" eval sets.

### A2. Critiques of a single ground truth

**3. Aroyo, L., & Welty, C. (2015).** Truth Is a Lie: Crowd Truth and the Seven Myths of Human Annotation. *AI Magazine*, 36(1), 15–24. DOI: 10.1609/aimag.v36i1.2564. URL: https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2564 (full PDF read from the VU mirror: https://research.vu.nl/ws/files/1130974/04%20Aroyo.pdf)
- Verified (full text): the seven myths are (1) One Truth, (2) Disagreement Is Bad, (3) Detailed Guidelines Help, (4) One Is Enough, (5) Experts Are Better, (6) All Examples Are Created Equal, and (7) Once Done, Forever Valid.
- Verified: the authors say most myths derive from an "antiquated ideal of a single correct truth." They propose CrowdTruth, which treats disagreement as signal.
- Use: Myth 7 directly motivates maintaining and versioning golden sets. Myths 4 and 5 bear on annotator count and the expert-versus-crowd choice.

**4. Pavlick, E., & Kwiatkowski, T. (2019).** Inherent Disagreements in Human Textual Inferences. *TACL*, 7, 677–694. DOI: 10.1162/tacl_a_00293. URL: https://aclanthology.org/Q19-1043/
- Verified (abstract): disagreements in NLI ratings are "not dismissible as annotation 'noise'." They persist when more ratings are collected and when the context given to raters changes.
- Verified: the uncertainty that state-of-the-art NLI models express does not match the distribution of human disagreement. The authors propose that evaluation should target the full distribution of plausible human judgments.

**5. Plank, B. (2022).** The "Problem" of Human Label Variation: On Ground Truth in Data, Modeling and Evaluation. *EMNLP 2022*, 10671–10682. DOI: 10.18653/v1/2022.emnlp-main.731. URL: https://aclanthology.org/2022.emnlp-main.731/
- Verified (abstract): human label variation is usually treated as noise. Plank argues it reflects real disagreement, subjectivity, and multiple plausible answers, and that it affects data, modeling, *and evaluation*.
- Verified: the paper contributes a repository of public datasets with **un-aggregated labels**.

**6. Cabitza, F., Campagner, A., & Basile, V. (2023).** Toward a Perspectivist Turn in Ground Truthing for Predictive Computing. *Proceedings of AAAI 2023*, 37(6), 6860–6868. DOI: 10.1609/aaai.v37i6.25840. arXiv: 2109.04270.
- Verified (via search of DOI/arXiv records): the paper argues against majority-vote aggregation as the default "ground truth" and recommends keeping annotator disagreement (data perspectivism). The argument covers subjective tasks and also "objective" ones such as medical decision making.
- Note: page range 6860–6868 is taken from a secondary reference list (CEUR keynote). The DOI was confirmed.

**7. Northcutt, C. G., Athalye, A., & Mueller, J. (2021).** Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks. *NeurIPS 2021 Datasets & Benchmarks Track*. arXiv: 2103.14749. URL: https://arxiv.org/abs/2103.14749
- Verified: across 10 widely used CV/NLP/audio test sets, the average label error rate is at least 3.3%. At least 6% of the ImageNet validation set is mislabeled.
- Use: a quantitative reason why "gold" test sets must themselves be audited.

**8. Vendrow, J., Vendrow, E., Beery, S., & Madry, A. (2025).** Do Large Language Model Benchmarks Test Reliability? arXiv: 2502.03461. URL: https://arxiv.org/abs/2502.03461
- Verified (abstract): "pervasive label errors can compromise these evaluations." The authors propose **"platinum benchmarks,"** curated to minimize label errors and ambiguity. They revised 15 popular benchmarks.
- Verified: frontier LLMs still fail on simple tasks, such as elementary math word problems, once label noise is removed.
- Use: introduces a gold → platinum terminology, a useful foil for defining "golden." Peer-review venue not confirmed (arXiv only as checked).

### A3. Criteria frameworks for benchmark quality

**9. Bowman, S. R., & Dahl, G. E. (2021).** What Will it Take to Fix Benchmarking in Natural Language Understanding? *NAACL 2021*, 4843–4855. DOI: 10.18653/v1/2021.naacl-main.385. URL: https://aclanthology.org/2021.naacl-main.385/
- Verified (full PDF): there are four criteria. Benchmarks should (1) offer a valid test of the relevant phenomena, (2) have examples "accurately and unambiguously annotated," with test examples "validated thoroughly enough to remove erroneous examples and to properly handle ambiguous ones," (3) offer adequate statistical power, and (4) disincentivize potentially harmful (biased) systems.
- Verified: the authors argue that adversarial data collection "does not meaningfully address" the causes of these failures.

**10. Reuel, A., Hardy, A., Smith, C., Lamparth, M., Hardy, M., & Kochenderfer, M. J. (2024).** BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices. *NeurIPS 2024 Datasets & Benchmarks* (Spotlight). arXiv: 2411.12990.
- Verified: 46 best practices across the benchmark lifecycle were used to assess 24 AI benchmarks, and quality varied widely. Most benchmarks do not report statistical significance or allow easy replication.
- Verified: the paper provides a minimum QA checklist and a living repository (betterbench.stanford.edu).

**11. Bean, A. M., Mahdi, A., et al. (42 authors) (2025).** Measuring what Matters: Construct Validity in Large Language Model Benchmarks. *NeurIPS 2025 Datasets & Benchmarks Track*. arXiv: 2511.04703. URL: https://arxiv.org/abs/2511.04703
- Verified (abstract): a systematic review of **445** LLM benchmarks with **29** expert reviewers, ending in **8** recommendations.
- UNVERIFIED (search summary only): "16% use statistical tests," "~half test abstract phenomena without clear definitions," and "38% reuse existing benchmarks/exams." Check against the full paper before citing.

### A4. Documentation standards that put trust into practice

**12. Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021).** Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92. arXiv: 1803.09010. DOI (CACM): 10.1145/3458723.
- Verified (arXiv page): published in CACM, December 2021. Every dataset should come with a datasheet documenting its "motivation, composition, collection process, recommended uses, and so on."
- UNVERIFIED: the CACM DOI and page numbers come from memory. The full question count (about 57 questions in 7 sections) was not checked.

**13. Bender, E. M., & Friedman, B. (2018).** Data Statements for Natural Language Processing: Toward Mitigating System Bias and Enabling Better Science. *TACL*, 6, 587–604. DOI: 10.1162/tacl_a_00041. URL: https://aclanthology.org/Q18-1041/
- Verified: proposes data statements as a professional practice, so that claims about how research generalizes become more precise and exclusion and bias are reduced.
- UNVERIFIED: the element list (curation rationale, language variety, speaker/annotator demographics, ...) was not on the landing page.

**14. Pushkarna, M., Zaldivar, A., & Kjartansson, O. (2022).** Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI. *ACM FAccT 2022*. arXiv: 2204.01075.
- Verified: lessons drawn from deploying over 20 Data Cards, plus 2 case studies.
- UNVERIFIED: FAccT proceedings DOI (10.1145/3531146.3533231, from memory).

**15. Akhtar, M., Benjelloun, O., et al. (31 authors) (2024).** Croissant: A Metadata Format for ML-Ready Datasets. *NeurIPS 2024 Datasets & Benchmarks*. Short version at the DEEM@SIGMOD 2024 workshop. arXiv: 2403.19546.
- Verified: a shared metadata format that makes datasets discoverable, portable, and interoperable. It is supported by repositories that together span "hundreds of thousands of datasets." Human raters found Croissant metadata readable, understandable, complete, and concise.

**16. Jain, N., Akhtar, M., et al. (18 authors) (2024).** A Standardized Machine-readable Dataset Documentation Format for Responsible AI (Croissant-RAI). arXiv: 2407.16883.
- Verified: extends Croissant with machine-readable RAI documentation built on Schema.org, and ships with a Python library and a visual editor. ArXiv only; no peer-reviewed venue was shown.

**17. NeurIPS Datasets & Benchmarks / Evaluations & Datasets track requirements. [Official conference policy]**
- NeurIPS 2026 blog, "Responsible AI metadata requirements for the Evaluations and Datasets Track": https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/
  - Verified: "Dataset submissions to the track are already required to include a Croissant file." For 2026, "all dataset submissions must now include Responsible AI (RAI) metadata as part of the dataset's Croissant file," covering "dataset limitations, potential biases, intended use." The 2026 post refers to the track as the "Evaluations and Datasets Track" (no rename announcement was read).
- NeurIPS Paper Checklist: https://neurips.cc/public/guides/PaperChecklist
  - Verified: item 12 covers licenses of existing assets, item 13 covers documentation of new assets "via structured templates," item 14 covers crowdsourcing instructions and compensation, and item 15 covers IRB.
- NeurIPS 2025 D&B post-cycle blog (https://blog.neurips.cc/2025/12/05/...): per the search snippet, 2025 required persistent hosting plus mandatory Croissant, and license info was missing in 11.9% of submissions' metadata. **UNVERIFIED** (the page itself was not opened).

### A5. Maintenance, deprecation, and living benchmarks

**18. Luccioni, A. S., Corry, F., Sridharan, H., Ananny, M., Schultz, J., & Crawford, K. (2022).** A Framework for Deprecating Datasets: Standardizing Documentation, Identification, and Communication. *ACM FAccT 2022*. arXiv: 2111.04424.
- Verified: deprecated datasets keep circulating after retirement. The proposed framework has six components: risk assessment, impact mitigation, appeal mechanisms, timeline, post-deprecation protocols, and publication checks. It also proposes a centralized repository that tracks modifications and deprecations.

**19. Liang, P., Bommasani, R., et al. (2023).** Holistic Evaluation of Language Models (HELM). *Transactions on Machine Learning Research*. arXiv: 2211.09110.
- Verified: 16 core plus 26 targeted scenarios, 7 metrics, and 30 models. Coverage of core scenarios across models went from about 18% before HELM to 96.0%.
- Verified: intended as a "living benchmark for the community," updated with new scenarios, metrics, and models.

**20. Kiela, D., Bartolo, M., et al. (2021).** Dynabench: Rethinking Benchmarking in NLP. *NAACL 2021*, 4110–4124. DOI: 10.18653/v1/2021.naacl-main.324.
- Verified: an open-source platform for human-and-model-in-the-loop dynamic dataset creation, launched with 4 initial tasks. It argues that static benchmarks saturate while models still fail simple challenge examples.

**21. Chen, S., et al. (2025).** Recent Advances in Large Language Model Benchmarks against Data Contamination: From Static to Dynamic Evaluation. arXiv: 2502.17521 (v2, Sep 2025; search results indicate EMNLP 2025, **UNVERIFIED**).
- Verified: surveys methods that harden static benchmarks and identifies "the lack of standardized criteria for evaluating dynamic benchmarks." Proposes design principles for dynamic benchmarking.

### A6. Industry practice: golden sets and eval-driven development [GREY + one peer-reviewed-adjacent]

**22. OpenAI. "Evals" guide (API docs). [GREY]** https://developers.openai.com/api/docs/guides/evals (redirected from platform.openai.com/docs/guides/evals). Accessed 2026-10-25.
- Verified: test data is JSONL in which each item holds a test input and a "human-provided ground truth label." Graders ("testing criteria") include `string_check` exact match against `correct_label`.
- Verified: describes an eval-driven loop (specify behavior as an eval, run it, analyze, iterate) and compares it to behavior-driven development.
- Verified: the page notes that the Evals platform is being deprecated, with read-only access from 2026-10-31 and shutdown on 2026-11-30, in favor of "Datasets." **Cite with access date, and expect the URL to change.**

**23. Anthropic. "Create strong empirical evaluations" (Claude docs). [GREY]** https://platform.claude.com/docs/en/docs/test-and-evaluate/develop-tests (redirected from docs.anthropic.com). Accessed 2026-10-25.
- Verified: there are three design principles. (1) "Be task-specific," mirroring the real-world task distribution and including edge cases. (2) "Automate when possible." (3) "Prioritize volume over quality," meaning "more questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals."
- Verified: listed edge cases include irrelevant or nonexistent input, overly long input, harmful input, and "ambiguous test cases where even humans would find it hard to reach an assessment consensus." Success criteria should be specific, measurable, achievable, and relevant. Example: F1 ≥ 0.85 on a held-out set of 10,000 tweets. The page also advises grading with a different model from the generator.
- Note for the review: the "volume over quality" stance is in explicit tension with the "gold = high-quality, small" view (Bowman & Dahl; Vendrow et al.). That makes it a good "schools of thought" item for the Discussion section, which Frontiers requires.

**24. Husain, H. (2024, Mar 29).** Your AI Product Needs Evals. Blog post. **[GREY]** https://hamel.dev/blog/posts/evals/
- Verified: proposes three levels of evaluation: (1) unit-test assertions, (2) human and model eval over logged traces, and (3) A/B testing.
- Verified: "You must remove all friction from the process of looking at data." Start with binary good/bad labels. Validate LLM judges against human labels, measuring precision and recall separately because raw agreement misleads on imbalanced data. Use LLMs to generate synthetic test inputs.

**25. Shankar, S., Zamfirescu-Pereira, J. D., Hartmann, B., Parameswaran, A. G., & Arawjo, I. (2024).** Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences. arXiv: 2404.12272. Published at ACM UIST 2024 (**venue UNVERIFIED**; the arXiv page lists none).
- Verified: EvalGen is a mixed-initiative interface. Users grade a subset of outputs, and those grades select the LLM-generated evaluators that best align with the user.
- Verified: the paper names **"criteria drift"**: users need criteria to grade outputs, but grading outputs helps them define criteria, and some criteria depend on the specific outputs observed. This challenges the assumption that a golden set's rubric can be fixed *a priori*.

### A7. Existing surveys (to position the review's novelty)

**26. Chang, Y., Wang, X., Wang, J., et al. (2024).** A Survey on Evaluation of Large Language Models. *ACM TIST*. arXiv: 2307.03109.
- Verified: organized around *what* to evaluate (tasks), *where* (benchmarks), and *how* (methods). The authors argue evaluation should be "an essential discipline."
- UNVERIFIED: journal details 15(3), article 39, DOI 10.1145/3641289 (from memory).
- Gap: catalogs benchmarks but does not treat how to *construct and validate* an application-specific golden set.

**27. Yu, H., Gan, A., Zhang, K., Tong, S., Liu, Q., & Liu, Z. (2024).** Evaluation of Retrieval-Augmented Generation: A Survey. arXiv: 2405.07437. Also a Springer chapter, DOI 10.1007/978-981-96-1024-2_8 (proceedings title **UNVERIFIED**; Springer page was paywalled/redirected; likely CCF BigData 2024).
- Verified: proposes the Auepora framework (A Unified Evaluation Process of RAG). Analyzes retrieval and generation metrics (relevance, accuracy, faithfulness) and benchmark limitations.

**28. Gan, A., Yu, H., Zhang, K., et al. (2025).** Retrieval Augmented Generation Evaluation in the Era of Large Language Models: A Comprehensive Survey. arXiv: 2504.14891.
- Verified: compiles and categorizes RAG datasets and frameworks, and includes a meta-analysis of evaluation practice in high-impact RAG papers.

**29. Xu, C., Guan, S., Greene, D., & Kechadi, M.-T. (2024).** Benchmark Data Contamination of Large Language Models: A Survey. arXiv: 2406.04244.
- Verified: defines benchmark data contamination (benchmark information leaking into training data), which makes performance unreliable. Reviews alternative assessment methods.

**Additional pointers found, not deeply verified:** "Know Your RAG: Dataset Taxonomy and Generation Strategies for Evaluating RAG Systems" (IBM, arXiv 2411.19710, COLING 2025 Industry). Per the search snippet, public and naively generated synthetic QA sets are highly unbalanced across information-request types. "Can LLMs Be Trusted for Evaluating RAG Systems? A Survey of Methods and Datasets" (arXiv 2504.20119; 63 papers in its final set per snippet). Both are **UNVERIFIED** beyond search snippets and are relevant to sibling researchers working on construction and synthetic data.

### Gap statement (synthesis for the Introduction)
Existing surveys cover (a) LLM evaluation broadly (Chang et al.), (b) RAG metrics and benchmarks (Yu et al.; Gan et al.), (c) contamination (Xu et al.; Chen et al.), and (d) general benchmark quality (BetterBench; Bean et al.; Bowman & Dahl). None of them gives a focused account of **building, validating, and maintaining an application-specific golden set for LLM/RAG systems**, the artifact practitioners actually create (OpenAI/Anthropic docs, Husain, Shankar et al.). Such an account would bring together the annotation-disagreement literature (Aroyo & Welty; Plank; Cabitza et al.), label-error auditing (Northcutt et al.; Vendrow et al.), and documentation and maintenance standards (Datasheets → Croissant-RAI; deprecation; living benchmarks). This is the gap a Mini Review can fill.

A candidate operational definition, synthesized from the sources rather than quoted: a golden evaluation set is (1) **valid** for the target construct and the deployment distribution (Bowman & Dahl; Bean et al.; Anthropic "task-specific"), (2) **reliably labeled**, with disagreement measured and either resolved or retained (Voorhees; Aroyo & Welty; Plank; Cabitza), (3) **audited** for label errors (Northcutt; Vendrow), (4) **sufficiently powered** (Bowman & Dahl; BetterBench), (5) **documented** in a machine-readable way (Datasheets, Data Cards, Croissant-RAI), (6) **uncontaminated and versioned or maintained** (Xu; Chen; Luccioni; HELM/Dynabench), and (7) **aligned with stakeholder criteria that may drift** (Shankar et al.).

---

## Part B. Format: Frontiers Mini Review

Sources: Frontiers in Artificial Intelligence article types, https://www.frontiersin.org/journals/artificial-intelligence/for-authors/article-types. Frontiers in Big Data article types, https://www.frontiersin.org/journals/big-data/for-authors/article-types. Frontiers author guidelines, https://www.frontiersin.org/guidelines/author-guidelines. All accessed 2026-10-25.

Verified (both journals, identical wording):
- "Mini Review articles are peer-reviewed, have a maximum word count of **3,000** and may contain no more than **2 Figures/Tables**."
- Scope: "cover focused aspects of a current area of investigation and its recent developments."
- Required structure: **Abstract → Introduction → Subsections relevant for the subject → Discussion**.
- The Discussion must cover "different schools of thought or controversies," "current research gaps," and "potential future developments in the field" (Frontiers in AI page).
- No unpublished material is allowed (original data, submitted manuscripts, personal communications). Violations "may be rejected or reclassified." This is a B-type article fee.

Verified (general author guidelines):
- Abstract: "no longer than a single paragraph." No explicit word count appears on either page checked. The often-quoted "max 350 words" is **UNVERIFIED** for Mini Reviews.
- Keywords: "minimum of five and a maximum of eight."
- Word count includes main text, footnotes, and in-text citations. It **excludes** the abstract, section titles, figure/table captions, table contents, funding, acknowledgments, and references.
- Reference style: Frontiers uses either Harvard (author-date) or Vancouver (numbered), depending on the journal, as listed in the help center. **Which style Frontiers in AI uses is UNVERIFIED.** Indirect evidence (CSL styles for sister CS journals) points to author-year. A Frontiers template states that Frontiers style is applied at typesetting as long as citations are complete.
- Figures: 300 dpi, RGB, minimum 8 pt text, width of 85 mm (one column) or 180 mm (two columns).
- Generative-AI use must be acknowledged (name, version, model, source) in the Acknowledgements, and in Methods if applicable. AI cannot be an author.
- Conflict-of-interest, author-contribution, and data-availability statements were not described on the page fetched. Standard Frontiers sections exist, but the exact wording is **UNVERIFIED** here.

Implication for a "4-page" Korean Mini Review: the 3,000-word cap (excluding abstract and references) and the limit of 2 figures/tables, combined, are the binding constraints. Plan for one schematic figure (construction → validation → maintenance pipeline) plus one criteria table.

### Optional: Korean journal style (정보과학회논문지 / Journal of KIISE)
- **UNVERIFIED.** The search did not surface KIISE's official submission rules. Search results confused it with the 한국컴퓨터정보학회 journal (journal.kci.go.kr/jksci). An Overleaf template exists for KIISE *conference* papers (https://www.overleaf.com/latex/templates/hangugjeongbogwahaghoe-hagsuldaehoe-nonmunjagseong-yangsig/nhgcmdbskkrv). Korean journals commonly require both Korean and English titles, abstracts, and keywords, but confirm at kiise.or.kr before relying on this.
