#import "conference.typ": *
#show: research-paper.with(title: "SkillMerge: A Conditional Guard for Agreement")
#title-block("SkillMerge: A Conditional Guard for Agreement","Compact working paper v21, 2026-10-19. New conditional theorem and deterministic follow-up on an exposed bank; no independent skill history, native benchmark, model/API call, or professor endorsement. Preserved v20 sources and complete v19 scientific record accompany the supplement.")
#abstract-block[#text("Can agreement be promoted without discarding useful evidence? We analyze a reference-blind prefix guard on an already exposed SciFact-derived bank, not a behavioral effect of executable skills. Fixed round-robin and stable common-item promotion orders share an output capacity. The guard accepts promotion when their selected ID sets coincide or promotion preserves either complete input. We prove this condition necessary and sufficient for full-containment no-loss over every reference family making both complete inputs annotation-sufficient; otherwise the policy falls back to round-robin. Among 12,067 such constructed pairs, guarded gain/loss counts are 563/0, 95/0, and 0/0 at capacities one, two, and three. Conservatism discards two promotion gains, while all 22,794 pairs retain 487 losses at capacity one. First-three scoring still fails above capacity three. Frozen computation and separate author verification preserve denominators, counterexamples, and earlier failed checks. Independent skill histories and qualified behavioral effects remain absent.")]

= #text("Introduction")

#text("When two skill changes help separately, their joint availability may still reduce performance. Possible causes include incompatible requirements, context length, lost evidence, changed ranking, or a restrictive grader. We first isolate the last three mechanisms using fixed evidence-ID lists. Agreement denotes repeated IDs, not semantic agreement or independently sampled reasoning. Figure 1 separates this executed diagnostic lane from the still unexecuted skill-authoring and behavioral-evaluation lane.")

#text("The question is which reference-blind switch between round-robin and common-item promotion can guarantee no full-containment regression, assuming each complete input already contains a valid reference alternative. This assumption enables a stronger guarantee than unrestricted references, but is not independently observed usefulness of executable skills. We prove the exact structural boundary, evaluate its conservative fallback, and retain the unprotected all-pair losses.")

#figure(figure-image("figures/overview.svg", 205.667699pt, "skillmerge overview"), kind: image, caption: [#text("Executed evidence-contract diagnostics and prospective behavioral inference are separate. The inherited source audit contains 531 tasks in 325 structural components; 309 evidence-bearing tasks in 204 components feed the current pair bank. Authoring histories, independently qualified pairs, and fresh behavioral effects remain absent. Counts are nested, not independent integration events.")]) <fig-overview>

#text(weight: "bold")[Contributions.]

- #text("An exact reference-blind no-loss certificate for a conditional family of evidence contracts.")
- #text("A guarded promotion policy with a sharp length boundary and explicit failure witnesses.")
- #text("Paired results exposing conservative rejection, endpoint mismatch, and missing behavioral evidence.")

= #text("Related Work")

#text("SciFact and FEVER tie correctness to reference evidence ")#link(<bib1>)[#text("[1,3]")]#text(". The pinned SciFact scorer inspects only three supplied rationale IDs for rationalized abstract correctness ")#link(<bib2>)[#text("[2]")]#text(". ERASER separates human-rationale agreement from predictive faithfulness ")#link(<bib4>)[#text("[4]")]#text("; our annotation containment is not its confidence-based sufficiency. CheckList motivates focused invariance and directional tests ")#link(<bib5>)[#text("[5]")]#text(", here of deterministic contracts.")

#text("Multi-metric evaluation ")#link(<bib6>)[#text("[6,7]")]#text(", construct validity ")#link(<bib8>)[#text("[8,9]")]#text(", underspecification ")#link(<bib11>)[#text("[11]")]#text(", documentation ")#link(<bib12>)[#text("[12]")]#text(", benchmark selection ")#link(<bib13>)[#text("[13]")]#text(", and selection bias ")#link(<bib21>)[#text("[21]")]#text(" motivate explicit score-to-claim boundaries. DSPy compilation ")#link(<bib10>)[#text("[10]")]#text(", SkillCommit replay ")#link(<bib14>)[#text("[14]")]#text(", SkillSmith migration ")#link(<bib15>)[#text("[15]")]#text(", SkillCAT assembly ")#link(<bib16>)[#text("[16]")]#text(", and SkillEvoReg regression tests ")#link(<bib17>)[#text("[17]")]#text(" are substantive unexecuted comparisons. Resource controls ")#link(<bib18>)[#text("[18]")]#text(", SkillsBench v1.1 ")#link(<bib19>)[#text("[19]")]#text(", and self-consistency ")#link(<bib20>)[#text("[20]")]#text(" use different information and budgets; sampled-answer voting is not our ID promotion. All 21 inherited references retain their inspection scopes. New prospective benchmark reading is separated in Supplement S22.")

