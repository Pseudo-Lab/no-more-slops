# R2 citation and fact verification

Verifier pass, 2026-10-25. All checks below were rerun in this pass against primary metadata:
arXiv API (authors, comments, journal-ref), Crossref DOI records (publisher/ACL Anthology metadata),
OpenReview API (venue decisions; DBLP itself blocked automated access, but OpenReview mirrors DBLP
records), PMLR, and full-text PDFs where numbers are quoted. The manuscript was not edited.

Legend: **FIX** = the current line is wrong or incomplete in a way that matters. **ADD** = the current line
is acceptable, and the replacement only adds a venue, pages, or DOI that has now been confirmed.
Entries not listed in section 1 were checked and need no change.

## 1. Corrected reference lines (copy-paste ready)

### FIX (errors in the current line)

- bean2025: Bean AM, Kearns RO, Romanou A, et al. Measuring what matters: construct validity in large language model benchmarks. In: NeurIPS Datasets and Benchmarks Track; 2025. arXiv:2511.04703.
  - The second author is Ryan Othniel Kearns, not "Mahdi A" (arXiv lists 42 authors: Bean, Kearns, Romanou, Hafner, Mayne, ...). The venue is confirmed by the arXiv comment ("NeurIPS 2025 Track on Datasets and Benchmarks").
- gsm8kplatinum: Vendrow E, Vendrow J, Madry A, Beery S. GSM8K-Platinum: revealing performance gaps in frontier LLMs [blog]. 2025 Mar 6. https://gradientscience.org/gsm8k-platinum/ (accessed 2026-10-25).
  - The blog's byline order is Edward Vendrow, Joshua Vendrow, Aleksander Mądry, Sara Beery; the date is Mar 6, 2025.
- kwiatkowski2019: Kwiatkowski T, Palomaki J, Redfield O, et al. Natural Questions: a benchmark for question answering research. Trans Assoc Comput Linguist. 2019;7:453–66. doi:10.1162/tacl_a_00276.
  - Crossref gives pages 453–466, not 452–66.
- chen2025: Chen S, Chen Y, Li Z, et al. Benchmarking large language models under data contamination: a survey from static to dynamic evaluation. In: Proc EMNLP; 2025. p. 10091–109. doi:10.18653/v1/2025.emnlp-main.511. arXiv:2502.17521.
  - The published EMNLP 2025 version has a **different title** (Crossref). The arXiv v2 title is "Recent Advances in Large Langauge Model Benchmarks against Data Contamination: From Static to Dynamic Evaluation" (note the "Langauge" typo on arXiv). Authors per arXiv: Simin Chen, Yiming Chen, Zexin Li, Yifan Jiang, Zhongwei Wan, Yixin He, Dezhi Ran, ... (11). If you prefer to cite the preprint, use: `Chen S, Chen Y, Li Z, et al. Recent advances in large language model benchmarks against data contamination: from static to dynamic evaluation. arXiv:2502.17521. 2025.`
- sainz2023: Sainz O, Campos JA, García-Ferrero I, Etxaniz J, Lopez de Lacalle O, Agirre E. NLP evaluation in trouble: on the need to measure LLM data contamination for each benchmark. In: Findings of EMNLP; 2023. p. 10776–87. doi:10.18653/v1/2023.findings-emnlp.722.
  - Findings of EMNLP **2023** is confirmed by Crossref/ACL Anthology. The arXiv comment says "Accepted at EMNLP2024-Findings", which is a typo on arXiv; do not follow it.
- thomas2024: Thomas P, Spielman S, Craswell N, Mitra B. Large language models can accurately predict searcher preferences. In: Proc SIGIR; 2024. p. 1930–40. doi:10.1145/3626772.3657707. arXiv:2309.10621.
  - The key says 2024 but the line says 2023. The published version is SIGIR 2024 (Crossref, issued 2024-07-10).
- luccioni2022: Luccioni AS, Corry F, Sridharan H, Ananny M, Schultz J, Crawford K. A framework for deprecating datasets: standardizing documentation, identification, and communication. In: Proc ACM FAccT; 2022. p. 199–212. doi:10.1145/3531146.3533086. arXiv:2111.04424.
  - Note: the arXiv record shows the DOI 10.1145/1122445.112, which is an ACM template placeholder. Do not use it. Crossref confirms the DOI above.

