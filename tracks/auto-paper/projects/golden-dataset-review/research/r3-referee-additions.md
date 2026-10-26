# R3 — Referee-requested additions (sources 1–28)

Researcher notes for the Mini Review on building and validating golden evaluation datasets for LLM and RAG applications. Compiled 2026-10-25.

## Verification key

- **[V-full]**: quote checked against the full text. This was the arXiv PDF, latest version, unless noted. For ACL papers it was the ACL Anthology PDF.
- **[V-abs]**: checked against the abstract or metadata only. Sources were the arXiv abstract page, the Crossref record, or the publisher's landing page.
- **[V-web]**: checked against the primary web page, or its web.archive.org snapshot when the live page returned HTTP 403.
- **[V-meta]**: venue, pages, or DOI checked against Crossref, PMLR, OpenReview, NeurIPS, or ACL Anthology metadata.
- **UNVERIFIED**: not confirmed on a primary page.

Vancouver lines list up to 6 authors, then "et al." Venue, pages, and DOI appear only where [V-meta] confirmed them.

---

## 1. ppi2023 — Prediction-powered inference

- ppi2023: Angelopoulos AN, Bates S, Fannjiang C, Jordan MI, Zrnic T. Prediction-powered inference. Science; 2023. 382(6671) p. 669-674. doi:10.1126/science.adi6000. arXiv:2301.09633.
- Facts:
  - [V-abs, Crossref abstract of the Science version] The core claim is: "a framework for performing valid statistical inference when an experimental dataset is supplemented with predictions from a machine-learning system." It "yields simple algorithms for computing provably valid confidence intervals for quantities such as means, quantiles, and linear and logistic regression coefficients without making any assumptions about the machine-learning algorithm," and "more accurate predictions translate to smaller confidence intervals."
  - [V-full, arXiv] The paper frames two alternatives that PPI improves on:
    - **Imputation**: "proceed as if they are gold-standard measurements … the conclusions may be invalid because the predictions may have biases."
    - **Classical**: "only use the available gold-standard measurements, which are typically far less abundant than predictions."

    PPI corrects the bias with a "rectifier," which is estimated on the small gold-labelled set.
- Status: venue, volume, issue, pages, and DOI are [V-meta] (Crossref). The science.org page returned 403, so the abstract was read through Crossref.

## 2. boyeau2024 — AutoEval done right

- boyeau2024: Boyeau P, Angelopoulos AN, Li T, Yosef N, Malik J, Jordan MI. AutoEval done right: using synthetic data for model evaluation. In: Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267; 2025. p. 5276-5290. arXiv:2403.07008.
- Facts:
  - [V-abs] "These algorithms increase the effective human-labeled sample size by up to 50% on experiments with GPT-4."
  - [V-full] On the ImageNet ResNet experiment: "Our ESS exceeds that of the classical approach by approximately 50%." The method is an instantiation of PPI/PPI++ that is "compatible with existing evaluation systems such as Chatbot Arena."
- Status: the venue is **ICML 2025**, not 2024. PMLR v267 lists pages 5276–5290 and six authors; it adds Tianle Li, who is missing from the arXiv author list. OpenReview lists it as an "ICML 2025 poster" [V-meta]. **Update the key year or the cite text accordingly.**

## 3. dorner2025 — Limits to scalable evaluation at the frontier

- dorner2025: Dorner FE, Nastl VY, Hardt M. Limits to scalable evaluation at the frontier: LLM as judge won't beat twice the data. In: International Conference on Learning Representations (ICLR 2025); 2025. arXiv:2410.13341.
- Facts:
  - [V-full] The main result: "when the judge is no more accurate than the evaluated model, no debiasing method can decrease the required amount of ground truth labels by more than half."
  - [V-full] The empirical results suggest "that at the frontier, stratified PPI rarely improves sample efficiency by more than a factor of two, compared to standard stratified sampling." The abstract adds: "the sample size savings achievable in practice are even more modest than what our theoretical limit suggests."
- Status: the venue is [V-meta]. OpenReview lists it as "ICLR 2025 Oral", and the arXiv comment reads "ICLR 2025". No page numbers exist (ICLR has no paginated proceedings).

## 4. yao2024tau — τ-bench

