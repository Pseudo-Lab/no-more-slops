# R1 — Construction methods for golden evaluation datasets (LLM / RAG / agents)

Researcher notes for the Mini Review "Building golden evaluation datasets for LLM and RAG applications".
Compiled 2026-10-25. Verification key:
- **[V-abs]**: checked against the arXiv/ACL abstract page.
- **[V-full]**: checked against the full text (arXiv HTML).
- **[V-snippet]**: the primary page returned HTTP 403, so the claim was checked only against search-engine snippets of the primary page.
- **UNVERIFIED**: not checked against any source.

Venue notes: venues are taken from the arXiv "comments" or "journal-ref" fields or from the ACL Anthology. Where the arXiv page lists no venue, the entry says "arXiv preprint".

---

## 1. Expert / human authoring and annotation protocols

### S1. GPQA
Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang, R. Y., Dirani, J., Michael, J., Bowman, S. R. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark.* arXiv:2311.12022 (COLM 2024; venue UNVERIFIED). https://arxiv.org/abs/2311.12022
- [V-full] Pipeline:
  1. A PhD-level expert writes a question, with an explanation of the correct answer and the distractors.
  2. A first expert validator answers it and gives feedback.
  3. The writer may revise the question.
  4. A second expert validator answers it.
  5. Three non-experts attempt it with web access but no LLMs (at least 15 min; mean 37 min).

  61 Upwork contractors produced 564 questions. The extended set has 546.
- [V-full] Subsets are defined by validator outcomes:
  - **Main set (448):** at least half of the experts agree, and at most 2/3 of non-experts are correct.
  - **Diamond set (198):** both experts agree, and at most 1/3 of non-experts are correct.
- [V-abs] Expert accuracy is 65% (74% after discounting mistakes the experts identified in retrospect). Skilled non-experts reach 34%, and the GPT-4 baseline 39%.
- [V-full] Bonuses depend on validator outcomes, which pays writers for questions that are both correct and hard. Average pay was about $95/h.

### S2. HealthBench
Arora, R. K., Wei, J., Soskin Hicks, R., Bowman, P., Quiñonero-Candela, J., Tsimpourlas, F., Sharman, M., Shah, M., Vallone, A., Beutel, A., Heidecke, J., Singhal, K. (2025). *HealthBench: Evaluating Large Language Models Towards Improved Human Health.* arXiv:2505.08775 (OpenAI). https://arxiv.org/abs/2505.08775
- [V-abs] The benchmark has 5,000 multi-turn conversations, each graded by its own physician-written rubric. 262 physicians wrote 48,562 unique rubric criteria.
- [V-full] The conversations are mostly synthetic, a hybrid design:
  - Physicians specified the situation types to cover, and an LLM pipeline turned them into conversations.
  - Other conversations came from physician red-teaming or were rewritten from HealthSearchQA queries.
  - A model then filtered all conversations for realism, physical-health relevance, and completeness.
- [V-full] The physicians practise in 60 countries, across 26 specialties and 49 languages. The conversations cover 7 themes.
- [V-full] Meta-evaluation of the GPT-4.1 grader against physicians gives macro-F1 0.709 (random baseline 0.50). Physicians' own macro-F1 ranged from 0.569 to 0.730. Physician–physician and model–physician agreement both fall roughly between 55% and 75%. Even expert labels are noisy.

### S3. SWE-bench Verified
OpenAI (2024, Aug 13). *Introducing SWE-bench Verified.* OpenAI blog. https://openai.com/index/introducing-swe-bench-verified/ . It builds on Jimenez et al. (2024), *SWE-bench*, ICLR 2024, arXiv:2310.06770. The base paper's details are UNVERIFIED here.
- [V-snippet] 93 professional Python developers screened 1,699 random samples from the SWE-bench test set. 500 samples were kept as "Verified". By our arithmetic from these two counts, about 70.6% of the screened samples were discarded.
- [V-snippet] Annotators rated each sample 0–3 on two criteria: an underspecified issue description, and FAIL_TO_PASS tests that reject valid solutions. A rating of 2 or 3 counted as severe, and the sample was discarded.
- [V-snippet] Epoch AI's evaluations use 484 of these samples, the ones that validate on its infrastructure. Even a curated golden set loses items when it runs on a different execution environment.

