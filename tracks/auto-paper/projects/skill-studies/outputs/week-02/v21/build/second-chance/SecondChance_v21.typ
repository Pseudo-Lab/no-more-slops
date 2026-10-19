#import "conference.typ": *
#show: research-paper.with(title: "SecondChance: Exact Audit-Schedule Frontiers")
#title-block("SecondChance: Exact Audit-Schedule Frontiers","Compact working paper v21, 2026-10-19. New exact structural schedule analysis of frozen authored streams; no new natural histories, actual audits, independent samples, model calls or native-method trials.")
#abstract-block[#text("Correcting an evaluator does not establish recovery of an integrated agent state. SecondChance distinguishes scenario-conditioned uncertainty, unknown-scenario union uncertainty, and a utility-blind pre-outcome objective. We now compute the complete terminal-safe-width versus checkpoint-area frontier over arrival-feasible audit schedules on fixed recovery streams. An exact audited-set dynamic program and a separate exhaustive verifier agree on 33,658 schedule-contract combinations across eight horizon/cap settings. Each frontier contains one objective point: 28 of 72 saved causal-policy configurations match it and 44 are dominated. At horizon eight with three quotes, hindsight structure attains width 1/24 and area 73/64, dominating both FIFO and delayed auditing. This oracle uses future arrivals and occupations, never utility payloads; it is not an online policy. Prior negative findings remain: all sixteen union-rule final comparisons tie, four areas improve by 1/192, and realized ambiguity premiums are zero in 1,620 dependent views. No natural recovery, statistical coverage, or real audit-speed improvement is established.")]

= #text("Introduction")

#text("An evaluator patch can reverse an old rejection while leaving the current system broken. A saved correct candidate may not have been integrated; a harmful lesson may remain active; a valid later change may be lost during repair. Rescoring an archive, invoking a candidate and auditing the integrated state therefore answer different questions. Figure 1 retains this distinction without representing the authored recovery counts as language-model performance.")

#text("We ask how to allocate scarce state audits when future commits are unknown. Comparing a few declared policies can show a final-width versus uncertainty-area tradeoff without establishing that the tradeoff is unavoidable. We therefore ask a second, retrospective question: on the same fixed recovery streams, can any arrival-feasible schedule jointly improve both endpoints? The answer bounds what the declared schedule contract permits; it does not supply an implementable online rule.")

#text("Our exact structural oracle uses all realized arrivals and occupations but no utility values. Across eight contracts its frontier is a singleton, so the earlier nine-rule timing reversal is not an intrinsic two-objective conflict on these streams. We retain the three uncertainty objectives, negative comparisons, thirteen dependent membership views, and historical recovery controls. Supplement S1-S14 preserves prior derivations; S15-S19 supplies the complete schedule analysis and new reading resources.")

#figure(figure-image("figures/overview.svg", 194.207855pt, "second_chance overview"), kind: image, caption: [#text("Recovery endpoints after evaluator correction: saved-answer rescoring, fresh candidate invocation and fresh integrated-state audit. The retained counts describe twelve authored histories; they are not model performance estimates or new v21 observations.")]) <fig-overview>

#text(weight: "bold")[Contributions.]

- #text("An exact utility-blind structural frontier over every schedule allowed by the fixed arrival and quote contract.")
- #text("Audited-set dynamic programming cross-checked against exhaustive enumeration, preserving all 72 old policy rows and ties.")
- #text("Explicit separation of hindsight structure, online information, prior width distinctions and missing natural-history evidence.")

= #text("Related Work")

#text("SkillOpt, Reflexion, Self-Refine and CRITIC change skills, reflective memory or responses under different feedback contracts ")#link(<bib1>)[#text("[1,2,3,4]")]#text(". Intrinsic self-correction and SCoRe additionally differ in external-feedback and training rights ")#link(<bib5>)[#text("[5,6]")]#text(". Verifier selection, temporal memory and environment interaction motivate preserving the candidate, lesson and tool state ")#link(<bib7>)[#text("[7,8,19]")]#text(". None is a native comparator executed in this study.")

#text("Proxy optimization, selection bias and adaptive holdout reuse motivate separating policy decisions from retrospective outcome inspection ")#link(<bib9>)[#text("[9,10,11]")]#text(". Variability and aggregate-evaluation studies motivate explicit experimental units rather than counting repeated views as independent trials ")#link(<bib12>)[#text("[12,13]")]#text(". Performance profiles and COCO motivate distinguishing budget-limited quality, target attainment and nonattainment ")#link(<bib14>)[#text("[14,15,16]")]#text("; our checkpoint area is a declared local summary, not an imported runtime theorem.")

#text("Partial identification separates compatible-value bounds from statistical coverage ")#link(<bib20>)[#text("[20]")]#text(". Adaptive submodularity requires structural conditions that our robust width-reduction objective need not satisfy ")#link(<bib21>)[#text("[21]")]#text(". EvalPlus and SWE-bench are possible future evaluation environments ")#link(<bib17>)[#text("[17,18]")]#text(", not acquired benchmarks or sources of authenticated correction histories here. We retain all twenty-one references and their previously reviewed scopes; no new external effect size or theoretical guarantee is imported.")