- yao2024tau: Yao S, Shinn N, Razavi P, Narasimhan K. τ-bench: a benchmark for tool-agent-user interaction in real-world domains. In: International Conference on Learning Representations (ICLR 2025); 2025. arXiv:2406.12045.
- Facts:
  - [V-full] Ground truth is defined by the final state of the database: "Our evaluation scheme compares the database state at the end of each episode with the ground truth expected state." This "allows for objective measurement … while also providing room for stochastic variation in the conversation itself." The benchmark was built in three stages: "manual schema and API design, LM-assisted generation of data entries, and manual scenario generation and verification."
  - [V-full] The metric is defined as "pass^k (pass hat k), defined as the chance that all k i.i.d. task trials are successful, averaged across tasks." It contrasts with pass@k, "the chance that at least one out of k i.i.d. task trials is successful."
  - [V-full] For gpt-4o with function calling: pass^1 is "∼61% on τ-retail and ∼35% on τ-airline" and falls "to as low as ∼25% for pass^8 on τ-retail." The abstract gives "pass^8 <25% in retail." Size, from Table 1: 115 retail tasks and 50 airline tasks.
- Status: the venue is [V-meta] as an "ICLR 2025 Poster" (OpenReview forum roNSXZpUDN, via the OpenReview search API). The forum page itself returned a challenge (403).

## 5. bai2024 — MT-Bench-101

- bai2024: Bai G, Liu J, Bu X, He Y, Liu J, Zhou Z, et al. MT-Bench-101: a fine-grained benchmark for evaluating large language models in multi-turn dialogues. In: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers); 2024. p. 7421-7454. doi:10.18653/v1/2024.acl-long.401. arXiv:2402.14762.
- Facts:
  - [V-abs/V-full] Size and taxonomy: "a three-tier hierarchical ability taxonomy comprising 4208 turns across 1388 multi-turn dialogues in 13 distinct tasks." The tiers are:
    - Tier 1: "three progressive overarching abilities" (Perceptivity, Adaptability, Interactivity).
    - Tier 2: "seven detailed abilities."
    - Tier 3: the 13 tasks.
  - [V-full] Construction: "we utilized GPT-4 to generate over 1000 samples [per task]. These samples were then rigorously curated by human annotators … each piece of data … underwent screening by five annotators, and we ultimately retained only the data that all annotators deemed to be of high quality."
  - [V-full] Judge validation: "The agreement between GPT-4 and human expert evaluations reached 87%."
- Status: [V-meta] (Crossref and ACL).

## 6. liu2024agentbench — AgentBench

- liu2024agentbench: Liu X, Yu H, Zhang H, Xu Y, Lei X, Lai H, et al. AgentBench: evaluating LLMs as agents. In: International Conference on Learning Representations (ICLR 2024); 2024. arXiv:2308.03688.
- Facts:
  - [V-abs] "a multi-dimensional benchmark that consists of 8 distinct environments."
  - [V-full] The environments fall into three groundings:
    - Code: Operating System, Database, Knowledge Graph.
    - Game: Digital Card Game, Lateral Thinking Puzzles, House-Holding.
    - Web: Web Shopping, Web Browsing.

    The paper notes: "All datasets, whether newly created or adapted from existing ones, are … reformulated to simulate interactive environments."
- Status: the venue is from the arXiv comment ("Published in ICLR 2024"). OpenReview was not checked directly, so treat the venue as [V-abs].

## 7. mazeika2024 — HarmBench

- mazeika2024: Mazeika M, Phan L, Yin X, Zou A, Wang Z, Mu N, et al. HarmBench: a standardized evaluation framework for automated red teaming and robust refusal. In: Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR 235; 2024. p. 35181-35224. arXiv:2402.04249.
- Facts:
  - [V-full] Size and splits: "HarmBench contains 510 unique harmful behaviors, split into 400 textual behaviors and 110 multimodal behaviors." It has an official split: "The validation set contains 100 behaviors and the test set contains 410 behaviors."
  - [V-full] Categories:
    - 7 semantic categories: Cybercrime & Unauthorized Intrusion, Chemical & Biological Weapons/Drugs, Copyright Violations, Misinformation & Disinformation, Harassment & Bullying, Illegal Activities, General Harm.
    - 4 functional categories: standard, copyright, contextual, and multimodal, with "200, 100, 100, and 110 behaviors, respectively."
  - [V-full] Validation:
    - Several authors curated the behaviors manually, filtering for "differential harm / online searchability."
    - Success classifiers were checked against "human judgments on our manually labeled validation set." The HarmBench classifier averages 93.19% agreement, against 88.37% for the GPT-4 judge (Table 3).
    - "The validation classifier obtains 88.6% agreement with human labels, compared to 93.2% for the test classifier."
- Status: [V-meta] (PMLR v235).

## 8. rottger2024 — XSTest

