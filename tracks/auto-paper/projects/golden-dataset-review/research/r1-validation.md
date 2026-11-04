# R1 — Validation / Quality Assurance of Evaluation Datasets

Research notes for the Mini Review "Building golden evaluation datasets for LLM and RAG applications". Collected 2026-10-25.

How claims were verified:
- **[V]** means I opened the source (arXiv abstract or HTML full text, ACL Anthology PDF, or the project page) and confirmed the claim there.
- **[V-sec]** means the claim was confirmed only through a secondary source, which is named. Check the primary source before citing it.
- **UNVERIFIED** means the claim comes from memory or could not be checked.

Venues are taken from the arXiv "comments" or "journal-ref" field or from the proceedings page, unless the entry says otherwise.

---

## 1. Inter-annotator agreement (IAA)

### S1. Artstein & Poesio (2008)
- Ron Artstein, Massimo Poesio. "Survey Article: Inter-Coder Agreement for Computational Linguistics." *Computational Linguistics* 34(4):555–596, 2008. DOI: 10.1162/coli.07-034-R2. URL: https://aclanthology.org/J08-4004/
- [V] (from the full text) CL practice follows Krippendorff (1980), as reported by Carletta (1996): "K>.8 as good reliability, with .67<K<.8 allowing tentative conclusions." The authors note that Krippendorff's 0.67 boundary was "highly tentative and cautious." In later work, Krippendorff treats α = .800 as "a pretty low standard" (Krippendorff 2004a, p. 242).
- [V] §5.3 "Interpreting the Values": "if a threshold needs to be set, 0.8 is a good value." The authors also say "we doubt that a single cutoff point is appropriate for all purposes." Some discourse corpora were useful at around 0.7.
- [V] Limits of agreement (Table 8, segmentation example). With broad segments, observed agreement A_o = 0.96 gives only K = 0.65 because expected agreement A_e = 0.89. With finer units, A_o = 0.88 gives K = 0.75. Skewed category prevalence therefore pushes chance-corrected coefficients down even when raw agreement is high. The survey also argues that weighted, α-like coefficients may suit many annotation tasks better than κ, at the cost of harder interpretation.

### S2. Krippendorff (2004), *Content Analysis* (2nd ed.)
- Klaus Krippendorff. *Content Analysis: An Introduction to Its Methodology*, 2nd ed. Sage, 2004, pp. 241–243. A related article is Krippendorff, K. (2004), "Reliability in content analysis: Some common misconceptions and recommendations," *Human Communication Research* 30(3):411–433, DOI 10.1111/j.1468-2958.2004.tb00738.x.
- [V-sec] (Wikipedia "Krippendorff's alpha", citing Krippendorff 2004, pp. 241–243) The standard is to rely on data with α ≥ 0.800. Data with 0.667 ≤ α < 0.800 support only tentative conclusions, and data with α < 0.667 are discarded.
- [V] The "α = .800 … is a pretty low standard" quote (Krippendorff 2004a, p. 242) is confirmed only as it is quoted inside Artstein & Poesio (S1).
- UNVERIFIED: I could not open the HCR article (publisher returned 403), so its exact wording is unconfirmed.

### S3. Cohen (1960)
- Jacob Cohen. "A Coefficient of Agreement for Nominal Scales." *Educational and Psychological Measurement* 20(1):37–46, 1960. DOI: 10.1177/001316446002000104.
- UNVERIFIED (bibliographic only, not opened). This is the canonical citation for κ = (p_o − p_e)/(1 − p_e). Landis & Koch (1977, *Biometrics* 33(1):159–174) give the "moderate/substantial" bands. Artstein & Poesio (S1, Fig. 1) reproduce these bands and contrast them with Krippendorff's stricter convention [V via S1].

---

## 2. Label errors in benchmarks

### S4. Northcutt, Athalye & Mueller (2021)
- "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks." NeurIPS 2021 Datasets & Benchmarks Track. arXiv:2103.14749. https://arxiv.org/abs/2103.14749
- [V] The authors estimate an average of at least 3.3% label errors across 10 commonly used test sets. At least 6% of the ImageNet validation set is mislabeled.
- [V] Rankings can flip. On corrected ImageNet labels, ResNet-18 outperforms ResNet-50 if the share of mislabeled test examples rises by just 6%. On CIFAR-10, VGG-11 outperforms VGG-19 at a 5% increase.

