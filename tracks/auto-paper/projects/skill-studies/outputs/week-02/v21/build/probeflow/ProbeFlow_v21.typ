#import "conference.typ": *
#show: research-paper.with(title: "ProbeFlow: Frozen Policies, Changing Preferences")
#title-block("ProbeFlow: Frozen Policies, Changing Preferences","Development paper v21, 2026-10-19. New exact preference diagnostics on already exposed saved evidence; no new independent sample, model call, policy selection, physical experiment or external peer review.")
#abstract-block[#text("Adaptive acquisition must survive a strong fixed-source comparison under an explicit loss and cost contract. We analyze frozen policies on one hydraulic rig with 102 policy-fit cycles, 102 development cycles, and 421 previously exposed evaluation cycles. An oracle-separated diagnostic locates constraints without treating hindsight gains as learnable improvements. New per-cycle checks show identical component and complete-diagnosis error counts for the primary TS1 and TS1-plus-PS1 leaves on every evaluation cycle; the larger mask only adds a source quote. TS1 therefore weakly dominates this leaf pair for every convex mixture of the two error rates and every nonnegative equal-source cost weight. A secondary frozen gate reduces 63 component errors and 324 quotes but adds ten complete-diagnosis failures. Its exact preference boundary separates that genuine tradeoff from the primary conditional obstruction. Neither retrospective reweighting, repeated diagnostics nor homogeneous policy-fit labels establish independent generalization, physical savings, or native-method superiority.")]

= #text("Introduction")

#text("Active feature acquisition chooses which information to buy before predicting. Policy complexity is useful only when its apparent gain survives comparison with an affordable, strong fixed source. Otherwise a favorable contrast may reflect comparator weakness, predictor changes, or a different loss. ProbeFlow asks a narrower diagnostic question: given a frozen predictor and an already fitted observation-dependent gate, where does its remaining objective gap originate? The goal is to identify what a subsequent experiment must change, rather than introduce another acquisition optimizer.")

#text("Our public-data setting uses PS1, FS1, and TS1 records from hydraulic monitoring ")#link(<bib1>)[#text("[1]")]#text(". A policy first acquires one completed-cycle source mean and then stops or acquires another source. We distinguish this executable offline observation boundary from physical online sensing. Figure 1 preserves the historical support-first rationale. The new question is whether a frozen contrast changes sign when the importance of component errors, complete diagnoses and source quotes changes. A conditional dominance certificate and a preference boundary answer different parts of that question.")

#figure(figure-image("figures/overview.svg", 235.912251pt, "probeflow overview"), kind: image, caption: [#text("Inherited support-first diagnostic sequence. Historical support and predictor checks motivate bounded acquisition controls; arrows describe study logic, not a causal or universally sufficient guarantee.")]) <fig-overview>

#text(weight: "bold")[Contributions.]

- #text("A matched, inspectable contract separating acquired observations, frozen predictions, costs, and retrospective oracle rights.")
- #text("An exact finite-cohort oracle decomposition and a directly checked all-preference dominance certificate for the primary frozen leaf pair.")
- #text("An exact component/vector/cost boundary for a second frozen contrast, with adverse cases, source-specific benchmark plans and an unclosed prospective evidence gate.")

= #text("Related Work")

#text("AFA spans model-based, model-free, and hybrid policies ")#link(<bib13>)[#text("[13]")]#text(". Joint acquire-or-classify methods ")#link(<bib8>)[#text("[8, 21]")]#text(" and hierarchical costly features ")#link(<bib20>)[#text("[20]")]#text(" connect classification to information prices. EDDI ")#link(<bib12>)[#text("[12]")]#text(" and generative surrogates ")#link(<bib9>)[#text("[9]")]#text(" model missing observations; learned mutual-information selection supplies a stronger greedy comparator ")#link(<bib10>)[#text("[10]")]#text(". Learning-To-Measure ")#link(<bib2>)[#text("[2]")]#text(", BRiG-AFA ")#link(<bib3>)[#text("[3]")]#text(", offline source planning ")#link(<bib4>)[#text("[4]")]#text(", and pathwise policy gradients ")#link(<bib5>)[#text("[5]")]#text(" address predictor coupling or future consequences. Our small gate is neither a native implementation nor an empirical replacement for these methods.")

