#set document(title: "ProbeFlow: Certified Search for Budgeted Information Design — 한국어 해설")
#set page(paper: "a4", margin: 17mm, numbering: "1")
#set text(font: ("New Computer Modern", "Malgun Gothic", "Noto Sans KR"), size: 10pt, lang: "ko")
#set par(justify: true, leading: 0.48em, spacing: 0.55em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 12pt, weight: "bold")
#set figure(gap: 5pt)
#show figure.caption: set text(size: 9pt)
#let fit-equation(body) = layout(size => { let natural = measure(body); let factor = calc.min(1, size.width / natural.width); align(center, scale(factor * 100%, reflow: true, body)) })
#align(center)[#set par(justify: false)
#text(size: 18pt, weight: "bold", hyphenate: false)[#text("ProbeFlow: Certified Search for Budgeted Information Design — 한국어 해설")]]
#v(4pt)
#align(center)[#text(size: 9pt)[#text("Corrected conference narrative edition · 26 October 2026 · certified search and a separate acquisition diagnostic")]]
#v(6pt)
#v(8pt)
#outline(title: "목차", depth: 1)
#pagebreak()
= #text("교정판 요약: 계산 개선과 응용 회귀를 함께 읽기")

#text("이 해설의 앞부분은 이번 교정판의 현재 설명이다. 본문은 동기와 선행연구에서 문제를 세운 뒤 방법, 평가 설정과 결과, Discussion, 한계와 결론으로 이어진다. 뒤의 보존부에는 이전 79절을 제목·문단·알고리즘·그림 구조까지 그대로 남겼다. 보존부의 “현재”와 장·그림 번호는 당시 판본의 말이며 이번 상태로 읽지 않는다.")

#text("완료된 연구는 두 갈래다. 주연구는 고정 질의 묶음의 최악 식별구간폭 R을 같은 값으로 더 적은 계산에 찾을 수 있는지 묻는다. 별개 응용 진단은 공동 행 분포의 내부 일관성이 분류 오류·기권·구매 비용을 합친 J를 좋게 하는지 묻는다. R 탐색의 CPU 감소는 J 정확도의 향상이 아니다.")

#text("정확 B&B가 강한 DP보다 CPU와 Python 할당 peak를 함께 줄인 것은 7조건 중 2조건이다. 정확 R 개선은 0/no_gain이다. coherent J는 비교 추정기보다 회귀했고 자기 fixed/myopic과는 경로까지 동률이다. 노출된 2명·524창, 145기권, 독립 final 0이라는 제한은 그대로다. 새 외부 SEFA 비교와 미노출 final 성능은 아직 없으며 후속 연구다.")

= #text("1. 문제를 나누면 주장도 분명해진다")

#text("R에서는 질의 묶음 S를 예산 안에서 먼저 고정한다. 받은 결과와 양립하는 세계들에서 route−static 손실 차이의 최소 L과 최대 U를 구하고, 가능한 모든 결과 중 가장 큰 U−L을 R(S)로 삼는다. 바깥은 이 최악 폭이 가장 작은 S를 찾는 최소화, 안쪽은 고정 S의 가장 넓은 결과를 찾는 최대화다. 분류기의 관측 정확도와 목적이 다르다.")

#text("대표 하나만 돌려주는 계약은 위험, 비용, mask 순의 사전식 최소를 요구한다. 모든 동률 설계와 모든 최악 결과를 남기는 옛 계약과 출력 권리가 다르다. 따라서 옛 all-tie 열거 대비 절감 전부를 새 bound의 이득으로 돌릴 수 없다. 강한 비교 DP는 같은 inner kernel, witness 하나, cold cache, warm start와 global floor 권리를 받는다.")

#text("J의 실행자는 이미 산 정보와 허용된 비용·cache·실패 표지만 본다. 평가용 전체 특성이나 정답은 선택자의 입력이 아니다. 시도 비용을 먼저 지불하고 선택한 반환을 공개하며 STOP 또는 ABSTAIN으로 끝낸다. 현재 관측에서는 cache 반환이 모두 성공했다. 실제 센서 고장·지연·에너지나 OS 차단을 검증한 계약은 아니다.")

= #text("2. 인증 탐색의 두 bound와 작동 예")

#text("안쪽 최대화에서는 미완성 prefix에 양립하는 세계 집합이 완성 reading의 집합을 포함한다. prefix 폭은 후손 폭의 상한이다. 이미 끝낸 witness의 폭보다 클 수 없으면 witness 하나와 숫자 최댓값만 필요한 계약에서 그 가지를 버린다. 바깥 최소화에서는 더 큰 후보 묶음의 검증된 feasible reading을 작은 묶음에 투영해 폭의 하한을 만든다. 두 방향을 뒤집으면 좋은 설계를 버릴 수 있다.")

#text("hard Q4의 반환 상한은 21/64이고 남은 frontier 하한은 97/320이다. 차이는 1/40이며 허용 epsilon 1/32보다 작다. 이것이 저장된 절대 regret 인증서다. 유한 oracle에서 관측한 regret 0과 알고리즘이 종료 때 알고 있던 gap 1/40은 다른 정보다. epsilon=0에서는 숫자 gap만으로 멈추지 않고 비용·mask 동률도 해결한다.")

#text("종료·실패 경계도 방법의 일부다. 중단 응답은 미인증이며, 현재 cooperative node guard에는 마지막 검사 뒤 node가 증가하여 cap보다 1개 더 갈 수 있는 정적 한계가 남는다. 이를 엄격 ceiling이나 OS 강제로 바꾸지 않는다. 새 strict-cap 수정·검사는 별도 등록 연구가 맡아야 한다.")

#figure(image("figures/search_bounds.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Bound directions and a nonzero certificate. Outer search minimizes R and uses verified full-reading lower bounds; inner search maximizes transcript width and uses prefix upper bounds. In the hard Q4 case, epsilon = 1/32 returns UB 21/64 and LB 97/320, a certified gap 1/40. The finite oracle later finds actual regret 0, which does not make that saved certificate exact.")])
= #text("3. 공동 추정과 유료 실행은 왜 따로 필요한가")

#text("공동 추정기는 fitting 사람 5와 6의 T와 C 행에 참가자 균형 가중치를 주고 (64 P_T+192 P_C)/256을 만든다. 현재 관측 h에 조건화한 같은 행 가중치로 위험, 다음 token 전이, 시작 질량을 계산한다. h에서 두 집단의 질량이 다르면 조건부 혼합 비율을 그대로 1/4·3/4로 둘 수 없다.")

#text("이렇게 만든 유한 행 법칙 안에서는 직접 전체 정책 손실과 Bellman 재귀가 일치한다. 그 항등식은 새로운 사람에 대한 보정·개선 정리가 아니다. 참가자 가중치, 위험, 전이, 초기 질량을 한꺼번에 바꾸었으므로 회귀를 coherence 하나의 인과 효과라고 말할 수도 없다.")

#text("계획은 T/C에서 고정하고 DEV에서 다시 고르지 않는다. 온라인에서는 이미 지불한 group 0에서 시작해 허용 action만 선택하며 재시도·mask·잔여 예산을 기록한다. 과거 실패는 없는 mask 15 metadata와 exact 산술 기권 버그 때문에 DEV 0/12,576에서 멈췄다. 그 실패를 새 완료 연구와 합치거나 봉인 원본을 고쳐 재실행하지 않았다.")

= #text("4. 관측 결과: 이긴 조건과 지지하지 못한 결론")

#text("hard Q4에서 DP와 정확 B&B는 모두 위험 21/64와 mask 85를 찾았다. DP의 CPU 중앙값 0.71875초와 Python peak 334535 bytes에 대해 정확 B&B는 0.28125초와 141338 bytes였다. 두 지표 공동 승리는 complementarity와 hard Q4뿐이다. equality, impossible bins, zero cap, shared-cap ties, hard Q2의 DP 승리 또는 동률도 본문 표와 보충자료에 남겼다. Python peak는 RSS나 센서 에너지가 아니다.")

#text("예산 2와 3의 coherent macro J는 정확히 157023/457520, 다섯 자리 반올림은 0.34320이다. 예산 3 empirical은 1364/4515, statewise는 10141/39216이므로 낮을수록 좋은 J에서 coherent는 회귀다. 자기 fixed-order와 myopic에 대해서는 모든 관측 예산에서 경로까지 동률이다. 새 분모나 통계적 유의성을 추가하지 않는다.")

#text("오류 81개에는 기권 145개가 동반된다. 사람 7/8의 오류는 52/29, 기권은 100/45, quote는 392/437이다. empirical과 둘 다 예측한 379창의 5교정·12피해와 145기권 전환, statewise와 둘 다 예측한 296창의 1교정·0피해와 기권 양방향 분할을 함께 읽어야 한다. 완료 56,592경로는 여전히 노출된 2명·524고유창이며 독립 표본 수가 아니다.")

#figure(image("figures/joint_results.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("Separate application objective J:3 estimators, total budgets 1–3 and 2 previously exposed people/524 windows; independent final=0. Coherent adaptive equals its fixed/myopic controls. Curves are participant-macro full loss including abstention and attempted quotes. Right: budget 3 paired-error and abstention partitions; corrections/harms use only both-predict windows. No confidence intervals or physical-cost inference.")])
= #text("5. Discussion과 한계: 다음 증거가 필요한 이유")

#text("검색 bound의 계산비, frontier와 cache 오버헤드는 가지치기 절감을 상쇄할 수 있다. 일곱 조건 중 다섯 조건의 비승리는 그 범위를 드러낸다. 어떤 연산 절감이 CPU 차이를 일으켰는지는 분리 실험하지 않았다. 같은 정확 문제를 푼 두 방법의 목적값 동률은 예상되는 결과이며 계산 절감을 정확도 상승으로 읽지 않는다.")

#text("하나의 coherent 법칙은 계산의 내부 일관성을 준다. 그 법칙의 calibration과 새 집단에서의 효용은 다른 실증 질문이다. fixed/myopic/adaptive 동률은 이 관측 정책군에서 더 긴 계획의 이익이 없었음을 뜻한다. 노출 DEV의 회귀를 미래 final 개선의 증거로 바꾸지 않는다.")

#text("완전한 외부 원전·구현 대응, 같은 정보·학습·선택·실패·비용 권리 아래 외부 비교, 미노출 final, 실제 provider의 실패·지연·cache 계약, strict cap 검사가 남는다. 이 판은 완료된 문서의 교정판이며 그 후속 실험의 완료표나 최신 공개 Universe 판본이 아니다. 과학 인증·게재 적합성·물리 안전·보편 우위를 주장하지 않는다.")

= #text("6. 정오표: 바뀐 표시와 보존한 원문")

#text("교정 대상은 기존 source.DOCUMENT.json 해시 d84c4b83ae98d918ed20aa32472ede84ab8840749b7ca919397c49eb272d50f0의 /paper/13/paragraphs/0이다. 정확 분수 157023/457520의 0.34321 표기를 이번 활성 본문에서 0.34320으로 고쳤다. 그림 5는 이미 0.34320이었다. 원시 J, 분수, 분모, 회귀·동률 및 결론은 바뀌지 않는다.")

#text("기존 /supplement/136/paragraphs/0과 /explainer/7/paragraphs/0은 exact 보존 대상이다. 새 보충자료 /supplement/137/paragraphs/0과 새 한국어 /explainer/15/paragraphs/0에 같은 문장을 그대로 남겼다. 거기에 보이는 0.34321은 역사 원문의 오기이며 현재 수치로 사용하지 않는다. ERRATA.json에는 원문 포인터, UTF-8 문장 해시와 structured 해시, 정정값 및 이동한 역사 포인터가 연결되어 있다.")

= #text("역사 보존부 시작: 다음 79절은 이전 판본 그대로다")

#text("여기부터는 기존 학회 흐름 안내 1절과 그 이전 한국어 해설 78절을 연속된 역사 보존부로 전재한다. 모든 제목·문단·식·표·그림·알고리즘 구조는 원본과 같다. 그중 “새 판”, “이번 최종판”, “현재”, “미완료”라는 말과 장·그림 번호는 각 원본의 시점을 가리킨다. 이번 교정판의 현재 결과·범위·정오표는 위 0–6절을 기준으로 읽는다.")

#text("보존부의 “6. 실제 J는 회귀했고 같은 정책군은 동률이다” 첫 문단은 0.34321 오기를 의도적으로 유지한다. 정정값은 0.34320이며 바로 앞 정오표와 ERRATA.json이 그 관계를 고정한다. 과거 저자·검토 수락 표현은 당시 한정 범위이며 이번 교정판의 독립 검토 수락이나 과학 인증을 대신하지 않는다.")

= #text("이번 판: 학회 논증 흐름으로 읽기")

#text("이번 편집은 네 개 표제를 강제하는 일이 아니다. 문제와 선행연구 뒤 R·J를 구별하고, 검색·보장·추정·실행을 방법의 하위 절로 둔다. 실험에서는 주연구인 R 검색 결과를 먼저, 별개 J 응용 진단을 다음에 제시한다. Discussion에서는 계산 이득의 조건, 인증 gap과 실제 최적값의 차이, coherent 추정과 성능 회귀의 관계를 해석한다.")

#text("기존 해설 78절과 보충자료 124절은 원문 구조 그대로 보존한다. 아래 기존 장의 번호와 그림 참조는 그 장이 작성된 판본을 가리킨다. 새 본문의 그림 4는 검색 비용이고 그림 5는 J 진단이다. 2/7 계산 이득, 정확 R 개선 0, 145 보류/524 노출창/2명과 독립 final 0, 실패 W50의 DEV 시작 0, 가능한 마지막 node +1을 바꾸지 않았다. 외부 기준선 우위나 새 final 수치는 아직 이 판의 관측 결과가 아니다.")

= #text("새 판의 결론: 계산 이득과 예측 회귀를 구별하기")

#text("이번 최종판은 끝난 두 연구를 함께 설명한다. 인증 탐색은 같은 정보 설계 답을 더 적은 계산으로 찾은 조건이 있다. 공동 행 분포 보정은 내부 계산이 일관되지만 실제 개발 목적값은 나빠졌다. 전자는 구간폭 R의 탐색 비용, 후자는 분류·기권·구매 비용 J의 문제다. 한쪽의 CPU 감소를 다른 쪽의 정확도 향상으로 바꾸지 않는다.")

#text("가장 어려운 네 쌍·예산4 조건에서 정확 탐색과 강한 DP는 모두 위험21/64, 유일 mask 85를 찾았다. CPU 중앙값은 DP 0.71875초에서 정확 B&B 0.28125초, 최대 Python 할당 peak는334535에서141338 bytes다. 그러나 두 지표가 함께 좋아진 조건은7개 중2개다. 독립 최종 사람은0명이며 실용적 우위·보편적 속도 향상·안전 보장은 없다.")

= #text("1. 구간폭 R은 무엇이며 왜 정확도와 다른가")

#text("원래 세계에는 아직 모르는 오류와 가용성이 있다. 한 질의 묶음 S를 먼저 고정하고, 받은 bin 결과 z와 양립하는 세계들에서 route−static 손실 차이의 최소 L과 최대 U를 구한다. U−L은 아직 식별되지 않은 범위다. 가능한 모든 결과 중 가장 넓은 폭이 R(S)다. 이것은 분류기를 얼마나 자주 맞혔는지와 다른 값이다.")

#text("질의 가격은 양의 정수이고 합이 Q를 넘으면 그 묶음은 불가능하다. 정확 대표는 R, 가격, 정수 mask 순으로 작아야 한다. 기존 계약은 모든 위험 동률 묶음과 모든 최악 결과를 돌려줬다. 새 계약은 대표 하나와 witness 하나를 고른다. 계산을 줄일 수 있는 대신 모든 동률을 보존하지 않는다는 차이를 숨기지 않는다.")

#text("closed bin은 [0,t]와[t,1]이므로 경계 t의 세계가 양쪽 label과 양립할 수 있다. 서로 모순되는 결과는 impossible이며 0점이 아니다. 표본 수0으로 평균을 못 구하는 경우와도 구별한다.")

= #text("2. 안쪽은 최댓값, 바깥쪽은 최솟값이다")

#text("안쪽 탐색은 고정 S에서 최악 결과를 찾는다. 덜 읽은 prefix의 세계 집합은 끝까지 읽은 결과의 집합을 포함한다. 따라서 prefix 폭은 후손 결과 폭의 위쪽 한계다. 이미 끝낸 결과 폭 b가 있으면 prefix 폭<=b에서 숫자 최댓값과 witness 하나는 유지한다. 모든 동률 결과가 필요하면 엄격한 <를 써야 한다.")

#text("바깥쪽은 질의 묶음 사이에서 가장 작은 위험을 찾는다. node의 포함 I와 미정 U를 합친 M에서 실제 가능한 결과 하나를 먼저 고른다. 그것을 더 적은 묶음 S에 투영하면 세계 집합이 넓어지므로 그 폭은 R(S)보다 작거나 같다. 이렇게 검증된 하나의 M 결과 폭은 바깥쪽의 아래쪽 한계다. M이 비싸도 낙관적인 완화일 뿐, 반환한 설계가 그 비싼 질의를 실행한 것은 아니다.")

#text("방향을 뒤집으면 틀린다. 보존된 작은 검사에서는 R(빈 묶음)=1/2, 첫 질의 뒤 R=1/3이다. 부모의 폭1/2를 후손의 아래 한계라고 쓰면 더 좋은 질의를 버린다. 그림은 두 방향과 실제 epsilon 인증 숫자를 분리해 보여 준다.")

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

#figure(image("figures/search_bounds.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("바깥 최솟값에는 feasible reading에서 얻은 아래 bound, 안쪽 최댓값에는 prefix의 위 bound를 쓴다. 서로 바꿔 쓰지 않는다.")])
= #text("3. epsilon 인증을 실제 분수로 읽기")

#text("hard Q4에서 반환된 위험 상한21/64는105/320이다. 남은 frontier의 하한은97/320이므로 차이는8/320=1/40, 즉0.025다. 허용 epsilon은1/32, 즉0.03125이므로 저장된 보증은 충분하다. 독립 유한 oracle가 나중에 실제 최적도21/64라고 확인해 실제 regret는0이었다.")

#text("그렇다고 탐색이 exact certificate를 제공한 것은 아니다. 저장 당시의 보증 gap은1/40이다. 관측한 실제 최적값과 알고리즘이 낸 인증서를 구별해야 한다. epsilon 탐색은14개 outer node, 정확 탐색은47개를 사용했다. epsilon = 0에서는 숫자 gap 0만으로 끝내지 않고 가격·mask가 더 작은 동률 후보까지 해결한다.")

#fit-equation[$ 21/64-97/320=1/40<=1/32 $]
#text("UB−LB가 허용 epsilon보다 작으면 반환 위험의 절대 regret를 인증한다. 이는 정확도 퍼센트나 상대오차 보장이 아니다.")