### S5. Gema et al. (2024/2025) — "Are We Done with MMLU?"
- Aryo Pradipta Gema et al. (16 authors). "Are We Done with MMLU?" arXiv:2406.04127 (v3, Jan 2025). https://arxiv.org/abs/2406.04127. Published at NAACL 2025 (UNVERIFIED; the arXiv page lists no venue).
- [V] MMLU-Redux consists of 5,700 manually re-annotated questions covering all 57 MMLU subjects.
- [V] An estimated 6.49% of MMLU questions contain errors. In the Virology subset, 57% of the analyzed questions contain errors.

### S6. Vendrow, Vendrow, Beery & Madry (2025) — Platinum benchmarks
- "Do Large Language Model Benchmarks Test Reliability?" arXiv:2502.03461. https://arxiv.org/abs/2502.03461. The page lists no peer-reviewed venue. A workshop version, "Large Language Model Benchmarks Do Not Test Reliability," appeared in NeurIPS 2024 Workshops (listed on mlanthology, not opened).
- [V] The authors revise 15 popular benchmarks into "platinum benchmarks," defined as "carefully curated to minimize label errors and ambiguity." The 15 are SingleOp, SingleEq, MultiArith, SVAMP, GSM8K, MMLU HS Math, three BBH tasks, TabFact, SQuAD2.0, HotpotQA, DROP, WSC, and VQA v2.0.
- [V] Procedure: several frontier LLMs answer each item. Every item that at least one model gets wrong is inspected by hand, then relabeled if the label is wrong or removed if the item is ambiguous or ill-posed. The authors note that the error counts are "only a lower bound," because the procedure misses items where all models agree with a flawed label.
- [V] On a 300-question GSM8K sample, 27 items were flagged. Of these, 26 were removed as poorly written and 1 was relabeled, leaving 274 items. Average model errors fell from 10.1 to 5.2.

### S7. GSM8K-Platinum (Vendrow et al., 2025, project blog)
- "GSM8K-Platinum" release, gradientscience.org (MIT Madry Lab), 2025. https://gradientscience.org/gsm8k-platinum/
- [V] This release revises the full GSM8K test set. 219 questions were flagged because at least one LLM disagreed with the stated answer. Of these, 110 were removed (ambiguity or logical inconsistency), 99 were verified as correct, and 10 were relabeled.
- [V] Rankings change. Claude 3.7 Sonnet (extended thinking) and Llama 405B each made 45 errors on the original GSM8K. On Platinum, they made 2 and 17 errors respectively. The noise in the original set had been masking an 8x difference.

### S8. Truong et al. (2025) — "Fantastic Bugs and Where to Find Them in AI Benchmarks"
- Sang Truong, Yuheng Tu, Michael Hardy, Anka Reuel, …, Sanmi Koyejo. arXiv:2511.16842 (Nov 2025, preprint). https://arxiv.org/abs/2511.16842
- [V] The authors run psychometric item statistics on 9 benchmarks. They assume a single latent construct, flag items whose statistics fall outside the expected ranges, and add an LLM-judge first pass. This guides expert review to problematic items with up to 84% precision.
- [V-sec] (search snippet of the PDF) The method finds additional invalid items in GSM8K and MMLU HS Math that the platinum revision (S6) missed.

### S9. SWE-bench Verified (OpenAI & SWE-bench authors, Aug 2024)
- OpenAI. "Introducing SWE-bench Verified." Blog, 13 Aug 2024 (date UNVERIFIED). https://openai.com/index/introducing-swe-bench-verified/ . Also see https://www.swebench.com/verified.html
- [V] (swebench.com) SWE-bench Verified is a "human-filtered subset of 500 instances." Annotators checked whether problem descriptions were clear, whether test patches were correct, and whether the task was solvable with the information given.
- [V-sec] (the OpenAI page returned 403; text confirmed through search snippets of the page and LongTermWiki) 93 professional Python developers annotated 1,699 random test samples, labeling each for underspecification and for whether the FAIL_TO_PASS tests reject valid solutions. Severity labels 2–3 meant the sample was discarded. 68.3% of samples were filtered out (secondary figure), which is consistent with 500/1,699 ≈ 29% retained.
- UNVERIFIED: OpenAI later published "Why we no longer evaluate SWE-bench Verified" (URL exists, page returned 403). A search snippet mentions an audit of 138 problems that o3 did not consistently solve, which found residual flawed tests. This shows that "verified" sets also decay.