### ADD (venue, pages, or DOI now confirmed)

- gema2024: Gema AP, Leang JOJ, Hong G, et al. Are we done with MMLU? In: Proc NAACL; 2025. p. 5069–96. doi:10.18653/v1/2025.naacl-long.262. arXiv:2406.04127.
  - The first three authors are spelled correctly (Aryo Pradipta Gema, Joshua Ong Jun Leang, Giwon Hong; 16 authors). NAACL 2025 Long is confirmed by Crossref. Consider renaming the key to gema2025 (optional; renaming the key requires updating source.md).
- chang2024: Chang Y, Wang X, Wang J, et al. A survey on evaluation of large language models. ACM Trans Intell Syst Technol. 2024;15(3):1–45. doi:10.1145/3641289. arXiv:2307.03109.
  - Crossref: vol 15, issue 3, pages 1–45, issued 2024-03-29. The article number "39" was not returned by Crossref, so it is omitted.
- rein2023: Rein D, Hou BL, Stickland AC, et al. GPQA: a graduate-level Google-proof Q&A benchmark. In: Proc COLM; 2024. arXiv:2311.12022.
  - COLM 2024 is confirmed by OpenReview (venueid colmweb.org/COLM/2024/Conference).
- panickssery2024: Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. In: Proc NeurIPS; 2024. arXiv:2404.13076.
  - NeurIPS 2024 (oral) is confirmed by OpenReview.
- jain2024: Jain N, Han K, Gu A, et al. LiveCodeBench: holistic and contamination free evaluation of large language models for code. In: Proc ICLR; 2025. arXiv:2403.07974.
  - ICLR 2025 (poster) is confirmed by OpenReview.
- liu2023: Liu J, Xia CS, Wang Y, Zhang L. Is your code generated by ChatGPT really correct? Rigorous evaluation of large language models for code generation. In: Proc NeurIPS; 2023. arXiv:2305.01210.
  - NeurIPS 2023 is confirmed by OpenReview (NeurIPS.cc/2023/Conference poster, plus the DBLP mirror).
- oren2023: Oren Y, Meister N, Chatterji N, Ladhak F, Hashimoto TB. Proving test set contamination in black-box language models. In: Proc ICLR; 2024. arXiv:2310.17623.
  - ICLR 2024 (oral) is confirmed by OpenReview. The ICLR title hyphenates "Black-Box".
- recht2019: Recht B, Roelofs R, Schmidt L, Shankar V. Do ImageNet classifiers generalize to ImageNet? In: Proc ICML (PMLR 97); 2019. arXiv:1902.10811.
  - Confirmed at proceedings.mlr.press/v97/recht19a.html ("Proceedings of the 36th International Conference on Machine Learning"). Page numbers were not extracted, so they are omitted.
- shankar2024: Shankar S, Zamfirescu-Pereira JD, Hartmann B, Parameswaran AG, Arawjo I. Who validates the validators? Aligning LLM-assisted evaluation of LLM outputs with human preferences. In: Proc ACM UIST; 2024. p. 1–14. doi:10.1145/3654777.3676450. arXiv:2404.12272.
  - UIST 2024 is confirmed by Crossref.
- es2023: Es S, James J, Espinosa-Anke L, Schockaert S. RAGAs: automated evaluation of retrieval augmented generation. In: Proc EACL System Demonstrations; 2024. p. 150–8. doi:10.18653/v1/2024.eacl-demo.16. arXiv:2309.15217.
  - EACL 2024 demo is confirmed by Crossref.
- tang2024: Tang Y, Yang Y. MultiHop-RAG: benchmarking retrieval-augmented generation for multi-hop queries. In: Proc COLM; 2024. arXiv:2401.15391.
  - COLM 2024 is confirmed by OpenReview.
- li2024: Li T, Chiang WL, Frick E, et al. From crowdsourced data to high-quality benchmarks: Arena-Hard and BenchBuilder pipeline. In: Proc ICML; 2025. arXiv:2406.11939.
  - ICML 2025 (poster) is confirmed by OpenReview.
- truong2025: Truong S, Tu Y, Hardy M, et al. Fantastic bugs and where to find them in AI benchmarks. In: NeurIPS Datasets and Benchmarks Track; 2025. arXiv:2511.16842.
  - The authors are correct (Sang Truong, Yuheng Tu, Michael Hardy, Anka Reuel, ...; 11 authors). The venue is confirmed by OpenReview (NeurIPS 2025 D&B poster).
