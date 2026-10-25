---
type: Mini Review
title: LLM·RAG 애플리케이션 평가용 골든 데이터셋의 구축과 검증: 미니 리뷰
title_en: Building and Validating Golden Evaluation Datasets for LLM and RAG Applications: A Mini Review
authors: [저자명 추후 기입]
affiliation: [소속 추후 기입] · 교신 저자: [연락처 추후 기입]
---

## 초록

대형 언어모델(LLM)과 검색 증강 생성(RAG) 애플리케이션 개발팀은 회귀 검사, 모델 선택, 판정 모델 보정에 평가셋을 쓰고 이를 흔히 골든 데이터셋이라 부르지만, 무엇이 평가셋을 "골든"으로 만드는지에 대한 합의된 정의는 없다. 널리 쓰이는 공개 벤치마크에서도 전체 문항의 수 퍼센트, 일부 하위 영역에서는 분석 문항의 절반이 넘는 오류가 보고되었다. 본고는 주로 2015–2026년의 문헌을 종합하여 평가셋을 어떻게 구축하고, 어떤 측면에서 검증하며, 어떤 조건에서 골든이라 부를 수 있는지를 정리한다. 전문가 작성, 실사용 로그, LLM 합성, 적대적 수집의 네 구축 방식은 어느 것도 정확성, 현실성, 비용을 함께 만족하지 못하며, RAG, 에이전트, 안전성, 다국어 평가셋에는 고유한 요건이 더해진다. 검증은 구성 타당도, 라벨 신뢰도, 오류 감사, 통계적 충분성, 오염·재현성 통제의 다섯 측면으로 정리되며, 한 측면의 검토를 거친 평가셋에서 다른 측면의 결함이 발견된 사례가 여럿 있었다. 본고는 골든을 명시된 목적과 버전에 대해 일곱 조건의 충족 증거가 문서로 남은 상태로 정의하고 조건별 최소 판정 기준을 제시한다. 또한 감사된 핵심셋으로 대규모 보조셋의 자동 판정을 보정하는 2단 구성을 예측 기반 추론과 그 한계에 비추어 검토하고, 네 가지 쟁점을 논의한다.

**주제어**: 골든 데이터셋, 평가 데이터셋, 대형 언어모델, 검색 증강 생성, 라벨 품질, 벤치마크 타당도

## Abstract

Teams building large language model (LLM) and retrieval-augmented generation (RAG) applications use evaluation sets, often called golden datasets, for regression testing, model selection, and judge calibration, yet there is no agreed definition of what makes a set "golden." Widely used public benchmarks contain errors in a few percent of items overall and in more than half of the analyzed items in some subsets. This mini review synthesizes literature, mainly from 2015 to 2026, on how evaluation sets are built, how they are validated, and when they can be called golden. None of the four construction methods (expert authoring, curation of user logs, LLM-based synthesis, and adversarial collection) achieves correctness, realism, and low cost simultaneously, and RAG, agent, safety, and multilingual sets add their own requirements. Validation can be organized into five dimensions (construct validity, label reliability, error auditing, statistical adequacy, and control of contamination and reproducibility), and several sets that had passed review on one dimension were later found deficient on another. We propose that "golden" denote a state in which, for a stated purpose and version, documented evidence shows that seven conditions are met, and we give minimum criteria for each condition. We examine a two-tier design, in which an audited core calibrates automatic judgments on a larger auxiliary set, in light of prediction-powered inference and its limits, and we discuss four controversies: scale versus quality, a single answer versus perspectivism, human versus LLM labels, and static versus dynamic sets.

**Keywords**: golden dataset, evaluation dataset, large language models, retrieval-augmented generation, label quality, benchmark validity

## 1. 서론

LLM 애플리케이션 개발에서 평가셋은 프롬프트, 모델, 검색기를 바꿀 때마다 결과를 비교하는 기준이다. OpenAI 문서는 사람이 제공한 정답 라벨로 기대 동작을 먼저 명세하고 변경을 검사하는, 행동 주도 개발과 비슷한 절차를 제시하며[1], Anthropic 문서는 실제 과제 분포를 반영한 과제 특화 평가를 권고한다[2]. 실무에서는 이런 기준 집합을 골든 데이터셋(golden dataset, 이하 골든셋)이라 부르지만, 그 이름이 어떤 품질을 보장하는지는 합의되어 있지 않다.

정답 자체가 틀릴 수 있다는 점은 공개 벤치마크에서 거듭 확인되었다. 널리 쓰이는 평가셋 10종의 라벨 오류율은 평균 3.3% 이상으로 추정되었고, 수정된 ImageNet 라벨에서 원래 오표기 문항의 비율이 약 6%p 늘면 ResNet-18이 ResNet-50을 앞섰다[3]. MMLU에서는 문항·선지 불명확, 정답 없음, 복수 정답, 정답 오표기를 포함한 오류가 전체 문항의 6.49%, Virology 하위 영역에서는 분석 문항의 57%로 추정되었다[4]. GSM8K를 재검수하자 원래 평가셋에서 똑같이 45개를 틀린 두 모델이 각각 2개와 17개를 틀려, 라벨 잡음이 모델 간 차이를 가리고 있었음이 드러났다[5]. 공개 검수를 거치지 않는 사내 평가셋에는 같은 종류의 오류가 발견되지 않은 채 남을 수 있다.

기존 문헌은 이 문제를 애플리케이션 평가셋의 관점에서 다루지 않는다. LLM 평가 서베이는 평가 대상과 방법을 정리하였고[6], RAG 평가 서베이는 지표와 벤치마크를 분류하였으며[7], 오염 서베이는 학습 데이터 유출을 다루었다[8]. 벤치마크 품질 연구는 갖출 기준을 제시하거나[9] 공개 벤치마크의 모범 사례와 구성 타당도를 평가하였다[10,11]. 특정 애플리케이션의 평가셋을 만들고 검증하며 골든이라 부를 조건까지 묶은 리뷰는 본고의 검색 범위에서 확인되지 않았다.

본고는 (Q1) LLM·RAG 평가셋은 어떤 방식으로 구축되며 각 방식의 위험은 무엇인가, (Q2) 어떤 측면에서 검증되는가, (Q3) 어떤 조건을 갖추면 골든이라 부를 수 있는가를 다룬다. 2–4장이 각 질문에 답하고 5장은 쟁점과 과제를 논의한다. 평가셋(evaluation set)은 출력을 채점하는 문항과 정답의 집합, 벤치마크는 공개되어 여러 연구가 공유하는 평가셋, 시험 모음(test collection)은 정보검색에서 질의, 문서, 관련성 판정으로 이루어진 평가셋을 가리킨다.

문헌은 2026년 10월에 arXiv, ACL Anthology, 주요 학회 논문집, 개발사 문서에서 평가셋 구축, 라벨 품질, 오염, 통계적 검정력, 데이터셋 문서화를 주제어로 검색하고 인용을 앞뒤로 추적하여 모았다. 대상은 주로 2015–2026년 문헌이며, 골드 표준, 관련성 판정, 주석 일치도 개념의 기원은 2000–2010년 문헌으로 보충하였다. 구축 또는 검증 절차를 구체적으로 기술하거나 정량 보고한 문헌을 우선하였고, 개발사 문서와 블로그는 회색 문헌으로 구분하여 실무 관행과 사건 기록의 근거로만 썼다. 중복 포함 약 120건의 출처 기록을 검토하였으며, 검색 주제와 원문 대조 기록은 보충 자료로 공개한다. 본고는 체계적 문헌고찰이 아닌 서술형 미니 리뷰이다.

