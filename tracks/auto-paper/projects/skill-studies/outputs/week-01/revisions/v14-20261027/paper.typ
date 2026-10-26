#set document(title: "ProbeFlow: Certified Search for Budgeted Information Design")
#set page(paper: "us-letter", margin: (x: 19mm, y: 19mm), numbering: "1")
#set text(font: ("New Computer Modern", "Malgun Gothic", "Noto Sans KR"), size: 10pt, lang: "en")
#set par(justify: true, leading: 0.57em, spacing: 0.60em)
#set heading(numbering: none)
#show heading.where(level: 2): set text(size: 10.4pt, weight: "bold")
#show heading.where(level: 1): set text(size: 11.4pt, weight: "bold")
#set figure(gap: 5pt)
#show figure.caption: set text(size: 8.3pt)
#let fit-equation(body) = layout(size => { let natural = measure(body); let factor = calc.min(1, size.width / natural.width); align(center, scale(factor * 100%, reflow: true, body)) })
#align(center)[#set par(justify: false)
#text(size: 17pt, weight: "bold", hyphenate: false)[#text("ProbeFlow: Certified Search for Budgeted Information Design")]]
#v(4pt)
#align(center)[#text(size: 9pt)[#text("Corrected conference narrative edition · 26 October 2026 · certified search and a separate acquisition diagnostic")]]
#v(6pt)
#block(inset: (x: 8mm))[#set text(size: 9.4pt)
#align(center)[#strong[Abstract]]
#text("Information design and sequential prediction have different objectives and different opportunities for improvement. ProbeFlow develops a certified single-winner search for the fixed-subset problem of minimizing the worst sharp conditional loss-interval width under a hard query budget. Verified feasible readings supply lower bounds for the outer subset minimization, while partial-transcript widths supply upper bounds for the inner maximization. Exact lexicographic selection and an absolute epsilon certificate replace the earlier all-tie output contract.")

#text("Seven constructed conditions, four solvers and three cold cyclic orders yield 84 completed runs. In the hardest eight-coordinate condition, all exact solvers return risk 21/64 and the same unique design; observed median CPU is 0.71875 s for a strong memoized value-only DP and 0.28125 s for exact branch-and-bound, with maximum traced Python peaks 334,535 and 141,338 bytes. Joint CPU/peak wins occur in only 2/7 conditions. A separate participant-balanced acquisition estimator on 524 previously exposed windows is coherent but regresses, ties its fixed/myopic controls and has no independent final participants. We therefore claim bounded engineering gains and conditional certificates, with no accuracy improvement, universal speedup or population-safety claim.")

]
#v(4pt)
#columns(2, gutter: 6mm)[
= #text("1. Introduction")

#text("Choosing a fixed set of measurements under a hard budget requires solving two nested problems: select the query set, then account for its worst feasible reading. When uncertainty is represented by sharp intervals for a loss contrast, a useful design minimizes the largest remaining interval width. Exhaustively returning every tied design and every worst reading can make this computation expensive even when a user needs only one reproducible optimum.")

#text("ProbeFlow addresses that computational gap in the retained public-world model. It returns one canonical risk/cost/mask winner, or a feasible design with an absolute epsilon certificate. Verified complete readings lower-bound the outer subset minimization; partial transcripts upper-bound the inner maximization. Separating these directions permits safe pruning. A value-only subset dynamic program supplies a strong comparison with the same inner kernel, cache rights, warm start and global floor.")

#text("The contributions are the single-winner/epsilon contract, code-matched exactness and certificate arguments, and a matched seven-condition engineering comparison that retains all negative cases. Exact branch-and-bound lowers both CPU and traced peak in only two of seven conditions; it leaves the exact objective unchanged. Branch-and-bound and dynamic programming themselves are established tools, and the present evidence does not establish external novelty or superiority over a reproduced published implementation.")

#text("A separate application diagnostic asks whether one participant-balanced row law improves sequential prediction and purchase decisions. Its objective J differs from fixed-subset interval width R. The coherent estimator regresses on exposed DEV and ties its fixed/myopic controls. Keeping that negative diagnosis separate tests the boundary between internal consistency, computation and application utility. Sections 3–4 define the two problems and methods, Section 5 reports their distinct experiments, and Sections 6–7 interpret the observations and limits.")