### S10. Liu, Xia, Wang & Zhang (2023) — EvalPlus / HumanEval+
- "Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation." arXiv:2305.01210. NeurIPS 2023 (venue UNVERIFIED on the arXiv page). https://arxiv.org/abs/2305.01210
- [V] HumanEval's tests are extended 80x to create HumanEval+, and 26 LLMs are evaluated. Insufficient tests had hidden wrong code: pass@k drops by up to 19.3–28.9%.

---

## 3. Contamination detection and mitigation

### S11. Sainz et al. (2023)
- Oscar Sainz, Jon Ander Campos, Iker García-Ferrero, Julen Etxaniz, Oier Lopez de Lacalle, Eneko Agirre. "NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark." Findings of EMNLP 2023. arXiv:2310.18018. https://arxiv.org/abs/2310.18018
- [V] The worst case is a model trained on a benchmark's test split and then evaluated on it. Contamination inflates scores and leads to wrong published conclusions. The authors call for automatic and semi-automatic detection and for flagging compromised papers.
- Note: the arXiv comment field says "EMNLP 2024 Findings", but the paper is widely cited as Findings of EMNLP 2023. Check the ACL Anthology before citing.

### S12. Xu, Guan, Greene & Kechadi (2024)
- "Benchmark Data Contamination of Large Language Models: A Survey." arXiv:2406.04244 (31 pp.). https://arxiv.org/abs/2406.04244
- [V] The survey defines Benchmark Data Contamination (BDC) as models absorbing benchmark information during training, which makes evaluation unreliable. It reviews alternative assessment methods and mitigation directions. The category breakdown is UNVERIFIED (not read beyond the abstract).

### S13. Oren et al. (2023) — Black-box contamination test
- Yonatan Oren, Nicole Meister, Niladri Chatterji, Faisal Ladhak, Tatsunori B. Hashimoto. "Proving Test Set Contamination in Black Box Language Models." arXiv:2310.17623. ICLR 2024 (venue UNVERIFIED on the arXiv page). https://arxiv.org/abs/2310.17623
- [V] For an exchangeable benchmark, all orderings should be equally likely. If a model assigns significantly higher likelihood to the canonical ordering than to shuffled ones, that indicates contamination. The test needs no access to training data or model weights.
- [V] The test is sensitive with models as small as 1.4B parameters, about 1,000-example test sets, and data that appears only a few times in pretraining. An audit of 5 public models found little evidence of pervasive contamination.

### S14. Srivastava et al. (2022) — BIG-bench canary string
- Aarohi Srivastava et al. (450 authors, 132 institutions). "Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models." TMLR 2023. arXiv:2206.04615. https://arxiv.org/abs/2206.04615 . Repo: https://github.com/google/BIG-bench
- [V] The benchmark has 204 tasks.
- [V] (repo README) "All task files … contain a 'canary' string, which should not be edited … to prevent BIG-bench tasks from leaking into web-scraped training data." Canaries only work if trainers filter on them, and they also let auditors probe whether a model has memorized the string.

### S15. Zhang et al. (2024) — GSM1k
- Hugh Zhang, Jeff Da, Dean Lee, …, Summer Yue. "A Careful Examination of Large Language Model Performance on Grade School Arithmetic." NeurIPS 2024 Datasets & Benchmarks. arXiv:2405.00332. https://arxiv.org/abs/2405.00332
- [V] The authors build a fresh, held-out, GSM8K-style set and observe accuracy drops of up to 8% versus GSM8K.
- [V] Across models, the probability of generating GSM8K examples is positively related to the GSM8K–GSM1k gap (Spearman r² = 0.36), which is evidence of memorization.
- GSM1k size (~1,250 problems) is UNVERIFIED.