= #text("4. 강한 DP가 이기는 조건도 모두 읽기")

#text("비교 DP는 단순 중복 열거가 아니다. 같은 묶음 M에 도달한 서로 다른 취득 순서를 memoization으로 합친다. B&B와 같은 endpoint, witness 하나용 inner solver, cold cache, greedy warm start, global floor를 받는다. 따라서 이 대조보다 나은 조건을 찾아야 새 bound의 실질 계산 가치를 말할 수 있다.")

#text("정확 B&B가 CPU와 Python peak 둘 다 좋은 조건은 complementarity와 hard Q4다. equality·impossible bins·zero cap·공유 cap 동률·hard Q2에서는 DP가 이기거나 동률이다. 공유 cap 조건은 DP 0.203125초·85789 bytes, 정확 B&B 0.25초·137717 bytes다. 새 방법 이름 때문에 이 음성 결과를 지우지 않는다.")

#text("원 all-tie는 더 많은 답과 동률 label을 남기므로 그 대조와의 차이를 전부 새 outer bound 덕분이라고 할 수 없다. Figure의 Python peak는 RSS가 아니며 CPU는 물리 센서 속도나 에너지가 아니다. 반복3회와7구성 조건은 독립 사람을 늘리지 않는다.")

#figure(image("figures/search_costs_final.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("같은 hard Q4 답을 찾는 계산 비용이다. 전체7조건의 모든 승리·동률·회귀는 Supp 표와 동결 원자료에 남아 있다.")])
= #text("5. 위험과 전이를 같은 행 분포에서 만드는 이유")

#text("새 공동 추정기는 사람5와6에게 같은 무게를 준 T분포와 C분포를 먼저 만든다. 그다음 (64 P_T+192 P_C)/256을 섞고 현재 관측 h에 조건화한다. h에 들어오는 T와 C의 질량이 다르면 조건부 혼합 비율은1/4·3/4가 아니다. 같은 조건부 행 가중치로 위험과 다음 token확률, 시작 문맥 질량을 모두 계산한다.")

#text("이렇게 하면 유한 행 분포 안에서 직접 계산한 전체 정책 손실과 Bellman 재귀가 같다. 이것은 전확률 분해의 항등식이지 새로운 사람에 대한 보정·안전 보장이 아니다. 예측기를 다시 학습하거나 실제 모델을 새로 호출하지도 않았다. 변경은 사람 가중치·위험·전이·초기 질량을 묶어서 바꾼 것이므로 coherence 하나의 인과 효과로 해석하지 않는다.")

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

= #text("6. 실제 J는 회귀했고 같은 정책군은 동률이다")

#text("예산3에서 coherent J는157023/457520≈0.34321, empirical은1364/4515≈0.30210, statewise는10141/39216≈0.25859다. 낮을수록 좋은 값이므로 새 coherent는 둘보다 나쁘다. 자신의 강한 fixed-order와 myopic과는 모든 예산에서 실제 경로까지 동률이다. 내부 일관성을 성능 개선으로 적을 수 없다.")

#text("사람7은 오류52·기권100·quote 392, 사람8은 오류29·기권45·quote 437이다. 사람7의 손실은 (52+(2/5)100+(1/20)392)/266=279/665다. 사람8은459/1720이며 두 사람을 동일하게 평균한다. 오류81개만 말하고 기권145개를 빼면 전체 손실을 숨긴다.")

#text("empirical과 둘 다 답한379창에서는5교정·12피해,145창은 기권으로 바뀌었다. statewise와 둘 다 답한296창은1교정·0피해지만,145개 기권 전환과83개 기권 해제가 따로 있다. 이 작은 교정 숫자로 전체 목적값 회귀를 덮지 않는다. 56592정책 경로도 여전히 노출된2사람·524고유창이다.")

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

#figure(image("figures/joint_results.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("J는 오류·기권·시도 quote의 참가자 균형 손실이다. 구간폭 R의 탐색 성능과 합쳐 하나의 정확도 표를 만들지 않는다.")])
= #text("7. 실패·자원 경계·원전과 보존부를 읽는 법")

#text("원래 W50은 없는 mask 15 정보와 Fraction/float 집계 문제로 실패했다. 그 봉인 파일을 고치거나 재실행하지 않았다. 새 연구는 자기 정상 Task와 새 출력에서 완료했고, 별도 정상 native 검토가 계산의 제한된 사실성을 수락했다. 이것은 canonical 과학 차수 worker_report나 과학적 인증이 아니다.")

#text("탐색 코드의 일반 node guard는 counter>cap을 보고 마지막 callback/pop이 검사 뒤 증가할 수 있어 끝에서1 node를 넘길 가능성이 있다. 실제84 arm은250000보다 훨씬 작았고 관측 위반은 없다. 정적 코드의 한계를 밝힌 것이며 새 위반 실험을 했다는 뜻도 아니다. 엄격 ceiling은 별도 새 수정·검사를 거쳐야 한다.")

#text("같은 질의 집합을 영속 no-eviction DAG로 계산하면 ancestor union을 한 번씩 지불하는 비용은 순서와 무관하다. 다른 집합·STOP·만료·실패 조건이 있어야 순서 효과를 따로 논할 수 있다. static에도 같은 cache권리를 준다. 물리 센서·전체 배포 비용은 아직 측정하지 않았다.")

#text("아래에는 고급v 4 한국어55장과 실제W 49·실패W 50의 설명을 원구조 그대로 보존했다. 당시의 “현재”·미완료 표현은 그 시점의 기록이며 새 판의 상태가 아니다. 새로운 결과와 원전의 정확한 선택 읽기 범위는 앞 절과 SOURCE_BINDINGS, CLAIM_STATUS, BUILD에 연결된다. 옛 원문·실패·기존 최신 선택은 덮어쓰지 않았다.")

= #text("보존부 D. 고급 v4와 실제 W49·실패 W50 원문")

#text("다음 원문은 당시 판본의 구조와 내용을 정확히 보존한다. 과거 pending·현재·추후 검토 표현은 그 시대의 기록으로 읽으며, 앞의 새 결과를 대체하지 않는다.")

= #text("1. 이 책의 질문과 읽는 경로: 정보가 많아지면 언제 더 좋은가")

#text("진단을 내리기 전에 추가 측정을 할지 고르는 일을 생각하자. 이미 본 센서만으로 답을 알 수 있는 창에서는 멈추고, 애매한 창에서만 다른 위치를 읽을 수 있다면 평균 자원을 아낄 가능성이 있다. 하지만 추가 정보가 현재 예측기에 쓸모없거나, 어느 창이 애매한지를 현재 관측으로 알아낼 수 없거나, 간단한 고정 센서가 이미 더 좋다면 적응 정책이 이길 이유가 없다. ProbeFlow는 이 가능성과 실제로 입증된 효과를 구분하는 연구다.")

#text("이 해설은 최초 취득 모델, 유압 자료의 실패와 진단, HAR·Gas·MHEALTH 비교, 관측되지 않은 실패의 부분식별, 정확한 정보 묶음 선택과 heap, 순차 평균·최악폭·순서의 관계, W45~47의 개발 진단을 하나의 논리로 잇는다. 같은 목적을 개선해 온 일직선의 성능 연대표가 아니다. 예측 오류, 확인 가능한 구간폭, 계산량, 실제 물리 취득은 서로 다른 질문이고 자료의 종류도 다르다.")

#text("처음 읽는 독자는1~12장의 정보·확률·비용·자료 단위를 익힌 뒤13~23장의 유압·실데이터·식별 문제를 읽으면 된다. 수학을 재구성하려면24~39장의 식별식·정확 solver·순차 의미·순서 정리를 따라가고, 최신 구현과 평가를 보려면40~48장을 읽는다.49~52장은 출처·비용·검증·다음 acceptance를 연결한다. 학습 경로는 안내일 뿐 학습시간이나 이해도 실측이 아니다.")

#text("모든 실제 숫자는 SOURCE_LINKS의 주장 ID와 고정 파일 hash에 연결한다. 손계산 예시는 별도로 교육용이라고 표시한다. 이 판본은 기존 모델을 다시 학습하거나 추론하지 않는다. 새로운 기술 EDA는 동결된 NPZ 특징 배열과 이미 저장된 정수 결과를 읽어 요약하는 일이며, 새 연구 성능이나 새 독립 표본을 만들지 않는다.")

= #text("2. 용어부터 구별하기: source·특징·예측기·정책·관측")

#text("source는 한 번 취득하는 원천 단위다. 유압 실험에서는 PS1·FS1·TS1 세 채널을 썼고, MHEALTH에서는 위치와 용도에 따라 네 특징 묶음을 정했다. 특징은 원천에서 계산한 평균·표준편차 같은 요약이다. 한 센서에서 특징을 세 개 만들었다고 센서를 세 번 산 것은 아니다. 반대로 같은 원천을 내부에 보관했다고 그로부터 계산 가능한 모든 특징을 정책에 공짜 공개한 것도 아니다.")

#text("예측기 f는 현재 허용된 관측에서 정답을 추측하는 고정 함수다. 정책 pi는 다음에 무엇을 사거나 STOP할지 고른다. 예측기를 더 잘 학습해 정확도가 좋아진 일과, 같은 예측기에서 더 좋은 관측을 고른 일은 구별해야 한다. 정책만 비교하려면 예측기 hash와 모든 관측 mask의 해석을 같게 고정한다.")

#text("관측은 정책이 실제로 받은 값이다. 미구매 UNKNOWN, 원자료의 자연 결측 NaN, 시도했으나 실패한 상태, 정상적으로 받은 값은 서로 다르다. 전체 특징표를 정책에 건네고 미구매 열을 사용하지 말라고 약속하는 것만으로 정보 경계가 생기지 않는다. 현재 구현은 같은 프로세스의 평가자가 허용된 값을 골라 전달하는 협력 인터페이스이며 OS 격리가 아니다.")

#text("label은 활동이나 고장 상태의 정답이며 평가자가 STOP 뒤 점수를 매길 때 쓴다. 개발·감사 분석에서는 label과 전체 배열을 읽을 수 있지만, 이 권한을 실제 선택기의 입력으로 올리면 oracle 정책이 된다. 읽은 출처의 hash는 바이트가 무엇인지 식별할 뿐 내용이 사실이거나 selector가 누출 없이 동작한다는 인증이 아니다.")

= #text("3. 집합과 mask를 손으로 읽기")

#text("세 원천의 번호를 PS1=0, FS1=1, TS1=2라고 두면 mask는 해당 위치의 이진 비트를 켠 정수다. mask0은 빈 관측,1은 PS1,2는 FS1,3은 PS1+FS1,4는 TS1,5는 PS1+TS1,6은 FS1+TS1,7은 모두다. mask5는 원천 다섯 개라는 뜻이 아니다. 네 그룹의 MHEALTH는0~15를 사용하므로 같은 정수라도 어떤 원천 배열의 mask인지 함께 적는다.")

#text("집합 S는 원천 목록이고 순서 pi는 목록을 읽는 순서다. S={A,B}와 순서(A,B),(B,A)는 마지막에 같은 두 값을 가질 수 있지만 행동 기록은 다르다. 가용성·실패·시간 제약이 있으면 마지막 관측도 달라질 수 있다. 반대로 고정되어 항상 즉시 읽을 수 있는 값만 다루면 마지막 정보의 재색인을 통해 일부 목적값이 같아진다. 이 구분이 W44 정리의 중심이다.")

#text("관측 집합 O_t와 시도 집합 B_t는 실패가 있을 때 달라진다. O_t는 B_t의 부분집합이고, 실패한 시도도 B_t와 비용 장부에 남는다. 계산된 모듈 C_t, 이미 가진 원천 O_t, 외부에 공개된 mask m_t를 따로 관리한 초기 상태 설계는 이 차이를 표현하기 위한 것이다. 한 기호 O를 구매 집합과 정상 관측 집합 양쪽 의미로 읽지 않도록 각 연구의 정의를 확인한다.")

#text("연습으로 PS1과 TS1을 갖고 FS1을 아직 사지 않은 상태를 적어보자. 세 원천 체계에서는 mask5이며, FS1의 실제 값·NaN 여부·정답 관련 위험도는 공개되지 않는다. 남은 예산이0이면 FS1이 아무리 유용해 보여도 합법 행동이 아니다. 논리적 집합과 실제 예산이 함께 있어야 가능한 다음 행동을 안다.")

= #text("4. 상태가 충분하다는 말에 필요한 가정")

#text("초기 상태는 공개 값 z, 공개 mask m, 보유 원천 O, 계산 모듈 C, 가용성 v, 남은 예산 b 등으로 쓴다. 상태가 충분하다는 뜻은 같은 상태에 도달한 두 이력이 다음 비용·공개·전이·예측에 같은 의미를 준다는 뜻이다. 예전에 실패한 시도나 deadline이 다음 행동을 바꾸는데 그것이 상태에서 빠지면 값과 mask만으로는 충분하지 않다.")

#text("공유 원천 때문에 문제가 생기는 작은 예를 보자. A와 B가 같은 파일을 전처리한다면 A를 먼저 실행해 파일이 캐시에 있던 상태와, 같은 공개 A값만 외부에서 받았지만 파일은 없는 상태는 이후 B의 비용이 다르다. 공개 값이 같아도 내부 자원 상태가 달라서 앞으로의 최적 행동이 다를 수 있다. 이 예시는 모델링 반례이지 실제 산업 이득 실험이 아니다.")

#text("반대로 내부 캐시에 파일이 존재한다고 정책이 그 파일의 모든 특징을 볼 수는 없다. executor는 계산과 비용을 추적하고, public view는 허용된 값만 내보낸다. 이 두 장부가 함께 있어야 중복 청구와 정보 누출을 별개의 오류로 발견할 수 있다. 과소 청구를 없앤다고 자동으로 관측 권한도 올바르게 되는 것은 아니다.")

#text("따라서 Markov 형태의 상태 표기를 썼다는 이유만으로 보편적인 상태 충분성 정리가 생기지 않는다. 이력과 일관된 observation/transition 모델이라는 조건이 필요하다. 새 failure·chronology·delay를 추가하면 상태와 대조군 모두 같은 전이를 사용하도록 다시 계약해야 한다. [C01]")

#text("공유 DAG의 교육용 두 경로를 비교해 보자. 경로1은 파일 취득→평균 공개까지 했고 경로2는 같은 평균 숫자를 외부 입력으로 받았다. 공개 z와 m은 같아도 O와 C가 달라 다음 표준편차 모듈의 marginal quote가 다를 수 있다. 이후 행동을 동일하게 취급하려면 숨은 자원이 비용에 영향을 주지 않는다는 조건을 추가하거나 상태에 O,C를 포함해야 한다. 이 조건부 반례는 초기 아이디어의 필요성을 보여줄 뿐 세 유압 채널 replay가 일반 DAG 시스템을 모두 구현했다는 뜻은 아니다.")

= #text("5. 확률·평균·조건부 기댓값을 계산하는 순서")

#text("확률은 가능한 세계에 붙인 비음수 가중치이며 합이1이다. 기댓값은 각 세계의 손실에 그 가중치를 곱해 더한 값이다. 교육용으로 오류가0,1인 두 세계의 확률이3/4,1/4이면 평균 오류는1/4이다. 최악 오류는 확률이 작더라도 가능한 세계 중 가장 큰1이다. 평균과 최악은 서로 다른 연산이라 순위를 바꿀 수 있다.")

#text("조건부 기댓값은 이미 관측한 값과 맞는 세계들만 남겨 확률을 다시 정규화한 평균이다. 현재 A=0을 봤다면 A=1인 세계의 손실을 그 다음 행동의 조건부 평균에 넣지 않는다. 하지만 실제 test의 숨은 B나 label을 먼저 읽어 세계를 고르면 허용 정보가 달라진다. 예측한 조건부 분포와 이미 확인한 실제 값을 구별해야 한다.")

#text("참가자 평균은 사람마다 창 오류율을 낸 뒤 사람들을 같은 비중으로 평균한다. pooled 평균은 모든 창을 합친 뒤 한 번 나눈다. 교육용 두 사람의 오류가1/2와0/8이면 macro는1/4, pooled는1/10이다. 둘 다 계산은 맞지만 질문이 다르다. 창이 많은 사람이 최종 점수에 더 큰 비중을 갖는지 여부가 달라진다.")

#text("예정한 참가자의 평가 창 수가0이면 해당 오류율은 계산 불가다. 그 사람을 사후 제거하거나 오류0으로 채워 평균을 좋게 만들지 않는다. 연구는 not_evaluable이나 null 상태를 유지해야 한다. 마찬가지로 두 번째 행동이0회면 그 행동의 실패율·branch 위험 분모도0이고,0%로 보고할 수 없다.")

= #text("6. 오차·quote·lambda·hard cap의 단위")

#text("한 창의 손실을 오류0/1과 lambda 곱하기 quote로 더하면 J=평균오류+lambda·평균quote가 된다. quote1은 계약에서 정한 논리 단위이고, 실제1mJ나1ms가 아니다. lambda=0.05이면 추가quote1을 오류율0.05와 같은 가중치로 평가하겠다는 선호다. 예측 오차의 확률 단위와 물리 비용을 바꾸려면 별도 실측·환산 계약이 필요하다.")

#text("hard cap은 평균 비용 벌점과 다르다. lambda가 작아 유용해 보여도 cap2에서 세 번째 구매는 허용되지 않는다. STOP의 가격0과 빈 관측 STOP의 허용 여부도 미리 고정한다. 실패한 구매를 시도했으면 비용은 지불하고 관측 mask는 늘지 않을 수 있다. 성공한 원천 수만 세면 실패가 많은 정책이 인위적으로 싸 보인다.")

#text("교육용으로 현재 오차0.35가 추가 측정 뒤 기대0.05로 내려가고 추가quote1,lambda0.1이면 순가치0.30−0.10=0.20으로 양수다. 현재 오차0.04가0.02가 되면0.02−0.10<0라 STOP한다. 이 숫자는 실측이 아니며, 정확한 조건부 위험을 알고 있다고 가정한 손계산이다. 실제 평균 mu는 학습오차·분포변화가 있으므로 결정 규칙도 평가 대상이다.")

#text("동일 정보·비용 비교에서는 같은 predictor, 같은 public view, 같은 STOP, 같은 cap과 quote를 모든 정책에 준다. 학습·조건부 위험추정·선택 계산의 비용은 온라인 quote와 별도다. 같게 붙인 source cap 하나만으로 전체 계산 예산이 같다고 말하지 않는다.")

