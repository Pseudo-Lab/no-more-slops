#import "conference.typ": *
#show: research-paper.with(title: "SecondChance: Auditing Recovery under Unknown Continuations")
#title-block("SecondChance: Auditing Recovery under Unknown Continuations","Compact working paper v20, 2026-10-19. Reanalysis and presentation of frozen authored evidence; no new model calls, actual audits, independent histories or native-method trials.")
#abstract-block[#text("Correcting an evaluator does not establish recovery of an integrated agent state. SecondChance studies which recovery comparisons remain identified when audits and future state transitions are incomplete. We distinguish worst scenario-conditioned width, the interval union when the continuation scenario is unknown, and its utility-blind pre-outcome maximum. An exact four-case objective yields two causal audit rules; a zero-sum L1 tube adds a common width term under explicit fresh-state conditions. Replaying 168 saved paths from twelve authored templates yields no positive realized ambiguity premium in 1,620 dependent panel views. All sixteen new-rule contracts tie their controls in final safe width; four checkpoint areas improve by 1/192. A late-query control attains width 1/24 rather than 1/12 but has worse uncertainty area. Increasing tube radius includes more of thirteen reused views without establishing calibration. No new audits, model calls or natural histories are added. The contribution is a bounded identification and comparison contract, not demonstrated real-agent recovery superiority.")]

= #text("Introduction")

#text("An evaluator patch can reverse an old rejection while leaving the current system broken. A saved correct candidate may not have been integrated; a harmful lesson may remain active; a valid later change may be lost during repair. Rescoring an archive, invoking a candidate and auditing the integrated state therefore answer different questions. Figure 1 retains this distinction without representing the authored recovery counts as language-model performance.")

#text("We ask a further question: how should an auditor allocate scarce state observations when future commits are unknown? A rule can optimize uncertainty conditional on a forecast while overlooking uncertainty about which forecast applies. A stronger objective can also improve a retrospective diagnostic without improving final information or justifying an operational speedup. The central comparison must separate these possibilities.")

#text("Our contribution is deliberately narrow. We derive three distinct width objectives, implement utility-blind rules for unknown-scenario auditing, and preserve negative results under the same saved histories. The new rules change four intermediate-area summaries but none of sixteen final widths. A simpler delayed rule can win the final-width comparison while losing the area comparison. Complete proofs, causal-access contracts and historical results are routed to Supplement S1-S14; the full prior manuscript is preserved after those additions.")

#figure(figure-image("figures/overview.svg", 194.207855pt, "second_chance overview"), kind: image, caption: [#text("Recovery endpoints after evaluator correction: saved-answer rescoring, fresh candidate invocation and fresh integrated-state audit. The retained counts describe twelve authored histories; they are not model performance estimates or new v20 observations.")]) <fig-overview>

#text(weight: "bold")[Contributions.]

- #text("Three distinct audit-width objectives with exact endpoint and pre-outcome derivations.")
- #text("A transparent causal comparison retaining sixteen final ties and four small area changes.")
- #text("Explicit tube-attainment, information-access and prospective-confirmation boundaries.")

= #text("Related Work")

#text("SkillOpt, Reflexion, Self-Refine and CRITIC change skills, reflective memory or responses under different feedback contracts ")#link(<bib1>)[#text("[1,2,3,4]")]#text(". Intrinsic self-correction and SCoRe additionally differ in external-feedback and training rights ")#link(<bib5>)[#text("[5,6]")]#text(". Verifier selection, temporal memory and environment interaction motivate preserving the candidate, lesson and tool state ")#link(<bib7>)[#text("[7,8,19]")]#text(". None is a native comparator executed in this study.")

#text("Proxy optimization, selection bias and adaptive holdout reuse motivate separating policy decisions from retrospective outcome inspection ")#link(<bib9>)[#text("[9,10,11]")]#text(". Variability and aggregate-evaluation studies motivate explicit experimental units rather than counting repeated views as independent trials ")#link(<bib12>)[#text("[12,13]")]#text(". Performance profiles and COCO motivate distinguishing budget-limited quality, target attainment and nonattainment ")#link(<bib14>)[#text("[14,15,16]")]#text("; our checkpoint area is a declared local summary, not an imported runtime theorem.")

#text("Partial identification separates compatible-value bounds from statistical coverage ")#link(<bib20>)[#text("[20]")]#text(". Adaptive submodularity requires structural conditions that our robust width-reduction objective need not satisfy ")#link(<bib21>)[#text("[21]")]#text(". EvalPlus and SWE-bench are possible future evaluation environments ")#link(<bib17>)[#text("[17,18]")]#text(", not acquired benchmarks or sources of authenticated correction histories here. We retain all twenty-one references and their previously reviewed scopes; no new external effect size or theoretical guarantee is imported.")