= #text("Problem and Method")

#text("References form a finite nonempty family of nonempty ID sets. Full containment passes when any complete alternative occurs anywhere in an ordered output. First-three applies containment only to its first three IDs; exact-annotated requires equality with an enumerated alternative. Distinct, in-range input lists A and B are scanned alternately, retaining first occurrences, to produce the complete round-robin order V. Stable promotion P moves common IDs first and preserves V order within both classes; both outputs are capped at k.")

#text("Write X and Y for their selected ID sets. The guard below reads A, B, k only. If it accepts, H returns promotion; otherwise it returns round-robin. References enter only subsequent scoring and descriptive stratification. The conditional reference class requires some alternative wholly inside each complete input, possibly different alternatives. It does not require each k-truncated input to pass.")

#text("For every family in that class, promotion cannot lose full containment exactly when G=1. Sufficiency follows from identical selected sets or retention of an entire sufficient input. Conversely, if all three tests fail, choose a removed baseline ID and an ID outside Y in each input. At most two singleton alternatives make both inputs sufficient, the baseline successful, and promotion unsuccessful. Supplement S16 proves this reverse construction and its quantifiers.")

#text("Thus the guard is maximal only among binary P-or-V switches promising safety for this conditional reference class. It may reject a gain under the actual annotations. For input lengths at most d, where d is at least two, capacity at least 2d-2 always satisfies the guard; a common-last construction shows sharpness at 2d-3. The earlier length-three/cap-four result is a special case. Empty inputs and cap zero are explicit endpoints. No-loss allows both outputs to fail.")

$ G = bb(1)[X = Y or "set"(A) subset.eq Y or "set"(B) subset.eq Y] $

$ H_k = cases(P_k & G = 1, V_k & "otherwise") $

= #text("Experimental Setup")

#text("The unchanged bank contains 309 evidence-bearing tasks, 204 recorded components, 2,494 distinct authored inputs, and 22,794 ordered pairs. Reversed and diagonal pairs are constructed views, not independent histories. Seven capacities yield 159,558 decisions, 478,674 outputs across three policies, and 1,436,022 endpoint cells. They add zero independent observations. Capacity counts output IDs; actual tokens, tools, and authoring costs are unmeasured.")

#text("The fixed both-input annotation-sufficient stratum has 12,067 pairs, 308 tasks, and 203 components. It uses complete original inputs and cannot substitute for held-out Q qualification. Aggregation reports pair-pooled, equal-task, and equal-component means separately. Full, first-three, and exact transitions retain gain, loss, tie, and fallback denominators; false guards remain visible even when falling back produces a score tie.")

#text("A pre-execution plan, two code files, and six consumed sources are hash-frozen. A separately authored implementation reconstructs every output, endpoint cell, and aggregate using scheduled first occurrences and bitmasks. It checks 3,046 authored input pairs across 21,322 pair-cap shapes, including 2,112 explicit rejected-guard counterfamilies, and rejects altered copied inputs and outputs. These are same-author checks, not external replication or independent reference families. Supplement S21 distinguishes this new pass from the preserved earlier failed verifier.")

= #text("Results")

#text("Table 1 compares transitions to the same round-robin baseline. In the sufficient-input stratum, guarded full-containment losses are zero at every capacity. At cap one, fallback removes 1,409 promotion losses while sacrificing two of its 565 gains; 563 gains remain. Cap two retains 95 gains without its 25 losses. Cap three repairs two promotion losses but ties round-robin throughout: it adds no gain over baseline. Fallback counts are 1,502, 29, and two respectively.")

#text("The conditional premise matters. Among all pairs, the guard retains 487 cap-one losses despite 2,361 fallbacks. A minimal authored illustration is A=(0,1), B=(1), with reference {0}. Retaining all of B accepts promotion (1), while round-robin (0) succeeds. B is insufficient, so this is outside the theorem. The saved bank also contains this failure shape. Calling the policy unconditionally safe would be false.")

#text("At caps four through six, full-containment transitions tie, but guarded first-three scoring retains two losses. For A=(1,2,0), B=(4,5,0), and alternatives {1,2} or {4,5}, promotion (0,1,4,2) restores full containment at four while its first three still fail. Figure 2 preserves the original endpoint separation; Supplement S18 visualizes the added guard. Exact scores are separately reported, without inheriting the theorem.")

