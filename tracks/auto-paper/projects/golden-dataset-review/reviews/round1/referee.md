# 심사보고서 (Round 1)

- 원고: LLM·RAG 애플리케이션 평가용 골든 데이터셋의 구축과 검증: 미니 리뷰 (Mini Review)
- 심사 대상 파일: `manuscript/paper.md`(빌드본), `reviews/round1/paper-v2.pdf`(A4 2단, 6쪽)
- 심사 기준: Frontiers in Artificial Intelligence Mini Review(본문 ≤3,000단어, 그림·표 ≤2, Abstract→Introduction→주제 소절→Discussion), 저자 목표 4쪽(+1–2쪽 허용)
- 심사일: 2026-10-25
- 원문 대조: arXiv abs/HTML, ACL Anthology PDF, 출판사·개발사 원문 페이지를 직접 열어 확인함(아래 "사실 대조 표" 참조). OpenAI 블로그(ref 49)는 403으로 직접 열지 못해 저자 기록(research/r2-verification.md)의 아카이브 인용을 2차 근거로만 사용함.

---

## 총평

원고는 LLM·RAG 애플리케이션 평가셋의 구축(4개 출처+RAG 요건)과 검증(5개 층위)을 74편의 문헌으로 압축하고, "골든"을 목적·버전에 대한 7조건 충족 증거의 문서화 상태로 정의하자는 제안과 2단(골든 핵심셋 + 은 표준 보조셋) 구성을 내놓는다. 인용 수치의 정확도는 높은 편이며(대조한 41개 항목 중 수치를 잘못 옮긴 사례는 없고, 주체·조건이 어긋난 서술 6건과 과장 2건), 실무자가 바로 쓸 수 있는 표 2의 점검표는 분명한 장점이다. 그러나 (1) 7조건이 Bowman–Dahl, BetterBench, Bean 등 기존 기준과 무엇이 다른지 대조되지 않고 통과 기준도 없어 정의가 사실상 "문서화 여부"로 환원되며, (2) 2단 구성의 핵심 근거가 되어야 할 예측 기반 추론(PPI)·AutoEval 문헌과 그 이론적 한계(Dorner 등, ICLR 2025)가 빠져 있어 핵심셋 규모(150–300 vs 약 1,000)에 대한 논증이 정합하지 않고, (3) "다섯 층위" 분류의 근거 사례가 층위 간 독립성을 직접 보이지 못하며, (4) 제목이 표방한 "애플리케이션" 평가셋 가운데 에이전트·다중 턴, 안전성·과잉 거부, 한국어·다국어 평가셋이 빠져 있다. 또한 핵심 사례로 쓴 SWE-bench Verified를 OpenAI가 2026년 2월 평가에서 제외했다는 사실이 반영되지 않았다. 이 문제들은 원고의 틀을 유지한 채 고칠 수 있으므로 판정은 다음과 같다.

**판정: Major revision**

---

## Major comments

### M1. 7조건 정의의 차별성과 판정 가능성이 입증되지 않았다

- **위치**: 초록 "셋째", 4장 둘째 문단(정의), 표 2, 6장 결론.
- **문제**:
  1. 저자는 "일곱 조건으로 나눈 구성은 어느 한 문헌이 제시한 것이 아니다"라고 쓰지만, 조건 대부분은 기존 기준과 겹친다. Bowman과 Dahl의 네 기준(validity, reliable annotation, statistical power, 편향 억제)[11]이 C1·C2·C3·C4에, BetterBench의 46개 모범 사례(설계–구현–문서화–유지)[12]가 C1·C4·C6·C7에, Bean 등의 권고[13]가 C1·C4에 대응한다. 기존 틀 대비 무엇이 새로운지(예: 애플리케이션 특화, C5 오염 통제와 C7 채점 기준 버전 관리의 결합, "증거 문서화" 상태라는 정의 방식)를 독자가 판단할 수 없다.
  2. 정의는 "조건을 충족한다는 증거가 문서로 남은" 상태인데, 표 2에는 C2(α 기준)와 C4(예시 계산)를 빼면 충족 여부를 가를 기준이 없다. 예컨대 α=0.45를 기록한 평가셋은 C2의 "증거가 문서로 남은" 것인가, 미충족인가? 기준이 없으면 정의는 문서화 여부로 환원되어 반증할 수 없다.
  3. 정의를 실제 평가셋에 적용한 예가 없다. 5.2절 마지막 문장이 스스로 인정하듯 제안은 검증되지 않았으며, 미니 리뷰라 해도 적용 예 하나가 없으면 결론의 "점검표로 쓸 수 있다"는 주장이 뒷받침되지 않는다.
