#set document(title: "ProbeFlow: Certified Search for Budgeted Information Design — Supplement")
#set page(paper: "a4", margin: 17mm, numbering: "1")
#set text(font: ("New Computer Modern", "Malgun Gothic", "Noto Sans KR"), size: 10pt, lang: "en")
#set par(justify: true, leading: 0.48em, spacing: 0.55em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 12pt, weight: "bold")
#set figure(gap: 5pt)
#show figure.caption: set text(size: 9pt)
#let fit-equation(body) = layout(size => { let natural = measure(body); let factor = calc.min(1, size.width / natural.width); align(center, scale(factor * 100%, reflow: true, body)) })
#align(center)[#set par(justify: false)
#text(size: 18pt, weight: "bold", hyphenate: false)[#text("ProbeFlow: Certified Search for Budgeted Information Design — Supplement")]]
#v(4pt)
#align(center)[#text(size: 9pt)[#text("Corrected conference narrative edition · 26 October 2026 · certified search and a separate acquisition diagnostic")]]
#v(6pt)
#v(8pt)
#block[
#set par(leading: 0.18em, spacing: 0.18em)
#outline(title: "Contents", depth: 1)
]
#pagebreak()
= #text("Correction note: active display and unchanged historical copies")

#text("The current main Section 5.3 corrects the nearest-five-decimal display of the already recorded exact macro loss 157023/457520 from 0.34321 to 0.34320. Figure 5 already displays 0.34320. No observation, fraction, denominator, policy, regression or conclusion changes. ERRATA.json binds the original source, exact paragraph text hashes, corrected active pointer and new historical pointers.")

#text("All pre-existing supplementary sections below are exact historical/source copies. In particular the preserved previous-main application-result section retains its original 0.34321 typo; read that display through this correction note. Earlier local section/figure numbers and words such as current or pending refer to their dated source editions. The full current seventeen-section main is not duplicated here. Ongoing external-baseline and untouched-final work has no result in this edition.")

= #text("Reader guide: argument and preserved record")

#text("This edition leads with the certified fixed-subset search. Main Section 3 separates R from J, Section 4 gives search, guarantees, the diagnostic estimator and execution as subsections, and Section 5 reports search before the separate acquisition diagnosis. Section 6 interprets those observations without presenting a new experiment. Original Appendices A–E and every historical section below remain exact structured copies.")

#text("The previous completed edition used a different main order and contained an incorrect five-entry requirements index. Its source, map, failure receipt and independent corrected anchors remain immutable inputs. The present COVERAGE resolves new headings/algorithms and hashes their actual target structures. At the end of this supplement the complete previous main paper is retained verbatim; its old section/figure numbers refer to that historical edition.")

= #text("A. Reading the completed edition and preserved evidence")

#text("The main now leads the completed separately reviewed certified-search study. Its objective R is worst sharp identified width, not the application objective J. The completed coherent-estimation study is a negative application diagnosis. The advanced-v 455 supplement sections,55 Korean chapters, previous main and actual W49/failed W50 material remain exact structured copies, with dated historical wording and one canonical location each in COVERAGE.json. Current result slots have actual values, not inherited draft placeholders.")

#text("Both new studies and both distinct reviews use normal native Task provenance. They are not relabeled canonical scientific-wave orca_supervised worker_reports. Review acceptance is bounded to source integrity, declared conditional theory and saved finite observations; scientific certification, population utility, external novelty and publication remain false. Existing public selection still points to an older through 44 source; this new private edition does not change that pointer.")

= #text("A.1. Original loss model and sharp endpoints")

#text("For participant j, binary requested errors have one shared global count cap B, known stop-error coordinates are fixed 1 and other stops 0. Independent route/static availability vectors lie in[0,1]^n and each sum to n/2. Requested route success uses r_i; nonrequested route success is 0. Route loss is (1-success_i)u_i+c(1+requested_i)+k requested_i(1-r_i). Static loss is (1-v_i)u_i+2 c+k(1-v_i), with c=1/20,k>=0. Delta is their equal-participant macro difference.")

#text("Sharp endpoints optimize this original loss over feasible binary-error placements and availability box/sum sets, preserving one global cap instead of duplicating it for each person. Query thresholds use closed intervals[0,t_i] and[t_i,1]; boundary worlds can support both labels. An impossible conjunction is distinct from an empty statistical denominator and cannot be filled with a favorable zero. Historical full derivations, shared-cap dynamic programming/heap and failed shortcuts are retained below.")

= #text("A.2. Outer lower bound proof")

#text("At node(I,U), let M=I union U and let S be any represented affordable design. A verified feasible reading z_M induces z_S by projection. Since Omega(M,z_M) is contained in Omega(S,z_S), sharp lower endpoints can only decrease and upper endpoints can only increase when passing to S. Thus W(M,z_M)<=W(S,z_S)<=R(S). Taking the maximum over a finite bank of feasible M readings preserves a lower bound for every S. M need not be affordable: additional information is an optimistic relaxation, never an executed purchase.")

#text("The bank contains exactly three predetermined public-model worlds: midpoint availability, a participant box/sum vertex formed by filling n/2 from the first coordinate, and its reverse. Set route availability to 1/2 and requested errors to 0; known stop errors remain fixed. Validate every box, mean, cap and closed-bin membership. Projected duplicate label vectors are evaluated once. The bound cache key is M because this bank and its projected-reading width depend on M rather than the particular I/U partition.")

#text("All prices are positive. Any individually unaffordable undecided item can be removed; adding items cannot lower c(I) or the integer bitmask. Therefore(LB,c(I),mask(I)) is a lexicographic lower tuple for every represented design. Pruning this tuple when it is no better than an exact incumbent preserves the canonical risk/price/mask representative.")

= #text("A.3. Inner upper bounds, lost ties and a wrong-direction example")

#text("For fixed S, a prefix h defines a superset of each descendant complete world set. Consequently L(h)<=L(z)<=U(z)<=U(h). A completed feasible width b lower-bounds the inner maximum; W(h)<=b may prune while retaining numeric maximum and an already stored witness. It may remove further maximizing readings. Original full-tie traversal must instead use W(h)<b. The new output deliberately gives one witness and does not retroactively satisfy the all-tie contract.")

#text("A completed partial maximum is also a lower bound on R(S), so a risk evaluation can stop early only when its full tuple cannot improve the outer incumbent; such a partial value is not cached as an exact risk or used to update the incumbent. The preseal direction fixture has n=[2],a=[1],e=[1],B=0,k=0 and thresholds 1/3: R(empty)=1/2 while R(first query)=1/3. Parent width is therefore not a valid outer lower bound. Complementarity separately gives R(4)=R(5)=R(6)=3/8 and R(7)=1/4, rejecting a stale greedy marginal upper bound.")

= #text("A.4. Frontier certificate and canonical exact stopping")

#text("Frontier nodes cover unresolved feasible subsets. Exact-pruned nodes cannot beat the incumbent, and every incumbent has an exact feasible risk. Set UB=R(incumbent), L=min(UB,min_frontier LB), or L=UB when the frontier is empty. Then L<=R*<=UB. At epsilon>0, UB-L<=epsilon certifies absolute returned-risk regret. At epsilon = 0, a scalar zero gap alone does not settle cheaper equal-risk masks, so the implementation resolves the lexicographic frontier.")

#text("A handled interruption restores an active popped node if it exists and returns uncertified saved state. It does not resume, rerun or assert success from coincident scalar bounds. A preseal zero-CPU case checks uncertified exhaustion; no registered main arm exhausted. Generic strict node-cap enforcement has a disclosed last-step possible+1 overshoot; all observed counts are far below the registered cap. The frozen implementation remains unchanged.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 1. Certified subset search with one winner")]]
#v(3pt)
#strong[Require] #text("Positive query prices, hard budget Q, tolerance epsilon; sharp endpoints and three verified public-model seed worlds. Included/undecided sets I,U; exact incumbent tuple (risk,cost,mask); initially cold shared caches.")
#parbreak()
#strong[Ensure] #text("One canonical optimum if epsilon=0 and search completes; otherwise feasible design plus scalar certificate [L,U]. Interruption is uncertified.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[$t^*<-$#text(" exact feasible empty/greedy incumbent; ")$F<-$#text(" Push(empty,all).")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("while frontier F is nonempty:")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.96em))[#text("check cooperative resource guard; restore active node on handled interruption.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$epsilon>0$#text(" and ")$"UB"-min("UB",min_F "LB")<=epsilon$#text(": break.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.96em))[$(I,U)<-$#text(" pop minimum bound/cost/mask node.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$("LB",c(I),I)>=t^*$#text(": continue.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$U=emptyset$#text(": compute exact ")$R(I)$#text("; update best only on exact completion.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.96em))[#text("else: choose first undecided item; Push both exclude/include children.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.0em))[#text("procedure Push")$(I,U)$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("10")], [#block(width: 100%, inset: (left: 0.96em))[#text("remove individually unaffordable items from ")$U$#text("; ")$M<-I union U$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("11")], [#block(width: 100%, inset: (left: 0.96em))[$"LB"<-max_k W(M,z_M^k)$#text(" from verified feasible seed readings.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("12")], [#block(width: 100%, inset: (left: 0.96em))[#text("retain node only if ")$("LB",c(I),I)<t^*$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("13")], [#block(width: 100%, inset: (left: 0.0em))[#text("return ")$"UB"=R(S^*)$#text("; ")$"LB"_F=min("UB",min_F "LB")$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("14")], [#block(width: 100%, inset: (left: 0.0em))[#text("epsilon = 0 resolves remaining lex ties; no all-tie output or strict node-cap promise.")]])
#v(1.2pt)
]

= #text("A.5. Strong memoized DP, caching rights and computational scope")

#text("The strong baseline uses V(M)=min_lex{(R(M),c(M),M),V(M union{i}) for affordable i}. Memoization merges permutations of the same acquired subset. Remaining budget is Q-c(M), so subset M is sufficient for this static problem. DP and B&B share the exact one-witness inner search, initially cold endpoint/local/risk caches, exact greedy warm starts and the three-reading global floor. If R(M) equals that floor, positive additions cannot improve the cheapest extension-family representative, permitting a DP floor stop.")

#text("The original all-tie reference invokes the unchanged historical flat solver on all affordable masks and retains all primary/transcript ties, including its historical per-call cache resets. Its larger output and cache contract differ; speed differences against it cannot all be assigned to the new outer bound. Greedy only creates feasible incumbents and has no approximation certificate. A persistent no-eviction computation DAG pays the union of ancestors for a fixed query set regardless of order, if each operation is paid once. Different acquired sets/STOP, TTL/eviction/deadlines or failures require their own model; no cache experiment was performed here.")

#text("Worst-case subset and subset/reading counts remain 2^N and 3^N. Sharp endpoints, Fraction bit lengths, warm-start construction, cache keys/entries, frontier, output serialization and retained ties add costs. The finite cases N 2/3/4/7/8 do not establish polynomial scaling or total deployment savings.")

= #text("A.6. Complete seven-condition engineering comparison")

#text("The table reports median direct CPU seconds / maximum traced Python bytes across three cold cyclic repeats. Every exact method has identical risk and canonical design. Exact B&B beats DP on CPU and peak together only on complementarity and hard Q4; equality and the five other DP-win/tie patterns remain visible. Epsilon observed regret is 0 in all seven finite conditions, but Q2/Q4 certificates have positive gaps.")

#text("Hard Q4 exact endpoint_calls are original 1411, DP 1476 and B&B 330. Original counts only feasible endpoint invocations, although raw endpoint events include impossible None readings; the other Context counter includes computed infeasible calls. Independent reviewer attempt 1 initially confused these definitions, failed, preserved its checker/failure and corrected only reviewer code. This was not a producer rerun or performance failure.")