## 2. 구축: 네 가지 출처와 애플리케이션별 요건

평가셋의 문항과 정답은 전문가 작성, 실사용 로그, LLM 합성, 적대적 수집 중 하나 또는 그 조합에서 나온다. 표 1은 각 방식과 애플리케이션별 요건의 장점, 위험, 보완책을 비교하며, 이 장은 그 근거를 검토한다.

<!-- wide -->
**표 1.** 평가셋 구축 방식과 애플리케이션별 요건의 장점, 위험, 문헌에서 확인한 보완책

| 구축 방식·요건 | 장점 | 주요 위험 | 보완책(대표 사례) |
| --- | --- | --- | --- |
| 전문가 작성 | 정답 정확성, 고난도 문항 | 높은 비용, 전문가 간 불일치, 보상 구조가 낳는 오류 | 다단계 전문가 검토와 합의 기준 등급화(GPQA), 독립 작성자 2인 일치와 제3자 재풀이(SimpleQA) |
| 실사용 로그 | 배포 분포 반영 | 저가치 문항 다수, 선별에 따른 분포 변화, 개인정보 | 군집화 후 품질 채점과 선별 기준 기록(BenchBuilder), 사용자 동의(WildChat) |
| LLM 합성 | 저비용, 범위 확대 | 정답 오류, 생성·판정 모델의 자기 선호 | 왕복 일관성 필터와 사람 라벨 보정(ARES), 생성 후 다수 주석자 선별(MT-Bench-101) |
| 적대적 수집 | 높은 변별력, 쉬운 단서 회피 | 정답 모호성·오류 증가 | 작성자와 독립된 검증자 다수결(ANLI) |
| RAG | 검색·생성 오류의 분리 진단 | 판정 누락 문서, 근거 귀속 자동 판정의 중간–상당 수준 일치도(κ 0.53–0.70) | 판정 구멍 측정과 추가 판정(BEIR), 층화와 답 없는 질의(CRAG, MultiHop-RAG) |
| 에이전트·안전성·다국어 | 배포 행동과 언어·문화 맥락의 직접 측정 | 반복 실행 변동, 거부 오류의 비대칭 비용, 번역 결함 | 최종 상태 판정과 pass<sup>k</sup>(τ-bench), 안전·유해 대조 문항(XSTest), 원어 시험 기반 구축(KMMLU) |

### 2.1 전문가 작성

전문가가 문항과 정답을 작성하는 방식은 정확성을 우선하지만 비용이 크고 전문가 라벨에도 잡음이 남는다. GPQA는 박사급 전문가가 쓴 문항을 다른 전문가 두 명이 차례로 검토하고, 웹 검색을 허용한 비전문가 세 명이 풀게 하였다[12]. 전문가 검토를 통과하고 비전문가 정답률이 1/3 이하인 198문항이 최고 품질 부분집합이 되었으며, 참여 전문가에게는 시간당 평균 약 95달러가 지급되었다[12]. HealthBench에서 의사 262명이 작성한 채점 기준 48,562개에 대해 의사 간 일치도(macro F1)는 주제별 0.569–0.730이었다. 저자들은 이를 GPT-4.1 채점기(0.709)가 의사 수준에 이른다는 근거로 제시하였으나, 같은 수치는 전문가 라벨의 변이가 크다는 뜻이기도 하다[13]. 보상 구조도 오류를 낳는다. 최신 LLM이 틀린 문항만 받고 상금을 건 Humanity's Last Exam(HLE)은 약 13,000개 후보를 두 차례 전문가 검토에 넘겼지만, 출시 후 감사에서 공개셋의 전문가 불일치율이 15.4%로 추정되었다[14]. 반대로 SimpleQA는 두 작성자의 독립 답이 일치하는 문항만 남기고, 제3의 작성자가 1,000문항을 다시 풀게 하여 오류율을 약 3%로 추정하였다[15].

### 2.2 실사용 로그

실제 사용자 질의는 해당 서비스의 배포 분포를 반영하지만 평가 가치가 낮은 문항이 많다. Arena-Hard의 BenchBuilder는 Chatbot Arena 질의 20만 개를 4,000개 주제로 군집화하고, LLM으로 구체성, 복잡성 등 일곱 가지 품질 기준을 채점하여 500개를 선별하였다[16]. 선별은 변별력을 높이지만 원래 트래픽의 분포를 바꾸므로, 로그 기반 평가셋은 선별 기준을 함께 기록해야 해석할 수 있다. 로그 사용은 수집 동의와 비식별화를 전제로 하며, WildChat은 수집에 동의(opt-in)한 사용자의 대화를 공개하였다[17].

### 2.3 LLM 합성

LLM 합성은 적은 비용으로 규모와 범위를 확보하지만 정답의 정확성과 생성 모델의 편향을 따로 검증해야 한다. 학습용 지시문을 합성한 Self-Instruct에서 표본 200개 중 입력과 출력까지 모두 올바른 항목은 54%였고[18], 이는 평가셋 합성에도 같은 위험이 있음을 시사한다. RAG 평가 도구는 문서로 지식 그래프를 만든 뒤 단일·다중 홉 질의를 생성한다[19]. ARES는 생성 질의가 자신의 원문 단락을 1위로 검색하는 경우만 남기고, 사람 라벨 150–300개로 판정 모델을 보정하였다[20]. MT-Bench-101은 GPT-4가 생성한 대화 중 주석자 다섯 명 모두가 고품질로 판정한 것만 남겼다[21]. GPT-4와 Llama 2는 자신의 출력을 구별하였고, 미세조정으로 자기 인식 능력을 바꾸자 자기 선호의 강도가 선형으로 함께 변하였다[22]. LLM으로 만든 검색 시험 모음이 LLM 기반 검색기에 유리할 위험도 분석되었다[23].

### 2.4 적대적 수집

모델을 틀리게 하는 문항을 사람이 작성하는 적대적 수집은 난이도를 높이지만 정답의 모호성과 오류도 늘린다. 이 방식은 군중 작성 데이터가 가설 문장만으로 SNLI의 약 67%를 맞히게 하는 주석 흔적[24]에 대응하는 방법의 하나로 쓰였다. 그러나 ANLI에서 모델을 속인 것으로 보인 사례의 비율은 세 라운드 합계 기준 18.54%에서 사람 검증 후 9.52%로 줄어(1라운드 29.68%→18.33%), 그런 문항의 약 절반이 독립 검증자의 동의를 얻지 못하였다[25].

### 2.5 RAG 평가셋

RAG 평가셋은 질의, 근거 문서, 정답의 삼중 구조를 가지며, 관련성 라벨의 불완전성이 결과를 바꿀 수 있다. BEIR의 여러 데이터셋은 어휘 기반 검색 후보만 판정하여, TREC-COVID에서 밀집 검색기 상위 10개 결과의 최대 31.8%가 판정되지 않은 문서였다. 980건을 추가 판정하자 DPR의 nDCG@10이 0.332에서 0.445로 오르고 ANCE가 BM25를 앞서게 되었다[26]. LLM 관련성 판정은 비용을 낮추지만 프롬프트를 바꾸어 표현하는 것만으로 정확도가 달라졌다[27]. 근거 귀속을 NLI 모델로 자동 판정한 ALCE의 사람 일치도는 인용 재현율 κ 0.698, 인용 정밀도 0.525였다[28]. 질의 범위는 층화와 답할 수 없는 질의로 설계할 수 있다. CRAG는 4,409개 질의를 영역, 유형, 개체 인기도, 시간 변동성으로 층화하여 인기도가 낮고 변동이 큰 층의 낮은 정확도를 드러냈고[29], MultiHop-RAG는 답할 수 없는 질의 301개로 응답 거부를 평가하였다[30]. 능력×검사 유형 행렬로 문항을 계획하는 CheckList[31]도 같은 원리를 행동 검사에 적용한 예이다.