- rottger2024: Röttger P, Kirk H, Vidgen B, Attanasio G, Bianchi F, Hovy D. XSTest: a test suite for identifying exaggerated safety behaviours in large language models. In: Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers); 2024. p. 5377-5400. doi:10.18653/v1/2024.naacl-long.301. arXiv:2308.01263.
- Facts:
  - [V-abs] Size and purpose: "XSTest comprises 250 safe prompts across ten prompt types that well-calibrated models should not refuse to comply with, and 200 unsafe prompts as contrasts that models, for most applications, should refuse." Each type has 25 safe prompts. The suite is "a small and hand-crafted diagnostic test suite for exaggerated safety."
  - [V-full] Response labels were annotated by hand: "All annotations were completed by three authors of this paper, with two annotations per prompt." Agreement figures:

    | Model | Agreement | Fleiss' κ |
    |---|---|---|
    | Llama2.0 | 96.4% | 0.93 |
    | Llama2.1 | 95.8% | 0.93 |
    | MistrI | 97.6% | 0.92 |
    | MistrG | 93.8% | 0.89 |
    | GPT-4 | 98.4% | 0.97 |

    "All disagreements were discussed among the three annotating authors to decide on a final label."
- Status: [V-meta].

## 9. cui2025 — OR-Bench

- cui2025: Cui J, Chiang WL, Stoica I, Hsieh CJ. OR-Bench: an over-refusal benchmark for large language models. In: Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267; 2025. p. 11515-11542. arXiv:2405.20947.
- Facts:
  - [V-abs] Size: "80,000 over-refusal prompts across 10 common rejection categories, a subset of around 1,000 hard prompts … and an additional 600 toxic prompts."
  - [V-full] Labelling uses an LLM moderator ensemble: "a model ensemble consisting of GPT-4-turbo-2024-04-09, Llama-3-70b, and Gemini-1.5-pro-latest … only those deemed safe by a majority vote are included." Claude-3-opus was excluded because it "produced overly conservative results and had a lower agreement ratio."
  - [V-full] Validation against humans (Table 1, 100 tasks; 3 workers plus one author; Appendix L):

    | Labeller | Accuracy | False-positive rate |
    |---|---|---|
    | Ensemble | 93.0% | 16.0% |
    | Human expert | 94.0% | 8.0% |

    The paper states: "we achieve over 98% of the performance level of human experts."
- Status: [V-meta] (PMLR v267). The ICLR 2025 submission was rejected (OpenReview).

## 10. son2025kmmlu — KMMLU

- son2025kmmlu: Son G, Lee H, Kim S, Kim S, Muennighoff N, Choi T, et al. KMMLU: measuring massive multitask language understanding in Korean. In: Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers); 2025. p. 4076-4104. doi:10.18653/v1/2025.naacl-long.206. arXiv:2402.11548.
- Facts:
  - [V-abs] "35,030 expert-level multiple-choice questions across 45 subjects … While prior Korean benchmarks are translated from existing English benchmarks, KMMLU is collected from original Korean exams."
  - [V-full] Filtering pipeline:
    - Sources: "533 diverse sources, spanning the Public Service Aptitude Test (PSAT), Korean License Tests, and the College Scholastic Ability Test (CSAT)."
    - Crawl: "Initially, we collected 371,002 questions using automatic crawling."
    - Filters: heuristic filters for duplicates and parsing errors, plus format standardization. "This filtering reduces the dataset by 34% to 243,777 questions."
    - Human baseline: about 90% of the exams have test-taker data, with "an average accuracy of 62.6%."
  - [V-full] Error and contamination notes:
    - "we released the dataset to the public for six months. During this period, we received five issues reported by the community, and 741 instances were modified accordingly."
    - "the 35,030 questions in the test set underwent manual review to remove copyrighted materials. We replaced 147 instances … No additional errors were identified during this process."
    - A leakage probe following Xu et al. (2024) found that LLMs "fail to recall the KMMLU benchmark implying low likelihood of benchmark contamination."
- Status: [V-meta]. The arXiv comment still reads "Under Review", but Crossref and ACL confirm NAACL 2025.

## 11. son2024haerae — HAE-RAE Bench

- son2024haerae: Son G, Lee H, Kim S, Kim H, Lee J, Yeom JW, et al. HAE-RAE Bench: evaluation of Korean knowledge in language models. In: Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024); 2024. p. 7993-8007. arXiv:2309.02706.
- Facts:
  - [V-abs] Focus: "six downstream tasks across four domains: vocabulary, history, general knowledge, and reading comprehension … emphasizes a model's aptitude for recalling Korean-specific knowledge and cultural contexts." The authors argue against "back translations or re-implementations of English tests."
  - [V-full, Table 1] Questions per task: Loan Words 169, Rare Words 405, Standard Nomenclature 153, Reading Comprehension 447, General Knowledge 176, History 188. The total is **1,538** (our arithmetic from Table 1).
  - [V-full] Example construction (History): "randomly selected 40 pages [from Namuwiki]. From each page, authors manually crafted five questions … filtered out 12 questions with overlapping tokens between questions and answers."