= #text("Problem and Method")

#text("Let B be a fixed recovery-cost horizon, t a checkpoint and r=(B-t)/B the remaining fraction. Across twelve equally weighted template pairs, p records the completed-prefix signed state occupations of neutral minus selective recovery. The current arm-frequency difference is d. A complete state has a deterministic fixed-input utility in [0,1]; one cached quote reveals the three fixed-panel utilities of a visible identity. Shared identities use the same utility variable.")

#text("The diagnostic continuation class is c(lambda)=p+lambda*r*d for lambda in [0,1], with endpoints c0=p and c1=p+r*d. It describes persistence followed by cancellation, not a fitted probability model. For an audited set A, first consider the worst remaining width after the scenario is fixed. Its value is W_cond below because the unqueried absolute-coefficient sum is convex in lambda.")

#text("Second, hold the actually revealed utilities fixed while allowing the scenario itself to vary. At endpoint i, Li is the known contribution plus all negative unknown coefficients; Ui adds all positive unknown coefficients instead. Their interval union has width W_union. Known contributions can move with the scenario even when every original utility is known, so W_cond and W_union need not coincide.")

#text("Third, deliberately ignore all utility payloads and maximize W_union over possible audited utilities, including earlier quoted values. This defines F and protects against all quote outcomes in the declared continuation class. Expanding an upper endpoint minus a lower endpoint leaves four ordered endpoint pairs; each known utility is maximized according to its coefficient difference. Supplement S3-S4 supplies the exact separable formula and proof. New one-query and visible-set rules optimize F; their controls optimize W_cond with identical rights and tie rules.")

#text("Restricted objectives also need not have diminishing returns. In a four-state construction, either of two individual quotes has zero immediate worst-width gain, but their combination reduces width by one quarter. A one-query rule can therefore wait while a visible-set rule identifies a useful pair. This is a counterexample to an assumption about this objective, not a refutation of adaptive-submodularity theory or a claim of globally optimal online allocation. Supplement S8 preserves the construction and stopping rules.")

#text("A zero-sum coefficient perturbation with L1 radius epsilon=2*eta*r expands each width and F by exactly epsilon only when freely valued, unaudited fresh coordinates attaining zero and one are allowed. Positive and negative perturbation masses are epsilon/2. With a fixed eta and the same remaining fraction for every candidate, the addition is constant and cannot change rankings. A physically restricted continuation set can invalidate attainment. All actual sign certificates therefore retain the unrestricted prefix-plus-unknown-suffix bound, rather than treating the diagnostic class as established truth.")

$ W_("cond")(A) = max_(i in {0,1}) sum_(s in A^c) abs(c_(i,s)) $

$ W_("union")(A; u_A) = max_(i in {0,1}) U_i - min_(i in {0,1}) L_i $

$ F(A) = max_(u_A in [0,1]^A) W_("union")(A; u_A) $

= #text("Experimental Setup")

#text("We reuse 168 already exposed paths from twelve authored templates and nine complete state identities. Horizons are B=5 and B=8; distinct-state quote caps are one through four. Nine declared causal rules give 72 dependent configurations, including sixteen new-rule contracts paired with corresponding restricted controls. The rules share arrivals and permit at most one visible-state quote per integer checkpoint, with no checkpoint-zero query. An audit never pauses the fixed recovery stream.")

#text("Selectors receive only arrived identities, timestamps, completed-prefix coefficients, current arm frequencies and their own query history. They receive no future commits, final coefficients, utility payloads or program semantics. Replacing hidden payloads while preserving the public prefix leaves decisions unchanged. Visible-set optimization is a static calculation followed by replanning, not a globally optimal causal policy.")

#text("The comparison records final unrestricted safe width, normalized left-step checkpoint-width area, quote count and certificate timing. Area sums widths at checkpoints zero through B-1 and divides by B. Quotes inspect saved values; their units are neither measured audit latency nor tokens. New actual audit executions, model calls, natural histories and independent units are all zero. Exact verification and counterfactual subset checks are distinguished from additional observations in Supplement S12.")

= #text("Results")

#text("The two-state analytic example with endpoint coefficients (1/4,-1/4) and (-1/4,1/4), and known utilities (1,0), has W_cond=0 but W_union=1/2. This establishes a mathematical separation, not observed prevalence. On every one of the 1,620 actual dependent panel views, the realized union premium is zero. Counterfactual pre-outcome objectives can nevertheless differ because they range over unobserved quote outcomes.")