#text("Weighting remains consequential. Unprotected promotion at cap one in the fixed sufficient-input stratum has pooled contrast -844/12067, approximately -0.06994, but equal-component contrast +3363459013/266277211200, approximately +0.01263. A policy cannot choose its preferred weighting retrospectively. These exposed finite contrasts estimate neither natural pair prevalence nor behavioral composition effects.")

#text("The inherited completion-rank identity explains fixed-order full-containment transitions: the first successful capacity is the minimum, across alternatives, of their last required ID rank. It does not automatically apply to a cap-dependent policy switch. The earlier verifier mistakenly asserted guaranteed success for disjoint sufficient inputs; its frozen failure and corrected no-loss check remain preserved. This revision changes neither those results nor their correction history.")

#result-table(([#text("Cap")],[#text("P all G/L")],[#text("H all G/L")],[#text("P sufficient G/L")],[#text("H sufficient G/L")],[#text("H fallback all/sufficient")],),(([#text("0")],[#text("0 / 0")],[#text("0 / 0")],[#text("0 / 0")],[#text("0 / 0")],[#text("0 / 0")],),([#text("1")],[#text("565 / 2700")],[#text("563 / 487")],[#text("565 / 1409")],[#text("563 / 0")],[#text("2361 / 1502")],),([#text("2")],[#text("95 / 25")],[#text("95 / 0")],[#text("95 / 25")],[#text("95 / 0")],[#text("34 / 29")],),([#text("3")],[#text("0 / 2")],[#text("0 / 0")],[#text("0 / 2")],[#text("0 / 0")],[#text("2 / 2")],),([#text("4..6")],[#text("0 / 0")],[#text("0 / 0")],[#text("0 / 0")],[#text("0 / 0")],[#text("0 / 0")],),),"Full-containment gain/loss versus round-robin. Each row reuses 22,794 all pairs or 12,067 sufficient-input pairs. H denotes guarded promotion. Counts are deterministic transitions, not skill trials.")

#figure(figure-image("figures/capacity-boundary-v19.svg", 269.999764pt, "skillmerge capacity-boundary-v19"), kind: image, caption: [#text("The unchanged capacity audit: full-containment loss counts across output capacities, with a cap-three-to-six zoom contrasting full recovery and persistent first-three losses. Each point reuses the same constructed pair cohort. No curve measures independently qualified skill behavior.")]) <fig-capacity-boundary-v19>

= #text("Limitations")

#text("The guarantee is about complete-input annotation sufficiency and full containment, not semantic truth, actual Q-qualified skills, arbitrary output policies, first-three, or exact matching. Its necessity quantifies over all admissible families; actual annotations may permit a rejected promotion. Stable class order, equal output count, and the declared union construction matter for the length corollary. Compatibility of natural-language requirements needs separate validation.")

#text("Independent A/B histories, Q-qualified skill pairs, reserved-S outcomes, native-method runs, and measured token costs remain absent; the behavioral effect is null. Future evaluation must freeze source-disjoint D/Q/S, candidate rights, resets, total cost, and rejection before fresh outcomes. FollowBench and ManyIFEval offer constraint controls, not missing skill qualification. SkillsBench supplies native task environments, not evidence that this guard improves agents. Supplement S23 states prospective gates and falsification tests.")

= #text("Conclusion")

#text("A reference-blind structural guard exactly characterizes conditional full-containment safety for this binary switch. Its measured benefit is bounded by conservative lost gains, endpoint mismatch, and all-pair failures. Transparent accounting preserves those limits while separating a reproducible evidence-contract result from the independently qualified behavioral study still required.")


#heading(numbering: none)[Acknowledgements]
#text("This work was created as part of the No-More-Slops group activities at Pseudo Lab.")

#heading(numbering: none)[References]

#bibliography-entry(1, [#text("David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi. 2020. Fact or Fiction: Verifying Scientific Claims. Proceedings of EMNLP, 7534–7550.")],"https://aclanthology.org/2020.emnlp-main.609/") <bib1>

#bibliography-entry(2, [#text("Allen Institute for AI. SciFact evaluation implementation, commit 68b98a56d93e0f9da0d2aab4e6c3294699a0f72e. verisci/evaluate/lib/metrics.py and data.py.")],"https://github.com/allenai/scifact/blob/68b98a56d93e0f9da0d2aab4e6c3294699a0f72e/verisci/evaluate/lib/metrics.py") <bib2>

#bibliography-entry(3, [#text("James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. 2018. FEVER: a Large-scale Dataset for Fact Extraction and VERification. Proceedings of NAACL-HLT, 809–819.")],"https://aclanthology.org/N18-1074/") <bib3>