- Status: pages are [V-meta] (Crossref). Crossref gives an unusual DOI, 10.63317/3rfkwnhbtxpn, which is not used here (UNVERIFIED). The ACL Anthology ID was not checked.

## 12. singh2025 — Global-MMLU

- singh2025: Singh S, Romanou A, Fourrier C, Adelani DI, Ngui JG, Vila-Suero D, et al. Global MMLU: understanding and addressing cultural and linguistic biases in multilingual evaluation. In: Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers); 2025. p. 18761-18799. doi:10.18653/v1/2025.acl-long.919. arXiv:2412.03304.
- Facts:
  - [V-abs] "28% of all questions requiring culturally sensitive knowledge … for questions requiring geographic knowledge, an astounding 84.9% focus on either North American or European regions." The dataset spans "42 languages."
  - [V-full] Translation verification: "professional translations with post-edits (14 languages), crowdsourced translations (11 languages), and machine translations (16 languages)" plus English. "We hire professional annotators to verify translation quality and include improvements from rigorous per-question post-edits as well as human translations."
  - [V-full] Cultural annotation: "50 per subject, totaling 2,850 samples" (MMLU Annotated). "Each data point was reviewed by at least three annotators … 96.4% of all data points were reviewed by more than 3 human annotators."
- Status: [V-meta]. Caveat: only 14 of the 41 non-English languages are professionally post-edited, and 16 remain machine-translated. A review should not describe all 42 languages as human-verified.

## 13. wei2024simpleqa — SimpleQA

- wei2024simpleqa: Wei J, Karina N, Chung HW, Jiao YJ, Papay S, Glaese A, et al. Measuring short-form factuality in large language models. arXiv preprint; 2024. arXiv:2411.04368.
- Facts:
  - [V-full] Size and answer-key design: "SimpleQA, which contains 4,326 short, fact-seeking questions … Reference answers to questions are determined by two independent AI trainers." The paper adds: "each question was answered by an independent AI trainer without access to the answer given by the question creator."
  - [V-full] The adversarial collection: "it is adversarially collected against GPT-4 responses."
  - [V-full] Error-rate estimate:
    - Third-trainer check: "randomly selecting 1,000 examples and having them answered by a third trainer … performance of the third trainer was 94.4%."
    - Of the 5.6% (56/1000) graded wrong, manual review attributed many to trainer error. "The remaining 2.8% of the errors from the third trainer revealed real issues with the data."
    - Conclusion: "we estimate that the error rate of our benchmark is around 3%, assuming no false positives from the prompted ChatGPT grader."
    - Common issues: ambiguous questions and conflicting reputable sources.
- Status: no peer-reviewed venue is listed on arXiv (the comment says only "Blog post"). Cite as an arXiv preprint.

## 14a. hle — Humanity's Last Exam

- hle: Center for AI Safety, Scale AI, HLE Contributors Consortium. A benchmark of expert-level academic questions to assess AI capabilities. Nature; 2026. 649(8099) p. 1139-1146. doi:10.1038/s41586-025-09962-4. arXiv:2501.14249.
  - The arXiv preprint has a different title, "Humanity's Last Exam", with authors Phan L, Gatti A, Han Z, Li N, Hu J, Zhang H, et al.
  - Crossref and the arXiv DOI field both link the preprint to this Nature article. It was published online on 2026-01-28 and in print on 2026-01-29.
- Facts:
  - [V-web, Nature page] "HLE consists of 2,500 questions across dozens of subjects … Each question has a known solution that is unambiguous and easily verifiable but cannot be quickly answered by internet retrieval."
  - [V-full, arXiv] The pipeline:
    - LLM-difficulty filter: "we logged over 70,000 attempts, resulting in approximately 13,000 questions which stumped LLMs that were forwarded to expert human review."
    - Expert review in "two rounds of reviews" by reviewers with graduate degrees.
    - Post-release: "Following release, we conducted a public review period."
    - Searchability audit with "GPT-4o mini/GPT-4o search and Perplexity Sonar models."
  - [V-web Nature + V-full arXiv] Error estimates:
    - "two main rounds of auditing, each on a sample of 200 questions … yielded a final estimated expert disagreement rate of 15.4% for the public set."
    - "A targeted peer review on a biology, chemistry and health subset, proposed in ref. 63, found an expert disagreement rate of approximately 18%." The arXiv version cites [47] for this. The reference is presumably FutureHouse; the reference list was not checked (UNVERIFIED).
    - The arXiv version describes an "HLE-Rolling" process.
