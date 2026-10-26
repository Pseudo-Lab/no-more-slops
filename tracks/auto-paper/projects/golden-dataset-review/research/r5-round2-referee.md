# R5: Round-2 referee checks against primary sources

Checked 2026-10-25. Each quote was taken from text fetched in this session (arXiv HTML/abs, arXiv API, NeurIPS proceedings, Crossref API, ACL Anthology, a web.archive.org snapshot, or the author-hosted PDF), unless a line is marked otherwise.

---

## 1. `haas2025`: SimpleQA Verified

**Verdict: CONFIRMED, with one correction.** Authors and size are correct. The paper does **not** report one aggregate "fraction of labels changed". It reports stepwise removal counts (4,326 to 1,000, a 76.9% cumulative reduction) and describes label corrections only qualitatively.

- Authors (arXiv abs): Lukas Haas, Gal Yona, Giovanni D'Antonio, Sasha Goldshtein, Dipanjan Das. v1 is dated 9 Sep 2025. v2 was revised 10 Mar 2026, and the quotes below come from the current HTML (v2).
- URL: https://arxiv.org/abs/2509.07968 ; https://arxiv.org/html/2509.07968

Quotes:
- Abstract: "We introduce SimpleQA Verified, a 1,000-prompt benchmark for evaluating Large Language Model (LLM) short-form factuality based on OpenAI's SimpleQA. It addresses critical limitations in OpenAI's benchmark, including noisy and incorrect labels, topical biases, and question redundancy."
- Introduction: "SimpleQA suffers from incorrect ground truths and disproportionally leans toward specific topics and question formats. The dataset contains a high degree of redundancy with semantically similar or lexically overlapping questions."
- Redundancy: "SimpleQA contains 119 questions (2.7% of dataset) asking about the founding dates of different Colombian municipalities."
- Topical/answer-type bias: "32.8% of questions in SimpleQA require a date and 24.1% require a person's name as the answer" and "SimpleQA over-indexes on science and technology domains".

The paper does not frame these step counts as label-error rates:

| Step (section) | Quote | Count |
|---|---|---|
| Unique reference URL (2.1) | "This reduced the dataset size from 4,326 to 3,095 questions (−28.5%)." | −1,231 |
| Semantic dedup, cosine 0.77 (2.2) | "reduced the number of samples in our dataset from 3,095 to 2,871 (−7.2%)." | −224 |
| TF-IDF dedup, threshold 0.4, manual review (2.2) | "further reduces our dataset size from 2,871 to 2,664 (−7.2%)." | −207 |
| Publisher crawl-preference filter (2.3) | "reduces the dataset from 2,664 to 1,855 (−30.4%)" | −809 |
| Answer-type/topic rebalancing (2.4) | "our dataset shrinks from 1,855 to 1,218 (−34.3%)" | −637 |
| Source reconciliation, non-numeric (2.5) | "We remove questions from the dataset which are clearly ambiguous or where sources point to more than one distinct answer. Additionally, where possible, we correct both answers and reference URLs. This reduces our dataset further from 1,218 to 1,117 (−8.3%) samples." | −101 |
| Source reconciliation, numeric, 5% margin (2.5) | "This lowers the dataset size from 1,117 to 1,073 (−3.9%)." | −44 |
| Headroom/difficulty filter (2.6) | "This brings down the dataset size from 1,073 to 1,000 (−6.8%)." | −73 |

- Manual review (2.7): "Date precision: ... the provided ground truth is either too specific or not specific enough. By checking the sources, we correct these labeling mistakes." The number of corrected labels is not given.
- Caution: the dedup, crawl-filter, rebalancing and difficulty steps are *curation* choices, not label errors. Only the §2.5 removals (101 + 44 = 145 of 1,218) and the uncounted §2.5/§2.7 corrections are about label correctness. Even those mix ambiguity with error.
- Arithmetic: dedup removed 224 + 207 = 431 items, but the paper does not give this sum.

Reference:
- haas2025: Haas L, Yona G, D'Antonio G, Goldshtein S, Das D. SimpleQA Verified: a reliable factuality benchmark to measure parametric knowledge. arXiv [Preprint]; 2025. doi:10.48550/arXiv.2509.07968. arXiv:2509.07968.

---

## 2. `fisch2024`: Stratified PPI