#figure(image("figures/architecture.svg", width: 100%), placement: top, scope: "parent", caption: [#text("Information and cost architecture. O denotes observed source material, C internal computations and X actor-visible purchased information. Offline fitting/evaluation rights differ from paid policy inputs; caches confer no right to inspect an unpurchased value. The fixed-subset search operates on a declared public world model, while the application actor receives purchased tokens only. These are cooperative interfaces, not OS isolation.")])
= #text("2. Related work and comparable rights")

#text("Active feature acquisition chooses observations and terminal predictions [1, 2]. The closest selected primary source already contains fixed predictors, terminal risks, conditional acquisition kernels, hard budgets and Bellman comparison [8]. Our participant-balanced row construction is not a new Bellman principle or joint predictor training. Learning-To-Measure pretrains then freezes a predictor and learns conditional/meta-policy structure [9]; SEFA uses latent gradient/Monte Carlo acquisition and grants a test availability mask in its selected availability experiment [10]. AFAPE concerns counterfactual acquisition-plus-misclassification cost under identification and positivity assumptions [11]. Local count support is not whole-policy identification.")

#text("The fixed-subset worst-width objective instead commits to queries before reading their closed bins. The retained complementarity witness violates diminishing returns, so a greedy warm start has no transferred adaptive-submodularity guarantee [7]. Branch-and-bound, lower bounds and exact subset DP are established general ideas; this study evaluates the specified variant and certificates, not external novelty, AO* correspondence or an external implementation benchmark. Repeated exposed-DEV selection remains a separate concern [3].")

#text("Table 1 summarizes selected-source rights rather than published numerical performance. Its audit read selected HTML sections and official metadata, with inherited capture/prefix limits retained separately. Full-paper proofs and code were not reproduced. A representation invariant to item order does not make deadlines, failures or stateful cache behavior order invariant.")