- Status: the venue is [V-meta] (Crossref, and the Nature page meta tags). The individual-author byline on the Nature version is UNVERIFIED: Crossref lists the three group authors first, then individuals. **Cite the Nature version by its Nature title.**

## 14b. futurehouse2025 — FutureHouse HLE audit

- futurehouse2025: Skarlinski M, Laurent J, Bou A, White A. About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong [Internet]. FutureHouse; 2025 Jul 23 [updated 2025 Sep 16; cited 2026 Oct 25]. Available from: https://www.futurehouse.org/research-announcements/hle-exam
- Facts:
  - [V-web] Headline figure: "We found that 29 ± 3.7% (95% CI) of the text-only chemistry and biology questions had answers with directly conflicting evidence in peer reviewed literature. We believe this arose from the incentive used to build the benchmark."
  - [V-web] Method:
    - Scope: "text-only biology/health and chemistry subsets of HLE (321 questions)."
    - Agent screen: the PaperQA2-based agent Crow "found 53.3% (n=171) of the rationales provided to be directly conflicting with published evidence" (57.0% for chemistry, 51.6% for biology/health).
    - Expert check: "independent expert chemistry and biology evaluators … examine 150 of the 321 outputs," rating on a 5-point Likert scale.
    - Output: the supported subset was released as "HLE-Gold-Bio/Chem" on Hugging Face. Its size was not stated on the page (UNVERIFIED).
  - [V-web] Update of Sep 16, 2025: the HLE team "did an independent follow-up analysis and found about 18% of a subset of questions in Bio/Chem were problematic … via a three expert review … They found that 25% of the time at least one reviewer disagreed." They "plan to announce a rolling revision process."
- Status: [V-web], read from raw HTML. The author names come from the page byline as parsed by WebFetch, and were not confirmed in raw HTML (partly UNVERIFIED).

## 15. openai2026swe — SWE-bench Verified retirement

- openai2026swe: OpenAI. Why SWE-bench Verified no longer measures frontier coding capabilities [Internet]. OpenAI; 2026 Feb 23 [cited 2026 Oct 25]. Available from: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ (archived 2026-10-15 at web.archive.org/web/20261015182204/…)
- Facts:
  - [V-web, archive] The headline finding: "We audited a 27.6% subset of the dataset that models often failed to solve and found that at least 59.4% of the audited problems have flawed test cases that reject functionally correct submissions."
  - [V-web] Audit set and procedure:
    - "an audit of 138 SWE-bench Verified problems that OpenAI o3 did not consistently solve over 64 independent runs." 138/500 = 27.6%.
    - "Each case was independently reviewed by at least six experienced software engineers. If an expert flagged an issue, it was re-verified by an additional team."
    - Breakdown: 35.5% "narrow" tests that enforce implementation details, 18.8% "wide" tests that check unspecified functionality, and 5.1% miscellaneous.
  - [V-web] Contamination reason: "all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics." Also: "improvements on SWE-bench Verified … increasingly reflect how much the model was exposed to the benchmark at training time." OpenAI recommends SWE-bench Pro.
- Status: the live page returned 403. The archive snapshot was read in full. Correction: the audited set was selected using **o3** failures. GPT-5.2, Claude Opus 4.5, and Gemini 3 Flash are the models in the contamination section; secondary press attributed the audit set to GPT-5.2.

## 16. vania2021 — Comparing test sets with IRT

- vania2021: Vania C, Htut PM, Huang W, Mungra D, Pang RY, Phang J, et al. Comparing test sets with item response theory. In: Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers); 2021. p. 1141-1158. doi:10.18653/v1/2021.acl-long.92.
- Facts:
  - [V-full] Scope: "we draw on Item Response Theory and evaluate 29 datasets using predictions from 18 pretrained Transformer models on individual test examples."
  - [V-full] Findings: "Quoref, HellaSwag, and MC-TACO are best suited for distinguishing among state-of-the-art models, while SNLI, MNLI, and CommitmentBank seem to be saturated." The span-selection format "is effective in differentiating between strong and weak models."
- Status: [V-meta]. No arXiv ID was checked (UNVERIFIED).

## 17. rodriguez2021 — Evaluation examples are not equally informative