#text("Offline acquisition validity depends on observation and deployment assumptions ")#link(<bib11>)[#text("[11]")]#text("; adaptive-submodularity guarantees require their stated distribution and objective properties ")#link(<bib7>)[#text("[7]")]#text(". Selection bias and structured dependence also constrain interpretation ")#link(<bib14>)[#text("[14–16]")]#text(". Selective prediction distinguishes risk from coverage ")#link(<bib6>)[#text("[6, 17, 18]")]#text(", while loss-dependent decisions explain why component and joint errors can disagree ")#link(<bib19>)[#text("[19]")]#text(". We retain these distinctions without transferring external guarantees or benchmark scores. All 21 references and their inherited scopes remain preserved. The v21 resource ledger additionally records a selected official AFAPE body review ")#link(<bib11>)[#text("[11]")]#text(" and three candidate dataset contracts; none was downloaded or run as a new benchmark.")

= #text("Problem and Method")

#text("A mask is a source set: PS1=1, FS1=2, TS1=4. Each acquired source permits its predefined terminal features; the policy's branch observes only the purchased root mean. The inspected decision interface receives the immutable policy, acquired mask, and disclosed means. Labels, cycle identities, unrequested values, and the prediction bank are excluded. A private executor validates affordability and charges each source once. After STOP, the terminal mask selects an already cached prediction from the same fixed k-neighbor predictor.")

#text("Let L_i(m) be four-head component errors divided by 4, C(m) the sum of declared source prices, and B a per-cycle hard cap. The feasible set includes every mask satisfying that cap, including the empty mask with its frozen fallback. Lambda controls error–quote tradeoffs within feasibility; it cannot purchase permission to exceed B. Quote units are declared proxies, not measured latency, energy, or money. Every oracle comparison holds the predictor k, feasible masks, prices, B, lambda, and cohort fixed.")

#text("Write F for the locked fixed-policy mean and G for the actual gate mean. A is the per-cycle all-feasible-mask oracle mean; P restricts that hindsight choice to the gate's two frozen leaves. Thus A≤F and A≤P≤G. Adding and subtracting A and P gives the exact accounting identity below. E includes mandatory-root, leaf-set, and price constraints; R uses labels and unobserved predictions. Neither is a pure learning error or causal effect. Positive R does not prove an observable policy can attain P.")

#text("The distinction between hindsight and executable choice is essential. The all-mask oracle may select a source that the gate can never reach, whereas the pair oracle retains the mandatory root and its purchase cost. A policy cannot replace either oracle's privileged label access with its current confidence. Even a positive difference between G and P combines imperfect branching, restricted observations, and unavoidable uncertainty. Establishing a learnable gain would require a separately trained observable selector and an evaluation that did not help construct it.")

#text("For the new analysis, let alpha in[0,1] mix the component-error rate and the probability of any head error. Add lambda times mean source quote divided by3, with equal prices and the same cap2. Alpha specifies a decision preference, not a fitted parameter. Predictions, thresholds, leaves and original selections remain fixed throughout the sensitivity calculation; k1 and k3 contrasts are never pooled.")

$ u_(i) (m) = L_(i) (m) + lambda (C(m))/(sum_(j=1)^3 c_j), quad C(m) <= B $

$ A = (1/n) sum_(i=1)^n min_(m in cal(F)_B) u_(i) (m), quad P = (1/n) sum_(i=1)^n min(u_(i) (m_L),u_(i) (m_R)) $

$ H = F - A, quad E = P - A, quad R = G - P, quad G - F = -H + E + R $

= #text("Experimental Setup")

#text("The frozen predictor was trained on historical cycles 1..1540. Policies use 102 fit cycles 1561..1662, 102 development cycles 1663..1764, and 421 evaluation cycles 1785..2205:625 existing cycles from one rig. The evaluation interval was examined in earlier revisions. Recording policy locks before the current evaluation replay does not restore blindness or create an independent final. Root means summarize completed 60-second records; terminal features also include population standard deviation and slope. Actual online availability, overlapping-window costs, and sensor failures were not tested.")