- bavaresco2025: Bavaresco A, Bernardi R, Bertolazzi L, et al. LLMs instead of human judges? A large scale empirical study across 20 NLP evaluation tasks. In: Proc ACL (Short Papers); 2025. p. 238–55. doi:10.18653/v1/2025.acl-short.20. arXiv:2406.18403.
  - The authors are correct (20 authors: Bavaresco, Bernardi, Bertolazzi, Elliott, Fernández, Gatt, ...). Crossref shows it is an ACL 2025 **short** paper.
- gebru2021: Gebru T, Morgenstern J, Vecchione B, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86–92. doi:10.1145/3458723. arXiv:1803.09010.
  - DOI, volume, issue, and pages are confirmed by Crossref (7 authors).
- pushkarna2022: Pushkarna M, Zaldivar A, Kjartansson O. Data cards: purposeful and transparent dataset documentation for responsible AI. In: Proc ACM FAccT; 2022. p. 1776–826. doi:10.1145/3531146.3533231. arXiv:2204.01075.
  - The DOI from memory is correct (Crossref).
- buckley2007: Buckley C, Dimmick D, Soboroff I, Voorhees E. Bias and the limits of pooling for large collections. Inf Retr. 2007;10(6):491–508. doi:10.1007/s10791-007-9032-x.
  - Volume, issue, and pages are confirmed by Crossref, and the DOI is added.
- cabitza2023: Cabitza F, Campagner A, Basile V. Toward a perspectivist turn in ground truthing for predictive computing. In: Proc AAAI; 2023;37(6):6860–8. doi:10.1609/aaai.v37i6.25840.
- bowman2021: no change (Crossref confirms pp. 4843–55).
- saadfalcon2024: Saad-Falcon J, Khattab O, Potts C, Zaharia M. ARES: an automated evaluation framework for retrieval-augmented generation systems. In: Proc NAACL; 2024. p. 338–54. doi:10.18653/v1/2024.naacl-long.20. arXiv:2311.09476.
- rahmani2024: Rahmani HA, Craswell N, Yilmaz E, Mitra B, Campos D. Synthetic test collections for retrieval evaluation. In: Proc SIGIR; 2024. p. 2647–51. doi:10.1145/3626772.3657942. arXiv:2405.07767.
- wang2023: Wang Y, Kordi Y, Mishra S, et al. Self-Instruct: aligning language models with self-generated instructions. In: Proc ACL; 2023. p. 13484–508. doi:10.18653/v1/2023.acl-long.754. arXiv:2212.10560.
- nie2020: Nie Y, Williams A, Dinan E, Bansal M, Weston J, Kiela D. Adversarial NLI: a new benchmark for natural language understanding. In: Proc ACL; 2020. p. 4885–901. doi:10.18653/v1/2020.acl-main.441. arXiv:1910.14599.
- ribeiro2020: Ribeiro MT, Wu T, Guestrin C, Singh S. Beyond accuracy: behavioral testing of NLP models with CheckList. In: Proc ACL; 2020. p. 4902–12. doi:10.18653/v1/2020.acl-main.442. arXiv:2005.04118.
- gururangan2018: Gururangan S, Swayamdipta S, Levy O, Schwartz R, Bowman SR, Smith NA. Annotation artifacts in natural language inference data. In: Proc NAACL; 2018. p. 107–12. doi:10.18653/v1/N18-2017. arXiv:1803.02324.
- gao2023: Gao T, Yen H, Yu J, Chen D. Enabling large language models to generate text with citations. In: Proc EMNLP; 2023. p. 6465–88. doi:10.18653/v1/2023.emnlp-main.398. arXiv:2305.14627.
- card2020: Card D, Henderson P, Khandelwal U, Jia R, Mahowald K, Jurafsky D. With little power comes great responsibility. In: Proc EMNLP; 2020. p. 9263–74. doi:10.18653/v1/2020.emnlp-main.745. arXiv:2010.06595.
- chen2024rgb: Chen J, Lin H, Han X, Sun L. Benchmarking large language models in retrieval-augmented generation. In: Proc AAAI; 2024;38(16):17754–62. doi:10.1609/aaai.v38i16.29728. arXiv:2309.01431.
- swebenchverified: OpenAI. Introducing SWE-bench Verified [blog]. 2024 Aug 13. https://openai.com/index/introducing-swe-bench-verified/ (archived: https://web.archive.org/web/20240909063313/https://openai.com/index/introducing-swe-bench-verified/; accessed 2026-10-25).
- **NEW (needed for fact 2a, see below)** epochswebench: Epoch AI. SWE-bench Verified [benchmark page]. https://epoch.ai/benchmarks/swe-bench-verified (accessed 2026-10-25).