#figure(kind: table, placement: top, scope: "parent", caption: [#text("Selected primary-source comparison: information, terminal and computation rights. These sources were not reproduced as numerical baselines.")])[
#set par(justify: false)
#set text(size: 8.5pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Work")],[#text("Predictor")],[#text("Kernel/model")],[#text("Terminal rights")],[#text("Availability")],[#text("Objective")],[#text("Computation")]),
[#text("Incomplete-t​raining AFA")],[#text("Fixed")],[#text("Risk/kernel restoration")],[#text("STOP")],[#text("Incomplete-t​rain assumptions")],[#text("Prediction+a​cquisition")],[#text("Finite Bellman")],
[#text("Learning-To-​Measure")],[#text("Pretrain; freeze")],[#text("Learned conditional")],[#text("Full path in cited eval")],[#text("Queried features")],[#text("Held-out log likelihood")],[#text("Greedy/looka​head")],
[#text("SEFA")],[#text("Masked encoder/pred​ictor")],[#text("Latent/MC score")],[#text("Acquisition curves")],[#text("App I.1 prior mask")],[#text("AFA curves")],[#text("Approximate scoring")],
[#text("AFAPE")],[#text("Target policy/class​ifier")],[#text("DM/IPW/DRL nuisance")],[#text("Target-polic​y rules")],[#text("NDE/NUC/posi​tivity")],[#text("Counterfactu​al cost")],[#text("Offline estimation")],
[#text("This search")],[#text("No new predictor")],[#text("Sharp public world model")],[#text("Fixed query subset")],[#text("Guaranteed closed bins")],[#text("Worst interval width R")],[#text("Exact/epsilo​n B&B")],
[#text("Separate DEV study")],[#text("Same frozen forest")],[#text("One balanced row law")],[#text("Same STOP/abstain")],[#text("Paid tokens only")],[#text("Participant-​macro J")],[#text("Finite recursion")])
]

= #text("3. Problem formulation")

#text("Fixed-subset design. A nonempty compatible-world set Omega defines an original route-minus-static macro loss contrast Delta. Query i has positive integer price c_i and a guaranteed closed-bin observation relation. Choose subset S before any readings. A feasible transcript z restricts the original worlds to Omega(S,z), with sharp endpoints L(S,z) and U(S,z). Empty intersections are impossible readings, never zero endpoints. Closed bins overlap at their threshold, so a boundary world can support both labels.")

#text("The exact representative minimizes the tuple (R(S),c(S),mask(S)) subject to c(S)<=Q. Risk is the maximum conditional interval width over feasible complete readings. The original all-tie contract additionally returned every affordable primary-risk mask and every worst transcript. The new contract returns one canonical representative and one worst witness per completed risk. An epsilon guarantee concerns absolute macro-loss interval-width units, not accuracy percentages or relative prediction regret.")

#text("Sequential prediction. A public state contains paid values/tokens, successful groups S_a, all attempted groups T_a, remaining cap and permitted cache/history metadata. STOP uses the current frozen predictor; ABSTAIN incurs a specified loss. Every attempt is charged, including failures in contracts that contain failure. Current cached DEV has successful returns only, so its attempt and success sets coincide; physical provider reliability is unmeasured. Gold labels and full feature caches are evaluator-only inputs.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ R(S)=max_(z:Omega_(S,z)!=emptyset) [U(S,z)-L(S,z)] $]], [#text("(1)")])
#text("Minimize this width under the query budget, then price and integer mask. It is not the application objective J.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ J(pi)=(1/P) sum_(s=1)^P (E_s(pi)+eta A_s(pi)+lambda C_s(pi))/n_s $]], [#text("(2)")])
#text("Participant means precede equal-person averaging. E counts errors on predictions, A abstentions and C attempted quotes; every planned n_s must be positive.")

#figure(image("figures/decision_contract.svg", width: 100%), placement: top, scope: "parent", caption: [#text("STOP, abstention and paid attempts have separate semantics. Failed attempts enlarge T_a and cost while leaving S_a unchanged; only selected returns become public. The completed cached-DEV study includes abstention but no observed failure outcomes. The general failure branch is an explicit future/application contract, not measured sensor behavior.")])
== #text("3.1. Sharp loss intervals")

#text("The search objective is defined by a finite-participant uncertainty set, not an empirical classification score. Participant j has n_j coordinates, requested coordinates A_j and known stop errors E_j. Requested binary errors share one global cap B_err across all participants; known stop errors equal one and other stop errors equal zero. Independent route/static availability vectors r and v lie in the unit box and each have participant sum n_j/2. The fixed cost is c=1/20 and k is nonnegative.")

#text("Let a_ji indicate a requested coordinate. Its route success is a_ji r_ji. The following losses charge a base route quote plus a requested quote, or two static quotes; k charges failed acquisition. Their equal-person difference Delta is optimized over the declared errors and availability constraints. A query observes a static-availability bin with threshold t_i in (0,1). No new participant, prediction or sensor reading is generated in the constructed search comparison.")

#text("The common endpoint routines optimize these original losses exactly over feasible error placements and box/sum vertices. The global binary cap is not duplicated for each participant. Query observations restrict the same original world set; they do not replace its unknown errors with labels or favorable zeros. This retained world model is what allows the different solvers and the raw-only independent checks to agree on an identical R.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ ell_("route",j i)=(1-a_(j i)r_(j i))u_(j i)+c(1+a_(j i))+k a_(j i)(1-r_(j i)) $]], [#text("(3)")])
#text("Per-coordinate route loss; a is the fixed requested-coordinate indicator.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ ell_("static",j i)=(1-v_(j i))u_(j i)+2c+k(1-v_(j i)) $]], [#text("(4)")])
#text("Per-coordinate static loss, with its independently constrained availability vector.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ Delta=(1/P) sum_(j=1)^P (1/n_j) sum_(i=1)^(n_j) (ell_("route",j i)-ell_("static",j i)) $]], [#text("(5)")])
#text("Sharp L and U are respectively the minimum and maximum Delta over the nonempty compatible original worlds.")

= #text("4. Method")

#text("The primary method solves the fixed-subset R problem with a certified outer frontier and an exact inner width calculation. The separate acquisition diagnostic uses the same explicit information ledger to construct a conditional surrogate and execute paid decisions; it does not optimize R or train a new predictor.")

== #text("4.1. Certified subset search")

#text("An outer node (I,U) represents all affordable subsets between included I and M=I union U. For any verified feasible complete reading on M, projecting its labels to a represented S gives Omega(M,z_M) contained in Omega(S,z_S). Hence the width of that one M reading lower-bounds R(S). Maximizing over a fixed finite bank of such feasible readings remains a valid lower bound. M may itself be too expensive: it is an optimistic relaxation, not a design that the returned policy executes.")

#text("The implementation fixes three public-model worlds: all availability coordinates 1/2, a participant vertex that fills its required n_j/2 mass from the first coordinate, and its reversal. It validates box/mean/error-cap constraints and closed-bin membership. Projected duplicate readings are evaluated once. The resulting bound is cached by M. Positive query prices let the search remove individually unaffordable undecided items and use (LB,c(I),mask(I)) as a lexicographic lower tuple.")

#text("Inside a fixed subset, a partial transcript h contains the worlds of any completed descendant z. Its sharp width therefore upper-bounds descendant width. A completed feasible reading supplies the inner lower incumbent b. Cutting prefix width<=b preserves the numeric maximum and one existing witness, while the original all-tie traversal requires a strict inequality. A partial completed maximum can abandon an outer loser only when its full risk/cost/mask tuple cannot beat the exact incumbent.")

#text("Algorithm 1 combines these different bound directions. Greedy supplies only an exactly evaluated feasible warm start, without a submodularity claim. The frontier covers unresolved subsets and every incumbent comes from an exact feasible risk. At epsilon = 0 the search resolves remaining cheaper equal-risk subsets rather than stopping at scalar gap zero. At positive epsilon, the incumbent upper risk minus the minimum frontier lower bound certifies scalar regret. A handled resource interruption returns uncertified state and restores the active node if present; it does not resume or retry.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ "LB"(I,U)=max_k W(M,z_M^k)<=R(S), quad I subset.eq S subset.eq M $]], [#text("(6)")])
#text("Outer minimization: the reading must be verified feasible. This is a lower bound for every represented affordable S, even if M exceeds the query budget.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ L(h)<=L(z)<=U(z)<=U(h), quad W(z)<=W(h) $]], [#text("(7)")])
#text("Inner maximization: partial-prefix width is an upper bound. The preseal direction witness has R(empty)=1/2 and R({1})=1/3; using the former as an outer lower bound would be invalid.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ L_F=min("UB", min_(v in F) "LB"(v)), quad L_F<=R^*<="UB" $]], [#text("(8)")])
#text("With an empty frontier set L_F=UB. UB-L_F<=epsilon certifies returned-risk regret; at epsilon = 0 canonical price/mask ties still require resolution.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 8.9pt)
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

#figure(image("figures/search_bounds.svg", width: 100%), placement: top, scope: "parent", caption: [#text("Bound directions and a nonzero certificate. Outer search minimizes R and uses verified full-reading lower bounds; inner search maximizes transcript width and uses prefix upper bounds. In the hard Q4 case, epsilon = 1/32 returns UB 21/64 and LB 97/320, a certified gap 1/40. The finite oracle later finds actual regret 0, which does not make that saved certificate exact.")])
== #text("4.2. Guarantees and the strong DP control")

#text("Proposition 1 (canonical exactness). Assume exact sharp endpoints, positive prices and verified feasible seed readings. If the zero-tolerance search terminates without interruption, its returned tuple is the minimum affordable (R,cost,mask). Each retained outer node covers its affordable descendants; removing an individually unaffordable item removes no such descendant. The node lower tuple is no larger than any represented tuple. Thus every pruned node is unable to improve the exact incumbent, while branching covers all remaining subsets. Empty-frontier termination proves the claim. Inner equality pruning preserves the numeric R and one witness, which is the output contract needed by this proof.")

#text("Proposition 2 (absolute certificate). At a positive-tolerance stop, every unresolved design is represented by a frontier lower bound and every resolved loser cannot improve the incumbent. Hence L_F is a lower bound on the global optimum and UB is a feasible upper bound. Subtracting these inequalities gives returned-risk regret at most UB-L_F, which is at most epsilon. This scalar statement does not certify the cheapest mask among equal-risk subsets. Handled timeouts are explicitly uncertified.")

#text("The strong comparison is a memoized value-only subset DP, rather than a traversal that repeats acquisition permutations. Its state M determines remaining budget Q-c(M), and its recurrence compares stopping with every affordable extension. Positive additions cannot lower price or integer mask. If R(M) reaches the shared global seed floor, M is already the canonical winner of its extension family and the DP may stop there. The same exact inner kernel, cold endpoint/local/risk caches, warm-start construction and global floor are granted to both methods.")

#text("Bound and cache overhead can exceed the saved search work. General affordable subsets and subset/reading pairs still grow exponentially, up to 2^N and 3^N before feasibility reductions. Fraction bit lengths, endpoint work, frontier storage and retained output also matter. Greedy is only a feasible warm start: a retained complementarity fixture has R(4)=R(5)=R(6)=3/8 and R(7)=1/4, so a diminishing-returns shortcut would lack its required premise.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ D(M)=min_("lex") {tau(M),H(M)} $]], [#text("(9)")])
#text("The exact tuple is tau(M)=(R(M),c(M),mask(M)). A_Q(M) contains the affordable items outside M.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ H(M)=min_(i in A_Q(M)) D(M union {i}) $]], [#text("(10)")])
#text("All minima use the same lexicographic order; an empty extension family gives an infinite tuple. Terminal or floor-reaching states retain tau(M).")

== #text("4.3. Separate coherent-estimation diagnostic")

#text("The application study holds an inherited forest/prediction bank fixed and compares three estimators. Legacy empirical uses T-window-uniform risks/transitions. Legacy statewise shrinks calibration errors toward T risk while retaining T transitions. The coherent estimator first forms participant-balanced complete-row laws P_T and P_C, then mixes (64 P_T+192 P_C)/256 before conditioning. The state-dependent T/C proportions are generally not 1/4 and 3/4. One row law supplies terminal risks, next-token probabilities and initial-token mass.")

#text("Algorithms 2 and 3 match the frozen code. Common support requires at least 30 T rows and fitting participants 5 and 6 at the current state and every positive T-or-joint successor. Unsupported current states force STOP. Supported fixed orders with a blocked next action retain the better STOP/ABSTAIN decision, without replacing the query. Total budgets 1,2,3 include paid group 0; quote loss is 1/20 and abstention 2/5. Mask 15 and budget 4 are outside the seven-mask bank. All ten global orders may stop/abstain after revealed histories, making them stronger than fully committed subsets.")

#text("Under a sufficient finite state, nonnegative prices, a decreasing attempt horizon and common terminal rights, backward induction minimizes the declared surrogate. Legacy statewise risks and T transitions still define a valid abstract terminal-cost MDP; they need not represent the same complete-row predictive law. For the coherent law, partitioning compatible rows proves direct conditional tree loss equals recursive value. Myopic one-step value differs from eventual replanning-tree loss and is checked separately. These are algebraic identities, not population calibration. The estimator change bundles participant weighting, risks, kernels and initial mass, rather than identifying the causal effect of coherence alone.")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ P_J=(64 P_T+192 P_C)/256, quad P_D=(P_(D,5)+P_(D,6))/2 $]], [#text("(11)")])
#text("Algorithm 2 mixes complete-row laws before conditioning. Each row in D_s has mass 1/(2 n_Ds).")

#grid(columns: (1fr, 2em), column-gutter: 3pt, align: (center, right), [#fit-equation[$ V_b(h)=min {r(h),eta,min_(a in A(h,b)) [lambda c_a+sum_z p(z|h,a)V_(b-c_a)(h a z)]} $]], [#text("(12)")])
#text("At supported states, all families compare the same terminal losses. Unsupported states return the declared STOP fallback. Fixed orders restrict the next query; myopic truncates lookahead to one step.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 8.9pt)
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

== #text("4.4. Frozen planning and paid execution")

#text("Policy tables and the selected fixed reference are frozen using T/C before the DEV bank is opened. Runtime selection sees purchased tokens and its frozen table, not current unpurchased values or labels. In this all-success replay, a selected reveal increments attempted/successful masks and consumes one quote. The purchased cache has no additional acquisition right. The evaluator records full denominator, abstention and paired-error partitions after decisions.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: false)[
#set par(justify: false)
#set text(size: 8.9pt)
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

= #text("5. Experiments")

#text("We evaluate computational efficiency for R and descriptive application loss for J in separate studies. Shared framing makes the comparison rights and denominators explicit; it does not pool their outcomes or treat repeated solver/policy paths as new application samples.")

== #text("5.1. Setup, comparators and measurement")

#text("The search study freezes seven constructed conditions: equality ties, impossible bins, zero shared-error cap with unequal prices, complementarity, a shared-cap tie case, and four independent two-coordinate pairs at budgets 2 and 4. There are four solvers and three cold cyclic orders, giving 84 planned and completed runs. Cyclic orders are descriptive repeated measurements, not independent application samples or a complete four-position Latin balance. The original all-tie solver is unchanged; value-only DP and both B&B variants share the exact one-witness inner routine, cold caches, greedy candidates and global seed floor.")

#text("Arm CPU/wall and tracemalloc peaks include validation, applicable seed construction, warm starts, endpoint/bound/cache/search work and raw event writes. Common imports, terminal receipt serialization and independent oracle have separate recorded scopes. The original all-tie endpoint-call counter excludes impossible-bin attempts, whereas its raw event stream retains those None readings. We disclose that definition rather than comparing unequal counts as the same primitive. Python allocation peak is not RSS, physical I/O or acquisition energy.")

#text("The application comparison reuses 514 complete fitting rows: T participants 5/6 have 168/154 rows and C 96/96. Three estimators, twelve policies and three total budgets produce 108 tables and 56,592 paths on the same 524 previously exposed DEV windows from participants 7/8 (266/258). No predictor is fitted or run anew. All current paths complete; failed/unknown/unstarted are 0 under cached successful returns. Independent final participants remain 0. Direct raw-only audits and distinct normal native review tasks inspect both studies without rerunning their producer experiments.")

== #text("5.2. Primary search results")

#text("All exact solvers agree on risk and the canonical design in every condition. The hard Q4 case has a unique mask 85 and risk 21/64; Q2 has mask 5 and risk 51/128. In Q4, median CPU is 6.96875 s for original all-tie,0.71875 s for strong DP and 0.28125 s for exact B&B. Maximum Python peaks are 231,943/334,535/141,338 bytes. The DP and exact B&B endpoint-call counts are 1,476 and 330 under their common counter; original all-tie reports 1,411 actual feasible calls under its distinct definition.")

#text("Exact B&B beats DP in both median CPU and maximum traced peak on complementarity and hard Q4, 2/7 conditions. Equality, impossible bins, zero-cap, shared-cap ties and hard Q2 preserve DP wins or ties. The shared-cap DP result is 0.203125 s versus 0.25 s for exact B&B and 85,789 versus 137,717 bytes. Table 2 retains all seven conditions; the supplement includes all four solvers and recorded work counters.")

#text("At epsilon = 1/32 every observed finite-oracle regret is 0, while hard Q4 has lower 97/320, upper 21/64 and certificate gap 1/40. Epsilon uses 14 outer nodes versus 47 for exact search. Exact objective gain is 0/no_gain. Figure 4 reports the hard-Q4 computational measurements.")

#figure(kind: table, placement: top, scope: "parent", caption: [#text("All seven constructed conditions. Each cell gives strong DP / exact B&B: median direct CPU seconds or maximum traced Python bytes over three cold cyclic orders. Same exact risk in both methods; joint CPU/peak wins only in complementarity and Q4.")])[
#set par(justify: false)
#set text(size: 8.5pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("Condition")],[#text("CPU seconds: DP / B&B")],[#text("Python bytes: DP / B&B")],[#text("Exact R")]),
[#text("Equality ties")],[#text("0.015625 / 0.015625")],[#text("16224 / 16842")],[#text("0")],
[#text("Impossible bins")],[#text("0.015625 / 0.03125")],[#text("25126 / 27007")],[#text("11/30")],
[#text("Zero cap / prices")],[#text("0.0625 / 0.078125")],[#text("46670 / 72149")],[#text("41/120")],
[#text("Complementarity")],[#text("0.25 / 0.21875")],[#text("73531 / 59281")],[#text("1/4")],
[#text("Shared-cap ties")],[#text("0.203125 / 0.25")],[#text("85789 / 137717")],[#text("3/5")],
[#text("Four pairs Q2")],[#text("0.125 / 0.125")],[#text("66535 / 80798")],[#text("51/128")],
[#text("Four pairs Q4")],[#text("0.71875 / 0.28125")],[#text("334535 / 141338")],[#text("21/64")])
]

#figure(image("figures/search_costs_final.svg", width: 100%), placement: top, scope: "parent", caption: [#text("Hard Q4, three cold cyclic repeats: median direct CPU seconds and maximum traced Python bytes. All exact methods return the same risk 21/64 and unique mask 85. Original all-tie retains more output; the strong DP comparison controls the one-winner inner kernel/cache/warm-start rights. Exact B&B wins CPU+peak over DP in only 2/7 conditions. Epsilon has a saved 1/40 certificate gap, not an exactness claim.")])
== #text("5.3. Separate acquisition results")

#text("The coherent adaptive policy ties its selected fixed order and myopic control on every observed path at all budgets. At budgets 2 and 3 its macro J is 157023/457520, approximately 0.34320. At budget 3 the empirical adaptive J is 1364/4515 and statewise J is 10141/39216; coherent therefore regresses by 8059/196080 and 58067/686280 respectively. Figure 5 shows the full budget contrast, including budget 1 ties.")

#text("At coherent budget 3, participants 7/8 have errors 52/29, abstentions 100/45 and quotes 392/437. The 81 errors are accompanied by 145 abstentions. Against empirical, both policies predict on 379 windows with 5 corrections and 12 harms; 145 switch to abstention. Against statewise, the both-predict subset has 296 windows with 1 correction and 0 harms, plus 145 switches to and 83 from abstention.")

#text("The historical follow-up failed on unavailable mask 15 metadata and an exact-arithmetic abstention bug, with 0/12,576 DEV paths started. The failed run remains separate from the completed present study. All current 56,592 paths complete under cached successful returns; independent final participants remain 0.")

#figure(image("figures/joint_results.svg", width: 100%), placement: top, scope: "parent", caption: [#text("Separate application objective J:3 estimators, total budgets 1–3 and 2 previously exposed people/524 windows; independent final=0. Coherent adaptive equals its fixed/myopic controls. Curves are participant-macro full loss including abstention and attempted quotes. Right: budget 3 paired-error and abstention partitions; corrections/harms use only both-predict windows. No confidence intervals or physical-cost inference.")])
= #text("6. Discussion")

#text("The search result supports an engineering claim under an unchanged objective. Equality pruning removes work because one numeric maximum and one witness suffice; the outer feasible-reading bound can then eliminate subsets before exact evaluation. The matched DP already merges repeated subset orders and has the same warm-start and cache rights, so the Q4 contrast cannot be attributed solely to comparison with an all-tie enumerator. Which saved operations account for the timing difference was not isolated causally. Bound computation and frontier/cache overhead can offset pruning, consistent with the five conditions without a joint CPU/peak win.")

#text("A certificate and an observed optimum answer different questions. The hard-Q4 incumbent happens to match the finite oracle, but its saved lower bound leaves gap 1/40. Reporting that gap preserves what the search knew at termination. Similarly, exact objective gain 0 is expected when both methods solve the same problem. Lower computation cost may make that solution easier to obtain; it does not supply an accuracy gain or a larger information-design benefit.")

#text("The application diagnosis shows why coherent estimation is a method property rather than an improvement theorem. A common row law makes recursive values agree with direct conditional tree loss. It does not make that law calibrated on a new population. The revision jointly changes participant weighting, risks, transitions and initial mass, so the observed regression does not identify coherence as its cause. The pathwise fixed/myopic/adaptive tie provides no observed advantage from extra planning in this policy family. Counting only 81 errors would also omit 145 abstentions and their cost in J; both-predict corrections and harms must be read with the abstention partitions.")

#text("Together the studies locate the supported contribution: conditional certificates and bounded computational improvements for R, alongside a negative exploratory diagnostic for J. The earlier local positive and failed follow-up have different support and terminal contracts and cannot establish unchanged-system progress. A matched external implementation and a newly frozen, untouched final evaluation are follow-up requirements. They are not measured results in this edition.")

= #text("7. Limitations")

#text("The search proofs require the stated static immediate closed-bin world model, verified feasible seed readings, positive prices and correct sharp endpoints. General subsets/readings remain exponential (up to 2^N/3^N), with rational bit, cache, frontier and retained-output costs in addition. Seven small constructed conditions do not establish asymptotic or universal speedup. Greedy is a feasible incumbent heuristic, not a certificate; the original full-tie and new one-winner contracts cannot be conflated.")

#text("Resource guards are cooperative. Independent review found that the generic node guard tests counter>cap and a final callback/pop may increment after the last check, allowing a possible one-node overshoot on that final step. All 84 observed arms are far below 250,000, with no observed cap violation or invalid certificate. We preserve the frozen code and disclose this general boundary; a strict ceiling requires a separate corrected implementation and boundary regression. Timeouts remain explicitly uncertified. No OS isolation is claimed.")

#text("The application has no untouched final participant, provider-failure process, physical sensor cost, clinical validation or external-method reproduction. Coherent conditionals do not guarantee transport; support counts do not certify density, positivity or safety. No-eviction persistent DAG caching has the same ancestor-union cost for a fixed acquired set under any order; only different sets/STOP or additional cache assumptions can change that comparison. Static controls receive the same cache rights. Historical fit, authoring cost, RSS and complete deployment cost remain unmeasured.")

= #text("8. Conclusion")

#text("ProbeFlow provides certified single-winner and epsilon search for the stated information-design problem. CPU/peak improvements over strong DP occur in two of seven conditions. The separate coherent acquisition estimator instead yields ties and regressions.")

]
#pagebreak()
#metadata("main-content-end") <main-content-end>
= #text("Acknowledgements")
#text("This work was created as part of the No-More-Slops group activities at Pseudo Lab.")

= References
#columns(2, gutter: 6mm)[
#set text(size: 9pt)
#text("[1] Hajin Shim, Sung Ju Hwang, Eunho Yang (2018). Joint Active Feature Acquisition and Classification with Variable-Size Set Encoding. Advances in Neural Information Processing Systems 31: 1368-1378")
#link("https://proceedings.neurips.cc/paper_files/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html")[#text("https://proceedings.neurips.cc/paper_files/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html")]

#text("[2] Yang Li, Junier Oliva (2021). Active Feature Acquisition with Generative Surrogate Models. Proceedings of the 38th International Conference on Machine Learning 139: 6450-6459")
#link("https://proceedings.mlr.press/v139/li21p.html")[#text("https://proceedings.mlr.press/v139/li21p.html")]

#text("[3] Gavin C. Cawley, Nicola L. C. Talbot (2010). On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. Journal of Machine Learning Research 11: 2079-2107")
#link("https://jmlr.org/papers/v11/cawley10a.html")[#text("https://jmlr.org/papers/v11/cawley10a.html")]

#text("[4] Oresti Banos, Rafael Garcia, Alejandro Saez (2014). MHEALTH. UCI Machine Learning Repository. DOI 10.24432/C5TW22")
#link("https://archive.ics.uci.edu/dataset/319/mhealth%2Bdataset")[#text("https://archive.ics.uci.edu/dataset/319/mhealth%2Bdataset")]

#text("[5] Yang Li, Junier B. Oliva (2020). Active Feature Acquisition with Generative Surrogate Models. arXiv preprint. DOI 10.48550/arXiv.2010.02433")
#link("https://arxiv.org/abs/2010.02433v2")[#text("https://arxiv.org/abs/2010.02433v2")]

#text("[6] V. B. Zubek, Thomas G. Dietterich (2002). Pruning Improves Heuristic Search for Cost-Sensitive Learning. Proceedings of the International Conference on Machine Learning")
#link("https://web.engr.oregonstate.edu/~tgd/publications/index.html")[#text("https://web.engr.oregonstate.edu/~tgd/publications/index.html")]

#text("[7] Daniel Golovin, Andreas Krause (2011). Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization. Journal of Artificial Intelligence Research 42: 427-486. DOI 10.1613/jair.3278")
#link("https://jair.org/index.php/jair/article/view/10731")[#text("https://jair.org/index.php/jair/article/view/10731")]

#text("[8] Active Feature Acquisition with Incomplete Training Data. arXiv:2609.32325v1.")
#link("https://arxiv.org/html/2609.32325v1")[#text("https://arxiv.org/html/2609.32325v1")]

#text("[9] Learning-To-Measure. arXiv:2510.12624v2; official ICML 2026 bibliography.")
#link("https://arxiv.org/html/2510.12624v2")[#text("https://arxiv.org/html/2510.12624v2")]

#text("[10] SEFA. arXiv:2508.01957v3.")
#link("https://arxiv.org/html/2508.01957v3")[#text("https://arxiv.org/html/2508.01957v3")]

#text("[11] AFAPE. JMLR 26(60), 2025; arXiv:2312.01530v4.")
#link("https://www.jmlr.org/papers/v26/23-1635.html")[#text("https://www.jmlr.org/papers/v26/23-1635.html")]

#text("[12] Tang et al. AISTATS 2026, PMLR 300. Motivation only.")
#link("https://proceedings.mlr.press/v300/tang26d.html")[#text("https://proceedings.mlr.press/v300/tang26d.html")]

]