### S4. Humanity's Last Exam (HLE)
Phan, L., et al. (2025; 1,178 authors, last author Hendrycks, D.). *Humanity's Last Exam.* arXiv:2501.14249. The page shows revisions through v12 (Oct 2026). Venue: preprint per the abstract page. https://arxiv.org/abs/2501.14249
- [V-abs] The benchmark has 2,500 questions across dozens of subjects. Answers are multiple-choice or exact-match, so grading can be automatic. Each answer is unambiguous and cannot be found quickly by internet search.
- [V-full] A pre-submission adversarial filter kept a question only if the frontier LLMs failed it. Over 70,000 attempts left about 13,000 questions that stumped the models and went on to two rounds of expert review:
  1. Graduate-degree reviewers graded each question against rubrics (1–3 reviews per question).
  2. Organizers approved the final set.

  After release came a public review period, and a private held-out set is kept to detect overfitting.
- [V-full] Nearly 1,000 contributors from over 500 institutions in 50 countries took part. The incentive was a $500k prize pool plus co-authorship. About 14% of questions are multimodal and 24% multiple-choice.
- [V-full] The HLE bibliography cites an external FutureHouse analysis: "About 30% of HLE chemistry/biology answers are likely wrong." The 30% figure comes from FutureHouse, not HLE's own audit, and we have not read the FutureHouse source.

---

## 2. Mining real user queries and production logs

### S5. MS MARCO
Bajaj, P., Campos, D., Craswell, N., et al. (2016/2018). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* arXiv:1611.09268. https://arxiv.org/abs/1611.09268
- [V-abs] The dataset has 1,010,916 anonymized questions sampled from Bing search logs, each with a human-generated answer. 182,669 answers were fully rewritten into well-formed natural language.
- [V-abs] It includes 8,841,823 passages extracted from 3,563,535 web documents.

### S6. Natural Questions
Kwiatkowski, T., Palomaki, J., Redfield, O., Collins, M., Parikh, A., Alberti, C., Epstein, D., Polosukhin, I., Devlin, J., Lee, K., Toutanova, K., Jones, L., Kelcey, M., Chang, M.-W., Dai, A. M., Uszkoreit, J., Le, Q., Petrov, S. (2019). *Natural Questions: A Benchmark for Question Answering Research.* TACL 7:452–466. DOI 10.1162/tacl_a_00276. https://aclanthology.org/Q19-1026/
- [V-abs] The questions are real, anonymized, aggregated Google search queries. The split is 307,373 training examples (single-annotated), 7,830 dev examples (5-way annotated), and 7,842 sequestered test examples (5-way annotated). The multi-way annotation of the eval splits is a design choice that quantifies annotator variance.

### S7. WildChat
Zhao, W., Ren, X., Hessel, J., Cardie, C., Choi, Y., Deng, Y. (2024). *WildChat: 1M ChatGPT Interaction Logs in the Wild.* arXiv:2405.01470; ICLR 2024. https://arxiv.org/abs/2405.01470
- [V-abs] The dataset has about 1M user–ChatGPT conversations with more than 2.5M turns. Users received free ChatGPT access in exchange for affirmative, consensual opt-in to anonymous transcript collection.
- [V-abs] Transcripts carry timestamps, state/country, hashed IPs, and request headers. This metadata makes it possible to stratify real traffic by geography and time.

### S8. Chatbot Arena
Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhang, H., Zhu, B., Jordan, M., Gonzalez, J. E., Stoica, I. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference.* arXiv:2403.04132 (ICML 2024; venue UNVERIFIED). https://arxiv.org/abs/2403.04132
- [V-abs] Users submit their own prompts and vote on pairwise comparisons; the paper reports more than 240K votes. The authors report that crowdsourced votes "are in good agreement" with expert raters. The abstract gives no number for this agreement.