#text("All seed/warm-start/endpoint/bound/cache/search/raw-write arm work is charged. Terminal receipt serialization and common imports are in main total, and independent oracle is separate. Main+oracle total is 44.734375 CPU seconds and 46.02244799997425 wall seconds. Preseal tests, authoring, RSS and physical I/O/energy are not included. Python peaks are traced allocations, not process memory.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("All conditions: CPU seconds / maximum Python bytes; lower is better. No inferential error bars or universal speed ratio.")]]
#v(4pt)
#table(columns: (1.15fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Condition")],[#text("Original all-tie")],[#text("Strong DP")],[#text("Exact B&B")],[#text("epsilon B&B")],[#text("Exact R")]),
[#text("equality_ties")],[#text("0.015625 / 18902")],[#text("0.015625 / 16224")],[#text("0.015625 / 16842")],[#text("0.0 / 16978")],[#text("0")],
[#text("impossible_bins")],[#text("0.015625 / 25006")],[#text("0.015625 / 25126")],[#text("0.03125 / 27007")],[#text("0.015625 / 21834")],[#text("11/30")],
[#text("tight_zero_cap")],[#text("0.0625 / 54629")],[#text("0.0625 / 46670")],[#text("0.078125 / 72149")],[#text("0.046875 / 38676")],[#text("41/120")],
[#text("complementarity")],[#text("0.265625 / 111334")],[#text("0.25 / 73531")],[#text("0.21875 / 59281")],[#text("0.171875 / 49589")],[#text("1/4")],
[#text("w 41_shared_cap_ties")],[#text("4.09375 / 316230")],[#text("0.203125 / 85789")],[#text("0.25 / 137717")],[#text("0.203125 / 137933")],[#text("3/5")],
[#text("hard_pairs_Q 2")],[#text("0.34375 / 88869")],[#text("0.125 / 66535")],[#text("0.125 / 80798")],[#text("0.109375 / 67217")],[#text("51/128")],
[#text("hard_pairs_Q 4")],[#text("6.96875 / 231943")],[#text("0.71875 / 334535")],[#text("0.28125 / 141338")],[#text("0.15625 / 89232")],[#text("21/64")])
]

= #text("B. Complete-row estimator, support and Bellman identity")

#text("The frozen bank has 514 rows. T participants 5/6 contribute 168/154 rows, C 96/96. Each P_D gives each participant mass 1/2, each of its rows mass 1/(2 n_Ds). P_joint=(64 P_T+192 P_C)/256 is formed before conditioning on the transcript. The effective mixture source weights at h are proportional to 64 P_T(h) and 192 P_C(h); they are not fixed statewise 1/4 and 3/4.")

#text("Compatible-row sets at successor outcomes partition the parent. Thus the same conditional row law gives both terminal risk and next-token probabilities, and the tower identity equates exact direct finite tree loss with recursive value. The identity compares a particular row variable under one law; it does not equate losses of different mask predictors. Myopic one-step lookahead and eventual replanning-tree loss are separately evaluated.")

#text("Common union support applies to every estimator/policy: current and all positive T-or-joint successors require>=30 T rows and both people 5/6. Unsupported current state forces STOP. Supported fixed policies may stop or abstain if their next query is blocked. The seven mask domain excludes 15 and terminal three-group states have no children. Quote 1/20 and abstain 2/5 are shared. Legacy risk-only and joint results are new matched comparisons under this common domain, not an unchanged replay of the older study.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 2. Construct the participant-balanced complete-row law")]]
#v(3pt)
#strong[Require] #text("Frozen complete T/C rows for people 5,6 and seven mask predictions; labels are fitting-only inputs. Common support: at least 30 T rows and both fitting participants.")
#parbreak()
#strong[Ensure] #text("Joint row law, risks, transition probabilities and common eligible action table, frozen before DEV.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("for ")$D in {T,C}$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.96em))[#text("for ")$s in {5,6}$#text(": set ")$P_D(i)<-1/(2 n_(D,s))$#text(" for each ")$i in D_s$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[$w<-(64 P_T+192 P_C)/256$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("for each admitted transcript ")$h$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.96em))[$I_h<-$#text(" compatible rows; ")$Z_h<-sum_(i in I_h) w_i$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$Z_h=0$#text(": set risk")$<-1/2$#text("; mark unsupported; continue.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.96em))[$r(h)<-Z_h^(-1) sum_(i in I_h) w_i ell(f_S(i),y_i)$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$abs(S(h))=3$#text(": no child construction; continue.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.96em))[#text("for each remaining action ")$a$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("10")], [#block(width: 100%, inset: (left: 1.92em))[$p(z|h,a)<-Z_h^(-1) sum_(i in I_h:z_i(a)=z) w_i$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("11")], [#block(width: 100%, inset: (left: 1.92em))[#text("admit ")$a$#text(" only if every positive T-or-joint successor has common support.")]])
#v(1.2pt)
]

= #text("B.1. All budget results, abstention and paired partitions")

#text("The coherent estimator has the same complete paths as its selected fixed and myopic policies in all budgets. Budgets 2/3 give J 157023/457520. At budget 3 its loss increases by 8059/196080 versus empirical and 58067/686280 versus statewise. Lower J is better, so these are regressions. Budget 1 is a three-estimator tie. All 108 policy tables and 56592 paths complete on the same 2 exposed people/524 windows; no path multiplicity is an independent sample.")

#text("Participant 7:52 errors,100 abstentions,392 quotes, J 279/665. Participant 8:29 errors,45 abstentions,437 quotes, J 459/1720. The macro coverage is 16581/22876; pooled predicted windows 379/524 is a different summary. Against empirical, both predict 379 times:5 corrections/12 harms,145 to-abstain/0 from. Against statewise, both predict 296 times:1 correction/0 harms,145 to/83 from. Whole-objective loss includes all windows and abstentions; these subsets do not define a safety claim.")

#text("The estimator difference bundles participant balancing, the unconditional law, kernel and root weights. No causal isolation of coherence, independent generalization, provider failure or joint predictor training is claimed. Fixed global orders retain adaptive terminal stopping and abstention. Full direct raw arithmetic, every policy result and descriptive seven-mask Brier values remain in the frozen study/review artifacts.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 3. Freeze the common plan, then execute paid decisions")]]
#v(3pt)
#strong[Require] #text("Frozen risks, transitions, support and predictor bank; total budget B in{1,2,3}, quote 1/20, abstention 2/5. Adaptive, receding one-step myopic, or a fixed global order with history-dependent STOP/ABSTAIN.")
#parbreak()
#strong[Ensure] #text("Prediction or abstention; attempted/successful masks, cache, remaining budget and terminal path.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("procedure Plan")$(h,b)$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.96em))[#text("if current state is unsupported: return STOP.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.96em))[#text("compare STOP, ABSTAIN and admitted query values by the Bellman equation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.96em))[#text("STOP wins terminal ties; queries require strict improvement; lower action index breaks query ties.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.96em))[#text("fixed order permits only its next action; myopic depth is at most 1.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("freeze decision maps and selected fixed reference using T/C only.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("online: ")$S=T={0}$#text("; quote ")$q=1$#text("; reveal only the paid group 0 token.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("while the frozen map requests action ")$a$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.96em))[#text("assert ")$a$#text(" not in ")$T$#text(", ")$q<B$#text("; debit quote; ")$q<-q+1$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("10")], [#block(width: 100%, inset: (left: 0.96em))[#text("reveal selected token; update ")$S,T,h,X$#text(" with that paid result.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("11")], [#block(width: 100%, inset: (left: 0.0em))[#text("return prediction ")$f_S$#text(" on STOP, or abstention on ABSTAIN; retain ")$B-q$#text(" and evaluator-only paired scores.")]])
#v(1.2pt)
]

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Completed matched application comparison: exact adaptive macro J; coherent fixed/myopic paths tie its adaptive in every budget.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Total budget")],[#text("Legacy empirical")],[#text("Legacy statewise")],[#text("Coherent joint")]),
[#text("1")],[#text("7057/16340")],[#text("7057/16340")],[#text("7057/16340")],
[#text("2")],[#text("1364/4515")],[#text("453329/1372560")],[#text("157023/457520")],
[#text("3")],[#text("1364/4515")],[#text("10141/39216")],[#text("157023/457520")])
]

= #text("C. Independent review, historical failures and source scope")

#text("Distinct method review accepts artifact integrity, finite-law identity and saved limited DEV truth, not practical improvement, generalization or safety. Its 15 independent arithmetic/source groups inspect all 56592 paths,108 tables and 38 states per estimator;36 coherent trees match direct conditional losses. The author unit 12 and oracle 70371 records are reconciled without rerunning them. A clerical report-header adaptation was recorded before official reviewer completion; findings/checks/limits were unchanged.")

#text("Distinct search review checks 307 affordable subsets,17382 endpoints,189 seedworlds,3630 witnesses,1509 lowerbounds,549 prunes and 84 certificates via non-importing original-loss arithmetic. It accepts conditional proofs and bounded engineering truth and discloses the last-node overshoot. Reviewer first-checker failure and preseal oracle n<=3 to<=4 wording/clock-zero regression remain preserved. No producer, model or frozen failed run was repaired.")

#text("Earlier guard improvement inside 41 changed windows did not remove whole-policy 39 harms or myopic/static negatives. The actual W49 completed study differs from the selected old-through 44 companion. Its small exposed-DEV contrast and omitted failure-abstain control are historical evidence; W50 is a completed failure report with main/oracle failures and 0/12576 DEV paths. Exact old sections below preserve these values and limitations. New normal native tasks are not converted into canonical-wave worker_reports.")

#text("Related-work source scopes come from the separate selected-HTML audit and method reviewer. The local audit hash identifies the record, not full external HTML/PDF bytes. Prior prefix/truncated captures remain separate. No external numerical result is pooled with these own observations. Original AO* version/code/guarantees, methodological novelty and strongest external reproduction remain unresolved.")

= #text("C.1. Document identity, annotations and figure data")

#text("This edition uses a custom measured two-column Typst manuscript, not official qualified LaTeX or venue acceptance. BUILD follows the existing document-build schema for documents only, with scientific_certification=false. source.DOCUMENT.json is an exact byte copy of canonical DOCUMENT.json. The base builder, private renderer, current renderer and installed engine are separately hashed. PDF/HTML/source and canonical section arrays are bound for the existing owner to ingest; no browser/server probe or public pointer update is performed.")

#text("Architecture and state diagrams are source-bound interfaces, not measured hardware. New application and search figures use exact frozen result fractions/counts and their distinct units. Timing is descriptive repeated execution, not a confidence interval. All previous 55 Supp/55 Korean chapters and failures have exact structured coverage. Active sections contain actual results; historical edition-specific wording is explicitly retained as dated material. The corrected real Korean 목차 and a literal backslash-u four-hex scan guard the previous layout defect.")

= #text("D. Historical advanced corpus: exact retained sections")

#text("The following sections are the166exact structured source sections retained by the independently prepared layout: advanced-v4 supplement55, Korean55, previous main12, actualW49 and failedW50. Their dated statements remain historical; they do not override the current completed results. Full item mapping follows in COVERAGE.json.")

= #text("S1. Reconstructing the lineage and reading evidence IDs")

#text("Evidence identifiers C01-C22 are cumulative claims linked in CUMULATIVE_EVIDENCE.json to actual local source paths, SHA256 values and JSON-pointer or code coordinates. Initial observation, historical carry and current review facts are distinguished there. DOCUMENT.json is the authored source; its evidence file does not hash itself. Source hashes prove which bytes were read, not that the measured data, theorem premises or cited paper claims are true.")

#text("The inspected archival revisions are v5, v12, v13, v14, v15, v16, v17, v18, v19, v19.1, v20, v21, v21.1, v22, v23 and v24. Their immutable receipts identify parent runs and preserve the exact source. V19.1 and v21.1 are explicitly documented reading/display revisions; v20 is a document split. No undocumented v1-v4 or v6-v11 manuscript is invented to fill a version gap. References to v11 results inside later manuscripts are inherited historical reports with that scope.")

#text("The campaign starts from the initial registered reviewed MHEALTH execution and follows the receipt-selected result chain. A wave whose overall outcome is blocked can still contain a valid accepted ProbeFlow result; W2, W19, W21 and W22 are such cases. Conversely, a completed campaign wave can carry an older ProbeFlow edition without a new project execution. The complete forty-two-row inventory below is project-specific and should be read with the result status, not just the campaign status.")

#text("This edition retains the complete inherited paragraphs, tables, algorithms, historical negatives and W1-W42 inventory except explicit temporal clarification of superseded review wording. New C23-C29 entries link W44 theory, raw rows and readable independent checks. COVERAGE maps every new paragraph/table/algorithm/figure to its exact edition coordinate and an original source locator. Old PDF page coordinates are never reused.")

= #text("S2. Original module and acquisition contract")

#text("The original state records disclosed values/mask separately from acquired sources and computed analyses. An action has source prerequisites, computation prerequisites, a public output contract, an incremental quote and an availability/failure outcome. The controller receives only outputs authorized by purchased public history. A raw source cached inside the executor cannot be inferred to be publicly disclosed, and a revealed statistic cannot authorize all related statistics. The sufficiency claim depends on history-consistent resource transitions and future-observation distributions.")

#text("This distinction matters in both comparisons and implementation. Charging each of three statistics for the same already-acquired trace would alter policy rankings through a ledger error. Granting a controller an internally computed prerequisite would instead alter its information set. The historical cache/disclosure construction is an authored design; the grouped-source experiments do not separately isolate every proposed state component or prove a general POMDP reduction.")

#text("A correct history audit therefore checks the same frozen predictor, identical public observations and marginal ledger, STOP rights, and failed-attempt accounting. When every action discloses a whole source group and cache state can be reconstructed from the mask, a richer cache state may add no independent predictive information. Complementary features can still defeat one-step value heuristics. These two modeling observations should not be confused with an observed advantage for the full proposed architecture.")

= #text("S3. MHEALTH data roles, prediction bank and admission")

#text("The official archive was downloaded by the coordinator; the author consumed a fixed local copy and recorded the archive/member hashes. Before numeric processing an immutable amendment admitted the already-declared contiguous positional groups because README repeats column 13 and omits column 12. It did not resolve their physical axis labels. Groups are source columns 1-3, 4-5, 6-14 and 15-23; the label is column 24. An invalid numeric row aborts admission. Groups are engineering bundles over three placements, with ECG separated from chest acceleration.")

#text("For each source log, nonoverlapping blocks of 128 rows are anchored at row zero. Exclude a final partial block first; for complete blocks, null labels take precedence over mixed nonnull labels. Retain only a constant integer label in 1-12. Each channel supplies mean, population standard deviation and mean absolute successive difference, giving 69 channel-major features and group dimensions 9, 6, 27 and 27. These choices define the analyzed windows; they are not a clinical admission standard.")

#text("The sole shared bank fits fifteen nonempty-mask random forests on subjects 1-3, forty-eight trees per mask, depth at most twelve, minimum leaf size three, square-root feature sampling, bootstrap, balanced class weights, one thread and mask-offset fixed seeds. Empty-mask output is the fit-only prior. Subject 4 selects a temperature from 0.25,0.5,1,2,4 by NLL. Argmax class ties choose the smallest label, temperature ties the first grid value. Calibration changes confidence and STOP behavior; it is not automatically an argmax classification gain.")

#text("Subjects 5-6 estimate second-action gains conditional on first mask, predicted class and right-sided margin bin with cutpoints 0.1,0.25,0.5,0.75. Fewer than twenty examples use the same-mask unconditional action; action ties choose the smallest group. The fixed grid has eleven size-at-most-two subsets, seventy-two ordered-pair/threshold rules, twenty-four myopic rules and twenty-four routing rules. The total is 131 candidates; twenty-four full-order aliases are preserved because suffixes after the two-attempt cap cannot affect a path. Subjects 7-8 select by macro J, mean quote, mean error and canonical ID. [C07]")

= #text("S4. Empirical execution, adaptation gate and original controls")

#text("The source bank is sealed once, and its readiness is distinct from permission to open target subjects. Joint release binds both ProbeFlow and ChronoSense policy seals. Target subjects 9 and 10 are decoded once under that contract, selected aliases are deduplicated into canonical executions, and target results cannot replace a selected comparator. The same bank shared across projects is charged/identified once and does not create two independent dataset replications.")

#text("MHEALTH requires a negative primary macro contrast, no participant-level positive contrast, at least two selected second-group types with twenty or more windows each, and a positive complete second-action denominator before an adaptive-gain claim. Development branch support must pass as well. Development used only G4 in all 252 second actions; an explicit frozen descriptive release allowed evaluation while keeping that support failure active. Target second actions were G4 in 129/129, all using the sparse-state fallback. Consequently branch support and strict improvement both failed, despite a nonzero target second-action count.")

#text("The selected target path counts are 398 G3-to-STOP and 129 G3-to-G4. Participant 9 has n=267, 50 second acquisitions, 22 errors and 317 attempts; participant 10 has n=260, 79 second acquisitions, zero errors and 339 attempts. Fixed G3+G4 uses two attempts per window and zero errors. Accepted, failed, late and unread-pending attempt partitions were all retained, with the last three equal to zero under the primary no-injection condition. Missing G3-only outputs on requested windows cannot be recovered from this ledger alone.")

#text("The existing standard-library verifier independently reaggregated 68,644 development and 2,108 selected evaluation trace rows, reselected dev winners and reconciled paths/classes/costs without importing the runner aggregation helpers. It did not independently rewrite the raw source parser. Poisoned unpurchased-feature and evaluator-label/ID controls preserved controller outputs. A four-binary-group fixture checked masks, aliases, STOP and ties. Those checks validate the local boundary under their assumptions, not adversarial OS isolation or a new independent population experiment.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 4. Frozen offline acquisition and support audit")]]
#v(3pt)
#strong[Require] #text("Pinned source/member hashes and subject roles; frozen shared mask predictor, calibrated margins and selected policy IDs. Two-attempt quote contract, STOP rule, primary macro comparator and declared branch-support gain gate.")
#parbreak()
#strong[Ensure] #text("One canonical path/prediction/cost ledger per selected episode, all aliases and participant/class/branch summaries. Exact paired contrast with no_gain, insufficient_support or explicitly justified improvement status.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Validate row/window admission and preserve exclusion counts; build fit-only features and prediction banks using only allowed subjects.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Fit action tables and select every family on the assigned development subjects; store both policy seals before joint evaluation release.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("At each target history reveal only purchased groups. STOP on the frozen margin condition or acquire at most one additional group under cap two.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Charge every accepted or failed attempted acquisition under the same ledger; store late/pending/missing partitions instead of dropping them.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Deduplicate selected canonical IDs while retaining alias links; compute participant means before the unweighted macro contrast.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Evaluate strict contrast and branch-support gates separately. Preserve a failed support gate even if a secondary predictor diagnostic looks favorable.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Audit saved traces with separate aggregation and negative controls, without reopening targets for policy revision.")]])
#v(1.2pt)
]

= #text("S5. Partial identification: assumptions that changed the answer")

#text("At zero failure penalty W2 gives a conditional route-static contrast 9653/2776800 when all requests succeed. Its eighteen-cell calculation varies a common failure rate q and an additional penalty k, with the conditional independence break-even 9653/114400 at k=0. The interval includes unknown G3 fallbacks on 129 requested windows. A sensitivity grid is an algebraic model over existing traces; no failed or delayed target attempt was observed.")

#text("W5 optimizes dependence between failure and loss rather than inserting independence. For participant-specific marginal failure q=1/20,k=0, its Delta bounds are [-59767/2776800,9653/2776800], whereas the independence value is 1311/925600. Both strict rankings remain possible. The route-universal threshold under that family is q>1283653/1388400, a conditional sharp statement that differs from the independence break-even. The pooled-opportunity family weights a different set of opportunities and is separately tabulated.")

#text("W6 distinguishes pointwise-uniform availability from a participant mean and shared G3 fallback from separate acquired-window fallbacks. With both success marginals 1/2 and k=0, pointwise-uniform/shared fallback yields the point value -15849/925600; separate fallback admits [-388477/2776800,293383/2776800]. Merely reporting the same average availability hides the relevant placement and coupling assumptions. Its one/two-window constructions are counterexamples, not new measurements.")

#text("W7 shows that learning an upper or exact count of fallback errors need not resolve policy sign. At half success and k=0, fixing every unknown requested error to zero shrinks width by about 92.26 percent yet leaves both strict rankings possible. At k=1/20 the saved example is route-strict up to error cap four, but cap five crosses zero. W8 adds guaranteed availability bins at known stop-error windows; low and high readings can favor opposite policies. An error count, a queried availability value and a failure observation are different data. [C09-C11]")

= #text("S6. Shared-cap endpoint reconstruction and sharpness")

#text("For fixed subset S and bin reading z, let Omega(S,z) contain the binary requested errors and rational availability vectors satisfying all declared constraints. The sharp endpoints are min and max of Delta over this set, not a confidence interval for a sampled population parameter. A feasible world for the lower endpoint may differ from the upper-endpoint world. Empty Omega is an impossible reading and remains distinct from execution failure.")

#text("For a fixed local binary error placement, each availability optimization is linear over l_i<=x_i<=h_i with sum x_i=m. Feasibility is sum l_i<=m<=sum h_i. Start at l; sort coefficients ascending for minimization or descending for maximization; allocate the remaining mass up to each h_i-l_i. A pairwise transfer from a worse to a better coefficient improves any allocation violating this order. This proves exactness for fixed binary errors. Enumerate the binary placements for each exact count j and retain both extrema.")

#text("Across participants use weights 1/(P*n_j). The min/max convolution combines local exact-count curves under a single total count <=B. Replicating B at every participant admits worlds outside the original model; pooling weights instead changes the estimand. W14 measured both errors in constructed controls. W12 also exposed competition for availability mass when prior slack is insufficient, so a simplified independent sorting expression from the restricted parent regime must not be used as a general sharp oracle.")

#text("W15 performs this endpoint calculation for every feasible bin transcript of every fixed subset and takes its maximum width. The exact all-subset selector and the original-world reference have equal public information, budget and objective. Their equality establishes implementation consistency; any improvement over that exact reference would signal either a changed problem or an error.")

= #text("S7. Prefix bounds, output completeness and rejected shortcuts")

#text("A partial reading creates a larger world set than any completion. Its sharp interval contains every completed interval, even though a difference between the two endpoints is not itself an endpoint realized by one world. Width containment is enough for an upper bound on the inner maximum. The incumbent b comes only from a completed feasible transcript; a prefix before any such leaf cannot justify pruning by an invented incumbent.")

#text("Strict comparison is required by the requested output, not just by conservative numerics. If an internal upper width equals b, some descendants can be additional worst-transcript ties. The saved zero-width example and W22 equality example show such losses under an equality cutoff. Bounds that are safe for finding one numeric maximum may be insufficient for listing all maximizers. Subset primary ties and worst-transcript ties are distinct collections and both are preserved.")

#text("The non-submodular construction has nested masks 4 subset 5 and adds the same remaining item: risk stays 3/8 from mask4 to6, but drops from 3/8 at5 to1/4 at7. For F(S)=R(empty)-R(S), the latter marginal is 1/8 while the former is zero. This falsifies diminishing returns for this declared objective, so stale-marginal lazy greedy has no transferred certificate. It neither refutes the published Bayesian adaptive-submodularity theorem nor proves every alternate prior/model non-submodular.")

#text("W19 maintains DFS coverage records for feasible leaves, impossible subtrees and strictly pruned subtrees; the disjoint completion counts reconcile to the full subset label family. A safe upper for R(S) cannot eliminate S in the outer minimization as though it were a lower bound. W22 preserves a numeric example with upper1/2, outer incumbent1/3 and exact mask2 value1/3: confusing bound direction would lose an affordable primary tie. [C15-C18]")

= #text("S8. Local envelopes and shared marginal allocation proof")

#text("Expand the unweighted local original loss difference as D=C-k*sum_A r+sum_E v+T, where C=-(n-a)(c+k)+k*m, m=n/2 and T=sum_A u_i(v_i-r_i). Write l_A,h_A,l_E,h_E,l_O,h_O for aggregate box bounds. Then rL=max(0,m-(n-a)), rU=min(a,m), eL=max(l_E,m-h_A-h_O), and eU=min(h_E,m-l_A-l_O). Summing w(C-k*rU+eL) and w(C-k*rL+eU) yields the common base [L0,U0].")

#text("For an exact requested-error count b, the coupling term is bounded below by -min(b,a-l_A) and above by min(b,h_A). Optimizing each sign correction over global sum b_j<=B gives f_j(b)=w_j min(b,c_j). Solving these corrections independently from the base relaxes coupling inside a participant, so the resulting interval is outward and need not be sharp. Solving the shared global cap is tighter than permitting every participant its own full cap. At B=0, T vanishes and the independent base extrema can be attained.")

#text("For integer t>=1 the marginal is w_j*min(1,max(0,c_j-(t-1))). This is nonnegative and nonincreasing even when the cap c_j is fractional. Any allocation of b_j units selects the first b_j entries of chain j. The largest unseen marginal must be a chain head because every later entry is no larger. Popping the greatest head therefore obtains a globally greatest remaining marginal and exposes the next entry of that chain. By induction the heap selects a prefix-closed set of q=min(B,positive-entry count) largest gains, attaining the upper bound on any feasible allocation. Zeros need not consume the at-most budget.")

#text("Scalar equality with the shared DP follows separately for minus and plus signs before the old width/pruning proof is reused. Equal marginal choices may yield several allocation witnesses but do not change the scalar bound. The algorithm still reports every maximizing bin transcript and every affordable primary-risk subset; a heap tie order for allocation is not a license to discard those output ties. The exact sharp endpoint, with its separate local binary enumeration/cache/DP, remains unchanged. [C19,C20]")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 5. Shared-cap envelope with strict full-tie transcript traversal")]]
#v(3pt)
#strong[Require] #text("Public feasible box/mean model, requested/known-error partitions, global cap B, guaranteed closed bins and positive query prices. Frozen sharp endpoint implementation, same stop-error-first/index order and per-solver initially cold cache contract.")
#parbreak()
#strong[Ensure] #text("Safe shared envelope at each visited prefix; exact risk, every worst label and all affordable risk ties after complete processing.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Validate field sets, dimensions, cap, prices, thresholds and box/mean feasibility; retain impossible coverage instead of changing the model.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Visit each fixed subset in the declared common coordinate order; traverse label zero before one and do not bound-cut before a feasible leaf supplies an incumbent.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("At a complete feasible reading evaluate the sharp endpoint, update maximum width and append every equal-width label.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("At an internal prefix aggregate L0,U0 and both local marginal-chain parameters. B=0 returns the base without heap/DP allocation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("For each sign independently heapify first positive marginals, pop the largest and advance its chain until B pops or positive exhaustion; alternatively run the exact shared-count DP.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Use [L0-Mminus,U0+Mplus] as an inner-max width upper. Cut only when strictly below the completed-leaf incumbent; expand equality.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Record feasible, impossible and pruned completion partitions; retain every subset risk before applying each query budget and the separate complete primary-tie rule.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compare saved raw original-loss endpoints and integer allocations with the separate no-import audit; retain regression costs and unresolved assumptions.")]])
#v(1.2pt)
]

= #text("S9. Finite solver fixtures and the strong exact controls")

#text("W39 uses one synthetic two-participant heterogeneous structure and B in {1,0}; its 64 subset-risk records, 486 complete labels and twenty budget decisions must not be counted as twenty independent trials. Four solvers share exact endpoint rights: flat, sharp-prefix cached, cap-relaxed and shared-cap DP. At B1, shared DP endpoints201 versus relaxed208 is a seven-call reduction, but sharp-prefix121 is much lower. Linear calls480 and observed CPU0.046875 seconds remain unchanged between relaxed and shared. At B0 no new allocation improvement is available, and shared paired output51465 bytes exceeds relaxed51342.")

#text("W41 fixes n=(3,2,2), a=(2,1,1), e=(1,1,1), k=1/10, thresholds=(1/5,1/2,4/5,1/3,2/3,1/4,3/4), prices=(1,2,1,2,1,3,2), B in {2,0}, Q=0,...,12. Each cap evaluates all128 subsets, including budget-ineligible diagnostics. The original-world oracle checks binary requested-error placements and box/sum vertices with a separately written path; the allocation audit checks stored sign maxima against direct integer allocations. These are exact constructed checks with zero new observed participants.")

#text("Five W41 solvers have identical stop-error-first/index order, label order, sharp endpoint bytes, cold cross-mask/local cache rights, objective and outputs. The heap receives only implicit local parameters, not a completed DP table. All ten solver-condition records completed; risks, canonical choices and every tie agree. The raw-only author oracle is separate implementation by the author, while coordinator review is a separate authorship boundary. Neither is an external real-world replication.")

#text("B2 exact risks have thirteen budget decisions and all tie the empty subset in primary risk; price chooses the empty set canonically while risk ties proliferate. This is a strong no-gain result about query usefulness in that fixture, not solver failure. Heap-vs-DP scalar equality yields zero additional endpoint or pruning savings. At B0 the heap is bypassed; any CPU difference among labels includes nonallocation work and measurement noise.")

= #text("S10. Work, memory, bits and failed performance hypotheses")

#text("The cost columns refer to nested scopes and must not be added blindly. Solver CPU includes its own preprocessing, search/trace writes and decision/result output under the same Fraction profiler and tracemalloc. Whole-main CPU additionally includes common orchestration/output; direct-stage CPU includes process startup. Authoring-model tokens/cost, launcher work, operating-system RSS, all physical I/O and intermediate Fraction-product bits are outside these scopes. The cumulative author performed no new timings.")

#text("W41 B2 observed heap CPU22.875 seconds versus DP24.5, cap-relaxed22.21875 and sharp-prefix8.921875. Heap Python peak4350232 bytes exceeds DP4347301; heap data output1099471 exceeds DP1090097. A single instrumented observation neither estimates a stable speed ratio nor establishes total-cost dominance. Earlier W19 leaf reduction accompanied increased endpoints/raw bytes; W21 endpoint reduction accompanied CPU/node/retention regressions. The record deliberately retains these failures of the efficiency hypothesis.")

#text("The exponential output itself matters. Complete bin-label families scale as3^N across all subsets, and listing all tied labels may require similarly large disk output even if numeric workspace streams. Copied box keys, cache values and retained per-subset arrays are additional memory; DFS retains state across depth. Heap O(P) storage is only its local allocator space. A lower-bound statement should use the actual total serialized length, while shared in-memory child objects may have fewer distinct objects.")

#text("Current W42 O(K*m^2*h^2) and Omega(K*T) claims remain explicitly partial under its review. Stop-only h0 still evaluates prediction/loss, and maximum tree size T alone does not prove total explicit size equals K*T. This edition does not convert a review request into a repaired proof. Bit bounds need input and returned rational sizes, intermediate products, GCD/comparison cost and serialization length distinguished; observed seven or ten bits alone provide no such general bound. [C22]")

= #text("S11. sequential-objective analysis formal translation and exact witness arithmetic")

#text("The theorem begins with a common feasible world set, deterministic public observations, identical feasible subset family, prices and hard path budget. Always-available immediate true-value reveals, no failure/delay, no repeated purchase and no additional chronology are substantive assumptions. Restrict the sequential policy to one precommitted subset and an explicitly common order. Map S to its open-loop reveal tree and that tree back to S. If observation functions are closed-bin correspondences at thresholds, model each feasible label explicitly on both sides.")

#text("A terminal-width bridge g(S,omega)=W(S,x_S(omega)) is then imposed. It can be encoded as absolute regression loss against zero with predictor W, but that synthetic construction is not the original learned prediction target. If every transcript has positive p_t, max W-E W=sum p_t(max W-W_t). Every term is nonnegative, so equality holds precisely when every feasible transcript width is constant for that subset. To preserve values for every policy, require this for every allowed subset. Accidental equality of optimizers under weaker conditions is possible and does not prove policywise equivalence.")

#text("With alpha=0 and a common hard budget, preserve secondary lex(price,mask) separately from the complete primary-risk tie collection. Positive additive price can select only the cheapest member of a primary-risk tie. A sufficiently small alpha can preserve an isolated finite lex optimum relative to positive risk gaps but cannot retain unequal-price primary ties as additive minimizers. An adversarial distributional supremum equals max g, but substitutes a robust problem for a fixed learned-distribution objective.")

#text("Example1 worlds are (A=0,y=0,p=1/4), (A=0,y=1,p=1/2), (A=1,y=0,p=1/4), with feature price1, hard budget1, alpha1/8. The fixed Bayes predictor has initial tie prediction0 and expected stop error1/2. Buying A leaves expected error1/4, so priced expected value1/4+1/8=3/8. The worst world still errs, producing buy worst value9/8 versus stop1. Delta=y width remains1 at empty and at the ambiguous A0 transcript; both subset worst risks are1. Twelve direct world checks cover two public policies and two subsets.")

#text("Example2 worlds are (A=0,B=1,y=0,p=1/2), (1,0,0,1/4), (1,1,1,1/4), with two unit prices, hard budget2 and alpha1/16. Query A, STOP at0, query B at1 gives zero error and expected price1+1/2=3/2; priced expected loss is3/32. Static AB has zero error and price2, hence1/8. Adaptive and static worst price2, error0 and worst width0 tie. Nine public policies and four subsets give39 direct world checks. The two examples total11 policies,6 subsets,51 world checks and zero new empirical samples.")

#text("The saved unrestricted binary policy count obeys F(n,h)=1+n*F(n-1,h-1)^2 with F(n,0)=1 in the always-affordable fixture: F(1,1)=2 and F(2,2)=9. A fixed predictor is not an extra prediction action. The theorem concerns restricted open-loop policies; the harness also enumerates allowed adaptive STOP trees to expose the class difference. No trained surrogate, original AO* implementation or W41 solver is executed in these witnesses.")

= #text("S12. Source reading, related work and attribution limits")

#text("Historical official abstract pages for Shim et al., Li and Oliva, and Cawley and Talbot motivated acquisition/selection contracts. They did not certify original architectures or reproduce benchmark scores. W18 later read selected cached adaptive-submodularity body ranges but retained its one-byte source-limit protocol deviation, missing failed raw and text LF/CRLF hash distinction. A partial saved body and an unverified publisher/version identity remain partial related work.")

#text("The W42 cached GSMRL body is unversioned ar5iv content with recorded full byte hash. Its selected source bytes and 132 math nodes were directly compared in that study, with additional reviewer header reading. This edition reads the saved source-read receipt and reports its bounded scope; it does not independently fetch the publication. GSMRL reporting AO* and a Zubek et al.2004 bibliography entry is indirect evidence, not reading the original AO* body or resolving the 2002/2004 identity.")

#text("The historical annotation map contains eight retrospective editorial connections to Fei-Fei Li, Kaiming He, Andreas Krause, Donald Rubin and Judea Pearl, with public source IDs and explicit reading scopes. The v15 map contains actual saved Codex issues under Bengio and He lenses; the named people did not author that review. Its two current issues take precedence for the corresponding immutable revision. The new exact-paragraph links retain this provenance, with no recycled page coordinates, new scholar feedback or generic companion marks presented as Big Guy advice.")

= #text("S13. Full early research campaign project inventory and retained negatives")

#text("Each row below is grounded in its own campaign receipt. The evidence artifact records exact receipt/result/METHOD hashes, source pointers, summaries, parent carry and status distinctions. The accepted W10 failure remains a failure even though the controller accepted its provenance. W13 start observation is unknown before freezing; W25 and W34 are failed operational starts with no author research. Unattempted slots are not scientific failures or successes.")

#text("The table includes every wave number rather than inferring a scientific experiment from a wave title. Repeated publication, inherited evidence, optional source inspection and operational readiness checks create neither new participants nor new independent prediction measurements.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Complete cumulative wave inventory; status concerns ProbeFlow only.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Wave")],[#text("Project status")],[#text("Scientific limitation / negative / carry")]),
[#text("1")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("2")],[#text("accepted bounded result")],[#text("Conditional failure model; strongest baseline tie; unknown fallback129; no new failures observed.")],
[#text("3")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("4")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("5")],[#text("accepted bounded result")],[#text("19/36 strict rankings nonidentified; myopic tie remains.")],
[#text("6")],[#text("accepted bounded result")],[#text("24/72 cells allow both strict rankings; shared/separate fallback changes result.")],
[#text("7")],[#text("accepted bounded result")],[#text("Upper/exact no_gain534/530; zero-error sign ambiguity; no new measurements.")],
[#text("8")],[#text("accepted bounded result")],[#text("No_gain58/322 and placement controls92/92; hypothetical availability only.")],
[#text("9")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("10")],[#text("accepted failed result")],[#text("FAILED: substantive main at least twice; accidental second temporary raw absent.")],
[#text("11")],[#text("accepted bounded result")],[#text("Count-only ties14228/29120; parent failed replay remains recorded.")],
[#text("12")],[#text("accepted bounded result")],[#text("Old formula nonsharp4913/6548; cap/exact differ1294; information no_gain2362.")],
[#text("13")],[#text("operational failure no scientific result")],[#text("Start observation unknown; frozen without scientific main/result.")],
[#text("14")],[#text("accepted bounded result")],[#text("Information no_gain974; infeasible672; replicated shared cap nonsharp912.")],
[#text("15")],[#text("accepted bounded result")],[#text("No_gain29/73; pooling regret20; cheapest regret12; exponential oracle.")],
[#text("16")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("17")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("18")],[#text("accepted bounded result")],[#text("Non-submodular; heuristic regret1/60; source-read protocol gaps.")],
[#text("19")],[#text("accepted bounded result")],[#text("Leaf837→642 but endpoint837→1370 and raw183934→287257; no compute gain.")],
[#text("20")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("21")],[#text("accepted bounded result")],[#text("Endpoint785→741; 2/4 no endpoint gain; CPU/node/output regression.")],
[#text("22")],[#text("accepted bounded result")],[#text("Endpoint17→17; nodes18→28; original AO* uninspected.")],
[#text("23")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("24")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("25")],[#text("operational failure no scientific result")],[#text("Readiness/update prompt failed before author research; no result.")],
[#text("26")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("27")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("28")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("29")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("30")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("31")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("32")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("33")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("34")],[#text("operational failure no scientific result")],[#text("Readiness/update prompt failed before author research; no result.")],
[#text("35")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("36")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("37")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("38")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("39")],[#text("accepted bounded result")],[#text("B1 endpoint208→201 but sharp121; linear480 tie; B0 no allocation gain.")],
[#text("40")],[#text("unattempted by project receipt")],[#text("No ProbeFlow worker/result in receipt; earlier edition carried.")],
[#text("41")],[#text("accepted bounded result")],[#text("B2 all13 budgets tie empty risk; no extra pruning; heap output/peak exceed DP.")],
[#text("42")],[#text("accepted bounded result")],[#text("Worst price/error/width ties; canonical trace and h0/shared-object complexity gaps.")])
]

= #text("S14. Current six-area review and next acceptance conditions")

#text("At W42 the algorithm review was partial because stop-error-first and increasing-index orders were not aligned. W44 now gives an explicit bidirectional ID-preserving terminal quotient, as proved above, for static relation semantics. This does not prove equal original ordered action/diagnostic execution. Delay, availability, failure, chronology and history-dependent STOP retain non-comparable status when those assumptions fail.")

#text("Architecture exists within the sealed finite harness: public fixtures to public policy to original-world loss to saved raw to no-import author audit, with explicit failure/unknown boundaries. It does not certify a real acquisition platform or OS sandbox. Complexity is partial: account for h0 STOP work, distinct shared objects versus serialized length, posterior scans, rational bits and output cost without presenting a new unproved asymptotic expression as a fix.")

#text("Evaluation is partial: no independent physical acquisition group, availability/failure/delay receipts, real model training/inference utility or practical scale. Baselines exist for the finite problem: complete public trees/subsets share fixed prior, predictor, loss, price and budget, with intentionally changed objective/class rows marked non-comparable for algorithm superiority. Application baselines remain unrun. Related work is partial: directly inspect original AO* body/version/guarantees and Ng/Shim primary under a separate bounded reading contract.")

#text("This authoring task checks source hashes, JSON schema, exact paragraph links and text integrity only. It creates no experiment, replay, API/network/model request, external/person review, skill activation, publication, registration or lifecycle transition. The coordinator owns compilation, PDF size/page/render verification, independent cumulative review, exact-edition annotation placement, publication and Task settlement.")

= #text("S15. Full terminal proof, boundary semantics and exact scope")

#text("Assumption ledger: immutable unique IDs; one common nonempty Omega; identical static per-ID relation; the same fixed subset; all selected items acquired once; immediate always-successful reveals; no chronology restriction; common terminal STOP; order-invariant terminal Delta or predictor; additive fixed prices and common hard Q. Feasible-world equality itself uses only the common conjunction. Claims about executed acquisition and price additionally need the acquisition/STOP/cost assumptions. These logical dependencies should not be collapsed.")

#text("For any omega in F_pi(b), each i in M occurs at position pi inverse(i), so R_i(omega,b_pi_inverse(i)) holds. At sigma's position j, i=sigma_j and T(b)_j is exactly this same label. Thus every required sigma atom holds and omega belongs to F_sigma(T(b)). Interchanging pi and sigma proves reverse inclusion. Composition gives b_pi_inverse(sigma_sigma_inverse(pi_j))=b_j. The transformation therefore preserves both feasible and impossible tuples; no label mass is silently discarded.")

#text("For any equal nonempty feasible sets F, the sets {Delta(omega):omega in F} coincide. Their infima and suprema, and therefore widths, coincide. On the stored bounded closed polytopes with a finite binary component, the extrema are attained. The bijection transports every width maximizer in both directions; retaining one representative is insufficient when complete ties are requested. After fixing the same affordable subset family, equality of every R and C transports primary subset ties as well as the lex representative.")

#text("At a threshold t the original bins are [0,t] and [t,1]. A boundary value may therefore appear in both labels. Keep the relation, or introduce an expanded world carrying a fixed admissible label assignment, consistently on both sides. One cannot break a tie differently because a coordinate was asked first. The saved boundary point (1/5,1/2,4/5) has sum 3/2 and belongs to all four queried-label pairs for IDs0 and2; it confirms overlap was preserved rather than rounded away.")

#text("A=action trace and D=solver diagnostics remain outside this proof. Equal order and common reveal/STOP rules give the same A by a position-by-position induction, with coupled worlds/labels fixed. Equal A that retains all item IDs forces equal order by inspection of each position. Different order can share the same terminal ID reading without the same prefix worlds, bounds, cache state, first incumbent or work. None of those computational equalities follows from conjunction commutativity.")

#text("Empty M has one empty tuple, F=Omega, C=0 and one worst-tuple tie; an invalid empty Omega is rejected. These semantics do not supply the previously missing h=0 policy-generation complexity argument. Likewise a pushforward prior preserves expectation across two static orders only; equality of expectation and maximum additionally requires the W42 full-support/constant-width condition, which the W44 unequal widths fail to provide.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 6. ID-preserving terminal reindexing and complete-tie audit")]]
#v(3pt)
#strong[Require] #text("Fixed M; valid unique-ID permutations pi and sigma; complete label tuples; common immutable world/relation/Delta specification. Fixed additive prices, hard budget and full output contract; separate stored action/diagnostic records.")
#parbreak()
#strong[Ensure] #text("Reindexed tuple for every original tuple, inverse correspondence, equal feasible worlds/endpoints/widths/prices and transported full ties, or an explicit failed static-assumption comparison. Original action schedules and diagnostic records preserved without an equivalence or speed claim.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Check that pi and sigma are duplicate-free permutations of the same fixed M and that all label tuples have the matching length; reject mismatches before evaluating endpoints.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Require the same observation relation including closed-bin boundaries. Establish the acquisition/STOP/cost assumptions before extending terminal claims to schedules or prices.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("For each full original tuple construct an ID-to-label dictionary and emit its labels in sigma order; use the reverse map to recover the original tuple.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Build both conjunctions with the same immutable world/constraint/Delta inputs. Preserve infeasible tuples and compare every nonempty endpoint pair, not only its width.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Take the width maximum for each order and transport all maximizing tuples back to the same ID-keyed set. Compare price and budget with the same ledger.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Store original action-ID sequences and original solver prefix diagnostics separately; do not sort those records and call the runs identical.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("In the separate deadline environment, apply the same deadline/duration/price rules to both schedules, retain the rejected prefix and its compatible worlds, and label the result an assumption-violation counterexample.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Report one saved subset/four conjunctions, eight static encodings and eight deadline rows. A raw-only or independent arithmetic recheck adds validation passes, never independent samples.")]])
#v(1.2pt)
]

= #text("S16. Reconstructing all eight saved static encodings")

#text("The fixture uses stored mask5, M={0,2}, price 2, in the unchanged W41 n=(3,2,2), a=(2,1,1), e=(1,1,1), B=2 environment. The remaining five coordinates still constrain the original route/static loss; they were not new queried actions. Thresholds for the queried coordinates are 1/5 and 4/5. The original saved order is [2,0] and canonical order [0,2]. The source input record gives original JSON and JSONL hashes as well as the extracted subset copy.")

#text("Every row below is saved in raw_001/static_permutation.json. The strong reference builds a conjunction directly from the ID labels; the candidate reconstructs it through the immutable positional helper. The raw-only audit substitutes original route/static loss into box/mean vertices and globally capped binary errors without importing study helpers. The coordinator's saved arithmetic independently recomputed four distinct conjunctions, not eight independent datasets.")

#text("For original labels (0,1), the first label belongs to ID2 and the second to ID0. In canonical order the tuple is (1,0). Their lower=-11/90 and upper=43/90 give width (43+11)/90=54/90=3/5. Original tuples (0,0),(0,1) are worst; canonical tuples (0,0),(1,0) are worst. Both map to z2=0 and z0 in {0,1}. The saved price equals 1+1=2. No terminal risk or price advantage occurred.")

#text("For z2=1 the lower changes to -4/45=-8/90, giving width (43+8)/90=51/90=17/30. Four unequal-width conjunctions show why preserving the maximum is weaker than making all transcript widths equal. Direct endpoint equality and an inverse map are stronger checks than a rounded equality of two decimal maxima.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("All static rows; one stored subset, four unique ID conjunctions, two encodings each.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Order name")],[#text("Tuple")],[#text("ID-label pairs")],[#text("Lower")],[#text("Upper")],[#text("Width")],[#text("Price")]),
[#text("original_ord​er")],[#text("[0, 0]")],[#text("[[0, 0], [2, 0]]")],[#text("-11/90")],[#text("43/90")],[#text("3/5")],[#text("2")],
[#text("original_ord​er")],[#text("[0, 1]")],[#text("[[0, 1], [2, 0]]")],[#text("-11/90")],[#text("43/90")],[#text("3/5")],[#text("2")],
[#text("original_ord​er")],[#text("[1, 0]")],[#text("[[0, 0], [2, 1]]")],[#text("-4/45")],[#text("43/90")],[#text("17/30")],[#text("2")],
[#text("original_ord​er")],[#text("[1, 1]")],[#text("[[0, 1], [2, 1]]")],[#text("-4/45")],[#text("43/90")],[#text("17/30")],[#text("2")],
[#text("canonical_or​der")],[#text("[0, 0]")],[#text("[[0, 0], [2, 0]]")],[#text("-11/90")],[#text("43/90")],[#text("3/5")],[#text("2")],
[#text("canonical_or​der")],[#text("[0, 1]")],[#text("[[0, 0], [2, 1]]")],[#text("-4/45")],[#text("43/90")],[#text("17/30")],[#text("2")],
[#text("canonical_or​der")],[#text("[1, 0]")],[#text("[[0, 1], [2, 0]]")],[#text("-11/90")],[#text("43/90")],[#text("3/5")],[#text("2")],
[#text("canonical_or​der")],[#text("[1, 1]")],[#text("[[0, 1], [2, 1]]")],[#text("-4/45")],[#text("43/90")],[#text("17/30")],[#text("2")])
]

= #text("S17. All deadline rows and the exact rejected prefix")

#text("Four worlds (x0,x2)=(0,0),(0,1),(1,0),(1,1) share target x0 XOR x2, unit action duration/price, budget2 and completion deadlines d0=1,d2=2. Both schedules begin at time0. For [2,0], item2 completes at1 and item0 would complete at2; the second action is rejected before acquisition because2>1. Price remains1 and actual elapsed ticks1. The record completion_time2 is the proposed disallowed completion, not an executed second acquisition or actual elapsed time.")

#text("When item2=0 the rejected prefix leaves worlds w00 and w10; when item2=1 it leaves w01 and w11. In either pair XOR ranges from0 to1, hence width1. For [0,2], both items meet deadlines at1 and2, price2, and the compatible world is a singleton with width0. The eight rows are two schedules applied to the same four constructed worlds.")

#text("Completion0/4 versus4/4 demonstrates schedule dependence under this deliberately changed environment. These are not binomial samples, natural sensor failure rates or candidate/base accuracy observations. There is no deadline injected into the original W41 optimization, no new full search, and no use of its static price2 as the successful price of a failed schedule.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("All deadline schedule/world records; rejected-prefix price and actual elapsed ticks retained.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Order")],[#text("World")],[#text("Status")],[#text("Revealed prefix")],[#text("Price")],[#text("Elapsed")],[#text("Residual XOR width")]),
[#text("original_ord​er")],[#text("w00")],[#text("infeasible_s​chedule")],[#text("[[2, 0]]")],[#text("1")],[#text("1")],[#text("1")],
[#text("original_ord​er")],[#text("w01")],[#text("infeasible_s​chedule")],[#text("[[2, 1]]")],[#text("1")],[#text("1")],[#text("1")],
[#text("original_ord​er")],[#text("w10")],[#text("infeasible_s​chedule")],[#text("[[2, 0]]")],[#text("1")],[#text("1")],[#text("1")],
[#text("original_ord​er")],[#text("w11")],[#text("infeasible_s​chedule")],[#text("[[2, 1]]")],[#text("1")],[#text("1")],[#text("1")],
[#text("canonical_or​der")],[#text("w00")],[#text("completed")],[#text("[[0, 0], [2, 0]]")],[#text("2")],[#text("2")],[#text("0")],
[#text("canonical_or​der")],[#text("w01")],[#text("completed")],[#text("[[0, 0], [2, 1]]")],[#text("2")],[#text("2")],[#text("0")],
[#text("canonical_or​der")],[#text("w10")],[#text("completed")],[#text("[[0, 1], [2, 0]]")],[#text("2")],[#text("2")],[#text("0")],
[#text("canonical_or​der")],[#text("w11")],[#text("completed")],[#text("[[0, 1], [2, 1]]")],[#text("2")],[#text("2")],[#text("0")])
]

= #text("S18. Source-path correction, damaged review and independent validation")

#text("W44 SOURCE_READS.json declares study_copy snapshots/gsmrl_response.bin, but that path is absent. The actual preserved original is projects/research_autonomous_20261022_01/waves/wave_000022_52097256b0b4/projects/probeflow/snapshots/gsmrl_response.bin, length246752 bytes, SHA25668c70a3a4f6a0746648ab2d3c2eb56a0cceae2679f642e7020c38c06088335df. Its origin and the existing W44 pinned range/excerpts are preserved separately; this document fixes its own link without modifying the frozen receipt.")

#text("The W44 selected excerpts use physical original UTF-8 byte ranges [26876,30240), [48940,50990), [89303,91186), [92629,93211), lengths3364,2050,1883,582 (total7879). They address acquired sets/remaining candidates/STOP/reveal, terminal prediction, and chronological action restrictions. Existing source hashes identify retained bytes, not scientific truth or a certified publisher/arXiv version. This authoring task adds no network source read.")

#text("The saved W44 independent_checks.json records source3_match=true, execution_seal_files_matched43, static_rows8, distinct_static_conjunctions_recomputed4, deadline_rows8, endpoint_mismatches0 and matching closed-boundary labels. It imports/replays no author study code and adds no application data. This is an independently authored finite arithmetic review in the same research environment; it is not an external population replication or proof of the general theorem.")

#text("Frozen METHOD_REVIEW.json and METHOD_REVIEW.candidate.json include question-mark damage in some prose. They remain unchanged and hash-linked. The current edition makes no claim that their missing text was restored or that a previous submission/intake hold was lifted. It distinguishes raw numeric checking, author document selfchecks and any later independent document review. The coordinator owns PDF compilation/render/page/size checks and any publication or official Task settlement.")

= #text("S19. terminal-order analysis work accounting and the remaining acceptance ledger")

#text("The order adapter moves k label references, after constructing an ID map, in O(1+k) average dictionary operations and O(k) additional references for fixed-length labels and ordinary hashing. General variable-size IDs/labels require byte/bit hashing, comparisons and copies; an explicit serialized output of lengthL costs Omega(L). This adapter excludes all endpoint computation, 2^k tuple enumeration, rational-vertex work, shared-cap optimization and original diagnostic search.")

#text("Per saved static row k=2 and input/output label JSON each has5 bytes. W44 main observed7 returned/input integer bits; it did not profile every temporary multiplication/GCD. The direct-stage CPU/wall receipts are one observation per unit/main/audit process and exclude startup before the measured interval, ownership gate, shell, authoring, physical acquisition and model costs. All those absent costs remain unknown, not0. No ratio, repeated timing or practical-scale throughput is inferred.")

#text("The original all-subset theorem is a logical consequence for a common finite family; W44 did not rerun all128 W41 subsets or its entire solver. W42 stop-only h0, shared child objects versus complete serialization length sumS, and original-policy audit complexity remain unresolved. Closed-bin behavior is retained; changing it can alter feasible worlds and invalidates a direct same-problem comparison.")

#text("The new edition itself executes only deterministic document construction, saved-data figure rendering and schema/hash/content checks. It runs no unit/main/oracle research stage, API/model/native episode, acquisition or worker. New physical evidence, independently separated groups, measured prices/availability/failure/delay, original AO* body/version and complete fair application controls remain the next acceptance requirements. Scientific_gate_closure=false; no skill activation, operational registration or publication is performed by the author.")

= #text("S20. Historical loss and oracle derivations restored from v24")

#text("For four prediction heads let e_ih be the binary head error, k_i=sum_h e_ih, component loss C=sum_i k_i/(4n), vector loss V=sum_i1[k_i>0]/n, worst-head loss W=max_h sum_i e_ih/n and pump loss P=sum_i e_i3/n. Pointwise k_i/4<=1[k_i>0]<=k_i gives C<=V<=min(1,4C). W maximizes after averaging each head and is not the average of a per-cycle maximum. Selection on a new loss reuses outcomes; it does not add independent evidence.")

#text("With legal mask set F_B, per-cycle declared error-plus-cost u_i(m), all-mask oracle a_i=min over F_B u_i(m), pair oracle b_i=min(u_i(m_L),u_i(m_R)), and actual gate g_i, feasibility gives a_i<=b_i<=g_i. Let F be fixed-policy mean, A mean all-mask oracle, P mean pair oracle and G actual gate mean. H=F-A>=0, E=P-A>=0, R=G-P>=0, so G-F=-(F-A)+(P-A)+(G-P)=-H+E+R. The pair need not contain the fixed policy; H remains nonnegative if the fixed mask is legal. E and R combine information, action-class, tie and fitting constraints, not separately identified causal mechanisms.")

#text("The historical primary counts give F=13561/25260,A=10201/25260,P=12391/25260,G=12413/25260 and G-F=(-3360+2190+22)/25260=-1148/25260. Relative to the stronger TS1 comparator, pair oracle already ties its objective and actual gate adds22 quote units on421 cycles. The secondary k3/lambda0 case gives924,625,789,861 component errors, hence-299+164+72=-63 out of1684 head-cycle decisions; vector failures rise381to391 while quotes fall842to518. Labels are used only by the retrospective diagnostic oracle. [C04,C36]")

= #text("S21. Tuple-copy obstruction and pointwise prediction dominance")

#text("Let T be training four-label tuples. A nonempty-mask one-nearest-neighbor that copies an entire training tuple can output only T. Every evaluation truth outside T is necessarily an exact-vector failure, hence successes<=number of evaluation truths in T. Here that number is30 of421;391 are outside T. Empty-mask componentwise modal fallback need not belong to T in general: training tuples(1,0,0,0),(0,1,0,0),(0,0,1,0) have modal composition(0,0,0,0) outside T. The historical actual fallback(3,100,0,90) was separately found in T. The conditional bound therefore covers this saved bank but not arbitrary compositional predictors. V15's unselected k3 output can compose new tuples and escapes, rather than refutes, the premise.")

#text("V24 directly compared the four-component prediction vectors for masks4 and5 over421 cycles, rather than inferring vector identity from matching error counts. They agree pointwise. For any common loss of(prediction,label,cycle), any normalized nonnegative cycle weights w_i, nonnegative source prices and lambda, and possibly randomized larger-mask probabilities q_i, risk difference is lambda*c_PS1/Z*sum_i w_i q_i>=0, Z=sum prices>0. Feasibility requires both masks affordable. This proves conditional non-improvement within the saved leaf pair; mask-dependent sensor harm, new models, people and physical costs are outside it.")

#text("The3510 dependent historical price/weight cells comprised2430 ties and1080 strictly extra-cost outcomes; the algebra supplies the general nonnegative statement, not grid density. The saved842 prediction rows and421 comparisons do not become842 independent cycles. The v24 synthetic40960 interface traces are separate from observed Hydraulic outcomes and from PAMAP2, which remained a plan. [C36]")

= #text("S22. Exact descriptive EDA protocol and limitations")

#text("EDA.json records each original W47 frozen NPZ path, SHA256, byte size and x/y/offset coordinates. Loading uses numpy allow_pickle=False. Assertions require x.shape=(n,69), integer label IDs1..12, finite admitted features, unique offsets and offsets divisible by128. No study module, pickle, saved unit/main/oracle or learned predictor is imported. The arrays are copied only in memory; none of the source files are changed.")

#text("Per participant we count label frequencies, missing/nonfinite feature values, zero-variance features and each group's value quantiles and feature-standard-deviation ranges. The class heatmap presents count denominators explicitly. The scale plot shows per-feature within-person standard deviation on a logarithmic axis in mixed native units, not an accuracy curve or a comparable physical sensor scale. No DEV normalization is fitted or substituted for frozen training mean/scale. Finite admitted summaries cannot reconstruct excluded null/mixed windows, dropped partial tails or raw-series missingness.")

#text("All16 policy J values are recalculated by exact Fraction arithmetic from saved per-participant error and quote counts and checked against stored floats to1e-14. This is a fresh documentary numeric check of existing results, not a new research run. Participant7/8 differences and support counts are descriptive. This edition did not acquire full raw datasets for Hydraulic/HAR/Gas, perform their missingness/feature EDA, infer unknown physical axes or recover unobserved acquisition failures. Those EDA gaps are explicit rather than filled with synthetic data.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 7. Descriptive verification of admitted feature arrays")]]
#v(3pt)
#strong[Require] #text("Frozen subject5/6/7/8NPZ,manifest/source hashes,training-only normalization metadata and saved integer policy summaries.")
#parbreak()
#strong[Ensure] #text("Per-person shape/finite/label/offset/class/feature-block statistics and exactly reconstructed saved macro scores; no fitted model or new predictions.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Verify immutable source paths and SHA256 against the manifest; load NPZ using allow_pickle=False.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Require x(n,69),aligned y/offset dimensions,finite admitted features,label1..12 and unique128-aligned offsets; failure aborts rather than repairing data.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Count each person's labels and summarize native-unit feature blocks; keep conditional-fit inputs and exposedDEV roles separate.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Use saved participant integer errors/quotes to calculate Fraction macroerror,macroquote and J with lambda1/20.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Assert agreement with stored scores,write EDA/source/figure records and preserve missing raw-series/physical-unit evidence as a gap.")]])
#v(1.2pt)
]

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Directly inspected feature-array roles and dimensions.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Participant")],[#text("Role")],[#text("Windows")],[#text("Features")],[#text("New independent person?")]),
[#text("5")],[#text("conditional fit audit")],[#text("264")],[#text("69")],[#text("No")],
[#text("6")],[#text("conditional fit audit")],[#text("250")],[#text("69")],[#text("No")],
[#text("7")],[#text("already exposed DEV")],[#text("266")],[#text("69")],[#text("No")],
[#text("8")],[#text("already exposed DEV")],[#text("258")],[#text("69")],[#text("No")])
]

#figure(image("figures/eda_feature_scale.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Per-person69-feature scale profile. Vertical dotted boundaries separate9/6/27/27 feature groups. The log axis uses heterogeneous native units and is only descriptive; no fitted model or attribution to sensor usefulness. Original NPZ hashes and block statistics are in EDA.json. [C34,F6]")])
= #text("S23. Reconstructing full-pool support study counts without replay")

#text("For participant7 candidate error64/266 and mean quotes383/266, and for8 error95/258 and quotes445/258. Average person errors first, average person quotes separately, then add1/20times the latter. The pooled error159/524 differs from the macro error0.3044092790114822; averaging all policy paths is not the participant-macro estimand. Guard-specific error change is-0.5*(16/266+0/258)=-0.03007518796992481; extra macro quotes0.5*(33/266+8/258)=0.07753395115696216, yielding objective change-0.026198490412076725.")

#text("For candidate against initial STOP,80 corrections minus39 harms gives41 fewer errors in pooled counts, a distinct comparison from16 guard-specific corrections. The41 guard-changed windows are selected by the rules' disagreement, not a random independent group. Each of the candidate's action3 support counts3and52 is preserved; total55 with two people passes the declared descriptive threshold but provides no calibrated confidence bound. A fitted leaf's30-window/two-participant admission is a separate upstream criterion.")

#text("Candidate/local_myopic, legacy blanket, four support-gated subsets and nine order/multiplier rules total16 arms. All use initial group0 and one additional quote. Four additional current subset masks are1,3,5,9; incompatible original full-budget subsets/orders remain unexecuted. Historical W46 subsets were unconditional, so their scores cannot be put on one unchanged-policy cross-wave curve with current support-gated subsets.")

#figure(image("figures/w47_support_harm.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Left: candidate branch counts split by participant (249action2,55action3); P7action3 has only3windows. Right:16corrections/25ties/0harms are restricted to41guard-changed windows, while39harms use the complete candidate-versus-initial-STOP set. Different comparison sets are explicit, so bars must not be summed. [C33,C34,F8]")])
= #text("S24. Cost scopes and the current selector proof in detail")

#text("The local rule's no-unsupported-purchase property follows directly from selecting a in S; its budget property follows from initial spent+remaining=2 and either STOP or one unit debit. Conditional fitted-value dominance over blanket follows by cases: if S=F choices coincide; if S is proper blanket value0 and local max(0,best supported value)>=0; if S empty both STOP. Estimated means may be wrong, and pointwise fitted-value dominance does not establish pointwise realized loss dominance. An independently sorted negative-net list over the same S with the same lower-index tie rule returns the identical action, proving the local myopic tie before looking at labels.")

#text("The broad saved word-operation account uses F encoded features,T trees,depth d,C prediction classes,K conditional actions,conditional depth h,conditional output classes D and P stored fitting-participant identifiers: O(F+T(d+C)+K(h+D+P)+KlogK+B_logging), with a second encoding/forest pass after purchase. B_logging includes control, hashing, serialization and journals and remains nonzero at STOP. Model/input storage and repeated serialized output must be distinguished; the historical audit has stronger hidden-array/label rights and separate caches. No asymptotic bit-arithmetic, complete RSS/transient, physical-I/O or deployment theorem is inferred.")

#text("W47 provider completions3403 and initial local copies8384 are repeated local operations. Stage CPU64.546875seconds and wall215.7763239000seconds include their declared wrapper body, not all import/startup, final EXIT or Orca launcher work. The4806 observed-zero row CPU readings remain observed quantization, not unknown or free work. The additional per-policy full shared charge20.4981172000/10.40625 and residual5.9793097021/3.078125 are accounting scenarios with no asserted amortization horizon. Full deployment, historical fitting and physical sensor cost remain null. [C32,C33,C35]")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 8. One-remaining-quote action-local admission")]]
#v(3pt)
#strong[Require] #text("Frozen73-input RF and fold0 conditional trees; public acquired group0 values/mask1; spent1,remaining1,total2,empty cache. Feasible actions1,2,3; per-action fitting leaf counts/participants; quote1,lambda0.05; lower-index tie rule.")
#parbreak()
#strong[Ensure] #text("STOP with empty-support/nonpositive reason, or one supported extra action and a final frozen prediction; complete cost/intent/trace records.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Validate model/input hashes, public mask, dimensions and budget; mismatch fails without a new inference attempt.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Encode only acquired group0 and observation bits; compute the frozen initial prediction.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Look up each feasible action's conditional leaf using public state, retaining its fitting window/participant support and mean.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Build S using each action's own30-window/two-participant predicate; do not veto one supported action because a different action is unsupported.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("If S is empty, STOP insufficient_support. Otherwise select maximum mean minus0.05 with smallest action-index tie; if value<=0 STOP nonpositive.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Before a positive purchase, validate remaining quote/control/time, write intent, copy only the selected local group, debit quote and compute final prediction.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Write and flush the trace, check finalization barrier and preserve all failures/unknown states; do not retry an interrupted accepted path.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compute label-based scores only in the evaluator after selection. Keep full-bank/raw-label audit rights separate and retain myopic equality and stronger static controls.")]])
#v(1.2pt)
]

= #text("S25. terminal semantics and support studies lineage and the six current review areas")

#text("W43 has no ProbeFlow RESULT at the discovered per-project path; its checkpoint reports routing/startup work and does not create a new ProbeFlow result. W44 supplies static terminal semantics and the deadline witness, while its damaged fourteen-field review/source-copy intake hold is preserved. W45 supplies new fitting artifacts plus a failed instrumented main. W46 supplies a completed bounded timing/replay-free local study with insufficient_support. W47 supplies a completed larger exposed-DEV comparison with a narrower local-support implementation result and retained no_gain/static regression. These statuses have different scientific and operational meanings.")

#text("The canonical W47 METHOD and its validated binding, independent_review and completed reviewer Task proof are source-hashed. Algorithm/architecture exists means bounded inspected procedures/components exist; complexity/evaluation/baselines/related_work partial keeps the full-cost, independent-sample, exact-reference/full-budget and primary-version gaps. Earlier W42 and damaged W44 reviews remain dated artifacts, not silently superseded scientific approvals. This documentary author's source hash/EDA/schema checks do not substitute for the separate new manuscript pedagogical/scientific review or whole-PDF visual inspection.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Current full-pool support study independent METHOD statuses; document completeness does not imply scientific certification.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Area")],[#text("Status")],[#text("Remaining boundary")]),
[#text("algorithm")],[#text("exists")],[#text("Bounded inspected procedure exists; no population/security certification.")],
[#text("architecture")],[#text("exists")],[#text("Bounded inspected procedure exists; no population/security certification.")],
[#text("complexity")],[#text("partial")],[#text("Complete preparation/fitting/deployment lifetime and transient-memory/physical acquisition cost remain unknown: EXIT and launcher tails, mixed residual, historical fitting horizon, authoring/reporting and physical I/O are not fully observed. One measured cooperative clock pass is not a hard deadline or general scaling guarantee.")],
[#text("evaluation")],[#text("partial")],[#text("Untouched independent groups/families, valid paired group or rare-event uncertainty and complete-cost utility evidence are absent. No real provider/crash failure was injected. Enlarging an already exposed pool does not repair W46 insufficient_support or W45 failed/unstarted/heldout0.")],
[#text("baselines")],[#text("partial")],[#text("This finite fixed-prefix catalogue is not the original full-budget application comparison; closest reference-paper version/code and matched exact external reproduction are missing. Exposed-pool best ranking and the legacy ablation do not establish confirmatory superiority. Current support-gated subsets differ from W46 unconditional controls.")],
[#text("related_work")],[#text("partial")],[#text("Closest-method primary body/version/code and AO*2002/2004 identity/guarantee comparison remain not_reproduced; inherited metadata does not close the preserved W44 fourteen-field/source-copy hold or establish novelty.")])
]

= #text("S26. Complete current policy table and descriptive estimands")

#text("The following table retains every current compatible policy rather than reporting only favorable contrasts. Error and quotes are each equally weighted participant means over P7n266/P8n258; J adds0.05times quotes. All rows describe the same524 exposed windows. This is a retrospective descriptive ordering, not independent model selection, an uncertainty estimate or a new performance experiment. The corresponding exact rational forms and per-person integer numerators are retained in EDA.json.")

#text("Support-gated subsets have no positive-net requirement; orders apply their named0.5/1/2cost multiplier to the conditional positive-value test. Their terminal quote is nevertheless scored with the common0.05objective. Identical score rows may have different scoped runtime; observed CPU0 is quantization. Thirty-four incompatible full-budget catalogue policies are unexecuted rather than scored0. Current support-gated subsets differ from W46 unconditional subsets, so the two tables do not define a like-for-like cross-wave treatment contrast.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("All16 full-pool support study policy scores, descriptively recalculated from saved per-person integers.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Policy")],[#text("Macro error")],[#text("Macro quotes")],[#text("Macro J")]),
[#text("candidate")],[#text("0.304409279")],[#text("1.582327913")],[#text("0.383525675")],
[#text("local_myopic")],[#text("0.304409279")],[#text("1.582327913")],[#text("0.383525675")],
[#text("legacy_blanket")],[#text("0.334484467")],[#text("1.504793962")],[#text("0.409724165")],
[#text("subset_1")],[#text("0.381884945")],[#text("1.000000000")],[#text("0.431884945")],
[#text("subset_3")],[#text("0.375954421")],[#text("1.918706650")],[#text("0.471889753")],
[#text("subset_5")],[#text("0.155169901")],[#text("1.918998077")],[#text("0.251119805")],
[#text("subset_9")],[#text("0.224704202")],[#text("2.000000000")],[#text("0.324704202")],
[#text("order_0_1_m0.5")],[#text("0.381884945")],[#text("1.000000000")],[#text("0.431884945")],
[#text("order_0_1_m1")],[#text("0.381884945")],[#text("1.000000000")],[#text("0.431884945")],
[#text("order_0_1_m2")],[#text("0.381884945")],[#text("1.000000000")],[#text("0.431884945")],
[#text("order_0_2_m0.5")],[#text("0.265649589")],[#text("1.533936586")],[#text("0.342346418")],
[#text("order_0_2_m1")],[#text("0.265649589")],[#text("1.533936586")],[#text("0.342346418")],
[#text("order_0_2_m2")],[#text("0.302471295")],[#text("1.375473568")],[#text("0.371244973")],
[#text("order_0_3_m0.5")],[#text("0.378650114")],[#text("1.347875503")],[#text("0.446043889")],
[#text("order_0_3_m1")],[#text("0.399326805")],[#text("1.106414292")],[#text("0.454647520")],
[#text("order_0_3_m2")],[#text("0.399326805")],[#text("1.106414292")],[#text("0.454647520")])
]

= #text("S27. Abstract")

#text("ProbeFlow studies when buying more information improves a frozen prediction system, and when the available evidence can support that conclusion. This cumulative edition connects the original shared-source acquisition design, exposed Hydraulic development studies, participant-separated HAR and MHEALTH controls, and the exact robust information-design program through research wave 42. These are different studies with different estimands; they are connected by their information, objective and accounting contracts, rather than pooled as one performance benchmark.")

#text("The controlled MHEALTH study evaluated 527 windows from two participants after a joint policy release. Conditional routing tied its strongest development-selected myopic baseline exactly, used only one second-group type, and failed its branch-support gate. Later waves quantified the resulting missing-fallback and availability uncertainty, constructed an exact pre-observation minimax subset selector, and proved safe strict pruning, shared-error-cap envelopes and an implicit marginal heap. Exactness preserved all primary ties; it did not establish application benefit. Reduced endpoint counts sometimes accompanied greater CPU, storage and output costs. Wave 42 separated sequential expected prediction loss from fixed-subset worst interval width with a conditional translation and two finite witnesses. Independent physical cost, new participant utility, original-method version identity, canonical ordered-trace correspondence and parts of the general complexity accounting remain unresolved. This edition performs documentary synthesis only.")

#text("This complete edition incorporates the W44 terminal-permutation result into those same contracts. A bijection between ID-indexed terminal readings preserves the feasible worlds, endpoints, additive price and complete worst ties under static, always-available reveals. It preserves neither literal action order nor solver prefix diagnostics. One stored W41 subset has worst width 3/5 and price 2 in both orders (no_gain); a separate two-item deadline construction completes 0/4 versus 4/4 schedules under the same changed conditions. Eight static encodings and eight deadline rows, plus rechecks, are not independent experiments. The W42 review statements below are dated evidence; the new terminal theorem narrows one semantic question without closing the original intake hold, general correspondence, complexity or application-evidence gaps. [C23-C28]")

#text("The W45-W47 return to a frozen mask-aware predictor is integrated without replacing the earlier identification and exact-solver results. W45's timed main failed after8 completed paths out of4152 planned; W46 completed1800 paths on120 exposed DEV windows but failed its two-action support gate. W47 completed8384 paths for16 policies on524 exposed windows from two people. Action-local support admission restored41 purchases relative to a same-run blanket guard, correcting16 errors with25 error ties and no guard-subset harms. The candidate nevertheless equals local myopic on every window, harms39 initially correct windows overall, and has higher declared objective than strong support-gated fixed subset/order controls. These are development diagnostics, not independent confirmation, a nonmyopic advance or a general safety result. New descriptive EDA inspects frozen feature arrays only; no study/model replay, fit or inference is performed. [C30-C35]")

= #text("S28. Acquisition motivation and the cumulative question")

#text("The original acquisition question is practical: a source may support several analyses, while its physical acquisition, internal computation and public disclosure occur at different times. Before adding a deeper planner, ProbeFlow asks whether the fixed predictor can use the permitted evidence, whether the chosen loss represents the intended decision, and whether a strong affordable baseline already produces the same result. The cumulative contribution is an auditable sequence of answers and failures to these questions, rather than an assertion that a more elaborate policy must be better.")

#text("The earliest archived v5 manuscript separates disclosed values z and mask m from acquired sources O, computed modules C, availability v, remaining budget b and required public failure history. A hidden cached prerequisite can reduce a later charge without authorizing its disclosure. Conversely, revealing one statistic need not reveal every statistic computed from the same raw trace. The state (z,m,O,C,v,b) is sufficient only under a history-consistent observation and transition model; it is not a universal Markov-state theorem. [C01]")

#text("This account therefore has three linked questions. First, do completed offline controlled observations demonstrate useful conditional acquisition? Second, what can be identified when required counterfactual outcomes are missing? Third, how can an exact solver choose a fixed information subset before its readings, without importing unavailable outcome information? The last question is a theory problem motivated by the earlier failures. Its solution does not retrospectively make those empirical failures successes.")

#text("The result is organized around one continuous chain: acquire only permitted information; preserve negative controls and unobserved counterfactuals; optimize a precisely declared uncertainty objective; and distinguish a terminal information set from a history of actions. The latest theorem addresses the last distinction. It is part of the same information contract, rather than an appended claim of empirical progress.")

= #text("S29. Objectives, information rights and comparable policies")

#text("An acquisition quote, a prediction error, an interval width and a physical resource bill are separate quantities. Shared-source accounting charges a raw acquisition once while keeping computation and disclosure rights explicit; the later minimax studies instead price guaranteed availability queries. Neither ledger measures sensor energy, clinical benefit, money or actual communication delay. A cheaper logical transcript is evidence about its declared accounting contract, and requires an additional physical measurement contract before it can support a deployment saving.")

#text("For an offline episode let pi use only the purchased public features and a frozen predictor f. A common secondary objective is J=mean(error)+lambda*mean(quotes), with the same lambda, price units, hard attempt cap and STOP privilege for every competing policy. Participant-macro objectives average each participant mean equally; pooled window objectives weight people by their number of retained windows. Their rankings need not agree. Training, calibration, selection, prediction inference, acquisition, audit and authoring costs also have different scopes. [C02,C07]")

#text("For the later robust problem, S is fixed before seeing query readings. Each feasible complete reading z induces a sharp interval [L(S,z),U(S,z)] for the route-minus-static macro loss difference Delta. Its risk is R(S)=max_z(U-L). Under query budget Q select lexicographically (R(S),sum prices,numeric mask), while separately returning every affordable subset tied in primary risk. A costlier primary tie remains part of the output even when the canonical answer is cheaper. There is no learned prior over these readings and no observation-dependent subset change. [C08]")

#text("A comparison supports an algorithmic advantage only when predictor rights, information, feasible policies, loss, aggregation, price and budget match. An exact same-information oracle must tie a correct exact selector. Pooling, an inaccessible outcome oracle, a different loss or an intentionally different policy class can diagnose a boundary, but cannot be relabeled an inferior implementation of the same task.")

#text("For order comparisons the public record is (S,z), where z maps immutable item IDs to labels. A positional tuple additionally depends on an order pi. The observation relation must stay the same when tuple positions change. Reindexing a tuple is permitted; replacing a chronological acquisition contract by a set of observations is a change of problem unless the static assumptions are established. [C23,C24]")

#fit-equation[$ J(pi) = E[ell(f(x_(O_pi)), y)] + lambda E[C_pi] $]
#text("Prediction-loss objective. The prior, predictor, permitted public information, cost scope and hard budget must be common before algorithms are compared.")

#fit-equation[$ R(S) = max_z (U(S,z) - L(S,z)) $]
#text("Fixed pre-observation subset risk; z ranges over feasible complete readings. This is a worst identified-width objective, not expected prediction error.")

#fit-equation[$ C(S) = sum_(i in S) c_i <= Q $]
#text("The later information-design problem uses additive logical query prices and a hard budget; complete primary-risk ties are returned separately from lexicographic price selection.")

= #text("S30. Related work and the precise comparison boundary")

#text("Joint acquisition/classification with variable-size set encoding [shim2018] motivates representing the acquired information without granting unpurchased features to a policy. Generative-surrogate active feature acquisition [li2021,gsmrl-local-primary] supplies a sequential action/STOP/prediction formulation. ProbeFlow's current exact selector instead commits to a subset before readings and optimizes worst conditional uncertainty. These methods are related by an information-acquisition question, not by an established equivalence of losses, learned policies or implementations.")

#text("The cached GSMRL source expressly retains action chronology in time-series and real-world masking. A set-valued acquired-state notation alone does not remove schedule constraints. W44 read four saved intervals totaling 7,879 bytes concerning acquired sets, STOP, the terminal predictor and chronology. This is bounded local reading of an unversioned cache, not a fresh primary-paper reproduction. The missing declared W44 full-copy path and the actual preserved source hash are documented in the supplement. [C27]")

#text("Adaptive submodularity [adaptive-submodularity] gives guarantees under its own structural assumptions; the saved ProbeFlow complementarity witness violates diminishing returns for the present worst-width gain. Cawley and Talbot [cawley2010] motivate treating repeated model/policy selection as part of evaluation. Original AO* identity and guarantees remain an inherited unresolved primary-source comparison [inherited-author-index]. We claim no new external benchmark advantage, generic GSMRL/AO* equivalence or externally established novelty.")

#text("The separate bibliography verifier for this edition checked official metadata and selected current primary passages: Shim et al., NeurIPS31 (2018),1368-1378; Li and Oliva, PMLR139 (2021),6450-6459; Cawley and Talbot, JMLR11(70) (2010),2079-2107; and MHEALTH's UCI dataset citation (2014), DOI10.24432/C5TW22. A newly readable official GSMRL v2 page is a separate source from the old unversioned cache. The official AO* author index gives2002 while GSMRL v2 cites2004; original-body/pagination identity remains unresolved. The official adaptive-submodularity v5 comment reports a correction to Theorem13 with additional conditions; neither its revised proof nor a guarantee transfer is claimed. REFERENCES.json records exact reading and access limits.")

= #text("S31. Evidence lineage and units of inference")

#text("The historical evaluation lineage remains exposed. The Hydraulic studies repeatedly reused one rig and 421 evaluation cycles after earlier inspection; neither a chronological gap nor a newly frozen selection file creates an independent final sample. The later MHEALTH release recorded a local access boundary for two previously unparsed target participants, but its 527 windows and subsequent wave analyses still share those people and observations. More masks, predictions, scenarios or publication waves increase calculation records, rather than independent participants.")

#text("The preserved library begins with the v5 four-page source, followed by the v12 extended manuscript and v13 conference restructuring. V14 audited objective choice and a tuple-copy output ceiling; v15 broadened the output class; v16 jointly selected predictor and mask; v17 learned small gates; v18 and v19 retained the exposed-data setting while adding diagnostics. V19.1 changed reading diagrams, v20 separated main and supplement, v21 strengthened dominance checks, v21.1 repaired display encoding, and v22-v24 refreshed the argument. These publication version numbers are not autonomy wave numbers. [C01-C04]")

#text("The registered HAR, Gas and MHEALTH studies form the immediate empirical lineage of the autonomy campaign. The W1-W42 receipt inventory records accepted bounded results, an accepted failed result, operationally blocked starts and unattempted project slots separately. Carrying an earlier paper through another wave does not mean ProbeFlow executed in that wave. Accepted intake is a provenance/lifecycle fact, not scientific approval. The supplement and timeline preserve every wave status without replacing scientific history with operational incidents.")

#text("W44 adds two semantic witnesses, not two application datasets: the static witness reuses mask 5 of one previously stored seven-coordinate W41 environment, and the deadline witness uses two acquired IDs in four constructed bit worlds. The original eight static rows encode four distinct conjunctions twice; the eight deadline rows apply two schedules to the same four worlds. The author's sixteen raw-only checks and a separate coordinator arithmetic review reuse these observations. No row, recheck, saved policy or new document version adds an independent participant. [C25,C26]")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Evidence units are study-specific and must never be pooled into one performance denominator.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Lineage")],[#text("Observed / constructed unit")],[#text("Retained negative or limit")]),
[#text("Hydraulic v12-v24")],[#text("One rig; 421 exposed evaluation cycles")],[#text("No independent final; repeated selections and diagnostics")],
[#text("HAR")],[#text("9 target participants; 2,947 dependent windows")],[#text("No development-feasible primary policy")],
[#text("Gas")],[#text("Batches 8-10; 4,364 measurements")],[#text("Route/myopic tie; second-action count 0")],
[#text("MHEALTH")],[#text("2 target participants; 527 windows")],[#text("Route/myopic tie; branch-support gate failed")],
[#text("W15-W41 solvers")],[#text("Authored finite world/constraint fixtures")],[#text("Exact implementation checks; no physical acquisition")],
[#text("W42")],[#text("2 finite witnesses; 51 world calculations")],[#text("Different objectives and policy classes")],
[#text("W44 static")],[#text("1 stored subset; 4 conjunctions encoded in 8 rows")],[#text("Worst width and price no_gain")],
[#text("W44 deadline")],[#text("4 constructed worlds under 2 schedules")],[#text("Assumption-violation counterexample; no superiority claim")])
]

= #text("S32. What the Hydraulic lineage established and failed to establish")

#text("The three-channel Hydraulic replay first exposed a support failure: restoring marginal training labels did not restore useful selective coverage, and 391 of the 421 evaluation joint conditions were absent from the training prefix. In v12, removing a centroid prior offset reduced full-source component error from 0.723872 to 0.473872, with the entire 0.25 change confined to the cooler head. The selection-chosen nearest neighbor tied that full-source score. Under raw-sample prices TS1 matched full-source error at quote 60 rather than 6660; under equal source prices the selection-locked choice lost to a simple source/order control. These are exposed within-program observations. [C02]")

#text("The tuple-copy premise gave the v14 ceiling of 30/421 complete-vector successes. V15 permitted class-balanced per-head neighbor voting at k in {1,3,5,11,31}; it generated 25,000 prediction records and matched all 5,000 prior k=1 records. Selection still chose k=1, preserving all nine price-budget choices. An unselected k=3/mask3 diagnostic composed ten train-unseen tuples and reached 40/421 complete successes. This escapes the copying premise rather than refuting its conditional ceiling or validating the unselected model. [C03]")

#text("V16 joint predictor-mask selection changed three equal-price decisions but the strong TS1/k1 control still had one fewer component error. V17 fitted 390 gates on 102 policy-fit cycles, selected on another 102 cycles and evaluated 90 dependent settings on the same 421 exposed cycles. Its primary selector retained fixed PS1; a forced TS1-first gate matched TS1 component error while spending 22 extra quotes. Six k3-gate selections included four component improvements and two regressions, and all policy-fit targets shared one joint condition. V19-v24 then narrowed the conditional obstruction: the primary two leaves ultimately had identical four-head predictions on all 421 cycles, so any common prediction-label loss agrees and extra acquisition only adds nonnegative price. A secondary gate saved 63 component errors and 324 quotes while adding ten vector failures. No single aggregate turns that tradeoff into general utility. [C04]")

= #text("S33. Controlled HAR, Gas and MHEALTH observations")

#text("The HAR study fit on 14 participants and 4,996 windows, selected on seven participants and 2,356 windows, and evaluated the official nine-participant, 2,947-window test split. No candidate met the primary development error threshold 0.10, so the primary selected policy was null. A secondary cap-two gate reduced macro error by about 0.514 percentage points relative to strong fixed A while increasing mean quote from 1 to about 1.08127; its paths matched the same-STOP fixed order, three participants had worse error and four had worse secondary objective. The now-exposed test cannot become a new independent final for later edits. [C05]")

#text("The next Gas study opened batches 8-10 once under its joint release: 4,364 measurements, 3,277 errors and 4,364 quotes gave exact J=4369/5455. Routing and the strongest myopic policy both bought G4 and immediately stopped on every measurement. Their contrast was zero and the second-action denominator was zero. Naming a controller adaptive did not create adaptive behavior. [C06]")

#text("The same frozen predictor and the same development opportunities belong to the simple baselines as well as the proposed controller. MHEALTH routing, myopic acquisition and an ordered prefix executed identical target actions, and all 129 routing second decisions used the sparse-state unconditional fallback. The route-minus-strongest-baseline participant-macro contrast was exactly zero. Retaining the fixed G3+G4 policy with zero target errors at a higher logical quote exposes an objective tradeoff; it does not permit replacing the preselected primary comparator after release.")

#text("MHEALTH used subjects 1-3 for fifteen RF mask fits, subject 4 for temperature selection, 5-6 for action gains, 7-8 for policy selection and 9-10 for evaluation. The four positional groups were chest acceleration, ECG, ankle and wrist/lower arm, not four independent devices. The group definition avoided inferring the unresolved physical identity of duplicated/missing README axis entries. The 128-row nonoverlapping admission rule yielded 267 and 260 target windows. A sole frozen bank was shared with ChronoSense, making those projects dependent analyses of the same data. [C07]")

#text("The selected development policy had all 252 second decisions in G4; the target route likewise used G4 in all 129 second decisions, with 398 G3-to-STOP windows. The joint release explicitly permitted descriptive evaluation after the development support failure; it did not waive the adaptation-claim gate. Participant 9 supplied all 22 routing errors, all class 2 after STOP; participant 10 supplied none. Full-access RF had zero errors across 527 windows, while the full-access centroid had 34/267 and 22/260 errors. Those full-access diagnostics lie outside the cap-two policy contest and demonstrate neither conditional-routing gain nor clinical validity. The original outcome remains insufficient_support. [C07]")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("MHEALTH target observations; rows reuse two people, not independent replications.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Participant")],[#text("Windows")],[#text("Route errors")],[#text("Route attempts")],[#text("Route J")],[#text("Fixed G3+G4 J")],[#text("Route minus strongest")]),
[#text("9")],[#text("267")],[#text("22")],[#text("317")],[#text("757/5340")],[#text("1/10")],[#text("0")],
[#text("10")],[#text("260")],[#text("0")],[#text("339")],[#text("339/5200")],[#text("1/10")],[#text("0")])
]

#figure(image("figures/mhealth_objective.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("MHEALTH exact participant J values from the saved per-arm ledger. Routing and its selected myopic comparator coincide; fixed G3+G4 is an additional tradeoff diagnostic. The two groups of bars reuse the same two participants (267/260 windows); no inferential error bars or independent-repeat claim. [C07,F1]")])
= #text("S34. Missing counterfactuals led to partial identification")

#text("The stored MHEALTH traces contain no observed acquisition failure or late attempt. They also omit G3-only fallback predictions for the 129 windows on which the route requested G4, and do not identify the ranking of all eleven feasible subsets. W2 therefore computed eighteen conditional failure/penalty scenarios, preserving the strongest-myopic zero contrast. Its conditional break-even failure rate 9653/114400 at zero penalty relies on its loss-independence model; it is not an observed failure rate. [C09]")

#text("W5 removed that independence restriction. Across 36 coupling conditions it retained six universal static wins, nineteen nonidentified strict rankings and eleven universal route wins; its 72 endpoint witnesses were constructed, not observed failed acquisitions. W6 separated policy availability and shared versus separate fallbacks: 72 conditions split into 24 route wins, 24 static wins and 24 cases allowing both strict rankings. Equal average success is insufficient when window placement or fallback coupling differs. [C10]")

#text("W7 bounded unknown fallback errors rather than filling them with favorable predictions. Of 2,340 upper-count and 2,340 exact-count cells, 1,806 and 1,810 contracted; 534 and 530 did not. Exact counts created no additional strict-sign identifications in that grid. Even zero unknown errors left a zero-penalty half-success condition nonidentified. W8 then studied hypothetical availability intervals at known stop-error windows: 264 of 322 cells contracted, 58 did not, and all 92 placement negative controls had no gain. These are assumption-sensitive information results with zero new availability observations. [C11]")

#text("W10 preserved its first 41,860-cell raw calculation but was correctly marked failed: a temporary-path test unintentionally invoked the substantive main again, violating the single-main contract, and the second temporary raw was automatically removed. W11 did not erase that failure; a new bounded study calculated 29,120 cells, with 14,892 contractions and 14,228 ties against count-only information. W12 demonstrated that a parent simplified formula was nonsharp outside its slack regime in 4,913 of 6,548 constructed cells. The corrected joint optimization preserved infeasible scenarios and differences between exact counts and caps. [C12]")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Retained partial-identification outcomes; scenario cells are constructed calculations over inherited observations.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Wave")],[#text("Calculation denominator")],[#text("Negative / uncertainty preserved")]),
[#text("W2")],[#text("18 failure/penalty scenarios")],[#text("129 missing G3 fallback outputs; no observed failure rate")],
[#text("W5")],[#text("36 coupling conditions")],[#text("19 nonidentified strict rankings")],
[#text("W6")],[#text("72 conditions")],[#text("24 allow both strict rankings")],
[#text("W7")],[#text("2,340 upper-count + 2,340 exact-count cells")],[#text("534/530 no_gain; no extra exact-count sign identifications")],
[#text("W8")],[#text("322 cells + 92 placement controls")],[#text("58 no_gain; all 92 controls tie")],
[#text("W10")],[#text("First 41,860-cell raw retained")],[#text("FAILED: unintended main replay; temporary second raw lost")],
[#text("W11")],[#text("29,120 cells")],[#text("14,228 ties; parent failure stays recorded")],
[#text("W12")],[#text("6,548 constructed cells")],[#text("Parent shortcut nonsharp in 4,913")],
[#text("W14")],[#text("3,636 cells")],[#text("974 no_gain; 672 infeasible; replicated-cap nonsharp 912")])
]

= #text("S35. From identified intervals to a fixed minimax information design")

#text("W14 replaced a homogeneous-window shortcut with nonuniform window boxes, unequal participant sizes and a single shared cap B on unknown requested errors. It computed 3,636 cells; macro and pooled endpoints differed in 3,506, and copying the full cap to every participant was nonsharp in 912. Informative cells still included 974 no-gain outcomes, and 672 scenarios were infeasible. W15 made the query subset a decision variable fixed before readings, evaluating eight constructed designs, 368 subsets, 3,726 transcripts and 73 budget decisions. Information improved the specified worst width in 44 decisions and tied in 29; these are design choices, not new participants. [C13,C14]")

#text("In the current declared world model, participant j has n_j windows, requested set A_j, known stop-error set E_j and other stops O_j. Requested binary errors u share sum(u)<=B; u=1 on E and zero on O. Route availability r and static availability v are independent within-participant box/mean polytopes, each with sum n_j/2. For request indicator A, c=1/20 and k>=0, route loss is (1-A*r)u+c(1+A)+kA(1-r), static loss is (1-v)u+2c+k(1-v). Delta averages the per-participant differences. Querying coordinate i returns a guaranteed closed bin [0,t_i] or [t_i,1] for v_i. The bins overlap at t_i and the implementation preserves that semantics. [C08,C13]")

#text("The endpoint oracle minimizes and maximizes Delta over compatible original worlds. At fixed requested errors, each availability term is linear on a box intersected with one sum constraint: fill lower bounds, then allocate remaining mass in coefficient order. Enumerating local binary placements and convolving exact error counts across participants preserves one global cap. Independence of the declared participant/policy availability sets permits concatenating optimizers and hence sharp endpoints; it is a model assumption, not a discovery about real failures.")

#text("A change in a fixed program can explain a change in that program without identifying a physical mechanism or a population effect. The Hydraulic scoring-offset contrast, the MHEALTH RF-versus-centroid diagnostic and the finite availability models answer different controlled questions. None identifies the causal effect of purchasing a real sensor reading, corrects unknown physical metadata, or supplies the independent clinical or industrial utility evidence that the original acquisition motivation still requires.")

= #text("S36. Integrated procedure and module boundaries")

#text("The observation-dependent part must be stated precisely. An acquisition policy may react to revealed feature values, whereas the minimax query selector commits to its entire subset before any bin reading. Its internal enumeration of hidden losses supplies an adversarial bound, never information disclosed to the policy. Wave 42 deliberately compares these policy classes and shows that adaptive early stopping can change expected paid price even when final error, worst price and worst conditional width remain tied.")

#text("The integrated scientific procedure has an empirical observation layer and a robust-design layer. The empirical layer freezes predictor/development access and evaluates observable paths and failures. The robust layer consumes only a validated public model of the unresolved quantities; it does not read an unobserved fallback prediction as though it had been measured. The sharp endpoint routine, prefix traversal, optional envelope allocator and budget selector have distinct contracts. Saved raw records support a separately written original-loss arithmetic audit. [C08,C15-C18]")

#text("Operationally the preserved studies use source/contract seals, exact owned output directories, single-attempt stage records and explicit failed, unknown, impossible and unstarted states. A source mismatch, malformed public field, infeasible box, resource breach or ambiguous call is retained, rather than silently repaired or retried. Those local guards are cooperative code boundaries; timeout and path checks are not OS security isolation, external preregistration or scientific certification.")

#text("The terminal-permutation adapter is a representation boundary between an ordered tuple and an ID-keyed reading, not a new acquisition planner. It validates identical unique-ID subsets, reindexes every full label, preserves impossible/feasible status and all ties, and leaves the original action and solver diagnostic records untouched. In deadline or history-dependent settings it returns a failed static-assumption comparison instead of applying the quotient. [C23-C26]")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 9. Integrated ProbeFlow procedure: freeze, observe, identify and design")]]
#v(3pt)
#strong[Require] #text("Frozen predictor and explicit public acquisition/STOP/cost contract; training, development and evaluation access ledger. For robust design only: participant partitions, guaranteed availability bins, shared binary-error cap, prices, budget and exact endpoint specification.")
#parbreak()
#strong[Ensure] #text("Observable policy contrasts and their support/failure denominators; or stated insufficient_support/no_gain. Under the declared world model: exact fixed-subset risks, all worst transcript ties, canonical affordable choice and all affordable primary-risk ties.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Freeze predictor, observation rights, loss, aggregation, prices, candidate selection and source versions before the relevant evaluation release.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Run only authorized empirical acquisition stages; retain attempts, STOP paths, missing counterfactuals, participant errors and cost scope. A zero branch denominator cannot demonstrate routing gain.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Represent unresolved requested losses and availability as explicit compatible worlds; reject hidden outcome inputs and unverified guaranteed-bin claims.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("For each precommitted query subset traverse feasible bin transcripts, using exact sharp endpoints at leaves and safe outward prefix envelopes only for the inner width maximum.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("For the shared envelope use exact local-cap allocation by DP or the proved implicit marginal heap. Preserve the separate sharp endpoint routine and per-solver cold-cache rights.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Prune only if a prefix upper width is strictly below an already completed leaf incumbent. Expand equality and keep every worst transcript tie.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("If comparing static orders, validate the common item-ID set and observation relation, then reindex terminal tuples by ID before comparing endpoints/full ties. Keep action order and solver diagnostics as separate outputs; do not apply this step across schedule-dependent feasibility.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Apply each hard query budget to the completed risk table; minimize (risk,price,mask) and separately return every affordable primary-risk tie.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.0em))[#text("Audit original-world arithmetic and full output partitions from saved records, retain failed/no_gain/cost-regression results, and state the scope still requiring independent application evidence.")]])
#v(1.2pt)
]

= #text("S37. Exactness, safe pruning and why greedy transfer fails")

#text("The worst-width information objective does not inherit a greedy approximation guarantee merely because its subject is information acquisition. The preserved complementarity witness has R(4)=R(5)=R(6)=3/8 and R(7)=1/4, so the same added item has marginal gain zero at one subset and 1/8 at a larger subset. A stale zero marginal is therefore not a certified future upper bound. Safe pruning instead follows containment of compatible worlds and preserves equality branches when all worst transcripts are required.")

#text("For prefix h and completion z, compatible worlds satisfy Omega_z subset Omega_h. Thus L(h)<=L(z)<=U(z)<=U(h), so prefix width is an upper bound for every descendant width. The largest completed feasible leaf width b is a lower bound on R(S). Cutting only U(h)-L(h)<b preserves the maximum and every maximizing complete label. Equality pruning can lose ties even when the numeric optimum is unchanged. This is an inner maximization certificate, not a lower bound that can discard a subset from the outer minimization. [C15,C16]")

#text("W18 verified the complementarity and heuristic boundary on three synthetic cases: 84 subsets and 819 readings, of which 730 were feasible and 89 impossible. A cost-ratio heuristic incurred regret 1/60 on a declared budget trap. W19 preserved 108 subset risks, five budget choices and all worst labels after strict pruning, but fewer feasible leaves (837 to 642) required more endpoint calls (837 to 1370) and more raw node bytes (183,934 to 287,257). A correct bound alone was not a compute saving. [C15,C16]")

#text("W21 derived a cheaper outward local envelope, exact at B=0. Endpoint calls fell from 785 to 741 across its four conditions, but two conditions had no endpoint gain and total nodes, CPU and retained output regressed. W22 then made the objective/backup distinction explicit: expected-cost AND/OR search, worst-transcript width search, upper/lower certificates and primary-tie contracts must agree before a solver correspondence is claimed. Its two conditions tied endpoint counts at 17 while prefix nodes rose from 18 to 28. [C17,C18]")

= #text("S38. Shared-cap dynamic programming and the implicit heap")

#text("For each participant the local outward envelope yields a base interval and one correction curve per sign f_j(b)=w_j min(b,c_j), where w_j=1/(P*n_j), 0<=b<=a_j, c_minus=a_j-l_A and c_plus=h_A. W39 combines these curves with sum b_j<=B by exact dynamic programming, tightening the cap-relaxed envelope. It still relaxes local coupling, so its interval is generally not the sharp endpoint interval. The established containment is L_relaxed<=L_shared<=L_sharp<=U_sharp<=U_shared<=U_relaxed. At B=0 the corrections vanish and the base is attainable under the declared independent model. [C19]")

#text("W41 observes nonnegative nonincreasing marginal chains delta_j(t)=w_j min(1,max(0,c_j-(t-1))). For each sign, initialize the first positive marginal from each chain in a heap, repeatedly pop the greatest and advance only that chain, stopping after B pops or no positive gain. The selected positive marginals form prefixes and attain the sum of the globally greatest available gains. Any feasible at-most-B allocation chooses chain prefixes and cannot exceed that sum. Therefore heap and DP scalar corrections agree exactly; allocation tie choices do not replace the required transcript/subset ties. This restates the saved theorem, rather than adding a new empirical result. [C20]")

#text("W39 used one heterogeneous two-participant, five-coordinate structure and two cap conditions: 64 risks, 486 complete labels and 20 budget decisions. At B=1 the shared bound reduced endpoint calls from cap-relaxed 208 to 201, with the same 480 linear calls and the same single-observation CPU, while strong sharp-prefix caching needed only 121 endpoints. W41 used one three-participant, seven-coordinate structure: 256 risks, 4,374 complete labels and 26 budget decisions across two cap conditions. The ten solver-condition records were complete, but B=2 all thirteen budgets tied the empty subset in risk. These quantities are constructed verification denominators. [C19,C20]")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("shared-marginal heap study B=2: one instrumented observation, identical risks and complete ties.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Solver")],[#text("CPU seconds")],[#text("Traced Python peak bytes")],[#text("Data output bytes")]),
[#text("Sharp-prefix cached")],[#text("8.921875")],[#text("1707637")],[#text("476055")],
[#text("Shared-cap DP")],[#text("24.5")],[#text("4347301")],[#text("1090097")],
[#text("Shared-marginal heap")],[#text("22.875")],[#text("4350232")],[#text("1099471")])
]

#figure(image("figures/w41_costs.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("shared-marginal heap study B=2 costs, one instrumented observation per saved solver-condition. CPU includes its documented solver scope; peak is traced Python allocation, MB means 1,000,000 bytes, and output is logical data size. Equal risks/full ties and zero extra endpoint/prune gain remain explicit. No timing uncertainty, speed ratio or total-cost superiority is estimated. [C20,F2]")])
= #text("S39. Terminal permutation: a precise invariance theorem")

#text("Let I be immutable item IDs, Omega a common nonempty world set, and R_i(omega,b) a static observation relation. A subset M is fixed before any observations. Its order pi is a permutation of M; b is a positional label tuple, while z={pi_j maps to b_j} is the terminal ID function. Define F_pi(b) by the conjunction of all R_pi_j(omega,b_j). Closed threshold bins may overlap: either retain the same relation on both sides or use one identical deterministic boundary rule. Changing the rule with order violates the theorem. [C23]")

#text("Theorem (terminal reindexing). For another permutation sigma of the same M define T(b)_j=b_(pi inverse(sigma_j)). T has inverse T from sigma back to pi, and F_pi(b)=F_sigma(T(b)). Hence feasible tuple sets correspond bijectively, infeasible tuples remain infeasible, and the infimum, supremum and width of the same Delta agree. Proof: every item-ID observation atom occurs once on both sides with the same label; conjunction order changes no atom. Substituting them gives both set inclusions. Inversion follows by composing the two positional index maps. [C23]")

#text("If all selected items are immediately and always available, are revealed once, and the policy reads all M before a history-independent terminal STOP, additive C(M) and affordability under Q agree. An order-invariant terminal predictor P(M,z) has equal terminal loss. Maximizing width over the terminal bijection preserves R(M) and transports every maximizing label; applying this argument to a common subset family preserves the (risk,price,mask) choice and all affordable primary-risk subset ties. This is a mathematical consequence for the family, not a newly executed all-subset study. [C23,C24]")

#text("The empty subset has the unique empty order and tuple, F(())=Omega, price 0 and full worst tie set {()}. An empty base Omega is an invalid model, never a zero-risk observation. If infima/suprema are not attained their equality still follows from equal world sets; the stored finite-binary compact polytopes attain both. A common prior pushed forward along T preserves expected terminal loss across orders, which still does not equate expectation with a worst value. [C23]")

#text("In the saved static witness M={0,2}, actual W41 enumeration order [2,0] becomes canonical [0,2]. Positional (0,1) maps to (1,0), both meaning z(0)=1,z(2)=0. Its sharp interval is [-11/90,43/90], with width 54/90=3/5; both price 2. Both z(2)=0 readings are worst ties. The other two ID readings have width 17/30, so the widths are not constant and W42's full-support constant-width bridge is not established. [C25]")

#fit-equation[$ F_pi(b) = F_sigma(T(b)) $]
#text("The conjunction is invariant only after ID-preserving reindexing under a common static observation relation.")

#fit-equation[$ L_pi(b) = L_sigma(T(b)), quad U_pi(b) = U_sigma(T(b)) $]
#text("Equal feasible worlds and the same original loss imply equal endpoints, hence equal width and transported complete worst ties.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Static terminal-order analysis result after reindexing to the same ID labels; four conjunctions from one saved subset, each encoded under two orders.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("z(0),z(2)")],[#text("[2,0] tuple")],[#text("[0,2] tuple")],[#text("Lower")],[#text("Upper")],[#text("Width")]),
[#text("0,0")],[#text("0,0")],[#text("0,0")],[#text("-11/90")],[#text("43/90")],[#text("3/5")],
[#text("1,0")],[#text("0,1")],[#text("1,0")],[#text("-11/90")],[#text("43/90")],[#text("3/5")],
[#text("0,1")],[#text("1,0")],[#text("0,1")],[#text("-4/45")],[#text("43/90")],[#text("17/30")],
[#text("1,1")],[#text("1,1")],[#text("1,1")],[#text("-4/45")],[#text("43/90")],[#text("17/30")])
]

#figure(image("figures/w44_terminal_intervals.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Four distinct ID-indexed static conjunctions, two order encodings each. Horizontal segments are exact identification intervals, not confidence/error bars. The worst width is 3/5 for both orders at price 2 (no_gain); the narrower 17/30 intervals prevent a constant-width claim. [C25,F3]")])
= #text("S40. Action order, solver diagnostics and a deadline counterexample")

#text("Three objects must remain distinct: a terminal ID reading (M,z), an acquisition action sequence A, and the solver diagnostic prefix record D. W41's stop-error-first order at research.py lines 216-225 controls static enumeration/label coordinates; it is not a record that sensors ran in that time order. D can contain visits, bounds, incumbent updates, cache hits and strict-prune decisions. Terminal equivalence asserts none of those prefix facts. [C24]")

#text("With common reveal/boundary/STOP semantics, equal order functions on reachable inputs imply equal acquisition traces by induction on their positions. Conversely, if all items are acquired and traces preserve IDs, literal trace equality forces the same item at each position. Distinct permutations therefore differ at the first unequal ID, even if the observed labels coincide. Different prefixes can condition on different subsets and yield different bounds, pruning and total work. The theorem does not predict a solver speedup. [C24]")

#text("The counterexample changes the environment identically for both schedules: items {0,2}, unit duration and price, hard budget 2, completion deadlines d0=1 and d2=2, four bit worlds and target XOR. Order [0,2] completes at times 1 and 2. Order [2,0] reveals item 2 at time 1, then rejects item 0 before acquisition because its proposed completion 2 exceeds deadline 1. All four [2,0] schedules are infeasible; all four [0,2] schedules complete. The rejected prefix pays price 1 and leaves XOR width 1; completion pays 2 and leaves width 0. Lower incomplete-prefix price is not a successful cheap policy. [C26]")

#text("Two IDs are minimal for distinct permutations; one world suffices to show schedule infeasibility. The four constructed worlds additionally show residual target uncertainty and do not claim minimal world count or empirical failure probability. The comparison demonstrates violation of static always-available reveals under a common changed deadline model. It is not an improvement over the original W41 problem and must not be pooled with static width rows as an algorithm benchmark. [C26]")

#figure(image("figures/w44_deadline.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Completion counts 0/4 versus 4/4 for the same four constructed worlds, under the same new deadlines. This is a deterministic assumption-violation counterexample, not a sampled success rate, sensor trial or algorithm-superiority estimate. [C26,F4]")])
= #text("S41. Complexity and measurement limits")

#text("Let N=sum n_j, A=sum a_j, b=min(B,A), and P be the number of participants. A conservative sharp endpoint cost is H=O(sum_j 2^a_j*n_j*log(n_j)+P*(b+1)^2) rational operations, with implementation-specific caches. All subsets and their binary readings contain sum_S 2^|S|=3^N complete labels; full prefix traversal has at most 2*3^N-2^N nodes. The full solver therefore remains exponential even when its envelope allocation becomes cheaper. Required complete tie coordinates, copied box keys, DFS frames and serialized raw records have output-sensitive storage costs. [C08,C16,C20]")

#text("The shared-cap allocation module uses O(sum_j B*min(B,a_j)) rational DP transitions, O(B) rolling layers and stored local tables. The implicit heap uses O(N+P+q*log(max(2,P))) rational work including aggregation, q<=min(B,sum a_j), and O(P) heap storage. These bounds concern the envelope allocator; the separate sharp endpoint can still enumerate binary placements and use DP. Fraction GCD, products, comparisons and integer bit growth add costs not captured by rational-operation counts.")

#text("Single-run instrumented CPU is neither randomized timing evidence nor a throughput guarantee. In W41 B=2 the heap used less observed CPU than DP but more than sharp-prefix, and had larger peak Python allocations and output than DP. No additional pruning or endpoint reduction occurred. Tracemalloc peak is not RSS; logical file lengths are not physical I/O; returned or sampled Fraction bits do not bound every temporary product. Zero-rounded short-phase CPU means below timer resolution, while missing measurements remain null/unknown. [C20]")

#text("W42 review found two remaining complexity gaps: the written O(K*m^2*h^2) policy-audit bound omits the nonzero stop-only h=0 branch, and the claimed Omega(K*T) storage does not distinguish shared child objects from complete serialized tree lengths. This synthesis withdraws those expressions as general validated bounds; it does not claim to repair them with a new theorem. A revised account must separate explicit serialized length sum from shared in-memory objects, original-world scans and arithmetic bits. [C22]")

#text("For already supplied valid permutations and fixed-length label references, the new reindexing operation uses O(1+k) average dictionary operations and O(k) additional references, k=|M|. ID hashing/comparison and copying or serializing variable-length labels have their own bit/byte cost; writing L bytes costs at least Omega(L). Enumerating 2^k binary tuples, computing endpoints E(Omega,M,z), rational arithmetic and diagnostic output remain separate. The empty tuple still incurs validation/call work. This local bound does not repair the W42 h=0 policy-generation or shared-object/full-serialization issue. [C28]")

= #text("S42. sequential-objective analysis: sequential prediction and fixed-subset width are different tasks")

#text("The saved GSMRL body describes acquisition and terminal prediction loss. W42 inspected 98,206 selected source bytes and 132 math nodes, with zero alttext/TeX mismatches. The reviewer also read an additional header interval, giving 100,488 bytes in the union. This establishes the recorded extraction and reading scope, not correctness of 132 mathematical statements or identity to a particular publisher/arXiv edition. Printed Equation 1 is per-instance; expected undiscounted loss is the author's explicit MDP interpretation with gamma=1 and no shaping. The original AO* paper and the 2002/2004 identity were not directly established. [C21,C22]")

#text("The saved conditional translation matches worlds, feasible observations, prices, hard budgets and precommitted subset policies. It additionally bridges terminal loss to conditional width g(S,omega)=W(S,x_S(omega)); this changes a prediction target when encoded as regression to zero. Under a fixed full-support distribution, E[g]=max W for a given subset if and only if every feasible transcript has constant width: every term p_t(max W-W_t) is nonnegative and their sum vanishes only when each gap does. Alpha=0, a common hard budget, the same secondary lex rule and separately retained complete primary ties then support the restricted value/tie correspondence. Positive additive price can destroy unequal-price primary ties. Maximizing over all distributions restores a maximum but changes the problem. [C21]")

#text("The W42 review required a narrower execution claim: W41 orders known stop-error coordinates first and then indices; W42 uses increasing-index canonical subsets. The W44 theorem now supplies the explicit terminal permutation map under static assumptions. Literal original-program ordered traces, prefix bounds/prunes/cache/incumbents and schedule-dependent cases remain outside that result. Availability, delay, failure and chronology can invalidate the quotient, as the common-deadline counterexample shows. The original W42 ordered-program equivalence was not established, and the later terminal result does not retroactively close its review. [C22-C26]")

#text("Witness 1 has one feature and three worlds: expected priced loss buys A at 3/8, while worst priced loss stops at 1. Fixed-subset worst conditional Delta=y width is 1 for both empty and one-feature subsets. Witness 2 has two features and three worlds: observe A, stop when A=0, otherwise buy B. It has zero error and expected price 3/2, giving 3/32 at alpha=1/16; the best fixed subset buys both for 1/8. Both have worst price 2, zero final error and zero worst width. The eleven public policies, six subset tables and 51 original-world arithmetic checks are exhaustive finite witnesses, not trained GSMRL, a replay of W41, or new empirical samples. [C21]")

#text("The W42 expected-versus-worst and adaptive-versus-static witnesses retain their original objectives and arithmetic after W44. Reindexing observations neither supplies a learned prior nor imposes constant width, alpha=0 or gamma=1. The two sets of results can therefore be read together without inferring a general GSMRL-to-minimax reduction. In particular, the static W44 widths 3/5 and 17/30 differ across readings. [C21,C25]")

= #text("S43. Validation scope, finite denominators and unmeasured cost")

#text("The W44 author main stored eight static rows and eight deadline rows, and its separately written raw-only arithmetic audited the same sixteen. The reported total 32 counts passes over saved checks. A separate coordinator recomputed four distinct static conjunctions and the eight schedule/world rows without importing or replaying the study. These checks found zero endpoint mismatches and preserved all closed-boundary labels and worst ties. They provide finite implementation evidence; the general theorem rests on its proof and assumptions. [C25,C26,C29]")

#text("W44 direct-stage CPU/wall receipts cover one unit, main and raw-only audit process. Unit CPU/wall were 0.25/6.6203746 seconds; main 0.46875/3.9016218; audit 0.1875/0.3869421. These single stage observations have different work and are not a speed contest. Recorded scopes exclude startup before measurement, earlier ownership-gate CLI, shell, authoring, actual acquisition and model cost. Returned endpoint bits reached 7; intermediate rational growth, RSS and physical I/O remain unmeasured. [C28]")

#text("The saved independent review reports that the declared W44 path snapshots/gsmrl_response.bin does not exist. The full source actually preserved in the W22 origin has SHA256 68c70a3a4f6a0746648ab2d3c2eb56a0cceae2679f642e7020c38c06088335df; four W44 excerpts totaling 7,879 bytes match retained byte ranges. This edition links the real source and exact excerpts and leaves the incorrect historical path intact. It does not authenticate an external version. [C27,C29]")

#text("Some sentences in the frozen W44 METHOD review contain damaged question marks. We preserve those bytes as a historical defect and use readable raw results, code coordinates and the separate arithmetic review for this new document. We do not reconstruct missing review prose, assert that the previous intake hold was resolved, or count the current author's schema/hash/content checks as an independent scientific review. [C29]")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Cost categories must retain their measurement scopes; unknown costs are not zero.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Category")],[#text("What is available")],[#text("What remains unknown")]),
[#text("Empirical acquisition")],[#text("Logical quotes and target attempts")],[#text("Physical energy, delay, sensor failure, external utility")],
[#text("W41 solver")],[#text("One instrumented CPU / Python peak / logical-output observation")],[#text("Repeated timing, RSS, total practical throughput")],
[#text("W44 reindexing")],[#text("2 moved labels and 5-byte input/output tuple serialization per static row")],[#text("General bit cost, endpoint/search speedup")],
[#text("W44 direct stages")],[#text("Unit/main/audit CPU and wall, separately scoped")],[#text("Startup/gate/shell/authoring and physical/model cost")],
[#text("Current authoring")],[#text("Document/figure/schema/hash checks only")],[#text("Model tokens/cost, new experiments: not measured / not run")],
[#text("Deployment/model evaluation")],[#text("not_started; cost null")],[#text("Independent application and real acquisition benefit")])
]

= #text("S44. What the cumulative evidence supports")

#text("Equal component weights, fixed quote coefficients and worst interval width are declared research objectives, rather than elicited stakeholder preferences. A policy can reduce component errors while worsening complete diagnoses, or reduce expected quoted price while leaving worst price unchanged. The cumulative record therefore keeps target-specific failures and denominators beside each favorable contrast. Clinical safety, participant benefit and industrial utility require evidence beyond the selected scalar objective and remain unmeasured here.")

#text("The evidence supports completed local observation contracts, exact conditional numerical contrasts, finite counterexamples, and saved theorem arguments for a declared robust world model. It supports several negative conclusions: no admitted MHEALTH routing gain, no new information at unmeasured fallback cells, no generic submodular guarantee, no objective gain over a matched exact solver, and no consistent total-cost advantage of pruning/DP/heap variants. It also preserves specific theoretical gains, including sharpness outside the failed slack shortcut and tighter shared-cap envelopes, with their domains stated. [C07-C22]")

#text("The six W42 review areas remain dated evidence: architecture and finite same-information baselines existed; algorithm correspondence, complexity, application evaluation and related-work version matching were partial. The new ID-preserving terminal quotient answers one narrowly stated semantic question. Literal original-program execution equivalence, stop-only/shared-object/output complexity, independent measured acquisition utility and original AO* primary/version comparison remain needs_evidence. A source hash, accepted Task, terminal theorem or new manuscript does not close those scientific questions. [C22-C29]")

= #text("S45. Saved feedback, limitations and the next decisive evidence")

#text("The saved current-review distribution concern remains active in this cumulative edition. A one-rig exposed Hydraulic result, a two-participant MHEALTH result and a constructed multi-participant fixture have different support. They cannot be pooled into an independent final study, and repeated wave publication does not create a new physical unit. The later theory explains what assumptions would identify an answer; it does not supply the missing independent population or physical-acquisition observations requested by that review.")

#text("The saved current-review baseline concern is answered by preserving its negative result rather than selecting a more attractive diagnostic. Hydraulic v15 still admits k=1 and its unchanged nine price-budget decisions; MHEALTH routing still ties the strongest selected myopic rule; shared-cap DP and heap still match the same exact risks and ties. Unselected predictor gains, altered objectives and lower counts for one internal operation remain separately labeled and cannot replace the admitted comparison.")

#text("Historical Big Guy highlights in the local library are publication-based editorial interpretations of public writings; the named scholars did not review this work. The newer v15 current-review links point to actual saved Codex review issues PF15-DISTRIBUTION and PF15-BASELINE, authored in a separate lane of the same native session, with their stated audit scope. This edition maps those saved concerns to new exact paragraphs and preserves the original attribution limits. Generic companion reading marks are not feedback, and no new professor, external or model review was commissioned.")

#text("A decisive application study would first define independent participant/device units, frozen predictor and information rights, true availability/failure/latency and cost receipts, and a loss chosen for the intended user. Strong static, same-STOP myopic and permitted adaptive controls would share data, tuning opportunities, budgets and outputs. Missing/failed/unknown/no-gain records would remain in denominators; physical and model costs would have explicit scopes. Until those contracts and observations exist, actual acquisition/model evaluation is not_started with cost null and science_status needs_evidence. The cumulative edition preserves completed work without claiming that the remaining research is complete.")

#text("The combined contribution is a traceable boundary between completed local evidence and remaining inference: an explicit shared-source/disclosure design, exposed and registered negative application results, sharp assumption-dependent identification, exact fixed-subset selection with complete ties, and a terminal invariance theorem whose deadline counterexample marks its domain. None of these converts an unchanged strongest baseline, unobserved fallback, higher retained cost or invalid schedule into an admitted practical gain.")

= #text("S46. A return to prediction: frozen representations and source identity")

#text("The historical MHEALTH15-mask RF bank and the W45-W47 single mask-aware RF are different predictor contracts over related source windows. The former fits subjects1-3, calibrates4 and reports527 target windows from9-10. The latter was fitted once on1098 windows from1-4, augmented across16 masks to17568 encoded rows, with69 normalized channel-summary features plus4 observation bits. Thirty-two conditional trees were fitted in W45 across two participant-separated conditional folds. W46 and W47 reuse the frozen predictor and fold0; the two conditional-fit participant IDs5 and6 do not denote two new fits. Current new_fits=0. [C30,C31]")

#text("Frozen NPZ copies for subjects5,6,7,8 contain264,250,266,258 windows respectively. The current524-window DEV pool is subjects7-8, rather than the historical527-window target pool. The split is by participant role, but repeated analysis and policy selection on these exposed people remove any fresh confirmatory interpretation. The subject5/6 arrays are read by this edition for descriptive and historical-fit-audit provenance; no learning is repeated. Original source identity, admitted feature identity and model identity have separate hashes.")

#text("The descriptive EDA verifies dimensions, finite feature values, class counts and unique128-row-aligned offsets. A finite admitted feature array does not establish absence of missing source readings or correctness of the original physical sensor axes. Feature standard deviations span heterogeneous native units; this is a reason to preserve the training-only normalization, not to refit it on DEV. The four engineering groups remain9,6,27,27 features. Raw activity labels are available to the post hoc evaluator, while the selector's public encoding receives only acquired values and observation bits.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 10. Descriptive verification of admitted feature arrays")]]
#v(3pt)
#strong[Require] #text("Frozen subject5/6/7/8NPZ,manifest/source hashes,training-only normalization metadata and saved integer policy summaries.")
#parbreak()
#strong[Ensure] #text("Per-person shape/finite/label/offset/class/feature-block statistics and exactly reconstructed saved macro scores; no fitted model or new predictions.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Verify immutable source paths and SHA256 against the manifest; load NPZ using allow_pickle=False.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Require x(n,69),aligned y/offset dimensions,finite admitted features,label1..12 and unique128-aligned offsets; failure aborts rather than repairing data.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Count each person's labels and summarize native-unit feature blocks; keep conditional-fit inputs and exposedDEV roles separate.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Use saved participant integer errors/quotes to calculate Fraction macroerror,macroquote and J with lambda1/20.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Assert agreement with stored scores,write EDA/source/figure records and preserve missing raw-series/physical-unit evidence as a gap.")]])
#v(1.2pt)
]

#figure(image("figures/eda_class_balance.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Direct descriptive EDA of four frozen local NPZ arrays; counts per participant and label ID. Subjects5-6 are conditional-fit audit inputs,7-8 are exposed DEV.1038 windows are four people, not1038 independent people. No raw archive reread, model fitting or inference. EDA.json fixes exact NPZ hashes and count arrays. [C34,F5]")])
= #text("S47. The action-local rule and its conditional theorem")

#text("At the fixed public state the first group/action0 has been acquired, mask=1, spent=1, remaining=1, total=2 and cache is empty. Let F be feasible next actions1,2,3. Each action's frozen fitting leaf supplies a mean loss reduction mu_a and support metadata. S contains only actions with at least30 fitting windows and two fitting participants. With one-quote actions and lambda=0.05, choose the smallest-index supported action maximizing mu_a-0.05 only when the maximum is strictly positive; otherwise STOP. Empty support and nonpositive fitted gain have distinct reasons. [C32]")

#text("The blanket ablation applies this same choice only if S=F, otherwise it STOPs. Thus both rules coincide when every feasible action is supported. When some action is unsupported but a different supported action has positive fitted value, only local admission can buy. Every local purchase is supported by construction and at most one additional quote is used. Its fitted incremental value max(0,max over S of mu_a-0.05) weakly exceeds the blanket rule's value; there is no implication for realized prediction error, rare-event safety, population risk or true acquisition value. The local myopic control independently sorts the same values under the same support/STOP/tie rules and therefore defines the identical decision map.")

#text("Support-gated fixed subsets1,3,5,9 retain only their one predetermined optional action and buy it when supported, with no positive-net requirement and no replacement. Fixed orders[0,1],[0,2],[0,3] additionally require positive fitted value under multipliers0.5,1,2. All16 policies share the model, first acquired group, attempt cap, information and support lookup rights. This limited fixed-prefix catalogue is not the original full-budget policy class. Thirty-four incompatible static policies, representing17816 paths, were unexecuted and must not be scored as zeros.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 11. One-remaining-quote action-local admission")]]
#v(3pt)
#strong[Require] #text("Frozen73-input RF and fold0 conditional trees; public acquired group0 values/mask1; spent1,remaining1,total2,empty cache. Feasible actions1,2,3; per-action fitting leaf counts/participants; quote1,lambda0.05; lower-index tie rule.")
#parbreak()
#strong[Ensure] #text("STOP with empty-support/nonpositive reason, or one supported extra action and a final frozen prediction; complete cost/intent/trace records.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Validate model/input hashes, public mask, dimensions and budget; mismatch fails without a new inference attempt.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Encode only acquired group0 and observation bits; compute the frozen initial prediction.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Look up each feasible action's conditional leaf using public state, retaining its fitting window/participant support and mean.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Build S using each action's own30-window/two-participant predicate; do not veto one supported action because a different action is unsupported.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("If S is empty, STOP insufficient_support. Otherwise select maximum mean minus0.05 with smallest action-index tie; if value<=0 STOP nonpositive.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Before a positive purchase, validate remaining quote/control/time, write intent, copy only the selected local group, debit quote and compute final prediction.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Write and flush the trace, check finalization barrier and preserve all failures/unknown states; do not retry an interrupted accepted path.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compute label-based scores only in the evaluator after selection. Keep full-bank/raw-label audit rights separate and retain myopic equality and stronger static controls.")]])
#v(1.2pt)
]

= #text("S48. timed-main failure study failure and limited-pool support study support failure are retained results")

#text("W45 constructed one common predictor and32 conditional models, then computed53 development selection tables on1038 windows from four exposed participants. The instrumented main planned4152 paths. It completed8 candidate paths, failed the ninth at subject5/index8 before acquisition because the two-second measured budget was crossed, and left4143 paths unstarted. Heldout groups=0. The saved selection calculations are explicitly not a completed, numerically certified main comparison; the partial oracle checked syntax/counts/hashes only.17 pre-STOP events and the original failure prefix remain preserved. [C30]")

#text("W46 reused the same predictor and conditional fold0 at mask1/one remaining quote. Its15 compatible policies completed1800 paths on120 exposed DEV windows,60 per participant7 and8. Candidate/myopic tied; action2 occurred in46 windows from two people and action3 in11 from only participant8. The specified support admission failed. Candidate macro J=0.4154166667 exceeded subset5 J=0.2333333333 and compatible order J=0.3716666667. The saved maximum scoped row wall0.1046045seconds is one observed pass, not an operating-system deadline guarantee. Preparation process exit remained unobserved/null after wrapper metadata loss. [C31]")

#text("W47 enlarges the exposed pool and changes the subset support semantics under an explicit clarification. It cannot retrospectively convert W45's failed main into a success or W46's insufficient_support into a pass. Within-run candidate versus blanket compares the guard under a common pool; cross-wave differences combine pool, path and policy-contract changes and do not isolate a guard effect.")

= #text("S49. full-pool support study: local guard improvement, myopic tie and stronger-static regression")

#text("All16 current policies completed524 paths each:8384 planned=started=completed, with failed/partial/unknown/unstarted all0. Unsupported purchases were0 for every policy. Candidate and local myopic tie on524 paired windows. Their two actual branches use action2 on249 windows (P7=114,P8=135) and action3 on55 (P7=3,P8=52). The descriptive total>=30 and two-participant gate passes, but it is not30 windows per participant; the three-window P7 branch remains sparse. The same larger pool also makes the legacy rule pass the descriptive gate. [C33]")

#text("Local admission changes41 purchases relative to the same-run blanket guard:33 in P7 and8 in P8. It corrects16 errors, introduces0 errors and leaves25 error ties within those41; P8 pays8 extra quotes and corrects0 errors. Across all524 candidate windows, extra acquisition corrects80 initially wrong predictions but harms39 initially correct ones. A zero harm count in the guard-changed subset must not be used as a whole-policy safety statement.")

#text("Exact count reconstruction gives candidate error=(64/266+95/258)/2, quotes=(383/266+445/258)/2, J=0.38352567465174564. Legacy blanket J=0.40972416506382237, strong support-gated subset5 J=0.25111980532727163, and order0,2 multiplier1 J=0.3423464183715102. Candidate minus legacy J=-0.026198490412076725, but candidate minus subset5=+0.132405869324474 and minus order=+0.04117925628023544. These are paired descriptive differences on previously exposed people; no uncertainty interval, population superiority, causal acquisition effect or new independent sample is claimed.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("full-pool support study saved integer counts and participant-macro objectives; all share the same524 exposed DEV windows.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Policy")],[#text("P7 errors/quotes (n266)")],[#text("P8 errors/quotes (n258)")],[#text("Macro J")]),
[#text("candidate")],[#text("64/383")],[#text("95/445")],[#text("0.383525675")],
[#text("local_myopic")],[#text("64/383")],[#text("95/445")],[#text("0.383525675")],
[#text("legacy_blanket")],[#text("80/350")],[#text("95/437")],[#text("0.409724165")],
[#text("subset_5")],[#text("31/492")],[#text("50/513")],[#text("0.251119805")],
[#text("order_0_2_m1")],[#text("64/382")],[#text("75/421")],[#text("0.342346418")])
]

#figure(image("figures/w47_objective.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("full-pool support study participant-macro error plus0.05times macro quotes. Every plotted value is independently reconstructed here from saved participant integer counts, not generated predictions. Lower is better; same524 exposed windows and no confirmatory error bars. Candidate=myopic, and strong fixed controls have lower J. [C33,C34,F7]")])
= #text("S50. Updated architecture, cost ledger and independent review scope")

#text("The current evaluator holds full frozen feature arrays and labels in one process and cooperatively passes only acquired values into selection. The policy plane computes public encoding, frozen prediction, conditional leaf/support lookup, selection and optional local feature copy. The audit plane separately has full arrays/labels and a manually implemented forest traversal. This is inspected information flow, not process isolation or a proof that an adversarial selector cannot read hidden memory. No physical sensor was acquired. A local provider completion records a selected copy, not a new measurement from a device. [C32,C35]")

#text("The W47 main direct stage observed215.7763239000 wallseconds and64.546875 direct CPUseconds. Each row's two-second scope runs from work_started logging through post-trace finalization, excluding terminal timing-receipt serialization, EXIT and launcher tails. There were4806 observed-zero CPU rows at timer resolution; missing CPU is a different state. Full shared preparation/import/load charges20.4981172000 wallseconds/10.40625 CPUseconds and the mixed unallocated main residual5.9793097021/3.078125 are shown identically for each policy as accounting scenarios, not16 physical preparations. Full deployment, historical-fit amortization, physical I/O/cache/energy and transient memory remain null or unobserved.")

#text("The current selector's max step is linear in K eligible actions, while sorted myopic and serialized sorted sets may cost KlogK. The saved implementation's broad word-operation account includes feature encoding, forest traversal and class accumulation, all conditional lookups including support participant metadata, logging/control/hash work and an optional second forest call. It does not become constant total cost merely because the actual73 features,48 trees and3 optional actions are fixed. Audit/export/authoring costs have separate scopes; the earlier exponential exact-solver bounds concern a different computation.")

#text("The completed independent W47 reviewer Task is task_2941f86cd801. Its canonical METHOD SHA77a849c1154a65af7aece7ec05ffc81be4a2a0fc99b16d95cb78ae9ceefdecac marks algorithm and architecture exists, with complexity, evaluation, baselines and related_work partial. Manual arithmetic, hidden-feature/label intervention checks and portable-export agreement are bounded evidence, not independent confirmation of the export's statistical validity. This new documentary author's selfcheck is separate again. Scientific status remains needs_evidence; all scientific gate/promotion claims remain false. [C35]")

= #text("S51. Completion of the record and the next acceptance boundary")

#text("This edition keeps the entire earlier paper and supplement argument through W44 and adds the later development return, local descriptive EDA and source-selection matrix. A longer or newer source was not automatically preferred: v24's detailed loss/oracle/support explanations are retained and rewritten coherently, its PAMAP2/benchmark plans remain unexecuted designs, and later source-verified limitations qualify older open-ended language. Repeated historical tutorial passages are mapped to their consolidated chapters instead of duplicated. The old53-page explainer page count is a handoff report until its actual PDF is located; the210099-byte v24 Markdown itself was obtained and hash-bound. [C36]")

#text("A decisive next application result still requires a separately frozen independent participant/group sample, actual acquisition/failure/delay and complete-cost contracts, strong feasible fixed and matched myopic/adaptive controls, and an acceptance rule set before opening outcomes. More DEV windows or restatements of the same source do not provide that evidence. No new model, learner/provider/API request, fitting, unit/main/oracle replay, dependency, publication, active skill or submission is part of this edition.")

= #text("S52. Exact preference sensitivity of a frozen hydraulic gate")

#text("This restores the substantive preference derivation from the older detailed supplement, not merely its topic label. The comparison fixes secondary gate g301/k3 versus locked fixed mask3, equal source prices (1,1,1), cap2 and the same421 exposed evaluation cycles. No policy is refitted or selected for a new preference. Alpha weights complete diagnosis against mean-head loss; lambda weights the separately normalized source quote. They are independent decision parameters.")

#text("For cycle i and mask m, d_i(m) is an integer number of wrong heads in0..4 and v_i(m)=1 when at least one head is wrong. Component loss is d_i/4; vector loss is v_i. Their convex mixture expresses a preference: alpha0 values each head equally, alpha1 values complete-diagnosis success. It does not transform four dependent head decisions into four independent samples.")

#text("Each source quote is1 and a mask may cost at most2. Therefore the mean cost term divides total quotes by3n; the component term divides total wrong heads by4n and the vector term divides wrong cycles byn. In this continuation only, the cost normalizer3 is fixed by the equal-price contract. Replacing it by another price book without changing the derivation is invalid. Lambda cannot authorize an action outside the cap.")

#text("The fixed mask3 has924 wrong head decisions,381 wrong complete diagnoses and842 quotes. The unchanged g301 has861,391 and518 respectively. Their signed differences are-63,+10,-324. Component improvement and complete-diagnosis regression are simultaneously true; neither cancels the other before a preference is declared.")

#text("Multiplying the component change by1-alpha gives(-63+63alpha)/1684. The vector change is10alpha/421=40alpha/1684. The normalized cost change is-324lambda/1263=-432lambda/1684. Adding them yields(-63+103alpha-432lambda)/1684. The103 coefficient therefore combines63 lost units of component emphasis and40 units of complete-diagnosis penalty; it is not a fitted regression slope.")

#text("The zero set isalpha=(63+432lambda)/103. Withlambda0 it is63/103; withlambda1/20 it is423/515. Below the boundary the frozen gate has lower scalar loss, on it the losses tie, and above it fixed mask3 has lower loss. Atlambda5/54 the line reachesalpha1; beyond that cost weight g301 has strictly lower scalar loss for everyalpha in[0,1]. At the threshold onlyalpha1 ties.")

#text("Although the gate wins these weighted comparisons at sufficiently large lambda, it still does not dominate the three-coordinate outcome vector: its vector-error coordinate is worse. Cost preference has compensated that regression, not removed it. If one chooses the arbitrary numerical diagonalalpha=lambda, the same algebra gives(-63-329alpha)/1684<0; this one-dimensional slice is not a reason to identify the two parameters or to select them using evaluation outcomes.")

#text("The phase diagram evaluates the same two locked outputs everywhere. Its cells are dependent recalculations, not60 separately trained policies or60 independent trials. Policies chosen by a new alpha/lambda-specific fit/dev search would be a different experiment, requiring a new locked candidate-selection protocol and independent evaluation.")

#text("The six exact cells below describe the same two outputs. The full region is: for 0<=lambda<5/54, gate wins when alpha<alpha*(lambda), ties at the boundary, and loses above it; at lambda=5/54 gate wins for alpha<1 and ties at1; for lambda>5/54 it wins the scalar objective for every alpha in[0,1]. This does not become Pareto dominance because vector failures remain10 higher. Negative lambda and alpha outside[0,1] are outside this preference contract.")

#fit-equation[$ ell_(alpha,i)(m) = (1-alpha) d_i(m)/4 + alpha v_i(m) $]
#text("d counts wrong heads0..4; v indicates at least one wrong head. Alpha is a preference, not a fitted coefficient.")

#fit-equation[$ Delta_(alpha,lambda) = ((-63)(1-alpha))/1684 + (10 alpha)/421 - (324 lambda)/1263 = (-63+103 alpha-432 lambda)/1684 $]
#text("421 cycles imply4n=1684 head decisions and3n=1263 normalized source quotes.103=63+40 and432=324*4/3.")

#fit-equation[$ alpha^*(lambda) = (63+432 lambda)/103 $]
#text("The line meets alpha1 at lambda5/54; below/on/above it the signed gate-minus-fixed objective is negative/zero/positive.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Exact post-hoc arithmetic from the same421-cycle contrast; original g301 selection remains lambda0.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("alpha")],[#text("lambda")],[#text("Gate minus fixed")],[#text("Interpretation")]),
[#text("0")],[#text("0")],[#text("-63/1684")],[#text("Component-only benefit")],
[#text("1")],[#text("0")],[#text("10/421")],[#text("Complete-diagnosis regression")],
[#text("0")],[#text("1/20")],[#text("-423/8420")],[#text("Errors and cost prefer gate")],
[#text("1")],[#text("1/20")],[#text("23/2105")],[#text("Vector emphasis still prefers fixed")],
[#text("423/515")],[#text("1/20")],[#text("0")],[#text("Exact preference boundary")],
[#text("1")],[#text("5/54")],[#text("0")],[#text("Boundary reaches alpha1")])
]

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Complete region over alpha in[0,1] and lambda>=0; lower signed loss is better.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Lambda region")],[#text("Gate lower")],[#text("Tie")],[#text("Fixed lower")]),
[#text("0<=lambda<5/54")],[#text("alpha<alpha*(lambda)")],[#text("alpha=alpha*(lambda)")],[#text("alpha>alpha*(lambda)")],
[#text("lambda=5/54")],[#text("0<=alpha<1")],[#text("alpha=1")],[#text("none")],
[#text("lambda>5/54")],[#text("all alpha in[0,1]")],[#text("none")],[#text("none")])
]

#figure(image("figures/preference_boundary.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Exact sensitivity of unchanged gate g301/k3 versus mask3 on421 exposed hydraulic cycles, equal unit prices and cap2. The boundary is alpha=(63+432lambda)/103; the shaded/dashed regions reweight identical outputs. No new policy selection, trial, uncertainty interval or empirical efficacy claim.")])
= #text("S53. Root-range strata and heterogeneous complete-diagnosis failures")

#text("Secondary component errors improve on73 cycles, worsen on10 and tie on338. Vector errors worsen on10, improve on none and tie on411. These counts come from all421 raw rows, not from the four illustrative branch examples. New exception rows remain in cycle_metrics.jsonl and are not dropped to make a monotone gain narrative.")

#text("The already used root min/max indicator partitions secondary evaluation into39 inside-range cycles and382 outside. The inside group changes wrong heads by-1, wrong vectors by+8 and quotes by-32. The outside group changes them by-62,+2,-292. Eight of the ten complete-diagnosis regressions are therefore inside the original range. Outside-range status is neither necessary nor sufficient to explain a failure in this contrast.")

#text("Target-seen strata use labels only after decisions for diagnosis. On30 seen-target cycles both contrasts have zero errors; secondary saves9 quotes, while primary spends19 additional quotes. The391 unseen-target cycles carry all reported component/vector errors. These overlapping descriptive partitions neither define a deployable policy nor identify a causal mechanism, and they are not independent replication units.")

#text("The inside-range vector-regression frequency is8/39 and the outside frequency2/382; their numerator sum is10, not a new outcome sample. The root was already purchased before its range indicator could be known. The original gate still branches only on its original threshold. Neither this descriptive flag nor the evaluator-only seen-target tuple flag is an extra policy input. A min/max interval says nothing about internal density gaps or joint feature support; consequently8/10 inside failures rule out the story that outside-range status alone explains this contrast.")

#text("Saved-row aggregation retains all421 secondary rows. For component errors the counts are73 improvements,10 regressions,338 ties; for complete vectors they are0 improvements,10 regressions,411 ties. These are different loss partitions on the same cycles. The inside/outside signed quote sums(-32,-292) reconcile to-324; signed head sums(-1,-62) to-63; vector sums(8,2) to10. Target-seen30 and unseen391 strata overlap the range partition and must not be added as separate samples.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Gate minus fixed from the same frozen masks and original root range. This is a descriptive partition, not new cohort selection or density support.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Secondary original root stratum")],[#text("Cycles")],[#text("Head difference")],[#text("Vector difference")],[#text("Quote difference")]),
[#text("Inside fit min/max")],[#text("39")],[#text("-1")],[#text("+8")],[#text("-32")],
[#text("Outside fit min/max")],[#text("382")],[#text("-62")],[#text("+2")],[#text("-292")],
[#text("All exposed evaluation")],[#text("421")],[#text("-63")],[#text("+10")],[#text("-324")])
]

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("All421 cycles retained; loss changes use gate minus fixed.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Loss")],[#text("Improved")],[#text("Regressed")],[#text("Tied")],[#text("Total")]),
[#text("Wrong-head count")],[#text("73")],[#text("10")],[#text("338")],[#text("421")],
[#text("Complete-diagnosis indicator")],[#text("0")],[#text("10")],[#text("411")],[#text("421")])
]

#figure(image("figures/root_strata.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Complete-diagnosis regressions in two descriptive root-range strata:8 of39 inside and2 of382 outside. Ten total regressions reuse421 exposed cycles. Direct labels and different bar patterns retain meaning in grayscale; no causal mechanism or deployment rule is inferred.")])
= #text("S54. Prospective transfer roles, failed attempts and constrained policy selection")

#text("This is a prospective implementation contract, not executed PAMAP2 acquisition. After verifying the actual Protocol archive and rights, order eligible participant IDs by a fixed label-independent hash. For nine eligible participants assign the first three to predictor training, next two to policy fitting, next two to development selection and final two to reserved test. Thus the earlier five fit subjects are split into disjoint 3+2 roles. If inventory or activity support differs, stop and amend before test access; these planned counts are not a power calculation.")

#text("Fit normalizers and the mask-aware predictor or fixed per-mask predictor bank only on the three predictor-training subjects. Freeze them before fitting selectors. The two policy-fit subjects supply acquisition/risk training examples; development selects among predeclared candidates and test is opened once for final reporting. Do not silently refit the predictor on five subjects after policy selection. Any such refit is a separate named intervention with its own controls.")

#text("The primary task uses nonoverlapping 256-sample completed windows within one Protocol subject/session and one activity-label segment, after raw-time continuity checks. Exclude label0 transition segments from this conditional offline target and retain their counts. Label-based curation defines an evaluation subset; a deployed actor cannot use that gold label or future segment boundaries to choose acquisition. Online prefix inference needs a separate causal windowing contract.")

#text("Before fitting, verify internal column names for 16g acceleration xyz and gyroscope xyz in each physical hand/chest/ankle IMU. The proposed minimal representation is per-channel mean and population standard deviation over the completed window: twelve summaries per acquired IMU. Exclude heart rate, Optional sessions, orientation, temperature, magnetometer and redundant acceleration range in this primary interface. Do not invent column offsets before the bundled specification is admitted. Stop rather than adapt features after viewing test outcomes.")

#text("For this initial complete-group interface, a requested group is unavailable if any chosen raw channel has an invalid timestamp/sample or missing value inside the window. Retain the failed attempt and its quote. No pre-purchase complete missingness mask, unrevealed summary, activity label or subject identifier is an actor input. A static catalog of the three eligible IMU units is public. Only a charged purchase returns the selected unit summaries or its unavailability indicator. Repeated purchase of an already attempted unit is invalid; STOP costs zero.")

#text("The primary caps are one and two attempted IMU purchases. Charge one simulator quote even when the requested group is unavailable; define C as the raw attempted-purchase count in quote units, without division by three, consistently with the main tutorial equation and across all caps/policies. Lambda has units of error per quote; changing the cost normalization requires a corresponding lambda rescaling. These are declared proxy units, not measured energy or wall-clock savings. All-three features are an over-budget reference at caps one/two, not a feasible baseline. Include the zero-purchase predictor prior and every fixed subset feasible at each cap.")

#text("Train all selectors against the same frozen predictor and the same two policy-fit subjects. For fixed global GREEDY, use the equal-subject attempt-marginal table defined in S26 on a common mask-eligible row set for each S. Failures contribute zero error reduction, remain in the denominator and cost one quote. This global comparator ignores current purchased values and past failure identities when estimating gains; a conditional selector is a different candidate. Account for every offline target-generation read and fitting cost.")

#text("Freeze a common candidate/tuning inventory before development selection, including zero-purchase prior, all feasible fixed subsets, the fixed GREEDY rule and the proposed adaptive selector. Bound training passes, seeds, hyperparameter proposals and selector-compute budget. CAFA-ML or BRiG-AFA is a native comparator only under its pinned classifier, unmasker, budget and data protocol; plugging its acquisition rule into this shared-predictor sensor-group interface is an explicitly adapted comparator. Do not merge the native-system and controlled shared-predictor lanes.")

#text("For the single-label primary target use alpha=0. The proposed error cap epsilon=0.10 applies to equal-subject mean development error, not worst-subject error or a population guarantee. At each hard cap k, the predeclared feasible set contains candidates with development equal-subject error at most epsilon, no hard-cap violations, and complete failure/cost accounting. Choose minimum equal-subject attempted cost among feasible candidates, then lower development error, then a predeclared simplicity/order key. Do not use reserved-test labels for ties.")

#text("If no candidate is feasible, record no_feasible_policy and keep every candidate failure and excess-error distance; do not silently choose the least-infeasible candidate and claim constraint satisfaction. Lambda values 0,1/20,1/5 define separately labeled preference-sensitivity analyses, not a post-hoc way to relax the primary constrained decision. Report equal-subject mean, every subject, worst subject and pooled-window counts; the last two are diagnostics, not covert alternative selection objectives.")

#text("Uncertainty must respect subjects rather than treating overlapping or repeated windows as independent subjects. With two proposed test subjects, show the full per-subject table and refrain from broad population or deployment guarantees. Actual eligible groups, archive identity, missingness, fit, policy choice, native baselines and independent transfer remain unobserved.")

#text("Erratum for the deliberately preserved earlier scientific record: the Source-mask errors table caption says development, but the displayed 421-cycle quantities are exposed evaluation diagnostics. The historical source bytes remain intact; this current correction prevents using those values as independent policy-selection evidence. In Figure2, component counts printed above bars and normalized right-axis values use different units explicitly explained in the new caption.")

#text("The reviewer-input coverage gap was identified separately from manuscript scope. Current benchmark selection and project-specific primary-source records must be frozen into the next review context; their absence from a previous nine-source review bundle did not establish absence from the signed publication run.")

#text("Maintain an attempted set T and a successful-observation set S separately. Every attempt increments cost and T; only a valid returned complete group augments S. Query the frozen predictor by S, never by T. At STOP, use the same empty-observation prior, trained on predictor-training subjects with a prespecified class-ID tie rule, if and only if S is empty; otherwise predict from the successfully observed set S, retaining earlier successes after any later failed purchase. Keep their classification errors and consumed cost in every window/subject denominator. No policy may drop unavailable windows after seeing its own acquisition path.")

#text("For fixed global GREEDY use S26, not success-conditional mean gain. Maintain successful-observation set S and attempted set T, rank only j outside T, and use the same S-indexed gain table after failures. Positive ties use the declared hand/chest/ankle order. STOP for nonpositive gains or exhausted cap. A reached state with an undefined fit denominator is not_estimable and falls back to STOP with its current valid prediction, never zero gain imputation or row deletion. S26 states the limits of this deliberately history-blind table.")

#text("Participant assignment uses predeclared structural admission and a label-independent ID hash, never model outcomes or test class frequencies. Apply the fixed label0/transition curation after assignment and log every resulting window count. The equal-subject formula is defined only if every planned evaluated subject has m_s greater than zero. If any dev/test subject has zero retained windows, record not_evaluable with the original planned subject denominator; do not drop, impute zero error, replace subjects or claim the original reserved test remains untouched. This differs from no_feasible_policy, which requires defined metrics and no candidate meeting the fixed constraints.")

= #text("S55. Attempt-marginal global GREEDY with common eligible windows")

#text("This section defines a prospective comparator; no PAMAP2 archive was acquired and no selector was fitted. Let S be successfully purchased units and T all attempted units. The actor sees S, T, purchased summaries, remaining cap and a previously fitted table; it receives no current unpurchased availability mask, values or labels. The executor alone resolves a purchase and charges one quote even on failure.")

#text("For each planned policy-fit subject s and mask S, I_s(S) contains all prespecified retained policy-fit windows where every group in S is valid. Use this same set for every candidate j outside S; do not additionally restrict it to successful j purchases. A_sij records whether j would return a complete valid group. The after-loss is evaluated only when A=1. Failures retain the prediction f_S, so their error reduction is exactly zero, not an excluded denominator. The empty mask includes every prespecified retained window. Offline target construction may inspect policy-fit labels and availability, with its full collection/compute cost recorded. Define d_sij(S) as the before-minus-after loss on success and exactly zero on failure; the after-loss need not exist for a failed return.")

#text("Define m_s(S)=|I_s(S)| and average each subject first, then subjects equally. If any planned subject has m_s(S)=0, the whole S table is not_estimable. Do not drop that subject, replace its mean by zero or change the subject count. At a reached unestimable state, STOP using f_S (the frozen prior only for S empty), keep its error and attempted cost, and separately count this fallback. Do not claim the table was estimated.")

#text("This is a global mask-indexed baseline. It does not condition the gain table on current purchased values or the identities of failed earlier attempts. Correlated failures can therefore make it suboptimal. All rows where S is valid are used instead of rows selected by a fitted test policy. There is no causal transport, unbiased on-policy utility or optimality claim. A T-conditioned or observation-conditioned acquisition rule is a separately fitted and budgeted candidate.")

#text("Choose the unattempted unit with largest strictly positive g(S,j); break ties by hand/chest/ankle. Attempt it, increase T and cost, augment S only on a valid return, then repeat within the hard cap. Nonpositive best gain, no remaining unit, exhausted cap or an unestimable table causes STOP. The unit-quote rule makes raw-error gain ranking well defined here; non-unit future prices would require a separate declared ranking or constrained optimization, not a silent gain/price ratio.")

#text("Constructed counterexample: candidate A fixes nine of100 baseline errors but succeeds on only those nine windows; B succeeds on100 windows and fixes20. Attempt-marginal gains are9/100 versus20/100, favoring B. Success-conditional means are1 versus1/5, incorrectly favoring A for this declared attempt objective. These are invented arithmetic examples, not data frequencies.")

#text("Subject weighting can independently reverse a ranking. With one window for subject1 and nine for subject2, A has gains1 and0, whereas B has gains0 and2/9. Equal-subject gains are1/2 versus1/9, but pooled-window gains are1/10 versus1/5. The estimator must follow the predeclared equal-subject target rather than whichever average favors the selected method.")

#text("The executed standard-library check enumerates8 complete availability patterns,256 frozen binary per-mask output banks, four caps0..3 and five fixed gain-table patterns:40,960 constructed traces. It checks attempt charging, no repeat purchases, S subset T, failed-return state preservation, tie order, prior-only-when-S-empty and undefined-table STOP. It is a same-author contract check; its trace count is neither independent people nor measured accuracy. analysis/probeflow-v24-results.json and its frozen code document exact denominators and a trace hash.")

#text("In the formula, K is the fixed planned policy-fit subject count. For each S, every candidate j uses exactly I_s(S), including j failures; j-specific success filtering is forbidden. Offline target construction is permitted only on the policy-fit subjects under its own charged collection/compute scope. The actor cannot inspect an unpurchased success indicator. After a failed attempt, T grows and S remains unchanged; the same S-indexed table is consulted for the remaining unattempted candidates. A failed after-loss is not evaluated or invented: d is defined as zero by retained f_S, while its quote is still charged.")

#text("The40960 count belongs to an already saved same-author synthetic contract check, not a new replay by this edition. Its factors are8availability patterns×256binary frozen per-mask output banks×4caps(0..3)×5gain-table patterns. No PAMAP2 raw acquisition, accuracy result, learned selector, new benchmark or independent participant is supplied by these traces. The current16-policy MHEALTH catalogue is a separate executed study and is not claimed to contain this prospective GREEDY comparator.")

#fit-equation[$ g(S,j) = (1/K) sum_(s=1)^K (1/m_s(S)) sum_(i in I_s(S)) d_(s,i,j)(S) $]
#text("All candidate actions share each S-indexed eligible-window denominator. If any planned m_s(S)=0 the entire table is not_estimable, not zero.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 12. Prospective global mask-indexed attempt-marginal GREEDY")]]
#v(3pt)
#strong[Require] #text("Frozen predictor f_S (training-only prior for empty S), planned fit subjects, common I_s(S), unit attempted quote, hard attempt cap and fixed hand/chest/ankle tie order. Offline fitted S-indexed gains, initially S=T=empty; actor observes purchased summaries/failures only, never current unpurchased availability or label.")
#parbreak()
#strong[Ensure] #text("STOP plus valid f_S prediction or a sequence of charged attempts; distinct successful S and attempted T; complete failure/cost/fallback denominators.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("For every planned fit subject and successful mask S, fix I_s(S) from retained windows where all S groups are valid, using identical rows for every next j.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("On successful j define before-minus-after loss; on failed j define d=0 without requesting a nonexistent after-loss, retaining that window and attempted quote.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Average within each subject by m_s(S), then equally over all K planned subjects; if any m_s=0 mark the whole S table not_estimable.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("At a reached not_estimable state STOP with current f_S (prior only if S empty), retain prediction error/attempt cost and count this fallback.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Among j outside T, choose strictly positive maximum g(S,j), ties by fixed physical-unit order; STOP when cap exhausted, no candidates or no positive gain.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Attempt j and charge one quote regardless of success; add j to T always, to S and purchased summaries only on a valid complete return.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Continue with the same S-indexed table after failure. No repeated purchase, hidden availability read, subject dropping, zero filling or policy-dependent row filtering is allowed.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Retain all declared evaluation subjects/windows; an empty dev/test subject is not_evaluable, distinct from a defined feasible-set search returning no_feasible_policy.")]])
#v(1.2pt)
]

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Constructed comparator examples only. Failed purchase attempts remain in the declared denominator.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Example")],[#text("Declared attempt/equal-subject gain")],[#text("Alternative conditional/pooled gain")],[#text("Declared choice")]),
[#text("A9 successful repairs vs B20")],[#text("9/100 vs1/5")],[#text("1 vs1/5 success-conditional")],[#text("B")],
[#text("1 and9 windows per subject")],[#text("1/2 vs1/9")],[#text("1/10 vs1/5 pooled")],[#text("A")],
[#text("Any empty planned subject")],[#text("undefined")],[#text("Dropping or zero-filling forbidden")],[#text("STOP + not_estimable")])
]

= #text("Abstract")

#text("ProbeFlow examines when additional acquired information improves a frozen predictor and when incomplete observations support only a bounded conclusion. We connect explicit acquisition/disclosure accounting, negative controlled prediction studies, sharp partial identification and exact fixed-subset information design. These are separate estimands, not one pooled benchmark. Conditional proofs establish sharp endpoints, strict full-tie pruning, a shared-marginal heap and static terminal reindexing; they do not establish real acquisition utility.")

#text("The most recent saved comparison uses16 policies on524 already exposed development windows from two participants. Action-local support admission corrects16 errors within41 guard-changed windows, with25 error ties and0 local harms. The candidate nevertheless ties local myopic on every paired window, harms39 initially correct windows overall, and has higher macro error-plus-quote loss than strong fixed subset/order controls. No untouched final groups remain. We restore exact preference and support-stratum diagnostics and a prospective failure-inclusive GREEDY denominator contract. This edition performs source synthesis and saved-data arithmetic, with no new fit, inference, acquisition or efficacy experiment.")

= #text("1. Introduction and bounded contributions")

#text("Buying a source, computing a statistic and disclosing it to a decision policy are different events. ProbeFlow starts from that accounting problem and asks a stricter question before adding planning: can a frozen predictor use the permitted information better than a strong affordable fixed or myopic rule? The cumulative application record frequently answers no or insufficient_support. Its later identification theory states what follows from declared missing-outcome and availability assumptions; it does not repair a failed application comparison. [C01-C07]")

#text("Our contributions are bounded: (i) an explicit public-information and charged-attempt contract with preserved negative comparisons; (ii) sharp original-loss bounds and exact pre-observation subset selection under a specified world model, including every primary and transcript tie; (iii) a proof of static terminal reindexing with a common-deadline counterexample; and (iv) a paired descriptive assessment of action-local support admission against its ablation and stronger matched controls. None claims nonmyopic benefit, physical cost savings, population safety or external-method superiority.")

#text("The main paper follows problem, theory, experimental setup and results. Full teaching, assumptions, data admission, EDA, failed executions, proof details and chronological evidence remain in the supplement and55-chapter Korean guide. Every previous body section has one canonical retained location, recorded separately from new synthesis. Edition-specific claims inside historical chapters are dated historical statements; their filenames refer to the frozen source inventory unless the new coverage map supplies a successor.")

= #text("2. Related work and scope of comparison")

#text("Joint active feature acquisition/classification [shim2018] motivates set encoding; generative-surrogate acquisition [li2021,gsmrl-local-primary] models sequential actions, STOP and prediction. Our fixed-subset worst-width design instead selects all queries before readings. Matching a name or set notation does not match the objective or policy class. Chronological action masking in the saved time-series source prevents a general transfer of static order invariance.")

#text("Adaptive-submodularity guarantees [adaptive-submodularity] require structural assumptions not proved here; a stored complementarity witness violates diminishing returns for this worst-width objective. Repeated selection requires evaluation discipline [cawley2010]. Original AO* body/version identity, including the2002/2004 citation conflict, remains unresolved [inherited-author-index]. No native GSMRL/AO* benchmark was reproduced.")

#text("Reference reading is bounded and inherited from the separately saved verifier: official metadata/abstracts and specifically identified GSMRL or Shim opening passages, not full-paper/proof/code reproduction. UCI metadata identify the MHEALTH dataset [uci319], not local physical-axis correctness or clinical validity. The seven reference scope records and exact source hashes remain intact.")

= #text("3. Problem, information rights and objectives")

#text("A prediction actor receives only purchased public values, observation mask and allowed support metadata. The executor tracks attempted versus successful acquisition, quotes and failures; the evaluator alone reads gold labels after decisions. Internal source/cache state and public disclosure are distinct. The current same-process implementation is a cooperative interface, not OS isolation. One logical quote is not measured energy, latency or money.")

#text("Current prediction policies share a frozen mask-aware predictor, first acquired group0, optional actions1..3, one remaining unit quote and total cap2. The primary descriptive objective averages each participant error and quotes first, then weights participants equally with lambda=1/20. All planned subject denominators must be positive. Pooled windows answer a different question.")

#text("The separate identification task fixes subset S before reading guaranteed closed bins. Compatible original worlds give sharp [L(S,z),U(S,z)] for route-minus-static macro loss Delta. Risk is the largest conditional interval width. Select the affordable lexicographic risk/price/mask representative and separately return every affordable primary-risk tie. There is no learned prior over readings and no observation-dependent subset change. [C08,C13-C20]")

#fit-equation[$ J(pi) = (1/P) sum_(s=1)^P (E_s(pi)/n_s + (1/20) C_s(pi)/n_s) $]
#text("E_s and C_s are integer error and attempted-quote totals. P=2,n7=266,n8=258 in the current exposed comparison.")

#fit-equation[$ R(S) = max_z (U(S,z)-L(S,z)), quad sum_(i in S) c_i <= Q $]
#text("This is worst identified width under a hard logical query budget, distinct from expected prediction loss.")

= #text("4. Method and executable decision contract")

#text("At mask1 each feasible optional action has a frozen fitting-leaf mean loss reduction mu and its own support. Admit an action only with at least30 fitting windows from two fitting participants. Select the smallest-index supported action maximizing mu−0.05 if that maximum is strictly positive; otherwise STOP, distinguishing empty support from nonpositive gain. An unsupported alternative does not veto another supported action. The blanket ablation requires every feasible action to be supported before applying the same selection.")

#text("The independently implemented local myopic rule sorts these same net values under identical support, STOP and ties, so it defines exactly the same one-step decision map. Fixed subsets buy their single prescribed optional action when supported, without requiring positive fitted net value. Fixed orders additionally apply the specified multiplier to the positive-net test. All16 current arms share predictor, public input, support rights, unit quotes, cap and524 paired windows. They are a limited fixed-prefix catalogue, not a complete full-budget external comparison.")

#text("For the robust-design branch, traverse feasible readings of each precommitted subset with exact sharp endpoints and strict certified prefix pruning. Shared-cap DP or the proved marginal heap tightens only the outward envelope; it leaves the sharp oracle and all output ties intact. The integrated algorithm and full proof are retained in the supplement. The prospective mask-indexed GREEDY comparator has its own common eligible-window and failed-attempt contract; it was not executed in the current16-arm study.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 13. One-remaining-quote action-local admission")]]
#v(3pt)
#strong[Require] #text("Frozen73-input RF and fold0 conditional trees; public acquired group0 values/mask1; spent1,remaining1,total2,empty cache. Feasible actions1,2,3; per-action fitting leaf counts/participants; quote1,lambda0.05; lower-index tie rule.")
#parbreak()
#strong[Ensure] #text("STOP with empty-support/nonpositive reason, or one supported extra action and a final frozen prediction; complete cost/intent/trace records.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Validate model/input hashes, public mask, dimensions and budget; mismatch fails without a new inference attempt.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Encode only acquired group0 and observation bits; compute the frozen initial prediction.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Look up each feasible action's conditional leaf using public state, retaining its fitting window/participant support and mean.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Build S using each action's own30-window/two-participant predicate; do not veto one supported action because a different action is unsupported.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("If S is empty, STOP insufficient_support. Otherwise select maximum mean minus0.05 with smallest action-index tie; if value<=0 STOP nonpositive.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Before a positive purchase, validate remaining quote/control/time, write intent, copy only the selected local group, debit quote and compute final prediction.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Write and flush the trace, check finalization barrier and preserve all failures/unknown states; do not retry an interrupted accepted path.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compute label-based scores only in the evaluator after selection. Keep full-bank/raw-label audit rights separate and retain myopic equality and stronger static controls.")]])
#v(1.2pt)
]

= #text("5. Theory: conditional guarantees and failure boundaries")

#text("Action-local admission never buys an unsupported action and uses at most one remaining quote. Its fitted incremental value weakly dominates blanket by cases: when all feasible actions are supported they coincide; otherwise blanket contributes0 while local contributes max(0,best supported net). This is a fitted-value statement. It supplies no realized error or population-safety dominance; the observed39 harms demonstrate the distinction.")

#text("For exact design, compatible-world containment gives L(h)<=L(z)<=U(z)<=U(h) for every completed descendant z of prefix h. A completed feasible leaf supplies incumbent b. Prune only when the certified prefix width is strictly below b; equality must be explored to preserve every worst transcript. The shared-cap correction has nonnegative nonincreasing marginal chains; repeatedly taking the largest exposed chain head attains the best at-most-B allocation. It agrees with DP scalar bounds, not a new application result. [C15-C20]")

#text("Static terminal theorem: under immutable unique IDs, a common nonempty world set, the same static per-ID observation relation and fixed subset, ID-preserving tuple reindexing is a bijection with identical feasible worlds and endpoints. Immediate always-successful reveals, common terminal STOP, additive price and no chronology restrictions extend this to cost and terminal prediction. Literal action traces, prefix diagnostics, cache/incumbent behavior and work are not preserved. A two-item common-deadline construction violates the static assumptions and yields0/4 versus4/4 completions, not an algorithm benchmark. [C23-C28]")

#text("The solver remains exponential: all subset/binary-reading pairs total3^N. Heap bounds concern its local allocator, with rational bits and output length separate. Stop-only work, shared child objects versus serialized policy length, full deployment and physical acquisition costs remain unresolved. The non-submodular witness and stronger exact controls prevent a generic greedy or total-cost superiority claim.")

= #text("6. Experimental setup and evidence units")

#text("This edition executes no experiment. It reads frozen documents and saved integer/raw trace rows. Historical hydraulic analyses reuse421 exposed cycles from one rig. HAR, Gas and the original MHEALTH study retain their own splits, losses and support gates; synthetic world calculations stay separate. The historical15-mask MHEALTH bank and current single mask-aware forest are different predictor contracts and must not be pooled.")

#text("The current predictor was fitted in the earlier timed-main study on1098 windows from participants1..4, augmented over16 masks;32 conditional trees used two participant-separated folds. The subsequent studies reuse the same predictor and fold0, with new_fits0. Current DEV comprises participant7 n266 and8 n258, both already exposed. The four locally admitted NPZ arrays for5..8 contain1038 windows and69 features; their existing descriptive EDA is preserved, with raw missingness and physical-axis gaps explicit. [C30-C35]")

#text("Sixteen policies each completed524 paths, so8384 paths are repeated evaluations of524 windows from two people. All planned/started/completed counts agree and failed/partial/unknown/unstarted are0. No fresh independent final groups were acquired. The enlarged pool and changed subset support semantics prevent treating cross-study score changes as an unchanged-policy improvement. No independent-window confidence interval is fabricated.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Units and roles; these denominators are not interchangeable.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Evidence")],[#text("Denominator")],[#text("Scope")]),
[#text("Current policy comparison")],[#text("2 exposed people;524 windows;16 arms")],[#text("Same data/public input/model/quote/cap; paired")],
[#text("Feature EDA")],[#text("4 people;1038 admitted windows")],[#text("Descriptive arrays only; no new final sample")],
[#text("Hydraulic sensitivity")],[#text("1 rig;421 exposed cycles")],[#text("Same two frozen outputs; post-hoc preferences")],
[#text("Static-order witness")],[#text("1 subset;4 conjunctions;8 encodings")],[#text("Constructed exact semantics")],
[#text("Synthetic GREEDY check")],[#text("40960=8×256×4×5 traces")],[#text("Historical interface contract check; not accuracy")])
]

= #text("7. Results: matched baselines and support ablation")

#text("The candidate and local myopic agree on all524 paired decisions and final predictions: no_gain for the proposed one-step rule over its matched myopic control. Action2 is used249 times(P7=114,P8=135), action3 55 times(P7=3,P8=52). The total>=30/two-participant descriptive branch gate passes, but it is not30 per person and the three-window branch remains sparse.")

#text("Against the same-run blanket guard, local admission changes41 purchases(P7=33,P8=8), correcting16 errors with25 error ties and0 harms within that disagreement subset. P8 pays8 additional quotes and gains no corrections. Across the complete candidate-versus-initial-STOP comparison there are80 corrections and39 harms. These comparisons have different denominators;0 local harms is not a whole-policy safety result.")

#text("Exact participant-count reconstruction gives candidate J=0.38352567465174564 versus blanket0.40972416506382237, a descriptive difference−0.026198490412076725. Strong support-gated subset5 has J=0.25111980532727163, and order0,2 multiplier1 has0.3423464183715102. Candidate differences+0.132405869324474 and+0.04117925628023544 are regressions. Same information and acquisition budget make these essential controls; the weaker blanket contrast alone cannot establish method improvement.")

#text("Current improvement verdict: bounded local guard correction observed; matched myopic tie; stronger fixed controls lower loss;39 whole-policy harms; independent-final evidence absent. This is a retrospective paired DEV assessment, not causal sensor utility, confirmatory winner selection or nonmyopic advance.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("full-pool support study saved integer counts and participant-macro objectives; all share the same524 exposed DEV windows.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Policy")],[#text("P7 errors/quotes (n266)")],[#text("P8 errors/quotes (n258)")],[#text("Macro J")]),
[#text("candidate")],[#text("64/383")],[#text("95/445")],[#text("0.383525675")],
[#text("local_myopic")],[#text("64/383")],[#text("95/445")],[#text("0.383525675")],
[#text("legacy_blanket")],[#text("80/350")],[#text("95/437")],[#text("0.409724165")],
[#text("subset_5")],[#text("31/492")],[#text("50/513")],[#text("0.251119805")],
[#text("order_0_2_m1")],[#text("64/382")],[#text("75/421")],[#text("0.342346418")])
]

#figure(image("figures/w47_objective.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Participant-macro error plus0.05×quote on the same524 exposed DEV windows(P7=266,P8=258). Lower is better. Integer numerators are given in the table; candidate=myopic and strong fixed subset/order controls are lower. No uncertainty interval was measured or estimated.")])
= #text("8. Diagnostic results: preferences, strata and failed-purchase denominators")

#text("The older frozen hydraulic secondary contrast exposes a genuine tradeoff: gate-minus-fixed wrong heads−63, complete-diagnosis failures+10 and quotes−324 on421 cycles. With mixed loss ell_alpha=(1−alpha)d/4+alpha v and quote normalization3n, Delta=(-63+103alpha−432lambda)/1684. The exact zero boundary is alpha*=(63+432lambda)/103:63/103 atlambda0,423/515 atlambda1/20, reachingalpha1 atlambda5/54. This is reweighting unchanged policies, not a preference-specific selection experiment.")

#text("The original root min/max partitions39 inside and382 outside cycles. Their signed(head,vector,quote) changes are(-1,+8,-32) and(-62,+2,-292). Thus8/10 complete-diagnosis regressions occur inside range. Min/max membership is not density/joint support or a causal explanation, and evaluator-only label strata cannot become deployment inputs. Full counts and both error partitions are retained in Supplement S53 and Korean chapter54.")

#text("The prospective GREEDY baseline uses the same S-valid eligible windows for every candidate action. Failed j attempts contribute d=0, retain f_S and cost one quote; no nonexistent after-loss is queried. Subject means precede equal-subject averaging, and any planned empty subject makes the whole table not_estimable and forces STOP at a reached state. The9/100 versus20/100 attempt example and1/2 versus1/9 equal-subject example demonstrate why success filtering and pooling can reverse decisions. Its40960 historical synthetic traces check interface rules, not PAMAP2 accuracy or independent efficacy. Full definitions, S/T transition and counterexamples appear in Supplement S54-S55 and Korean chapter55.")

= #text("9. Historical negatives, cost and unresolved comparisons")

#text("The timed-main study completed8 of4152 planned paths, failed the ninth before acquisition and left4143 unstarted; its development tables were not a completed main. The next study completed1800 paths on120 exposed windows but failed its support gate. Later completion and local guard diagnostics do not rewrite either result. Original Gas/MHEALTH routing ties, HAR primary null selection, hydraulic predictor/support failures and partial-identification no_gain cells remain in the full record.")

#text("Current main scope observed215.7763239 wallseconds and64.546875 direct CPUseconds.4806 observed-zero CPU rows are clock quantization, not missing or free work. Per-policy shared preparation charges and residuals are accounting scenarios, not repeated physical preparations. Historical heap/DP endpoint, CPU, traced-memory and output measurements have different scopes; equal risk/full ties and strong sharp-prefix controls prevent calling isolated operation-count reductions total-cost gains. [C20,C30-C35]")

#text("Thirty-four incompatible full-budget controls remain unexecuted, not scored zero. Physical acquisition/failure/energy/latency, independent group utility, historical fitting amortization, full deployment/transient memory and original external-method version/code comparisons remain unmeasured. These gaps constrain efficacy and cost claims even when local arithmetic, hashes or document rendering pass.")

= #text("10. Limitations and conclusion")

#text("The evidence comprises exposed local prediction cohorts, declared mathematical world models and finite constructed witnesses. It supplies neither an untouched confirmatory population nor measured physical acquisition utility. Support thresholds are admission counts, not calibrated guarantees. Preference and root-range analyses are post-hoc diagnostics. New source coverage, check counts, page counts and theorem exactness do not turn them into practical improvement.")

#text("ProbeFlow currently contributes explicit information/attempt accounting, preserved negative comparisons, sharp assumption-dependent identification and exact fixed-subset design with full ties. Action-local admission improves one blanket-guard contrast locally, while matched myopic ties and stronger fixed-policy regressions remain decisive. A next application claim requires independently frozen groups, prespecified utility, real failure/delay/cost receipts and the strongest feasible controls under common data, public information, tuning and acquisition budgets. Scientific status remains needs_evidence; scientific certification, gate closure, promotion and submission are false.")

= #text("11. Reproducibility and reporting checklist")

#text("Claims and limitations: bounded contributions, negative findings, harms, denominators and missing independent final are stated above. Theory: assumptions and detailed proofs are retained in the supplement. Experimental reproducibility: frozen source hashes, integer counts, public-information contracts and original failure records are linked; this edition adds arithmetic checks only, without executing research code. Statistical uncertainty: no independent-window confidence interval or new population estimate is claimed.")

#text("Resources and ethics scope: logical quotes, measured CPU/wall scopes and missing full costs remain separate. Existing licensed-source reading scopes are preserved; no new dataset or participant information is acquired. Code, frozen-model/source and policy identities are supplied by hash; authoring tokens/cost and physical acquisition remain unmeasured. This reporting checklist is an editorial disclosure, not a claim that an official conference checklist, nine-page limit, anonymous review, author identity, submission or LaTeX compliance has passed.")

#text("The reading PDFs are to be produced with the pinned existing Typst builder by a separate integration Task. The earlier PATH-only compiler search was incomplete: integration located an existing Tectonic0.17.0 executable. Official-style preprint LaTeX source remains preparatory here; author compilation and venue compliance are unverified. Integration will test the existing cache without network downloads. Separate independent semantic review, actual full-book compilation, per-PDF size/page measurements and all-page visual review remain required before publication.")

= #text("Question, contribution and evidence status")

#text("The question is whether incomplete-log identification sets preserve contextual acquisition gains against strong fixed strategies, and whether risk correction changes the error/cost/harm of a frozen predictor on already exposed development participants. This study implements an actual log→joint completion set→full-policy contrast→gate chain and a separate frozen-forest DEV arm.")

#text("The bounded execution and alternative raw-only oracle completed once. Scientific status is needs_evidence. Controlled comparisons have a failure-abstain fixed-control omission; they cannot establish superiority to all eligible static strategies. DEV is two previously used participants, not independent application confirmation.")

= #text("Information, architecture and trust boundary")

#text("Controlled logging, set construction, fixed policy evaluation and evaluator-only truth are separate functions. H is paid equally before selection; one shared potential world determines both policies and query failures. Full trees are frozen before calibration, and a single completion parameter is used across all branches and both policies.")

#text("DEV reuses only the portable48-tree forest, source-hashed standard-library NPZ/forest semantics and W48 tokens/thresholds. No parent module, main, pickle or lifecycle is imported. Selector access is cooperative within one process: hidden labels/features and evaluator cache are not passed to it, but no OS security isolation is claimed.")

= #text("Algorithm and validity conditions")

#text("Four known mixture designs generate coarsened labels with independent MCAR retention3/4. Conditional on independent retained Bernoulli samples, Hoeffding union bounds induce one nonrectangular set with four coordinates and at most16 constraints. Unknown coordinates remain ranges; empty/unsupported conditions fall back to reference. The PRNG run illustrates the declared model and does not estimate population coverage.")

#text("Exact rational active-set enumeration gives sharp affine paired-loss intervals over this bounded set. Literal per-context lower gating and coupled global minimax enumeration are distinct. No branch-wise nature reselection or post-calibration continuation change occurs.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 14. Log-derived shared-completion certificate for frozen whole policies")]]
#v(3pt)
#strong[Require] #text("Train-only reference and at most32 complete nonanticipating policy trees Independent calibration logs with known mixture and MCAR assumptions; common8-world K Initial paid context, failure/abstain/cost contract and remaining attempt budget")
#parbreak()
#strong[Ensure] #text("Sharp conditional paired terminal-loss intervals and literal gate or reference fallback Same-world terminal metrics, explicit unsupported/empty/failure and limitations")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Freeze all whole trees and reference using train only; never give evaluator theta to interval/gate functions.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Read each calibration outcome/missing event and count retained labels per known mixture design.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Intersect simultaneous Bernoulli mean bounds with the four-coordinate unit box; leave unobserved ranges free.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Enumerate exact feasible vertices, compute full terminal-loss contrasts in the same potential worlds and optimize each affine contrast over that one set.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("At supported context choose the largest lower contrast, reference first on ties; return reference on unsupported or empty sets.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Execute the selected frozen tree through observed tokens/failures only, charging every attempt and initial context. Do not replan its continuation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compare literal gate with a separately enumerated coupled root optimum and retain gain/no_gain/regression and coverage failures.")]])
#v(1.2pt)
]

= #text("Conditional guarantee and its limits")

#text("For Delta_j(h)=E[L_b-L_j|h], the good simultaneous-containment event gives J_gate<=J_b and J_gate-min_j J_j<=B-A. A is the contextual oracle gap over the complete frozen menu; B averages the true best contrast width on supported contexts and M on unsupported ones. A/B use evaluator truth and are posthoc explanatory quantities, not gate inputs.")

#text("Let D=E_H[max_j Delta_j-Delta_gate]. Bounded terminal losses imply0<=D<=M=23/20 on all events and D<=B on the good event. Thus expected baseline regret is at most delta*M and expected menu regret is at most E[B-A]+delta*M under the stated sampling assumptions. These elementary bounds do not establish novelty, arbitrary-MNAR/OOD safety or DEV calibration.")

= #text("Controlled observations and comparator failure")

#text("The main stores all1024 complete potential-world terminal records and eight log-derived sets. Narrow/wide true containment, unsupported fallback, inconsistent empty sets and literal/global values pass the alternative exact check. All main conservatism gaps are0; a synthetic unit case separately has gap1/2. A=0 in these menus because they already include contextual trees; this is not an empirical proof that adaptation has no value.")

#text("Recorded narrow contextual gain against the declared fixed list is0.075; narrow static-sufficient gain is0.025. Inspection reveals the latter gate is q1_abstainF in both contexts, itself a fixed-order strategy omitted from reference selection. This is a comparator-design failure, preserved in INCIDENTS and CONTROLLED_DIAGNOSTICS. Positive numbers are not promoted to a strongest-static result.")

#text("Predeclared flipped-theta diagnostics remain better than reference and therefore did not supply the intended harmful example. Separate posthoc algebra of stored affines at theta=(0,0,0,0), outside narrow sets, yields gate-minus-reference regret0.05 contextual and0.10 static-sufficient. This is a mathematical counterexample derived after the run, not a replay or predeclared experimental success.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Predeclared comparisons as recorded. Fixed-control omission prevents interpreting positive values as superiority to every eligible static strategy.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Mechanism")],[#text("Case")],[#text("Truth in C")],[#text("Gate gain vs declared fixed")],[#text("Scientific interpretation")]),
[#text("contextual")],[#text("narrow")],[#text("True")],[#text("0.075")],[#text("baseline gap; preserve raw gain")],
[#text("contextual")],[#text("wide")],[#text("True")],[#text("0.05")],[#text("baseline gap; preserve raw gain")],
[#text("contextual")],[#text("unsupported")],[#text("True")],[#text("0.0")],[#text("baseline gap; preserve raw no_gain")],
[#text("contextual")],[#text("inconsistent")],[#text("False")],[#text("0.0")],[#text("baseline gap; preserve raw no_gain")],
[#text("static_sufficient")],[#text("narrow")],[#text("True")],[#text("0.025")],[#text("baseline gap; preserve raw gain")],
[#text("static_sufficient")],[#text("wide")],[#text("True")],[#text("0.0")],[#text("baseline gap; preserve raw no_gain")],
[#text("static_sufficient")],[#text("unsupported")],[#text("True")],[#text("0.0")],[#text("baseline gap; preserve raw no_gain")],
[#text("static_sufficient")],[#text("inconsistent")],[#text("False")],[#text("0.0")],[#text("baseline gap; preserve raw no_gain")])
]

= #text("Exploratory DEV results: estimator and adaptivity separated")

#text("Tau64 minimizes the declared C-fold score. Empirical Bellman and myopic have identical DEV paths and macro J=0.302104097. Calibrated Bellman has J=0.245246109; calibrated myopic has J=0.308091450 with305 different paths. Both C-selected fixed references happen to be initial STOP, J=0.431884945.")

#text("The best recorded fixed strategy on DEV is descriptive committed_order_02/subset5, J=0.251293933. Calibrated Bellman is lower by0.006047823; this is an exposed two-person observation, not a selected deployment guarantee. Committed subset/order behavior is unchanged across estimators; Bellman changes while myopic slightly regresses. Risk correction and planning interact rather than showing a universal estimator gain.")

#text("Against the descriptive best fixed strategy the calibrated candidate has45 corrections and42 harms. Failed/unknown/unstarted paths are0; coverage1 and abstention0 are observed under this no-provider-failure DEV arm. These do not establish safety.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Exposed DEV, two participants and524 unique windows. Same T-derived support for all methods; reference selected on C. Hindsight controls are descriptive.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Estimator")],[#text("Policy")],[#text("Macro error")],[#text("Mean quote")],[#text("Macro J")]),
[#text("empirical")],[#text("bellman")],[#text("0.202104")],[#text("2.0")],[#text("0.302104")],
[#text("empirical")],[#text("myopic")],[#text("0.202104")],[#text("2.0")],[#text("0.302104")],
[#text("empirical")],[#text("selected_reference")],[#text("0.381885")],[#text("1.0")],[#text("0.431885")],
[#text("empirical")],[#text("subset_5")],[#text("0.151294")],[#text("2.0")],[#text("0.251294")],
[#text("empirical")],[#text("subset_13")],[#text("0.153232")],[#text("2.308562")],[#text("0.26866")],
[#text("calibrated")],[#text("bellman")],[#text("0.144839")],[#text("2.008145")],[#text("0.245246")],
[#text("calibrated")],[#text("myopic")],[#text("0.215145")],[#text("1.858921")],[#text("0.308091")],
[#text("calibrated")],[#text("selected_reference")],[#text("0.381885")],[#text("1.0")],[#text("0.431885")],
[#text("calibrated")],[#text("subset_5")],[#text("0.151294")],[#text("2.0")],[#text("0.251294")],
[#text("calibrated")],[#text("subset_13")],[#text("0.153232")],[#text("2.308562")],[#text("0.26866")])
]

= #text("Complexity, cost and remaining scope")

#text("For general d,m,H,K,W, active-set enumeration uses O(binomial(m,d)*(d^3+md)) rational operations and coupled root selection O(K^H*HV) after V vertices are found. Bit lengths depend on rational input/pivots; word counts do not imply bit or polynomial general-policy complexity. This run is only d4,m<=16,H2,K<=32,W8. DERIVATION gives assumptions, memory and DEV forest/state costs.")

#text("Measured arm-body wall/directCPU seconds are controlled2.074605/1.562500 and DEV3.654179/2.390625. Preparation, calibration, selection, prediction, recording and raw-only verification costs remain separate. Shared preparation/cache is one physical construction with equal accounting rights; it is not sixty refits or a speedup claim.")

#text("Model API calls0, new predictor fits0, native episodes0 and no skill activation. SOL authoring usage, historical fitting, installed-module traffic, transient/peak memory, physical sensor/IO/energy, shell/Orca/reporting tails and full deployment cost are unmeasured. Exact external-method/primary-version overlap and independent data remain open. Parent W48 no_gain/static regressions and earlier failures are preserved.")

= #text("Frozen identities, lineage and execution order")

#text("TASK SHA256=9ec097fa8de1cb80a4a3761cb105206c83878583302ed6107c86da424df983ca. Parent RESULT=f91fd7df005062b775e8306e5032118dbfac595d9d77ca7d6e863d2ab7e38b40; exact WAVE parent path/hash is copied unchanged into RESULT and SOURCE_HASHES. Fifty-two input/source records were verified before experiments.")

#text("Historical controller source drift is kept alongside additive coordinator prelaunch evidence. POLICY, METHOD contract, reviewer and builder hashes match at start/checkpoint/end. Commands prepare, smoke, unit, seal, main and oracle each ran once with recorded interpreter flags, OS command line, PIDs, stdout/stderr and exits. Four smoke checks and nine unit checks are readiness evidence only; no experimental replay occurred.")

= #text("Complete controlled procedure and log events")

#text("For each mechanism, train logs use1024 events per design with seed101 or102. Calibration narrow uses4096 per design; wide16; unsupported omits design3; inconsistent uses incompatible deterministic labels. Every original event is retained as an indexed0/1/M character with design weights, observed/positive/missing counts. Hidden mixture component is deliberately absent from the logging interface.")

#text("Train mixture means solve theta0=m0,theta2=m1,theta1=2m2-theta0,theta3=2m3-theta1 with clipping. Twenty conditional tree forms are paired over two contexts, all mandatory controls retained and train-ranked pairs fill at most32 frozen whole policies. This is a finite author-defined menu, not all conceivable policies.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 15. Log-derived shared-completion certificate for frozen whole policies")]]
#v(3pt)
#strong[Require] #text("Train-only reference and at most32 complete nonanticipating policy trees Independent calibration logs with known mixture and MCAR assumptions; common8-world K Initial paid context, failure/abstain/cost contract and remaining attempt budget")
#parbreak()
#strong[Ensure] #text("Sharp conditional paired terminal-loss intervals and literal gate or reference fallback Same-world terminal metrics, explicit unsupported/empty/failure and limitations")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Freeze all whole trees and reference using train only; never give evaluator theta to interval/gate functions.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Read each calibration outcome/missing event and count retained labels per known mixture design.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Intersect simultaneous Bernoulli mean bounds with the four-coordinate unit box; leave unobserved ranges free.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Enumerate exact feasible vertices, compute full terminal-loss contrasts in the same potential worlds and optimize each affine contrast over that one set.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("At supported context choose the largest lower contrast, reference first on ties; return reference on unsupported or empty sets.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Execute the selected frozen tree through observed tokens/failures only, charging every attempt and initial context. Do not replan its continuation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compare literal gate with a separately enumerated coupled root optimum and retain gain/no_gain/regression and coverage failures.")]])
#v(1.2pt)
]

= #text("Failure law, classifier and matching limits")

#text("Action1 fails when F1/B0, action2 when F1/A0. Failed attempts cost one quote and consume budget, emit F and may be followed only by the other action. Initial context quote1 and at most two extra attempts enter total loss. Classifier predicts the observed relevant token or0; abstain costs0.4. Both compared policies use the same V and Y law, not independent worst worlds.")

#text("The declared fixed catalogue has STOP, abstain, one-query and both orders plus train-value-gated order controls. It omitted the failure-abstain variants in fixed_ids/reference selection even though they were permitted whole-menu trees. That omission invalidates the promised exhaustive strongest-static interpretation. In static-sufficient narrow, the gate is the identical q1_abstainF tree in both contexts. All original values and selection are unchanged; a new Task is needed for a corrected preregistered comparison.")

= #text("From counts to one set and exact endpoints")

#text("For each nonempty design, eps=ceil(10^6*sqrt(log160/(2n)))/10^6, delta0.05. Intersect0<=theta_k<=1 with max(0,e/n-eps)<=a_g theta<=min(1,e/n+eps). n0 leaves the design unconstrained. This derives one joint set from logs, never a risk interval supplied by evaluator truth.")

#text("Main Gaussian elimination enumerates active four-constraint systems and checks feasibility against every inequality. Raw-only oracle independently uses determinant/Cramer completion points. Nonempty vertex counts are contextual20/24/20 and static-sufficient24/24/20 for narrow/wide/unsupported; inconsistent has0 each. Each case checks64 conditional intervals; total512 slots include empty-case null endpoints. Every recorded extremizer and literal/global selection matches.")

= #text("Proof, selection validity and counterexamples")

#text("Condition on train-selected reference/menu and independent calibration retention counts. IID Bernoulli sampling with known coarsening and MCAR permits simultaneous mixture-mean coverage by union bound. Containment implies all affine whole-policy contrasts are covered simultaneously even after selecting by those intervals. Unknown logging weights, informative missingness, learned K, non-IID calibration or changed predictor invalidate this argument.")

#text("DERIVATION gives Delta,ell,u,A,B,D and the good/failure-event algebra. The fixed-menu minimum includes contextual complete policies and must not be relabeled minimum fixed acquisition order. A0 in all recorded menus is explicitly preserved. Width-only chooses reference because reference contrast width is0; this ablation is therefore trivial no_gain rather than evidence for useful uncertainty minimization.")

#text("The supplied branch-coupled unit construction establishes only that literal gate can be strictly more conservative than the coupled optimizer. All actual main gaps are0. The prerecorded flipped truth produced negative regret, while posthoc stored-affine all-zero truth produced positive regret. Both are retained with different evidentiary status; no unconditional safety is claimed.")

= #text("DEV data admission and exact predictor semantics")

#text("All MHEALTH1..10 have use records. Predictor-fit metadata reports people1..4,1098 windows and17568 augmented rows; this run fits nothing and does not authenticate historical training. Frozen5/6 provide514 cached rows. Split ((index//8)%5)<3 givesT168+154=322,C96+96=192. No subject9/10 payload is opened.")

#text("Only portable48-tree probability export is used. Standardization preserves observed feature blocks, missing entries remain0, presence columns69..72 mark acquired blocks; then float32 rounding precedes threshold comparisons. Normalize each leaf probability and sum scores in original tree order; ties choose first class. All3598 actual5/6 predictions match cached labels before DEV; these checks do not independently authenticate original pickle/export training.")

= #text("DEV calibration, support and full policy catalogue")

#text("Empirical risk is eT/nT with emptyT1/2 and unsupported status. Calibrated risk is(eC+tau*rT)/(nC+tau), with emptyC prior fallback even at tau0. C folds alternate(index//8)%2, fitting the other fold and scoring each held-out row at all7 masks. Tau0/16/64 are scored with participant-macro Brier; larger tau wins exact ties. CV stores every fold count/fallback and selects64.")

#text("Every current state and all positive-probability T successors must have30 windows and both5/6. Policies share this rule and total3quotes. Static masks1,3,5,9,7,11,13; ten orders0,01,02,03,012,013,021,023,031,032 as committed and value-gated forms; myopic and depth-two plus duplicate selected_reference give30 per estimator. Eight subsets and31 order skeletons incompatible with already acquired0 are not executed or counted as provider failures.")

#text("All27 fixed strategies are scored by actual C terminal error+quotes/20 and participant macro; lexical ties choose the reference. C also enters calibrated risks, so selection reuses calibration and has no independent guarantee. SELECTION and its SHA256 are persisted before7/8 load. Calibrated risk with T transition frequencies need not be a coherent joint posterior: planning optimality is only for its stated surrogate.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 16. Frozen predictor, matched estimators and single exposed DEV opening")]]
#v(3pt)
#strong[Require] #text("W48 portable forest and frozen5/6/7/8 arrays with exact hashes T322/C192 split, tau candidates0/16/64, identical support30/two-person rule and total3quote budget")
#parbreak()
#strong[Ensure] #text("SELECTION frozen before DEV, sixty policy tables and31440 terminal records Per-person/macro errors, quotes, losses, correction/harm and explicit failure denominators")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Decode5/6 and check all3598 cached predictions using float32/leaf-normalization/first-class tie semantics.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Compute T state risks and transitions; score shrinkage tau on two C time-block folds using participant-macro Brier.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Freeze empirical and calibrated tables; score all27 fixed controls per estimator on C and select a reference with lexical ties.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Write SELECTION bytes/hash before opening7/8; fixed-order, myopic and depth-two policies share information/support/output/cost rights.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Open exposed DEV once; evaluator builds3668 predictions. The selector reads acquired tokens, frozen tables and budget only.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Record every path, aggregate two participant means, and separate estimator changes from adaptive-versus-fixed differences.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("Audit saved rows with a separate implementation; do not rerun prediction, retune using DEV or call it an independent final test.")]])
#v(1.2pt)
]

= #text("DEV evaluation, pairs, harms and negative results")

#text("Subject7 has266 unique windows and8 has258. Seven evaluator predictions per window yield3668 unique DEV inferences. Selector is given its acquired token history/frozen tables/budget; evaluator owns full arrays, label and all-mask cache. All60 configurations execute on the same524 windows, rotating policy order;31440 paths are repeated policy evaluations, not independent units.")

#text("Calibrated Bellman errors/quotes are7:42/492,8:34/559. Per-person and macro rates are in SUMMARY. Initial-STOP corrections/harms are7:56/0,8:72/4. Corrections do not erase harms.")

#text("Empirical Bellman=myopic/no_gain persists within that estimator. Calibrated Bellman differs from myopic on305 paths; matched estimator effect improves Bellman but worsens myopic. Committed strategy predictions/costs remain identical across estimators. Every policy score and fallback is preserved, including strategies worse than references. static13 is reported descriptively, never selected using DEV or renamed train-reference.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Exposed DEV, two participants and524 unique windows. Same T-derived support for all methods; reference selected on C. Hindsight controls are descriptive.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Estimator")],[#text("Policy")],[#text("Macro error")],[#text("Mean quote")],[#text("Macro J")]),
[#text("empirical")],[#text("bellman")],[#text("0.202104")],[#text("2.0")],[#text("0.302104")],
[#text("empirical")],[#text("myopic")],[#text("0.202104")],[#text("2.0")],[#text("0.302104")],
[#text("empirical")],[#text("selected_reference")],[#text("0.381885")],[#text("1.0")],[#text("0.431885")],
[#text("empirical")],[#text("subset_5")],[#text("0.151294")],[#text("2.0")],[#text("0.251294")],
[#text("empirical")],[#text("subset_13")],[#text("0.153232")],[#text("2.308562")],[#text("0.26866")],
[#text("calibrated")],[#text("bellman")],[#text("0.144839")],[#text("2.008145")],[#text("0.245246")],
[#text("calibrated")],[#text("myopic")],[#text("0.215145")],[#text("1.858921")],[#text("0.308091")],
[#text("calibrated")],[#text("selected_reference")],[#text("0.381885")],[#text("1.0")],[#text("0.431885")],
[#text("calibrated")],[#text("subset_5")],[#text("0.151294")],[#text("2.0")],[#text("0.251294")],
[#text("calibrated")],[#text("subset_13")],[#text("0.153232")],[#text("2.308562")],[#text("0.26866")])
]

= #text("Raw-only oracle and denominators")

#text("Main and oracle stages run once. Oracle reconstructs1024 controlled terminal affines and all512 interval slots, literal gates, coupled global values and A/B/D separately. For DEV it checks3598 equivalence records, split, tau selection,38 states per estimator, all60 decision tables, C references,31440 final paths and per-person/macro/paired arithmetic. It does not reopen DEV, infer the forest again or import author experiment functions.")

#text("Main controlled has10 planned/completed case records, including diagnostic empty/outside states; DEV has31440 planned/started/completed, failed0,unknown0,unstarted0. Failed query mass in controlled is an observed paid outcome rather than an execution failure. Preparation incidents and comparator/diagnostic failures are retained separately. Scientific interpretation remains needs_evidence despite exit0.")

= #text("Costs, bytes, computational scope and omissions")

#text("COST_ACCOUNTING reconciles each measured arm total with disjoint named phases plus residual. DEV paths/recording are one combined measured phase, not isolated provider/selection/serialization clocks. The same common preparation/prediction cache is charged identically in an accounting scenario to all policies; actual work is not multiplied by60. No policy-specific runtime speedup is claimed.")

#text("General vertex enumeration and root-combination complexity are exponential in variable dimension/context count; exact rational bit size and output storage matter. DEV uses a finite token state table but state growth is exponential in blocks. Original input bytes, explicit repeated reads, raw output bytes and conservative4MiB interactive-read allowance are distinguished. Installed-module traffic, physical reads/energy, peak/transient memory, historical fit and final launcher/reporting tails stay null.")

#text("The CPU/wall limits are cooperative, not OS security isolation or hard deadlines. No new dependency, account, model, API, download, worker, scheduler, service or global/active skill change occurred. Authoring model usage is unmetered and cannot be inferred from experiment model_api_calls0.")

= #text("Related work and release boundary")

#text("The required diagnosis, data-admission and inherited primary-read records are copied and hashed. Their metadata and attributed proposal notes are not freshly verified primary passages or reproduced external methods. Existing robust baseline regret/fallback overlap and an unresolved closest-overlap lead remain open; no novelty or conference-readiness claim follows.")

#text("Only existing build_documents.validate is called for literal manuscript schema; no rendering, PDF, METHOD, VERIFICATION, INTAKE, AOP, publication, Git push or global skill activation is performed. Coordinator owns independent review and subsequent intake. Parent results and all old research runs remain unchanged.")

= #text("문제와 이번 기여")

#text("W49의 static-sufficient +1/40은 정적 failure-abstain 정책 누락 때문에 적응 이익으로 해석할 수 없었다. W50은 고정된 acquisition 순서에도 관측별 STOP·abstain 권리를 모두 주고, 문맥 적응과 추정기 변경을 교차 대조하도록 사전 계약을 고정했다.")

#text("이번 기여는 순서 제약과 종료 규칙을 분리한 완전 정책 문법 및 정확한 분해 최적화다. 새 controlled 계산은 완료했으나 DEV 연결과 원시 검산이 실패했다. 과학 상태는 failed이며 실제 응용의 추정기 효과 분리는 미완료다.")

= #text("알고리즘·정보와 정당성")

#text("고정 순서는 H와 무관하게 공유된다. 그 순서 안의 STOP·abstain은 H와 모든 획득 이력에 의존할 수 있다. 따라서 같은 공개 정보와 실패 권리를 주면서 acquisition 순서의 적응성만 제한한다. 다음 query의 성공 여부나 숨은 값을 먼저 보는 정책은 허용하지 않는다.")

#text("같은 첫 순서에서 마지막 STOP/A 선택2개, 그 전 이력에서는 STOP/A 또는 두 번째 query의8개 종료 지도로10개 선택이 있다. 첫 query의 세 관측 가지를 합치면1002나무다. 두 H의 같은 순서 정책 공간은 중복4개를 빼2008004개이며, H별 첫 순서도 다른 전체 공간은4008004개다. 역방향 최소화는 이 문법의 모든 결정적 정책을 포함한다. 혼합 정책은 동일 선형 목적함수에서 더 작은 값을 만들지 않는다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 17. 동일 종료 권리의 전체 고정 순서 대조")]]
#v(3pt)
#strong[Require] #text("고정 predictor, 알려진 공통 세계/실패 법칙, T/C 위험 추정값 전역 고정 순서 문법과 공개 H·획득 이력 초기 quote1, 추가 시도2, 실패 과금, abstain 손실2/5")
#parbreak()
#strong[Ensure] #text("전체 적격 정적 정책 중 추정 목적함수 최소 reference 문맥 적응·근시안·하한 gate와 같은 세계의 비교 기록 미지원은 STOP/reference, 실행 실패는 실패 영수증과 미실행 분모")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("고정 순서마다 모든 관측0/1/F의 STOP·abstain·다음 query 가지를 정의한다. 숨은 센서와 정답은 selector에 주지 않는다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("각 마지막 이력에서 STOP과 abstain의 위험을 비교한다. 역순으로 query의 비용과 후속 위험을 합산해 모든 종료 규칙을 최적화한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("순서는 모든 H에 공유하고 종료 규칙은 H/이력에 반응하도록 허용한다. 짧은 subset은 긴 순서의 조기 종료로 표현한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("동일 추정기에서 고정 순서들의 평균 추정 J를 최소화하여 reference를 고른다. 적응 정책은 H별 첫 행동도 선택한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("calibration 직사각형 네 꼭짓점에서 같은 세계의 reference 대조 손실 하한을 구한다. 동률·미지원은 reference를 유지한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("선택을 동결하고 평가 전용 참값/예측 자료로 비용·오류·보류·교정·피해를 기록한다. 실패 시 재실행하지 않는다.")]])
#v(1.2pt)
]

= #text("직접 관측: static 동률, contextual 비용 차이")

#text("두 추정기 모두 static-sufficient에서 reference와 적응 정책의 나무가 완전히 같고 J=33/160, 이득0이다. 누락된 실패 보류를 채운 정적 대조가 이전 가짜 적응 이득을 제거하는 방향과 일치한다. 다른 모형의 새 결과이며 W49 숫자를 소급 정정하지 않는다.")

#text("contextual에서는 reference J=35/160, 적응과 근시안 모두33/160으로 차이1/80이다. 초기 quote를 포함한 평균 quote가5/2에서9/4로 줄고 coverage7/8은 같다. 점 추정기 변경으로 선택과 J가 바뀌지 않아 controlled estimator effect=0이며 유한지평이 근시안보다 낫다는 근거도 없다.")

#text("통제의 사람별 결과 대신 두 선언 문맥별 오류·J·quote·coverage 및 짝지은 교정/피해를 기록했다. 같은 참가자로 해석하지 않는다. 완전 terminal 지표의 oracle는 부동소수점 오류율 표현에서 멈췄으므로 전체 검산 통과로 쓰지 않는다.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("단회 controlled 원시 기록. 정책 최적값 대조는 검산 prefix에 포함되지만 전체 terminal 지표 검산은 실패했다.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("구조")],[#text("추정기")],[#text("고정 reference J")],[#text("적응 J")],[#text("근시안 J")],[#text("적응 이득")],[#text("기록 상태")]),
[#text("static_suffi​cient")],[#text("empirical")],[#text("33/160")],[#text("33/160")],[#text("33/160")],[#text("0")],[#text("no_gain")],
[#text("static_suffi​cient")],[#text("calibrated")],[#text("33/160")],[#text("33/160")],[#text("33/160")],[#text("0")],[#text("no_gain")],
[#text("contextual")],[#text("empirical")],[#text("7/32")],[#text("33/160")],[#text("33/160")],[#text("1/80")],[#text("gain")],
[#text("contextual")],[#text("calibrated")],[#text("7/32")],[#text("33/160")],[#text("33/160")],[#text("1/80")],[#text("gain")])
]

= #text("실패와 미실행이 결론에 미치는 영향")

#text("본실험은 DEV 선택 metadata에서 mask15의 예측을 찾다 KeyError로 끝났다. 네 센서가 모두 있는 mask15는 추가 구매2회 계약 밖이며 저장 일곱 mask 예측에도 없다. 선택표 동결·DEV bank 읽기·사람별 비교·경로12576개는 수행되지 않았다.")

#text("별도 raw-only oracle는16032개 열거 점수와 최소값/reference/certificate 대조 prefix를 지난 뒤 exact7/160과 binary-float 저장값의 불일치로 실패했다. 두 오류 모두 unit smoke가 다루지 못한 실제 경계다. 미래 수정안을 이 봉인 실행의 성공으로 계산하지 않는다.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("실제 실행·검산·미실행을 구별한다. 표본 수는 정책/검사 수가 아니다.")]]
#v(4pt)
#table(columns: (2fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("대상")],[#text("계획")],[#text("시작")],[#text("완료")],[#text("실패")],[#text("미실행")]),
[#text("command_stages")],[#text("6")],[#text("6")],[#text("4")],[#text("2")],[#text("0")],
[#text("main_arms")],[#text("2")],[#text("2")],[#text("1")],[#text("1")],[#text("0")],
[#text("oracle_arms")],[#text("2")],[#text("2")],[#text("0")],[#text("2")],[#text("0")],
[#text("controlled_cases")],[#text("8")],[#text("8")],[#text("8")],[#text("0")],[#text("0")],
[#text("controlled_cases_fully_verified")],[#text("8")],[#text("1")],[#text("0")],[#text("1")],[#text("7")],
[#text("DEV_selection")],[#text("1")],[#text("1")],[#text("0")],[#text("1")],[#text("0")],
[#text("DEV_paths")],[#text("12576")],[#text("0")],[#text("0")],[#text("0")],[#text("12576")],
[#text("DEV_policy_tables")],[#text("24")],[#text("0")],[#text("0")],[#text("0")],[#text("24")])
]

= #text("조건부 인증, 복잡도와 주장 한계")

#text("새 인증은 두 token별 Bernoulli calibration 표본의 Hoeffding 구간을 함께 만족하는 직사각형을 쓴다. 참값이 안에 있고 알려진 공통 세계가 맞으면 모든 전체 정책의 affine 대조가 동시에 포함된다. reference와 정책이 C에 의존해도 이 uniform 포함 아래 하한 gate의 reference 대비 비악화가 따른다. 한 seed의 참값 포함은 population coverage 실측이 아니다.")

#text("일반 고정 순서 B단계의 syntactic 나무 수는 T0=2, T_b=2+(T_{b-1})^r로 빠르게 증가한다. explicit 공통 세계 N개와 충분 상태 S개가 주어질 때 DP는 각 상태·행동·세계의 유리수 계산과 저장을 요구한다. S 자체가 관측 수/차원에 지수적으로 늘 수 있고 bit 길이와 실제 파일 byte를 별도 비용으로 센다.")

#text("본실험 exit1·oracle exit1을 보존하며 science_status=failed다. 완결된 실패 보고는 태스크의 완료와 구별한다. 봉인 후 코드·계약·입력을 수정하거나 재실행하지 않았다.")

#text("통제 모형은 W49의 네 좌표 혼합로그 공동-polytope와 다르다. H 사이에 공유되는 두 label 확률, 알려진8세계와 직접 iid Bernoulli label 표본을 가정한다. 이 단순화는 정적 종료 권리라는 이번 질문을 분리하기 위한 것이며 W49의 보장·신규성·응용 결과를 상속하지 않는다.")

#text("모든 MHEALTH1..10은 과거 사용됐다. 계획 DEV는 노출7/8의2명·524고유창이며 이번 평가 완료는0명/0창, 독립 final-test는0명이다. 정책경로·합성세계·검사 수를 사람 또는 독립 표본 수로 세지 않는다.")

#text("신규 외부 원문 읽기0이며 closest prior-art overlap, 정확한 판본/가정/재현과 신규성은 미해결이다. 상속 metadata나 독립 검토자의 동의를 사실/과학 인증으로 바꾸지 않는다.")

#text("quote는 논리 비용이다. 센서 I/O·전력·물리 속도·provider 실패율·population coverage·MNAR/OOD 안전은 검증하지 않았다. 실험 model_api_calls=0/native_episodes=0과 SOL 저술 사용량 미계측을 구별한다.")

= #text("사전 계약·출처·단회 위상")

#text("TASK 해시379543ef3048eb0bc49742f4eba7ff28265b636294f8d9130d4d37b360062fb9와 사전 evaluation_contract를 고정했다. TASK parents5개, latest METHOD2개, task builder 및 source pins를 시작 시 실제 bytes로 비교했다. WAVE의 parent RESULT 경로/hash와 정확히 같은 parent를 유지한다.")

#text("prepare→smoke4→unit10→seal→main1→oracle1을 실행했다. prepare/smoke/unit/seal exit0, main/oracle exit1이다. 실패한 stage는 다시 실행하지 않았다. commands의 START/command/exit/log hash가 실제 실행 근거이며 shell 대화나 저술을 별도 과학 episode로 만들지 않는다.")

#text("초기 schema 확인에서 부모의 DEV 첫1행을 이미 보았다. 이 자료는 원래부터 공개된 DEV이며 새로운 독립 holdout이라고 부르지 않는다. 본 main에서는 선택 실패로 DEV bank를 열지 않았다. 이 구분은 EXPERIMENT_INCIDENTS와4MiB 사전읽기 예약에 남긴다.")

= #text("정적 정책 완전성의 유도")

#text("적격 정책은 H를 받은 뒤 STOP/A 또는 지정 순서의 첫 query를 택한다. query가 반환한0/1/F마다 STOP/A 또는 순서의 다음 query를 택하고, 마지막 query의 세 결과마다 STOP/A를 택한다. 실패도 quote/시도를 소비하고 같은 action을 반복하지 않는다. 성공 뒤 abstain과 두 번째 실패 뒤 abstain도 빠지지 않는다.")

#text("순서[1]은[1,2]에서 첫 query 뒤 모두 terminal인 나무로, 빈 순서는 두 maximal-order 문법의 root terminal로 포함된다. first1/first2의 유일한 공통 나무는 root STOP/A다. 따라서 한 H의 union은1002+1002-2=2002이고 두 H에서 같은 first를 쓰는 union은2*1002²-2²이다.")

#text("일반 나무의 첫 결정과 각 관측 아래 자식은 선형 기대손실 합으로 연결된다. 고정된 부모 결정에서 자식 최소화가 전체 최소화와 교환되므로 Bellman 역귀납으로 전수 정책 최소와 같다. 이것은 선언 문법/공통 세계에서의 수학적 정당성이지 실측 성능이나 외부 방법의 신규성 증명이 아니다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 18. 동일 종료 권리의 전체 고정 순서 대조")]]
#v(3pt)
#strong[Require] #text("고정 predictor, 알려진 공통 세계/실패 법칙, T/C 위험 추정값 전역 고정 순서 문법과 공개 H·획득 이력 초기 quote1, 추가 시도2, 실패 과금, abstain 손실2/5")
#parbreak()
#strong[Ensure] #text("전체 적격 정적 정책 중 추정 목적함수 최소 reference 문맥 적응·근시안·하한 gate와 같은 세계의 비교 기록 미지원은 STOP/reference, 실행 실패는 실패 영수증과 미실행 분모")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("고정 순서마다 모든 관측0/1/F의 STOP·abstain·다음 query 가지를 정의한다. 숨은 센서와 정답은 selector에 주지 않는다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("각 마지막 이력에서 STOP과 abstain의 위험을 비교한다. 역순으로 query의 비용과 후속 위험을 합산해 모든 종료 규칙을 최적화한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("순서는 모든 H에 공유하고 종료 규칙은 H/이력에 반응하도록 허용한다. 짧은 subset은 긴 순서의 조기 종료로 표현한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("동일 추정기에서 고정 순서들의 평균 추정 J를 최소화하여 reference를 고른다. 적응 정책은 H별 첫 행동도 선택한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("calibration 직사각형 네 꼭짓점에서 같은 세계의 reference 대조 손실 하한을 구한다. 동률·미지원은 reference를 유지한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("선택을 동결하고 평가 전용 참값/예측 자료로 비용·오류·보류·교정·피해를 기록한다. 실패 시 재실행하지 않는다.")]])
#v(1.2pt)
]

= #text("새 controlled 확률 실험과 비교 조건")

#text("H 두 값은 각각1/2이고 A/B/F는8개 균등 세계다. q1은 F=1,B=0일 때, q2는 F=1,A=0일 때 실패한다. 실패는 F만 반환하고 추가 quote1을 청구한다. predictor는 필요한 token을 획득했으면 그 token, 없으면0이다. STOP은 predictor를 반환하고 A는 null과 고정 손실2/5를 반환한다.")

#text("theta는 두 token값에 대한(1/20,19/20)이며 H 사이에 공유된다. train64/token seed50051, calibration4096/token seed50052의 고정 PRNG를 써8320개 고유 합성 label을 생성했다. H마다 로그를 복제해 표본 수를 늘리지 않는다. 독립 iid Bernoulli 모형/알려진 세계는 가정이다.")

#text("empirical=eT/nT, calibrated=(eC+64*empirical)/(nC+64)이며 C가 없으면 prior를 쓴다. 두 비교군 모두 같은 T/C 정보에 접근하고 추가 tuning은0이다. 같은 추정기 안에서는 reference/adaptive/myopic/gate가 predictor·세계·실패·abstain·support·quote·남은 budget을 공유한다. estimator 이름이 다르면 데이터 사용량이 다르다는 의도한 조작만 달라진다.")

= #text("인증 계산과 실패 경계")

#text("nC=4096, delta1/20일 때 radius=ceil(1e6*sqrt(log(4/delta)/(2*nC)))/1e6이다. 두 Bernoulli 평균 구간을[0,1]과 교차하고 네 꼭짓점을 쓴다. 모든 정책의 error+quote는 theta에 affine이므로 최소/최대는 꼭짓점에 있다. 대조 두 정책은 같은 world와 같은 theta를 사용한다.")

#text("공동 포함 사건의 확률 하한은 두 좌표 Hoeffding과 union bound에 의존한다. data-dependent 정책까지 동시에 affine 포함을 적용하기 때문에 C와 선택 간 별도 독립성으로 가장하지 않는다. 미지원 C 진단4개는 reference를 유지한다. 이 단순 직사각형 모형은 W49의 비직사각4차원 혼합집합과 같지 않다.")

#text("outside_flipped와 outside_zero는 이번 계약에는 사전 명시한 진단이다. 네 경우 모두 참값이 집합 밖이나 reference 대비 gate regret는 static0/contextual-1/80으로 피해 반례를 만들지 못했다. 임의 OOD 안전으로 일반화할 수 없고, 과거 W49 사후 theta0 대입도 이번 사전 결과로 고쳐 쓰지 않는다.")

= #text("기록된 문맥별 오류·비용·보류와 피해")

#text("ordinary의 adaptive/myopic/reference 관련 예측 가능 mass는7/8이며 오류 mass는 기록상0.04375다. 정확한 수학값7/160과 serialized binary-float 차이 때문에 oracle가 멈췄다. 값이 작아 보인다는 이유로 tolerance를 사후 추가하거나 raw를 고치지 않았다. J와 quote 항은 유리수 문자열이다.")

#text("static-sufficient 양 H와 contextual 적응 정책의 J=33/160, quote9/4, failure3/8, abstain1/8이다. contextual 고정 reference는 H0 quote9/4/J33/160, H1 quote11/4/J37/160으로 macro35/160이다. 같은 terminal 예측끼리의 correction/harm mass는 ordinary reference 대조에서0/0이며 비용 차이가 핵심이다. 이 숫자는 raw 단회 관측이고 전체 metric 검산은 미완료다.")

#text("더 강한 정적 비교군을 준 뒤 작은 contextual 이득만 남았고 empirical/calibrated 선택은 같았다. 따라서 이 controlled 자료에서는 추정 보정 효과0과 H별 action 비용 차이를 개념적으로 구별할 수 있으나 현실 DEV에서 두 요인을 분리했다는 결론은 실패 때문에 내릴 수 없다.")

= #text("DEV 설계와 실제 선택 단계 오류")

#text("설계는 subject5/6의 T168+154=322,C96+96=192를 쓰고38상태를 만든다. support는 T30이상·양쪽 참가자 및 모든 양의 확률 successor의 같은 조건이다. 일곱 mask1/3/5/9/7/11/13만 허용하며 initial1와 추가 두 block까지만 산다.")

#text("각10고정 순서의 전체 STOP/A/next 결정 최적값을 계산하고, adaptive와myopic을 더해 추정기당12정책을 만들 계획이었다. calibrated tau64는 상속 설계에서 고정한 값이며 새 CV/tuning은0이다. 참된 state posterior와 다른 surrogate 위험/전이를 최적화한다는 한계를 유지한다.")

#text("실제 dev_select는 states metadata의 branches를 만들면서3block 마지막 상태에도 나머지 block의 자식 info를 요구했다. child mask15의 cached predictions가 없어 KeyError가 발생했다. actions 예산 검사는 먼저 실행됐어도 metadata 생성 경로는 제한하지 못했다. 이는 단일 shared domain 경계에서 고칠 문제이나 여기서는 봉인을 지켰다.")

#text("DEV selection 자체는시작1/실패1이고 정책표 생성완료0/24, 경로시작0/12576이다. 평가 예정2명/524창을 실제 평가 결과로 보고하지 않는다. 오류·J·quote·coverage·paired 교정/피해·estimator interaction은 전부 null/미실행이다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 19. 노출 DEV의 추정기 교차 대조와 실패 반환")]]
#v(3pt)
#strong[Require] #text("해시로 연결한 기존 training514행, 평가 예정 DEV524행 일곱 mask와38상태, T322/C192, 두 추정기와10고정 순서 같은 support>=30/양쪽 참가자와 STOP fallback")
#parbreak()
#strong[Ensure] #text("성공 시24정책의 선택표와12576경로, 사람별 J·오류·coverage·짝지은 피해 이번 실제 반환: 선택 단계 KeyError15, 평가 경로0/12576, 원본 보존")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("T/C만 읽어 empirical 및 tau64 calibrated 위험과 T 전이를 계산한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("각 순서의 suffix 안에서 STOP·abstain·다음 query를 최적화한다. 다음 query가 미지원이면 대체 구매 없이 STOP한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("T의 참가자별 초기 상태 비율로 reference를 선정하고 적응·근시안 표와 함께 저장·해시 동결한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("선택표가 저장됐을 때만 노출 DEV 예측을 읽고, 요청한 token만으로 경로를 따라간다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("이번 실행은 상태 metadata가 허용되지 않은 mask15 위험을 참조해 3단계 전 실패했다. 저장 표와 이후 평가를 생성하지 않았다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("실패를 보존하고 남은 전체 경로를 미실행으로 반환한다. 다음 연구는 새 Task/새 계약에서만 수정한다.")]])
#v(1.2pt)
]

= #text("검산 prefix와 검증 공백")

#text("oracle는 research.py나 부모 코드를 import하지 않았다. 나무 번호를 radix10/bit leaf 방식으로 복호화하고 직접 잠재 세계를 따라가16032개 점수를 재계산했다. 저장 minima와 reference/게이트 꼭짓점 대조도 이 prefix 안에서 비교한 뒤 첫 지표의 exact equality에 실패했다.")

#text("REPORT의 checks16146은 시도 수이며 마지막 하나가 실패하므로 그 전 통과는16145다. 각 arm은 한 번씩만 시도했다. DEV oracle는 선택표가 없어서 FileNotFoundError로 실패했다. 두 구현을 같은 작성자가 썼고 독립 과학 검토는 coordinator의 후속 범위다. 완전 verifier 통과·과학 인증·publication readiness를 주장하지 않는다.")

#text("smoke4와unit10은 fixture이며 DEV 전체 metadata 경계 및 aggregate type 보존을 잠그지 못했다. 테스트 통과를 본실험 성공으로 치환하지 않는다. 새 regression은 다음 Task에서 실제 seven-mask/terminal branch 및 exact type aggregate를 다뤄야 한다.")

= #text("일반 복잡도·실제 byte·자원 계측")

#text("r개 결과와 B번 구매인 고정 순서의 전체 syntax 수는 T0=2,T_b=2+T_{b-1}^r다. 전체 policy 나무를 나열하면 이 크기만큼 시간/출력이 든다. 충분 상태를 쓰면 각 state에서 terminal2와 허용 query의 조건부 기대를 비교하므로 대략 O(S*d*r*N) 유리수 연산으로 평가/최적화할 수 있으나 N개 compatible world 집계를 상태마다 반복하는 구현 비용이 남는다.")

#text("d개 센서의 acquired/failure/value 상태 자체가 대략(r+1)^d로 증가할 수 있다. H별 tree 선택은 지수적인 joint catalogue를 분해하는 것이고 공통 순서 선택은 order별 H 최소를 합산한다. exact rational은 분모/분자의 bit 길이에 의존하며 단위 시간 실수 연산으로 세지 않는다. arbitrary histories가 상태로 압축되지 않으면 더 많은 history 상태가 필요하다.")

#text("DEV의 단순 위험표 계산은 O(S*(nT+nC)*d), K고정 순서의 DP와 표 저장은 대략 O(K*S*d*r), raw 경로는 O(nEval*K*B)시간/출력을 요구한다. 이번에는 metadata 실패로 뒤 비용을 지출하지 않았다. 수학적 bound와 실제 측정1회 비용을 구분한다.")

#text("COST_ACCOUNTING.json은 준비/main/oracle 직접 process CPU와 launcher wall, 명시 읽기 및 실제 output byte를 기록한다. unit의 직접 CPU는null이다. source hashes는 시작/checkpoint/종료의 POLICY·reviewer·builder가 동일함을 확인한다. 실제 OS IO·peak memory·SOL 저술·Orca 전송 tail은null/미계측이다.")

= #text("관련연구·승격·다음 단계")

#text("본실험 exit1·oracle exit1을 보존하며 science_status=failed다. 완결된 실패 보고는 태스크의 완료와 구별한다. 봉인 후 코드·계약·입력을 수정하거나 재실행하지 않았다.")

#text("통제 모형은 W49의 네 좌표 혼합로그 공동-polytope와 다르다. H 사이에 공유되는 두 label 확률, 알려진8세계와 직접 iid Bernoulli label 표본을 가정한다. 이 단순화는 정적 종료 권리라는 이번 질문을 분리하기 위한 것이며 W49의 보장·신규성·응용 결과를 상속하지 않는다.")

#text("모든 MHEALTH1..10은 과거 사용됐다. 계획 DEV는 노출7/8의2명·524고유창이며 이번 평가 완료는0명/0창, 독립 final-test는0명이다. 정책경로·합성세계·검사 수를 사람 또는 독립 표본 수로 세지 않는다.")

#text("신규 외부 원문 읽기0이며 closest prior-art overlap, 정확한 판본/가정/재현과 신규성은 미해결이다. 상속 metadata나 독립 검토자의 동의를 사실/과학 인증으로 바꾸지 않는다.")

#text("quote는 논리 비용이다. 센서 I/O·전력·물리 속도·provider 실패율·population coverage·MNAR/OOD 안전은 검증하지 않았다. 실험 model_api_calls=0/native_episodes=0과 SOL 저술 사용량 미계측을 구별한다.")

#text("동일 process의 함수 인자 제한은 협력적 정보 경계이며 OS 격리가 아니다. 위험표와 전이표는 일관된 joint label posterior가 아닐 수 있다. 지수 정책 공간의 동적계획법 목적함수 최적성을 현실의 최적성으로 바꾸지 않는다.")

#text("준비·본실험·oracle의 저장 process CPU/wall 및 launcher wall을 구별한다. 단위검사의 직접 CPU, OS/stdlib 읽기, peak memory, 과거 모델 학습, shell/Orca 최종 전송 및 SOL token 비용은 미계측이다. 수동 사전 읽기는4MiB 예약량이며 정확 계측이 아니다.")

#text("사전 outside-flipped/zero 진단4건은 모두 gate의 reference 대비 양의 피해를 보이지 않았다. 같은 세계에서 종료 예측이 같고 quote만 줄어드는 이번 구조에서는 분포 이탈만으로 피해 반례가 생기지 않을 수 있다. 이 진단 실패를 W49 사후 theta0 분석의 성공으로 대체하지 않는다.")

#text("원고 schema는 기존 build_documents.validate로만 확인한다. METHOD_REVIEW/VERIFICATION/INTAKE/AOP/조판/게시는 작성하지 않는다. SKILL_CANDIDATE는 비활성 실패 사례 메모이고 전역 스킬·운영 상태·공유 모델 서버는 변경하지 않는다.")

= #text("E. completed-coherent-study: complete authored document")

#text("The following complete authored sections remain source-bound. Any then-pending parent lifecycle/review statement is dated producer wording; current completed normal-task/review references are recorded separately.")

= #text("Question and methodological change")

#text("The previous statewise calibration changed terminal errors while retaining T-only transitions. This new study derives risks, transitions and root masses from one participant-balanced complete-row law. It changes an implementable estimator, not the inherited predictor.")

#text("Coherent adaptive at totalbudget3 versus legacy empirical: regression (J gain -8059/196080); versus legacy statewise: regression (J gain -58067/686280). Main and raw-only oracle status: completed/passed.")

#fit-equation[$ P = (64 P_T + 192 P_C) / 256 $]
#text("P_T and P_C first balance people5/6. Condition this single unconditional row law on the observed transcript; conditional T/C proportions usually differ from1/4 and3/4.")

= #text("Algorithm, state and budget")

#text("The observed token state and total remaining blocks delimit every call. Terminal three-block metadata has no children, so no mask15 prediction can be requested. The unequal-state-mass regression rules out mixing conditional laws with fixed1/4 and3/4 weights.")

#text("All ten global orders retain all observed-history STOP and abstain decisions and share support, query cost and predictor access with myopic/adaptive. Unsupported current states STOP; blocked next queries at supported states retain both terminal choices.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 20. Participant-balanced coherent joint calibration and matched finite acquisition")]]
#v(3pt)
#strong[Require] #text("514 frozen complete rows from people5/6; T322/C192, inherited7-mask predictor outputs Observed state: four token entries; unacquired=-1; masks1,3,5,9,7,11,13 only Total block budgets1,2,3; initialblock0; query1/20; abstain2/5; shared T support>=30/bothpeople")
#parbreak()
#strong[Ensure] #text("Frozen10 static order policies, replanning myopic and adaptive for each estimator/budget Train/calibration-selected reference and exact complete-row coherence evidence Exploratory per-person errors, cost, coverage, paired corrections/harms and all no_gain/regression")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Give each training person half the T mass and half the C mass. Form the unconditional mixture P=(64P_T+192P_C)/256 before conditioning.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Restrict the same weighted complete rows to the acquired-token transcript. Normalize once; compute terminal error and every next-token probability from those identical weights.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Permit a query only in the cached mask/budget domain and when every positive T/joint successor passes the common T support rule. Charge every permitted attempt.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("At a supported terminal compare STOP and abstain; each fixed global order may also take its next admitted query. Adaptive may choose any admitted query. Myopic re-evaluates one step after each observation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Solve exact rational finite Bellman recurrences and score the resulting whole trees. Select the reference with T/C only and freeze all108 policy tables before opening DEV bytes.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Evaluate56592 policy-window paths on exposed people7/8. A separate raw-only implementation reconstructs laws, decisions, direct conditional J and every aggregate. Preserve failures and no_gain.")]])
#v(1.2pt)
]

= #text("Finite-law identity and proof scope")

#text("For any fixed eligible tree and any positive-mass observed state, conditional expected terminal loss plus future quote cost under P equals its frozen-tree recurrence. At leaves this is the definition of conditional error/abstain. At a query, partition the same row set by observed token, apply the induction hypothesis to each child and the law of total expectation. Add exactly one query charge. The finite horizon proves the identity.")

#text("Adaptive/fixed Bellman tables use this whole continuation. A myopic one-step value is checked against a directly truncated continuation, and its frozen replanning tree is scored separately. This identity establishes coherence only under the declared empirical P; it gives no population risk, safety or new-algorithm theorem.")

= #text("Exploratory results and fair controls")

#text("Each estimator supplies12 policies at each of three total budgets; all108 policy tables and56592 paths reuse524 unique windows from only two previously exposed people. Per-person corrections and harms compare only pairs where both predict; abstain transitions, coverage and cost are separate.")

#text("Budget changes re-optimize policies at the same fixed lambda, rather than re-score one policy. Estimator changes are compared within a policy family; adaptive gains are compared with same-estimator static and myopic controls. DEV-best fixed order remains descriptive hindsight.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Already-exposed DEV, exact participant-macro logical objective. Static reference selected without DEV; no final-test inference.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("estimator/bu​dget")],[#text("selected fixed")],[#text("adaptive J")],[#text("fixed J")],[#text("myopic J")],[#text("fixed-adapti​ve")],[#text("status")]),
[#text("legacy_empir​ical::b1")],[#text("fixed_1")],[#text("7057/16340")],[#text("7057/16340")],[#text("7057/16340")],[#text("0")],[#text("no_gain")],
[#text("legacy_empir​ical::b2")],[#text("fixed_2")],[#text("1364/4515")],[#text("134663/45752​0")],[#text("1364/4515")],[#text("-10667/13725​60")],[#text("regression")],
[#text("legacy_empir​ical::b3")],[#text("fixed_2")],[#text("1364/4515")],[#text("134663/45752​0")],[#text("1364/4515")],[#text("-10667/13725​60")],[#text("regression")],
[#text("legacy_state​wise::b1")],[#text("fixed_1")],[#text("7057/16340")],[#text("7057/16340")],[#text("7057/16340")],[#text("0")],[#text("no_gain")],
[#text("legacy_state​wise::b2")],[#text("fixed_3")],[#text("453329/13725​60")],[#text("453329/13725​60")],[#text("453329/13725​60")],[#text("0")],[#text("no_gain")],
[#text("legacy_state​wise::b3")],[#text("fixed_32")],[#text("10141/39216")],[#text("10141/39216")],[#text("10141/39216")],[#text("0")],[#text("no_gain")],
[#text("coherent_joi​nt::b1")],[#text("fixed_1")],[#text("7057/16340")],[#text("7057/16340")],[#text("7057/16340")],[#text("0")],[#text("no_gain")],
[#text("coherent_joi​nt::b2")],[#text("fixed_2")],[#text("157023/45752​0")],[#text("157023/45752​0")],[#text("157023/45752​0")],[#text("0")],[#text("no_gain")],
[#text("coherent_joi​nt::b3")],[#text("fixed_2")],[#text("157023/45752​0")],[#text("157023/45752​0")],[#text("157023/45752​0")],[#text("0")],[#text("no_gain")])
]

= #text("Computational scope, prior work and limitations")

#text("All MHEALTH1..10 were previously exposed. DEV is two already-exposed people7/8 and524 unique windows; independent final-test people0. Window/policy multiplicity is not independent sample size; no IID window CI.")

#text("The forest/prediction bank is inherited frozen data. This is coherent estimation and matched decision diagnosis, not joint predictor training, new model inference or population calibration.")

#text("Coherent_joint changes participant balancing, the unconditional risk/kernel law and transition weighting together. Its difference from legacy_statewise is a bundled estimator change, not an identified causal effect of coherence alone. Fixed acquisition orders retain adaptive history-dependent stopping; they are not completely nonadaptive masks.")

#text("No external primary-source reads or closest-method reproduction were performed here. Finite Bellman planning, risk calibration and reference fallback alone establish no algorithmic novelty or SOTA. Parent literature audit and independent method review remain separate.")

#text("Logical quote cost1/20 is not measured sensor latency, energy, physical I/O or provider failure. Cached rows have no failure outcomes; missingness, MNAR, OOD and safe-policy guarantees are unmeasured.")

#text("No-eviction persistent DAG caching alone has order-independent cost for a fixed acquired set: pay the union of required ancestors once. Adaptive set/STOP changes can change this union; a static policy has the same cache rights. This is an algebraic observation, not a cache experiment.")

#text("Common T support checks the union of positive T and joint successors, so calibrated C-only mass cannot buy privileged acquisitions. Unsupported current states force STOP; supported fixed policies with blocked next query retain STOP/abstain. This explicit fair-domain correction is shared across every estimator.")

#text("Direct process CPU/wall and explicit bytes are measured. Authoring/model token charges, preledger exact reads, historical fit, peak memory, OS/stdlib reads, physical I/O and final shell tail remain unmeasured. Manual preledger reads reserve4MiB; quotas are cooperative, not OS isolation.")

#text("W49/W50 frozen files and their failures remain unchanged. No new synthetic performance experiment, private clean test, totalbudget4, mask15 inference, publication, Git, official Task completion or settlement was performed by this executor.")

= #text("Exact implementation and negative results")

#text("Coherent adaptive at totalbudget3 versus legacy empirical: regression (J gain -8059/196080); versus legacy statewise: regression (J gain -58067/686280).")

#text("Code/contract/inputs were sealed after real-schema regression. One main and one alternative raw-only oracle were allowed. W50 failures are preserved and not rerun. All raw paths, selection tables, source pins and costs are retained.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 21. Participant-balanced coherent joint calibration and matched finite acquisition")]]
#v(3pt)
#strong[Require] #text("514 frozen complete rows from people5/6; T322/C192, inherited7-mask predictor outputs Observed state: four token entries; unacquired=-1; masks1,3,5,9,7,11,13 only Total block budgets1,2,3; initialblock0; query1/20; abstain2/5; shared T support>=30/bothpeople")
#parbreak()
#strong[Ensure] #text("Frozen10 static order policies, replanning myopic and adaptive for each estimator/budget Train/calibration-selected reference and exact complete-row coherence evidence Exploratory per-person errors, cost, coverage, paired corrections/harms and all no_gain/regression")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Give each training person half the T mass and half the C mass. Form the unconditional mixture P=(64P_T+192P_C)/256 before conditioning.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Restrict the same weighted complete rows to the acquired-token transcript. Normalize once; compute terminal error and every next-token probability from those identical weights.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Permit a query only in the cached mask/budget domain and when every positive T/joint successor passes the common T support rule. Charge every permitted attempt.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("At a supported terminal compare STOP and abstain; each fixed global order may also take its next admitted query. Adaptive may choose any admitted query. Myopic re-evaluates one step after each observation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("Solve exact rational finite Bellman recurrences and score the resulting whole trees. Select the reference with T/C only and freeze all108 policy tables before opening DEV bytes.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Evaluate56592 policy-window paths on exposed people7/8. A separate raw-only implementation reconstructs laws, decisions, direct conditional J and every aggregate. Preserve failures and no_gain.")]])
#v(1.2pt)
]

= #text("Identity, cache accounting and limits")

#text("For any fixed eligible tree and any positive-mass observed state, conditional expected terminal loss plus future quote cost under P equals its frozen-tree recurrence. At leaves this is the definition of conditional error/abstain. At a query, partition the same row set by observed token, apply the induction hypothesis to each child and the law of total expectation. Add exactly one query charge. The finite horizon proves the identity.")

#text("Adaptive/fixed Bellman tables use this whole continuation. A myopic one-step value is checked against a directly truncated continuation, and its frozen replanning tree is scored separately. This identity establishes coherence only under the declared empirical P; it gives no population risk, safety or new-algorithm theorem.")

#text("All MHEALTH1..10 were previously exposed. DEV is two already-exposed people7/8 and524 unique windows; independent final-test people0. Window/policy multiplicity is not independent sample size; no IID window CI.")

#text("The forest/prediction bank is inherited frozen data. This is coherent estimation and matched decision diagnosis, not joint predictor training, new model inference or population calibration.")

#text("Coherent_joint changes participant balancing, the unconditional risk/kernel law and transition weighting together. Its difference from legacy_statewise is a bundled estimator change, not an identified causal effect of coherence alone. Fixed acquisition orders retain adaptive history-dependent stopping; they are not completely nonadaptive masks.")

#text("No external primary-source reads or closest-method reproduction were performed here. Finite Bellman planning, risk calibration and reference fallback alone establish no algorithmic novelty or SOTA. Parent literature audit and independent method review remain separate.")

#text("Logical quote cost1/20 is not measured sensor latency, energy, physical I/O or provider failure. Cached rows have no failure outcomes; missingness, MNAR, OOD and safe-policy guarantees are unmeasured.")

#text("No-eviction persistent DAG caching alone has order-independent cost for a fixed acquired set: pay the union of required ancestors once. Adaptive set/STOP changes can change this union; a static policy has the same cache rights. This is an algebraic observation, not a cache experiment.")

#text("Common T support checks the union of positive T and joint successors, so calibrated C-only mass cannot buy privileged acquisitions. Unsupported current states force STOP; supported fixed policies with blocked next query retain STOP/abstain. This explicit fair-domain correction is shared across every estimator.")

#text("Direct process CPU/wall and explicit bytes are measured. Authoring/model token charges, preledger exact reads, historical fit, peak memory, OS/stdlib reads, physical I/O and final shell tail remain unmeasured. Manual preledger reads reserve4MiB; quotas are cooperative, not OS isolation.")

#text("W49/W50 frozen files and their failures remain unchanged. No new synthetic performance experiment, private clean test, totalbudget4, mask15 inference, publication, Git, official Task completion or settlement was performed by this executor.")

= #text("E. completed-certified-search: complete authored document")

#text("The following complete authored sections remain source-bound. Any then-pending parent lifecycle/review statement is dated producer wording; current completed normal-task/review references are recorded separately.")

= #text("Problem and output contract")

#text("Precommit affordable fixed subset S before reading: minimize worst feasible closed-bin sharp macro route-minus-static interval width R(S)=max_z[U(S,z)-L(S,z)], under the unchanged original r/v independent box/mean and globally capped binary requested-error model. Exact output is one lex(R,cost,mask) winner, not all primary/transcript ties. Epsilon 1/32 is an absolute macro-loss-width tolerance and certifies scalar regret only.")

#text("Same robust sharp-width objective was solved under a one-winner contract. Exact objective improvement is 0/no_gain by design. Observed exact B&B CPU lower than memoized DP in 2/7 conditions; Python peak lower in 2/7. Both baselines, all ties retained only by the original, epsilon certificates and every observed DP win remain in the tables.")

#text("Constructed finite engineering observations, three cyclic cold orders, no confidence interval or universal speedup. Python traced peaks exclude RSS; common imports and independent oracle are separate measured scopes. Terminal receipt serialization is charged to main total, outside arm timers. No new data/model/prediction/acquisition or accuracy gain; no original AO* execution or external novelty claim. Raw-only oracle is separate code by the author; distinct formal review belongs to the parent. Static immediate closed-bin world model only. n_j<=3 proposal wording was corrected before seal to <=4 for the already fixed n4 cases. One preseal zero-budget clock-quantization regression failed and was corrected before the input seal; all attempts are preserved in SELF_CHECK.json. No frozen code or registered failed main/oracle was repaired/replayed.")

= #text("Certified search")

#text("The full proof and exact world objective are in THEORY.md. Three feasible full-M readings lower-bound every affordable completion; sharp prefix widths upper-bound only the inner maximum. The bound directions are deliberately different.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 22. Certified fixed-subset one-winner branch and bound")]]
#v(3pt)
#strong[Require] #text("Validated original world model and sharp endpoint; positive integer prices and cap Q; epsilon>=0 in macro-loss-width units; fixed three feasible witness worlds.")
#parbreak()
#strong[Ensure] #text("One feasible subset and [L,U] certificate; at epsilon0 original lex(risk,cost,mask) winner. Timeout returns uncertified bounds and preserved partial work. No all-tie output claim.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("Build the same exact marginal-greedy incumbent and global witness floor used by value-only DP; charge all preprocessing, cache and bound work.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("Represent remaining static subsets by included I and undecided U; remove unaffordable remaining items. Let M=I union U.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("Project three verified world readings to M. The largest sharp width at these readings is a lower bound for every represented subset. Queue nodes by (lower,cost(I),I,U).")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("Prune only when the lex lower tuple cannot beat the incumbent; otherwise branch on the fixed stop-error-first/index item, include or exclude.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("At a complete subset maximize sharp width by DFS. Prefix sharp width is an upper bound; equality may be cut for one worst reading. A completed reading supplies its lower incumbent.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("Update only from exact feasible subset risks. A partial inner maximum may abandon a loser only when its lex lower tuple cannot beat the incumbent.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("For epsilon>0 stop only when U minus the minimum live-frontier lower bound is <=epsilon; at epsilon0 resolve remaining cheaper equal-risk possibilities.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("On a cap return uncertified partial bounds, reinsert any active unresolved node, retain all failures and never silently retry.")]])
#v(1.2pt)
]

= #text("Matched cost observations")

#text("All arm times include seed construction, greedy search, all endpoint/bound work, caches and raw writes. No old timing is pooled with these observations.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Fresh finite arm measurements; zero new empirical samples.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Condition")],[#text("Original CPU")],[#text("Memo DP CPU")],[#text("Exact B&B CPU")],[#text("Epsilon B&B CPU")]),
[#text("equality_ties")],[#text("0.015625")],[#text("0.015625")],[#text("0.015625")],[#text("0.0")],
[#text("impossible_bins")],[#text("0.015625")],[#text("0.015625")],[#text("0.03125")],[#text("0.015625")],
[#text("tight_zero_cap")],[#text("0.0625")],[#text("0.0625")],[#text("0.078125")],[#text("0.046875")],
[#text("complementarity")],[#text("0.265625")],[#text("0.25")],[#text("0.21875")],[#text("0.171875")],
[#text("w41_shared_cap_ties")],[#text("4.09375")],[#text("0.203125")],[#text("0.25")],[#text("0.203125")],
[#text("hard_pairs_Q2")],[#text("0.34375")],[#text("0.125")],[#text("0.125")],[#text("0.109375")],
[#text("hard_pairs_Q4")],[#text("6.96875")],[#text("0.71875")],[#text("0.28125")],[#text("0.15625")])
]

#figure(image("search_costs.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("CPU seconds and traced Python bytes under identical fixed model/cost/query budgets. Three cyclic cold orders are descriptive repeats, not independent datasets. All costs and DP wins are retained.")])
= #text("Full metrics and negative comparisons")

#text("Same robust sharp-width objective was solved under a one-winner contract. Exact objective improvement is 0/no_gain by design. Observed exact B&B CPU lower than memoized DP in 2/7 conditions; Python peak lower in 2/7. Both baselines, all ties retained only by the original, epsilon certificates and every observed DP win remain in the tables.")

#text("Constructed finite engineering observations, three cyclic cold orders, no confidence interval or universal speedup. Python traced peaks exclude RSS; common imports and independent oracle are separate measured scopes. Terminal receipt serialization is charged to main total, outside arm timers. No new data/model/prediction/acquisition or accuracy gain; no original AO* execution or external novelty claim. Raw-only oracle is separate code by the author; distinct formal review belongs to the parent. Static immediate closed-bin world model only. n_j<=3 proposal wording was corrected before seal to <=4 for the already fixed n4 cases. One preseal zero-budget clock-quantization regression failed and was corrected before the input seal; all attempts are preserved in SELF_CHECK.json. No frozen code or registered failed main/oracle was repaired/replayed.")

= #text("F. Previous completed main paper: exact historical copy")

#text("The following fourteen structured sections preserve the complete earlier main narrative before reordering and copyediting. Their local section, algorithm, table and figure references identify the earlier edition. Current interpretation is in the new main paper; these dated source copies are retained to prevent silent scientific omissions.")

= #text("Abstract")

#text("Information design and sequential prediction have different objectives and different opportunities for improvement. ProbeFlow develops a certified single-winner search for the fixed-subset problem of minimizing the worst sharp conditional loss-interval width under a hard query budget. Verified feasible readings supply lower bounds for the outer subset minimization, while partial-transcript widths supply upper bounds for the inner maximization. Exact lexicographic selection and an absolute epsilon certificate replace the earlier all-tie output contract.")

#text("Seven constructed conditions, four solvers and three cold cyclic orders yield 84 completed runs. In the hardest eight-coordinate condition, all exact solvers return risk 21/64 and the same unique design; observed median CPU is 0.71875 s for a strong memoized value-only DP and 0.28125 s for exact branch-and-bound, with maximum traced Python peaks 334,535 and 141,338 bytes. Joint CPU/peak wins occur in only 2/7 conditions. A separate participant-balanced acquisition estimator on 524 previously exposed windows is coherent but regresses, ties its fixed/myopic controls and has no independent final participants. We therefore claim bounded engineering gains and conditional certificates, with no accuracy improvement, universal speedup or population-safety claim.")

= #text("1. Introduction")

#text("A system may improve the computation of an information design without improving the accuracy of a prediction policy. These are different claims. ProbeFlow studies both questions under explicit information and cost contracts: a fixed subset of queries can reduce uncertainty about a loss contrast, while a sequential policy can buy features to reduce classification-plus-acquisition loss. Sharing an acquisition vocabulary does not make their objectives or evidence interchangeable.")

#text("Our main algorithmic result concerns the former problem. We retain the original sharp endpoint model and hard query budget, but change the output from every primary-risk subset and every worst reading to one canonical subset and one witness. This permits equality pruning inside a numeric maximum. More importantly, a finite bank of verified worlds yields a lower bound for every subset represented by an outer search node. A best-bound frontier combines that lower bound with an exact feasible incumbent and returns either the exact risk/cost/mask winner or an absolute epsilon gap.")

#text("We test this search against both the original all-tie solver and a strong value-only dynamic program that merges repeated subset orders and receives the same inner solver, cache rights, greedy warm start and global floor. The result is conditional: exact branch-and-bound reduces CPU and traced peak together in two of seven conditions; DP wins or ties elsewhere. The objective itself does not improve because every exact method solves the same problem. The separate application study supplies a useful counterpoint: internally coherent risk/kernel estimation does not imply better decisions.")

#text("The contributions are a single-winner/epsilon contract, code-matched bound proofs, a matched strong-DP comparison with retained negative cases, and a separate negative acquisition diagnostic. The supplement and Korean guide retain all legacy results, endpoint derivations, failures and source-inspection limits.")

#figure(image("figures/architecture.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Information and cost architecture. O denotes observed source material, C internal computations and X actor-visible purchased information. Offline fitting/evaluation rights differ from paid policy inputs; caches confer no right to inspect an unpurchased value. The fixed-subset search operates on a declared public world model, while the application actor receives purchased tokens only. These are cooperative interfaces, not OS isolation.")])
= #text("2. Related work and comparable rights")

#text("Active feature acquisition chooses observations and terminal predictions [1, 2]. The closest selected primary source already contains fixed predictors, terminal risks, conditional acquisition kernels, hard budgets and Bellman comparison [8]. Our participant-balanced row construction is not a new Bellman principle or joint predictor training. Learning-To-Measure pretrains then freezes a predictor and learns conditional/meta-policy structure [9]; SEFA uses latent gradient/Monte Carlo acquisition and grants a test availability mask in its selected availability experiment [10]. AFAPE concerns counterfactual acquisition-plus-misclassification cost under identification and positivity assumptions [11]. Local count support is not whole-policy identification.")

#text("The fixed-subset worst-width objective instead commits to queries before reading their closed bins. The retained complementarity witness violates diminishing returns, so a greedy warm start has no transferred adaptive-submodularity guarantee [7]. Branch-and-bound, lower bounds and exact subset DP are established general ideas; this study evaluates the specified variant and certificates, not external novelty, AO* correspondence or an external implementation benchmark. Repeated exposed-DEV selection remains a separate concern [3].")

#text("Table 1 summarizes selected-source rights rather than published numerical performance. Its audit read selected HTML sections and official metadata, with inherited capture/prefix limits retained separately. Full-paper proofs and code were not reproduced. A representation invariant to item order does not make deadlines, failures or stateful cache behavior order invariant.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Selected primary-source comparison: information, terminal and computation rights. These sources were not reproduced as numerical baselines.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Work")],[#text("Predictor")],[#text("Kernel/model")],[#text("Terminal rights")],[#text("Availability")],[#text("Objective")],[#text("Computation")]),
[#text("Incomplete-t​raining AFA")],[#text("Fixed")],[#text("Risk/kernel restoration")],[#text("STOP")],[#text("Incomplete-t​rain assumptions")],[#text("Prediction+a​cquisition")],[#text("Finite Bellman")],
[#text("Learning-To-​Measure")],[#text("Pretrain; freeze")],[#text("Learned conditional")],[#text("Full path in cited eval")],[#text("Queried features")],[#text("Held-out log likelihood")],[#text("Greedy/looka​head")],
[#text("SEFA")],[#text("Masked encoder/pred​ictor")],[#text("Latent/MC score")],[#text("Acquisition curves")],[#text("App I.1 prior mask")],[#text("AFA curves")],[#text("Approximate scoring")],
[#text("AFAPE")],[#text("Target policy/class​ifier")],[#text("DM/IPW/DRL nuisance")],[#text("Target-polic​y rules")],[#text("NDE/NUC/posi​tivity")],[#text("Counterfactu​al cost")],[#text("Offline estimation")],
[#text("This search")],[#text("No new predictor")],[#text("Sharp public world model")],[#text("Fixed query subset")],[#text("Guaranteed closed bins")],[#text("Worst interval width R")],[#text("Exact/epsilo​n B&B")],
[#text("Separate DEV study")],[#text("Same frozen forest")],[#text("One balanced row law")],[#text("Same STOP/abstain")],[#text("Paid tokens only")],[#text("Participant-​macro J")],[#text("Finite recursion")])
]

= #text("3. Two problems and one information ledger")

#text("Fixed-subset design. A nonempty compatible-world set Omega defines an original route-minus-static macro loss contrast Delta. Query i has positive integer price c_i and a guaranteed closed-bin observation relation. Choose subset S before any readings. A feasible transcript z restricts the original worlds to Omega(S,z), with sharp endpoints L(S,z) and U(S,z). Empty intersections are impossible readings, never zero endpoints. Closed bins overlap at their threshold, so a boundary world can support both labels.")

#text("The exact representative minimizes the tuple (R(S),c(S),mask(S)) subject to c(S)<=Q. Risk is the maximum conditional interval width over feasible complete readings. The original all-tie contract additionally returned every affordable primary-risk mask and every worst transcript. The new contract returns one canonical representative and one worst witness per completed risk. An epsilon guarantee concerns absolute macro-loss interval-width units, not accuracy percentages or relative prediction regret.")

#text("Sequential prediction. A public state contains paid values/tokens, successful groups S_a, all attempted groups T_a, remaining cap and permitted cache/history metadata. STOP uses the current frozen predictor; ABSTAIN incurs a specified loss. Every attempt is charged, including failures in contracts that contain failure. Current cached DEV has successful returns only, so its attempt and success sets coincide; physical provider reliability is unmeasured. Gold labels and full feature caches are evaluator-only inputs.")

#fit-equation[$ R(S)=max_(z:Omega_(S,z)!=emptyset) [U(S,z)-L(S,z)] $]
#text("Minimize this width under the query budget, then price and integer mask. It is not the application objective J.")

#fit-equation[$ J(pi)=(1/P) sum_(s=1)^P (E_s(pi)+eta A_s(pi)+lambda C_s(pi))/n_s $]
#text("Participant means precede equal-person averaging. E counts errors on predictions, A abstentions and C attempted quotes; every planned n_s must be positive.")

#figure(image("figures/decision_contract.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("STOP, abstention and paid attempts have separate semantics. Failed attempts enlarge T_a and cost while leaving S_a unchanged; only selected returns become public. The completed cached-DEV study includes abstention but no observed failure outcomes. The general failure branch is an explicit future/application contract, not measured sensor behavior.")])
= #text("3.1. The original sharp world model")

#text("The search objective is defined by a finite-participant uncertainty set, not an empirical classification score. Participant j has n_j coordinates, requested coordinates A_j and known stop errors E_j. Requested binary errors share one global cap B_err across all participants; known stop errors equal one and other stop errors equal zero. Independent route/static availability vectors r and v lie in the unit box and each have participant sum n_j/2. The fixed cost is c=1/20 and k is nonnegative.")

#text("Let a_ji indicate a requested coordinate. Its route success is a_ji r_ji. The following losses charge a base route quote plus a requested quote, or two static quotes; k charges failed acquisition. Their equal-person difference Delta is optimized over the declared errors and availability constraints. A query observes a static-availability bin with threshold t_i in (0,1). No new participant, prediction or sensor reading is generated in the constructed search comparison.")

#text("The common endpoint routines optimize these original losses exactly over feasible error placements and box/sum vertices. The global binary cap is not duplicated for each participant. Query observations restrict the same original world set; they do not replace its unknown errors with labels or favorable zeros. This retained world model is what allows the different solvers and the raw-only independent checks to agree on an identical R.")

#fit-equation[$ ell_("route",j i)=(1-a_(j i)r_(j i))u_(j i)+c(1+a_(j i))+k a_(j i)(1-r_(j i)) $]
#text("Per-coordinate route loss; a is the fixed requested-coordinate indicator.")

#fit-equation[$ ell_("static",j i)=(1-v_(j i))u_(j i)+2c+k(1-v_(j i)) $]
#text("Per-coordinate static loss, with its independently constrained availability vector.")

#fit-equation[$ Delta=(1/P) sum_(j=1)^P (1/n_j) sum_(i=1)^(n_j) (ell_("route",j i)-ell_("static",j i)) $]
#text("Sharp L and U are respectively the minimum and maximum Delta over the nonempty compatible original worlds.")

= #text("4. Certified single-winner search")

#text("An outer node (I,U) represents all affordable subsets between included I and M=I union U. For any verified feasible complete reading on M, projecting its labels to a represented S gives Omega(M,z_M) contained in Omega(S,z_S). Hence the width of that one M reading lower-bounds R(S). Maximizing over a fixed finite bank of such feasible readings remains a valid lower bound. M may itself be too expensive: it is an optimistic relaxation, not a design that the returned policy executes.")

#text("The implementation fixes three public-model worlds: all availability coordinates 1/2, a participant vertex that fills its required n_j/2 mass from the first coordinate, and its reversal. It validates box/mean/error-cap constraints and closed-bin membership. Projected duplicate readings are evaluated once. The resulting bound is cached by M. Positive query prices let the search remove individually unaffordable undecided items and use (LB,c(I),mask(I)) as a lexicographic lower tuple.")

#text("Inside a fixed subset, a partial transcript h contains the worlds of any completed descendant z. Its sharp width therefore upper-bounds descendant width. A completed feasible reading supplies the inner lower incumbent b. Cutting prefix width<=b preserves the numeric maximum and one existing witness, while the original all-tie traversal requires a strict inequality. A partial completed maximum can abandon an outer loser only when its full risk/cost/mask tuple cannot beat the exact incumbent.")

#text("Algorithm 1 combines these different bound directions. Greedy supplies only an exactly evaluated feasible warm start, without a submodularity claim. The frontier covers unresolved subsets and every incumbent comes from an exact feasible risk. At epsilon = 0 the search resolves remaining cheaper equal-risk subsets rather than stopping at scalar gap zero. At positive epsilon, the incumbent upper risk minus the minimum frontier lower bound certifies scalar regret. A handled resource interruption returns uncertified state and restores the active node if present; it does not resume or retry.")

#fit-equation[$ "LB"(I,U)=max_k W(M,z_M^k)<=R(S), quad I subset.eq S subset.eq M $]
#text("Outer minimization: the reading must be verified feasible. This is a lower bound for every represented affordable S, even if M exceeds the query budget.")

#fit-equation[$ L(h)<=L(z)<=U(z)<=U(h), quad W(z)<=W(h) $]
#text("Inner maximization: partial-prefix width is an upper bound. The preseal direction witness has R(empty)=1/2 and R({1})=1/3; using the former as an outer lower bound would be invalid.")

#fit-equation[$ L_F=min("UB", min_(v in F) "LB"(v)), quad L_F<=R^*<="UB" $]
#text("With an empty frontier set L_F=UB. UB-L_F<=epsilon certifies returned-risk regret; at epsilon = 0 canonical price/mask ties still require resolution.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 23. Certified subset search with one winner")]]
#v(3pt)
#strong[Require] #text("Positive query prices, hard budget Q, tolerance epsilon; sharp endpoints and three verified public-model seed worlds. Included/undecided sets I,U; exact incumbent tuple (risk,cost,mask); initially cold shared caches.")
#parbreak()
#strong[Ensure] #text("One canonical optimum if epsilon=0 and search completes; otherwise feasible design plus scalar certificate [L,U]. Interruption is uncertified.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[$t^*<-$#text(" exact feasible empty/greedy incumbent; ")$F<-$#text(" Push(empty,all).")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("while frontier F is nonempty:")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.96em))[#text("check cooperative resource guard; restore active node on handled interruption.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$epsilon>0$#text(" and ")$"UB"-min("UB",min_F "LB")<=epsilon$#text(": break.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.96em))[$(I,U)<-$#text(" pop minimum bound/cost/mask node.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$("LB",c(I),I)>=t^*$#text(": continue.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$U=emptyset$#text(": compute exact ")$R(I)$#text("; update best only on exact completion.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.96em))[#text("else: choose first undecided item; Push both exclude/include children.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.0em))[#text("procedure Push")$(I,U)$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("10")], [#block(width: 100%, inset: (left: 0.96em))[#text("remove individually unaffordable items from ")$U$#text("; ")$M<-I union U$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("11")], [#block(width: 100%, inset: (left: 0.96em))[$"LB"<-max_k W(M,z_M^k)$#text(" from verified feasible seed readings.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("12")], [#block(width: 100%, inset: (left: 0.96em))[#text("retain node only if ")$("LB",c(I),I)<t^*$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("13")], [#block(width: 100%, inset: (left: 0.0em))[#text("return ")$"UB"=R(S^*)$#text("; ")$"LB"_F=min("UB",min_F "LB")$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("14")], [#block(width: 100%, inset: (left: 0.0em))[#text("epsilon = 0 resolves remaining lex ties; no all-tie output or strict node-cap promise.")]])
#v(1.2pt)
]

#figure(image("figures/search_bounds.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Bound directions and a nonzero certificate. Outer search minimizes R and uses verified full-reading lower bounds; inner search maximizes transcript width and uses prefix upper bounds. In the hard Q4 case, epsilon = 1/32 returns UB 21/64 and LB 97/320, a certified gap 1/40. The finite oracle later finds actual regret 0, which does not make that saved certificate exact.")])
= #text("4.1. Exactness, approximation and the strong baseline")

#text("Proposition 1 (canonical exactness). Assume exact sharp endpoints, positive prices and verified feasible seed readings. If the zero-tolerance search terminates without interruption, its returned tuple is the minimum affordable (R,cost,mask). Each retained outer node covers its affordable descendants; removing an individually unaffordable item removes no such descendant. The node lower tuple is no larger than any represented tuple. Thus every pruned node is unable to improve the exact incumbent, while branching covers all remaining subsets. Empty-frontier termination proves the claim. Inner equality pruning preserves the numeric R and one witness, which is the output contract needed by this proof.")

#text("Proposition 2 (absolute certificate). At a positive-tolerance stop, every unresolved design is represented by a frontier lower bound and every resolved loser cannot improve the incumbent. Hence L_F is a lower bound on the global optimum and UB is a feasible upper bound. Subtracting these inequalities gives returned-risk regret at most UB-L_F, which is at most epsilon. This scalar statement does not certify the cheapest mask among equal-risk subsets. Handled timeouts are explicitly uncertified.")

#text("The strong comparison is a memoized value-only subset DP, rather than a traversal that repeats acquisition permutations. Its state M determines remaining budget Q-c(M), and its recurrence compares stopping with every affordable extension. Positive additions cannot lower price or integer mask. If R(M) reaches the shared global seed floor, M is already the canonical winner of its extension family and the DP may stop there. The same exact inner kernel, cold endpoint/local/risk caches, warm-start construction and global floor are granted to both methods.")

#text("Bound and cache overhead can exceed the saved search work. General affordable subsets and subset/reading pairs still grow exponentially, up to 2^N and 3^N before feasibility reductions. Fraction bit lengths, endpoint work, frontier storage and retained output also matter. Greedy is only a feasible warm start: a retained complementarity fixture has R(4)=R(5)=R(6)=3/8 and R(7)=1/4, so a diminishing-returns shortcut would lack its required premise.")

#fit-equation[$ D(M)=min_("lex") {tau(M),H(M)} $]
#text("The exact tuple is tau(M)=(R(M),c(M),mask(M)). A_Q(M) contains the affordable items outside M.")

#fit-equation[$ H(M)=min_(i in A_Q(M)) D(M union {i}) $]
#text("All minima use the same lexicographic order; an empty extension family gives an infinite tuple. Terminal or floor-reaching states retain tau(M).")

= #text("5. A separate coherent-estimation diagnostic")

#text("The application study holds an inherited forest/prediction bank fixed and compares three estimators. Legacy empirical uses T-window-uniform risks/transitions. Legacy statewise shrinks calibration errors toward T risk while retaining T transitions. The coherent estimator first forms participant-balanced complete-row laws P_T and P_C, then mixes (64 P_T+192 P_C)/256 before conditioning. The state-dependent T/C proportions are generally not 1/4 and 3/4. One row law supplies terminal risks, next-token probabilities and initial-token mass.")

#text("Algorithms 2 and 3 match the frozen code. Common support requires at least 30 T rows and fitting participants 5 and 6 at the current state and every positive T-or-joint successor. Unsupported current states force STOP. Supported fixed orders with a blocked next action retain the better STOP/ABSTAIN decision, without replacing the query. Total budgets 1,2,3 include paid group 0; quote loss is 1/20 and abstention 2/5. Mask 15 and budget 4 are outside the seven-mask bank. All ten global orders may stop/abstain after revealed histories, making them stronger than fully committed subsets.")

#text("Under a sufficient finite state, nonnegative prices, a decreasing attempt horizon and common terminal rights, backward induction minimizes the declared surrogate. Legacy statewise risks and T transitions still define a valid abstract terminal-cost MDP; they need not represent the same complete-row predictive law. For the coherent law, partitioning compatible rows proves direct conditional tree loss equals recursive value. Myopic one-step value differs from eventual replanning-tree loss and is checked separately. These are algebraic identities, not population calibration. The estimator change bundles participant weighting, risks, kernels and initial mass, rather than identifying the causal effect of coherence alone.")

#fit-equation[$ P_J=(64 P_T+192 P_C)/256, quad P_D=(P_(D,5)+P_(D,6))/2 $]
#text("Algorithm 2 mixes complete-row laws before conditioning. Each row in D_s has mass 1/(2 n_Ds).")

#fit-equation[$ V_b(h)=min {r(h),eta,min_(a in A(h,b)) [lambda c_a+sum_z p(z|h,a)V_(b-c_a)(h a z)]} $]
#text("At supported states, all families compare the same terminal losses. Unsupported states return the declared STOP fallback. Fixed orders restrict the next query; myopic truncates lookahead to one step.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 24. Construct the participant-balanced complete-row law")]]
#v(3pt)
#strong[Require] #text("Frozen complete T/C rows for people 5,6 and seven mask predictions; labels are fitting-only inputs. Common support: at least 30 T rows and both fitting participants.")
#parbreak()
#strong[Ensure] #text("Joint row law, risks, transition probabilities and common eligible action table, frozen before DEV.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("for ")$D in {T,C}$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.96em))[#text("for ")$s in {5,6}$#text(": set ")$P_D(i)<-1/(2 n_(D,s))$#text(" for each ")$i in D_s$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[$w<-(64 P_T+192 P_C)/256$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("for each admitted transcript ")$h$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.96em))[$I_h<-$#text(" compatible rows; ")$Z_h<-sum_(i in I_h) w_i$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$Z_h=0$#text(": set risk")$<-1/2$#text("; mark unsupported; continue.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.96em))[$r(h)<-Z_h^(-1) sum_(i in I_h) w_i ell(f_S(i),y_i)$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.96em))[#text("if ")$abs(S(h))=3$#text(": no child construction; continue.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.96em))[#text("for each remaining action ")$a$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("10")], [#block(width: 100%, inset: (left: 1.92em))[$p(z|h,a)<-Z_h^(-1) sum_(i in I_h:z_i(a)=z) w_i$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("11")], [#block(width: 100%, inset: (left: 1.92em))[#text("admit ")$a$#text(" only if every positive T-or-joint successor has common support.")]])
#v(1.2pt)
]

= #text("5.1. Paid execution and terminal rights")

#text("Policy tables and the selected fixed reference are frozen using T/C before the DEV bank is opened. Runtime selection sees purchased tokens and its frozen table, not current unpurchased values or labels. In this all-success replay, a selected reveal increments attempted/successful masks and consumes one quote. The purchased cache has no additional acquisition right. The evaluator records full denominator, abstention and paired-error partitions after decisions.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 25. Freeze the common plan, then execute paid decisions")]]
#v(3pt)
#strong[Require] #text("Frozen risks, transitions, support and predictor bank; total budget B in{1,2,3}, quote 1/20, abstention 2/5. Adaptive, receding one-step myopic, or a fixed global order with history-dependent STOP/ABSTAIN.")
#parbreak()
#strong[Ensure] #text("Prediction or abstention; attempted/successful masks, cache, remaining budget and terminal path.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("procedure Plan")$(h,b)$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.96em))[#text("if current state is unsupported: return STOP.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.96em))[#text("compare STOP, ABSTAIN and admitted query values by the Bellman equation.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.96em))[#text("STOP wins terminal ties; queries require strict improvement; lower action index breaks query ties.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.96em))[#text("fixed order permits only its next action; myopic depth is at most 1.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("freeze decision maps and selected fixed reference using T/C only.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("online: ")$S=T={0}$#text("; quote ")$q=1$#text("; reveal only the paid group 0 token.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("while the frozen map requests action ")$a$#text(":")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("9")], [#block(width: 100%, inset: (left: 0.96em))[#text("assert ")$a$#text(" not in ")$T$#text(", ")$q<B$#text("; debit quote; ")$q<-q+1$#text(".")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("10")], [#block(width: 100%, inset: (left: 0.96em))[#text("reveal selected token; update ")$S,T,h,X$#text(" with that paid result.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("11")], [#block(width: 100%, inset: (left: 0.0em))[#text("return prediction ")$f_S$#text(" on STOP, or abstention on ABSTAIN; retain ")$B-q$#text(" and evaluator-only paired scores.")]])
#v(1.2pt)
]

= #text("6. Evaluation design")

#text("The search study freezes seven constructed conditions: equality ties, impossible bins, zero shared-error cap with unequal prices, complementarity, a shared-cap tie case, and four independent two-coordinate pairs at budgets 2 and 4. There are four solvers and three cold cyclic orders, giving 84 planned and completed runs. Cyclic orders are descriptive repeated measurements, not independent application samples or a complete four-position Latin balance. The original all-tie solver is unchanged; value-only DP and both B&B variants share the exact one-witness inner routine, cold caches, greedy candidates and global seed floor.")

#text("Arm CPU/wall and tracemalloc peaks include validation, applicable seed construction, warm starts, endpoint/bound/cache/search work and raw event writes. Common imports, terminal receipt serialization and independent oracle have separate recorded scopes. The original all-tie endpoint-call counter excludes impossible-bin attempts, whereas its raw event stream retains those None readings. We disclose that definition rather than comparing unequal counts as the same primitive. Python allocation peak is not RSS, physical I/O or acquisition energy.")

#text("The application comparison reuses 514 complete fitting rows: T participants 5/6 have 168/154 rows and C 96/96. Three estimators, twelve policies and three total budgets produce 108 tables and 56,592 paths on the same 524 previously exposed DEV windows from participants 7/8 (266/258). No predictor is fitted or run anew. All current paths complete; failed/unknown/unstarted are 0 under cached successful returns. Independent final participants remain 0. Direct raw-only audits and distinct normal native review tasks inspect both studies without rerunning their producer experiments.")

= #text("7. Application result: coherence does not improve J")

#text("The coherent adaptive policy ties its selected fixed order and myopic control on every observed path at all budgets. At budgets 2 and 3 its macro J is 157023/457520, approximately 0.34321. At budget 3 the empirical adaptive J is 1364/4515 and statewise J is 10141/39216; coherent therefore regresses by 8059/196080 and 58067/686280 respectively. Figure 4 shows the full budget contrast, including budget 1 ties. We do not headline the older exposed-DEV positive as the latest matched result.")

#text("At coherent budget 3, participants 7/8 have errors 52/29, abstentions 100/45 and quotes 392/437. The 81 errors are accompanied by 145 abstentions. Against empirical, both policies predict on 379 windows with 5 corrections and 12 harms;145 switch to abstention. Against statewise, the both-predict subset has 296 windows with 1 correction and 0 harms, plus 145 switches to and 83 from abstention. Those small paired counts cannot hide the full-objective regression.")

#text("Historical evidence remains visible but separate: the earlier completed calibration study had a small exposed-DEV contrast against a retrospective fixed best, while an omitted failure-abstention control invalidated one controlled strongest-static interpretation. The next sealed follow-up failed on unavailable mask 15 metadata and an exact-arithmetic abstention bug, with 0/12,576 DEV paths started. Current common support and terminal rights differ, so the present comparison is a new matched diagnosis, not a repair or unchanged-system replication of those results.")

#figure(image("figures/joint_results.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Separate application objective J:3 estimators, total budgets 1–3 and 2 previously exposed people/524 windows; independent final=0. Coherent adaptive equals its fixed/myopic controls. Curves are participant-macro full loss including abstention and attempted quotes. Right: budget 3 paired-error and abstention partitions; corrections/harms use only both-predict windows. No confidence intervals or physical-cost inference.")])
= #text("7.1. Search result: bounded engineering gain at identical R")

#text("All exact solvers agree on risk and the canonical design in every condition. The hard Q4 case has a unique mask 85 and risk 21/64; Q2 has mask 5 and risk 51/128. In Q4, median CPU is 6.96875 s for original all-tie,0.71875 s for strong DP and 0.28125 s for exact B&B. Maximum Python peaks are 231,943/334,535/141,338 bytes. The DP and exact B&B endpoint-call counts are 1,476 and 330 under their common counter; original all-tie reports 1,411 actual feasible calls under its distinct definition.")

#text("The engineering gain is not universal. Exact B&B beats DP in both median CPU and maximum traced peak only on complementarity and hard Q4,2/7 conditions. Equality, impossible bins, zero-cap, shared-cap ties and hard Q2 preserve DP wins or ties. The strongest shared-cap DP result, for example, is 0.203125 s versus 0.25 s for exact B&B and 85,789 versus 137,717 bytes. Table 2 retains all seven conditions; the supplement includes all four solvers and recorded work counters.")

#text("At epsilon = 1/32 every observed finite-oracle regret is 0, but certificates retain their actual gaps. Hard Q4 has lower 97/320, upper 21/64 and gap 1/40; epsilon uses 14 outer nodes versus 47 for exact search. It is a valid approximate certificate even though the returned design happens to be optimal. Exact objective gain is 0/no_gain by design. No classification or real acquisition accuracy result is inferred from this width-engineering study.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("All seven constructed conditions. Each cell gives strong DP / exact B&B: median direct CPU seconds or maximum traced Python bytes over three cold cyclic orders. Same exact risk in both methods; joint CPU/peak wins only in complementarity and Q4.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Condition")],[#text("CPU seconds: DP / B&B")],[#text("Python bytes: DP / B&B")],[#text("Exact R")]),
[#text("Equality ties")],[#text("0.015625 / 0.015625")],[#text("16224 / 16842")],[#text("0")],
[#text("Impossible bins")],[#text("0.015625 / 0.03125")],[#text("25126 / 27007")],[#text("11/30")],
[#text("Zero cap / prices")],[#text("0.0625 / 0.078125")],[#text("46670 / 72149")],[#text("41/120")],
[#text("Complementarity")],[#text("0.25 / 0.21875")],[#text("73531 / 59281")],[#text("1/4")],
[#text("Shared-cap ties")],[#text("0.203125 / 0.25")],[#text("85789 / 137717")],[#text("3/5")],
[#text("Four pairs Q2")],[#text("0.125 / 0.125")],[#text("66535 / 80798")],[#text("51/128")],
[#text("Four pairs Q4")],[#text("0.71875 / 0.28125")],[#text("334535 / 141338")],[#text("21/64")])
]

#figure(image("figures/search_costs_final.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Hard Q4, three cold cyclic repeats: median direct CPU seconds and maximum traced Python bytes. All exact methods return the same risk 21/64 and unique mask 85. Original all-tie retains more output; the strong DP comparison controls the one-winner inner kernel/cache/warm-start rights. Exact B&B wins CPU+peak over DP in only 2/7 conditions. Epsilon has a saved 1/40 certificate gap, not an exactness claim.")])
#block(width: 100%, breakable: false)[
= #text("8. Limits and failure boundaries")

#text("The search proofs require the stated static immediate closed-bin world model, verified feasible seed readings, positive prices and correct sharp endpoints. General subsets/readings remain exponential (up to 2^N/3^N), with rational bit, cache, frontier and retained-output costs in addition. Seven small constructed conditions do not establish asymptotic or universal speedup. Greedy is a feasible incumbent heuristic, not a certificate; the original full-tie and new one-winner contracts cannot be conflated.")

#text("Resource guards are cooperative. Independent review found that the generic node guard tests counter>cap and a final callback/pop may increment after the last check, allowing a possible one-node overshoot on that final step. All 84 observed arms are far below 250,000, with no observed cap violation or invalid certificate. We preserve the frozen code and disclose this general boundary; a strict ceiling requires a separate corrected implementation and boundary regression. Timeouts remain explicitly uncertified. No OS isolation is claimed.")

#text("The application has no untouched final participant, provider-failure process, physical sensor cost, clinical validation or external-method reproduction. Coherent conditionals do not guarantee transport; support counts do not certify density, positivity or safety. No-eviction persistent DAG caching has the same ancestor-union cost for a fixed acquired set under any order; only different sets/STOP or additional cache assumptions can change that comparison. Static controls receive the same cache rights. Historical fit, authoring cost, RSS and complete deployment cost remain unmeasured.")

= #text("9. Conclusion")

#text("ProbeFlow provides certified single-winner and epsilon search for the stated information-design problem. CPU/peak improvements over strong DP occur in two of seven conditions. The separate coherent acquisition estimator instead yields ties and regressions.")


]
#pagebreak()
= #text("Acknowledgements")
#text("This work was created as part of the No-More-Slops group activities at Pseudo Lab.")

= #text("References and actual inspection scopes")
#text("[shim2018] Hajin Shim, Sung Ju Hwang, Eunho Yang (2018). Joint Active Feature Acquisition and Classification with Variable-Size Set Encoding. Advances in Neural Information Processing Systems 31: 1368-1378")
#link("https://proceedings.neurips.cc/paper_files/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html")[#text("https://proceedings.neurips.cc/paper_files/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html")]

#text("Separate bibliography/source verifier in this authoring session: Official abstract and author/volume metadata; official JSON page_first/page_last and selected opening full_text paragraphs about sequential acquisition, stop/predict, joint classifier training and order-invariant encoding. The JSON includes additional full text that was archived but not fully read. No PDF, full proofs, experimental results or code read. Transfer limit: An order-invariant set encoder does not imply action-order invariance, equivalence to a fixed minimax objective, or ProbeFlow acquisition usefulness. No external benchmark transfer. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[li2021] Yang Li, Junier Oliva (2021). Active Feature Acquisition with Generative Surrogate Models. Proceedings of the 38th International Conference on Machine Learning 139: 6450-6459")
#link("https://proceedings.mlr.press/v139/li21p.html")[#text("https://proceedings.mlr.press/v139/li21p.html")]

#text("Separate bibliography/source verifier in this authoring session: Official PMLR title, authors, abstract and BibTeX/publication metadata only. No PMLR PDF, supplementary ZIP or code read. Transfer limit: The published metadata do not authenticate the edition of the inherited ar5iv cache or validate ProbeFlow against the learned GSMRL policy. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[cawley2010] Gavin C. Cawley, Nicola L. C. Talbot (2010). On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. Journal of Machine Learning Research 11: 2079-2107")
#link("https://jmlr.org/papers/v11/cawley10a.html")[#text("https://jmlr.org/papers/v11/cawley10a.html")]

#text("Separate bibliography/source verifier in this authoring session: Official title, both authors, year, volume/article/pages and abstract. No PDF, method, proof or experimental results read. Transfer limit: Does not certify that Research Forge's train/dev split or scientific evaluation is independent; that requires local evidence. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[uci319] Oresti Banos, Rafael Garcia, Alejandro Saez (2014). MHEALTH. UCI Machine Learning Repository. DOI 10.24432/C5TW22")
#link("https://archive.ics.uci.edu/dataset/319/mhealth%2Bdataset")[#text("https://archive.ics.uci.edu/dataset/319/mhealth%2Bdataset")]

#text("Separate bibliography/source verifier in this authoring session: Official UCI description, creators, dataset citation, DOI, license and variable-information text. No dataset archive, new sample data or original introductory-paper body downloaded or reread. Transfer limit: The UCI summary counter is not the number of independent local benchmark tasks or raw time-series rows. Official variable text still duplicates column 13 and omits column 12; do not silently repair physical axes or imply that a fresh UCI read validates the adapter, measurements or medical use. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[gsmrl-local-primary] Yang Li, Junier B. Oliva (2020). Active Feature Acquisition with Generative Surrogate Models. arXiv preprint. DOI 10.48550/arXiv.2010.02433")
#link("https://arxiv.org/abs/2010.02433v2")[#text("https://arxiv.org/abs/2010.02433v2")]

#text("Separate bibliography/source verifier in this authoring session: Fresh official v2 title/author/version/abstract metadata; selected original HTML Sec.2.1 state/action/stop and prediction-model paragraphs, Sec.2.2 chronology, Sec.2.3 action masking, and Sec.3/bibliography AO* citation. The inherited unversioned cache's four W44-selected passages totaling 7,879 bytes were independently reread at their physical byte ranges. No PDF, code, full proof or benchmark reproduction; other archived body sections are not claimed as fully read. Transfer limit: Ordinary vector-data set structure does not imply permutation invariance for a learned policy or predictor. The time-series method explicitly removes earlier acquisition candidates, so static terminal-order reasoning does not cover that process. Do not transfer AO* guarantees through GSMRL's related-work paragraph. The fresh v2 page is a separate source, not retroactive authentication of the unversioned cache. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[inherited-author-index] V. B. Zubek, Thomas G. Dietterich (2002). Pruning Improves Heuristic Search for Cost-Sensitive Learning. Proceedings of the International Conference on Machine Learning")
#link("https://web.engr.oregonstate.edu/~tgd/publications/index.html")[#text("https://web.engr.oregonstate.edu/~tgd/publications/index.html")]

#text("Separate bibliography/source verifier in this authoring session: Fresh official author-index entry under 2002 and the conflicting GSMRL v2 Sec.3/bibliography citation. Original AO* paper/PDF/proofs/code were not fetched or read; search-result snippets are discovery evidence only. Transfer limit: No original-paper optimality theorem, admissibility condition, statistical-pruning guarantee, or algorithm equivalence was independently verified. GSMRL's description is an indirect report. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[adaptive-submodularity] Daniel Golovin, Andreas Krause (2011). Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization. Journal of Artificial Intelligence Research 42: 427-486. DOI 10.1613/jair.3278")
#link("https://jair.org/index.php/jair/article/view/10731")[#text("https://jair.org/index.php/jair/article/view/10731")]

#text("Separate bibliography/source verifier in this authoring session: Official JAIR article metadata/abstract, official issue table of contents for pages, and official arXiv v5 authors/version/comment. The 2017 correction-comment paper's abstract was checked as context; its full proof was not read. No full current article body, PDF or independent proof audit. Transfer limit: ProbeFlow's fixed worst-width/minimax objective has not been shown here to satisfy the source assumptions. Do not claim the source's general greedy guarantee applies, or that the 2011 minimization theorem is unqualified by the later correction. Earlier local/source-read receipts remain inherited and separately hash-linked.")

#text("[afa-incomplete] Active Feature Acquisition with Incomplete Training Data. arXiv:2609.32325v1.")
#link("https://arxiv.org/html/2609.32325v1")[#text("https://arxiv.org/html/2609.32325v1")]

#text("Selected HTML sections 3.1-3.2 (equations 1-4), 4.1-4.3, 5.2 and B.2-B.3. Fixed predictor, conditional kernel, hard-budget STOP/Bellman and risk/kernel restoration are prior work; no MCAR result is transferred to arbitrary participant shift/MNAR. Separate read-only primary-source auditor, 2026-10-26; no external code, model training, numerical reproduction or formal METHOD acceptance. The local audit-record hash identifies that record, not complete external HTML/PDF bytes. Inherited HTML capture/prefix hashes and their truncation limits remain separate.")

#text("[l2m] Learning-To-Measure. arXiv:2510.12624v2; official ICML 2026 bibliography.")
#link("https://arxiv.org/html/2510.12624v2")[#text("https://arxiv.org/html/2510.12624v2")]

#text("Selected HTML sections 3.1, 4.1-4.3, 5-6 and A.4-A.5. Predictor pretraining then freezing, conditional/meta-policy learning, per-step held-out log likelihood and full-feature trajectories; section 6 leaves full cost-sensitive MDP outside scope. Official bibliography https://proceedings.mlr.press/v306/kobayashi26a.html checked separately. Separate read-only primary-source auditor, 2026-10-26; no external code, model training, numerical reproduction or formal METHOD acceptance. The local audit-record hash identifies that record, not complete external HTML/PDF bytes. Inherited HTML capture/prefix hashes and their truncation limits remain separate.")

#text("[sefa] SEFA. arXiv:2508.01957v3.")
#link("https://arxiv.org/html/2508.01957v3")[#text("https://arxiv.org/html/2508.01957v3")]

#text("Selected HTML sections 3-5, 6 and Appendices H/I/J. Masked stochastic encoder, latent-gradient/Monte Carlo acquisition; Appendix I.1 grants a test availability mask. No runtime or numerical superiority is transferred to this paper. Separate read-only primary-source auditor, 2026-10-26; no external code, model training, numerical reproduction or formal METHOD acceptance. The local audit-record hash identifies that record, not complete external HTML/PDF bytes. Inherited HTML capture/prefix hashes and their truncation limits remain separate.")

#text("[afape] AFAPE. JMLR 26(60), 2025; arXiv:2312.01530v4.")
#link("https://www.jmlr.org/papers/v26/23-1635.html")[#text("https://www.jmlr.org/papers/v26/23-1635.html")]

#text("Official abstract and selected arXiv HTML sections 3.2-3.5, 4.1 plus semi-offline positivity/identification passages at https://arxiv.org/html/2312.01530v4. NDE, NUC and positivity conditions are not replaced by local support counts; no DM/IPW/DRL estimator reproduction. Separate read-only primary-source auditor, 2026-10-26; no external code, model training, numerical reproduction or formal METHOD acceptance. The local audit-record hash identifies that record, not complete external HTML/PDF bytes. Inherited HTML capture/prefix hashes and their truncation limits remain separate.")

#text("[tang2026-motivation] Tang et al. AISTATS 2026, PMLR 300. Motivation only.")
#link("https://proceedings.mlr.press/v300/tang26d.html")[#text("https://proceedings.mlr.press/v300/tang26d.html")]

#text("Official abstract/bibliography only. Training-example active learning/experimental design is a different task from test-instance feature acquisition; not used as a theorem source or performance baseline. Separate read-only primary-source auditor, 2026-10-26; no external code, model training, numerical reproduction or formal METHOD acceptance. The local audit-record hash identifies that record, not complete external HTML/PDF bytes. Inherited HTML capture/prefix hashes and their truncation limits remain separate.")