### 2.6 에이전트, 안전성, 다국어 평가셋

애플리케이션 유형에 따라 정답의 정의와 검증 대상이 달라진다. τ-bench는 대화 후 데이터베이스 상태를 기대 상태와 비교하여 채점하고, k번의 독립 시행이 모두 성공할 확률인 pass<sup>k</sup>를 정의하였다. GPT-4o의 소매 영역 성공률은 pass<sup>1</sup> 약 61%에서 pass<sup>8</sup> 약 25%로 떨어졌다[32]. 에이전트 골든셋의 정답은 최종 상태이고 반복 실행의 일관성도 측정 대상이다. 안전성 평가셋에서는 거부해야 할 문항과 거부하면 안 되는 문항의 비용이 다르다. HarmBench는 유해 행동 510개를 검증·평가 분할로 나누고 공격 성공 판정기를 사람 라벨과 대조하였으며(평균 일치율 93.19%)[33], XSTest는 응해야 할 안전한 프롬프트 250개와 대조용 위험 프롬프트 200개를 손으로 작성하였다[34]. OR-Bench는 LLM 세 개의 다수결로 과잉 거부 문항 8만 개를 라벨링하였는데, 이 앙상블의 정확도(93.0%)는 사람 전문가(94.0%)에 근접하였다[35]. 다국어 평가셋에서는 번역이 오류의 원천이 된다. KMMLU는 번역 대신 한국 원어 시험에서 35,030문항을 구축하고 공개 후 커뮤니티 보고로 741개 문항을 수정하였다[36]. Global-MMLU는 MMLU 문항의 28%가 문화적 지식을 요구함을 보였고, 41개 비영어 언어 중 14개만 전문 번역 후 교정을 거쳤다[37].

네 구축 방식의 위험은 성격이 다르다. 전문가 작성과 적대적 수집은 정확성이나 변별력을 얻는 대신 비용과 모호성을 지고, 로그와 합성은 현실성이나 규모를 얻는 대신 정답 검증을 뒤로 미룬다. 애플리케이션별 요건은 여기에 정답의 형식과 채점 단위를 바꾼다. 따라서 구축 출처만으로는 품질을 판단할 수 없으며, 어떤 평가셋이든 3장의 검증을 거쳐야 한다.

## 3. 검증: 다섯 측면

본고는 평가셋 검증을 구성 타당도, 라벨 신뢰도, 오류 감사, 통계적 충분성, 오염·재현성 통제의 다섯 측면으로 정리한다. 이들은 위계가 아니라 병렬적인 점검 대상이며, 측정 대상을 정하는 구성 타당도만 논리적으로 먼저 온다. 측면을 나누어 점검해야 하는 이유는 한 측면의 검토를 거친 평가셋에서 다른 측면의 결함이 발견된 사례가 여럿 있기 때문이다. 두 차례 전문가 검토를 거친 HLE의 화학·생물 문항은 외부 감사에서 29±3.7%가 동료 심사 문헌과 직접 충돌하는 답을 가진 것으로 추정되었고[38], HLE 팀의 후속 검토도 해당 부분집합의 약 18%를 문제 문항으로 판정하였다[14]. 전문 개발자가 선별한 SWE-bench Verified는 2026년 감사에서 o3가 일관되게 풀지 못한 138문항(27.6%) 중 최소 59.4%가 올바른 해법을 거부하는 결함 시험을 가진 것으로 드러났다. 같은 감사는 최신 모델이 정답 패치를 그대로 재현하는 오염도 보고하였고, OpenAI는 이 벤치마크를 평가에서 제외하였다[39].

### 3.1 구성 타당도

라벨이 정확하고 표본이 충분해도 평가셋이 의도한 능력을 측정하지 않으면 골든이 아니다. LLM 벤치마크 445개를 검토한 연구에서 측정 대상을 정의한 벤치마크는 78.2%였으나 그 정의의 47.8%는 합의되지 않은 개념이었다[11]. BetterBench는 설계부터 폐기까지 46개 모범 사례를 제시하였다[10]. 애플리케이션 평가셋에서 측정 대상은 배포될 과제 자체이므로 과제 정의서와 층별 문항 구성이 이 측면의 증거가 된다.

### 3.2 라벨 신뢰도

주석자 간 일치도는 라벨이 개인의 판단을 넘어 재현되는지를 측정하며, 기준값과 함께 불일치 문항의 성격을 보고해야 해석할 수 있다. Krippendorff는 α 0.800 이상을 요구하고, 잠정적 결론에는 0.667 이상을 하한으로 제시하였다[40]. Artstein과 Poesio는 단일 기준값이 모든 목적에 맞는지 의문을 제기하고, 범주 분포가 치우치면 관측 일치율이 0.96이어도 우연 보정 계수 K가 0.65에 그치는 예를 보였다[41]. 자연어 추론의 불일치는 주석자를 늘리거나 맥락을 바꾸어도 남았고[42], 이런 변이를 제거할 잡음이 아니라 평가가 반영할 신호로 보아야 한다는 주장도 있다[43–45].

### 3.3 오류 감사

일치도가 높아도 모두가 같은 오류를 범할 수 있으므로 정답 자체를 감사하고 그 결과를 오류율의 하한으로 해석해야 한다. 플래티넘 벤치마크 연구는 15개 벤치마크의 부분집합에서 최신 LLM 중 하나라도 틀린 문항을 사람이 재검토하였고[46], GSM8K 전체에서는 219문항을 검토하여 110문항을 제거하고 10문항의 정답을 고쳤다[5]. 저자들은 모든 모델이 틀린 정답에 동의하는 문항은 이 절차로 찾을 수 없으므로 찾은 오류 수가 하한이라고 밝혔다[46]. 문항 반응 이론(IRT)에서 변별도가 음수인 문항은 주석 오류를 시사하였고[47], 문항 통계와 LLM 1차 선별을 결합한 연구는 벤치마크 9종에서 최대 84%의 정밀도로 문제 문항을 찾았다[48]. 다만 주석 오류 탐지 방법 18종을 비교한 연구는 어려운 데이터셋에서 성능 한계가 아직 멀다고 보고하였다[49]. 코드 평가에서는 판정 기준인 시험 코드도 감사 대상이다. HumanEval의 시험을 80배로 늘리자 pass@k가 최대 19.3–28.9% 떨어졌다[50]. SWE-bench Verified는 전문 개발자 93명이 표본 1,699개 중 부적격 항목(68.3%)을 걸러 낸 뒤 500개를 선정하였으나[51], 앞의 2026년 감사는 이 선별이 결함을 다 거르지 못했음을 보였다. 모델 불일치 기반 감사는 모든 모델이 공유하는 오류를 놓치므로 무작위 표본 감사와 함께 써야 한다.

### 3.4 통계적 충분성