### S9. Arena-Hard-Auto and the BenchBuilder pipeline
Li, T., Chiang, W.-L., Frick, E., Dunlap, L., Wu, T., Zhu, B., Gonzalez, J. E., Stoica, I. (2024). *From Crowdsourced Data to High-Quality Benchmarks: Arena-Hard and BenchBuilder Pipeline.* arXiv:2406.11939. https://arxiv.org/abs/2406.11939
- [V-full] BenchBuilder takes real traffic to a golden set in five steps:
  1. Start from 200K Chatbot Arena prompts.
  2. Deduplicate and remove multi-turn and non-English prompts.
  3. Cluster the remainder into 4,000 topics.
  4. Have GPT-4-Turbo score each prompt on 7 qualities: specificity, domain knowledge, complexity, problem-solving, creativity, technical accuracy, real-world application. Drop prompts scoring below 6 and clusters with a mean below 5.
  5. Sample 2 prompts from each of 250 random high-quality clusters, giving **500 prompts**.
- [V-abs] Arena-Hard-Auto separates models about 3x better than MT-Bench. Its rankings reach 98.6% correlation with human preference rankings, and a run costs about $20.

---

## 3. Synthetic / LLM-generated test sets and human-in-the-loop filtering

### S10. Self-Instruct (the generator template that synthetic test sets inherit)
Wang, Y., Kordi, Y., Mishra, S., Liu, A., Smith, N. A., Khashabi, D., Hajishirzi, H. (2023). *Self-Instruct: Aligning Language Models with Self-Generated Instructions.* ACL 2023. arXiv:2212.10560. https://arxiv.org/abs/2212.10560
- [V-full] Generation started from 175 seed tasks and produced about 52K instructions and 82K instances. A ROUGE-L ≥ 0.7 filter removed near-duplicate instructions.
- [V-full] Manual review of 200 sampled items found 92% of instructions were valid tasks, but only **54%** had all fields (instruction, input, output) correct. This is direct evidence that unfiltered synthetic items carry many label errors.

