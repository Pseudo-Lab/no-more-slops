# R4 — Round-2 fact checks against primary sources

Checked 2026-10-25. The arXiv HTML pages, the Nature HTML page, the simple-evals GitHub repo and the Hugging Face API were read directly. The OpenAI blog returns 403, so it was read from the Wayback snapshot 20261015182204.

## 1. SimpleQA (arXiv 2411.04368v1, the only version)

URL: https://arxiv.org/html/2411.04368 (§2.2 "Quality", §2.3 "Dataset diversity")

**(a) Chance-corrected IAA: NOT REPORTED.** The paper never mentions Cohen's κ, Krippendorff's α, or any "kappa" or "agreement coefficient". The only agreement mechanisms are:
- An agreement filter between two trainers: "we removed questions from the dataset if answers from two trainers didn't agree according to a prompted ChatGPT classifier, or if the second trainer said the question wasn't timeless or didn't have an indisputable answer."
- A requirement for two distinct source domains: "we also only kept questions for which there were two unique website domain names among the 2–4 sources found by the two AI trainers".
- A spot check with a third trainer: "randomly selecting 1,000 examples and having them answered by a third trainer. … the performance of the third trainer was 94.4%."
- A grader check, which is not an IAA measure: "Of 100 correct, 100 incorrect, and 100 not attempted completions we manually read, we only found two disagreements with the prompted grader."

**(b) Topics: CONFIRMED. There are 10 topics, tagged post hoc with ChatGPT.** Figure 1 gives the counts below. They sum to 4,326, which matches "contains 4,326 short, fact-seeking questions".
Science & technology 858 (19.8%), Politics 709 (16.4%), Art 550 (12.7%), Other 475 (11.0%), Geography 424 (9.8%), Sports 368 (8.5%), Music 341 (7.9%), TV shows 293 (6.8%), History 173 (4.0%), **Video games 135 (3.1%) is the smallest.**
Text quote: "SimpleQA contains questions from a diverse range of topics, which we tagged post-hoc with ChatGPT. The most common topics were Science & Technology (n=858), Politics (n=709), and Art (n=550)."

