#import "conference.typ": *
#show: research-paper.with(title: "SkillMerge: When Agreement Displaces Evidence")
#title-block("SkillMerge: When Agreement Displaces Evidence","Compact working paper v20, 2026-10-19. Editorial reorganization of unchanged v19 evidence; no new experiment, independent data, native-method execution, model/API call, or professor endorsement.")
#abstract-block[#text("Does prioritizing agreement preserve useful evidence when two outputs are composed? We study this measurement question on an already exposed SciFact-derived bank, rather than claim a behavioral effect of executable skills. Stable common-item promotion is compared with the same round-robin order on 22,794 constructed ordered pairs across seven output capacities. Full-containment gain/loss counts are 565/2700 at capacity one, 95/25 at two, and 0/2 at three; losses vanish from capacity four, while first-three scoring retains both failures. We derive a completion-rank identity, an exact single-window characterization, and a conditional no-loss boundary for individually annotation-sufficient inputs of length at most three. In a fixed sufficient-input stratum, pooled and equal-component contrasts have opposite signs. Separate author verification preserves an initially overstrong failed check and its correction. All findings concern finite annotation contracts: independent skill histories, qualified pairs, and fresh behavioral evaluations remain absent, and the behavioral composition effect is null.")]

= #text("Introduction")

#text("Reusable skill files create a practical integration question: when two changes help separately, should both become available together? A lower joint score could indicate lost evidence, a changed ranking, an incomplete reference, extra context, or different resource permissions. These explanations require different repairs. We therefore audit the measurement and output-construction mechanisms before estimating interference between independently authored skills.")

#text("Our completed study manipulates sentence-ID lists with auditor-supplied correct labels. It neither runs skill files nor observes new agent predictions. This narrow setting allows exact comparisons under fixed inputs and references. Agreement means repeated IDs, not agreement between independently sampled reasoning paths or scientific claims. Figure 1 distinguishes the executed diagnostic lane from the unexecuted authoring, qualification, and fresh-evaluation lane.")

#text("The central question is whether promoting shared IDs changes completion of a reference alternative under a declared capacity. We retain failures, empty outputs, exposure, and nested denominators. The contribution is a reproducible mechanism audit and a conditional theorem, rather than a generally superior integration controller. Supplement S1 provides the reading map; S2–S7 make every assumption and counterexample explicit.")

#text("A ranking failure can still matter operationally when the application requires short evidence. Preserving the full union refutes only the stronger allegation that an annotated sentence disappeared altogether. Conversely, recovering a reference score after changing the grader does not establish a better deployed answer. Our controls identify these logical distinctions before a future study chooses an integration policy.")

#figure(figure-image("figures/overview.svg", 205.667699pt, "skillmerge overview"), kind: image, caption: [#text("Executed evidence-contract diagnostics and prospective behavioral inference are separate. The inherited source audit contains 531 tasks in 325 structural components; 309 evidence-bearing tasks in 204 components feed the current pair bank. Authoring histories, independently qualified pairs, and fresh behavioral effects remain absent. Counts are nested, not independent integration events.")]) <fig-overview>

#text(weight: "bold")[Contributions.]

- #text("A controlled agreement intervention that separates common-item priority, output capacity, and evaluator truncation.")
- #text("Completion-rank proofs, an explicit conditional no-loss boundary, and preserved failure witnesses.")
- #text("Paired accounting that exposes weighting reversal, verifier correction, and the missing behavioral denominator.")

= #text("Related Work")

#text("SciFact and FEVER distinguish reference-supported correctness from other outcomes ")#link(<bib1>)[#text("[1,3]")]#text(". The pinned SciFact implementation slices the supplied rationale list to three IDs for rationalized abstract correctness ")#link(<bib2>)[#text("[2]")]#text(". ERASER distinguishes human-rationale agreement from predictive faithfulness ")#link(<bib4>)[#text("[4]")]#text("; our annotation containment is not its confidence-based sufficiency. CheckList motivates focused invariance and directional tests ")#link(<bib5>)[#text("[5]")]#text(", here applied to deterministic contracts.")

#text("Multi-metric evaluation ")#link(<bib6>)[#text("[6,7]")]#text(", construct validity ")#link(<bib8>)[#text("[8,9]")]#text(", underspecification ")#link(<bib11>)[#text("[11]")]#text(", dataset documentation ")#link(<bib12>)[#text("[12]")]#text(", and benchmark selection ")#link(<bib13>)[#text("[13]")]#text(" motivate explicit score-to-claim boundaries. Finite-data selection can itself overfit ")#link(<bib21>)[#text("[21]")]#text(". These sources motivate controls; none establishes a local behavioral composition effect.")