#text("The inherited grid contains 90 k/price/cap/lambda contexts and 390 fitted gate-context records. Fit-only quartile thresholds and distinct feasible leaf pairs produce small gates; development selects best-fixed, gate-only, and adaptive-enabled families with recorded deterministic ties. The primary context is k1, equal prices, B2, lambda 1/20; its adaptive-enabled selector retains fixed PS1. We separately inspect its forced gate g129 and a predetermined k3, lambda 0 selected-gate example. The diagnostic reuses all locked records, producing 1170 gate/cohort rows and 4680 support-stratum rows. It performs no new fitting or policy selection.")

#text("Within a setting, the fixed and gate families use identical cached terminal predictions and development loss. Candidate inclusion guarantees only that adaptive-enabled development loss cannot exceed the best fixed development loss under the recorded ordering; it supplies no evaluation guarantee. Across settings, differing normalization, lambda, or k changes the comparison contract. We therefore report primary and secondary examples separately and never average their differently scaled objectives into an overall improvement.")

#text("The v21 continuation snapshots nine existing input files before execution. It checks two predetermined contrasts, 842 policy-cycle rows, 421 leaf certificates and60 dependent preference cells. A failed metadata lookup is preserved separately: historical TS1 was not the primary development-selected fixed policy. A new frozen execution verifies TS1 directly from its cache and the prior pair-oracle objective; it performs no new selection.")

= #text("Results")

#text("Table 1 reports exact objectives and preserves distinct error denominators. For primary g129, the root is TS1, threshold 35.44636666666667, with leaves 5 and 4. On421 cycles its actual objective is 12413/25260 against fixed PS1's13561/25260. The decomposition is H=56/421, E=73/842, R=11/12630, hence G−F=−287/6315. Component errors fall 876→798, but vector errors remain 391 and total quotes rise 421→443. A favorable PS1 comparison therefore does not isolate an adaptive-routing benefit.")

#text("For primary k1, masks4 and5 have equal component-error counts and equal vector errors on every one of421 cycles; mask5 costs one additional quote. Thus TS1 weakly dominates these two frozen leaves pointwise for every alpha in[0,1] and lambda>=0. Actual g129 takes the larger mask22 times, giving gate-minus-TS1=22lambda/1263, or11/12630 at the original lambda1/20. At lambda0 the scalar losses tie. This directly checked boundary is stronger than the original one-loss oracle equality, but remains conditional on this predictor, pair, cohort and equal-price cap2 contract.")

#text("The predetermined secondary g301 retains k3, equal prices, cap2 and its original lambda0 selection. Fixed and gate counts are924/861 component errors,381/391 vector errors and842/518 quotes. Reweighting these unchanged outputs yields delta=(-63+103alpha-432lambda)/1684. At zero cost weight the gate helps exactly when alpha<63/103; at lambda1/20 the boundary is423/515. For lambda>=5/54 its scalar loss is no worse for any alpha, but the ten extra vector failures remain. This is post-hoc sensitivity, not a newly optimized winner or three-objective Pareto dominance. Figure2 preserves the original scale; SupplementS14-S20 derive the new comparisons.")

#text("Every policy-fit target has one tuple, seen in only30/421 evaluation cycles. Primary root means are outside the fit min/max interval in392/421 cases. These counts flag extrapolation, not density support or causality. In the secondary contrast, component errors improve on73 cycles and worsen on10; vector errors worsen on10 and improve on none. Eight vector regressions are inside its original root range and two outside. Range membership alone cannot explain those failures. Repeated settings and overlapping strata remain dependent diagnostics.")

#result-table(([#text("Setting / object")],[#text("Mean objective")],[#text("Component errors")],[#text("Vector errors")],[#text("Total quotes")],),(([#text("Primary F: PS1")],[#text("13561/25260")],[#text("876")],[#text("391")],[#text("421")],),([#text("Primary A: all-mask oracle")],[#text("10201/25260")],[#text("—")],[#text("—")],[#text("—")],),([#text("Primary P: two-leaf oracle")],[#text("12391/25260")],[#text("—")],[#text("—")],[#text("—")],),([#text("Primary G: actual gate")],[#text("12413/25260")],[#text("798")],[#text("391")],[#text("443")],),([#text("Primary historical TS1")],[#text("12391/25260")],[#text("798")],[#text("391")],[#text("421")],),([#text("Secondary F: PS1+FS1")],[#text("924/1684")],[#text("924")],[#text("381")],[#text("842")],),([#text("Secondary A: all-mask oracle")],[#text("625/1684")],[#text("625")],[#text("—")],[#text("—")],),([#text("Secondary P: two-leaf oracle")],[#text("789/1684")],[#text("789")],[#text("—")],[#text("—")],),([#text("Secondary G: actual gate")],[#text("861/1684")],[#text("861")],[#text("391")],[#text("518")],),),"Same frozen predictor and contract within each setting. Component counts use 1684 head decisions; vector counts use 421 cycles. Oracle dashes avoid importing unreported component/cost breakdowns. TS1 is a preserved historical control with different selection access, not a newly selected primary winner.")