평가셋의 크기는 구분하려는 성능 차이에 맞추어 정해야 한다. NLP 비교 실험의 상당수는 검정력이 부족하였고, 문장 2,000개의 기계번역 평가셋도 BLEU 1점 차이를 약 75%의 검정력으로만 탐지하였다[52]. Miller는 쌍체 비교와 함께, 같은 문서에서 나온 문항처럼 묶인 문항에는 군집 표준오차를 쓰도록 권고하였다. DROP에서 군집 표준오차는 단순 표준오차의 약 3.05배였다. 쌍체 차이의 문항 간 분산을 1/9, 반복 표집 분산을 0으로 둔 예시에서 3%p 차이를 유의수준 0.05, 검정력 80%로 탐지하려면 약 969문항이 필요하였고, 저자는 새 평가셋에 최소 1,000문항을 권고하였다[53]. IRT로 고른 과제별 100문항은 전체 점수를 평균 약 2% 오차로 추정하였는데, 정답 패턴 기반 앵커는 전문화된 모델에서 추정이 나빠진 반면 IRT 기반 앵커는 약간만 영향을 받았다[54]. 이런 소규모 부분집합은 상시 모니터링에는 쓸 수 있으나 작은 차이의 판정 근거로는 부족하다. 체크포인트 간 잡음 대비 모델 간 점수 분산(신호)의 비가 높은 벤치마크일수록 소규모 실험의 의사결정이 정확하였다[55]. 그러나 벤치마크 445개 중 불확실성 추정이나 통계 검정을 쓴 것은 16.0%에 그쳐[11], 이 측면은 공개 벤치마크에서도 자주 생략된다.

### 3.5 오염·재현성 통제

평가 문항이 학습 데이터에 들어가면 점수가 부풀고 잘못된 결론이 출판될 수 있다[8]. Oren 등은 문항 순서가 교환 가능한 벤치마크에서 원래 순서의 우도가 섞은 순서보다 유의하게 높은지를 검정하여, 학습 데이터 없이 오염을 탐지할 수 있음을 보였다[56]. BIG-bench는 학습 데이터에서 걸러 낼 수 있도록 과제 파일에 카나리아 문자열을 넣었다[57]. GSM8K와 같은 분포로 새로 만든 GSM1k에서는 정확도가 최대 8% 떨어진 모델이 있었고, GSM8K 문항의 생성 확률과 하락 폭 사이에 중간 정도의 양의 관계(Spearman r²=0.36)가 있었다[58]. LiveBench는 문항을 매월 갱신하고 LiveCodeBench는 공개 시점을 기록하여 학습 시점 이후 문항만 평가할 수 있게 하였다[59,60]. 오염이 없어도 점수가 재현되지 않을 수 있다. SWE-bench Verified 500문항 중 16문항은 다른 기관의 실행 환경에서 안정적으로 실행되지 않아 제외되었고[61], 프롬프트와 채점 구현의 차이도 점수를 바꾸므로 정확한 프롬프트와 평가 코드의 공개가 권고되었다[62]. 본고는 문헌이 권고한 비공개 보존 분할과 공개 시점 기록[11,59]에 더해 실행 환경과 평가 코드의 고정을 이 측면의 점검 항목으로 제안한다.

## 4. 무엇을 골든이라 부를 수 있는가

### 4.1 개념의 변천과 정의

정보검색의 시험 모음 전통에서 "골드 표준"은 절대적 정답을 뜻하지 않았다. TREC 계열 시험 모음에서는 평가자마다 관련성 판정이 크게 달랐지만 시스템 순위는 판정 집합을 바꾸어도 높은 상관을 유지하였고, 이 순위 안정성이 시험 모음을 실험 도구로 쓰는 근거가 되었다[63]. 이후 CALBC는 여러 자동 태거의 출력을 합의로 통합한 코퍼스를 은 표준(silver standard)이라 불렀고[64], Vendrow 등은 라벨 오류와 모호성을 최소화하도록 재검수한 벤치마크를 플래티넘이라 부를 것을 제안하였다[46]. Aroyo와 Welty는 "단일 정답", "한 번 만들면 영원히 유효하다" 등 사람 주석의 일곱 가지 신화를 비판하였다[44]. 본고는 이 흐름에 따라 골든을 평가셋의 고정된 속성이 아니라 목적과 시점에 따라 달라지는 상태로 본다.

본고는 골든셋을 **명시된 평가 목적과 버전에 대해 표 2의 일곱 조건을 충족한다는 증거가 문서로 남은 평가셋**으로 정의할 것을 제안한다. 조건 C1–C5는 3장의 다섯 측면에 차례로 대응하고, C6과 C7은 그 증거를 남기고 갱신하는 절차이다. 2장의 구축 방식은 정의의 조건이 아니라 C1과 C3에서 점검할 위험의 출처이다. 표 2의 마지막 열이 보이듯 조건 대부분은 Bowman과 Dahl의 네 기준(타당성, 일관된 라벨, 충분한 검정력, 사회적 편향을 드러내고 편향된 시스템의 유인을 주지 않을 것)[9], BetterBench[10], Bean 등의 권고[11]와 겹친다. 본고의 정의가 더한 것은 세 가지이다. 판정 단위를 목적과 버전으로 한정하였고, 오염·재현성(C5)과 채점 기준의 동시 버전 관리(C7)를 명시하였으며, 조건마다 충족 여부를 가를 최소 판정 기준을 두었다. 최소 판정 기준은 문헌의 기준값이 있으면 그것을 쓰고, 없으면 무엇을 보고해야 하는지를 정한 본고의 제안이다.

<!-- wide -->
**표 2.** 골든셋의 일곱 조건: 운영 점검, 최소 판정 기준, 문헌 근거, 기존 기준과의 대응

| 조건 | 운영 점검과 남길 증거 | 최소 판정 기준(본고 제안) | 문헌 근거 | 기존 기준 대응 |
| --- | --- | --- | --- | --- |
| C1 구성 타당도 | 과제 정의서, 배포 과제·위험 영역별 층과 층별 문항 수 | 정의서가 있고, 결론을 내릴 층마다 신뢰구간을 보고할 수 있는 문항 수 | 정의한 벤치마크의 47.8%가 합의되지 않은 개념[11]; 층별 성능 차이[29] | BD 1·4; BB 설계; Bean 1–4·8 |
| C2 라벨 신뢰도 | 다중 주석 표본, 우연 보정 일치도, 중재 기록, 비집계 라벨 | α≥0.800, 잠정 결론은 α≥0.667. 미달 문항은 분포형으로 분류하거나 제외 | 기준값[40]; 단일 기준값의 한계[41] | BD 2 |
| C3 오류 감사 | 모델 불일치 재검토와 무작위 표본 감사, 수정·제거 목록 | 무작위 표본으로 추정한 오류율의 95% 신뢰구간 상한이 탐지할 차이보다 작음 | 평가셋 10종 평균 오류율 ≥3.3%[3]; 감사 결과는 하한[46] | BD 2; Bean 7 |
| C4 통계적 충분성 | 최소 탐지 차이, 검정력 계산, 군집·쌍체 신뢰구간 | 목표 차이를 검정력 80%로 탐지하는 문항 수 | 예시 가정에서 3%p 탐지에 약 1,000문항[53] | BD 3; BB 구현; Bean 6 |
| C5 오염·재현성 통제 | 비공개 분할, 공개 시점, 카나리아, 오염 검정, 실행 환경·코드 고정 | 비공개 분할 또는 학습 시점 이후 문항이 있고, 재실행 점수가 신뢰구간 안에 듦 | GSM1k에서 최대 8% 하락[58]; 순서 검정[56] | Bean 5 |
| C6 문서화 | 구축 출처, 선별 기준, 주석자, 라이선스, 한계 | 데이터시트의 필수 항목과 기계 판독 메타데이터 | 데이터시트·데이터 카드[65,66]; Croissant-RAI[67] | BB 문서화 |
| C7 유지·버전 | 버전 식별자, 정오표, 재감사 주기, 채점 기준 동시 버전, 폐기 기준 | 버전마다 C1–C6 증거를 다시 기록 | 한 번 만들면 영원히 유효하다는 신화[44]; 기준 표류[68] | BB 유지·폐기 |