#text("유압 v19의 정확한 목적에는 정규화가 하나 더 있었다. u_i(m)=ell_i(m)+lambda·C(m)/Z, Z=sum_source c_j다. equal quote 세 개가 모두1이면 Z=3이므로 lambda=1/20에서 한 원천의 비용항은1/60이다. 최신 MHEALTH의 J=error+0.05·quotes에는 이 Z=3 나눗셈이 없다. 같은 lambda 표기만 보고 서로 다른 연구의 목적값을 직접 비교하면 안 된다. raw quote6000·600·60도 서로 다른 회계 단위이며 물리 시간·전력이 아니다.")

#fit-equation[$ J(pi) = (1/P) sum_j e_j(pi) + lambda (1/P) sum_j c_j(pi) $]
#text("e_j와c_j는 해당 사람의 창별오류와quote의평균이다. P는 사람 수이고 모든n_j가양수여야한다. 다른식의sourceprice기호c_i와구별한다.")

= #text("7. 한 단계 정보가치와 여러 단계 가치의 차이")

#text("현재 상태 z에서 바로 STOP할 기대 손실을 L(z)라고 하자. g를 사고 도달할 상태 z'의 손실을 조건부 평균하면 한 단계 정보가치는 Delta(g|z)=L(z)−E[L(z')|z,g]다. 추가 가격 lambda*c_g보다 이 감소가 크면 사는 myopic 규칙이 나온다. 이는 미래 관측 후 또 다른 구매가 열릴 수 있다는 효과를 무시한다.")

#text("여러 단계라면 V(z)=min{L(z), min_g[lambda*c_g+E[V(z')|z,g]]}의 Bellman 형태로 생각할 수 있다. 첫 항은 지금 멈추는 선택이고 두 번째 항은 하나 산 뒤 다시 결정하는 선택이다. 남은 cap과 시도 이력이 허용 g를 제한하며 실패도 다음 상태와 예산을 바꾼다. 식을 적었다고 이 조건부 모형이나 최적 정책을 실제로 구한 것은 아니다.")

#text("교육용 XOR에서는 독립 균등비트 A,B의 정답이 A xor B다. 아무것도 안 보면 오류1/2이고 A만 봐도1/2지만 둘 다 보면0이다. A의 한 단계 이득이0이어도 B까지 열리는 경로의 가치는 양수일 수 있다. 이 유한 예시는 가능한 complementarity를 보여주며 현재 센서 자료에서 그 구조를 발견했거나 학습했다는 실험이 아니다.")

#text("W47은 이미 처음 한 그룹을 갖고 남은quote가1인 문제다. 두 번 더 사는 미래 선택 자체가 없으므로 후보의 행동은 같은 지원집합의 local myopic과 정의상 같다. nonmyopic이라고 이름을 붙이거나 논문에서 Bellman 식을 인용해도 이 구현의 동률은 바뀌지 않는다. 새 장기 정책을 주장하려면 실제 상태 전이·지원·강한 대조를 새로 계약해야 한다.")

= #text("8. 실험 설계의 세 층: 예측기·정책 선택·평가")

#text("예측기 학습은 특징에서 label을 예측하는 함수를 맞춘다. 정책-fit은 어느 관측 상태에서 어떤 추가 정보가 나을지 추정한다. development는 후보 정책·threshold를 고른다. 마지막 평가가 독립이려면 이 선택에 쓰이지 않은 사람이나 장비·시간 계보가 있어야 한다. 한 자료를 여러 이름의 표로 나눴다고 독립성이 생기지 않는다.")

#text("유압에서는421개 평가 사이클이 앞선 작업에서 이미 노출되었다. 뒤에 policy lock을 만들고 그 파일을 다시 열었다는 것은 실행 순서의 증거지만 새로운 blind final은 아니다. HAR의 공식 test도 한 번 보고 후속 설계를 고치면 그 새 설계에 대해서는 이미 개발 정보다. MHEALTH의 반복 파생분석 역시 같은 사람과 창을 공유한다.")

#text("교차적합은 한 사람의 조건부 목표를 그 사람으로 학습한 모형이 평가하지 않게 나누는 장치다. 하지만 개발 결과를 보고 여러 규칙 중 고른 뒤 같은 사람에게 성능을 보고하면 선택 편향은 남는다. crossfit이 모든 의미의 독립 최종평가를 자동으로 만들어주지는 않는다. W45의 네 개발 참가자와 W47의 두 DEV 참가자는 모두 노출되었다.")

#text("학습 row·mask 증강 row·정책 경로·윈도·참가자·독립 장비는 다른 단위다. W45의1098학습창을16mask로 늘린17568행은1098개의 원창을 반복 표현한 것이다. W47의524창×16정책=8384경로도524개의 동일 창을 반복 처리한 것이며 독립 참가자는 새로0명이다. [C02,C05,C07,C30-C35]")

= #text("9. 자료 정체: 시계열 행에서69개 특징으로")

#text("MHEALTH 원본은 사람별 연속 로그이며 source 열23개와 label 열을 갖는다. 로컬 admission은 row0에 고정한128행 비중첩 블록을 만든다. 마지막 불완전 블록을 버리고, 완전 블록은 null label을 우선 제외한 뒤 서로 다른 비null label이 섞인 블록도 제외한다. 남긴 블록의 label은1~12의 일정한 정수여야 한다. 이는 실험 정의이며 임상적으로 적합한 진단 창이라는 인증이 아니다.")

#text("채널 하나에서 평균, 모집단 표준편차, 연속값 차이 절댓값의 평균을 계산한다. 각각 전체128행을 사용하므로 창이 끝나기 전에는 사용할 수 없는 요약이다. 채널23개에 특징3개씩69차원이다. group1의 source열1~3은9차원, group2의4~5는6차원, group3의6~14와group4의15~23은 각각27차원이다. 최근 공통 모델은 여기에 관측bit4개를 더해73입력을 쓴다.")

#text("README에는 column13이 중복되고12가 빠진 축 설명 문제가 있다. 원 연구는 사전에 위치 기반 묶음을 동결해 이 물리 축 미확정을 우회하지 않고 명시했다. chest 가속과 ECG는 같은 위치라도 별도 engineering group이며 전체 네 그룹을 독립 물리기기 네 대라고 세지 않는다. 해시가 일치해도 미확정 물리축이 해결되지는 않는다.")

#text("이번 EDA는 원시 로그를 다시 파싱하지 않고 이미 admission된 x,y,offset 배열만 읽는다. offset은 원본 시작행이므로 중복·128정렬·최소간격을 확인할 수 있다. 그러나 제외된 창의 결측·혼합label 이유와 전체 raw missingness를 finite 특징만으로 복원할 수는 없다. 원 archive hash와 admission 이력은 별도 출처로 보존한다.")

#fit-equation[$ mu = (1/128) sum_(t=1)^128 x_t $]
#text("한 채널의 완성창 평균이다. 전체창 요약을 창 시작 시점의 관측이라고 부르지 않는다.")

#fit-equation[$ s = sqrt((1/128) sum_(t=1)^128 (x_t-mu)^2) $]
#text("모집단 표준편차로 분모128을 쓴다. 표본불편분산의127과 다르다.")

#fit-equation[$ d = (1/127) sum_(t=1)^127 abs(x_(t+1)-x_t) $]
#text("평균 절대 연속차이다.128개 값 사이의 차이는127개이므로 분모가 달라진다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 4. 원시 로그에서 admitted128행 특징창으로 가는 역사적 절차")]]
#v(3pt)
#strong[Require] #text("사람별23source열과label열의 동결 로그,행0anchor,사전정한9/6/27/27그룹; 현재판본에서는원파싱재실행안함.")
#parbreak()
#strong[Ensure] #text("각사람의x(n,69),y(n),원본시작offset(n),제외원인과sourcehash;독립사람수는그대로.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("물리축미확정과위치기반그룹승인을먼저기록하고유효하지않은숫자행은실패로남긴다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("행0부터비중첩128행블록을만들고마지막부분블록을먼저제외한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("완전블록의null label을우선제외하고남은블록중mixed nonnull label을제외한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("label1..12가일정한블록의각채널에평균/모표준편차/평균절대연속차를계산해69특징을고정한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("사람/원행offset을보존하고사전에정한fit/calibration/policy/dev/evaluation역할을유지한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("현재EDA는이렇게이미admit된NPZ만검사한다.그유한값으로제외rawmissingness를추정하거나새전처리를fit하지않는다.")]])
#v(1.2pt)
]

= #text("10. 원래 MHEALTH bank와 최근 공통 예측기를 혼동하지 않기")

#text("초기 MHEALTH bank는 subject1~3으로15개 비어 있지 않은 mask별 RF를 맞추고, subject4에서 온도 calibration을 골랐다. 빈mask는 학습 prior다. 정책-fit은5~6, 정책 선택은7~8, 평가 개봉은9~10이었다. 각 RF는48tree·최대depth12·최소leaf3 등 동결 설정을 썼다. calibration은 확신과 STOP을 바꿀 수 있지만 argmax 정확도를 반드시 개선하는 것은 아니다.")

#text("W45의 공통 mask-aware RF는 subject1~4의1098창을16mask로 증강해 하나의 모델로 학습했다.69요약을 학습자료 평균·scale로 정규화하고 미관측 그룹을 가린 뒤 관측bit4개를 붙인다. 이어 개발5~8의 교차적합 conditional tree32개를 만든다. 따라서 초기15mask bank의 훈련·보정 역할과 최근 공통 모델의 역할은 다르다.")

#text("W46·W47은 W45의 공통 예측기와fold0을 재사용하며 새 통계적 fit0이다. fit_participants=[5,6]은 conditional fold0의 근거 사람 두 명이라는 뜻이고 현재 모델을 두 번 새로 학습했다는 뜻이 아니다. pickle hash와 portable export hash도 용도가 다르다. export 수치 일치검사는 바이트 계보를 강화하지만 통계 학습의 타당성까지 독립 인증하지 않는다.")

#text("기존 MHEALTH target527창은 subject9의267창과10의260창이었다. 최근 DEV524창은 subject7의266창과8의258창이다. 단순히527에서3개가 빠진 같은 집합이 아니며 사람·역할이 다르다. 두 표의 분모를 맞추려고 결과를 섞거나 최신 표본을 독립 재현이라고 부르지 않는다. [C07,C30-C34]")

#text("최신 별도 감사가 다시 구성한 historical fit target1542개는 P5의264창+P6의250창=514원창 각각에 현재 가능한 세 추가행동의 손실차 목표를 대응한514×3이다.1542명의 새 사람이나1542회의 새 fit이 아니다. 감사는 이 목표와 동결 leaf의 집계 지원/분포를 맞췄지만, 과거 개별 fit-row JSONL 전체를 다시 확보해 행별 동일성을 인증한 것은 아니다. 실제 학습을 다시 하지 않은 상태에서 가능한 재계산과 남은 계보 한계를 구별한다.")

= #text("11. 실제 EDA1: 배열·누락·활동 분포")

#text("직접 읽은 동결 배열은 P5=(264,69), P6=(250,69), P7=(266,69), P8=(258,69)이다. 네 배열의 특징값은 모두 finite였고 label은1~12, offset은 사람 안에서 중복 없이128의 배수였다. 여기서 finite는 admission된 특징의 검사 결과다. 원 신호에 NaN이 한 번도 없었다거나 제외가 없었다는 뜻은 아니다.")

#text("그림의 각 칸은 한 사람·한 label의 남긴 창 개수다. 행 합은264,250,266,258이며 같은 사람의 연속활동 창들은 종속될 수 있다. 같은 activity label이어도 사람별 세기·신체위치·센서 calibration이 다를 수 있다. class count를 보는 이유는 작은 branch나 label 불균형이 숨지 않도록 하려는 것이며, 이 그림만으로 새 정책을 선택하지 않는다.")

#text("P5·P6은 현재 conditional-fit 감사 자료이고 P7·P8은 노출 DEV다. 세로로 네 사람을 그렸다고 이 네 사람이 독립 final이라고 부를 수 없다. 또한12개 label은 독립 실험12건이 아니다. class별 창 수와 person별 창 수를 같이 읽어야 많이 반복된 활동을 많은 사람의 증거로 잘못 해석하지 않는다.")

#text("EDA.json의 각 source에는 실제 상대경로, SHA256, 배열 키와 bytes를 적었다. 분포를 재계산한 코드도 이 판본 안에 있으며 모델을 import하지 않는다. 유압·HAR·Gas의 원자료는 이번 직접 EDA 범위에 들어 있지 않다. 해당 자료의 기존 집계 결과를 원시자료 EDA인 것처럼 바꾸지 않는다.")