= #text("Problem and Method")

#text("Let B be a fixed recovery-cost horizon, t a checkpoint and r=(B-t)/B the remaining fraction. Across twelve equally weighted template pairs, p records the completed-prefix signed state occupations of neutral minus selective recovery. The current arm-frequency difference is d. A complete state has a deterministic fixed-input utility in [0,1]; one cached quote reveals the three fixed-panel utilities of a visible identity. Shared identities use the same utility variable.")

#text("The diagnostic continuation class c(lambda)=p+lambda*r*d, lambda in [0,1], has endpoints c0=p and c1=p+r*d. It is persistence followed by cancellation, not a probability model. Worst scenario-conditioned width W_cond sums unknown absolute coefficients after fixing the scenario. Actual union width W_union also allows the scenario-dependent known contribution to move. Maximizing that union over every possible audited utility gives a separate utility-blind objective F, with an exact four-endpoint-pair formula in Supplement S3-S4.")

#text("A four-state example violates diminishing returns for the restricted worst-width objective: either singleton quote has zero gain, but their pair reduces width by one quarter. Visible-set rules can exploit such complementarity without being globally optimal online policies. Under a zero-sum L1 tube of radius epsilon=2*eta*r, freely valued fresh coordinates attaining zero and one add exactly epsilon to each width and F. Fixed common inflation therefore cannot change candidate rankings. All certificates still use the unrestricted safe width W_t below.")

#text("For the complete schedule problem, A_t contains identities quoted by checkpoint t. A legal schedule may skip or reveal one not-yet-quoted identity that has actually arrived by each integer t=1..B, using at most q quotes overall. There is no checkpoint-zero quote. Disclosure is instantaneous at a checkpoint and never changes or pauses the recovery stream. Thus terminal queries change W_B but contribute no left-step area.")

#text("Dynamic programming retains the smallest cumulative area for each checkpoint and audited set. Two paths reaching the same state have identical future options and terminal widths; the larger accumulated area cannot improve a continuation. At B, we discard points dominated in both terminal width and area, retaining equal-objective multiplicities and a deterministic schedule witness. This is exact for the fixed structural path and stated clock. Seeing future arrival and occupation structure remains privileged even when the computation is entirely utility-blind.")

$ W_("cond")(A) = max_(i in {0,1}) sum_(s in A^c) abs(c_(i,s)) $

$ W_("union")(A; u_A) = max_(i in {0,1}) U_i - min_(i in {0,1}) L_i $

$ W_(t) (A_t) = sum_(s in A_t^c) abs(p_(t,s)) + 2 (B-t)/B, quad J = (1/B) sum_(t=0)^(B-1) W_(t) (A_t) $

= #text("Experimental Setup")

#text("We reuse 168 exposed paths from twelve authored templates and nine complete state identities. The contrast uses twelve equally weighted neutral/selective pairs per horizon. B is five or eight, and quote caps q range from one to four. All schedules share actual arrivals, the fixed recovery path, globally cached identity quotes and the same instantaneous-disclosure convention. The two horizon streams and nested caps do not create independent trials.")

#text("Selectors receive only arrived identities, timestamps, completed-prefix coefficients, current arm frequencies and their own query history. They receive no future commits, final coefficients, utility payloads or program semantics. Replacing hidden payloads while preserving the public prefix leaves decisions unchanged. Visible-set optimization is a static calculation followed by replanning, not a globally optimal causal policy. The oracle alone sees the full future structural path; its rights differ from every causal rule.")

#text("Before computation we copied plan, analysis, verifier and 172 input files into a new run and sealed hashes. The dynamic program used 4,458 transitions. A separate implementation reconstructed coefficients from integer occupation intervals and exhausted every legal schedule in all eight contracts. It rejected fourteen invalid schedules and exactly reproduced 72 old terminal/area rows. Counts total 33,658 schedule-contract combinations, including nested-cap repeats; at maximum cap there are 25,904 distinct horizon/schedule pairs. No actual audit, natural history, independent unit, model call or physical latency measurement was added.")

= #text("Results")

#text("The two-state analytic example with endpoint coefficients (1/4,-1/4) and (-1/4,1/4), and known utilities (1,0), has W_cond=0 but W_union=1/2. This establishes a mathematical separation, not observed prevalence. On every one of the 1,620 actual dependent panel views, the realized union premium is zero. Counterfactual pre-outcome objectives can nevertheless differ because they range over unobserved quote outcomes.")

#text("Every complete schedule frontier contains one objective point. At B5, the terminal-width/area pairs for q=1..4 are (1/3,31/25), (1/5,6/5), (2/15,6/5), and (1/15,6/5). At B8 they are (1/8,75/64), (1/12,37/32), (1/24,73/64), and (0,217/192). These are exact saved-stream outcomes, not a general theorem that all audit frontiers collapse. Twenty-eight of 72 causal-policy rows match their frontier; 44 are dominated under these two axes and the same cap.")