주: BD는 Bowman과 Dahl의 기준 번호[9], BB는 BetterBench의 수명 주기 단계[10], Bean은 Bean 등의 권고 번호[11]이다.

문서화 항목은 Datasheets와 Data Cards가 제시하였고[65,66], Croissant의 책임 있는 AI 확장은 기계 판독 형식을 제공하며[67], NeurIPS 2026 데이터셋 투고는 한계, 편향, 의도된 용도를 이 형식에 담도록 요구한다[69]. 버전 관리는 데이터셋 저장소의 버전과 데이터 카드 기능으로 구현할 수 있고[70], 폐기 절차는 데이터셋 폐기 틀을 참고할 수 있다[71]. 채점 기준도 유지 대상이다. 참여자 9명의 사용자 연구에서 출력을 채점하며 채점 기준을 바꾸는 기준 표류(criteria drift)가 관찰되었다[68].

정의를 SimpleQA에 적용하면 점검표의 쓰임이 드러난다[15]. 단답형 사실 질의라는 측정 대상이 명시되어 C1의 정의 요건을 충족하고, 독립 작성자 2인의 일치(C2)와 제3자 재풀이에 의한 약 3%의 오류율 추정(C3)이 증거로 남아 있다. 4,326문항은 정답률 50% 근처에서 표준오차가 약 0.76%p로 수 퍼센트포인트 차이의 비교에 충분하다(C4, 본고 계산). 반면 비공개 분할, 버전별 정오표, 재감사 주기(C5, C7)는 논문에서 확인되지 않는다. 따라서 SimpleQA는 단답형 사실성 비교라는 목적에 대해 C1–C4는 충족하고 C5–C7은 확인할 수 없는 평가셋으로 판정된다.

### 4.2 2단 구성과 핵심셋의 규모

본고는 정의의 적용 방안으로, 감사를 거친 골든 핵심셋이 합성·로그 기반 은 표준 보조셋의 자동 판정을 보정하고 보조셋이 회귀 탐지와 범위 확대를 맡는 2단 구성을 검토한다. 그 통계적 근거는 예측 기반 추론(prediction-powered inference, PPI)이다. PPI는 소규모 정답 라벨로 대규모 예측의 편향을 보정하여 유효한 신뢰구간을 얻는다[72]. 이를 모델 평가에 적용한 AutoEval은 GPT-4 실험에서 사람 라벨의 유효 표본 크기를 최대 50% 늘렸고[73], ARES도 같은 방식으로 판정 모델을 보정하였다[20]. 그러나 Dorner 등은 판정 모델이 평가 대상 모델보다 정확하지 않으면 어떤 편향 보정도 필요한 정답 라벨을 절반 넘게 줄이지 못함을 보였다[74]. 최신 모델을 비교할 때 보조셋은 핵심셋을 최대 두 배 정도 대신할 뿐이다.

핵심셋의 규모는 용도에 따라 다르다. 판정 모델 보정에는 ARES 수준의 150–300문항에서 출발할 수 있으나, 판정 모델을 승인하려면 일치율과 함께 점수 수준의 차이를 측정해야 한다. MT-Bench와 Chatbot Arena에서 GPT-4 판정의 사람 일치율은 80%를 넘었지만[75], TriviaQA 400문항 설정에서 정렬도가 가장 높은 판정 모델(GPT-4 Turbo, Llama-3 70B)도 사람 점수와 최대 5점, 일치율이 높은 다른 판정 모델은 10–20점까지 달랐다[76]. 판정 모델의 사람 일치도는 평가 속성과 주석자 전문성에 따라 크게 달랐고[77], 불균형한 라벨에서는 정밀도와 재현율을 따로 보아야 한다[78]. 모델 선택에 쓰려면 C4로 규모를 정한다. 같은 n문항에서 두 모델을 쌍체 비교할 때 문항별 점수 차의 분산은 σ<sub>A</sub><sup>2</sup>+σ<sub>B</sub><sup>2</sup>−2ρσ<sub>A</sub>σ<sub>B</sub>이고 필요한 문항 수는 대략 (z<sub>α/2</sub>+z<sub>β</sub>)<sup>2</sup>×(이 분산)/δ<sup>2</sup>이므로, 두 모델의 문항별 정오가 강하게 상관할수록 n은 줄어든다. Miller의 예시에서 쌍체 차이의 분산을 1/9 대신 1/36으로 두면 3%p 탐지에 필요한 문항은 약 969개에서 약 242개로 줄어든다(본고 계산). 따라서 1,000문항은 고정된 기준이 아니며, 핵심셋을 설계할 때는 예비 실행으로 이 분산을 추정해야 한다.

## 5. 논의

### 5.1 쟁점

첫째 쟁점은 규모와 품질이다. Anthropic 문서는 사람이 정밀 채점한 소수 문항보다 신호가 다소 약한 자동 채점 문항을 많이 두라고 권고하였고[2], PPI와 AutoEval은 자동 판정으로 사람 라벨의 효용을 높일 수 있음을 보였다[72,73]. 반면 벤치마크 연구는 철저히 검증되고 모호하지 않은 문항을 요구하였고[9,46], 최신 모델 평가에서 자동 판정이 정답 라벨을 절반 넘게 대신할 수 없다는 상한도 제시되었다[74]. 2단 구성은 두 입장을 결합하지만, 판정 모델이 평가 대상보다 약하고 비교할 차이가 작으면 성립하지 않으며 이때는 핵심셋을 키워야 한다.

둘째 쟁점은 단일 정답과 관점주의이다. 주관적 판단이 들어가는 평가에서는 다수결 라벨보다 라벨 분포를 보존하는 편이 타당하다는 주장이 있으나[42,43,45], 회귀 검사에는 실행마다 같은 판정을 내는 고정된 기준이 필요하다. 본고는 문항을 정답형과 분포형으로 나누어, 분포형 문항은 비집계 라벨을 보존하고 모델 응답에 동의한 주석자 비율로 채점하는 절충안을 제안한다. 분포형 문항이 많아 회귀의 합격 여부를 문항 단위로 정해야 하는 경우에는 이 절충이 판정을 모호하게 만든다.

셋째 쟁점은 사람 라벨의 LLM 대체이다. ChatGPT의 영점 주석 정확도는 군중 작업자보다 평균 약 25%p 높았고 비용은 약 30분의 1이었으며[79], Bing 검색 관련성 판정에서도 LLM이 제3자 작업자보다 정확하였다[27]. 그러나 LLM 판정 모델은 자기 선호를 보였고[22], LLM으로 만든 시험 모음의 검색기 편향 위험과[23] 정답 라벨 절감의 상한도 제시되었다[74]. 본고는 LLM 라벨을 사람 라벨로 보정된 은 표준으로 취급하고 핵심셋의 정답은 사람이 확정할 것을 제안한다. 다만 라벨 생성 모델이 평가 대상과 같은 계열일 때 이 보정이 자기 선호를 제거하는지는 확인되지 않았다.