#text("DSPy compilation ")#link(<bib10>)[#text("[10]")]#text(", conservative replay in SkillCommit ")#link(<bib14>)[#text("[14]")]#text(", typed migration in SkillSmith ")#link(<bib15>)[#text("[15]")]#text(", SkillCAT routing/assembly ")#link(<bib16>)[#text("[16]")]#text(", and SkillEvoReg regression validation ")#link(<bib17>)[#text("[17]")]#text(" supply substantive future comparisons. Instruction/resource controls ")#link(<bib18>)[#text("[18]")]#text(" and the SkillsBench v1.1 release ")#link(<bib19>)[#text("[19]")]#text(" address different budgets and environments. Self-consistency aggregates sampled final answers ")#link(<bib20>)[#text("[20]")]#text(", whereas we reorder fixed evidence IDs. None of these native methods is executed here; their reported scores are not imported. All 21 inherited reference records retain their original inspection scopes, including abstract-only reviews.")

= #text("Problem and Method")

#text("For each evidence-bearing task, references are nonempty alternative sets of sentence IDs. A valid response is an ordered list of distinct in-range IDs. Full sufficiency accepts if any complete alternative occurs anywhere in the output. First-three applies the same test only to its first three IDs. Exact-annotated requires equality with an enumerated alternative. These are separate operational endpoints, not interchangeable measures of semantic truth.")

#text("Round-robin scans A and B alternately, retaining each ID only on first appearance, to form a complete union order V. Stable promotion forms P by placing common IDs first while preserving V's relative order within both common and noncommon classes. Each output is then truncated to its first k IDs. Constructors read only A, B, and k; references enter post-hoc scoring and descriptive stratification. This fully stable rule differs from the earlier agreement constructor at small capacities, where common-ID internal order can matter.")

#text("With one-based ranks and absent IDs assigned infinity, the first sufficient capacity is the smallest completion rank across reference alternatives. Consequently, each order passes exactly from its threshold onward. Two orders can differ only on one contiguous capacity interval, with one polarity. This identity depends on nested prefixes and full containment; it does not extend automatically to exact matching, first-three evaluation, or meaningful natural-language answers.")

#text("If each complete input contains a valid alternative and each has length at most three, stable promotion cannot lose full sufficiency at k at least four. Empty intersection leaves the baseline unchanged; two shared IDs bound union size by four; one shared ID leaves at most one exclusive omission, preserving the other input. No-loss does not mean universal success, and annotation-sufficient inputs are not independently Q-qualified skills.")

#text("Promotion preserves every common ID already selected by the baseline and can remove only noncommon IDs. A loss therefore requires all previously complete alternatives to intersect the removed IDs and no alternative to become complete in compensation. This certificate uses references after construction; it is an explanatory audit, not a deployable label-free selector or a claim that shared content is erroneous.")

$ r(L) = min_(R in cal(R)) max_(x in R) "rank"_(L) (x) $

$ S_(k) (L) = bb(1)[k >= r(L)] $

= #text("Experimental Setup")

#text("The unchanged exposed bank contains 309 evidence-bearing tasks, 204 recorded components, 2,494 distinct inputs, and 22,794 ordered pairs. Diagonal and reversed pairs are retained as constructed views, not independent histories. Capacities zero through six produce 159,558 pair-capacity contracts, 319,116 deterministic outputs, and 957,348 endpoint cells. These computations add no independent observations. Capacity counts output IDs; tokens, tool calls, and authoring costs are unmeasured.")

#text("The primary descriptive weighting averages pairs within tasks, tasks within components, then components equally. Pair-pooled and equal-task alternatives are reported separately. A fixed both-input-sufficient stratum contains 12,067 pairs from 308 tasks and 203 components. It conditions on complete original inputs, not their k-truncated versions and not held-out behavioral qualification. We never reinterpret its inclusion rule as observed usefulness of executable skills.")

#text("Plans, code, eleven consumed inputs, results, and verifier snapshots are bound by hashes. A separately written prefix-set/bitmask checker covers 3,046 authored input pairs, 122,571 one/two-alternative reference families, and 857,997 reference-capacity cells. These certificates include overlapping alternatives and are not a native SciFact corpus replication. The same author wrote both implementations. Supplement S8–S12 preserves full denominators, commands, input locks, checks, and the failed verification attempt.")

#text("Exact enumeration removes sampling error within the declared finite constructions, not annotation error or uncertainty about external populations. Uniform-subset expectations are combinatorial controls rather than sampled model trials. Repeated capacities, endpoint cells, and alternative reference families are computational denominators and never increase the number of independently qualified histories.")

= #text("Results")