**Verdict: CONFIRMED.** Authors and venue are correct. The proceedings title is "Stratified Prediction-Powered Inference for **Effective Hybrid Evaluation of Language Models**". The arXiv title is different: "Stratified Prediction-Powered Inference for Hybrid Language Model Evaluation".

- Authors: Adam Fisch, Joshua Maynez, R. Alex Hofer, Bhuwan Dhingra, Amir Globerson, William W. Cohen.
- Venue: Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track. DOI 10.52202/079017-3541. Crossref gives pages 111489–111514.
- URLs: https://proceedings.neurips.cc/paper_files/paper/2024/hash/c9fcd02e6445c7dfbad6986abee53d0d-Abstract-Conference.html ; https://arxiv.org/abs/2406.04291 ; https://api.crossref.org/works/10.52202/079017-3541

Quotes (proceedings abstract):
- "we show that the basic PPI estimates can be considerably improved by employing simple data stratification strategies."
- "with appropriate choices of stratification and sample allocation, our approach can provide substantially tighter confidence intervals than unstratified approaches. Specifically, StratPPI is expected to improve in cases where the performance of the autorater varies across different conditional distributions of the target data."

Reference:
- fisch2024: Fisch A, Maynez J, Hofer RA, Dhingra B, Globerson A, Cohen WW. Stratified prediction-powered inference for effective hybrid evaluation of language models. Adv Neural Inf Process Syst. 2024;37:111489-111514. doi:10.52202/079017-3541. arXiv:2406.04291.

---

## 3. PPI i.i.d. assumption (Angelopoulos et al. 2023)

**Verdict: CONFIRMED.** The quotes come from arXiv HTML, §1 "Problem setup". I did not compare them with the Science text.

- URL: https://arxiv.org/html/2301.09633 (abs: https://arxiv.org/abs/2301.09633)
- Quote: "For now we assume that (X,Y) and (X̃,Ỹ) are independently and identically distributed samples from a common distribution, ℙ. We generalize our results to settings with distribution shift and finite populations in Section 4.2 and Appendix B, respectively."
- Supporting quote (§4.2): "In Section 2 we focused on forming prediction-powered confidence intervals when the labeled and unlabeled data come from the same distribution."
- Related assumption: "we have a prediction rule, f: 𝒳→𝒴, that is independent of the observed data."
- Science metadata from Crossref (doi:10.1126/science.adi6000): vol 382, issue 6671, pages 669–674.

Reference:
- angelopoulos2023: Angelopoulos AN, Bates S, Fannjiang C, Jordan MI, Zrnic T. Prediction-powered inference. Science. 2023;382(6671):669-674. doi:10.1126/science.adi6000. arXiv:2301.09633.

---

## 4. OpenAI 2026-02-23, SWE-bench Verified

**Verdict: BOTH wordings appear, and they describe different things.**

The page header reads "OpenAI February 23, 2026 Research Publication Why SWE-bench Verified no longer measures frontier coding capabilities". The HTML `<title>` is "Why we no longer evaluate SWE-bench Verified | OpenAI".

- URL: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- Snapshot: https://web.archive.org/web/20261015182204/https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/

Quotes:
- Summary bullet: "Tests reject correct solutions: We audited a 27.6% subset of the dataset that models often failed to solve and found that at least 59.4% of the audited problems have flawed test cases that reject functionally correct submissions, despite our best efforts in improving on this in the initial creation of SWE-bench Verified."
- Body: "We conducted an audit of 138 SWE-bench Verified problems that OpenAI o3 did not consistently solve over 64 independent runs. Each case was independently reviewed by at least six experienced software engineers. If an expert flagged an issue, it was re-verified by an additional team. We found that 59.4% of the 138 problems contained material issues in test design and/or problem description, rendering them extremely difficult or impossible even for the most capable model or human to solve."
- Breakdown: "35.5% of the audited tasks have strict test cases that enforce specific implementation details, invalidating many functionally correct submissions, which we call narrow test cases." / "18.8% of the audited tasks have tests that check for additional functionality that wasn't specified in the problem description, which we call wide test cases." / "The remaining 5.1% of tasks had miscellaneous issues that were not well grouped with this taxonomy." These add up: 35.5 + 18.8 + 5.1 = 59.4.

Recommendation: the body sentence ("material issues in test design and/or problem description") is the precise one. The summary bullet ("flawed test cases that reject functionally correct submissions") is looser: by the page's own breakdown, the 5.1% miscellaneous share does not clearly fit it. Also, the denominator is 138 hard problems, not the full set. 138/500 = 27.6%.