- rodriguez2021: Rodriguez P, Barrow J, Hoyle AM, Lalor JP, Jia R, Boyd-Graber J. Evaluation examples are not equally informative: how should that change NLP leaderboards? In: Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers); 2021. p. 4486-4503. doi:10.18653/v1/2021.acl-long.346.
- Facts:
  - [V-full] The model: an IRT (DAD) leaderboard "can guide what to annotate, identify annotation errors, detect overfitting, and identify informative examples." Two signals flag errors:
    - "Negative discriminability suggests an annotation error."
    - Feasibility: "1 − λi corresponds to the prevalence of annotation errors that lead to unsolvable items."
  - [V-full] Validation on SQuAD 2.0:
    - "we inspect sixty SQuAD development set items," ten from each of six IRT-defined groups.
    - "Inter-annotator agreement between three authors … Krippendorff's α … is 0.344. Despite only modest agreement … negative discriminability is predictive of bad items."
- Status: [V-meta].

## 18. klie2023 — Annotation error detection

- klie2023: Klie JC, Webber B, Gurevych I. Annotation error detection: analyzing the past and present for a more coherent future. Computational Linguistics; 2023. 49(1) p. 157-198. doi:10.1162/coli_a_00464. arXiv:2206.02280.
- Facts:
  - [V-abs] Scope: "we reimplement 18 methods for detecting potential annotation errors and evaluate them on 9 English datasets for text classification as well as token and span labeling … define a uniform evaluation setup including a new formalization of the annotation error detection task."
  - [V-full] Findings:
    - "AED can already be useful in real use cases to support data cleaning efforts. But especially for more difficult datasets, the performance ceiling is far from reached yet."
    - "finding inconsistencies is often more difficult than finding annotation errors." Model-based methods were good at errors but weak on inconsistencies; surface-form methods (kNN entropy, label entropy, weighted discrepancy) showed the opposite.
    - On cross-validation: "We therefore recommend the use of CV."
- Status: [V-meta].

## 19. gilardi2023 — ChatGPT vs crowd workers

- gilardi2023: Gilardi F, Alizadeh M, Kubli M. ChatGPT outperforms crowd workers for text-annotation tasks. Proceedings of the National Academy of Sciences of the United States of America; 2023. 120(30) e2305016120. doi:10.1073/pnas.2305016120. arXiv:2303.15056.
- Facts (PNAS version, [V-abs] via Crossref, matching arXiv v2 [V-full]):
  - "Using four samples of tweets and news articles (n = 6,183) … the zero-shot accuracy of ChatGPT exceeds that of crowd workers by about 25 percentage points on average, while ChatGPT's intercoder agreement exceeds that of both crowd workers and trained annotators for all tasks."
  - "the per-annotation cost of ChatGPT is less than $0.003—about thirty times cheaper than MTurk."
- **Version warning.** The figures the referee quoted come from the arXiv **v1** abstract, which is still shown in the arXiv metadata: "2,382 tweets … four out of five tasks … about twenty times cheaper." **They are not the published PNAS figures.** Cite the PNAS numbers (6,183 items; about +25 pp; about 30× cheaper), or explicitly label the others as preprint v1.
- Status: [V-meta].

## 20. chiang2023 — Can LLMs be an alternative to human evaluations?

- chiang2023: Chiang CH, Lee HY. Can large language models be an alternative to human evaluations? In: Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers); 2023. p. 15607-15631. doi:10.18653/v1/2023.acl-long.870. arXiv:2305.01937.
- Facts:
  - [V-abs] Method: "We present the LLMs with the exact same instructions, samples to be evaluated, and questions used to conduct human evaluation." It was tested on "open-ended story generation and adversarial attacks."
  - [V-abs] Finding: "the result of LLM evaluation is consistent with the results obtained by expert human evaluation." Results were also "stable over different formatting of the task instructions and the sampling algorithm."
  - [V-full] The human reference is English teachers. The paper notes that AMT workers "cannot distinguish GPT-2 … generated and human-written stories, while English teachers show a clear preference for human-written stories."
- Status: [V-meta].

## 21. heineman2025 — Signal and Noise

- heineman2025: Heineman D, Hofmann V, Magnusson I, Gu Y, Smith NA, Hajishirzi H, et al. Signal and noise: a framework for reducing uncertainty in language model evaluation. In: Advances in Neural Information Processing Systems 38 (NeurIPS 2025); 2025. arXiv:2508.13144.
- Facts:
  - [V-full] Definitions:
    - Noise is "the relative standard deviation of the final n checkpoints."
    - Signal is "dispersion, calculated as the maximum difference between the scores of any two models, divided by the mean."
    - "we consider a benchmark to have high signal when models evaluated on it have a wide and evenly distributed range of scores."
  - [V-abs/V-full] Key finding: "benchmarks with a better signal-to-noise ratio are more reliable when making decisions at small scale, and those with less noise have lower scaling law prediction error." Signal alone and noise alone "have low correlation with decision accuracy." The interventions are switching to perplexity, "filtering noisy subtasks," and checkpoint averaging. The study used 30 benchmarks and 375 models (arXiv v1).