### Checked, no change needed

rebholz2010 (Crossref: Rebholz-Schuhmann D, Jimeno Yepes AJ, van Mulligen EM, ... 10 authors; 8(1):163–79; DOI ok) · akhtar2024 (Akhtar, Benjelloun, Conforti, ...; 31 authors; NeurIPS 2024 D&B confirmed by arXiv comment and OpenReview) · jain2024rai (Nitisha Jain, Mubashara Akhtar, Joan Giner-Miguelez, ...; 18 authors; no venue, so arXiv only is correct) · liang2023 (Liang, Bommasani, Lee; TMLR 2023 per arXiv journal-ref) · srivastava2022 (first three: Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao; TMLR via OpenReview uyTL5Bvosj. The arXiv journal-ref says "May/2022", which looks wrong; DBLP/OpenReview list TMLR 2023. Keeping 2023 is reasonable) · northcutt2021 · vendrow2025 (no archival venue; only a NeurIPS 2024 SafeGenAI workshop version exists, under a different title) · yu2024 · gan2025 · xu2024 · reuel2024 · arora2025 · bajaj2016 · zhao2024 · white2025 · zhang2024 · thakur2021 · upadhyay2024 · yang2024 · kiela2021 · artstein2008 · pavlick2019 · plank2022 · aroyo2015 · miller2024 · polo2024 · raji2021 · zheng2023 · thakur2025 (ACL Anthology 2025.gem-1.33, pp. 404–430) · voorhees2000 · bender2018 · krippendorff2004 · grey-literature entries (openai-evals, anthropic-evals, husain-evals, neurips2026rai; their access dates were not re-opened in this pass).

## 2. Fact verdicts