- **근거**: Bowman & Dahl 2021 원문: "benchmarks should offer a valid test …, they should be built around consistently-labeled data, they should offer adequate statistical power, and they should disincentivize the creation of biased systems" (https://aclanthology.org/2021.naacl-main.385.pdf). BetterBench: https://arxiv.org/abs/2411.12990.
- **요구 수정**:
  - 표 2에 열 하나("기존 틀 대응": [11] 기준 번호, [12] 단계, [13] 권고)를 추가하거나 본문 두세 문장으로 대응 관계를 밝히고, 이 리뷰만의 추가분을 명시할 것.
  - 각 조건에 "충족/부분 충족/미충족"을 가를 최소 기준을 두거나, 기준을 정할 수 없는 조건은 "기준값 대신 무엇을 보고해야 하는가"로 명시할 것(예: C3 "무작위 표본 n개 감사, 오류율 95% 신뢰구간 상한 ≤x%").
  - 공개 사례 하나(예: SimpleQA[추가 문헌 A9] 또는 GSM8K-Platinum[5])에 7조건을 적용한 짧은 예시(표 2의 한 열 또는 3–4문장)를 넣을 것.

### M2. 2단 구성의 통계적 근거가 빠져 있고 핵심셋 규모 논증이 정합하지 않다

- **위치**: 4장 마지막 문단, 5.1 첫째 쟁점, 3.4절, 표 2 C4, 초록("소규모 평가셋").
- **문제**:
  1. "골든 핵심셋으로 대규모 LLM 판정 보조셋을 보정한다"는 설계는 예측 기반 추론(prediction-powered inference, PPI)과 그 평가 응용(AutoEval)으로 이미 정식화되어 있다. 원고가 인용한 ARES[22]도 PPI를 쓴다. 그런데 원고는 PPI 원전과 평가 응용을 인용하지 않아, 제안이 기존 통계 틀의 재진술인지 확장인지 알 수 없다.
  2. 더 중요하게, Dorner 등(ICLR 2025)은 판정 모델이 평가 대상 모델보다 정확하지 않으면 어떤 편향 보정 방법도 필요한 정답 라벨 수를 절반 넘게 줄일 수 없음을 보였다. 이는 "보조셋은 규모를 살려 회귀 탐지와 범위 확대를 맡는다"는 2단 구성의 이득에 정량적 상한을 준다. 이 결과를 다루지 않으면 2단 구성의 효용이 과대평가된다.
  3. 핵심셋 크기에 관해 원고는 150–300개(ARES)와 약 1,000개(Miller)를 함께 제시하고 "용도가 다르다"고만 말한다. 그러나 초록과 서론은 골든셋을 "소규모 평가셋"으로 전제한다. 1,000문항 핵심셋을 모두 C1–C7 수준으로 감사하는 비용이 실무자가 감당할 수준인지, 아니면 쌍체 설계·문항 간 상관을 이용해 필요한 n을 줄일 수 있는지 논의가 없다.
  4. Miller의 969는 특정 가정(조건부 분산 σ²_A=σ²_B=0, ω²=1/9, 독립 문항)에서 나온 예시 값이다. 표 2는 "가정한 예시"라고 적었지만 4장 마지막 문장은 가정 없이 "3%p 수준의 차이라면 약 1,000문항이 필요하다"고 단정한다. 쌍체 비교에서 두 모델 정답의 상관이 높으면 필요한 n은 크게 줄어든다(Miller 자신이 쌍체 분석을 권고함).
- **근거**:
  - Angelopoulos AN, Bates S, Fannjiang C, Jordan MI, Zrnic T. Prediction-powered inference. Science. 2023;382(6671):669–74. arXiv:2301.09633.
  - Boyeau P, Angelopoulos AN, Yosef N, Malik J, Jordan MI. AutoEval done right: using synthetic data for model evaluation. arXiv:2403.07008. 2024. 초록: "These algorithms increase the effective human-labeled sample size by up to 50% on experiments with GPT-4."
  - Dorner FE, Nastl VY, Hardt M. Limits to scalable evaluation at the frontier: LLM as judge won't beat twice the data. In: Proc ICLR; 2025. arXiv:2410.13341. 초록: "when the judge is no more accurate than the evaluated model, no debiasing method can decrease the required amount of ground truth labels by more than half."
  - Miller 2024 (https://arxiv.org/html/2411.00640): n≈969의 가정은 σ²_A=σ²_B=0, ω²=1/9.
- **요구 수정**:
  - 4장 2단 구성 문단에 PPI/AutoEval을 이론적 근거로 명시하고, Dorner 등의 상한을 한계로 적을 것. 5.1 셋째 쟁점(사람 vs LLM 라벨)에도 같은 근거를 연결할 것.
  - 핵심셋 규모를 "판정 모델 보정용(150–300, ARES)", "모델 선택용(검정력 계산; 쌍체 상관에 따라 달라짐)"으로 나누어 간단한 식(예: 쌍체 차이의 분산 = σ²_A+σ²_B−2ρσ_Aσ_B) 또는 민감도 한 줄을 제시하고, 4장 마지막 문장에 Miller의 가정을 되살릴 것.
  - 초록·서론의 "소규모 평가셋" 전제와 1,000문항 권고 사이의 긴장을 5.1 첫째 쟁점에서 명시적으로 다룰 것.

### M3. "서로를 보장하지 않는 다섯 층위" 분류의 정당성이 부족하다

- **위치**: 3장 제목·서두 문단, 3.5, 3.6, 6장 둘째 항목, 초록.
- **문제**:
  1. "층위(level)"는 위계를 함의하지만 다섯 항목은 위계가 아니라 병렬적인 측면(dimension)이다. 3.1은 구성 타당도가 "다른 모든 검증에 앞선다"고 하여 오히려 순서를 암시하는데, 나머지 사이의 관계는 제시되지 않는다.
  2. 분류의 근거로 든 세 사례가 "한 층위를 통과했지만 다른 층위에서 실패한" 사례로 깔끔하게 대응하지 않는다. [37]은 모델 합의(C3 내부 방법)의 한계이고, [38]은 평가셋이 아니라 판정 모델의 검증이며, [39]는 실행 환경 재현성이다. 즉 "C2를 통과했으나 C3에서 실패" 같은 대응을 보인 사례가 없다. 결론의 "검증의 다섯 층위는 서로를 보장하지 않았으며"는 이 근거보다 강한 주장이다.
  3. 3장은 "다섯 층위"를 표방하지만 소절은 여섯 개이며, 3.6(판정 모델 메타평가)은 C1–C7 어디에도 대응하지 않는다. 3.5는 "오염 통제와 재현성"을 묶었으나 재현성(ImageNetV2, Epoch의 실행 환경)은 오염과 원인이 다르다.
  4. C2(라벨 신뢰도)와 C3(오류 감사)는 경계가 흐리다. 3.3 첫 문장이 "일치도가 높아도 모두가 같은 오류를 범할 수 있으므로"라고 두 층위의 관계를 설명하는데, 이는 HLE(전문가 작성+검토 후에도 화학·생물 정답 약 29%가 문헌과 충돌)처럼 직접 근거가 있는 사례로 보강되어야 한다.
- **근거**: FutureHouse. About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong [blog]. 2025 Jul 23. https://www.futurehouse.org/research/hle-exam ("29 ± 3.7% (95% CI)" … "directly conflicting evidence in peer reviewed literature"). HLE 팀의 후속 검토도 Bio/Chem 부분집합의 약 18%를 문제 문항으로 판정함(같은 페이지 2025-09-16 갱신).
- **요구 수정**:
  - "층위"를 "검증 차원" 또는 "검증 측면"으로 바꾸거나, 층위라는 용어를 유지할 경우 그 순서의 의미를 정의할 것.
  - 3장 서두에 "X를 통과했지만 Y에서 실패"의 대응을 보이는 사례를 2–3개 명시할 것(예: GPQA·HLE 전문가 검토 통과 → 오류 감사 실패; GSM8K 공개·광범위 사용 → GSM1k 오염 실패; SWE-bench Verified 전문가 선별 통과 → 실행 환경·시험 결함 실패).
  - 3.6은 4장 2단 구성 문단으로 옮기거나, "골든셋의 용도"로 3장 밖에 독립시킬 것. 재현성은 C5에서 분리하거나 C5 이름을 "오염·재현성 통제"로 바꿔 표 2와 일치시킬 것.
  - 결론의 "서로를 보장하지 않았으며"를 "한 측면의 통과가 다른 측면의 문제를 배제하지 못한 사례가 보고되었다" 수준으로 낮출 것.

### M4. "애플리케이션 평가셋"을 표방하면서 주요 애플리케이션 유형과 실무 관점이 빠져 있다

- **위치**: 1장 셋째 문단(범위), 2장 전체, 3.2–3.4, 5.2 셋째 공백.
- **문제**: 근거 대부분이 공개 학술 벤치마크(ImageNet, MMLU, GSM8K, SNLI)에서 나왔고, 제목이 지칭하는 애플리케이션 평가셋의 다음 유형·관점이 빠져 있다. 분량 제약을 고려해 우선순위를 표시하였다(★ 꼭 필요).
  1. ★ **에이전트·다중 턴 평가셋**: 도구 사용 에이전트는 오늘날 LLM 애플리케이션의 주류이며, 정답이 "최종 상태"로 정의되고 반복 실행 신뢰도(pass^k)가 핵심이라 골든셋의 정의(C1, C4)가 달라진다.
     - Yao S, Shinn N, Razavi P, Narasimhan K. τ-bench: a benchmark for tool-agent-user interaction in real-world domains. arXiv:2406.12045. 2024.
     - Bai G, Liu J, Bu X, et al. MT-Bench-101: a fine-grained benchmark for evaluating large language models in multi-turn dialogues. In: Proc ACL; 2024. arXiv:2402.14762.
     - Liu X, Yu H, Zhang H, et al. AgentBench: evaluating LLMs as agents. In: Proc ICLR; 2024. arXiv:2308.03688.
  2. ★ **안전성·레드팀·과잉 거부 평가셋**: 안전성 골든셋은 거부해야 할 문항과 거부하면 안 되는 문항의 비대칭 비용, 유해 프롬프트 공개에 따른 오염·악용 위험이 있어 C5·C6 운영이 다르다.
     - Mazeika M, Phan L, Yin X, et al. HarmBench: a standardized evaluation framework for automated red teaming and robust refusal. In: Proc ICML; 2024. arXiv:2402.04249.
     - Röttger P, Kirk HR, Vidgen B, et al. XSTest: a test suite for identifying exaggerated safety behaviours in large language models. In: Proc NAACL; 2024. arXiv:2308.01263.
     - Cui J, Chiang WL, Stoica I, Hsieh CJ. OR-Bench: an over-refusal benchmark for large language models. In: Proc ICML; 2025. arXiv:2405.20947.
  3. ★ **한국어·다국어 평가셋 구축 사례**: 5.2절은 "한국어 등 다른 언어의 애플리케이션 평가셋에서 … 재검증해야 한다"고 공백으로 제시하지만, 번역 기반 평가셋의 결함과 원어 구축의 필요성을 다룬 문헌이 이미 있다. 한국어 원고에서 이 문헌을 빠뜨리는 것은 특히 아쉽다.
     - Son G, Lee H, Kim S, et al. KMMLU: measuring massive multitask language understanding in Korean. In: Proc NAACL; 2025. arXiv:2402.11548. (영어 번역 대신 한국 시험 원문으로 구축)
     - Son G, Lee H, Kim S, et al. HAE-RAE Bench: evaluation of Korean knowledge in language models. In: Proc LREC-COLING; 2024. arXiv:2309.02706.
     - Singh S, Romanou A, Fourrier C, et al. Global MMLU: understanding and addressing cultural and linguistic biases in multilingual evaluation. In: Proc ACL; 2025. arXiv:2412.03304. (번역 오류와 문화 민감 문항 분리)
  4. ★ **골든셋 구축의 모범·반례로서의 최근 사례**:
     - Wei J, Karina N, Chung HW, et al. Measuring short-form factuality in large language models (SimpleQA). arXiv:2411.04368. 2024. 두 명의 작성자가 독립적으로 같은 답을 낸 문항만 남기고, 세 번째 작성자의 1,000문항 재풀이로 고유 오류율을 약 3%로 추정함(https://arxiv.org/html/2411.04368). 표 2의 C2·C3 증거를 실제로 남긴 드문 사례이다.
     - Phan L, Gatti A, Han Z, et al. Humanity's Last Exam. arXiv:2501.14249. 2025 및 위 FutureHouse 감사(M3). 전문가 작성과 상금 구조가 오류를 낳은 사례로 2.1절에 필요하다.
  5. **문항 분석(IRT)**: tinyBenchmarks[53]만 인용되어 IRT가 "축소 표본" 도구로만 소개된다. IRT는 변별도가 낮거나 이상한 문항을 찾는 C3 도구이기도 하다.
     - Vania C, Htut PM, Huang W, et al. Comparing test sets with item response theory. In: Proc ACL; 2021. arXiv:2106.00840.
     - Rodriguez P, Barrow J, Hoyle AM, et al. Evaluation examples are not equally informative: how should that change NLP leaderboards? In: Proc ACL; 2021. doi:10.18653/v1/2021.acl-long.346.
  6. **사람 주석 품질 관리와 LLM 주석의 비교**: 3.2와 5.1 셋째 쟁점은 주석 오류 탐지와 LLM 주석의 비교 문헌 없이 진행된다.
     - Klie JC, Webber B, Gurevych I. Annotation error detection: analyzing the past and present for a more coherent future. Comput Linguist. 2023;49(1):157–98. arXiv:2206.02280.
     - Gilardi F, Alizadeh M, Kubli M. ChatGPT outperforms crowd workers for text-annotation tasks. Proc Natl Acad Sci U S A. 2023;120(30):e2305016120. arXiv:2303.15056.
     - Chiang CH, Lee HY. Can large language models be an alternative to human evaluations? In: Proc ACL; 2023. arXiv:2305.01937.
  7. **평가 신호 대 잡음과 재현 가능한 평가 실행**: 3.4·3.5 보강.
     - Heineman D, Hofmann V, Magnusson I, et al. Signal and noise: a framework for reducing uncertainty in language model evaluation. arXiv:2508.13144. 2025.
     - Biderman S, Schoelkopf H, Sutawika L, et al. Lessons from the trenches on reproducible evaluation of language models. arXiv:2405.14782. 2024.
  8. **데이터셋 버전 관리 도구**: C7은 "버전 이력"을 요구하지만 구체 수단이 없다. 최소한 Hugging Face Datasets(Lhoest Q, Villanova del Moral A, Jernite Y, et al. Datasets: a community library for natural language processing. In: Proc EMNLP System Demonstrations; 2021. arXiv:2109.02846)의 버전·데이터 카드 기능이나 DVC 같은 도구를 한 문장으로 언급할 것.
- **요구 수정**: 위 1–4는 본문에 반영하고(각 1–2문장), 5–8은 해당 절에 짧게 반영할 것. 분량을 맞추기 위해 애플리케이션 평가셋과 거리가 먼 인용(예: ImageNet 재현[60]은 [57]로 대체 가능, CALBC[65], Dynabench[27], HELM[73], MS MARCO·NQ 표집 출처[16,17] 중 하나)을 줄이는 것을 권한다. 1장 셋째 문단의 범위 서술에 "에이전트·안전성·다국어 평가셋은 다루지 않는다"와 같이 제외 범위를 명시하는 것도 대안이다. 다만 그 경우 제목과 초록의 "애플리케이션"을 좁혀야 한다.

### M5. 핵심 사례 SWE-bench Verified의 최신 상태가 반영되지 않았다

- **위치**: 3장 서두, 3.3(전문 개발자 검토 사례), 3.5(Epoch의 16문항 제외), 참고문헌 [39], [49].
- **문제**: 원고는 SWE-bench Verified를 "전문가 검수를 거친 집합"의 대표 예로 두 번 쓰지만, OpenAI는 2026년 2월 23일 이 벤치마크를 더 이상 평가에 쓰지 않는다고 발표했다. 발표에 따르면 모델이 자주 실패한 문항 중 감사한 부분집합의 최소 59.4%가 올바른 해법을 거부하는 결함 있는 시험을 가졌고, 학습 데이터 오염도 이유로 제시되었다. 이 사실은 원고의 논지(검증된 집합도 시간이 지나면 골든이 아니다, 감사 결과는 하한이다, C7 유지·폐기 필요)를 가장 직접적으로 뒷받침하는 최신 근거이다. 저자의 조사 기록(research/r1-validation.md, S9)에도 "UNVERIFIED"로 언급되었으나 본문에 반영되지 않았다. 또한 참고문헌 [1]의 OpenAI Evals 문서는 플랫폼 폐지(2026-11-30 종료 예정)를 공지하고 있어, 5.3절이 말한 회색 문헌의 변동 위험이 이미 현실화되었다.
- **근거**: OpenAI. Why SWE-bench Verified no longer measures frontier coding capabilities [blog]. 2026 Feb 23. https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ ("at least 59.4% of the audited problems have flawed test cases that reject functionally correct submissions"). OpenAI Evals 가이드(https://developers.openai.com/api/docs/guides/evals)의 폐지 공지.
- **요구 수정**: 3.3 또는 3.5에 SWE-bench Verified의 폐기와 그 사유를 한두 문장으로 추가하고, 4장 C7(폐기 기준) 근거로 연결할 것. 참고문헌 [1]에 폐지 일정을 주기하거나 5.3에서 언급할 것.

### M6. 인용 근거의 범위를 넘거나 원문과 어긋나는 서술이 여러 곳 있다

- **위치·문제·근거·요구 수정**(상세 수치는 아래 사실 대조 표 참조):
  1. **초록 "라벨 오류"(MMLU)**: Gema 등의 6.49%와 Virology 57%는 정답 라벨 오류만이 아니라 문항 불명확, 선지 불명확, 정답 없음, 복수 정답을 포함한 "오류(errors)"이다(https://arxiv.org/abs/2406.04127 "6.49% of MMLU questions contain errors"). 초록과 영문 초록의 "label errors"를 "오류(문항·선지·정답 오류 포함)"로 고칠 것.
  2. **3.6 "가장 큰 판정 모델조차 … 최대 5점까지 달랐고"[38]**: 원문은 정렬도(Scott's π)가 가장 높은 판정 모델(GPT-4 Turbo, Llama-3 70B)이 최대 5점 차이를 보였다는 것이며, 크기가 아니라 정렬도 기준이다. 또한 실험은 TriviaQA 400문항의 "사람 간 일치도가 높은 깨끗한 설정"이었다(https://arxiv.org/html/2406.12624). "정렬도가 가장 높은 판정 모델도 TriviaQA 기반 설정에서 …"로 고치고 일반화의 한계를 적을 것.
  3. **2.3 "자기 인식과 자기 선호의 강도가 상관을 보였으며"[23]**: 선형 상관은 미세조정 실험에서 발견되었다("By fine-tuning LLMs, we discover a linear correlation…", https://arxiv.org/abs/2404.13076). "미세조정으로 자기 인식 능력을 바꾸자 자기 선호 강도가 선형으로 변하였다"로 고칠 것.
  4. **3.4 "특이한 모델에서는 추정이 덜 정확하였다"[53]**: 원문에서 성능이 크게 떨어진 것은 정답 기반(correctness-based) 앵커 전략이며, IRT 기반 방법은 전문화된 모델에서도 "약간"만 영향을 받았다(https://arxiv.org/html/2402.14992). 문장 주어가 "문항 반응 이론으로 고른 100문항"이라 원문과 반대로 읽힌다. 주된 한계로 원문이 든 심한 분포 이동을 쓰는 편이 정확하다.
  5. **3.3 "15개 벤치마크를 수정하였고"[37]**: 대부분 벤치마크에서 무작위 부분집합(100–273문항)을 정제한 것이다("we select smaller subsets at random from many of these benchmarks", https://arxiv.org/html/2502.03461). "15개 벤치마크의 부분집합을 정제하였고"로 고칠 것.
  6. **3.4 "이 층위가 실무에서 가장 자주 생략됨을 보여 준다"**: [13]의 16.0%는 통계 검정 사용률이며, 다른 층위의 생략률과 같은 척도로 비교한 결과가 아니다. "가장"을 삭제하거나 비교 근거를 제시할 것.
  7. **4장 "유해 시스템 억제"(Bowman–Dahl 넷째 기준)**: 원문은 "plausibly harmful social biases를 드러내고 편향된 시스템을 만들 유인을 주지 않을 것"이다. "사회적 편향을 드러내고 편향된 시스템을 유인하지 않을 것"으로 고칠 것.
  8. **3.5 "GSM8K 문항의 생성 확률이 높은 모델일수록 하락 폭이 컸다"[57]**: 원문은 Spearman r²=0.36의 양의 관계이다. "중간 정도의 양의 관계(r²=0.36)"로 강도를 밝힐 것.

### M7. 논의(5.1)가 학파·논쟁을 충분히 다루지 않고, 모든 쟁점을 "용도에 따라 결합"으로 해소한다

- **위치**: 5.1 첫째–셋째 쟁점.
- **문제**: Frontiers Mini Review의 Discussion은 서로 다른 학파와 논쟁을 다루어야 한다. 그런데 첫째 쟁점은 개발사 문서 한 문장[2]과 학술 기준[11,37]을 대비시켜 회색 문헌을 한 학파로 세우는 구도이고, 세 쟁점 모두 "두 입장이 서로 다른 용도를 겨냥한다"는 같은 방식으로 해소된다. 실제 논쟁은 더 날카롭다. 예를 들어 (a) LLM 판정으로 사람 라벨을 줄일 수 있는 이론적 한계(Dorner 등)와 LLM 주석이 군중 작업자를 능가한다는 보고(Gilardi 등, Thomas 등[30])의 대립, (b) 정적 골든셋 대 동적·지속 갱신 벤치마크(LiveBench[58], Dynabench[27])의 대립, (c) 관점주의[45,47]가 회귀 검사의 결정성 요구와 어떻게 공존하는가에 대한 구체 방법(예: 분포형 문항의 채점 규칙)이 다뤄지지 않는다.
- **요구 수정**: 각 쟁점에서 양쪽의 학술적 근거를 한 편 이상씩 대비하고, 절충안이 성립하지 않는 조건(예: Dorner의 상한이 걸리는 경우, 분포형 문항으로 회귀 판정을 내려야 하는 경우)을 명시할 것. 정적 대 동적 평가셋 논쟁을 하나의 쟁점으로 추가하는 것을 권한다.

---

## Minor comments

### 내용·논증

- **m1. 초록 구조** (국문 초록): "세 질문에 답한다"라고 하고 질문을 제시하지 않은 채 "첫째, …"로 답을 나열한다. 질문을 한 구절씩 밝히거나 "세 가지를 정리한다"로 바꿀 것. 국문 초록(약 180어절, 10행)은 2단 조판 전폭에서 길게 보인다. 대상 기간 "2015–2026년"은 본문에서 2000–2010 문헌도 포함했다고 밝히므로 "주로"를 영문 초록과 함께 유지하되 본문과 일치시킬 것.
- **m2. 2장 마지막 문단의 자기모순**: "네 방식의 위험은 서로 겹치지 않는다"라고 한 직후 "전문가 작성과 적대적 수집은 … 비용과 모호성을 지고, 로그와 합성은 … 정답 검증을 뒤로 미룬다"고 하여 두 방식씩 위험을 공유한다고 쓴다. "네 방식은 서로 다른 위험을 진다" 또는 "두 묶음으로 갈린다"로 고칠 것.
- **m3. 표 1의 범주 혼합**: "RAG 추가 요건"은 구축 방식이 아니라 요구사항이므로 같은 표의 행으로 두면 "장점" 열("검색·생성 오류의 분리 진단")이 어색하다. 표 아래 각주로 옮기거나 열 이름을 "구축 방식/요건"으로 바꿀 것.
- **m4. 3장 서두의 전방 참조와 중복**: 3장 서두가 "4장 표 2의 조건 C1–C5에 대응한다"고 하고 4장 둘째 문단이 "C1–C5는 3장의 다섯 검증 층위에 차례로 대응"한다고 다시 쓴다. 한 곳(4장)에서만 밝힐 것.
- **m5. Northcutt 수치 표현(1장)**: "오류 문항의 비중이 6%만 늘어도"는 비율 증가(%)인지 백분율포인트(%p) 증가인지 모호하다. 원문은 "prevalence of originally mislabeled test examples increases by just 6%"이다. 원문 실험(정정된 시험셋에서 오류 문항 비중을 조정)에 맞추어 %인지 %p인지 확인하고 단위를 명확히 할 것.
- **m6. GPQA 기준(2.1)**: Diamond의 전문가 조건은 "첫 번째 검토자가 정답, 두 번째 검토자는 정답이거나 오답 후 실수를 명확히 인정"이다. "두 명이 모두 정답에 동의"는 근사이므로 "두 전문가 검토자가 모두 정답을 확인하고"로 바꾸거나 각주를 붙일 것.
- **m7. HealthBench 해석(2.1)**: 55–75%는 원문 Discussion의 요약이고, 표 기준 의사 간 macro F1은 주제별 0.569–0.730, 모델–의사 전체는 0.709이다. 원문은 이를 "모델 채점기가 의사 수준에 이른다"는 근거로 쓰는데 원고의 "머물렀다"는 전문가 잡음을 강조하는 해석이다. 해석의 방향을 밝히고 "주제별"을 덧붙일 것.
- **m8. 적대적 수집의 역사 서술(2.4)**: "주석 흔적 보고[25] 이후 쉬운 단서를 피하는 방법으로 주목받았다"는 인과·연대 주장에 근거가 없다(적대적 필터링 SWAG는 같은 2018년). "주석 흔적 문제[25]에 대한 대응의 하나로 쓰였다" 정도로 낮출 것.
- **m9. ANLI 해석(2.4)**: 18.54%/9.52%는 세 라운드 합계(A1–A3)이며 라운드별 차이가 크다(A1 29.68→18.33%). "전체 라운드 합계 기준"을 밝힐 것.
- **m10. LLM 관련성 판정의 프롬프트 민감성(2.5)**: 이 주장의 근거는 Thomas 등[30]("simple paraphrases" 차이)이다. UMBRELA[31]는 재현 구현이므로 이 문장에는 [30]만 두고 [31]은 "오픈소스 재현"으로 따로 소개하거나 삭제할 것.
- **m11. ALCE κ(2.5)**: 0.698은 인용 재현율(citation recall), 0.525는 인용 정밀도(citation precision)이다. 범위로 묶지 말고 구분해 쓸 것.
- **m12. Artstein–Poesio 예(3.2)**: 원문 표 8의 계수는 다중 코더 K(π 계열)이며 Cohen의 κ가 아니다. "κ" 대신 "K(우연 보정 계수)"로 쓰거나 각주를 붙일 것.
- **m13. OpenAI 문서 서술(1장)**: 해당 문서는 "평가 주도 개발(eval-driven development)"이라는 용어를 쓰지 않고 BDD와 비슷한 절차로 설명한다("somewhat similar to behavior-driven development"). 표현을 원문에 맞출 것.
- **m14. Self-Instruct의 이전 가능성(2.3)**: 학습용 지시문 합성 결과를 평가셋 합성의 근거로 쓰는 데는 비약이 있다. "평가셋 합성에도 같은 위험이 있음을 시사한다" 정도로 한정할 것.
- **m15. 5.2 셋째 공백**: M4-3의 한국어·다국어 문헌을 반영한 뒤, 공백을 "애플리케이션 수준의 한국어 RAG 평가셋에서 일치도·규모 기준을 실증한 연구가 드물다"로 좁힐 것.
- **m16. 5.3 방법 투명성**: 문헌 검색과 요약에 LLM 에이전트를 썼다고 밝혔으므로, 검색 질의어 목록, 검색·포함 편수, 원문 대조 절차(research/r2-verification.md 수준의 기록)를 보충 자료로 제시할 것. 미니 리뷰에 PRISMA는 필요 없지만 AI 보조 검색은 재현 정보가 있어야 신뢰할 수 있다.

### 문체·용어

- **m17. 용어 통일**: 평가셋(36회)·시험셋(6)·시험 모음(5)·벤치마크가 혼용되고, 골든셋(3)·골든 데이터셋(5)·골든 핵심셋, 판정 모델(16)·자동 판정 모델·자동 채점기(1)가 섞여 있다. 1장에서 "평가셋(evaluation set)"과 "시험 모음(test collection, 정보검색 용어)"을 정의하고 나머지는 하나로 통일할 것. "층위"는 M3에 따라 정리할 것.
- **m18. "이 리뷰" 반복**: 본문에서 19회 쓰였다. 4장 첫 문단 끝 "이 리뷰는 이 흐름을 근거로", 4장 둘째 문단 "이 리뷰는 … 제안한다", 4장 마지막 문단 "이 리뷰는 … 제안한다"가 연속된다. 주어를 생략하거나 "본고"·"여기서는"으로 바꿀 것.
- **m19. 긴 문장**: 1장 둘째 문단 Northcutt 문장, 2.3 Self-Instruct–ARES 문장, 3.5 Oren 문장("문항 순서"가 한 문장에 세 번), 4장 첫 문단 Voorhees 문장이 길다. 각 문장을 둘로 나눌 것.
- **m20. 번역투·상투 표현**: "~라는 점은 … 거듭 확인되었다", "한데 묶은 리뷰는 … 확인되지 않았다", "~을 거쳐야 한다"의 연속 사용이 단조롭다. 3.3 마지막 문장과 3.4 마지막 문장처럼 소절을 같은 형태의 규범 문장("~해야 한다")으로 끝내는 패턴이 반복된다. 소절 첫 문장이 이미 주장을 밝히므로(두괄식) 마지막 규범 문장 일부는 생략해도 된다.
- **m21. 시제**: 문헌 결과는 과거형으로 일관되나 2.2 "로그 사용은 … 전제로 하며", 2.5 첫 문장 등 일반 진술과 문헌 진술이 한 문장에 섞인 곳이 있다. 일반 진술(현재형)과 문헌 결과(과거형)를 문장 단위로 분리할 것.
- **m22. 영문 초록**:
  - "label errors at rates of a few percent overall and, in some subsets, in more than half of the analyzed items" → "errors in a few percent of items overall and in more than half of the analyzed items in some subsets" (M6-1의 "label" 삭제 포함).
  - "a state in which evidence that seven conditions are met is documented for a stated purpose and version" → "a state in which, for a stated purpose and version, documented evidence shows that seven conditions are met".
  - "Validation can be organized into five levels" → M3 반영 시 "five dimensions".
  - "none of them secures correctness, realism, and low cost at once" → "none achieves correctness, realism, and low cost simultaneously".
  - 국문 초록에는 쟁점 개수("세 가지")가 없고 영문 초록에는 "three controversies"가 있다. 맞출 것.

### 형식·참고문헌·조판

- **m23. Vancouver 형식 불일치**:
  - 저자 표기: ICMJE/NLM 방식은 6명까지 모두 쓰고 7명 이상이면 처음 6명 뒤 "et al."이다. 원고는 3명 뒤 "et al."([4],[6],[8] 등)과 6명 전부([12],[25])를 섞어 쓴다. 한 방식으로 통일할 것(Frontiers 지침 확인).
  - 학회 표기: "In: Proc NAACL"과 "In: NeurIPS Datasets and Benchmarks Track"(Proc 없음), AAAI를 학술지처럼 권·호로 쓴 [35],[47]이 섞여 있다.
  - [39] Epoch AI 항목에 연도·갱신일이 없다. [1],[2],[21]은 연도 2026이 접근일과 같아 판(版) 정보가 없다.
  - [37]은 학회 판이 없다면 "Preprint"를, [5]와 [37]의 저자 순서가 다르다는 점은 의도된 것이므로 그대로 두되 혼동을 피하도록 본문에서 "Vendrow 등[37]"과 블로그[5]를 구분해 쓸 것.
  - [74] UIST는 논문 번호(article number) 체계이므로 "p. 1–14" 대신 ACM 메타데이터의 논문 번호를 표기하는 편이 정확하다.
- **m24. Frontiers 필수 항목 누락**: Author contributions, Funding, Conflict of interest, (해당 시) Data availability 진술이 없다. 저자명이 GitHub 핸들("sooyoung-wind")이고 소속이 "Pseudo-Lab no-more-slops, Auto-Paper 트랙"으로 되어 있으며, 교신 저자 연락처가 없다. 투고 형식에 맞게 실명·기관·연락처를 쓸 것.
- **m25. 분량**: 본문(1장–6장) 약 2,610단어(표 제외), 표 포함 약 2,980단어로 3,000단어 한도에 근접한다. M4 반영 시 한도를 넘을 수 있으므로 M4에서 제안한 인용 축소와 3.6 통합(M3)으로 상쇄할 것. 참고문헌 74편은 미니 리뷰로는 많다(PDF 2쪽 분량). 조판 결과는 6쪽(본문 4쪽+α, 참고문헌 1.5쪽)으로 저자 목표(4쪽+2쪽 허용)의 상한이다. 참고문헌을 50–60편으로 줄이면 5쪽 안에 들어갈 것으로 보인다.
- **m26. 조판 품질(PDF)**:
  - 본문 국문은 명조 계열인데 라틴 문자·숫자는 다른 세리프 글꼴(Times 계열)로 찍혀 기준선과 굵기가 맞지 않는다(1쪽 서론 "Northcutt", "3.3%", 2쪽 "BEIR", "nDCG@10"). 국문 글꼴에 어울리는 라틴 글꼴을 지정할 것.
  - 양쪽 정렬로 어절 간격이 크게 벌어진 행이 많다(1쪽 오른쪽 단 문헌 검색 문단, 4쪽 왼쪽 단 정의 문단, 5쪽 결론 문단). 한국어 양쪽 정렬에서 글자 사이 조정(letter-spacing 허용)이나 왼쪽 정렬을 검토할 것.
  - 표 1이 2쪽 하단에 전폭으로 들어가면서 2장 마지막 문단이 표 아래 좌우 단으로 갈려(2쪽 하단) 읽는 순서가 끊긴다. 표를 2장 첫 부분 또는 쪽 상단에 배치할 것.
  - 참고문헌 [49]의 아카이브 URL이 단어 중간("introdu-cing")에서 끊긴다. URL 줄바꿈을 슬래시 뒤로 제한하거나 아카이브 URL을 생략할 것.
  - 6쪽은 왼쪽 단만 차고 오른쪽 단이 약 3분의 2 비어 있다. 참고문헌을 줄이면 해소된다.
  - 제목의 쌍점(":")이 다른 글꼴로 조판되어 앞뒤 간격이 어색하다(1쪽 제목, 2쪽 "2. 구축:", 3쪽 "3. 검증:").
- **m27. 표 2 형식**: "문헌의 근거·기준값" 열이 기준값(α≥0.800)과 사례(GSM1k 8% 하락)와 개념(신화, 기준 표류)을 한 열에 섞는다. "기준값"과 "근거 사례"를 구분하거나 기준값이 없는 칸에 "기준값 없음"을 명시할 것(M1-2와 연계). C1 행의 "47.8%가 논쟁적 정의"는 원고 본문의 "합의되지 않은 개념"과 표현을 맞출 것.

---

## 사실 대조 표

판정: **정확** = 원문과 일치, **부정확** = 수치는 맞으나 범위·주체·조건이 어긋남, **과장** = 원문보다 강한 주장, **확인 불가** = 원문 직접 접근 불가.

| # | 항목 | 원고 서술 | 원문 (출처) | 판정 |
|---|---|---|---|---|
| 1 | Northcutt [3] 평균 오류율 | 시험셋 10종 평균 3.3% 이상 | "an average of at least 3.3% errors across the 10 datasets" (arxiv.org/abs/2103.14749) | 정확 |
| 2 | Northcutt [3] 순위 역전 | 오류 문항 비중 6%만 늘어도 ResNet-18이 ResNet-50을 앞섬 | "ResNet-18 outperforms ResNet-50 if the prevalence of originally mislabeled test examples increases by just 6%" | 정확(%/%p 모호, m5) |
| 3 | MMLU [4] | 6.49% 오류, Virology 분석 문항 57% | "6.49% of MMLU questions contain errors"; "57% of the analysed questions in the Virology subset contain errors" (arxiv.org/abs/2406.04127) | 본문 정확 / 초록의 "라벨 오류"는 부정확(M6-1) |
| 4 | GSM8K-Platinum [5] | 원래 45개씩 틀린 두 모델이 2개와 17개 | Claude 3.7 Sonnet(extended thinking)과 Llama 405B가 GSM8K에서 각 45개, Platinum에서 2개와 17개 (gradientscience.org/gsm8k-platinum) | 정확 |
| 5 | GSM8K-Platinum [5,37] | 219문항 검토, 110 제거, 10 정답 수정 | "219 flagged questions, of which 110 were removed, 99 were verified, and 10 had mislabeled answers" | 정확 |
| 6 | Platinum [37] | 15개 벤치마크를 수정 | "revise examples from fifteen existing popular benchmarks"; "we select smaller subsets at random from many of these benchmarks"(100–273문항) (arxiv.org/html/2502.03461) | 부정확(부분집합, M6-5) |
| 7 | Platinum [37] 하한 | 찾은 오류 수가 하한 | "the number of errors that we identify for each benchmark is only a lower bound" | 정확 |
| 8 | GPQA [14] Diamond | 전문가 두 명 모두 정답 동의, 비전문가 정답률 ≤1/3, 198문항 | 첫 검토자 정답 필수, 두 번째는 정답 또는 실수 인정; 비전문가 ≤1/3; 비전문가 3명, 인터넷 사용 허용 (arxiv.org/html/2311.12022) | 대체로 정확(m6) |
| 9 | GPQA [14] 보수 | 시간당 평균 약 95달러 | "an average hourly payment of approximately $95 per hour" | 정확 |
| 10 | HealthBench [15] | 의사 262명, 채점 기준 48,562개 | "262 physicians"; "48,562 unique rubric criteria" (arxiv.org/abs/2505.08775) | 정확 |
| 11 | HealthBench [15] 일치도 | 의사 간·모델–의사 일치도(macro F1) 모두 55–75% | Discussion "range from 55% to 75%"; 표: 의사 간 주제별 0.569–0.730, 모델 전체 0.709 (arxiv.org/html/2505.08775) | 정확(해석 방향, m7) |
| 12 | Arena-Hard [18] | 20만 질의, 4,000 주제, 7개 품질 기준, 500개 | "initial pool of 200,000 prompts"; "4,000 distinct topics"; "seven key qualities"; 250개 군집에서 2개씩 = 500 (arxiv.org/html/2406.11939) | 정확 |
| 13 | Self-Instruct [20] | 200개 검토, 지시문 92% 타당, 전체 올바름 54% | 표 2: 92%, "All fields are valid" 54%, 200개 표본 (arxiv.org/html/2212.10560) | 정확 |
| 14 | ARES [22] | 왕복 일관성 필터, 사람 라벨 150–300개 | "retrieve its original passage as the top result"; Limitations "roughly 150-300 datapoints" (arxiv.org/html/2311.09476) | 정확 |
| 15 | Panickssery [23] | GPT-4·Llama 2가 자기 출력 구별, 자기 인식–자기 선호 상관 | "out of the box … non-trivial accuracy at distinguishing themselves"; "By fine-tuning LLMs, we discover a linear correlation" (arxiv.org/abs/2404.13076) | 부정확(미세조정 조건 누락, M6-3) |
| 16 | Gururangan [25] | 가설만으로 SNLI 약 67% | "correctly classify the hypothesis alone in about 67% of SNLI" (arxiv.org/abs/1803.02324) | 정확 |
| 17 | ANLI [26] | 18.54% → 9.52% | 표 2 ANLI 합계 Unverified 18.54%, Verified 9.52% (arxiv.org/html/1910.14599) | 정확(합계 기준 명시 필요, m9) |
| 18 | BEIR [29] | 밀집 검색기 Hole@10 최대 31.8%, 980건 추가, DPR 0.332→0.445, ANCE가 BM25 추월 | 표 4: TAS-B 31.8%; "annotated 980 query-document pairs"; DPR 0.332→0.445; ANCE 0.654→0.735, BM25 0.656→0.668 (arxiv.org/pdf/2104.08663) | 정확 |
| 19 | ALCE [32] | Cohen's κ 0.525–0.698 | "substantial agreement for citation recall (0.698) and moderate agreement for citation precision (0.525)" (arxiv.org/html/2305.14627) | 정확(지표 구분 필요, m11) |
| 20 | CRAG [33] | 4,409개 질의, 인기도 낮고 변동 큰 층에서 정확도 낮음 | "4,409 question-answer pairs"; "much lower accuracy … higher dynamism, lower popularity" (arxiv.org/abs/2406.04744) | 정확 |
| 21 | MultiHop-RAG [34] | 답할 수 없는 질의 301개 | 표 3 Null Query 301(11.78%), 전체 2,556 (arxiv.org/html/2401.15391) | 정확 |
| 22 | Bean [13] | 445개 중 78.2% 정의, 정의의 47.8% 논쟁적, 16.0% 통계 검정 | "445 LLM benchmarks"; "(78.2%)"; "47.8% are contested"; "16.0% used uncertainty estimates or statistical tests" (arxiv.org/html/2511.04703) | 정확 / "가장 자주 생략"은 과장(M6-6) |
| 23 | Artstein–Poesio [43] | 관측 일치율 0.96이어도 κ 0.65 | 표 8 Case 1: Ao=0.96, Ae=0.89, K=0.65 (aclanthology.org/J08-4004.pdf) | 정확(계수는 K, m12) |
| 24 | Truong [48] | 벤치마크 9종, 최대 84% 정밀도 | "Across nine widely used benchmarks … up to 84% precision" (arxiv.org/abs/2511.16842) | 정확 |
| 25 | SWE-bench Verified [49] | 93명, 1,699개, 68.3% 제거, 500개 선정 | 저자 기록의 아카이브 인용(research/r2-verification.md); openai.com 403, web.archive.org 접근 차단 | 확인 불가(2차 근거로는 일치) |
| 26 | Epoch [39] | 500문항 중 16문항 제외 | "We exclude 16 samples that do not reliably run in our infrastructure"; 484개 사용 (epoch.ai/benchmarks/swe-bench-verified) | 정확 |
| 27 | EvalPlus [50] | 시험 80배, pass@k 최대 19.3–28.9% 하락 | "extend the test-cases … by 80x"; "reduces pass@k by up-to 19.3-28.9%" (arxiv.org/abs/2305.01210) | 정확 |
| 28 | Card [51] | 문장 2,000개 MT 시험셋은 BLEU 1점 차를 약 75% 검정력 | "typical test sets of 2000 sentences have approximately 75% power to detect differences of 1 BLEU point" (arxiv.org/abs/2010.06595) | 정확 |
| 29 | Miller [52] | DROP 군집 SE 약 3.05배, 3%p에 약 969문항, 최소 1,000문항 권고 | 표 4 DROP 1.34/0.44=3.05; n≈969(σ²_A=σ²_B=0, ω²=1/9 가정); "new evals should contain at least 1,000 questions" (arxiv.org/html/2411.00640) | 정확 / 4장 마지막 문장은 가정 누락(M2-4) |
| 30 | tinyBenchmarks [53] | IRT로 고른 100문항, 평균 약 2% 오차, 특이 모델에서 덜 정확 | "within about 2% error on average"; 성능 저하는 "correctness-based anchor strategy … on specialized LLMs", IRT 기반은 약간만 영향 (arxiv.org/html/2402.14992) | 부정확(M6-4) |
| 31 | GSM1k [57] | 최대 8% 하락, 생성 확률 높을수록 하락 폭 큼 | "accuracy drops of up to 8%"; "positive relationship (Spearman's r^2 = 0.36)" (arxiv.org/abs/2405.00332, v4) | 정확(강도 명시 필요, M6-8) |
| 32 | Recht [60] | ImageNet 정확도 11–14% 하락 | "11% - 14% on ImageNet" (arxiv.org/abs/1902.10811) | 정확 |
| 33 | Zheng [61] | GPT-4 판정 사람 일치율 80% 초과 | "achieving over 80% agreement, the same level of agreement between humans" (arxiv.org/abs/2306.05685) | 정확 |
| 34 | Thakur [38] | 가장 큰 판정 모델도 최대 5점, 일치율 높은 모델도 10–20점 | 정렬도 최고(GPT-4 Turbo, Llama-3 70B) 판정 모델이 "up to 5 points"; "high percent agreement can still give scores that differ 10-20 points"; TriviaQA 400문항 (arxiv.org/html/2406.12624) | 부정확(주체·조건, M6-2) |
| 35 | Thomas [30] | LLM 판정이 제3자 작업자보다 정확, 프롬프트에 따라 정확도 변동 | "models produce better labels than third-party workers"; "simple paraphrases" also make a difference (arxiv.org/abs/2309.10621) | 정확 |
| 36 | Shankar [74] | 사용자 연구에서 기준 표류 관찰 | 참여자 9명, "Grading outputs spurred changes or refinements in participants' criteria … criteria drift" (arxiv.org/html/2404.12272) | 정확(표본 9명 명시 권장) |
| 37 | Bowman–Dahl [11] | 타당성, 정확한 라벨, 충분한 검정력, 유해 시스템 억제 | 넷째 기준: "reveal plausibly harmful social biases … should not incentivize the creation of biased systems" (aclanthology.org/2021.naacl-main.385.pdf) | 부정확(넷째 기준 요약, M6-7) |
| 38 | Anthropic 문서 [2] | 실제 과제 분포 반영; 소수 정밀 채점보다 다수 자동 채점 | "mirror your real-world task distribution"; "More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals" | 정확 |
| 39 | OpenAI 문서 [1] | 사람이 제공한 정답 라벨, 평가 주도 개발 절차 | "correct_label … a 'ground truth' output … provided by a human"; "somewhat similar to behavior-driven development"; 플랫폼 2026-11-30 종료 예정 공지 | 대체로 정확(용어, m13; 폐지 공지 M5) |
| 40 | NeurIPS 2026 [71] | 데이터셋 투고에 한계·편향·의도된 용도 포함 요구 | "all dataset submissions must now include" RAI metadata(limitations, biases, intended use) in Croissant; Evaluations and Datasets Track | 정확 |
| 41 | Ragas [21] | 지식 그래프 구축 후 단일·다중 홉 질의 생성 | 문서→노드→관계 구축, single-hop/multi-hop 질의 정의 (docs.ragas.io) | 정확 |

**요약**: 41개 항목 대조(직접 원문 확인 40개, 확인 불가 1개). 정확 34(일부 표현 보완 권고 포함; 이 중 #22·#29는 수치는 정확하나 원고의 해석 문장이 과장), 부정확 6(#3 초록, #6, #15, #30, #34, #37), 확인 불가 1(#25). 수치 자체를 잘못 옮긴 사례는 없었다.