- Status: the NeurIPS 2025 virtual site lists it as a "Spotlight Poster" (poster 115712) [V-web]. The track (main or Datasets & Benchmarks) and the proceedings pages are UNVERIFIED. A search summary suggested that the camera-ready abstract cites 465 models and four interventions (UNVERIFIED). Quote the arXiv version.

## 22. biderman2024 — Lessons from the trenches

- biderman2024: Biderman S, Schoelkopf H, Sutawika L, Gao L, Tow J, Abbasi B, et al. Lessons from the trenches on reproducible evaluation of language models. arXiv preprint; 2024. arXiv:2405.14782.
- Facts:
  - [V-full, v3, 31 May 2026] The "Key Problem": "there can be many semantically equivalent but syntactically different ways of expressing the same idea … our best automated tools for determining whether two sentences are semantically equivalent are the very models we are seeking to evaluate."
  - [V-abs] Named issues: "sensitivity of models to evaluation setup, difficulty of proper comparisons across methods, and the lack of reproducibility and transparency." The paper draws on "three years of experience" with lm-eval.
  - [V-full] Checklist: "Always share your exact prompts … full evaluation code including the full prompts … Prompts should not be optimized for performance on a given model, and the amount of prompt engineering done should be disclosed." Also: "Avoid copying results from other implementations."
- Status: no venue is listed on arXiv (UNVERIFIED). Note that v3 (2026) restructures the sections, so section numbers differ from v1.

## 23. lhoest2021 — Hugging Face Datasets

- lhoest2021: Lhoest Q, Villanova del Moral A, Jernite Y, Thakur A, von Platen P, Patil S, et al. Datasets: a community library for natural language processing. In: Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: System Demonstrations; 2021. p. 175-184. doi:10.18653/v1/2021.emnlp-demo.21. arXiv:2109.02846.
- Facts:
  - [V-abs] Aims: "Datasets aims to standardize end-user interfaces, versioning, and documentation." The library had ">650 unique datasets, … >250 contributors."
  - [V-full] Versioning and cards: "N practitioners using the same dataset should know they have exactly the same version … Each dataset utilizes a standard tabular format, and is versioned and cited." The library "prioritizes community management and documentation through the dataset hub and data cards" (Fig. 1 shows the data card for ELI5).
- Status: [V-meta] (ACL Anthology bib).

## 24. zellers2018swag — SWAG

- zellers2018swag: Zellers R, Bisk Y, Schwartz R, Choi Y. SWAG: a large-scale adversarial dataset for grounded commonsense inference. In: Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing; 2018. p. 93-104. doi:10.18653/v1/D18-1009. arXiv:1808.05326.
- Facts:
  - [V-abs] "SWAG, a new dataset with 113k multiple choice questions … we propose Adversarial Filtering (AF), a novel procedure that constructs a de-biased dataset by iteratively training an ensemble of stylistic classifiers, and using them to filter the data." It addresses "annotation artifacts and human biases." Human accuracy is 88%.
- Status: [V-meta]. The paper calls AF "novel", but **"first adversarial filtering" is a priority claim we did not verify.** Phrase it as "introduced Adversarial Filtering (AF)."

---

## Additional checks (25–28)

### 25. gema2025 — MMLU-Redux error taxonomy

- gema2025: Gema AP, Leang JOJ, Hong G, Devoto A, Mancino ACM, Saxena R, et al. Are we done with MMLU? In: Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers); 2025. p. 5069-5096. doi:10.18653/v1/2025.naacl-long.262. arXiv:2406.04127.
- [V-full] Confirmed. There are two groups and five leaf categories:
  - **Type 1, Question Assessment:**
    - (1a) Bad Question Clarity: "poorly presented in terms of various aspects, such as clarity, grammar, and sufficiency of information."
    - (1b) Bad Options Clarity: "options are unclear, similar, or irrelevant"; mostly parsing errors.
  - **Type 2, Ground Truth Verification:**
    - (2a) No Correct Answer.
    - (2b) Multiple Correct Answers.
    - (2c) Wrong Ground Truth.
- [V-full] Scale: "14 human experts manually assessed and re-annotated 5,700 questions across all subsets of MMLU. We estimate that 6.49% of the questions are erroneous." Also "57% of the analysed questions in the Virology subset contain errors."

### 26. polo2024 — tinyBenchmarks