### S11. RAGAS
Es, S., James, J., Espinosa-Anke, L., Schockaert, S. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* arXiv:2309.15217 (EACL 2024 demo; venue UNVERIFIED). https://arxiv.org/abs/2309.15217
- [V-abs] RAGAS is a framework of *reference-free* metrics. They cover context relevance and focus, faithful use of the context, and generation quality.
- [V-docs: https://docs.ragas.io/en/stable/concepts/test_data_generation/rag/] Testset generation starts by building a knowledge graph:
  - A document splitter makes hierarchical nodes.
  - LLM or rule-based extractors add entities and keyphrases.
  - A relationship builder links nodes, for example by Jaccard similarity over entities.

  "Scenarios" then combine nodes with query length, query style, and persona. Query types are single-hop or multi-hop, crossed with specific or abstract.

### S12. ARES
Saad-Falcon, J., Khattab, O., Potts, C., Zaharia, M. (2024). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.* NAACL 2024. arXiv:2311.09476. https://arxiv.org/abs/2311.09476
- [V-full] FLAN-T5 XXL generates synthetic queries and answers from corpus passages, prompted with few-shot examples. A query is kept only if the retriever returns its source passage at top-1, a round-trip consistency filter. Weak and strong negatives (same document or BM25 top-10, plus contradictory answers) train lightweight judges.
- [V-full] A small human preference validation set (about 150 or more items; 300 in the main experiments) calibrates the judges through prediction-powered inference. Performance degrades below about 100–150 items.
- [V-full] ARES's Kendall τ beats RAGAS by 0.065 for context relevance and 0.132 for answer relevance on KILT/SuperGLUE, and by about 0.16 and 0.15 on real RAG systems.

### S13. Synthetic test collections for retrieval
Rahmani, H. A., Craswell, N., Yilmaz, E., Mitra, B., Campos, D. (2024). *Synthetic Test Collections for Retrieval Evaluation.* SIGIR 2024. arXiv:2405.07767. https://arxiv.org/abs/2405.07767
- [V-abs] LLM-generated queries and LLM relevance judgments can produce test collections that "can reliably be used for retrieval evaluation". The paper also analyses the risk that such collections are biased toward LLM-based retrieval systems. The abstract does not report the size of this bias.

### S14. Self-preference bias (a risk when the generator or judge evaluates its own family)
Panickssery, A., Bowman, S. R., Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.* arXiv:2404.13076 (NeurIPS 2024; venue UNVERIFIED). https://arxiv.org/abs/2404.13076
- [V-abs] GPT-4 and Llama 2 can distinguish their own outputs from other LLMs' and from human text with non-trivial accuracy. After fine-tuning, self-recognition and self-preference strength are linearly correlated.

---

## 4. Adversarial and dynamic collection; contamination resistance

### S15. Adversarial NLI (ANLI)
Nie, Y., Williams, A., Dinan, E., Bansal, M., Weston, J., Kiela, D. (2020). *Adversarial NLI: A New Benchmark for Natural Language Understanding.* ACL 2020. arXiv:1910.14599. https://arxiv.org/abs/1910.14599
- [V-full] Collection ran in 3 rounds against progressively stronger targets: BERT-Large first, then RoBERTa, then a RoBERTa ensemble that included earlier rounds' data. The training splits are 16,946, 45,460, and 100,459 examples. The dev and test sets are 1,000, 1,000, and 1,200 per round, 3,200 each in total.
- [V-full] Verification: two human verifiers must agree with the writer's label, and a third breaks ties. If writer and verifiers still disagree, the example is discarded. The model-fooled rate drops sharply once human verification is applied (overall 18.54% unverified vs 9.52% verified; Round 1 29.68% vs 18.33%). Roughly half of the "adversarial" items that seemed to fool the model did not survive human verification.

### S16. Dynabench
Kiela, D., Bartolo, M., Nie, Y., et al. (2021). *Dynabench: Rethinking Benchmarking in NLP.* NAACL 2021. arXiv:2104.14337. https://arxiv.org/abs/2104.14337
- [V-abs] Dynabench is an open platform for human-and-model-in-the-loop dataset creation. Annotators write examples that the target model misclassifies "but that another person will not". The paper launched with 4 initial tasks.

### S17. LiveBench
White, C., Dooley, S., Roberts, M., et al. (2025). *LiveBench: A Challenging, Contamination-Limited LLM Benchmark.* ICLR 2025 (Spotlight). arXiv:2406.19314. https://arxiv.org/abs/2406.19314
- [V-abs] Questions are refreshed monthly from recent sources: new math competitions, arXiv papers, news articles, and datasets. Scoring is automatic against objective ground truth, with no LLM or human judge.
- [V-abs] The benchmark spans 6 categories (math, coding, reasoning, language, instruction following, data analysis). Top models scored below 70% at publication.

### S18. LiveCodeBench
Jain, N., Han, K., Gu, A., Li, W.-D., Yan, F., Zhang, T., Wang, S., Solar-Lezama, A., Sen, K., Stoica, I. (2024). *LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code.* arXiv:2403.07974 (ICLR 2025; venue UNVERIFIED). https://arxiv.org/abs/2403.07974
- [V-abs] The paper version has about 400 problems from LeetCode, AtCoder, and Codeforces, released May 2023 – May 2024 and time-stamped by release date. Beyond code generation, it covers self-repair, code execution, and test-output prediction. It evaluates 18 base and 34 instruction-tuned LLMs.

### S19. GSM1k (evidence that contamination inflates static sets)
Zhang, H., Da, J., Lee, D., et al. (2024). *A Careful Examination of Large Language Model Performance on Grade School Arithmetic.* NeurIPS 2024 Datasets & Benchmarks. arXiv:2405.00332. https://arxiv.org/abs/2405.00332
- [V-abs] GSM1k is a fresh set built to mirror GSM8k, matched on human solve rate, number of solution steps, and answer magnitude. Leading models' accuracy drops by **up to 8%** relative to GSM8k.
- [V-abs] A model's probability of generating GSM8k examples correlates with its GSM8k-to-GSM1k gap (Spearman r² = 0.36). Many frontier models show minimal overfitting.

### S20. Annotation artifacts (risk inherent to crowd-authored items)
Gururangan, S., Swayamdipta, S., Levy, O., Schwartz, R., Bowman, S. R., Smith, N. A. (2018). *Annotation Artifacts in Natural Language Inference Data.* NAACL 2018. arXiv:1803.02324. https://arxiv.org/abs/1803.02324
- [V-abs] A classifier that sees only the hypothesis reaches about 67% accuracy on SNLI and 53% on MultiNLI. Authoring protocols leave exploitable cues, which motivates adversarial collection and artifact audits.

---

## 5. RAG-specific golden sets: retrieval labels, attribution, robustness

### S21. Pooling bias in TREC-style relevance judgments
Buckley, C., Dimmick, D., Soboroff, I., Voorhees, E. (2007). *Bias and the Limits of Pooling for Large Collections.* Information Retrieval 10(6):491–508. The volume and pages come from a citing paper's reference list (UNVERIFIED), and the DOI is UNVERIFIED. An earlier short version appeared at SIGIR 2006. NIST page: https://www.nist.gov/node/650056
- [V-snippet: NIST abstract via search] As collections grow, a fixed-size pool covers a shrinking share of documents. The assumption that "unjudged documents are non-relevant" then breaks down. The AQUAINT collection (TREC 2005) shows a bias toward relevant documents that contain topic-title words.

### S22. BEIR
Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets & Benchmarks. arXiv:2104.08663. https://arxiv.org/abs/2104.08663
- [V-abs] BEIR covers 18 datasets and 10 retrieval systems, and finds that BM25 is a robust zero-shot baseline.
- [V-full] Several BEIR datasets were annotated from lexically retrieved candidates, so "hits without lexical overlap are automatically assumed to be irrelevant." On TREC-COVID, Hole@10 is 6.4% for BM25 but 30.6% for DPR and 31.8% for TAS-B.
- [V-full] Adding 980 manual judgments raised DPR's nDCG@10 from 0.332 to 0.445 and ANCE's from 0.654 to 0.735. ANCE moved from slightly below BM25 to above it. BM25 barely changed (0.656 to 0.668). Incomplete qrels can reverse system rankings.

### S23. LLM relevance labelling (Bing)
Thomas, P., Spielman, S., Craswell, N., Mitra, B. (2024). *Large Language Models Can Accurately Predict Searcher Preferences.* arXiv:2309.10621 (SIGIR 2024; venue UNVERIFIED). https://arxiv.org/abs/2309.10621
- [V-abs] LLM relevance labels are as accurate as human labellers. Measured against gold labels from real searchers, they beat third-party workers at "a fraction of the cost". The approach is deployed at Bing.
- [V-abs] Accuracy is sensitive to the prompt; even simple paraphrases change it.

### S24. UMBRELA
Upadhyay, S., Pradeep, R., Thakur, N., Craswell, N., Lin, J. (2024). *UMBRELA: UMbrela is the (Open-Source Reproduction of the) Bing RELevance Assessor.* arXiv:2406.06519. https://arxiv.org/abs/2406.06519
- [V-abs] UMBRELA is an open-source GPT-4o relevance assessor that reproduces Thomas et al. On TREC Deep Learning 2019–2023, rankings from its labels correlate highly with rankings from human qrels. The authors planned to use it in the TREC 2024 RAG Track.

### S25. ALCE (citation and attribution labels)
Gao, T., Yen, H., Yu, J., Chen, D. (2023). *Enabling Large Language Models to Generate Text with Citations.* EMNLP 2023. arXiv:2305.14627. https://arxiv.org/abs/2305.14627
- [V-full] ALCE has three datasets: ASQA and QAMPARI over a Wikipedia snapshot (about 21M passages), and ELI5 over Sphere (about 899M passages). Citation recall and precision are computed with an NLI model (TRUE, T5-11B).
- [V-full] Agreement between ALCE's automatic judgments and human judgments: Cohen's κ = 0.698 for citation recall and 0.525 for citation precision. Taking the human labels as gold, ALCE is 85.1% and 77.6% accurate.
- [V-abs] On ELI5, even the best models lack complete citation support about 50% of the time.

### S26. RGB
Chen, J., Lin, H., Han, X., Sun, L. (2024). *Benchmarking Large Language Models in Retrieval-Augmented Generation.* AAAI 2024. arXiv:2309.01431. https://arxiv.org/abs/2309.01431
- [V-abs] RGB tests 4 abilities: noise robustness, negative rejection, information integration, and counterfactual robustness. It is bilingual (English and Chinese).
- [V-full] Construction was semi-synthetic:
  1. ChatGPT drafts an event, a question, and the answer from recent news.
  2. Humans check the answers.
  3. Google API pages are chunked, and a dense retriever selects the top 30 chunks.
  4. Each chunk is labelled positive or negative by whether it contains the answer.
  5. For the counterfactual testbed, answers in the documents are manually edited to insert factual errors.

  RGB has 600 base questions plus 200 each for information integration and counterfactual robustness.
- [V-full] On negative rejection, the best rate (ChatGPT-judged) was 45% in English.

### S27. CRUD-RAG
Lyu, Y., Li, Z., Niu, S., Xiong, F., Tang, B., Wang, W., Wu, H., Liu, H., Xu, T., Chen, E. (2024). *CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models.* arXiv:2401.17043 (published in ACM TOIS; venue UNVERIFIED). https://arxiv.org/abs/2401.17043
- [V-abs] Tasks are organized by application type rather than by QA alone:
  - **Create:** text continuation
  - **Read:** question answering
  - **Update:** hallucination correction
  - **Delete:** summarization

  The benchmark also evaluates retriever, context length, knowledge-base construction, and LLM choices. The dataset size is not stated in the abstract (UNVERIFIED).

### S28. CRAG (stratified design)
Yang, X., Sun, K., Xin, H., et al. (2024). *CRAG — Comprehensive RAG Benchmark.* NeurIPS 2024 Datasets & Benchmarks. arXiv:2406.04744. https://arxiv.org/abs/2406.04744
- [V-abs] CRAG has 4,409 QA pairs plus mock web and knowledge-graph search APIs. It is explicitly stratified by 5 domains, 8 question categories, entity popularity (popular to long-tail), and temporal dynamism (from years to seconds).
- [V-abs] Results: frontier LLMs reach at most 34% accuracy, and straightforward RAG reaches 44%. The best industry RAG systems answer 63% of questions without hallucination. Accuracy drops for dynamic, low-popularity, and complex strata, which shows why slice-level reporting matters.

### S29. MultiHop-RAG
Tang, Y., Yang, Y. (2024). *MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries.* arXiv:2401.15391 (COLM 2024; venue UNVERIFIED). https://arxiv.org/abs/2401.15391
- [V-full] The dataset has 2,556 queries over 609 news articles published 26 Sep – 26 Dec 2023, chosen to postdate common LLM training cutoffs. Query types: inference 816, comparison 856, temporal 583, and null 301 (unanswerable, a hallucination check).
- [V-full] GPT-4 generated the queries from claim sets that share a bridge entity. UniEval checked claim–evidence alignment. Quality control combined manual review of a sample with GPT-4 scoring against criteria.

---

## 6. Coverage design: behavioural test plans and slices

### S30. CheckList
Ribeiro, M. T., Wu, T., Guestrin, C., Singh, S. (2020). *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.* ACL 2020 (Best Paper; award UNVERIFIED). arXiv:2005.04118. https://arxiv.org/abs/2005.04118
- [V-abs] CheckList is a task-agnostic test-plan methodology. A matrix of capabilities crossed with test types drives test ideation, and a tool generates test cases from templates.
- [V-abs] In the user study, practitioners using CheckList created twice as many tests and found almost three times as many bugs. A commercial sentiment model that had already been extensively tested still revealed new actionable bugs.
- The three test types are MFT (minimum functionality), INV (invariance), and DIR (directional expectation). These definitions come from the paper body and were not re-opened in this pass (UNVERIFIED).

(CRAG S28, BenchBuilder S9, RAGAS S11, RGB S26, and MultiHop-RAG S29 also show taxonomy-driven stratification. CRAG and MultiHop-RAG report per-stratum counts.)

---

## Cross-cutting insights (each with its supporting sources)

1. **Difficulty filtering versus label correctness.** An item that is adversarially filtered to defeat models is more likely to be ambiguous or wrongly keyed.
   - HLE kept only questions the LLMs failed (about 13K of 70K attempts). An external analysis cited in HLE's own bibliography estimates that about 30% of its chemistry/biology answers are wrong (S4).
   - In ANLI, roughly half of the apparent "model-fooling" examples disappear after human verification (18.5% vs 9.5%) (S15).
   - GPQA defines its main set and its Diamond subset (448 vs 198 questions) by expert-agreement thresholds (S1).

   Lesson: an adversarial filter needs an independent correctness check by a second expert.

2. **Synthetic scale versus fidelity and bias.**
   - In Self-Instruct, only 54% of generated items had all fields correct (S10).
   - Generator and judge models favour their own outputs (S14).
   - Synthetic retrieval collections can favour LLM-based retrievers (S13).

   Workable mitigations:
   - Round-trip filters (ARES top-1 retrieval check).
   - A small human-labelled calibration set of about 150–300 items with PPI (S12).
   - Hybrid designs where experts specify scenarios and write rubrics while an LLM drafts the conversations (HealthBench, S2).

3. **Realism from logs versus quality and coverage.**
   - Real queries carry the true task distribution: MS MARCO, NQ, WildChat, Chatbot Arena (S5–S8).
   - But raw traffic is noisy and skewed toward easy prompts. BenchBuilder kept only 500 of 200K prompts after clustering and LLM quality scoring (S9).

   Design implication: sample production logs by stratum (topic clusters, difficulty), not uniformly. Consent and anonymisation are part of the protocol (S7).

4. **Static golden sets decay.**
   - Contamination inflates static scores (GSM1k: up to 8% drop, S19).
   - Execution environments drift (Epoch re-validated only 484 of the 500 SWE-bench Verified tasks, S3).
   - Mitigations: time-stamped or refreshed sets (LiveBench, LiveCodeBench, post-cutoff news in MultiHop-RAG; S17, S18, S29), private held-out splits (HLE, S4), and versioned re-validation.

5. **For RAG, the "gold" includes incomplete relevance labels.**
   - Pooled qrels are biased toward the systems and terms that built the pool (S21). In BEIR, dense retrievers had up to about 31.8% unjudged top-10 hits, and filling the holes changed the system rankings (S22).
   - LLM assessors make denser judging affordable (S23, S24) but are prompt-sensitive.
   - Attribution labels judged by NLI agree with humans only moderately to substantially (κ 0.53–0.70, S25).
   - Expert rubric graders agree with physicians at levels comparable to physician–physician agreement, roughly 55–75% (S2).

   Implications: report label completeness and inter-annotator agreement alongside scores, and design slices explicitly. Examples are CRAG's popularity and dynamism strata (S28) and CheckList-style capability-by-test-type matrices (S30).

---

## Not yet verified / candidates for follow-up
- The SWE-bench base paper (Jimenez et al., ICLR 2024, arXiv:2310.06770): not opened.
- SWE-bench Verified: the OpenAI blog returned 403, so the figures come from search snippets only.
- The DOI for Buckley et al. (2007).
- The FutureHouse analysis of HLE label errors (an external blog; not opened).
- The venues marked UNVERIFIED above.
- Possible additions:
  - The TREC 2024 RAG Track overview (Pradeep et al.) for nugget-based golden answers.
  - KILT (Petroni et al., NAACL 2021) for provenance labels.
  - "Dynamic Data Collection" follow-ups (e.g., Adversarial QA, Bartolo et al., TACL 2020).