#figure(figure-image("figures/oracle-gap-decomposition-v19.svg", 269.999764pt, "probeflow oracle-gap-decomposition-v19"), kind: image, caption: [#text("Existing exact saved-evidence decomposition: primary normalized loss including quote penalty and secondary component-error counts. Oracle information is privileged; the plotted gaps are not achievable policy gains or new independent experiments.")]) <fig-oracle-gap-decomposition-v19>

= #text("Limitations")

#text("One rig, chronological dependence, prior evaluation exposure, and homogeneous fit labels prevent an independent generalization claim. Complete-cycle masking does not reproduce the timing or measurement effects of acquiring another physical sensor. Equal caps do not imply equal realized quotes, and those quotes omit offline collection, fitting, tuning, and wall-clock expense. The restricted gate class, fixed predictor, and two loss definitions limit every boundary. A root-range indicator alone cannot identify distributional support or explain individual prediction errors.")

#text("Separate arithmetic verification checked the prior1170 rows/4680 strata and, in the new continuation,1684 policy-cycle aggregates,421 leaf certificates and60 preference cells, including hash/metric tamper refusals. These are provenance and finite-computation checks, not independent validation. No new predictor forward pass, policy fit, selection, physical acquisition, device or native AFA trial was executed. Candidate HAR, drift and multisensor protocols in the supplement remain proposals, with observation-time, group-split and license limits.")

#text("The negative primary boundary is deliberately useful but local: it can stop one unsupported search claim without proving that adaptation is generally futile. A successful next study must defeat the strong control under its own locked contract, not merely lower error relative to PS1.")

= #text("Conclusion")

#text("ProbeFlow separates a weak-comparator gain, an exact local dominance obstruction and a real decision tradeoff. The primary frozen pair adds cost without changing errors on any exposed cycle. The secondary contrast exchanges fewer component errors and quotes for more complete-diagnosis failures, with an exact preference boundary. Future evidence must change or validate candidate, predictor, observation and support assumptions on independent groups; reweighting a saved cohort does not supply that evidence.")


#heading(numbering: none)[Acknowledgements]
#text("This work was created as part of the No-More-Slops group activities at Pseudo Lab.")

#heading(numbering: none)[References]

#bibliography-entry(1, [#text("N. Helwig, E. Pignanelli, and A. Schütze. Condition monitoring of hydraulic systems. UCI Machine Learning Repository, 2015.")],"https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems") <bib1>

#bibliography-entry(2, [#text("Y. Kobayashi, Z. Jing, J. Yao, H. Namkoong, and S. Joshi. Learning-To-Measure: In-Context Active Feature Acquisition. arXiv:2510.12624v2, 2026.")],"https://arxiv.org/html/2510.12624v2") <bib2>

#bibliography-entry(3, [#text("J. Feng, Q. Li, and Y. Li. BRiG-AFA: Bellman Risk-to-Go Learning for Non-Myopic Active Feature Acquisition. arXiv:2608.02305v1, 2026.")],"https://arxiv.org/html/2608.02305v1") <bib3>

#bibliography-entry(4, [#text("Z. Zhao, R. Xu, and Q. Ni. Learning Source Acquisition Policies by Offline Planning. arXiv:2609.14299v1, 2026.")],"https://arxiv.org/html/2609.14299v1") <bib4>

#bibliography-entry(5, [#text("L. Aronsson and M. Haghir Chehreghani. Non-Myopic Active Feature Acquisition via Pathwise Policy Gradients. arXiv:2605.05511v2, 2026.")],"https://arxiv.org/html/2605.05511v2") <bib5>