#text("Table 1 retains all 22,794 ordered pairs at every capacity. Full-sufficiency losses decrease from 2,700 to 25 to two at capacities one, two, and three; capacities four through six have no gains or losses on this bank. First-three scoring nevertheless retains zero gains and two losses above capacity three. Thus extending the generated output and extending what the grader reads are different interventions. Figure 2 shows this separation.")

#text("A saved witness has A=(1,2,0), B=(4,5,0), and alternatives {1,2} or {4,5}. At capacity three, round-robin outputs (1,4,2) and passes; promotion outputs (0,1,4) and fails. At four, (0,1,4,2) restores full containment but its first three IDs still fail. The two counted losses are ordered records, not two independent observed skill collapses. Across the bank, 3,387 pairs have different completion thresholds and 2,255 unions cannot contain any complete alternative.")

#text("Weighting changes the descriptive sign. In the fixed sufficient-input stratum at capacity one, gains 565 minus losses 1,409 give pooled contrast -844/12067, approximately -0.06994. Equal-component contrast is +3363459013/266277211200, approximately +0.01263. Unequal response multiplicities explain why these summaries answer different questions; neither is selected retrospectively as the universal effect.")

#text("Inherited length controls reinforce this caution. Intersection-only has equal-component sufficient/exact scores 0.290889/0.150539, below its pairwise length-matched uniform-subset control at 0.356638/0.221823. Component-fold selection adds no score beyond its stable fixed choices. A four-rule gold oracle bounds only its declared class; an excluded negative control can exceed it. Supplement S9–S10 preserves these comparison rights and their limitations.")

#text("Observed non-tie capacity intervals all have width one, but the theorem permits wider intervals under other references. The finite certificate finds minimal sufficient-input loss witnesses with union sizes three, four, and five at capacities one, two, and three; it finds none at zero or four through six. Exhaustive checking supports the declared bounded class, while the separate proof explains its assumptions. In particular, the bank's zero changes above three do not imply universal equality: the no-loss theorem allows gains and unchanged failures. These distinctions prevent a finite pattern from silently becoming a stronger general statement.")

#text("The original verifier incorrectly tested guaranteed success instead of no-loss for disjoint inputs. That frozen failed attempt remains recorded; a separately frozen corrected checker passes the registered implication without altering analysis outputs. This correction is author verification, not independent scientific replication.")

#result-table(([#text("Output cap")],[#text("Full gain")],[#text("Full loss")],[#text("First-three gain/loss")],),(([#text("0")],[#text("0")],[#text("0")],[#text("0 / 0")],),([#text("1")],[#text("565")],[#text("2700")],[#text("565 / 2700")],),([#text("2")],[#text("95")],[#text("25")],[#text("95 / 25")],),([#text("3")],[#text("0")],[#text("2")],[#text("0 / 2")],),([#text("4..6")],[#text("0")],[#text("0")],[#text("0 / 2")],),),"Paired promotion versus the same round-robin baseline on 22,794 exposed ordered records per capacity. Counts are deterministic transitions, not sampled model outcomes. Full and first-three are different endpoints.")

#figure(figure-image("figures/capacity-boundary-v19.svg", 269.999764pt, "skillmerge capacity-boundary-v19"), kind: image, caption: [#text("The unchanged capacity audit: full-containment loss counts across output capacities, with a cap-three-to-six zoom contrasting full recovery and persistent first-three losses. Each point reuses the same constructed pair cohort. No curve measures independently qualified skill behavior.")]) <fig-capacity-boundary-v19>

= #text("Limitations")

#text("Annotations are neither complete semantic truth nor independently adjudicated deployment outcomes. Correct labels are supplied, component separation does not erase prior exposure, and author-constructed pair multiplicities do not estimate natural prevalence. The cap-four result depends on both sufficient inputs, length at most three, complete union construction, stable class orders, and full containment. Same-length changed output sets cannot have a reference-blind universal guarantee: a removed singleton supplies a counterexample.")

#text("Independent A/B authoring histories, Q-qualified pairs, reserved-S outcomes, native-method runs, and measured token costs remain zero or unavailable; the behavioral composition effect is null. A future comparison must freeze candidate classes, qualification, rights, resets, and total costs before fresh evaluation, allow conservative rejection/fallback, and retain zero yield, failures, and missingness. Supplement S13–S14 states the prospective decisions and falsification criteria; this editorial revision executes none of them.")

= #text("Conclusion")

#text("Shared evidence can displace completion under a finite capacity without establishing general skill interference. Exact completion-rank analysis identifies when that happens, why full and first-three scores diverge, and which conditional boundary survives verification. Transparent weighting and a preserved verifier correction constrain the claim. Estimating executable-skill composition requires the still missing independently qualified behavioral study with complete resource accounting.")


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