**a. SWE-bench Verified (source.md ¶ line 35, line 80)**
- 93 developers / 1,699 / 500: **CONFIRMED, with a nuance.** The archived OpenAI post (13 Aug 2024; https://web.archive.org/web/20240909063313/https://openai.com/index/introducing-swe-bench-verified/) says: "We worked with 93 software developers experienced in Python to manually screen SWE-bench samples for quality. We annotated 1,699 random samples from the SWE-bench test set". It also refers to "professional software developers". The nuance is that 500 is not simply "what remained". The post says "68.3% of SWE-bench samples being filtered out", and the 500 were then drawn from the survivors: "We include as many samples with difficulty 1-4 hours and >4 hours as possible, and then we randomly sample the remainder to arrive at the 500 samples". Suggested wording: "…검토하여 부적격 항목(68.3%)을 걸러낸 뒤 남은 항목에서 500개를 선정하였다".
- "검증을 거친 집합도 실행 환경이 바뀌면 일부 문항이 재현되지 않는다" [@swebenchverified]: **CORRECTED (citation).** The OpenAI post does not say this about Verified itself. It only says that unreliable environment setup affected the original SWE-bench. The supporting source is Epoch AI (https://epoch.ai/benchmarks/swe-bench-verified): "We exclude 16 samples that do not reliably run in our infrastructure. Typical issues we have observed include tests that require network access"; "Epoch evaluations of this benchmark use 484 samples"; "GPT-5 used 477 tasks, and Sonnet-3.7 used 489 tasks." Cite the new `epochswebench` entry here instead of, or in addition to, swebenchverified.

**b. Krippendorff thresholds: CONFIRMED.** Primary source: Krippendorff K. Reliability in content analysis: some common misconceptions and recommendations. Hum Commun Res. 2004;30(3):411–33 (doi:10.1111/j.1468-2958.2004.tb00738.x; Penn postprint https://repository.upenn.edu/handle/20.500.14332/1886, p. 12 of the PDF): "I suggested elsewhere to require α ≥ .800, and where tentative conclusions are still acceptable, α ≥ .667 (Krippendorff, 2004, p. 241)." This confirms that the book citation (krippendorff2004, p. 241) is the correct anchor; consider adding "p. 241" to the in-text cite. Artstein & Poesio 2008 (p. 576) also reports the .8 and .67 convention via Carletta 1996, and notes that Krippendorff later called even α = .800 "a pretty low standard" (2004a, p. 242). The 2011 "Computing Krippendorff's Alpha-Reliability" note does not state these thresholds.

**c. HealthBench: CONFIRMED** (arXiv 2505.08775v1). Abstract: rubrics "created by 262 physicians" and "48,562 unique rubric criteria". p. 18: "both physician-physician and model-physician agreements range from 55% to 75%". This refers to grading of the 34 consensus criteria, and agreement is measured as macro F1 (Fig. 12). Table 6: GPT-4.1 grader MF1 = 0.709, the best of the graders tested (o4-mini 0.692, o3 0.681). Optional precision for the manuscript: "합의 기준 채점에서 (macro F1 기준)".

**d. Bean et al. 2025: CONFIRMED** (arXiv 2511.04703, p. 5). "systematic review of 445 LLM benchmarks"; "16.0% used uncertainty estimates or statistical tests to compare the results"; "Most of the articles provided a definition of their measured phenomenon (78.2%). Of the articles that provided definitions, 52.2% … are widely agreed upon, but 47.8% are contested". The manuscript wording ("측정 대상을 정의한 벤치마크의 47.8%") is accurate. Caution: the earlier search-snippet claim "~half test abstract phenomena without clear definitions" is not the paper's wording.

**e. Thakur et al. 2025: CONFIRMED** (arXiv 2406.12624v6 abstract): "only the best (and largest) models show reasonable alignment with humans, though they still differ with up to 5 points from human-assigned scores." Body: for judges with Scott's π > 80, scores differ "up to 5 points". The paper also notes that judges with high *percent agreement* "can still give scores that differ 10-20 points". The points are on the exam-taker accuracy scale (0–100).

**f. GSM8K-Platinum: CONFIRMED** (https://gradientscience.org/gsm8k-platinum/, Mar 6 2025): "We then manually inspected the 219 flagged questions, of which 110 were removed, 99 were verified, and 10 had mislabeled answers that were corrected." "both Claude 3.7 Sonnet (extended thinking) and Llama 405B showed identical error counts of 45 each on GSM8K… On GSM8K-Platinum, however, Claude 3.7 Sonnet (extended thinking) shows only 2 errors compared to Llama 405B's 17". "15 benchmarks" and "lower bound" are confirmed in arXiv 2502.03461: "platinum versions of fifteen 'saturated' benchmarks"; "the number of errors that we identify … is only a lower bound, as our approach could miss any bad question for which all LLM solutions happen to agree with the benchmark solution."

**g. Zheng et al. 2023: CONFIRMED** (arXiv 2306.05685 abstract): "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans."

**h. Miller 2024: CONFIRMED, with a nuance** (arXiv 2411.00640). Table 4: DROP SE_clustered 1.34 vs naive 0.44, ratio **3.05** ("clustered standard errors can be over 3X larger than naive standard errors"). p. 9–10: "Suppose we wish to detect an absolute difference of δ = 0.03 at least 80% of the time (β = 0.20) with a false-positive rate of 5% (α = 0.05)… n = (z0.025 + z0.20)²(1/9)/(0.03)² ≈ 969 independent questions. Although these parameters are fictional, they are reasonable, and suggest that new evals should contain at least 1,000 questions". So yes, the ~969 example uses δ = 3 pp, but it assumes a paired design, ω² = 1/9 and σ² = 0, and Miller calls the parameters "fictional". Suggested wording: "…가정한 예시에서 약 969개(따라서 최소 1,000개 권고)의 독립 문항이 필요하였다". The manuscript's "약 3.05배" and "약 1,000문항" are accurate.

**Also spot-checked in the abstracts (CONFIRMED):** Recht 2019 "11% - 14% on ImageNet"; Liu 2023 "reducing the pass@k by up-to 19.3-28.9%"; Truong 2025 "up to 84% precision" (across nine benchmarks).

**UNRESOLVED:** none of items a–h. Remaining gaps: the PMLR page range for recht2019 and the TIST article number for chang2024 were not extracted, so both are omitted rather than guessed.