#bibliography-entry(4, [#text("Jay DeYoung, Sarthak Jain, Nazneen Fatema Rajani, Eric Lehman, Caiming Xiong, Richard Socher, and Byron C. Wallace. 2020. ERASER: A Benchmark to Evaluate Rationalized NLP Models. Proceedings of ACL, 4443–4458.")],"https://aclanthology.org/2020.acl-main.408/") <bib4>

#bibliography-entry(5, [#text("Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin, and Sameer Singh. 2020. Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. Proceedings of ACL, 4902–4912.")],"https://aclanthology.org/2020.acl-main.442/") <bib5>

#bibliography-entry(6, [#text("Percy Liang et al. 2023. Holistic Evaluation of Language Models. arXiv:2211.09110v2.")],"https://arxiv.org/abs/2211.09110v2") <bib6>

#bibliography-entry(7, [#text("Aarohi Srivastava et al. 2023. Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models. arXiv:2206.04615v3.")],"https://arxiv.org/abs/2206.04615v3") <bib7>

#bibliography-entry(8, [#text("Timo Freiesleben and Sebastian Zezulka. 2025. The Benchmarking Epistemology: Construct Validity for Evaluating Machine Learning Models. arXiv:2510.23191v1.")],"https://arxiv.org/html/2510.23191v1") <bib8>

#bibliography-entry(9, [#text("Andrew M. Bean et al. 2025. Measuring what Matters: Construct Validity in Large Language Model Benchmarks. arXiv:2511.04703v1.")],"https://arxiv.org/html/2511.04703v1") <bib9>

#bibliography-entry(10, [#text("Omar Khattab et al. 2023. DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines. arXiv:2310.03714v1.")],"https://arxiv.org/html/2310.03714v1") <bib10>

#bibliography-entry(11, [#text("Alexander D’Amour et al. 2022. Underspecification Presents Challenges for Credibility in Modern Machine Learning. Journal of Machine Learning Research, 23(226):1–61.")],"https://jmlr.org/papers/v23/20-1335.html") <bib11>

#bibliography-entry(12, [#text("Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III, and Kate Crawford. 2021. Datasheets for Datasets. arXiv:1803.09010v8.")],"https://arxiv.org/html/1803.09010v8") <bib12>

#bibliography-entry(13, [#text("Mostafa Dehghani, Yi Tay, Alexey A. Gritsenko, Zhe Zhao, Neil Houlsby, Fernando Diaz, Donald Metzler, and Oriol Vinyals. 2021. The Benchmark Lottery. arXiv:2107.07002v1.")],"https://arxiv.org/html/2107.07002v1") <bib13>

#bibliography-entry(14, [#text("Yu He and Weikai Yang. 2026. SkillCommit: Evolving Agent Skills through Behaviorally Validated Scope Expansion. arXiv:2608.15165v1.")],"https://arxiv.org/html/2608.15165v1") <bib14>

#bibliography-entry(15, [#text("Yangbo Wei et al. 2026. SkillSmith: Co-Evolving Skills and Tools for Self-Improving Agent Systems. arXiv:2606.01314v2.")],"https://arxiv.org/html/2606.01314v2") <bib15>

#bibliography-entry(16, [#text("Kunfeng Chen, Qihuang Zhong, Juhua Liu, and Bo Du. 2026. SkillCAT: Contrastive, Assessment-Augmented and Topology-Aware Skill Self-Evolution for LLM Agents. arXiv:2606.13317v2.")],"https://arxiv.org/html/2606.13317v2") <bib16>

#bibliography-entry(17, [#text("Guanyu Nie et al. 2026. SkillEvoReg: Regularizing Agent Skill Evolution Against Overfitting. arXiv:2609.30861v1.")],"https://arxiv.org/html/2609.30861v1") <bib17>

#bibliography-entry(18, [#text("Ziyue Yang and Fan Ding. 2026. Signal or Noise? A Benchmark Study of Agent Skills in Web Development. arXiv:2608.23067v1.")],"https://arxiv.org/html/2608.23067v1") <bib18>

#bibliography-entry(19, [#text("BenchFlow contributors. 2026. SkillsBench v1.1: native task.md package release. Official release artifact.")],"https://github.com/benchflow-ai/skillsbench/releases/tag/v1.1") <bib19>

#bibliography-entry(20, [#text("Xuezhi Wang et al. Self-Consistency Improves Chain of Thought Reasoning in Language Models. Author version arXiv:2203.11171v4, 2023.")],"https://arxiv.org/abs/2203.11171v4") <bib20>

#bibliography-entry(21, [#text("Gavin C. Cawley and Nicola L. C. Talbot. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. JMLR 11(70):2079-2107, 2010.")],"https://jmlr.org/papers/v11/cawley10a.html") <bib21>