#bibliography-entry(6, [#text("Y. Geifman and R. El-Yaniv. Selective Classification for Deep Neural Networks. arXiv:1705.08500v2, 2017.")],"https://arxiv.org/html/1705.08500v2") <bib6>

#bibliography-entry(7, [#text("D. Golovin and A. Krause. Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization. JAIR 42; arXiv:1003.3967v5, 2011.")],"https://arxiv.org/html/1003.3967v5") <bib7>

#bibliography-entry(8, [#text("H. Shim, S. J. Hwang, and E. Yang. Joint Active Feature Acquisition and Classification with Variable-Size Set Encoding. NeurIPS, 2018.")],"https://proceedings.neurips.cc/paper_files/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html") <bib8>

#bibliography-entry(9, [#text("Y. Li and J. B. Oliva. Active Feature Acquisition with Generative Surrogate Models. ICML, PMLR 139:6450-6459, 2021.")],"https://proceedings.mlr.press/v139/li21p.html") <bib9>

#bibliography-entry(10, [#text("I. C. Covert, W. Qiu, M. Lu, N. Y. Kim, N. J. White, and S.-I. Lee. Learning to Maximize Mutual Information for Dynamic Feature Selection. ICML, PMLR 202:6424-6447, 2023.")],"https://proceedings.mlr.press/v202/covert23a.html") <bib10>

#bibliography-entry(11, [#text("H. von Kleist, A. Zamanian, I. Shpitser, and N. Ahmidi. Evaluation of Active Feature Acquisition Methods for Time-varying Feature Settings. JMLR 26(60):1-84, 2025.")],"https://jmlr.org/beta/papers/v26/23-1635.html") <bib11>

#bibliography-entry(12, [#text("C. Ma, S. Tschiatschek, K. Palla, J. M. Hernandez-Lobato, S. Nowozin, and C. Zhang. EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE. ICML, PMLR 97:4234-4243, 2019.")],"https://proceedings.mlr.press/v97/ma19c.html") <bib12>

#bibliography-entry(13, [#text("L. Aronsson, A. Rahbar, and M. Haghir Chehreghani. A Survey on Active Feature Acquisition Strategies. IJCAI Survey Track, pages 7740-7748, 2026.")],"https://www.ijcai.org/proceedings/2026/860") <bib13>

#bibliography-entry(14, [#text("G. C. Cawley and N. L. C. Talbot. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. JMLR 11(70):2079-2107, 2010.")],"https://www.jmlr.org/beta/papers/v11/cawley10a.html") <bib14>

#bibliography-entry(15, [#text("S. Varma and R. Simon. Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics 7:91, 2006.")],"https://link.springer.com/article/10.1186/1471-2105-7-91") <bib15>

#bibliography-entry(16, [#text("D. R. Roberts et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40:913-929, 2017.")],"https://nsojournals.onlinelibrary.wiley.com/doi/10.1111/ecog.02881") <bib16>

#bibliography-entry(17, [#text("Y. Geifman and R. El-Yaniv. SelectiveNet: A Deep Neural Network with an Integrated Reject Option. ICML, PMLR 97:2151-2159, 2019.")],"https://proceedings.mlr.press/v97/geifman19a.html") <bib17>

#bibliography-entry(18, [#text("R. El-Yaniv and Y. Wiener. On the Foundations of Noise-free Selective Classification. JMLR 11(53):1605-1641, 2010.")],"https://www.jmlr.org/papers/v11/el-yaniv10a.html") <bib18>

#bibliography-entry(19, [#text("K. Dembczyński, W. Waegeman, W. Cheng, and E. Hüllermeier. On label dependence and loss minimization in multi-label classification. Machine Learning 88:5–45, 2012.")],"https://link.springer.com/article/10.1007/s10994-012-5285-8") <bib19>

#bibliography-entry(20, [#text("J. Janisch, T. Pevny, and V. Lisy. Classification with costly features in hierarchical deep sets. Machine Learning 113:4487-4522, 2024.")],"https://link.springer.com/article/10.1007/s10994-024-06565-4") <bib20>

#bibliography-entry(21, [#text("J. Janisch, T. Pevny, and V. Lisy. Classification with Costly Features Using Deep Reinforcement Learning. AAAI33(01):3959-3966,2019.")],"https://ojs.aaai.org/index.php/AAAI/article/view/4287") <bib21>