### S16. White et al. (2024/2025) — LiveBench
- Colin White, Samuel Dooley, …, Yann LeCun, Tom Goldstein, Willie Neiswanger, Micah Goldblum. "LiveBench: A Challenging, Contamination-Limited LLM Benchmark." ICLR 2025 (Spotlight). arXiv:2406.19314. https://arxiv.org/abs/2406.19314
- [V] Questions come from recent sources (math competitions, arXiv papers, news) and are scored against objective ground truth with no LLM judge. Questions are "added and updated on a monthly basis." Top models score below 70%.

### S17. Jain et al. (2024) — LiveCodeBench (time-based split)
- Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, Ion Stoica. "LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code." arXiv:2403.07974. https://arxiv.org/abs/2403.07974 . ICLR 2025 (UNVERIFIED).
- [V] The benchmark continuously collects new problems from LeetCode, AtCoder, and CodeForces. It contains 400 problems published between May 2023 and May 2024, and it reports empirical contamination findings. That models perform worse on problems released after their training cutoff is UNVERIFIED in detail (not checked in the full text).

### S18. Recht et al. (2019) — Fresh-replication test sets
- Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt, Vaishaal Shankar. "Do ImageNet Classifiers Generalize to ImageNet?" ICML 2019 (venue UNVERIFIED on the arXiv page). arXiv:1902.10811. https://arxiv.org/abs/1902.10811
- [V] When the dataset-creation process is replicated to build new test sets, accuracy drops by 3–15% on CIFAR-10 and 11–14% on ImageNet. This is the classic evidence that a golden set should be rebuilt or refreshed with a documented, reproducible process.

---

## 4. Statistical adequacy

### S19. Card et al. (2020)
- Dallas Card, Peter Henderson, Urvashi Khandelwal, Robin Jia, Kyle Mahowald, Dan Jurafsky. "With Little Power Comes Great Responsibility." EMNLP 2020. arXiv:2010.06595. https://arxiv.org/abs/2010.06595
- [V] Underpowered experiments are common in NLP. Because GLUE test sets are small, most comparisons to the state of the art are not adequately powered. Typical human-rating designs are underpowered for small differences.
- [V] In machine translation, a typical 2,000-sentence test set has about 75% power to detect a 1-BLEU difference.

### S20. Miller (2024) — "Adding Error Bars to Evals"
- Evan Miller (Anthropic). "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations." arXiv:2411.00640. https://arxiv.org/abs/2411.00640
- [V] Report the standard error of the mean, SE = √(p̄(1−p̄)/n) for binary scores. Example: MATH 65.5% (SE 0.7%) on 5,000 questions.
- [V] Use clustered standard errors when questions are grouped (DROP, QuAC, RACE, SQuAD, MGSM). Clustered SE is about 3.05x the naive SE on DROP (1.34 vs 0.44) and about 1.88x on MGSM (1.62% vs 0.86%). Compare models with paired differences: in the paper's example, MATH +2.5% (CI +1.2 to +3.8) is significant, while HumanEval −3.1% (CI −7.2 to +1.0) is not.
- [V] Power analysis: n = (z_{α/2}+z_β)²(ω² + σ_A²/K_A + σ_B²/K_B)/δ². With δ = 3 pp, α = 0.05, 80% power, and ω² = 1/9, about 969 questions are needed, so the paper suggests at least 1,000. Resampling each question K times reduces conditional variance. Lowering the temperature to reduce variance is discouraged.

### S21. Polo et al. (2024) — tinyBenchmarks
- Felipe Maia Polo, Lucas Weber, Leshem Choshen, Yuekai Sun, Gongjun Xu, Mikhail Yurochkin. "tinyBenchmarks: evaluating LLMs with fewer examples." ICML 2024. arXiv:2402.14992. https://arxiv.org/abs/2402.14992
- [V] 100 curated examples per scenario estimate full-benchmark performance with about 2% average error. On MMLU (14K items), IRT++ is within 1.9% of true accuracy.
- [V] IRT-based anchor selection (IRT, IRT++) works best. Stratified random sampling would need well over 400 MMLU items to match IRT++ at 100. Caveat: estimates from a small subset are less reliable for unusual or specialized models.