- polo2024: Maia Polo F, Weber L, Choshen L, Sun Y, Xu G, Yurochkin M. tinyBenchmarks: evaluating LLMs with fewer examples. In: Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR 235; 2024. p. 34303-34326. arXiv:2402.14992.
- [V-full] What degrades: the **correctness-based anchor-point** strategy, not the IRT-based one.
  - Test: "a hand-picked test set of 40 specialized models … their correctness patterns might be different from those in the train set."
  - Result: "the correctness-based anchor strategy deteriorates when tested on specialized LLMs. In contrast to the IRT-based anchors that are only slightly affected."
  - The paper also flags this in its method section: correctness clustering "can be unreliable when such correctness patterns are spurious, e.g., when predicting the accuracy of an LLM specialized to a domain," and "can suffer from distribution shifts."
  - A "by date" train/test split, with the newest models as the test set, is used as the harder shift scenario.
- Headline claim [V-abs]: "100 curated examples" suffice for MMLU (about 14K items).

### 27. thakur2025 — Judging the judges

- thakur2025: Thakur AS, Choudhary K, Ramayapally VS, Vaidyanathan S, Hupkes D. Judging the judges: evaluating alignment and vulnerabilities in LLMs-as-judges. In: Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics (GEM²); 2025. p. 404-430. arXiv:2406.12624.
- [V-full] Setting:
  - Data: TriviaQA, "validation set of the unfiltered partition … we use a random sample of 400 questions."
  - Scale: 13 judge models and 9 exam-taker models.
  - Human reference: inter-human alignment from three human judges on 1,200 sampled answers. Human alignment was 96% (Fig. 1).
- [V-full] Which judges: "While **GPT-4 Turbo and Llama-3** achieve excellent alignment scores, they can differ by up to 5 points from human scores." Fig. 1 names Llama3-70B, Llama3.1-70B and GPT-4 Turbo as the judges with "excellent" Scott's π. The paper also warns that "high percent agreement can still give scores that differ 10-20 points from the human-assigned scores."
- Venue: the arXiv journal-ref gives GEM² 2025, pp. 404–430 [V-abs]. The DOI was not checked (UNVERIFIED).

### 28. northcutt2021 — "increases by just 6%"

- northcutt2021: Northcutt CG, Athalye A, Mueller J. Pervasive label errors in test sets destabilize machine learning benchmarks. In: Thirty-fifth Conference on Neural Information Processing Systems (NeurIPS 2021) Datasets and Benchmarks Track; 2021. arXiv:2103.14749.
- [V-full] Context: "on ImageNet with corrected labels: ResNet-18 outperforms ResNet-50 if the prevalence of originally mislabeled test examples increases by just 6%." On CIFAR-10, VGG-11 beats VGG-19 at "just 5%."
- **Interpretation:** this is percentage points of noise prevalence, not a relative increase, and not points of the whole test set.
  - Noise prevalence is defined as N = |C|/|P|: the share of the *pruned* test set (CL-flagged items with no human consensus removed) that is correctable mislabels.
  - The Figure 4 caption reads: "The ResNet-50 and ResNet-18 benchmarks cross at noise prevalence N = 9%, implying ResNet-18 outperforms ResNet-50 when N increases by around 6% relative to the original pruned test data (N = 2.9% originally)." So N goes from 2.9% to about 9%, roughly +6 pp.
  - The paper notes that "the noise prevalence reported throughout this section differs from the fraction of label errors originally found in each of the test sets."
- Other figures [V-abs/V-full]:
  - At least 3.3% average errors across the 10 datasets, and at least 6% for the ImageNet validation set.
  - 51% of CL-flagged candidates were confirmed by crowdsourcing.
  - The paper later estimates that ImageNet val "contains closer to 20% label errors" once non-CL-flagged items are included.

---

## Corrections and cautions for the manuscript

1. **boyeau**: the venue is ICML 2025 (PMLR 267), not 2024, with six authors including Tianle Li.
2. **gilardi**: the PNAS figures are n = 6,183, about +25 pp, and about 30× cheaper. The "4 of 5 tasks / 2,382 tweets / 20×" figures come from preprint v1 only.
3. **hle**: the paper is now in Nature 649:1139–1146 (2026) under a different title. Its own audits report a 15.4% expert disagreement rate on the public set and about 18% on the bio/chem/health subset. FutureHouse reports 29 ± 3.7%. These are different methods, so cite them as distinct estimates.
4. **openai2026swe**: the 138 audited problems were selected by o3 failures (138/500 = 27.6%). The "at least 59.4%" figure applies to that hard subset, not to all 500 problems.
5. **singh2025**: of the 42 languages, 14 are professionally post-edited, 11 crowdsourced, and 16 machine-translated.
6. **northcutt**: "6%" is about +6 pp of noise prevalence on the pruned test set (2.9% → about 9%).
7. **zellers2018swag**: avoid "first"; say it "introduced" Adversarial Filtering.