**(c) Data card, held-out split and errata: NONE FOUND.**
- OpenAI distributes the data only as a CSV at `https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv`. The reference is in `simpleqa_eval.py` at https://github.com/openai/simple-evals.
- The README entry gives only the reference link and the license: "SimpleQA: Measuring short-form factuality in large language models, reference: https://openai.com/index/introducing-simpleqa, MIT License".
- The README also carries this notice: "**July 2025**: `simple-evals` will no longer be updated for new models or benchmark results. The repo will continue to host reference implementations for HealthBench, BrowseComp, and SimpleQA."
- The Hugging Face listing for the `openai` author (https://huggingface.co/api/datasets?author=openai) has gsm8k, healthbench, MMMLU and others, but **no SimpleQA**. All the SimpleQA copies on HF are third-party mirrors (e.g. basicv8vc/SimpleQA).
- The paper does not mention a private or held-out split, a versioning policy or errata. arXiv has only v1.
- The closest thing to errata comes from a third party: Google DeepMind's **SimpleQA Verified** (arXiv 2509.07968; https://huggingface.co/datasets/google/simpleqa-verified), described as "A 1,000-prompt factuality benchmark … designed to reliably evaluate LLM parametric knowledge."

**(d) Error-rate wording: CONFIRMED, quoted in full.** The 2.8% is 28 of the 1,000 sampled items: 56 graded incorrect, minus 15 grader false negatives, minus 13 trainer errors.
> "Of the 5.6% of answers (56/1000) classified as incorrect by the prompted ChatGPT grader, we did a manual examination of all examples and found that fifteen were false negatives from the autograder. Of the remaining 41 (4.1%) actually incorrect answers, we found that seven were due to the third trainer not answering the question fully … and six were due to the third trainer giving an answer that contradicted the source they cited … The remaining 2.8% of the errors from the third trainer revealed real issues with the data. Hence, we estimate that the error rate of our benchmark is around 3%, assuming no false positives from the prompted ChatGPT grader."

## 2. HealthBench (arXiv 2505.08775)

URL: https://arxiv.org/html/2505.08775 (§8.1, Table 5, Fig. 12, Table 6)

**Verdict: 0.569–0.730 is the range of per-theme weighted-average physician MF1 across the 7 themes.** It is not a range across individual physicians. The individual physicians' scores appear only as dots in Fig. 12, with no numeric range given.
- Caption of Table 5: "Physician weighted average MF1 score and model (GPT-4.1) MF1 score on meta-examples, grouped by theme. For each theme we show the number of physicians evaluated, the average MF1 score across those physicians, and the model MF1 as an absolute score and as a percentile of physician scores."
- Method: "We report average physician MF1 score per theme, weighted by number of meta-examples per physician, in Table 5."
- The minimum is Response depth (34 physicians, 0.569; model 0.572, 58.8th percentile). The maximum is Health data tasks (32 physicians, 0.730; model 0.683, 37.5th percentile).
- Caption of Fig. 12: "Physician MF1 score per theme (one gray dot per physician) compared to model-based grader score (GPT-4.1)."
- Overall GPT-4.1 grader MF1 of **0.709: CONFIRMED.** Table 6, "Meta-evaluation MF1 score by grader model", lists "GPT-4.1 0.709; o4-mini 0.692; o3 0.681; GPT-4.1 mini 0.661; GPT-4.1 nano 0.580".
- Consensus criteria: **CONFIRMED, 34 criteria.** "We focus on the 34 pre-defined consensus rubric criteria … we obtain over 60,896 meta-examples, with an average of 1791 meta-examples per criterion (with a minimum of 1,072 and a maximum of 3,370)." The limitations section adds: "We studied quality of model-based grading via meta-evaluation against physician grading, but only on consensus criteria".
- MF1 is computed **per criterion**: "MF1 is computed per criterion". The 34 criteria are grouped into 7 themes.
- A related caveat in the limitations: "both physician-physician and model-physician agreements range from 55% to 75%."

## 3. GSM1k (arXiv 2405.00332)

URL: https://arxiv.org/html/2405.00332

**Verdict: absolute percentage points.** The text does not say "absolute", but Appendix Table 1 shows that "Diff" is the raw difference in accuracy.
- Abstract: "we observe accuracy drops of up to 8%".
- Conclusion: "with models showing performance drops of up to 8% accuracy."
- Introduction: "the worst models performing 8% worse on GSM1k compared to GSM8k".
- Table 1 ("Standard Prompt"), top row: "Yi-6B-Chat | Diff 0.080 | GSM8k 0.437 | GSM1k 0.357". 0.437 − 0.357 = 0.080, so the gap is 8 pp. As a relative drop it would be about 18%.
- The paper also says: "every percentage point difference in GSM8k and GSM1k performance is associated with…"

## 4. Bean et al. 2025, "Measuring what matters" (arXiv 2511.04703)

URL: https://arxiv.org/html/2511.04703 (§3 Recommendations)

**Verdict: CONFIRMED. There are 8 recommendations, and they map one-to-one onto your list in the same order.**
1. 3.1 **Define the phenomenon**
2. 3.2 **Measure the phenomenon and only the phenomenon** (the checklist box is titled "Measure only the phenomenon")
3. 3.3 **Construct a representative dataset for the task**
4. 3.4 **Acknowledge limitations of reusing datasets**
5. 3.5 **Prepare for contamination**. Its checklist includes "Maintain a held-out set of task items to facilitate ongoing, uncontaminated evaluation".
6. 3.6 **Use statistical methods to compare models**
7. 3.7 **Conduct an error analysis**
8. 3.8 **Justify construct validity**

Scope: "a systematic review of 445 benchmarks … annotated by 29 experts". Each recommendation "includes a specific checklist of items".

## 5. HLE (Nature, doi:10.1038/s41586-025-09962-4, published 28 Jan 2026; arXiv 2501.14249v12)

URLs: https://www.nature.com/articles/s41586-025-09962-4 (Methods, "Expert disagreement rate") and https://arxiv.org/html/2501.14249 (App. B.3)

**18% sentence: it cites FutureHouse (Skarlinski et al. 2025). CONFIRMED.**
- Nature: "Disagreement rates are often higher in domains such as health and medicine. A targeted peer review on a biology, chemistry and health subset, proposed in ref. 63, found an expert disagreement rate of approximately 18%."
- Nature ref. 63: "Skarlinski, M., Laurent, J., Bou, A. & White, A. About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong. *FutureHouse*", https://www.futurehouse.org/research-announcements/hle-exam
- arXiv v12 has the same sentence, with "We conducted another targeted peer review … as proposed by [47]". [47] is the same Skarlinski/FutureHouse post.
- Both versions add: "if we were to adopt a single-reviewer methodology … the disagreement rate on the aforementioned health-focused subset jumps from 18% to 25%, which is close to the setting described in [47]" (Nature: "…close to the approximate numbers and method from ref. 63").

**15.4%: CONFIRMED, but the audit was done BEFORE release.**
- Nature: "Before release, we conducted two main rounds of auditing, each on a sample of 200 questions. … This iterative process yielded a final estimated expert disagreement rate of 15.4% for the public set."
- arXiv: "Prior to release, we conducted two main rounds of auditing…"

**Timing of the 18% review:** the paper does not date it explicitly. It must have come after release, because it follows a proposal in a FutureHouse post that critiques the released dataset. In Nature, the "Expert disagreement rate" subsection is a sibling of the "Post-release" subsection, not part of it. In arXiv it sits under "B.3 Expert Disagreement Rate and HLE-Rolling".

**Other post-release items:**
- A bug bounty: "we opened up a community feedback bug bounty program following the initial release".
- A held-out private set: "a second held-out private set which will be used in future evaluations".
- HLE-Rolling: "a dynamic fork of the dataset post-release: HLE-Rolling".

## 6. Shankar et al. 2024, "Who Validates the Validators?" / EvalGen (arXiv 2404.12272v1)

URL: https://arxiv.org/html/2404.12272 (§6 User Study)

**Verdict: CONFIRMED, there were nine participants.**
- "we asked nine industry practitioners who had prior experience with LLMs to use EvalGen and think aloud."
- "We recruited nine industry practitioners via a Twitter post … We selected the first nine who had experience coding and building LLM pipelines for some company or product."

## 7. OpenAI, "Why SWE-bench Verified no longer measures frontier coding capabilities" (23 Feb 2026)

URL: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/, which returns 403. It was read via https://web.archive.org/web/20261015182204/https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/.

- The headline is as given above. The HTML `<title>` is "Why we no longer evaluate SWE-bench Verified | OpenAI". The subtitle is "SWE-bench Verified is increasingly contaminated. We recommend SWE-bench Pro."

**o3 phrase: CONFIRMED.**
> "We conducted an audit of 138 SWE-bench Verified problems that OpenAI o3 did not consistently solve over 64 independent runs. Each case was independently reviewed by at least six experienced software engineers. If an expert flagged an issue, it was re-verified by an additional team."
> "We found that 59.4% of the 138 problems contained material issues in test design and/or problem description, rendering them extremely difficult or impossible even for the most capable model or human to solve."

Summary wording: "We audited a 27.6% subset of the dataset that models often failed to solve and found that at least 59.4% of the audited problems have flawed test cases that reject functionally correct submissions".

**Contamination: CONFIRMED.**
> "In our analysis we found that all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics for certain tasks, indicating that all of them have seen at least some of the problems and solutions during training."

Models probed:
> "For each SWE-bench Verified question, we tasked GPT‑5 with probing a GPT‑5.2‑Chat, Claude Opus 4.5 and Gemini 3 Flash Preview for contamination. These models were chosen to exclude reasoning models…"

The probing used "15 turns", with a judge labeling severity "from 'none' to 'strong'". The authors then "manually reviewed the 'strong' examples".

Own-model signal:
> "We first encountered signs of contamination in our own models. For example, when GPT‑5.2 solved 31 tasks we identified to be almost impossible to solve."