---

## 5. Validity of benchmarks

### S22. Bean et al. (2025) — Construct validity
- Andrew M. Bean et al. (42 authors, Oxford-led). "Measuring what Matters: Construct Validity in Large Language Model Benchmarks." NeurIPS 2025 Datasets & Benchmarks Track. arXiv:2511.04703. https://arxiv.org/abs/2511.04703
- [V] 29 expert reviewers systematically reviewed 445 LLM benchmarks. Only 16.0% use uncertainty estimates or statistical tests. 78.2% define their phenomenon, but 47.8% of those definitions are contested. 38.2% reuse prior benchmarks or exams, and 31.2% generate data with LLMs. 12.3% rely only on convenience sampling. 81.3% use exact match at least in part, and 53.4% justify construct validity.
- [V] The paper makes 8 recommendations: (1) define the phenomenon; (2) measure only the phenomenon, controlling confounders such as formatting and parsing; (3) build a representative dataset; (4) acknowledge the limits of reused data; (5) prepare for contamination with held-out items; (6) use statistical methods (power, uncertainty, rater descriptions); (7) conduct error analysis; (8) justify construct validity. It also releases a Construct Validity Checklist.
- [V] Its own codebook reliability was a mean Brennan–Prediger κ of 0.524 ("moderate"). Even expert meta-review struggles to reach high agreement.

### S23. Reuel et al. (2024) — BetterBench
- Anka Reuel, Amelia Hardy, Chandler Smith, Max Lamparth, Malcolm Hardy, Mykel J. Kochenderfer. "BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices." NeurIPS 2024 Datasets & Benchmarks (Spotlight). arXiv:2411.12990. https://arxiv.org/abs/2411.12990 . Living repository: betterbench.stanford.edu (UNVERIFIED URL).
- [V] The assessment framework has 46 best practices across the benchmark lifecycle (design, implementation, documentation, maintenance, retirement) and is applied to 24 benchmarks. Quality varies widely. Most benchmarks do not report statistical significance or allow easy replication. The authors provide a minimum QA checklist.

### S24. Raji, Bender, Paullada, Denton & Hanna (2021)
- "AI and the Everything in the Whole Wide World Benchmark." NeurIPS 2021 Datasets & Benchmarks Track. arXiv:2111.15366. https://arxiv.org/abs/2111.15366
- [V] A few influential benchmarks are treated as stand-ins for broad, "general" capability. The paper identifies the construct validity problems with presenting them as general measures of progress.

### S25. Kiela et al. (2021) — Dynabench and saturation
- Douwe Kiela et al. (19 authors). "Dynabench: Rethinking Benchmarking in NLP." NAACL 2021. arXiv:2104.14337. https://arxiv.org/abs/2104.14337
- [V] Models quickly reach high benchmark scores yet "fail on simple challenge examples." The paper proposes dynamic, human-and-model-in-the-loop adversarial data collection, so that dataset creation, model development, and assessment inform one another.

---

## 6. Validating LLM judges and rubrics against a golden set

### S26. Shankar et al. (2024) — "Who Validates the Validators?"
- Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya G. Parameswaran, Ian Arawjo. "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences." arXiv:2404.12272. UIST 2024 (venue UNVERIFIED on the arXiv page). https://arxiv.org/abs/2404.12272
- [V] The paper names "criteria drift": users need criteria to grade outputs, but grading outputs is what helps them define those criteria. Some criteria depend on the outputs a user has seen. This challenges evaluation pipelines that assume criteria are fixed before any output is observed.
- [V] EvalGen generates candidate evaluators (Python assertions and LLM grader prompts), has users grade a subset of outputs, and selects the evaluators that best match those human grades. Alignment is "subjective and iterative." The participant count is UNVERIFIED.

### S27. Zheng et al. (2023) — MT-Bench / Chatbot Arena
- Lianmin Zheng et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." NeurIPS 2023 Datasets & Benchmarks. arXiv:2306.05685. https://arxiv.org/abs/2306.05685
- [V] A GPT-4 judge reaches over 80% agreement with humans, the same level as human–human agreement. The paper documents position, verbosity, and self-enhancement biases and limited reasoning ability.