넷째 쟁점은 정적 평가셋과 동적 평가셋이다. LiveBench, LiveCodeBench, HLE의 지속 개정 계획은 문항 갱신으로 오염과 포화를 늦춘다[14,59,60]. 반면 정적 평가셋은 시점이 다른 모델의 점수를 같은 척도로 비교하게 하며, 애플리케이션 회귀 검사는 이 비교 가능성에 의존한다. 본고는 고정된 스냅숏을 회귀 기준으로 두고 갱신 분할을 별도 버전으로 추가하여 두 점수를 함께 보고하는 방식을 제안한다. 갱신 주기가 짧아 스냅숏이 곧 오염되면 기준을 자주 바꾸어야 하는 부담이 남는다.

### 5.2 연구 공백과 향후 과제

네 가지 공백이 남아 있다. 첫째, 평가셋 오류가 실제 배포 결정을 얼마나 바꾸는지 정량화한 연구는 본고의 검색 범위에서 공개 벤치마크의 순위 역전과 차이 은폐 사례[3,5]를 넘지 못하였다. 사내 평가셋에 오류를 주입하여 모델 선택이 바뀌는 오류율을 측정하는 연구가 필요하다. 둘째, RAG 지식 베이스 문서가 갱신될 때 정답과 근거 라벨을 함께 갱신하는 절차는 확인하지 못하였다. 질의 수준의 시간 변동 층화[29]를 넘어 문서 버전과 정답 버전을 연결하는 방법이 설계되어야 한다. 셋째, 한국어에서는 원어 시험 기반 구축과 공개 후 오류 수정 사례가 있으나[36], 한국어 RAG·에이전트 평가셋에서 일치도 기준값과 필요 문항 수를 실증한 연구는 드물다. 넷째, 본고의 일곱 조건과 최소 판정 기준은 문헌 종합에서 도출한 제안이므로, 여러 평가셋에 적용하여 조건 충족과 평가 결론의 안정성 사이의 관계를 실증해야 한다.

### 5.3 본고의 한계

본고는 서술형 종합이므로 누락된 문헌이 있을 수 있다. 문헌 검색과 요약에는 LLM 에이전트를 활용하였고, 원문 접근이 막힌 일부 출처는 웹 아카이브 사본으로 확인하였다. 회색 문헌은 실무 관행과 사건 기록의 근거로만 썼으나 개정·폐기될 수 있으며, 실제로 본고가 인용한 OpenAI Evals 문서는 2026년 11월 30일 플랫폼 종료를 공지하고 있다[1].

## 6. 결론

본고는 세 질문에 다음과 같이 답하였다. 첫째, 전문가 작성, 실사용 로그, LLM 합성, 적대적 수집은 성격이 다른 위험을 지며 어느 방식도 정확성, 현실성, 비용을 함께 만족하지 못하였고, RAG, 에이전트, 안전성, 다국어 평가셋은 정답의 형식과 채점 단위에 요건을 더한다. 둘째, 다섯 검증 측면은 따로 점검해야 하였다. 한 측면의 검토를 거친 평가셋에서 다른 측면의 결함이 발견된 사례가 여럿 있었고, 통계적 충분성은 공개 벤치마크에서도 드물게 점검되었다. 셋째, 골든이라는 이름은 평가셋을 만든 방식이 아니라 명시된 목적과 버전에 대한 검증 증거에 붙어야 한다. 본고의 일곱 조건과 최소 판정 기준은 평가셋 감사의 점검표로, 2단 구성은 설계 지침으로 쓸 수 있다. 다만 판정 모델이 평가 대상보다 약하면 보조셋의 이득은 정답 라벨 절반 이하의 절감에 그치고, 작은 차이를 판정하려면 검정력에 맞는 핵심셋이 필요하다. 제안의 유효성은 한국어 등 영어 이외의 평가셋과 실제 배포 결정에서 검증되어야 한다.

## 저자 기여

[추후 기입]

## 연구비

[추후 기입]

## 이해상충

[추후 기입]

## 데이터 가용성

본고는 새로운 데이터를 생성하지 않았다. 검색 주제, 출처별 확인 기록, 원문 대조 결과, 퇴고와 심사 기록은 보충 자료로 제공한다.

## 생성형 AI 사용 고지

저자는 문헌 검색, 출처 확인, 초안 작성과 퇴고에 Anthropic Claude(Claude Code, claude-opus-5-5)를 사용하였다. 본문의 수치는 Claude 에이전트가 인용 문헌의 원문, 초록 또는 웹 아카이브 사본과 대조하였고 저자가 그 기록을 검토하였다. 최종 내용의 책임은 저자에게 있다.

## 참고문헌