---

## 5. Shankar et al. UIST 2024

**Verdict: 14 pages CONFIRMED. Article No. 131 is LIKELY but not directly verified.**

- 14 pages: Crossref gives `"page":"1-14"`. The author-hosted camera-ready PDF has 14 pages, and its ACM Reference Format line ends "...USA, 14 pages. https://doi.org/10.1145/3654777.3676450". That reference line omits the article number.
- Article No. 131: a search-engine snippet of the ACM DL page (dl.acm.org/doi/abs/10.1145/3654777.3676450) gave "Article No.: 131, Pages 1 - 14". I could not fetch ACM DL directly (403, Cloudflare), the web.archive.org capture is a Cloudflare challenge page, and Crossref and OpenAlex have no article-number field. Check this on ACM DL before final submission.
- Title: "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences". Authors: Shankar S, Zamfirescu-Pereira JD, Hartmann B, Parameswaran AG, Arawjo I. In: Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology (UIST '24), Pittsburgh PA. Published online 2024-10-11.
- URLs: https://api.crossref.org/works/10.1145/3654777.3676450 ; https://people.eecs.berkeley.edu/~bjoern/papers/shankar-validators-uist2024.pdf

Reference (confirmed fields only; add "Article 131" after ACM DL check):
- shankar2024: Shankar S, Zamfirescu-Pereira JD, Hartmann B, Parameswaran AG, Arawjo I. Who validates the validators? Aligning LLM-assisted evaluation of LLM outputs with human preferences. In: Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology (UIST '24); 2024. p. 1-14. doi:10.1145/3654777.3676450. arXiv:2404.12272.

---

## 6. BetterBench: lifecycle stages and the statistical-significance criterion

**Verdict:** There are five stages: design, implementation, documentation, maintenance and retirement. Retirement is not scored. The statistical-significance criterion belongs to **Documentation** in the main text (§4.3) and the full criteria list (App. J.3). The checklist template (App. I.1) contradicts this and lists it under Implementation. Cite it as Documentation, and footnote the inconsistency if needed.

- Venue (arXiv comments): "Accepted as a Spotlight Poster to NeurIPS 2024." Authors: Anka Reuel, Amelia Hardy, Chandler Smith, Max Lamparth, Malcolm Hardy, Mykel J. Kochenderfer.
- URL: https://arxiv.org/html/2411.12990

Quotes:
- Fig. 1 caption: "Five stages of the benchmark lifecycle." App. B headings: "Design.", "Implementation.", "Documentation.", "Maintenance.", "Retirement."
- §4: "Although the retirement stage is within the developer's control, we do not include specific criteria for this phase within the current framework, because we cannot assess the retirement of active benchmarks."
- §4.3 Benchmark Documentation: "Clearly documenting evaluation metric(s) and reporting the statistical significance of results is necessary so that users can understand a benchmark's actual signal [4]."
- App. J.3 (Benchmark Documentation) has the criterion "Report statistical significance of benchmark results for at least one model". Its 15-point level reads: "Benchmark developers run statistical significance tests on the benchmark results for at least one model and provide variance bounds or other uncertainty estimations."
- App. I.1 template, under "Benchmark Implementation": "Statistical significance or uncertainty quantification of benchmark results is reported". This is the inconsistency noted above.
- Results: "benchmarks get an average score of 3.75 on Including a script to replicate results and an average score of 5.62 on Reporting statistical significance." and "14 out of 24 benchmarks did not perform multiple evaluations of the same model or report statistical significance or uncertainty of results."

Reference (NeurIPS 2024 Datasets & Benchmarks proceedings pages and DOI not verified here):
- reuel2024: Reuel A, Hardy A, Smith C, Lamparth M, Hardy M, Kochenderfer MJ. BetterBench: assessing AI benchmarks, uncovering issues, and establishing best practices. arXiv [Preprint]; 2024. arXiv:2411.12990.

---

## 7. Miller 2024, ω² = 1/9

**Verdict: YES.** ω² = 1/9 comes from the continuous-score example in §4.2, and §5 reuses it explicitly. However, the §4.2 arithmetic as printed gives **1/12, not 1/9**. This is a possible error in the source.

- Paper: Evan Miller, "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations", arXiv v1, 2024-11-01. Only v1 exists.
- URL: https://arxiv.org/html/2411.00640

Quotes:
- §4.2: "Suppose an eval uses next-token probabilities to form continuous scores with zero conditional variance, and that these scores are uniformly distributed for two models over the [0,1] interval. Suppose that the model scores have a correlation coefficient of 0.5. Then Var(s_A)=Var(s_B)=1/12 and Cov(x_A,x_B)=0.5√(Var(s_A)Var(s_B))=1/24. In this case, using paired differences will reduce the variance of the estimator by 1/3 in relative terms (that is, from 1/6 to 1/9 in absolute terms)."
- §5: "As a simple example, suppose σ_A²=σ_B²=0 and ω²=1/9, following the conditions described in Section 4.2. Suppose we wish to detect an absolute difference of δ=0.03 at least 80% of the time (β=0.20) with a false-positive rate of 5% (α=0.05). Then the eval will need to contain at least n=(z_0.025+z_0.20)²(1/9)/(0.03)²≈969". I rechecked: 7.849 × (1/9) / 0.0009 ≈ 969.
- §5 second example: "Suppose that σ_A²=σ_B²=1/6 and ω²=1/9, following the conditions of Section 3.1 with an additional assumption that Corr(x_A,x_B)=0.5." Section 3.1 is the *binary* score example (Var(x)=1/12, E[σ²]=1/6), so here 1/9 is used outside the continuous setting.

My own arithmetic check (not a claim from the paper): ω² = Var(x_A)+Var(x_B)−2Cov = 1/12 + 1/12 − 2(1/24) = **1/12**. That is a 1/2 relative reduction from 1/6, not 1/3. The value 1/9 would need Cov = 1/36, which means a correlation of 1/3. If we cite n≈969, we should say it follows Miller's stated ω² = 1/9. Alternatively, recompute with ω² = 1/12, which gives n ≈ 727.

Reference:
- miller2024: Miller E. Adding error bars to evals: a statistical approach to language model evaluations. arXiv [Preprint]; 2024. doi:10.48550/arXiv.2411.00640. arXiv:2411.00640.

---

## 8. Systematic LLM-vs-human label differences

### 8a. Chiang & Lee 2023 (ACL)

**Verdict: NOT SUITABLE as support for "LLM labels systematically differ from experts".** Its headline finding is agreement with experts.

- URL: https://aclanthology.org/2023.acl-long.870/ . Crossref: pages 15607–15631, doi:10.18653/v1/2023.acl-long.870.
- Abstract: "We show that the result of LLM evaluation is consistent with the results obtained by expert human evaluation: the texts rated higher by human experts are also rated higher by the LLMs."
- It is also an LLM-as-*judge* (rating) study, not label generation.

### 8b. Pangakis, Wolken, Fasching 2023 (recommended instead)

**Verdict: CONFIRMED.** This paper supports "LLM-generated labels are task-dependent and need human validation". It shows variable, sometimes poor, per-task performance. It does not show a single systematic directional bias.

- URL: https://arxiv.org/abs/2306.00176 ; https://arxiv.org/html/2306.00176 . arXiv v1 is dated 31 May 2023. No venue was found on the abs page.

Quotes:
- Abstract: "Because these challenges will persist even as LLM technology improves, we argue that any automated annotation process using an LLM must validate the LLM's performance against labels generated by humans."
- Intro: "We use LLMs to replicate 27 different annotation processes from 11 non-public datasets used from articles recently featured in high-impact publications. In total, we classified over 200,000 text samples using an LLM (i.e., GPT-4)."
- Intro: "Our findings indicate that LLM performance for text annotation is promising but highly contingent on both the dataset and the type of annotation task. Across all tasks, we report a median accuracy of 0.850 and a median F1 of 0.707. Despite the strong overall performance, nine of the 27 tasks had either precision or recall below 0.5, which reinforces the necessity of researcher validation."

References:
- pangakis2023: Pangakis N, Wolken S, Fasching N. Automated annotation with generative AI requires validation. arXiv [Preprint]; 2023. doi:10.48550/arXiv.2306.00176. arXiv:2306.00176.
- chiang2023: Chiang CH, Lee HY. Can large language models be an alternative to human evaluations? In: Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers); 2023. p. 15607-15631. doi:10.18653/v1/2023.acl-long.870.