### S28. Thakur et al. (2024/2025) — "Judging the Judges"
- Aman Singh Thakur, Kartik Choudhary, Venkat Srinik Ramayapally, Sankaran Vaidyanathan, Dieuwke Hupkes. "Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges." GEM² Workshop 2025 (ACL), pp. 404–430. arXiv:2406.12624. https://arxiv.org/abs/2406.12624
- [V] The study tests 13 judge models on the outputs of 9 exam-taker models. Only the largest judges approach human alignment, and they still fall below inter-human agreement. Judge scores can differ from human scores by up to 5 points. Judges with high percent agreement can still assign very different scores, so the paper recommends alignment metrics beyond percent agreement. Judges also show leniency and sensitivity to prompt complexity and length.

### S29. Bavaresco et al. (2025) — JUDGE-BENCH
- Anna Bavaresco et al. (20 authors). "LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks." ACL 2025 (main). arXiv:2406.18403. https://arxiv.org/abs/2406.18403
- [V] The study evaluates 11 LLMs as judges on 20 human-annotated datasets. Judge-human agreement varies widely with the property evaluated, the expertise of the human judges, and whether the text is human- or model-generated. The authors conclude that LLMs "should be carefully validated against human judgments before being used as evaluators."

---

## Cross-cutting insights

1. **No benchmark is gold forever, and verification is a lower bound.** Error rates found in famous sets are not small: 3.3% on average and 6% on ImageNet (S4), 6.49% in MMLU with 57% in Virology (S5), and about 68% of sampled SWE-bench items unusable (S9). Even "platinum" or "verified" revisions miss errors (S6 calls its counts lower bounds, S8 finds more, and S9 was later retired). A golden set therefore needs versioning, an errata process, and periodic re-audit, not a one-time sign-off.
2. **Model disagreement is a cheap error detector, and agreement is a blind spot.** Platinum-style curation (S6, S7) and psychometric item flagging (S8) send items to human review when models disagree or when item statistics look anomalous. Items where every model agrees with a wrong label are never surfaced. Pair model-flagging with random human audits.
3. **Label noise and sample size interact.** The noise floor matters when model gaps are small: GSM8K masked an 8x error difference between models (S7), and small label-noise shifts flip rankings (S4). Small or clustered test sets also inflate apparent precision (S19, S20: clustered SE up to 3x the naive SE). Size the golden set with a power analysis for the smallest difference that matters (about 1,000 items for a 3-pp difference, S20), and report paired, clustered CIs. For cheap regression checks, an IRT-selected subset of about 100 items gives roughly 2% error (S21).
4. **Agreement statistics are necessary but not sufficient.** κ/α thresholds (0.8, or tentatively 0.667) are conventions, not laws (S1, S2), and κ is depressed by skewed prevalence (S1, Table 8). For LLM judges, percent agreement hides score disagreement (S28), and agreement varies by task and annotator expertise (S29). Report chance-corrected agreement, the confusion structure, and the score-level deviation on a human-labeled golden subset before trusting a judge.
5. **Validity is designed in, not measured afterward.** Construct-validity reviews (S22: only 16% use statistics, 47.8% of definitions are contested) and BetterBench (S23: 46 criteria) converge on the same requirements: an explicit construct definition, representative sampling, contamination planning (held-out or time-split items, canaries: S14–S17), and error analysis. For RAG and application golden sets, the construct is the deployment task. Rubrics co-evolve with observed outputs (criteria drift, S26), so treat rubric and dataset as a versioned pair.

## Open checks before citing
- SWE-bench Verified: confirm 1,699 / 93 annotators / 68.3% on the OpenAI page (blocked here, HTTP 403).
- Krippendorff 2004 thresholds: confirm the exact page in the book or the HCR article.
- Sainz et al. venue year (2023 vs 2024 Findings).
- Venues marked UNVERIFIED (EvalPlus NeurIPS'23, Oren ICLR'24, Recht ICML'19, Shankar UIST'24, LiveCodeBench ICLR'25, MMLU-Redux NAACL'25).