1. OpenAI. Evals [Internet]. OpenAI API documentation; 2026 [cited 2026 Oct 25; platform deprecation announced for 2026 Nov 30]. Available from: https://developers.openai.com/api/docs/guides/evals
2. Anthropic. Create strong empirical evaluations [Internet]. Claude documentation; 2026 [cited 2026 Oct 25]. Available from: https://platform.claude.com/docs/en/docs/test-and-evaluate/develop-tests
3. Northcutt CG, Athalye A, Mueller J. Pervasive label errors in test sets destabilize machine learning benchmarks. In: Proc NeurIPS Datasets and Benchmarks Track; 2021. arXiv:2103.14749.
4. Gema AP, Leang JOJ, Hong G, Devoto A, Mancino ACM, Saxena R, et al. Are we done with MMLU? In: Proc NAACL; 2025. p. 5069–5096. doi:10.18653/v1/2025.naacl-long.262.
5. Vendrow E, Vendrow J, Madry A, Beery S. GSM8K-Platinum: revealing performance gaps in frontier LLMs [Internet]. Gradient Science; 2025 Mar 6 [cited 2026 Oct 25]. Available from: https://gradientscience.org/gsm8k-platinum/
6. Chang Y, Wang X, Wang J, Wu Y, Yang L, Zhu K, et al. A survey on evaluation of large language models. ACM Trans Intell Syst Technol. 2024;15(3):1–45. doi:10.1145/3641289.
7. Yu H, Gan A, Zhang K, Tong S, Liu Q, Liu Z. Evaluation of retrieval-augmented generation: a survey. arXiv:2405.07437. 2024.
8. Xu C, Guan S, Greene D, Kechadi MT. Benchmark data contamination of large language models: a survey. arXiv:2406.04244. 2024.
9. Bowman SR, Dahl G. What will it take to fix benchmarking in natural language understanding? In: Proc NAACL; 2021. p. 4843–4855. doi:10.18653/v1/2021.naacl-main.385.
10. Reuel A, Hardy A, Smith C, Lamparth M, Hardy M, Kochenderfer MJ. BetterBench: assessing AI benchmarks, uncovering issues, and establishing best practices. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2411.12990.
11. Bean AM, Kearns RO, Romanou A, Hafner FS, Mayne H, Batzner J, et al. Measuring what matters: construct validity in large language model benchmarks. In: Proc NeurIPS Datasets and Benchmarks Track; 2025. arXiv:2511.04703.
12. Rein D, Hou BL, Stickland AC, Petty J, Pang RY, Dirani J, et al. GPQA: a graduate-level Google-proof Q&A benchmark. In: Proc COLM; 2024. arXiv:2311.12022.
13. Arora RK, Wei J, Hicks RS, Bowman P, Quiñonero-Candela J, Tsimpourlas F, et al. HealthBench: evaluating large language models towards improved human health. arXiv:2505.08775. 2025.
14. Phan L, Gatti A, Li N, Khoja A, Kim R, Ren R, et al. A benchmark of expert-level academic questions to assess AI capabilities. Nature. 2026;649(8099):1139–1146. doi:10.1038/s41586–41025-09962-4.
15. Wei J, Karina N, Chung HW, Jiao YJ, Papay S, Glaese A, et al. Measuring short-form factuality in large language models. arXiv:2411.04368. 2024.
16. Li T, Chiang WL, Frick E, Dunlap L, Wu T, Zhu B, et al. From crowdsourced data to high-quality benchmarks: Arena-Hard and BenchBuilder pipeline. In: Proc ICML; 2025. arXiv:2406.11939.
17. Zhao W, Ren X, Hessel J, Cardie C, Choi Y, Deng Y. WildChat: 1M ChatGPT interaction logs in the wild. In: Proc ICLR; 2024. arXiv:2405.01470.
18. Wang Y, Kordi Y, Mishra S, Liu A, Smith NA, Khashabi D, et al. Self-Instruct: aligning language models with self-generated instructions. In: Proc ACL; 2023. p. 13484–13508. doi:10.18653/v1/2023.acl-long.754.
19. Ragas. Testset generation for RAG [Internet]. Ragas documentation; 2026 [cited 2026 Oct 25]. Available from: https://docs.ragas.io/en/stable/concepts/test_data_generation/rag/
20. Saad-Falcon J, Khattab O, Potts C, Zaharia M. ARES: an automated evaluation framework for retrieval-augmented generation systems. In: Proc NAACL; 2024. p. 338–354. doi:10.18653/v1/2024.naacl-long.20.
21. Bai G, Liu J, Bu X, He Y, Liu J, Zhou Z, et al. MT-Bench-101: a fine-grained benchmark for evaluating large language models in multi-turn dialogues. In: Proc ACL; 2024. p. 7421–7454. doi:10.18653/v1/2024.acl-long.401.
22. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. In: Proc NeurIPS; 2024. arXiv:2404.13076.
23. Rahmani HA, Craswell N, Yilmaz E, Mitra B, Campos D. Synthetic test collections for retrieval evaluation. In: Proc SIGIR; 2024. p. 2647–2651. doi:10.1145/3626772.3657942.
24. Gururangan S, Swayamdipta S, Levy O, Schwartz R, Bowman S, Smith NA. Annotation artifacts in natural language inference data. In: Proc NAACL; 2018. p. 107–112. doi:10.18653/v1/N18-2017.
25. Nie Y, Williams A, Dinan E, Bansal M, Weston J, Kiela D. Adversarial NLI: a new benchmark for natural language understanding. In: Proc ACL; 2020. p. 4885–4901. doi:10.18653/v1/2020.acl-main.441.
26. Thakur N, Reimers N, Rücklé A, Srivastava A, Gurevych I. BEIR: a heterogenous benchmark for zero-shot evaluation of information retrieval models. In: Proc NeurIPS Datasets and Benchmarks Track; 2021. arXiv:2104.08663.
27. Thomas P, Spielman S, Craswell N, Mitra B. Large language models can accurately predict searcher preferences. In: Proc SIGIR; 2024. p. 1930–1940. doi:10.1145/3626772.3657707.
28. Gao T, Yen H, Yu J, Chen D. Enabling large language models to generate text with citations. In: Proc EMNLP; 2023. p. 6465–6488. doi:10.18653/v1/2023.emnlp-main.398.
29. Yang X, Sun K, Xin H, Sun Y, Bhalla N, Chen X, et al. CRAG – comprehensive RAG benchmark. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2406.04744.
30. Tang Y, Yang Y. MultiHop-RAG: benchmarking retrieval-augmented generation for multi-hop queries. In: Proc COLM; 2024. arXiv:2401.15391.
31. Ribeiro MT, Wu T, Guestrin C, Singh S. Beyond accuracy: behavioral testing of NLP models with CheckList. In: Proc ACL; 2020. p. 4902–4912. doi:10.18653/v1/2020.acl-main.442.
32. Yao S, Shinn N, Razavi P, Narasimhan K. τ-bench: a benchmark for tool-agent-user interaction in real-world domains. In: Proc ICLR; 2025. arXiv:2406.12045.
33. Mazeika M, Phan L, Yin X, Zou A, Wang Z, Mu N, et al. HarmBench: a standardized evaluation framework for automated red teaming and robust refusal. In: Proc ICML (PMLR 235); 2024. p. 35181–35224. arXiv:2402.04249.
34. Röttger P, Kirk H, Vidgen B, Attanasio G, Bianchi F, Hovy D. XSTest: a test suite for identifying exaggerated safety behaviours in large language models. In: Proc NAACL; 2024. p. 5377–5400. doi:10.18653/v1/2024.naacl-long.301.
35. Cui J, Chiang WL, Stoica I, Hsieh CJ. OR-Bench: an over-refusal benchmark for large language models. In: Proc ICML (PMLR 267); 2025. p. 11515–11542. arXiv:2405.20947.
36. Son G, Lee H, Kim S, Kim S, Muennighoff N, Choi T, et al. KMMLU: measuring massive multitask language understanding in Korean. In: Proc NAACL; 2025. p. 4076–4104. doi:10.18653/v1/2025.naacl-long.206.
37. Singh S, Romanou A, Fourrier C, Adelani DI, Ngui JG, Vila-Suero D, et al. Global MMLU: understanding and addressing cultural and linguistic biases in multilingual evaluation. In: Proc ACL; 2025. p. 18761–18799. doi:10.18653/v1/2025.acl-long.919.
38. Skarlinski M, Laurent J, Bou A, White A. About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong [Internet]. FutureHouse; 2025 Jul 23 [updated 2025 Sep 16; cited 2026 Oct 25]. Available from: https://www.futurehouse.org/research-announcements/hle-exam
39. OpenAI. Why SWE-bench Verified no longer measures frontier coding capabilities [Internet]. OpenAI; 2026 Feb 23 [cited 2026 Oct 25]. Available from: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
40. Krippendorff K. Reliability in content analysis: some common misconceptions and recommendations. Hum Commun Res. 2004;30(3):411–433. doi:10.1111/j.1468-2958.2004.tb00738.x.
41. Artstein R, Poesio M. Inter-coder agreement for computational linguistics. Comput Linguist. 2008;34(4):555–596. doi:10.1162/coli.07-034-R2.
42. Pavlick E, Kwiatkowski T. Inherent disagreements in human textual inferences. Trans Assoc Comput Linguist. 2019;7:677–694. doi:10.1162/tacl_a_00293.
43. Plank B. The "problem" of human label variation: on ground truth in data, modeling and evaluation. In: Proc EMNLP; 2022. p. 10671–10682. doi:10.18653/v1/2022.emnlp-main.731.
44. Aroyo L, Welty C. Truth is a lie: crowd truth and the seven myths of human annotation. AI Mag. 2015;36(1):15–24. doi:10.1609/aimag.v36i1.2564.
45. Cabitza F, Campagner A, Basile V. Toward a perspectivist turn in ground truthing for predictive computing. Proc AAAI Conf Artif Intell. 2023;37(6):6860–6868. doi:10.1609/aaai.v37i6.25840.
46. Vendrow J, Vendrow E, Beery S, Madry A. Do large language model benchmarks test reliability? arXiv:2502.03461. 2025.
47. Rodriguez P, Barrow J, Hoyle AM, Lalor JP, Jia R, Boyd-Graber J. Evaluation examples are not equally informative: how should that change NLP leaderboards? In: Proc ACL; 2021. p. 4486–4503. doi:10.18653/v1/2021.acl-long.346.
48. Truong S, Tu Y, Hardy M, Reuel A, Tang Z, Burapacheep J, et al. Fantastic bugs and where to find them in AI benchmarks. In: Proc NeurIPS Datasets and Benchmarks Track; 2025. arXiv:2511.16842.
49. Klie JC, Webber B, Gurevych I. Annotation error detection: analyzing the past and present for a more coherent future. Comput Linguist. 2023;49(1):157–198. doi:10.1162/coli_a_00464.
50. Liu J, Xia CS, Wang Y, Zhang L. Is your code generated by ChatGPT really correct? Rigorous evaluation of large language models for code generation. In: Proc NeurIPS; 2023. arXiv:2305.01210.
51. OpenAI. Introducing SWE-bench Verified [Internet]. OpenAI; 2024 Aug 13 [cited 2026 Oct 25]. Available from: https://openai.com/index/introducing-swe-bench-verified/
52. Card D, Henderson P, Khandelwal U, Jia R, Mahowald K, Jurafsky D. With little power comes great responsibility. In: Proc EMNLP; 2020. p. 9263–9274. doi:10.18653/v1/2020.emnlp-main.745.
53. Miller E. Adding error bars to evals: a statistical approach to language model evaluations. arXiv:2411.00640. 2024.
54. Maia Polo F, Weber L, Choshen L, Sun Y, Xu G, Yurochkin M. tinyBenchmarks: evaluating LLMs with fewer examples. In: Proc ICML (PMLR 235); 2024. p. 34303–34326. arXiv:2402.14992.
55. Heineman D, Hofmann V, Magnusson I, Gu Y, Smith NA, Hajishirzi H, et al. Signal and noise: a framework for reducing uncertainty in language model evaluation. In: Proc NeurIPS; 2025. arXiv:2508.13144.
56. Oren Y, Meister N, Chatterji N, Ladhak F, Hashimoto TB. Proving test set contamination in black-box language models. In: Proc ICLR; 2024. arXiv:2310.17623.
57. Srivastava A, Rastogi A, Rao A, Shoeb AAM, Abid A, Fisch A, et al. Beyond the imitation game: quantifying and extrapolating the capabilities of language models. Trans Mach Learn Res. 2023. arXiv:2206.04615.
58. Zhang H, Da J, Lee D, Robinson V, Wu C, Song W, et al. A careful examination of large language model performance on grade school arithmetic. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2405.00332.
59. White C, Dooley S, Roberts M, Pal A, Feuer B, Jain S, et al. LiveBench: a challenging, contamination-limited LLM benchmark. In: Proc ICLR; 2025. arXiv:2406.19314.
60. Jain N, Han K, Gu A, Li WD, Yan F, Zhang T, et al. LiveCodeBench: holistic and contamination free evaluation of large language models for code. In: Proc ICLR; 2025. arXiv:2403.07974.
61. Epoch AI. SWE-bench Verified [Internet]. Epoch AI Benchmarking Hub; n.d. [cited 2026 Oct 25]. Available from: https://epoch.ai/benchmarks/swe-bench-verified
62. Biderman S, Schoelkopf H, Sutawika L, Gao L, Tow J, Abbasi B, et al. Lessons from the trenches on reproducible evaluation of language models. arXiv:2405.14782. 2024.
63. Voorhees EM. Variations in relevance judgments and the measurement of retrieval effectiveness. Inf Process Manag. 2000;36(5):697–716. doi:10.1016/S0306–4573(00)00010-8.
64. Rebholz-Schuhmann D, Jimeno Yepes AJ, van Mulligen EM, Kang N, Kors J, Milward D, et al. CALBC silver standard corpus. J Bioinform Comput Biol. 2010;8(1):163–179. doi:10.1142/S0219720010004562.
65. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé III H, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86–92. doi:10.1145/3458723.
66. Pushkarna M, Zaldivar A, Kjartansson O. Data cards: purposeful and transparent dataset documentation for responsible AI. In: Proc ACM FAccT; 2022. p. 1776–1826. doi:10.1145/3531146.3533231.
67. Jain N, Akhtar M, Giner-Miguelez J, Shinde R, Vanschoren J, Vogler S, et al. A standardized machine-readable dataset documentation format for responsible AI. arXiv:2407.16883. 2024.
68. Shankar S, Zamfirescu-Pereira JD, Hartmann B, Parameswaran A, Arawjo I. Who validates the validators? Aligning LLM-assisted evaluation of LLM outputs with human preferences. In: Proc ACM UIST; 2024. p. 1–14. doi:10.1145/3654777.3676450.
69. NeurIPS. Responsible AI metadata requirements for the Evaluations and Datasets Track, NeurIPS 2026 [Internet]. NeurIPS blog; 2026 May 4 [cited 2026 Oct 25]. Available from: https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/
70. Lhoest Q, Villanova del Moral A, Jernite Y, Thakur A, von Platen P, Patil S, et al. Datasets: a community library for natural language processing. In: Proc EMNLP System Demonstrations; 2021. p. 175–184. doi:10.18653/v1/2021.emnlp-demo.21.
71. Luccioni AS, Corry F, Sridharan H, Ananny M, Schultz J, Crawford K. A framework for deprecating datasets: standardizing documentation, identification, and communication. In: Proc ACM FAccT; 2022. p. 199–212. doi:10.1145/3531146.3533086.
72. Angelopoulos AN, Bates S, Fannjiang C, Jordan MI, Zrnic T. Prediction-powered inference. Science. 2023;382(6671):669–674. doi:10.1126/science.adi6000.
73. Boyeau P, Angelopoulos AN, Li T, Yosef N, Malik J, Jordan MI. AutoEval done right: using synthetic data for model evaluation. In: Proc ICML (PMLR 267); 2025. p. 5276–5290. arXiv:2403.07008.
74. Dorner FE, Nastl VY, Hardt M. Limits to scalable evaluation at the frontier: LLM as judge won't beat twice the data. In: Proc ICLR; 2025. arXiv:2410.13341.
75. Zheng L, Chiang WL, Sheng Y, Zhuang S, Wu Z, Zhuang Y, et al. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In: Proc NeurIPS Datasets and Benchmarks Track; 2023. arXiv:2306.05685.
76. Thakur AS, Choudhary K, Ramayapally VS, Vaidyanathan S, Hupkes D. Judging the judges: evaluating alignment and vulnerabilities in LLMs-as-judges. In: Proc GEM² Workshop; 2025. p. 404–430. arXiv:2406.12624.
77. Bavaresco A, Bernardi R, Bertolazzi L, Elliott D, Fernández R, Gatt A, et al. LLMs instead of human judges? A large scale empirical study across 20 NLP evaluation tasks. In: Proc ACL (Short Papers); 2025. p. 238–255. doi:10.18653/v1/2025.acl-short.20.
78. Husain H. Your AI product needs evals [Internet]. 2024 Mar 29 [cited 2026 Oct 25]. Available from: https://hamel.dev/blog/posts/evals/
79. Gilardi F, Alizadeh M, Kubli M. ChatGPT outperforms crowd workers for text-annotation tasks. Proc Natl Acad Sci U S A. 2023;120(30):e2305016120. doi:10.1073/pnas.2305016120.