#text("At B8/q3, the structural witness quotes at checkpoints one, two and four. Its final width is 1/24 and area 73/64, jointly beating FIFO and both union rules at (1/12,37/32). Relative to that witness, their terminal gap is 1/24 and area gap 1/64. Late-prefix matches width 1/24 but has area 75/64, a gap of 1/32. The earlier timing reversal among declared rules remains true, but does not establish a necessary conflict across all schedules. A witness satisfying arrival constraints need not be selectable without future structure.")

#text("At B8/q4, no declared rule reaches the structural point (0,217/192). Current-disagreement spends only two available quotes and remains worse in width and area; unused allowance is preserved. Frontier equality holds for some B5 rules and B8 FIFO at q1/q2. Ties, nonattainment and all 72 comparisons remain explicit in Supplement S18. This two-axis fixed-cap frontier differs from the earlier nine-rule frontier that also minimized realized quote count.")

#text("Prior negative findings remain unchanged. All sixteen union-rule contracts tie restricted controls in final safe width; four B8 checkpoint areas decrease by 1/192 and twelve tie. Late-prefix's unaffected positive certificate still occurs only at checkpoint eight in the B8/q3 case. At eta 0,1/8,1/4,1/2,3/4,1 the same thirteen dependent nonterminal views have inclusion counts 4,8,10,13,13,13. Figure 2 retains this sensitivity: compatibility is not statistical coverage, and uniform inflation cannot improve rankings.")

#text("The earlier recovery controls also remain adverse: rescoring accepts all twelve saved cases while restoring no integrated state, and twelve development-positive candidates yield only four initial-state successes. A neutral joint control matches selective recovery with lower budget-five cost and collateral loss. Those inherited authored observations limit the recovery story; they are not new v21 evidence.")

#result-table(([#text("B8/q3 rule")],[#text("Quote checkpoints")],[#text("Final width")],[#text("Width area")],[#text("Positive certificate")],),(([#text("FIFO")],[#text("1,2,4")],[#text("1/12")],[#text("37/32")],[#text("Not reached")],),([#text("Restricted one")],[#text("4,5,6")],[#text("1/12")],[#text("223/192")],[#text("Not reached")],),([#text("Restricted set")],[#text("4,5,6")],[#text("1/12")],[#text("37/32")],[#text("Not reached")],),([#text("Union one / set")],[#text("4,5,6")],[#text("1/12")],[#text("37/32")],[#text("Not reached")],),([#text("Late prefix")],[#text("6,7,8")],[#text("1/24")],[#text("75/64")],[#text("Checkpoint 8")],),([#text("Structural oracle")],[#text("1,2,4")],[#text("1/24")],[#text("73/64")],[#text("Not optimized")],),),"B8/q3 on the same fixed authored stream and three-quote cap. The last row alone sees future structure and optimizes safe width/area, not sign-certificate timing. Quotes are saved-value inspections; area is not physical latency. Complete frontier points and all causal rows are in Supplement S16-S18.")

#figure(figure-image("figures/ambiguity-sensitivity-v19.svg", 269.999764pt, "second_chance ambiguity-sensitivity-v19"), kind: image, caption: [#text("Left: retrospective inclusion among thirteen dependent nonterminal views. Right: B8 union-minus-restricted checkpoint-area differences scaled by 192, for one-query and visible-set rules. Compatibility is descriptive; signed area differences are cached replay results, not new audit savings.")]) <fig-ambiguity-sensitivity-v19>

= #text("Limitations")

#text("The deterministic fixture was authored by the same research process that exposed its outcomes. Twelve templates, 168 files, repeated checkpoints and three panels do not supply independent natural correction histories. The original neutral-control advantages remain in the preserved manuscript. We claim no superiority over native SkillOpt, Reflexion, learned correction or deployed audit systems.")

#text("Identification requires complete commits, complete state identity and stable fixed-input utilities. Hidden mutation, stochastic audit disagreement or missing positive-duration observations must suspend unsupported point claims. The unrestricted suffix remains a conservative outer bound; restricted-segment membership is not assumed. Fresh-coordinate tube attainment need not be physically feasible. The complete schedule frontier covers only the fixed recovery streams and two stated axes, with no query-duration feedback. It is not an optimum over online policies, altered recovery actions, real latency or other quote prices.")

#text("A confirmatory study must freeze policies and any eta calibration on separate histories, reserve independent correction families, preserve failures and nonattainment, and measure worker calls, failures and elapsed audit cost. Improved retrospective inclusion, checksum agreement or a model critic cannot replace that evidence.")

= #text("Conclusion")

#text("SecondChance separates corrected verdicts from integrated-state recovery and causal audit choices from privileged structural bounds. Exact enumeration shows that the declared-rule timing reversal need not survive a complete schedule comparison on the same stream. It does not identify an online repair: future structure, complete deterministic state, real audit costs and new independent histories remain substantive admission gates.")


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