#text("The retained recovery experiment explains why fresh endpoints remain necessary: rescoring succeeds on all twelve saved cases while restoring no integrated state; candidate-selection procedures have twelve development-positive candidates but only four initial-state successes. Those earlier authored counts are not new evidence. A strong neutral joint control also matches selective recovery and has lower cost and collateral loss at budget five. Moving these details to the supplement preserves their constraints on the policy story rather than removing an unfavorable comparator.")

#text("All sixteen paired new-rule contracts tie their restricted controls in final safe width. Four B8 checkpoint areas decrease by exactly 1/192, with the same query checkpoints and quote counts; twelve areas tie. At B8/q3, the one-query objective changes the state chosen at checkpoint five: its safe width changes from 7/8 to 5/6, while later widths coincide. The area difference is therefore (5/6-7/8)/8=-1/192. No additional unaffected-state certificate is obtained.")

#text("Table 1 preserves the timing reversal. At B8/q3, late-prefix queries at six, seven and eight and finishes at width 1/24, whereas FIFO, restricted-set and both union rules finish at 1/12. Yet late-prefix has area 75/64 rather than 37/32, a larger uncertainty burden by 1/64. Its positive unaffected certificate appears only at checkpoint eight. These are different endpoints; neither the smaller final width nor the smaller area alone identifies the better operational policy.")

#text("At eta values 0, 1/8, 1/4, 1/2, 3/4 and 1, the same thirteen dependent nonterminal views have inclusion counts 4, 8, 10, 13, 13 and 13. Figure 2 makes this sensitivity visible alongside the four area changes. Inclusion is retrospective compatibility, not confidence coverage. Choosing eta after inspecting these final coefficients would not establish prospective calibration, and common tube inflation does not explain any policy-ranking improvement.")

#result-table(([#text("B8/q3 rule")],[#text("Quote checkpoints")],[#text("Final width")],[#text("Width area")],[#text("Positive certificate")],),(([#text("FIFO")],[#text("1,2,4")],[#text("1/12")],[#text("37/32")],[#text("Not reached")],),([#text("Restricted one")],[#text("4,5,6")],[#text("1/12")],[#text("223/192")],[#text("Not reached")],),([#text("Restricted set")],[#text("4,5,6")],[#text("1/12")],[#text("37/32")],[#text("Not reached")],),([#text("Union one / set")],[#text("4,5,6")],[#text("1/12")],[#text("37/32")],[#text("Not reached")],),([#text("Late prefix")],[#text("6,7,8")],[#text("1/24")],[#text("75/64")],[#text("Checkpoint 8")],),),"Same exposed paths, three quotes and unrestricted certificates. Width area is a normalized checkpoint summary, not elapsed latency. Supplement S10 retains all sixteen paired contracts.")

#figure(figure-image("figures/ambiguity-sensitivity-v19.svg", 269.999764pt, "second_chance ambiguity-sensitivity-v19"), kind: image, caption: [#text("Left: retrospective inclusion among thirteen dependent nonterminal views. Right: B8 union-minus-restricted checkpoint-area differences scaled by 192, for one-query and visible-set rules. Compatibility is descriptive; signed area differences are cached replay results, not new audit savings.")]) <fig-ambiguity-sensitivity-v19>

= #text("Limitations")

#text("The deterministic fixture was authored by the same research process that exposed its outcomes. Twelve templates, 168 files, repeated checkpoints and three panels do not supply independent natural correction histories. The original neutral-control advantages remain in the preserved manuscript. We claim no superiority over native SkillOpt, Reflexion, learned correction or deployed audit systems.")

#text("Identification requires complete commits, complete state identity and stable fixed-input utilities. Hidden mutation, stochastic audit disagreement or missing positive-duration observations must suspend an unsupported point estimate. The unrestricted suffix remains an outer bound for online information; restricted-segment membership is not assumed. Fresh-coordinate tube attainment need not represent a physically feasible transition process. The finite frontier covers nine declared rules, not all causal policies.")

#text("A confirmatory study must freeze policies and any eta calibration on separate histories, reserve independent correction families, preserve failures and nonattainment, and measure worker calls, failures and elapsed audit cost. Improved retrospective inclusion, checksum agreement or a model critic cannot replace that evidence.")

= #text("Conclusion")

#text("SecondChance separates correcting a saved verdict from identifying current-state recovery, and separates three audit-width questions that can otherwise be conflated. Exact objective changes yield limited intermediate-area effects and no final-width gain in sixteen saved contracts. Delayed auditing trades terminal precision against accumulated uncertainty. Proof conditions, negative results and unchanged natural-evidence gaps are essential parts of the contribution.")


#heading(numbering: none)[Acknowledgements]
#text("This work was created as part of the No-More-Slops group activities at Pseudo Lab.")

#heading(numbering: none)[References]