#text("활동12는 네 사람에서 각각8,7,8,7창이고, 여러 다른 활동은24창씩이다. 예를 들어 DEV P7의 label12 비중은8/266=약3.008%, P8은7/258=약2.713%다. 이 차이를 보며 branch support30창이 드문 label 하나의 보장을 뜻하지 않음을 알 수 있다. 현재 support는 label별 기준이 아니고, 이 EDA를 본 뒤 label을 제외하거나 threshold를 바꾸지 않았다.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("직접 기술EDA의 분모와 관측 범위")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("사람")],[#text("역할")],[#text("창")],[#text("특징 nonfinite")],[#text("원시 결측률")]),
[#text("5")],[#text("conditional fit audit")],[#text("264")],[#text("0")],[#text("미재구성")],
[#text("6")],[#text("conditional fit audit")],[#text("250")],[#text("0")],[#text("미재구성")],
[#text("7")],[#text("already exposed DEV")],[#text("266")],[#text("0")],[#text("미재구성")],
[#text("8")],[#text("already exposed DEV")],[#text("258")],[#text("0")],[#text("미재구성")])
]

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("동결 배열의 활동ID별 적격창 수; 활동명 물리해석은 새로 추정하지 않는다.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("활동ID")],[#text("P5 fit")],[#text("P6 fit")],[#text("P7 DEV")],[#text("P8 DEV")]),
[#text("1")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("2")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("3")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("4")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("5")],[#text("24")],[#text("24")],[#text("23")],[#text("24")],
[#text("6")],[#text("21")],[#text("17")],[#text("24")],[#text("16")],
[#text("7")],[#text("22")],[#text("16")],[#text("21")],[#text("23")],
[#text("8")],[#text("21")],[#text("18")],[#text("22")],[#text("20")],
[#text("9")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("10")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("11")],[#text("24")],[#text("24")],[#text("24")],[#text("24")],
[#text("12")],[#text("8")],[#text("7")],[#text("8")],[#text("7")])
]

#figure(image("figures/eda_class_balance.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("실제 동결 NPZ의 활동별 적격창 수. 합1038창은4명이며 현재 DEV는그중2명524창이다. 색은 개수이고 정확도·독립 표본크기가 아니다. EDA.json의 x/y/offset hash와 class_counts에 연결한다. [C34,F5]")])
= #text("12. 실제 EDA2: 특징 scale·관측 mask·누출 경계")

#text("평균·표준편차·차분 요약은 원래 단위가 같지 않고, 서로 다른 채널도 scale이 크게 다르다. 그림은69개 특징 각각의 사람 안 표준편차를 로그축에 그린다. 큰 값이 더 유용한 센서라는 뜻은 아니다. 가속·ECG·기타 위치신호의 단위와 분포가 섞인 그림이므로 물리 강도를 직접 비교할 수 없다.")

#text("scale을 보며 DEV 평균과 분산으로 정규화를 다시 맞추면 모델 입력이 바뀐다. 이번에는 그런 fit을 하지 않았다. 공통 RF의 training-only mean/scale은 predictor_fit.json에 동결되어 있으며 작은 분산의 특징을 어떻게 처리했는지도 원 구현 계약에 속한다. 기술 EDA는 분포를 설명할 뿐 예측기 선택이나 preprocessing 수정이 아니다.")

#text("mask1 상태에서 선택기는 group0의9차원만 실제 관측값으로 쓰고 나머지는 공개 encoding 규칙에 따라 가린다. 관측bit는 미관측값0과 실제값0을 구별한다. 미관측 그룹의 raw label이나 NaN 위치를 읽거나 전체mask 예측을 미리 읽어 action을 고르면 정책 정보가 늘어난다. label은 이 장의 후향 평가에만 사용한다.")

#text("독립 reviewer가 숨은 특징과label 치환으로 selector 불변성을 검사한 것은 협력 인터페이스의 구체적 근거다. 평가자가 같은 프로세스에서 full arrays를 보유한다는 사실은 남아 있으므로 OS 보안이나 악의적 코드 격리를 주장하지 않는다. 실제 deployment와 원시파일 권한까지 검증하려면 다른 경계가 필요하다.")

#text("수치로 보면 P7 G3의 특징별 표준편차 최소/중앙/최대는 약0.005999/1.884158/54.071513이고 G4는0.005365/2.293513/57.349279다. P8의 같은 중앙값은 G3 약2.994561, G4 약2.720799다. 이들은 혼합 단위 특징들의 기술 통계이지 같은 물리량의 센서 성능 순위가 아니다. 모든 네 사람·네 그룹에서 상수 특징 수는0이었지만 이것도 label 예측 유용성을 보장하지 않는다.")

#figure(image("figures/eda_feature_scale.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("69특징의 사람별 표준편차: 로그축, 서로 다른 native단위. 점선은9/6/27/27그룹 경계이며 새 정규화·모델 학습은 없다. [C34,F6]")])
= #text("13. Hydraulic 출발점: 주변 label과 공동 조건 지원")

#text("최초 유압 자료는2205사이클 중14물리 채널의 세 채널만 사용했다. 초기 시간분할에서는 평가의 cooler class가 train에 없어 예측기 학습 전제부터 어긋났다. 학습 prefix를 늘려 각 부품의 주변 class는 보이게 만들었지만,421평가 사이클 중391개의 네 label 공동조건은 여전히 학습에 없었다. 주변 지원과 공동 지원은 다른 문제다.")

#text("주변 지원은 각 부품의 label이 각각 학습에 있었다는 뜻이다. 공동 지원은 cooler·valve·pump·accumulator 네 label이 함께 이룬 tuple이 학습에 있었다는 뜻이다. A부품1과 B부품2를 각각 봤다고 A1+B2 조합을 본 것은 아니다. 한 학습 tuple을 통째로 복사하는 예측기는 이 구분 때문에 출력 가능한 조합이 제한된다.")

#text("선택적 centroid는 확신이 부족하면 abstain하도록 만들었지만 평가에서 전부 abstain했다. coverage0이면 선택된 예측의 risk 분모가 비어 null이다. 이를 오류0의 완벽한 진단으로 보고할 수 없다. 주변 label 지원을 보강한 뒤에도 selective coverage가 회복되지 않았다는 실패가 후속 predictor 진단의 출발점이다.")

#text("이 자료는 한 rig의 이미 노출된421사이클이다. 시간 간격이 있어도 같은 장비·조건과 선행 열람을 공유한다. 이후 판본의 score·gate·반례가 이 데이터를 다시 분석했다는 사실을 유지한다. 새 날짜의 원고나 통계표가 독립 장비 실험을 추가하지 않는다. [C02]")

#text("유압 정책의 root 분기는 획득 원천의 평균만 읽었다. 최종 진단기는 그 원천의 평균·모표준편차·기울기를 쓸 수 있었고, PS1/FS1/TS1의 한 사이클 길이는 각각6000/600/60표본이다. 정책 입력과 진단기 입력이 다르다는 점을 명시해야 한다. root 평균을 본 gate가 아직 공개하지 않은 다른 특징까지 직접 안다고 가정하면 원 연구의 정보권한을 넘어선다.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("유압의 고정 시간역할: 간격과 노출을 독립성으로 오인하지 않기.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("역할")],[#text("cycle ID")],[#text("개수")],[#text("사용")]),
[#text("predictor train")],[#text("1..1540")],[#text("1540")],[#text("동결 predictor bank")],
[#text("policy fit")],[#text("1561..1662")],[#text("102")],[#text("threshold/leaf 작성")],
[#text("policy dev")],[#text("1663..1764")],[#text("102")],[#text("후보 선택")],
[#text("exposed evaluation")],[#text("1785..2205")],[#text("421")],[#text("고정 정책 채점·사후 진단")])
]

= #text("14. prior offset을 빼 얻은25%p의 정확한 의미")

#text("v12는 prior-weighted centroid, 같은 centroid에서 class-prior offset만 제거한 규칙, train-only1NN을 비교했다. 같은 중심에서 채점항 하나를 바꾼 대비가 포함된다. full-source component 오류는0.723872에서0.473872로 줄었고 차이0.25는 cooler head 하나에 집중되었다.")

#text("전체 오차25%p 감소만 읽으면 모든 부품이 고르게 좋아졌거나 acquisition 정책이 성공한 것처럼 보일 수 있다. 실제 개입은 예측 채점규칙이다. 어느 head의 손실이 달라졌는지 확인해야 한다. 더 강한 predictor가 유용하다는 관측과 더 복잡한 정보 선택기가 필요하다는 주장은 별개다.")

#text("선택된1NN도 full-source에서 같은 오류를 냈다. 하지만 원천을 더 주면 항상 좋아지지는 않았다. 특징 scale·joint support·거리 구조 때문에 추가 채널에서 다른 이웃이 선택되고 오류가 늘 수 있다. 정보가 늘었다는 사실을 유한 학습 예측기의 정확도 단조성으로 바로 바꾸지 않는다.")

#text("raw-sample 가격에서 TS1은 full-source 오류를 quote60에 맞췄고 모두 읽으면6660이었다. 이는 채널 표본 수를 가격으로 둔 회계다. 동일 source 가격에서는 선택 고정 정책이 강한 단순 source/order보다 나빴다. 유리한 가격체계의 절약을 실제 에너지나 모든 가격의 우위로 확장하지 않는다. [C02]")

= #text("15. 네 손실을 한 줄씩 유도하기")

#text("사이클i의 네 head 오류를 e_i1,...,e_i4라 하고 합을 k_i라 하자. component 오류는 틀린 head를 모두 더해4n으로 나눈다. vector 오류는 k_i>0인 사이클을 세어n으로 나눈다. worst-head는 head별 전체 오류율을 먼저 낸 뒤 최대를 고르고, pump 오류는 지정한 pump head만 센다. 연산 순서가 다른 성공 정의다.")

#text("k_i는0~4이므로 k_i/4≤1[k_i>0]≤k_i다. 왼쪽은 틀린 head 비율이 하나라도 틀렸다는 지시값보다 클 수 없다는 뜻이다. 오른쪽은 틀린 사이클에 최소 한 오류 head가 있다는 뜻이다. 모든i에 대해 더하고n으로 나누면 C≤V≤min(1,4C)가 된다. 표본 독립성 없이 성립하는 유한 산술이다.")

#text("교육용 두 사이클에서 규칙A의 틀린 head 수가(4,0)이면 C=4/8=1/2,V=1/2다. 규칙B가(1,1)이면 C=2/8=1/4,V=1이다. B는 평균 head가 낫지만 완전 진단은 더 나쁘다. alpha로 두 손실을 섞을 수도 있지만 어떤 선호가 옳은지는 실제 피해 정의에서 먼저 정해야 한다.")

#text("v14의36행은4손실×9가격·예산 선택이다. 이전의4정책×9계약과 숫자가 같아도 다른 분석이며421사이클을 재사용한다. 결과를 본 뒤 유리한 손실을 primary로 바꾸면 선택 편향이 된다. 사전 선택 primary와 사후 민감도를 분리해야 한다. [C03,C36]")

#fit-equation[$ C = (1/(4n)) sum_i sum_(h=1)^4 e_(i,h), quad V = (1/n) sum_i 1_(sum_h e_(i,h) > 0) $]
#text("같은 사이클을 분모n 또는head-cycle분모4n으로 세는 두 정의다.")

#fit-equation[$ C <= V <= min(1,4C) $]
#text("각 사이클의 유한 부등식을 평균해서 얻는다. W=max_h 평균e_ih와V=평균max_h e_ih는 다르다.")

= #text("16. tuple-copy 상한:391개 실패를 피할 수 없는 전제")

#text("T를 학습 네 label tuple의 집합이라 하자. nonempty mask의1NN은 가장 가까운 학습 사이클의 네 label을 통째로 복사하므로 출력은 T 안에 있다. 평가 정답이 T 밖이면 어느 이웃을 골라도 완전히 맞을 수 없다. 평가에서 T 안인 정답은30사이클, 밖은391이므로 vector 성공은30/421=약7.126% 이하다.")

#text("이는1NN 출력군에 관한 조건부 정리다. 출력 가능 집합과 정답 집합의 포함관계에서 나오며 TS1은 지원된30개를 모두 맞혀 해당 예산에서 상한을 달성했다. budget0에서는 빈 mask만 가능해 달성되지 않았다. 정답 tuple이 지원되는 사이클30개를 tuple 종류30개로 바꾸지 않는다.")

#text("빈 mask는 예외를 점검해야 한다. 학습 tuple이(1,0,0,0),(0,1,0,0),(0,0,1,0)이면 head별 mode 조합(0,0,0,0)은 T 밖이다. 일반 modal fallback에 상한을 자동 적용할 수 없다. 실제 bank의 fallback(3,100,0,90)은 T 안임을 별도로 확인했다. 가정과 실제 보조 검사를 나눠야 한다.")

#text("v15의 head별 k-neighbor 투표는 새 tuple을 조합할 수 있다. 미선택 k3/mask3의40/421성공은 tuple-copy 전제 밖으로 나간 결과이며 원정리의 반박이나 선택 정책의 승리가 아니다. 저장 prediction5000행도 독립 사이클5000개가 아니다. [C03,C36]")

#text("상한이 막는 것은 완전 vector 성공이다. 같은 미지원391사이클에서도 pump 오류는 TS1이246/391, FS1이51/391로 달랐다. 완전 tuple을 맞힐 수 없다는 사실이 개별 부품 정보를 모두 무가치하게 만들지는 않는다. 반대로 pump만 낮은 mask를 선택해 vector 목표도 좋아졌다고 보고해서는 안 된다. 독자가 먼저 어느 손실이 목표인지 결정해야 하는 이유다.")

= #text("17. 예측군 확장·joint selection·gate가 남긴 부정 결과")

#text("v15는 k∈{1,3,5,11,31}의 head별 투표를 비교했다. 새 prediction25000기록에서 기존 k1의5000행 일치를 확인했지만 selection은 여전히 k1이었고9가격·예산 선택도 같았다. 표현 가능한 출력이 늘어난 것과 실제 개발 선택·평가가 개선된 것은 다르다.")

#text("v16은 모델을 먼저 고른 뒤 mask를 고르는 방식과 모델-mask를 동시에 고르는 방식을 비교했다. equal-price 선택 세 개가 달라졌지만 강한 TS1/k1은 component 오류가 하나 더 적었다. 최적화 순서를 바꾸면 개발 해는 달라질 수 있어도 노출 평가에 더 잘 전이한다는 보장은 없다.")

#text("v17은102policy-fit에서390gate를 맞추고 다른102dev로 선택해 같은421평가에서90종속 설정을 보았다. primary는 고정 PS1을 유지했고 강제 TS1-first gate는 TS1과 같은 오류에22quote를 더 썼다. k3민감도 여섯 선택은 네 개선·두 회귀였으며 policy-fit의 정답 공동조건은 한 종류였다.")

#text("이 실패는 적응 취득이 원리적으로 불가능하다는 뜻이 아니다. 현재 예측기·leaf·지원·가격·자료에서 어디가 막혔는지 보여준다. threshold나 판본 수를 늘리는 것만으로 정보가 생기지는 않는다. 어떤 제약을 바꿨는지 명명하고 새 독립 평가로 연결해야 한다. [C03,C04]")

#text("gate 학습에서는 fit root 평균의 사분위 위치로 threshold 후보를 만들고 각 branch의 최소 표본과 합법 leaf 조건을 검사했다. root를 포함하고 최대 두 원천인 서로 다른 leaf를 fit 목적값으로 고른 뒤 dev에서 후보 정책을 선택했다. best_fixed는 합법 고정 mask, gate_only는 gate만, adaptive_enabled는 둘의 합집합에서 고른다. 합집합의 dev 최소값이 fixed-only보다 나쁘지 않은 것은 포함관계 산술이며 평가자료의 개선 정리가 아니다.")

#text("fit102사이클은 정답 tuple이(100,100,0,90) 한 종류였고 dev102에는11종류, 평가421에는38종류가 있었다. fit에서 본 tuple에 속한 사이클은 dev2/102, 평가30/421이었다. tuple 종류 수와 사이클 개수를 나눠 읽어야 한다. root가 fit 최소·최대 범위 안이라는 것만으로 밀도 지원이 충분하지 않고, 범위 밖이라는 것만으로 반드시 오답인 것도 아니다. label-combination 지원과 관측값 범위 지원은 다른 축이다.")

= #text("18. 두 oracle과 세 원인 분해를 손으로 유도하기")

#text("실제 gateG와 고정 정책F의 차이를 나눠 보자. 모든 합법 mask에서 정답을 알고 가장 작은 손실을 고른 평균이 A, 현재 두 leaf 중 정답을 알고 고른 평균이 P다. 둘은 사후 진단 oracle이다. 현장 정책은 미구매 값과 label을 모르므로 실현 가능한 baseline으로 쓸 수 없다.")

#text("모든 합법 mask는 두 leaf를 포함하므로 A≤P≤G이며 고정F도 합법이면 A≤F다. H=F−A는 전체 oracle까지의 여지, E=P−A는 leaf쌍이 표현하지 못한 양, R=G−P는 두 leaf 안에서 실제 분기와 oracle의 차이다. A와 P를 더하고 빼면 G−F=−H+E+R이다.")

#text("각 항은 비음수지만 H 앞에는 음수가 붙는다. 여지가 커도 E+R이 더 크면 gate는 고정보다 나쁘다. E와 R에는 root·비용·leaf 제약·공개 정보 부족·동률·학습이 함께 섞인다. 순수한 표현오차·학습오차나 인과효과라고 단정할 수 없다.")

#text("원 primary 분모25260에서 F=13561,A=10201,P=12391,G=12413이다. −3360+2190+22=−1148이므로 PS1 대비 목적은 낮다. 그러나 더 강한 TS1의 목적은 P와 같아 gate의22추가 quote만 남는다. 약한 F 대비 개선을 강한 대조군 대비 개선으로 오해하면 안 된다. [C04,C36]")

#text("실제 저장 cycle2184를 순서대로 따라가자. 먼저 공개 TS1 평균35.442933333333336을 threshold35.44636666666667과 비교한다. 작거나 같으므로 left leaf mask5를 선택해 PS1을 더 읽는다. 그 뒤 예측은[100,100,0,90], 마지막에 평가자가 공개하는 정답은[100,90,0,90]이므로 component 오류1/4다. quote2의 정규화 비용1/30을 더해17/60이다. pair oracle은 같은 예측의 mask4에 quote1만 써4/15라 차이는1/60이다. 이 설명 사례는 사후 선택된 사례이며 그 한 행으로 발생빈도나 일반성능을 추정하지 않는다. [C37]")

#text("보조 k3 사례의 cycle1788에서는 PS1 평균161.01096이 threshold161.03447보다 작아 mask1로 STOP했다. 예측[100,100,0,90]은 정답[100,100,0,130]에서 head1개를 틀려 lambda0의 loss1/4다. 같은 고정 bank의 mask3 예측은 네 head를 모두 맞혔고 pair oracle도 그 leaf를 골라0이었다. 이는 현재 분기가 놓친 양을 보여주지만 전체 mask 출력을 먼저 보고 분기한 실현가능 정책은 아니다. [C37]")

#fit-equation[$ G-F = -(F-A)+(P-A)+(G-P) = -H+E+R $]
#text("동일표본·동일목적·합법mask포함조건의정확한항등식이다. 인과효과의분해나새일반화보장은아니다.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("유압의 저장 설명용10사례: 사후 선별행이며 성능추정 분모로 쓰지 않는다.")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("gate/k")],[#text("cycle")],[#text("공개 root평균")],[#text("실제 mask/loss")],[#text("pair loss")]),
[#text("g129/k1")],[#text("1785")],[#text("36.227300")],[#text("4 / 31/60")],[#text("31/60")],
[#text("g129/k1")],[#text("2184")],[#text("35.442933")],[#text("5 / 17/60")],[#text("4/15")],
[#text("g129/k1")],[#text("1786")],[#text("36.212483")],[#text("4 / 31/60")],[#text("31/60")],
[#text("g129/k1")],[#text("2185")],[#text("35.433333")],[#text("5 / 17/60")],[#text("4/15")],
[#text("g129/k1")],[#text("1812")],[#text("36.191217")],[#text("4 / 23/30")],[#text("23/30")],
[#text("g301/k3")],[#text("1785")],[#text("161.063452")],[#text("3 / 1/2")],[#text("1/2")],
[#text("g301/k3")],[#text("1788")],[#text("161.010962")],[#text("1 / 1/4")],[#text("0")],
[#text("g301/k3")],[#text("1786")],[#text("161.052122")],[#text("3 / 1/2")],[#text("1/2")],
[#text("g301/k3")],[#text("1789")],[#text("161.010892")],[#text("1 / 1/4")],[#text("0")],
[#text("g301/k3")],[#text("1787")],[#text("161.055567")],[#text("3 / 1/2")],[#text("1/2")])
]

= #text("19. pointwise 예측 동률이 비음수 가격 지배로 이어지는 이유")

#text("v24는 mask4와5의 오류 개수뿐 아니라 네 head 예측 벡터 자체를421사이클 모두 직접 비교했다. 벡터가 같으면 같은 label에 같은 공통 손실을 적용한 값도 사이클마다 같다. 서로 다른 부품을 하나씩 틀린 단순 오류개수 동률로는 피해 가중치를 바꾼 손실까지 같다고 말할 수 없으므로 이 직접 비교가 중요하다.")

#text("TS1 고정은 mask4이고 큰 mask5는 PS1을 더 산다. w_i≥0,합1인 사이클 가중치와 큰 mask 선택 확률q_i를 쓰면 예측 손실차는0이다. 비용차 lambda·c_PS1/Z·sum_iw_iq_i만 남는다. 가격과 lambda가 비음수이고 Z>0, 양쪽 mask가 합법이면 음수가 될 수 없다.")

#text("따라서 같은421개·동결 예측·공통 손실·두 leaf 안에서 threshold나 확률 혼합으로 TS1을 엄격히 이길 수 없다.3510가격·가중치 셀은2430동률과1080추가비용이었다. 일반 결론은 격자가 넓어서가 아니라 비음수 인자의 증명에서 나온다. 재가중 셀은 독립 연구가 아니다.")

#text("mask에 직접 의존하는 센서 위험·지연, 새 예측기·사람·source는 다른 조건이다. 실제 물리 피해나 에너지를 측정한 정리가 아니다. 이 좁은 부정 결과를 보존해야 후속 연구가 같은 두 leaf에서 무의미한 threshold 탐색을 반복하지 않는다. [C36]")

= #text("20. HAR와Gas: 적응이라는 이름과 실제 행동")

#text("HAR는14명4996창으로 fit하고7명2356창으로 선택한 뒤 공식9명2947창 test를 평가했다. primary 오류0.10을 dev에서 만족한 후보가 없어 선택 정책은 null이었다. secondary gate는 강한 고정A보다 macro오류를 약0.514%p 줄였지만 quote가1에서 약1.08127로 늘었고 same-STOP 고정순서와 경로가 같았다.")

#text("세 참가자는 오류가, 네 참가자는 secondaryJ가 악화되었다. 작은 평균 개선을 모든 사람의 이득으로 바꾸지 않는다. primary null을 secondary 결과로 덮지 않고 이미 본 test를 후속 수정의 독립 final로 다시 쓰지 않는다. HAR와 MHEALTH의 source 묶음도 같은 정의가 아니다.")

#text("Gas는 batch8~10의4364측정에서 오류3277,quote4364,J=4369/5455였다. route와 강한 myopic이 모두 G4를 한 번 사고 STOP했다. 두 번째 행동0회이므로 적응 branch의 평가 분모가 없다. controller 이름이 routing이라고 실제 조건부 취득이 발생한 것은 아니다.")

#text("두 사례는 강한 단순 대조를 남겨야 하는 이유다. 같은 predictor·STOP·예산의 fixed order나 myopic도 실행해야 한다. 경로까지 같으면 해당 관측에서 추가 정책 복잡성의 효과를 입증하지 못한 no_gain이다. [C05,C06]")

= #text("21. MHEALTH 원평가:527창·129추가구매·지원 실패")

#text("원 MHEALTH route는 subject9/10의527창에서398번 G3 뒤 STOP하고129번 G4를 추가 구매했다. 강한 myopic과 ordered prefix도 같은 행동을 해 primary macro차이는 정확히0이었다. 고정 G3+G4는 높은 quote에서 오류0이었지만 test를 본 뒤 primary comparator를 바꿀 수는 없다.")

#text("dev에서도 두 번째252결정을 전부 G4로 보냈다. target129추가 결정은 희소상태 때문에 모두 same-mask unconditional fallback을 썼다. 서로 다른 두 행동이 충분히 쓰이는지의 branch-support gate를 통과하지 못해 조건부 route 이득을 주장하지 않는다.")

#text("gain 추정의 leaf가 희소해서 unconditional action을 택하는 fallback과, 센서 실패 뒤 기존 G3예측으로 돌아가는 fallback은 다르다. 원 trace에는 후자의129개 G3-only 예측이 없어 실패 민감도를 점으로 확정할 수 없었다. 같은 단어라도 어느 계층인지 구별해야 한다.")

#text("bank는 ChronoSense와 공유했다. 모델·자료 계보가 같으면 두 project를 독립 재현으로 세지 않으며 공통 다운로드·구성을 두 번 물리 실행한 것처럼 청구하지 않는다. 새 연구 이름이 기존 사람을 늘리지 않는다. [C07]")

= #text("22. 관측되지 않은 실패를 확률 하나로 메우지 않기")

#text("실제 trace에는 취득 실패나 늦은 응답이 관측되지 않았다. 그렇다고 일반적인 실패확률0을 얻지는 않는다.129요청창의 G3fallback 예측도 없으므로 실패 뒤 맞을지 모른다. 없는 값을 유리한 예측으로 채우면 순위는 자료가 아니라 가정으로 결정된다.")

#text("W2는18개 가정적 실패·벌점 시나리오를 계산했다. 오류와 실패의 독립 및 zero-penalty 조건에서 손익분기 실패율9653/114400을 얻었지만 실측 failure rate가 아니다. strongest myopic 대비는 여전히 모든 조건에서0이다. 가정 경계와 실제 빈도를 구별한다.")

#text("W5가 독립을 풀자36조건에서6static승,11route승,19엄격순위 비식별이었다. W6은 availability와 fallback공유를 분리한72조건에서 route24승,static24승,양방향 가능24였다. 평균 성공률이 같아도 어느 창에서 실패하는지와 coupling이 다르면 결론이 달라진다.")

#text("관심 Delta의 가능한 최솟값L과 최댓값U를 보고0을 가로지르면 엄격순위를 정하지 않는다. 구간 수축과 부호 식별은 별개다. 구간 전체가 한쪽 부호에 있을 때만 해당 모형 안에서 그 순위를 말한다. [C09,C10]")

= #text("23. 부분식별: 가능한 세계 집합에서 sharp 구간까지")

#text("가능한 세계omega에는 모르는 fallback오류와 availability배치가 들어간다. 원자료와 box·평균·공유 cap을 만족하는 집합을 Omega라 하자. Delta는 route−static의 사람평균 손실차다. L=min_OmegaDelta,U=max_OmegaDelta는 관측과 가정에 맞는 모든 값을 감싼다.")

#text("sharp는 끝점이 넓게 안전할 뿐 아니라 같은 제약의 세계에서 실제 달성된다는 뜻이다. 독립인 사람·policy availability집합에서는 지역 최적해를 이어붙여 끝점 세계를 만들 수 있다. 공유 장치 failure 같은 coupling을 추가하면 이어붙이기가 불가능할 수 있어 원정리를 그대로 쓰지 않는다.")

#text("가정이 모순돼 Omega가 비면 infeasible이다. 빈집합의 min/max를0으로 채우지 않는다. cap은 최대B, exactcount는 정확히B개 오류다. 둘은 가능한 세계를 달리하며 목적의 결합 구조에 따라 끝점도 다르다.")

#text("W7의 upper-count/exact-count 각2340셀에서1806/1810은 수축했지만534/530은 no_gain이었고 새 strict-sign 식별은 없었다. W8도322중58no_gain,placement control92개 전부 동률이었다. 정보 추가가 항상 유용한 결론 추가는 아니다. [C11]")

#text("구간과 순위의 교육용 손계산을 하자. 어떤 모형의 Delta 가능값이[−0.08,0.03]이면 route가 더 좋은 세계와 static이 더 좋은 세계가 둘 다 있어 엄격순위를 정할 수 없다. 추가 정보로[−0.04,0.01]이 되면 폭은0.11에서0.05로 줄었지만 순위는 여전히 비식별이다. [−0.04,−0.01]이면 해당 가정 안에서는 route 손실이 항상 작다. 이 숫자들은 교육용이며 W5/W6 성능표에 추가하지 않는다.")

= #text("24. 원손실식을 한 항씩 빼서 Delta 만들기")

#text("요청 지시값 A_i∈{0,1}, fallback오류 u_i∈{0,1}, route availability r_i, static availability v_i라 하자. c=1/20,k≥0일 때 route손실은(1−A_ir_i)u_i+c(1+A_i)+kA_i(1−r_i), static은(1−v_i)u_i+2c+k(1−v_i)다. 이 식은 선언된 민감도 모형이다.")

#text("route가 요청하지 않으면 A=0이라 u가 남고 요청 성공 비율r만큼 fallback오류가 사라진다. quote는 기본1번과 요청A에 붙고 실패벌점은 요청했으나 실패한 A(1−r)에 붙는다. 실제 센서의 물리법칙이나 관측된 failure식을 발견한 것은 아니다.")

#text("두 식을 빼면(v_i−A_ir_i)u_i+c(A_i−1)+k(A_i−A_ir_i−1+v_i)다. 요청집합A는 u미지, known stop-error E는u=1,다른stop O는u=0이다. availability 합m=n/2를 대입해 D=C−k sum_Ar+sum_Ev+sum_Au(v−r), C=−(n−a)(c+k)+km를 얻는다.")

#text("지역합 D_j를 n_j와 사람 수P로 나눠 더하면 macroDelta이므로 w_j=1/(P n_j)다. 창 수가 작은 사람의 한 창은 더 큰 가중치를 갖는다. pooled로 바꾸면 이 가중치가 바뀌어 endpoint와 선택 query도 달라질 수 있다. [C08,C13]")

#text("식을 빼는 과정의 검산점은 세 곳이다. 첫째 u항은 route의u−Aru에서 static의u−vu를 빼므로(v−Ar)u가 된다. 둘째 c(1+A)−2c=c(A−1)다. 셋째 kA(1−r)−k(1−v)=k(A−Ar−1+v)다. 부호 하나를 잘못 바꾸면 실패가 많은 정책이 유리해지거나 macro 경계가 반대로 갈 수 있다. 원손실을 각 세계에서 직접 계산하는 독립 산술이 이 전개와 다른 구현경로를 갖는 이유다.")

#fit-equation[$ D = C - k sum_(i in A) r_i + sum_(i in E) v_i + sum_(i in A) u_i (v_i-r_i) $]
#text("지역합손실차다. C=−(n−a)(c+k)+k m이며m=n/2는이모형의availability합제약이다.")

#fit-equation[$ Delta = sum_(j=1)^P D_j/(P n_j) $]
#text("요청창·오류head·전체경로가아니라사람별창평균을동일비중으로평균한다.")

= #text("25. 정확 endpoint: box와 합제약의 선형문제")

#text("오류배치u를 고정하면 availability의 목적은 선형이다. l_i≤x_i≤h_i,sum x_i=m이면 먼저 모든 x를 하한에 놓고 잔량 m−sum l을 계산한다. 잔량이 음수거나 총 여유를 넘으면 infeasible이다. 최소화는 계수가 작은 변수부터 상한까지 채우며 최대화는 반대다.")

#text("계수 a_i<a_k인데 i에 여유가 있고 k가 하한보다 크면 epsilon을 k에서 i로 옮길 수 있다. 합과 box는 유지되고 목적은 epsilon(a_i−a_k)<0만큼 좋아진다. 최적점에는 이런 교환이 남아 있지 않아야 하므로 정렬 채우기가 최적이다.")

#text("u는 요청창의 binary배치이므로 지역 오류count별 배치를 열거한다. 사람마다 지역 endpoint를 구한 뒤 정확 count DP로 합쳐 sum b_j≤B를 지킨다. 같은 독립 availability모형 안에서는 최적 배치와 지역해를 이어 sharp끝점을 달성한다.")

#text("정확성이 계산이 작다는 뜻은 아니다. 요청창a_j에2^a_j배치가 생기고 Fraction비트도 커질 수 있다. 단순 outward envelope는 안전해도 달성 증명 없이는 sharp가 아니다. 원손실을 직접 대입하는 별도 audit가 부호·가중치·cap 실수를 찾는다.")

#text("교육용 box 문제 min x1+3x2, x1∈[0,0.6], x2∈[0.2,0.8], x1+x2=1을 계산하자. 하한을 놓으면(0,0.2), 잔량0.8이다. 싼 x1에0.6을 채우고 나머지0.2를 x2에 넣어(0.6,0.4), 목적1.8을 얻는다. 최대는 비싼 x2를0.8까지 먼저 채워(0.2,0.8), 목적2.6이다. 이는 정렬·합제약의 손계산이며 원자료의 availability 실측이 아니다.")

= #text("26. 공유 cap을 복제하면 왜 틀리는가")

#text("두 사람을 합쳐 unknown error capB=1이면 최대 하나의 오류만 허용된다. 각 사람에게 B=1을 따로 허용하고 두 극단을 더하면 합계2오류 세계를 만든다. 원제약 밖의 값이므로 넓게 안전할 수는 있어도 sharp끝점은 아니다.")

#text("W14는 불균일 box와 사람별 다른n으로3636셀을 계산했다. macro/pooled는3506셀에서 달랐고 cap복제식은912셀에서 nonsharp였다.974no_gain과672infeasible도 유지했다. 계산행을 새 사람이나 실제 실패 관측으로 세지 않는다.")

#text("W12는 부모 간이식이 slack조건 밖6548셀 중4913에서 nonsharp임을 발견했다. W10은 의도하지 않은 main재실행과 임시 두 번째raw소실로 failed였고 첫41860셀은 남겼다. W11의 새29120셀 결과가 부모 실패를 지우지는 않는다.")

#text("지역 계산이 쉽다는 이유로 globalcap을 독립budget으로 바꾸지 않는다. coupling을 유지하는 정확DP인지 고의로 relax한 outward bound인지 명시한다. relaxation의 안전성과 exactness는 별도 증명이다. [C12,C13]")

= #text("27. 정보를 보기 전에 고정하는 minimax subset")

#text("query subsetS는 값을 보기 전에 고른다. 각 query는 availability v_i가 threshold t_i의 아래·위 bin 중 어디에 속하는지 보장한다. label0은[0,t_i], label1은[t_i,1]로 경계가 겹친다. 반열린 bin으로 몰래 바꾸면 가능한 세계가 달라진다.")

#text("고정S의 완전 readingz마다 compatible world의 sharp구간[L,U]를 구한다. 폭 W=U−L은 정보를 본 뒤 남는 Delta 불확실성이다. R(S)=max_zW(S,z)는 가능한 reading 중 최악폭이다. 값을 본 뒤 subset을 바꾸면 adaptive라는 다른 정책문제다.")

#text("C(S)≤Q인 S 중 R을 최소화하고 그다음 price,그다음 numericmask로 canonical한 개를 정한다. primaryR만 같은 모든 합법 subset은 별도 반환한다. 더 비싼 tie를 canonical에서 밀렸다는 이유로 지우면 full-tie 계약을 어긴다.")

#text("W15는8작성설계·368subset·3726reading·73budget결정에서44개선/29no_gain을 얻었다. 이는73독립 참가자나 물리 query효용이 아니다. exactsolver는 선언한 모형을 빠짐없이 최적화하며 그 목적의 응용가치는 별도 근거가 필요하다. [C08,C14]")

#text("minimax의 결정 순서는 sum이나 max의 기호보다 먼저 읽어야 한다. 먼저 모든 후보 S를 아직 값이 없는 상태에서 정한다. 각 S에 대해 가능한 z를 전부 상상하고 각 z에서 남는 Delta 범위를 계산한다. 그중 가장 넓은 폭이 R(S)다. 마지막으로 가격 합법인 S들 중 이 최악폭이 작은 것을 택한다. min_S max_z의 min과 max를 바꾸면 값을 본 뒤 S를 고를 수 있는 다른 정책권한이 된다.")

= #text("28. solver 전체 절차와 실패·종료를 따라가기")

#text("전체 흐름은 입력검증→subset열거→reading DFS→endpoint→risk/ties→budget선택이다. field·차원·price·threshold·globalcap·box합을 먼저 검사한다. 불가능조건을 작은 구간으로 고쳐 통과시키지 않고 infeasible로 남기며 hash불일치를 같은 실험으로 부르지 않는다.")

#text("고정S의 트리는 선언된 coordinateorder를 쓴다. 완전 feasibleleaf에서 최악폭 incumbent를 갱신하고 같은 폭의 label을 전부 붙인다. prefix에서는 인증된 폭상한으로 잘라낼 수 있지만 동률을 남기는 strict조건이 필요하다. 완성 feasibleleaf가 없으면 임의 incumbent로 자르지 않는다.")

#text("마지막에 feasibleleaf·impossible subtree·strictpruned subtree의 completion수를 합쳐 전체 label가족과 맞춘다. 모든 S의 위험을 보관한 뒤 각Q에서 가격합법성·lex선택·primarytie를 구분한다. coverage를 생략하면 누락된 최악 reading을 낮은 risk로 오인할 수 있다.")

#text("연구 당시 main/unit/oracle와 이번 문서 selfcheck는 역할이 다르다. 이번에는 그 study코드를 import·재실행하지 않았다. 문서검사는 schema/hash/저장 산술이며 실패prefix와 미실행 분모를 보존하고 중단된 model/main을 자동 재전송하지 않는다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 5. 고정subset의정확worst-width선택과전체동률보존")]]
#v(3pt)
#strong[Require] #text("동결가능세계/box/평균/공유cap·querybin·양의price·budgetQ와canonicalorder. 정확endpoint또는인증된outwardprefix상한,완성leaf/risk/tie출력규약.")
#parbreak()
#strong[Ensure] #text("모든subset의정확risk·모든worstreading,각Q의canonical해와전체primarytie·coverage·실패장부.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("field·차원·hash·cap·price·threshold와feasibility를검사한다. 불일치/불가능을감추지않는다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("값을보기전고정S를열거하고선언한coordinate순서의readingDFS를시작한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("가능한완성leaf에서원손실sharpL/U와width를계산하고최대·동률을전부축적한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("prefix의compatibleworld가descendant를포함함을이용해폭상한을구한다. 완성feasibleincumbent가없으면cut하지않는다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("상한이incumbent보다엄격히작을때만cut한다. 같은값이면동률가능하므로탐색한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("feasible/impossible/prunedcompletion분할을검산한뒤모든S의risk를보관한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("C(S)<=Q로합법subset만남기고risk/price/masklex선택과전체primaryrisk동률목록을별도로반환한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("별도원손실audit·비용장부와연결한다. 실패/unknown은고정하고중단모델호출이나main을자동재전송하지않는다.")]])
#v(1.2pt)
]

= #text("29. prefix containment와 엄격한 가지치기 증명")

#text("prefixh의 세계 Omega_h는 이를 완성한 readingz의 Omega_z를 포함한다. 집합이 줄면 최솟값은 내려갈 수 없고 최댓값은 올라갈 수 없다. L(h)≤L(z)≤U(z)≤U(h)이므로 W(z)≤U(h)−L(h)다. 이것이 하위트리의 폭상한이다.")

#text("이미 끝낸 feasibleleaf의 최대폭b는 R(S)의 하한이다. 어떤 prefix의 폭상한이 b보다 작으면 그 아래에 최대나 최대동률이 없어 잘라도 된다. 상한=b이면 동률 reading이 남을 수 있다. 숫자 최대만 필요한 계약과 모든 최악 label을 내는 계약의 부등식은 다르다.")

#text("교육용으로 b=1/3,다른 prefix상한=1/3이면 ≤cut은 그 아래의 동률을 잃을 수 있다. <만 써야 한다. outer최소화에서 상한1/2를 현재 best1/3과 비교해 subset을 버릴 수도 없다. 실제값1/3일 가능성을 상한은 없애지 않는다.")

#text("W19는 feasibleleaf837→642로 줄었지만 endpoint837→1370,rawbytes183934→287257로 늘었다. bound계산도 일을 쓰기 때문이다. 가지치기 논리가 맞다는 것과 전체 비용이 준다는 것은 다른 명제다. [C16,C18]")

#text("정보가 추가돼 compatible world가 줄면 한 transcript의 폭은 커지지 않는다. 그러나 prefix traversal에 필요한 endpoint 호출 수는 커질 수 있고, 전체 subset의 최적 위험도 query 가격·예산의 영향을 받는다. '폭 단조성'·'탐색 비용 감소'·'선택된 정책의 실제 오류 감소'를 하나의 단조성으로 묶지 않는 것이 이 증명을 읽는 핵심이다.")

#fit-equation[$ Omega_z subset.eq Omega_h => L(h) <= L(z) <= U(z) <= U(h) $]
#text("prefixcontainment는최대화안의상한을준다. outer최소화의하한으로쓰지않는다.")

= #text("30. greedy와 adaptive submodularity를 바로 빌려올 수 없는 이유")

#text("정보가 추가되면 한계이득이 체감한다는 직관은 자동 정리가 아니다. submodular gain은 작은 집합의 추가이득이 큰 집합의 추가이득보다 작지 않아야 한다. 현재 worst-width에는 함께 있어야 유용한 complementarity가 있어 이 조건을 위반할 수 있다.")

#text("저장 반례 R(4)=R(5)=R(6)=3/8,R(7)=1/4에서 같은 추가항목의 이득은 작은 집합에서0,큰 집합에서1/8이다. stale0을 미래 한계이득의 상한으로 쓰면 좋은 조합을 놓친다. 현재 목적의 반례이지 원 Bayesian정리의 반증은 아니다.")

#text("W18의3사례는84subset·819reading 중730feasible/89impossible이었다. cost-ratio heuristic은 budgettrap에서 regret1/60을 냈다. 다른 prior·목적·정책class의 heuristic을 같은 정확문제의 열등한 구현이라고 부르지 않는다.")

#text("adaptive-submodularity 문헌은 검증된 metadata·abstract·revisioncomment 범위로 인용한다. 현 목적의 원가정 충족을 증명하지 않았고 후기 정정의 추가조건도 남는다. 인용이 있다는 것과 보장 전이가 있다는 것은 다르다. [C15,adaptive-submodularity]")

= #text("31. 국소 outward envelope를 식에서 만들기")

#text("sharpendpoint보다 싼 안전구간을 만들자. A,E,O의 box합을 l_A,h_A,l_E,h_E,l_O,h_O라 하자. route합m과 각창0~1에서 요청부합의 rL=max(0,m−(n−a)),rU=min(a,m)가 나온다. 요청 밖에 최대 n−a를 채우고도 남는 양이 하한이다.")

#text("static의 E합은 eL=max(l_E,m−h_A−h_O),eU=min(h_E,m−l_A−l_O)다. E밖 최대를 채운 뒤 남겨야 하는 양과 E하한 중 큰 값을 택한다. k≥0이므로 −k sum_Ar의 최소는 rU,최대는 rL에서 나온다.")

#text("coupling T를 빼면 base지역구간은[C−krU+eL,C−krL+eU]다. 사람별 w를 곱해[L0,U0]를 얻는다. 오류countb의 T는 아래−min(b,a−l_A),위 min(b,h_A)로 감싼다. base와 correction을 따로 최적화해 동시 달성되지 않을 수 있어 outward다.")

#text("B=0이면 T가 사라져 독립모형의 base가 달성된다. B>0은 local coupling relaxation이 남아 sharedcap 배분을 정확히 해도 sharp와 일반적으로 다르다. L_relaxed≤L_shared≤L_sharp≤U_sharp≤U_shared≤U_relaxed를 구별한다. [C17,C19,C20]")

#text("base와 correction을 따로 고르는 것이 왜 relaxation인지 교육용으로 생각하자. 같은 r변수에 대해 base를 작게 만드는 값이r=1이고 coupling을 작게 만드는 값이r=0이라면 두 최솟값의 합은 한 실제 r에서 동시에 달성되지 않을 수 있다. 그래도 각각 모든 세계의 항보다 작거나 같으므로 합은 안전한 하한이다. '안전하다'와 'sharp하다'의 차이는 바로 동시 달성 가능성이다.")

= #text("32. 공유 budget DP와 heap의 정확성 유도")

#text("한 부호의 사람별 correction은 f_j(b)=w_j min(b,c_j)다. minus는 c_j=a_j−l_A,plus는 c_j=h_A다. b는 정수count이고 sum b_j≤B다. DP는 사람을 하나씩 더하며 오류수별 최대합을 보관해 공유budget을 유지한다.")

#text("t번째 한계이득은 f_j(t)−f_j(t−1)=w_j min(1,max(0,c_j−(t−1)))다. c가 분수여도 앞부분은w,한 항은 분수곱w,이후0이므로 비음수·비증가다. b개 배분은 이 chain의 앞b항을 택하는 것과 같다.")

#text("각 chain의 첫 미선택 양수항만 heap에 넣는다. 전체 미선택 최대는 어떤 head여야 한다. 뒤 항이 head보다 클 수 없기 때문이다. 최대 head를 pop하고 그 chain 다음 항을 넣으면 매 단계 전역 최대 남은 항을 얻는다. B회 또는 양수 소진까지 반복한다.")

#text("어떤 합법배분도 B개 이하 chainprefix를 고르므로 이 상위합을 넘을 수 없다. heap은 상한을 달성해 DP와 scalar가 같다. 할당 tie가 여러 개여도 subset/reading 전체tie를 지울 수 없다. 교체되는 것은 envelope배분이며 sharpendpoint는 별도다. [C19,C20]")

#text("DP의 의미도 한 줄씩 적을 수 있다. D_j(b)를 처음 j명의 correction을 합해 정확히 b개 count를 썼을 때의 최대라 하면 D_j(b)=max_t[D_(j−1)(b−t)+f_j(t)]다. t는0부터min(b,a_j)까지이며 불가능 state는 별도로 남긴다. at-mostB 답은b≤B 중 최대다. heap은 이 DP 목적의 특수한 nonincreasing marginal 구조를 이용한 동치 알고리즘이지 일반적인 임의곡선 knapsack의 해법은 아니다.")

#fit-equation[$ delta_j(t) = w_j min(1,max(0,c_j-(t-1))) $]
#text("비음수·비증가chain이므로head최대heap이globallylargest남은marginal을정확히택한다.")

= #text("33. heap 손계산과 실제 비용표 읽기")

#text("교육용으로 w=(1/4,1/6),c=(3/2,2)면 chain은(1/4,1/8,0,...)와(1/6,1/6,0,...)다. B2에서1/4 뒤1/6을 택해5/12, B3은 다시1/6을 더해7/12다. 이 값은 설명용이며 실제 연구 성능표에 합치지 않는다.")

#text("W39는2사람·5좌표와 두 cap에서64risk·486label·20budget선택을 검산했다. B1 endpoint는 cap-relaxed208→shared201이었지만 strong sharp-prefix는121이었다. linear480과 단회CPU도 동률이다. 약한 대조의 한 열 개선으로 효율우위를 말할 수 없다.")

#text("W41는3사람·7좌표,두 cap의256risk·4374label·26budget선택이었다. B2의13budget은 전부 빈subset과 위험동률이었다. heap=DP의 값과 fulltie는 유지했지만 추가 endpoint/prune이득은0이다. 정확성과 실제 가치의 공백을 함께 읽는다.")

#text("B2단회 CPU는 sharp8.921875초,DP24.5초,heap22.875초다. heap peak4350232/output1099471bytes는 DP4347301/1090097보다 컸다. traced peak는 RSS가 아니고 file길이는 physicalIO가 아니다. 반복 timing이 없어 안정적 speedratio나 불확실성은 추정하지 않는다. [C19,C20]")

#figure(image("figures/w41_costs.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("공유 한계이득 heap 연구B2단회계측:값과동률은같지만strongsharp가더낮은CPU였고heappeak/output은DP보다컸다. MB는1,000,000bytes이며전체deployment비용이아니다. [C20,F2]")])
= #text("34. 복잡도에서 세야 하는 것: 산술·비트·출력")

#text("N좌표의 모든 subset과 binaryreading 합은 sum_S2^|S|=(1+2)^N=3^N이다. 좌표마다 미선택/0/1세 상태를 고르는 같은 계산이다. heap이 싸져도 전체 탐색과 모든tie 출력은 지수적일 수 있다. streaming은 보관량을 바꾸며 가족크기나 목적을 없애지 않는다.")

#text("rational-operation수는 Fraction연산을 한 단위로 센다. 실제 곱·GCD·비교는 정수bit가 커지면 비싸다. 반환값7bit 관측은 중간곱 최대나 일반 bitbound가 아니다. hash·복사key·DFSframe·직렬화raw도 비용과 공간을 쓴다.")

#text("allocation DP는 대략 sum_j B min(B,a_j)전이와 O(B)rolling층을 쓴다. heap은 집계 포함 O(N+P+q log max(2,P)),q≤min(B,sum a_j),heapspaceO(P)다. 이 식은 allocator범위이며 전체 sharp열거·subsetDFS·fulltie출력의 bound가 아니다.")

#text("W42의 O(Km²h²)는 h0 STOP-only의 비영 예측·평가를 빠뜨렸고 Omega(KT)는 공유child와 직렬화 전체길이를 구분하지 않았다. 검증된 일반정리로 쓰지 않는다. Lbytes직렬화에는 적어도 L쓰기 비용이 있지만 최대tree길이T만으로 총KT를 증명할 수 없다. [C20,C22]")

= #text("35. 순차 예측과 fixed worst-width는 왜 다른가")

#text("GSMRL계열은 순차 특징구매·STOP 뒤 예측loss+price의 기댓값을 줄인다. 현재 정확정보설계는 값을 보기 전 S를 고정해 Delta식별폭의 최악을 줄인다. target·목적·policyclass가 달라 일반 동치가 아니다.")

#text("제한 환원에는 같은 세계·public관측·가격·hardbudget이 필요하다. 순차정책도 precommittedsubset의 open-loopreveal로 제한하고 공통order 또는 terminalquotient를 정한다. 그다음 terminal loss를 g(S,omega)=W(S,x_S(omega))로 바꾸는 bridge를 넣는다. 원래 활동label 예측과 다른 합성 target이다.")

#text("고정분포에서 모든 feasible reading확률p_t>0이면 M−E[W]=sum_t p_t(M−W_t),M=maxW다. 각 항이 비음수이므로0이려면 모두 W_t=M이어야 한다. 따라서 policywise평균=max에는 모든reading폭이 일정하다는 강한 조건이 필요하다. optimizer가 우연히 같다고 목적전체가 같은 것은 아니다.")

#text("alpha0,같은 hardbudget과 별도 price/masklex·primaryties도 필요하다. 양의 additiveprice는 다른price의 risk동률 중 싼 것만 남길 수 있다. 분포전체sup로 max를 복원하면 fixedprior를 robust문제로 바꾼 것이다. [C21,C22]")

#text("정가중가격을 넣으면 값 동치와 동률 동치가 어떻게 달라지는지 보자. 두 subset의 primary risk가 둘 다0.3인데 price가1과2이면 alpha>0의 합산목적은0.3+alpha와0.3+2alpha라 비싼 해가 탈락한다. 원래 출력이 'risk0.3인 모든 subset'이었다면 이 합산 minimizer만 반환하는 것으로는 계약을 복원할 수 없다. 작은 alpha가 lex 한 개를 보존할 수 있다는 주장과 full primary ties를 보존한다는 주장은 별도다.")

= #text("36. 순차 목적 분석 첫 예제를 손으로 계산하기")

#text("세 세계는(A0,y0,p1/4),(A0,y1,p1/2),(A1,y0,p1/4)다. 처음 y0/y1확률이1/2씩이라 tie규칙으로0을 예측해 오류1/2다. A0을 보면 y1확률2/3이라1을, A1이면0을 예측한다. 구매 뒤 전체 오류는 첫 세계의1/4만 남는다.")

#text("price1,alpha1/8이면 buy기대목적은1/4+1/8=3/8,STOP은1/2다. 반면 worst오류는 buy에서도1이라 가격을 더하면9/8이고 STOP의worst1보다 나쁘다. 같은 정책과 정보도 기대·최악 목적이 선택을 바꾼다.")

#text("Delta=y의 width는 빈관측에서1,A0에서1,A1에서0이다. fixedsubsetrisk는 max라 빈집합과 A 둘 다1이다. 평균 pricedprediction과 fixedworstwidth를 동일 성능열로 비교할 수 없다.")

#text("두 publicpolicy와 두 subset의12world산술을 포함한 작은 이론 witness다. 학습GSMRL재현이나12독립 실제표본이 아니다. 확률·Bayestie·가격을 그대로 써야 손계산을 재구성할 수 있다. [C21]")

= #text("37. 순차 목적 분석 둘째 예제: adaptive STOP의 기대가격 이득")

#text("세 세계는(A0,B1,y0,p1/2),(A1,B0,y0,p1/4),(A1,B1,y1,p1/4)다. A를 먼저 보고0이면 y0으로 STOP,1이면 B를 사면 정답을 안다. 첫 quote1은 항상 쓰고 둘째는 확률1/2라 기대price3/2다.")

#text("alpha1/16에서 adaptive는 오류0,목적3/32다. staticAB는 항상 둘 다 사 price2,목적1/8이다. A0일 때 B가 필요 없다는 공개조건을 쓴 기대비용 절약이다. 숨은 label을 먼저 본 oracle행동은 아니다.")

#text("하지만 둘의 worstprice2,worsterror0,worstwidth0은 동률이다. adaptive기대이득을 fixedworstwidth알고리즘의 패배라고 하면 목적과 정책권한을 바꾼다. 두 질문을 나눠 보고해야 한다.")

#text("항상 affordable인 binarytree수는 F(n,h)=1+n F(n−1,h−1)²,F(n,0)=1이다. STOP하나와 feature선택n개,양 reading의 subtree선택을 센다. F(2,2)=9다. 두 예제합11policy·6subset·51worldcheck는 검산분모이며 새 실제사람0명이다. [C21]")

= #text("38. 말단 순서 분석 terminal permutation 정리: 무엇이 보존되는가")

#text("static모형은 ID값이 읽는 동안 고정되고 즉시 항상 가능하며 실패·delay·chronology가 없다. S를 미리 정해 끝까지 읽는다. orderpi의 positionaltuple을 ID→label사전으로 바꾸고 다른order대로 읽으면 재색인할 수 있다.")

#text("역변환이 있어 전단사다. 각 ID의 관측조건이 같아 compatibleworld가 같고 같은 Delta의 min/max·width·최악IDreading도 같다. additiveprice와 affordability·primarytie도 같다. outer모든subset의 결론은 이 정리에서 나오며 새 전수실행이 아니다.")

#text("literalactiontrace는 보존하지 않는다. A먼저와 B먼저는 다른 행동기록이다. prefixbound·cache·incumbent·prune·CPU도 달라질 수 있다. 마지막 정보의 같음으로 orderedprogram이나 solver진단까지 같다고 하지 않는다.")

#text("W41은 stop-error우선/index, W42는 increasingindex였다. W44는 staticterminalquotient를 연결하지만 이전 orderedprogram동치를 소급 인증하지 않는다. GSMRL time-series도 이전시간 후보를 mask하므로 순서조건을 버릴 수 없다. [C23,C24]")

#text("증명의 역함수를 손으로 보자. ID순서(A,B)에서 reading(0,1)은사전{A:0,B:1}이다. 순서를(B,A)로 바꾸면 tuple은(1,0)이고 다시 사전으로 돌리면 원래와 같다. 같은 positional tuple(0,1)을 두 순서에 그대로 넣으면 서로 다른 conjunction이 되어 잘못된 비교다. W44의 ID-indexed canonical key가 필요한 이유이며,8저장행은 이 재색인 의미를 확인한 동일4conjunction의 두 표현이다.")

= #text("39. 말단 순서 분석 수치와 deadline 반례를 재구성하기")

#text("static수치는 저장 W41환경의 subsetmask5하나다. 네 distinctconjunction을 두 order로 적은8행이다. worstwidth3/5,다른width17/30,price2,같은 최악IDties로 no_gain이다.8행이나 별도 recheck를 독립과제로 세지 않는다.")

#text("deadline반례는 두 item·네 bitworld에서 schedule을 바꾸면 완료0/4와4/4가 되게 만든다. 거절prefix는 price1,width1,완료는 price2,width0이다. static가정이 깨지면 보존이 안 된다는 반례이며 학습알고리즘의 실험적 우위가 아니다.")

#text("deadline으로 availability가 history에 의존하면 같은 마지막ID목록이어도 어떤 schedule에는 완전tuple이 없다. 재색인의 정의역부터 달라진다. 정보집합이 같다는 말만으로 실행가능성과 관측분포까지 같다고 할 수 없다.")

#text("재색인 adapter만 고정길이 reference·평균dictionary가정에서 O(1+k)작업,O(k)추가references다.2^k열거·endpoint·Fractionbit·직렬화는 따로 센다. 작은 adapter bound를 전체solver나 real-time보장으로 넓히지 않는다. [C25,C26,C28]")

#figure(image("figures/w44_deadline.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("네작성world의두schedule:완료0/4대4/4. staticterminal가정위반을보여주는반례이며실제deadline성능측정이아니다. [C26,F4]")])
= #text("40. 최근 방법의 public state와 fitting support")

#text("현재 시작은 action0을 읽은 mask1,spent1,remaining1,total2,빈cache다. quote1,lambda0.05이며 다음은 action1/2/3또는STOP이다. fold0의 conditional근거는 subject5/6이며 각 action의 fittingleaf에30창과두사람이 있어야 지원된다.")

#text("support는 근거 수가 있다는 admission이며 신뢰구간이나 정확도 보장이 아니다. 종속·불균형·분포변화가 남는다. fitting두사람은 상류 학습목표의 근거이고 DEVbranch두사람과 다르다. 한 counts필드를 양쪽 증거로 쓰지 않는다.")

#text("후보는 각 action의 mu_a−0.05를 비교한다. 미지원 action을 eligible에서 빼고 지원 최대가 양수일 때 작은indextie로 구매한다. 빈eligible이면 insufficient_support,nonempty지만 최대≤0이면 nonpositive STOP이다.")

#text("남은 구매가 한 번이라 같은 eligible의 localmyopic은 동일map이다. max와 sortednegative로 따로 써도 규칙·tie·STOP이 같으면 같아야 한다.524쌍 동률은 이 정의를 확인하며 새 nonmyopicplanning효과를 만들지 않는다. [C32,C33]")

= #text("41. blanket guard와 action-local admission 정리의 범위")

#text("F는 feasible전체,S는 각자의 fit지원집합이다. blanket은 하나라도 미지원이면 전체STOP하고 S=F일 때만 같은 최대순가치를 쓴다. local은 다른 action미지원 때문에 좋은 지원 action까지 막지 않는다. 같은 상태의 admissionpredicate만 바꾼다.")

#text("S=F이면 두 규칙은 같다. S가 진부분집합이고 양수 지원값이 있으면 blanket0,local은 그 양수최대다. 양수값이 없거나 S가 비면 둘 다0이다. 따라서 추정한 incrementalvalue 안에서 local이 weaklydominates한다.")

#text("실제 label손실은 추정mu와 다르다. 평균추정오차나 분포변화 때문에 추가구매가 맞던 예측을 틀리게 할 수 있다. 지원안된 구매를 하지 않고 한 quote를 지킨다는 구조정리이지 안전성·실제오류·임상효용 정리가 아니다. 전체harm39가 이 차이를 보여준다.")

#text("current fixedsubset은 자기extra만 지원되면 net이 음수여도 산다. fixedorder는 positive조건도 쓴다. 지원정보 권한이 같아도 policyclass는 다르며 원래 fullbudget·외부 reference비교 공백은 남는다.")

#text("교육용으로 feasible next action의 net이(a1=unsupported,a2=0.08,a3=−0.02)라고 하자. blanket은 a1 미지원 때문에 STOP0, local은 지원된 a2의0.08을 택한다. 모든 action이 지원되면 둘 다 a2다. a2 추정값0.08이 실제 오류감소0을 뜻하지 않을 수 있어 realized cost만 늘 수도 있다. 이 예시는 논리 규칙을 보여줄 뿐 W47의 새로운 trial이나 성능측정이 아니다.")

= #text("42. 시간 제한 본실행 연구는 학습을 했지만 main은 실패했다")

#text("W45는 RF1개와 conditionaltree32개,통계fit33회를 했다. LLM/API0과 통계fit33은 다른 회계라 모순이 아니다.1098원창의16mask증강17568행과 개발1038창의 반복conditional목표16608행을 사람·원창 수와 구별했다.")

#text("main은4152경로를 계획했지만8완료 뒤 subject5/index8의 취득전2초crossing에서 한 경로가 실패했다.4143은 미시작,heldout0이다.17사전STOPevent와 원prefix를 남겼고 acceptedmain을 다시 보내 성공으로 덮지 않았다.")

#text("실패 전에53개 개발 선택표가 계산돼 myopic동률·strongstatic회귀가 보였다. partialoracle는 JSON구문·행수·hash만 검사했다. mismatch0을 수치전체 일치로 해석하거나 개발표를 완료timedmain으로 바꾸지 않는다.")

#text("실패를 남긴 채 다음 유한질문으로 갔다. 왜 늦었는지는 phase별 미계측이라 단정하지 않고 full deploymentcost는 null이다. 새 판본이나 후속 성공은 과거4152/8/1/4143을 소급 바꾸지 않는다. [C30]")

= #text("43. 축소 개발군 연구의 완료1800경로와 insufficient_support는 함께 참이다")

#text("W46은 같은 frozenmodel/fold0/mask1/remaining1로 P7/P8각60창,합120노출DEV를15정책 처리해1800경로를 완료했다. 해당 범위에서 실행가능했다는 근거다. 최대rowwall0.1046045초가2초안이었다는 것은 단회 관측이다.")

#text("candidate action2는46창·2인,action3은11창·P8한명뿐이었다. 두 action 각각30창·2인이라는 DEVgate를 못 채워 insufficient_support다. 경로완료와 과학적 지원은 다른 필드라 모두완료가 지원실패를 없애지 않는다.")

#text("candidateJ0.4154166667은 subset5의0.2333333333과 order0,2의0.3716666667보다 높았다. candidate=myopic도 남는다. 강한 subset을 빼거나 일부 timing만 고르면 인상이 달라지므로 원 비교를 함께 읽는다.")

#text("준비wrapper sessionmetadata소실로 preparationexit는 unobserved/null이다. artifact정상만으로 exit0을 만들지 않았고 replay도 안 했다. 공통coldcharge와 mixedtail을 나눠 completecold/deploymentcost를 추정하지 않는다. [C31]")

= #text("44. 전체 개발군 연구 지원 분모:524창은 어디서 왔는가")

#text("W47은 같은 model/fold0에서 P7의266창과 P8의258창 전부를 썼다. 가능한 동안 사람을 번갈아 배치하고16정책순서를 창순번으로 회전했다. label로 좋은 창을 고르지는 않았지만 이미 노출된 개발자료라 독립final이 아니다.")

#text("16×524=8384경로는 planned=started=completed,실패·partial·unknown·unstarted0이다. 모든 policy unsupportedpurchase0이며 localcopy일 뿐 physicalacquisition0이다. 같은 원창의16반복을 독립8384표본으로 부풀리지 않는다.")

#text("action2는249창(P7 114/P8 135),action3은55창(P7 3/P8 52)이다. 합계30·두사람 gate는 통과하지만 사람마다30이 아니다. P7action3세창을 숨기지 않는다. 넓은 pool에서 legacy도 gate를 통과하므로 그 사실 자체가 guard효과는 아니다.")

#text("W46→W47에는 pool크기와 subset의 지원규칙이 함께 바뀌었다. cross-wave점수차는 동일policy의 순수개선이 아니다. 현재524창 안의 candidate/legacy비교로 guard효과를 좁히며 그것도 후향 개발진단이다. [C33,C35]")

= #text("45. guard가 바꾼41창:16교정·25동률·0피해")

#text("같은pool에서 local은 blanket이 막던 action2구매41개를 살렸다. P7 33/P8 8이며16오류교정·25오류동률·0새오류였다. 시작상태·모델·quote가 같은 admissionpredicate의 좁은 비교다.")

#text("사람평균 오류차는−(16/266+0/258)/2=−0.03007518797,quote차는(33/266+8/258)/2=0.07753395116다.0.05배quote차를 더해 J차−0.02619849041을 얻는다.16/524로 macro차를 계산하면 다른 평균이다.")

#text("P8은8추가quote에 교정0이었다. 평균이 좋아도 각 사람의 효용은 다르다.41창은 규칙불일치로 정해진 부분집합이지 random독립group이 아니다. 추가비용을 누가 부담하는지도 봐야 한다.")

#text("전체524에서 candidate는 초기STOP대비80교정과39harm이 있었다. guard41창의0harm은 전체정책 안전을 뜻하지 않는다. guard대조와 initialSTOP대조는 다르므로0과39를 모순으로 보거나 하나로 합산하지 않는다. [C33,C34]")

#figure(image("figures/w47_support_harm.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("왼쪽은사람별branch수,오른쪽은서로다른비교집합의교정/동률/피해다. guard41창의0피해와전체후보524창의39피해를분리해서읽는다. [F8]")])
= #text("46. 실제 J 손계산과 강한 baseline 회귀")

#text("candidate는 P7오류64/266·quote383/266,P8오류95/258·quote445/258이다. 사람평균 오류0.3044092790114822,quote1.582327912805269에 lambda0.05를 적용해 J0.38352567465174564를 얻는다. 각각 먼저 창평균하고 사람평균한다.")

#text("legacyJ는0.40972416506382237라 더 나쁘다. 하지만 subset5는 P7오류31/quote492,P8오류50/quote513으로 J0.25111980532727163,order0,2multiplier1도0.3423464183715102로 더 좋다. 국소guard개선이 전체algorithm우위는 아니다.")

#text("candidate−subset5=+0.132405869324474,candidate−order=+0.04117925628023544다. 낮을수록 좋아 양수는 회귀다. 그림은 오류와0.05quote를 쌓아 J를 보인다. candidate/localmyopic의 모든524창 동률은 no_gain이며 두 발견으로 세지 않는다.")

#text("subset은 지원되면 net음수도 구매하고 order는 multiplier별positive검사를 한다. 같은lookup권한이지만 class는 다르다. 노출DEV의 최저순위를 새확증winner로 인증하지 않으며 현재 fixedprefix범위의 강한 대조로 보존한다.")

#text("macro와 pooled를 실제 숫자로 대조하면 candidate pooled 오류는(64+95)/(266+258)=159/524=약0.303435115다. macro는0.304409279다. 근소하지만 서로 다른 값이며 실제 사람 수가 아주 적으므로 이를 독립창 binomial 표준오차로 꾸며 강한 확증처럼 보이지 않는다. 각 사람의 원시 정수(n,error,quote)를 보존하면 독자가 다른 가중치의 보조 분석을 하더라도 원래 primary와 구분할 수 있다.")

#block(width: 100%, above: 7pt, below: 7pt, breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("전체 개발군 연구 핵심participant-macro점수")]]
#v(4pt)
#table(columns: (1fr,1fr,1fr,1fr,), inset: 4pt, stroke: 0.35pt + rgb("#bac6d0"), table.header([#text("정책")],[#text("오류")],[#text("quote")],[#text("J")]),
[#text("candidate")],[#text("0.304409279")],[#text("1.582327913")],[#text("0.383525675")],
[#text("local_myopic")],[#text("0.304409279")],[#text("1.582327913")],[#text("0.383525675")],
[#text("legacy_blanket")],[#text("0.334484467")],[#text("1.504793962")],[#text("0.409724165")],
[#text("subset_5")],[#text("0.155169901")],[#text("1.918998077")],[#text("0.251119805")],
[#text("order_0_2_m1")],[#text("0.265649589")],[#text("1.533936586")],[#text("0.342346418")])
]

#figure(image("figures/w47_objective.svg", width: 100%, height: 82mm, fit: "contain"), caption: [#text("같은524노출DEV창의사람평균점수다. candidate=myopic이며강한subset/order가더낮은J를갖는다. errorbar는독립표본불확실성을측정하지않아그리지않았다. [F7]")])
= #text("47. 아키텍처와 의사코드: 단계마다 왜 필요한가")

#text("입력계층은 hash·shape·mask·budget을 검사한다. policy는 publicencoding·초기frozenprediction·conditional지원/net을 구한다. executor는 구매전intent를 남기고 선택group만 copy·과금한다. evaluator는 마지막에label로 점수를 매기고 audit는 fullarray/label권한으로 raw산술을 따로 확인한다.")

#text("구매전intent는 중간실패에서도 의도를 남긴다. traceflush와 finalizationbarrier는 기록까지 포함한 측정범위를 정한다. 그 뒤 timing영수증·EXIT·launcher가 남으므로2초안에 전체인프라가 끝났다고 하지 않는다.")

#text("timeout·controlstop·hash불일치·providerfailure는 원결과로 남기며 자동retry하지 않는다. acceptedcall 재송신은 단회main·중복취득 계약을 어길 수 있다. unitfailurefixture와 실제 providerfault발생도 다르다. W47main에는 실제providerfailure가 없었다.")

#text("아래는 한remainingquote 규칙이지 일반 다단계Bellman 구현이 아니다. audit의 전체bank/label을 policy입력에 섞지 않으며 author portableexport의 통계유효성도 독립인증됐다고 하지 않는다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 6. 동결모델의협력정보경계·실패보존실행")]]
#v(3pt)
#strong[Require] #text("검증된공통RF/fold0,mask1의관측값,spent1/remaining1,quote1/lambda0.05,fit30창/2인규칙. 고정DEVindex·16정책회전순서·control/time/출력범위와intent/trace장부.")
#parbreak()
#strong[Ensure] #text("한번의STOP또는지원된추가copy,최종prediction,실제cost·상태·실패/unknown보존기록.")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("source/model/inputhash와publicstate를검증한다. label과미구매값은선택기입력에서제외한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("work_started를기록하고획득group0만encoding해동결초기prediction을구한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("세feasibleaction의조건부leaf·지원창/참가자·mu를publicstate만으로조회한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("각action의지원여부로eligible집합을만든뒤max(mu−0.05)>0인최소indexaction을택한다. 빈지원과nonpositiveSTOP을분리한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("구매전에control·remainingquote·측정시간을검사하고intent를flush한다. 선택group만copy하고quote1을차감한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("구매후공개mask를갱신해동결prediction을한번더계산한다. STOP이면기존prediction을유지한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("7")], [#block(width: 100%, inset: (left: 0.0em))[#text("trace를flush하고finalizationbarrier를검사한다. 실패prefix·unknown·미실행을남기며재전송하지않는다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("8")], [#block(width: 100%, inset: (left: 0.0em))[#text("그뒤평가자가label로오류를세고사람별정수오류/quote를집계한다. 별도audit와costscope를연결하고완전한안전·효용인증을주장하지않는다.")]])
#v(1.2pt)
]

= #text("48. 시간2초·CPU0·준비비용을 정확히 읽기")

#text("2초scope는 work_started부터 encoding·prediction·세conditional조회·guard·intent·copy·finalprediction·traceflush·finalization까지다. timing영수증·EXIT·launcher끝은 제외된다. cooperative관측이지 OS강제종료나 미래분포 deadline보장이 아니다.")

#text("main은 wall215.7763239000초/directCPU64.546875초다. wall과 CPU는 다른 자원이며4806row의 관측CPU0은 해상도에서0일 뿐 무료계산이나 결측이 아니다. CPU실패/unknown과 나눠 적고0분모 speedup을 만들지 않는다.")

#text("공통준비/import/load fullcharge20.4981172000wall/10.40625CPU를 정책마다 같은 회계시나리오로 붙인다. 실제16준비가 아니다. mixedresidual5.9793097021wall/3.078125CPU도 공개하며 고립된coldload나 물리반복으로 부르지 않는다.")

#text("historicalfit상각·physicalIO/cache/energy·transientmemory·EXIT/launchtail·저술/보고/게시·fulldeployment는 측정밖/null이다. 단회warm차이로 총비용우위를 말하지 않고 oldsolver endpoint와 현재forestwall을 하나의 성능표로 합치지 않는다. [C33,C35]")

= #text("49. 관련 연구를 인용할 때 실제로 읽은 범위")

#text("Shim2018은 가변크기 관측집합 encoding과 joint acquisition/classification의 동기다. verifier는 공식abstract·metadata·JSON도입부일부를 읽었고 전체PDF·proof·실험·code는 읽지 않았다. order-invariantencoder가 행동순서 불변성을 뜻하지는 않는다.")

#text("Li/Oliva는 PMLR139:6450–6459의 metadata/abstract와 별도 arXivv2의 선택된 state/action/STOP·chronology·masking·AO*인용을 확인했다. 과거unversionedcache와 새v2는 다른source다. W44의 네구간7879bytes읽기는 전체재현이나 publisher동일성인증이 아니다.")

#text("AO*공식authorindex의2002와 GSMRL인용2004가 충돌한다. 원본문·판본·원보장을 직접 못 봤으므로 원AO*와 현재solver의 일반동치·보장전이를 주장하지 않는다. W44의 경로오기와 손상review도 남는다.")

#text("Cawley/Talbot은 선택편향 경계의 동기이며 로컬split인증이 아니다. UCI도 source/license설명만 확인하며 localaxis·window·의료효용을 인증하지 않는다. adaptive-submodularity의 원가정·정정범위를 유지한다.11검증entry 중 해당7개와 문서references를 일관되게 연결한다.")

#text("외부문헌의 DOI가 검증됐다는 말은 제목/저자/출판식별이 확인됐다는 뜻이다. 원문 전체를 확보했다거나 그 논문이 주장한 수치를 직접 재현했다는 뜻은 아니다. 현재 확인된 UCI DOI10.24432/C5TW22는 데이터셋 출처에만 쓰며 의료정확도나 source feature mapping 인증으로 확대하지 않는다. 원 AO* 본문이 없다는 gap은 최신 문서의 완결성 안에서 분명히 설명할 수 있지만 사실확인 완료로 바꿀 수는 없다.")

= #text("50. 옛53쪽 해설과 새 누적판을 어떻게 비교했는가")

#text("실제확보한 v24EXPLAINER_KO.md는210099bytes다. 입문부와 v21/v20길잡이,v19심화·전체진단,v17/v16/v15/v14보존문과 v23/v24추가를 함께 담았다.53쪽은 인계보고이며 해당PDF는 이번 확인에서 아직 못 찾았다. Markdown내용과hash는 실제 고정했다.")

#text("고유한 진전은 tuple-copy빈mask예외,−H+E+R분해,pointwise벡터동일성의 비음수가격지배,손실연산순서,미구매·실패·관측구분이었다. 이를 각 주제에 재작성하고 paper/Supp에도 복원했다. 반복된 이전판 정의는 한 번 설명하며 sourceheading별 연결을 남긴다.")

#text("PAMAP2·MiniBooNE·OPPORTUNITY와 benchmark계획은 당시 후속설계였다. 현재 실제EDA나 완료평가로 바꾸지 않는다. 검증된11references 밖의 옛최근문헌은 새원전을 읽지 않아 세부성능주장으로 확대하지 않는다. 실행·읽기범위를 분류하는 것이다.")

#text("v2의 throughW44 paper/Supp는 수학·실패를 보존했지만 KO22절은 대략530~1100자씩 짧았다. 새 해설은 전제·식유도·손계산·실제절차·대조·EDA를 연결한다. 날짜·버전·페이지길이보다 주제별 포함/정정/보류의 근거로 판본을 비교한다. [C36]")

= #text("51. 재현 순서와 source·claim·figure의 연결")

#text("INPUT_FREEZE의 실제Task/run/executor와10pin을 먼저 확인한다. SOURCE_LINKS에서 claimID의 파일/SHA256/키·구간을 찾고 본문anchor·표·그림과 대조한다. 한 hash가 맞는다고 모든 과학주장이 검증된 것은 아니다.")

#text("generate_figures.py는 NPZ를 allow_pickle=False로 읽고 shape/finite/label/offset을 assert한다. 저장count의16정책FractionJ를 재계산할 뿐 추론하지 않는다. oldSVG는 원hash로 복사해 provenance를 붙이고 축·단위·분모·불확실성을 caption에 둔다.")

#text("selfcheck는 기존 builder.validate를 호출해 schema·algorithm·수식금지문자·표차원·containedSVG를 검사한다. UTF-8손상·anchor·sourcehash도 본다. 이는 PDF조판이나 독립과학·교육심사가 아니다. build와 전체page열람은 root의 별도Task다.")

#text("미확보source와 실패는 기록한다. 손상된 frozenMETHOD를 고치지 않고 읽을 수 있는 raw·새검토를 구별한다. 원문명령은 자료로만 보며 study main/unit/oracle를 실행하지 않는다. 이판본의 고유v3scope만 쓴다.")

= #text("52. 무엇이 알려졌고 다음 acceptance는 무엇인가")

#text("알려진 것은 조건부유한정리와 고정개발자료 관측이다. 유압의 한leaf쌍은 같은예측이라 추가가격만 남고 원MHEALTH/Gas는 strongestmyopic과 동률이었다. 부분식별은 없는반사실을 채우지 않았고 exactsolver는 정확risk/fulltie를 보존했지만 늘 더 싸지는 않았다.")

#text("W42는 평균예측/worstwidth의 환원조건을,W44는 staticterminal순열 범위를 정했다. W45실패,W46지원실패,W47myopic동률·static회귀는 그대로다. guard41창개선은 좁은 개발관측이며 overallharm39·독립표본0·총비용unknown을 지우지 않는다.")

#text("다음 acceptance에는 새독립group과 사전동결/primary선택,실제취득·failure·delay·availability·전체비용,같은predictor/정보/cap/STOP의 강한subset/order/myopic/adaptive대조가 필요하다. rarebranch와 사람별피해의 불확실성도 미리 정한다. DEV재선택을 새final이라 부르면 충족되지 않는다.")

#text("이판본은 개념·이력·수식·절차·EDA·결과·실패·공백을 완결해 설명한다. Task완료와 hash/schema통과도 사실인증·신규성·의료/산업효용·총비용우위·제출·승격은 아니다. needs_evidence와 scientific_certification=false를 유지한다.")

= #text("53. 평균 head·완전 진단·가격의 선호 경계를 직접 유도하기")

#text("이 장은 기존 네 손실 정의만으로 빠졌던 실제 민감도 계산을 완성한다. 보조 g301/k3와 고정 mask3를 같은421노출 사이클,같은 가격(1,1,1),cap2로 고정한다. 고정의 오답head924·오답vector381·quote842와 gate의861·391·518을 빼면 각각−63,+10,−324다. 정책과 예측은 그대로이고 채점 선호만 바뀐다.")

#text("alpha는 component d/4와 complete vector v를 섞는 비중이다. lambda는 다른 질문인 정규화 quote의 가중치다. 한 사이클 손실 ell=(1−alpha)d/4+alpha v이며 quote항은 lambda·총quote/(3n)다. 현재 MHEALTH의 비정규화quote목적과 혼동하지 않는다. hard cap2는 lambda가 커져도 유지된다.")

#text("head항은−63(1−alpha)/1684,vector항은10alpha/421=40alpha/1684,quote항은−324lambda/1263=−432lambda/1684다. 합하면 Δ=(−63+103alpha−432lambda)/1684다. 103은63+40의 산술이며 학습한 회귀계수가 아니다. Δ는 gate−fixed라 음수면 gate의 이 스칼라 점수가 낮다.")

#text("동률 경계는 alpha*(lambda)=(63+432lambda)/103이다. lambda0에서는63/103,lambda1/20에서는423/515다. 경계보다 alpha가 작으면 gate,크면 fixed가 낮다. lambda5/54에서 경계가alpha1에 닿는다. 그때 alpha<1은 gate,alpha1은 동률이며 더 큰 lambda에서는 모든alpha∈[0,1]에서 gate가 낮다.")

#text("그래도 vector실패10개 증가는 없어지지 않는다. 가격 절약을 더 중요하게 셌을 뿐 세 좌표를 모두 개선한 Pareto지배가 아니다. alpha=lambda 대각선을 임의로 대입하면(−63−329alpha)/1684지만 두 선호를 같은 것으로 정할 근거는 아니다. 아래 여섯 행과 그림은 같은 출력의 재가중 계산이며 새 학습·60독립시험·사용자 선호 측정이 아니다.")

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
= #text("54. 범위 안39창·밖382창에서 무엇이 달라졌는가")

#text("기존 root의 fit최소·최대 범위를 기준으로 같은421사이클을 나누면 안39,밖382다. 안쪽 gate−fixed 변화는head−1,vector+8,quote−32이고 바깥은−62,+2,−292다. 합하면−63,+10,−324로 전체 집계가 복원된다. 전체10vector회귀 중8개가 범위 안에 있어 바깥이라는 한 변수로 실패를 설명할 수 없다.")

#text("전체component변화는73개선·10회귀·338동률이며vector는0개선·10회귀·411동률이다. 같은391미지원 공동정답의 오류라는 진단과39/382범위 진단은 겹치는 분할이다. 두 표를 더해 표본을 늘리지 않는다. 정답tuple을 본30사이클/못 본391사이클은 평가 후 label로 나눈 자료이며 actor가 쓸 입력이 아니다.")

#text("root범위 안은1차원최소·최대에 들어간다는 뜻이다. 내부에 밀도가 거의 없는 구간이 있을 수 있고 다차원 조합지원도 보장하지 않는다. 범위 밖에서도 맞힐 수 있다. 범위이탈은 필요조건도 충분조건도 아니므로 이것을 인과기제나 새로운 배포gate로 바꾸지 않는다.")

#text("현재 추가한 표는 저장 cycle_metrics의 모든 secondary행421개를 다시 합한 산술이다. 새 모델 실행이나 원시센서 수집이 아니다. 같은 창에서 head평균을 낮추며 완전진단을 더 자주 실패할 수 있다는 앞 장의 선호 충돌이 어디에 모였는지 보여준다.")

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
= #text("55. 실패한 구매도 포함하는 공통분모 GREEDY를 끝까지 따라가기")

#text("이 GREEDY는 아직 실행하지 않은 PAMAP2전이 비교의 사전설계다. S는 성공관측,T는 시도한 원천이다. 원천을 시도하면 실패여도T와quote가1늘고,정상반환만S에 더한다. predictor는T가 아닌S로 호출한다. S가비었을때만 trainingprior를 쓰고 기존성공이 남으면 f_S를 유지한다. actor는미구매availability·값·label을먼저보지않는다.")

#text("정책-fit사람s의 I_s(S)는 S의모든그룹이유효한사전보존창전체다. 같은S에서 모든후보j에 이집합을같이쓴다. 후보j가성공한창만고르면실패를숨긴다. 성공때 d는구매전손실−구매후손실,실패때는예측f_S유지로 d=0이다. 실패한 after-loss를계산하거나가짜값으로채우지않으며 시도quote는항상낸다.")

#text("m_s(S)=|I_s(S)|로나눠사람평균을먼저만들고 K명의계획사람을같은비중으로평균해 g(S,j)를만든다. 어떤계획사람이라도m_s=0이면전체S표가not_estimable이다. 그사람을빼거나평균0으로채우지않는다. 실행중그상태면현재f_S로STOP하고오류·시도비용·fallback수를보존한다. 평가대상사람의빈창은not_evaluable이며,정의된지표로찾은후보가없다는no_feasible_policy와다르다.")

#text("구성예1: A는100창중9번만성공하며그9오류를고치고 B는100번성공하며20오류를고친다. 시도당이득9/100대20/100은B를고른다. 성공창만평균하면1대1/5라A를잘못선호한다. 이수치는설명용이며실제센서성공률이아니다.")

#text("구성예2: 사람1에1창,사람2에9창이있다. A의사람별이득은1,0이고 B는0,2/9다. equal-subject는1/2대1/9로A,pooled는1/10대1/5로B다. 목적을먼저고정해야하며결과가좋아지는평균으로바꾸지않는다.")

#text("표는global mask-indexed다. 현재구매값이나실패한과거원천의정체에조건화하지않는다. j∉T중양수최대만고르고동률은hand/chest/ankle순이다. 실패뒤S는그대로라같은표를다시보되T로재시도를막는다. cap소진·후보없음·비양수·추정불가면STOP한다. 상관실패가있으면열등할수있고 T조건·관측조건정책은별도로fit·예산을준후보다.")

#text("40960은기존저장합성계약검사의8availability×256binarymask출력bank×4cap(0~3)×5gain표조합이다. 시도과금·재구매금지·S⊆T·실패뒤예측유지·tie·빈Sprior·정의불가STOP의코드계약을검사했다. 독립사람수나PAMAP2정확도가아니며 이판본은그검사를다시실행하지않았다.")

#fit-equation[$ g(S,j) = (1/K) sum_(s=1)^K (1/m_s(S)) sum_(i in I_s(S)) d_(s,i,j)(S) $]
#text("All candidate actions share each S-indexed eligible-window denominator. If any planned m_s(S)=0 the entire table is not_estimable, not zero.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 7. Prospective global mask-indexed attempt-marginal GREEDY")]]
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

= #text("이번에 실제로 한 일")

#text("불완전 로그에서 가능한 정답 확률들의 공동 집합을 만들고, 같은 잠재 세계에서 기준 전략과 후보 전략의 마지막 손실을 비교했다. 따로 실제로 노출된 MHEALTH7·8에서 예측기는 그대로 두고 위험 표만 보정했을 때 구매 전략이 달라지는지도 확인했다. 두 결과를 하나의 응용 성능표로 섞지 않는다.")

#text("본실행과 원시 검산은 각각 한 번 끝났다. 그러나 강한 정적 대조군 누락과 새 독립 자료 부재가 남아 과학 상태는needs_evidence다. 테스트 통과나 모델의 저술은 과학 인증이 아니다.")

= #text("입력에서 선택까지")

#text("로그의 각 사건은 알려진 혼합 실험 종류와 관측된0·1 또는 결측M으로 남는다. 결측은 정답과 독립이라고 가정한다. 관측되지 않은 좌표를 임의로 채우지 않고 가능한 범위로 둔다. 그 공동 범위 안에서 한 정책의 모든 가지와 기준 정책은 같은 정답 확률을 써야 한다.")

#text("보수적인 하한이 가장 큰 전체 정책을 고르고, 근거가 없거나 집합이 비면 원래 기준 전략을 쓴다. 선택 뒤 가지마다 마음대로 재계획하면 처음 계산한 보장이 적용되지 않을 수 있어 이 실행에서는 나무를 고정했다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 8. 공동 가능성 집합을 이용한 전체 전략 선택")]]
#v(3pt)
#strong[Require] #text("train에서 고정한 기준 전략·전체 정책 메뉴 독립 보정 로그와 알려진 결측/혼합 가정 초기 유료 관측·남은 예산·실패/보류 비용")
#parbreak()
#strong[Ensure] #text("대조 손실의 하한·상한과 선택한 전체 나무 미지원·빈 집합이면 기준 전략, 모든 실패·비용 기록")
#v(3pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("1")], [#block(width: 100%, inset: (left: 0.0em))[#text("각 로그에서 관측·결측 수를 세고 네 확률 좌표가 함께 만족하는 부등식을 만든다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("2")], [#block(width: 100%, inset: (left: 0.0em))[#text("가능한 꼭짓점을 정확한 유리수로 열거한다. 참 정답 확률은 이 함수에 주지 않는다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("3")], [#block(width: 100%, inset: (left: 0.0em))[#text("같은 세계에서 두 전략을 끝까지 실행한 손실 차이의 최소·최대를 계산한다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("4")], [#block(width: 100%, inset: (left: 0.0em))[#text("문맥별 최소 이득이 가장 큰 나무를 고르되 동률·미지원·빈 집합은 기준으로 돌린다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("5")], [#block(width: 100%, inset: (left: 0.0em))[#text("실패한 구매도 비용·시도 수에 포함하고 정지·보류·정답·피해를 각각 남긴다.")]])
#v(1.2pt)
#grid(columns: (1.5em,1fr), column-gutter: 5pt, align: (right,left), [#text("6")], [#block(width: 100%, inset: (left: 0.0em))[#text("저장된 원시 자료만 다른 구현으로 검산하고, 실제로 우위가 없거나 대조군이 부족하면 그대로 보고한다.")]])
#v(1.2pt)
]

= #text("작동 예와 대조군에서 드러난 실패")

#text("문맥에 따라 필요한 센서가 다르면 첫 문맥에서는1을, 둘째에서는2를 읽는 전략이 두 센서를 늘 읽는 전략보다 비용을 아낄 수 있었다. 선언한 정적 목록 대비 좁은 집합의 손실 이득은0.075였다. 넓은 집합·미지원·빈 집합도 따로 실행했고 미지원과 빈 집합은 기준 전략으로 돌아갔다.")

#text("그런데 정적 전략으로 충분해야 할 기제에서도0.025 이득이 나왔다. 원인을 보니 후보가 실패하면 보류하는 규칙을 썼지만 기준선 선정 목록에는 그 같은 순서의 실패-보류 전략이 빠져 있었다. 두 문맥에서 같은 나무를 쓰는 후보 자체가 정적 대조군이 될 수 있으므로 이 값을 적응성의 이득으로 해석하면 안 된다. 원시 결과를 고쳐 없애지 않았다.")

#text("원래 정해 둔 집합 밖 확률 뒤집기는 피해 반례가 되지 않았다. 이후 저장된 손실 식만 대입한 수학 분석에서는 정답이 항상0인 집합 밖 경우 기준보다0.05 또는0.10 나빠짐을 찾았다. 뒤의 분석은 새 본실험이나 사전 성공으로 세지 않는다.")

= #text("실제 개발 자료에서는 무엇이 달랐나")

#text("기존5·6 자료를T322/C192로 나누고C에서 보정 강도64를 골랐다. 예측기는 한 번도 다시 학습하지 않았다. 먼저5·6의3598개 캐시 예측과 일치함을 확인한 뒤 선택표를 해시로 고정하고7·8의524창을 한 번 열었다.")

#text("보정 전 Bellman과 근시안은 경로가 같았고 평균 손실은0.302104였다. 보정 후 Bellman은0.245246, 근시안은0.308091로305창에서 경로가 달랐다. 가장 좋은 기록상 정적 전략은0.251294였다. 이 정적 순위는 결과를 본 뒤의 설명이지 새 기준선 선정이 아니다.")

#text("보정이 항상 좋았다는 뜻도 아니다. Bellman은 좋아졌지만 근시안은 조금 나빠졌고, 약속한 부분집합/순서를 끝까지 읽는 전략들은 그대로였다. 위험 추정 변화와 적응 전략의 이득을 나눠 봐야 한다. 31440경로를 실행했어도 사람은2명, 고유 창은524개다.")

= #text("정답을 고친 예와 망친 예")

#text("보정 Bellman의 교정 예: 참가자7의 창23에서 초기 오답이 구매 뒤 정답으로 바뀌었다. 실제 구매 순서는[3, 2]이고 최종 예측/정답은1/1이다.")

#text("피해 예: 참가자8의 창187은 초기 정답이 구매 뒤 오답으로 바뀌었다. 구매 순서는[3, 2]이고 최종 예측/정답은8/9이다.")

#text("정적 최우수 기록과 짝지으면 교정45건과 피해42건이 함께 있다. 평균 손실이 작아졌다는 사실은 개별 사람·창의 무해 보장이 아니다. 모든 참가자별 수치와 실패0·불명0·미시작0을 원시에 남겼다.")

= #text("검증한 것과 아직 모르는 것")

#text("네 준비 smoke와 아홉 단위검사, 단회 본실행, 별도 저장원시 검산이 통과했다. 공동 집합의 꼭짓점·512개 구간 자리·전체 정책 대조와60개 DEV 정책표·31440경로를 확인했다. 작성자가 쓴 두 구현의 일치는 조정자의 독립 방법 검토를 대신하지 않는다.")

#text("보장의 전제는 알려진 공통 잠재 세계와 독립 결측/표본이다. 이 전제를 실제 MHEALTH 시간 창에 옮기지 않는다. MHEALTH1..10은 모두 과거 사용됐고 새 독립 최종시험 참가자는0명이다. 외부 선행 방법 본문과 신규성, 물리 센서의 비용·전력, 전체 배포 비용과 메모리는 아직 확인하지 못했다.")

#text("로그 집합 계산은 차원과 제약이 커지면 조합적으로 늘고 전체 문맥 선택도 지수적으로 늘 수 있다. 이번 작은4차원/2문맥/8세계/32메뉴 계산의 성공을 일반 대규모 효율로 바꾸지 않는다. 논리 quote와 실제 센서 절감을 구분한다.")

= #text("출처와 동결")

#text("SOURCE_HASHES에 원 입력·부모·정책·검토기·빌더·공유 소스 변경 영수증을 연결했다. 이전 W48의 근시안 동률·정적 전략 회귀와 과거 노출 이력은 그대로 보존한다. 문헌 메모는 출처가 표시된 상속 자료이며 이번에 원문을 새로 검증한 것은 아니다.")

#text("실험 API·새 예측기 학습·native episode·추가 worker·새 의존성은0이다. SOL 저술 사용량은 미계측이다. 스킬 후보는 비활성이며 전역 설정·조판·AOP·게시를 수행하지 않는다. 정확한 Task/Dispatch에 공식 결과를 한 번 보낸 뒤 이 연구 산출물을 동결한다.")

= #text("어떤 착각을 확인하려 했나")

#text("예전 비교에서는 정적 전략이 query 실패 뒤 보류할 권리가 빠져 있었다. 후보만 그 권리를 쓰면 센서를 똑똑하게 고른 효과처럼 보일 수 있다. 이번에는 순서를 고정해도 각 관측에서 정지·보류할 권리를 전부 주었다.")

#text("정적 순서의 가능한 종료 규칙을 작은 표본만 뽑지 않고 정의한 문법 전체에서 계산했다. 그러나 실제 DEV 연결과 검산에 오류가 나서 연구 결론은 성공이 아닌 완결된 실패 보고다.")

= #text("작동 예: 같은 정보와 실패 권리")

#text("먼저1을 사다가 실패하면 멈추거나 보류하거나2를 살 수 있다.2도 실패했을 때도 최종 보류를 선택할 수 있다. 실패한 구매도 값을 내고 시도 횟수를 쓴다. 정적 전략도 이 모든 선택을 가지므로 실패 대응을 후보의 독점 이득으로 세지 않는다.")

#text("항상1이 필요한 통제 구조에서는 정적과 적응 전략이 똑같아 이득0이었다. 문맥마다1/2가 번갈아 필요한 구조에서는 같은 최종 예측을 더 적은 quote로 얻어 기록상1/80 차이가 남았다. 근시안도 같아서 긴 계획의 우위가 아니고, 추정기를 바꿔도 결과가 같아서 보정 효과도0이었다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 9. 동일 종료 권리의 전체 고정 순서 대조")]]
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

= #text("실패 예: 예산 밖 센서를 준비 표에서 읽었다")

#text("DEV에서는 초기 센서와 추가 두 개만 읽도록 계약했다. 그런데 실행할 행동이 아닌 준비용 상태표를 만들면서 마지막 남은 센서까지 포함한 mask15의 예측을 찾았다. 저장된 예측에 그 경우가 없어 선택표를 만들기 전 멈췄다.")

#text("따라서 예정된2명/524창에서 새 경로를 한 개도 평가하지 않았다. 결과를0오류나0비용으로 채우지 않고 오류율·비용·교정/피해는미실행으로 두었다. 실패한 본실험은 다시 보내지 않았고 다음 새 계약에서 고칠 문제로 남겼다.")

= #text("검산도 왜 실패했나")

#text("오류를 셀 때 보류한 경우0을8로 나누는 작은 표현이 정수0을 소수0.0으로 바꿨다. 뒤 합계도 소수가 되어 정확한7/160과 아주 조금 다른 binary 표현으로 저장됐다. 유리수와 정확히 같아야 한다는 검산은 그 차이를 찾아 멈췄다.")

#text("16032개 나무 점수의 대조는 그 전에 끝났지만 전체 검산은 통과하지 않았다. 작은 수치 차이를 이유로 검산 기준을 바꾸거나 원본을 고치지 않았다. unit10개가 통과했어도 실제 전체 흐름의 성공을 보장하지 못했다.")

= #text("남은 질문과 동결")

#text("새 실험에서는 예산 마지막 상태의 branches가 비어 있어야 하는 경계를 실제 cached mask와 함께 검사해야 한다. 보류를 포함한 합계도 끝까지 유리수인지 검사해야 한다. 같은 실험을 몰래 다시 돌려 이번 실패를 없애지는 않는다.")

#text("현실 자료에서 추정 보정과 적응의 효과를 분리하는 일, 새 독립 집단, 실제 센서 비용/실패, 외부 논문의 직접 비교는 남아 있다. 과거 MHEALTH1..10은 이미 썼고 최종 독립시험은0명이다.")

#text("API·모델 호출·추가 worker·의존성·전역 스킬 활성화는0이다. SOL 저술 사용량은 미계측이다. 정확한 Task/Dispatch에 완결된 실패 보고를 한 번 보내고 이 폴더를 동결한다.")

#block(width: 100%, breakable: false)[
= #text("무엇을 실제로 바꿨는가")

#text("기존 예측기는 고정했습니다. 사람5·6의 완전한 학습 행으로 하나의 공동 분포를 먼저 만들고, 관측된 토큰에 조건화한 같은 가중치로 예측 위험과 다음 토큰 전이를 함께 계산했습니다.")

#text("정적 순서10개에도 같은 관측별 STOP·보류·지원·비용 권리를 줬습니다. 총 블록 예산1·2·3에서 모든 대조군을 다시 최적화하고, DEV를 열기 전에 정책과 기준선을 동결했습니다.")

#block(width: 100%, inset: (top: 5pt, bottom: 5pt), above: 7pt, below: 7pt, stroke: (top: 0.7pt + rgb("#20394f"), bottom: 0.7pt + rgb("#20394f")), breakable: true)[
#set par(justify: false)
#set text(size: 9pt)
#block(sticky: true)[#strong[#text("Algorithm 10. Participant-balanced coherent joint calibration and matched finite acquisition")]]
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

= #text("결과와 해석의 경계")

#text("Coherent adaptive at totalbudget3 versus legacy empirical: regression (J gain -8059/196080); versus legacy statewise: regression (J gain -58067/686280).")

#text("완료 경로는 56592개이며 실제 고유 창은524개·이미 노출된 참가자는2명입니다. 독립 최종 평가자는0명입니다. 공동 분포 내부의 정확한 산술 일치는 새 사람의 일반화나 안전성을 뜻하지 않습니다.")

#text("기존 W50의 실패 기록은 그대로 보존했습니다. 새 모델 학습·추론·외부 API·물리 센서 측정·게시·공식 작업 정산은 이 실행에서 수행하지 않았습니다.")


]
#pagebreak()
= #text("사사")
#text("This work was created as part of the No-More-Slops group activities at Pseudo Lab.")

= #text("참고문헌과 실제 열람 범위")
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