#bibliography-entry(1, [#text("Yifan Yang et al. SkillOpt: Executive Strategy for Self-Evolving Agent Skills. arXiv:2605.23904v2, 2026.")],"https://arxiv.org/abs/2605.23904v2") <bib1>

#bibliography-entry(2, [#text("Noah Shinn et al. Reflexion: language agents with verbal reinforcement learning. NeurIPS 2023.")],"https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html") <bib2>

#bibliography-entry(3, [#text("Aman Madaan et al. Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS 2023.")],"https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html") <bib3>

#bibliography-entry(4, [#text("Zhibin Gou et al. CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing. ICLR 2024.")],"https://proceedings.iclr.cc/paper_files/paper/2024/hash/fef126561bbf9d4467dbb8d27334b8fe-Abstract-Conference.html") <bib4>

#bibliography-entry(5, [#text("Jie Huang et al. Large Language Models Cannot Self-Correct Reasoning Yet. ICLR 2024.")],"https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html") <bib5>

#bibliography-entry(6, [#text("Aviral Kumar et al. Training Language Models to Self-Correct via Reinforcement Learning. ICLR 2025.")],"https://proceedings.iclr.cc/paper_files/paper/2025/hash/871ac99fdc5282d0301934d23945ebaa-Abstract-Conference.html") <bib6>

#bibliography-entry(7, [#text("Karl Cobbe et al. Training Verifiers to Solve Math Word Problems. arXiv:2110.14168v2, 2021.")],"https://arxiv.org/abs/2110.14168v2") <bib7>

#bibliography-entry(8, [#text("Preston Rasmussen et al. Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv:2501.13956v1, 2025.")],"https://arxiv.org/abs/2501.13956v1") <bib8>

#bibliography-entry(9, [#text("Leo Gao, John Schulman, and Jacob Hilton. Scaling Laws for Reward Model Overoptimization. ICML 2023, PMLR 202:10835–10866.")],"https://proceedings.mlr.press/v202/gao23h.html") <bib9>

#bibliography-entry(10, [#text("Gavin C. Cawley and Nicola L. C. Talbot. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. JMLR 11:2079–2107, 2010.")],"https://jmlr.org/papers/v11/cawley10a.html") <bib10>

#bibliography-entry(11, [#text("Cynthia Dwork et al. Generalization in Adaptive Data Analysis and Holdout Reuse. arXiv:1506.02629v2, 2015.")],"https://arxiv.org/abs/1506.02629v2") <bib11>

#bibliography-entry(12, [#text("Peter Henderson et al. Deep Reinforcement Learning that Matters. AAAI 2018; author version arXiv:1709.06560.")],"https://arxiv.org/abs/1709.06560") <bib12>

#bibliography-entry(13, [#text("Rishabh Agarwal et al. Deep Reinforcement Learning at the Edge of the Statistical Precipice. NeurIPS 2021; author version arXiv:2108.13264v4.")],"https://arxiv.org/abs/2108.13264v4") <bib13>

#bibliography-entry(14, [#text("Elizabeth D. Dolan and Jorge J. Moré. Benchmarking optimization software with performance profiles. Mathematical Programming 91:201–213, 2002.")],"https://link.springer.com/article/10.1007/s101070100263") <bib14>

#bibliography-entry(15, [#text("Nikolaus Hansen et al. COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting. arXiv:1603.08785v4, 2020.")],"https://arxiv.org/abs/1603.08785v4") <bib15>

#bibliography-entry(16, [#text("Nikolaus Hansen, Anne Auger, Dimo Brockhoff, Dejan Tušar, and Tea Tušar. COCO: Performance Assessment. arXiv:1605.03560v1, 2016.")],"https://arxiv.org/abs/1605.03560v1") <bib16>

#bibliography-entry(17, [#text("Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation. NeurIPS 2023.")],"https://proceedings.neurips.cc/paper_files/paper/2023/hash/43e9d647ccd3e4b7b5baab53f0368686-Abstract.html") <bib17>

#bibliography-entry(18, [#text("Carlos E. Jimenez et al. SWE-bench: Can Language Models Resolve Real-world Github Issues? ICLR 2024.")],"https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html") <bib18>

#bibliography-entry(19, [#text("Shunyu Yao et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023; author version arXiv:2210.03629v3.")],"https://arxiv.org/abs/2210.03629v3") <bib19>

#bibliography-entry(20, [#text("G. W. Imbens and C. F. Manski. Confidence Intervals for Partially Identified Parameters. Econometrica72(6):1845-1857,2004.")],"https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2004.00555.x") <bib20>

#bibliography-entry(21, [#text("Daniel Golovin and Andreas Krause. Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization. JAIR 42:427-486, 2011; revised author version arXiv:1003.3967v5, 2017.")],"https://arxiv.org/abs/1003.3967v5") <bib21>
