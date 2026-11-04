---
type: Mini Review
title: LLM·RAG 애플리케이션 평가용 골든 데이터셋의 구축과 검증: 미니 리뷰
title_en: Building and Validating Golden Evaluation Datasets for LLM and RAG Applications: A Mini Review
authors: [저자명 추후 기입]
affiliation: [소속 추후 기입] · 교신 저자: [연락처 추후 기입]
---

## 초록

대형 언어모델(LLM)과 검색 증강 생성(RAG) 애플리케이션 개발팀은 회귀 검사, 모델 선택, 판정 모델 보정에 평가셋을 쓰고 이를 흔히 골든 데이터셋이라 부르지만, 무엇이 평가셋을 "골든"으로 만드는지에 대한 합의된 정의는 없다. 공개 벤치마크의 감사에서도 전체 문항의 수 퍼센트, 한 하위 영역에서는 절반이 넘는 오류가 보고되었다. 본고는 주로 2015–2026년 문헌을 종합하여 평가셋의 구축, 검증, 골든의 조건을 정리한다. 전문가 작성, 실사용 로그, LLM 합성, 적대적 수집의 네 구축 방식은 정확성, 현실성, 비용을 함께 만족하지 못하는 것으로 정리되며, RAG, 에이전트, 안전성, 다국어 평가셋에는 고유한 요건이 더해진다. 검증은 구성 타당도, 라벨 신뢰도, 오류 감사, 통계적 충분성, 오염·재현성 통제의 다섯 측면으로 정리되며, 한 측면의 검토를 거친 평가셋에서 다른 측면의 결함이 발견된 사례가 보고되었다. 본고는 골든을 명시된 목적과 버전에 대해 일곱 조건의 충족 증거가 문서로 남은 상태로 정의하고, 조건별 최소 판정 기준을 제시하여 공개 평가셋 하나에 적용한다. 또한 감사된 핵심셋으로 대규모 보조셋의 자동 판정을 보정하는 2단 구성을 예측 기반 추론과 그 한계에 비추어 검토하고, 규모와 품질, 단일 정답과 관점주의, LLM 라벨, 정적·동적 평가셋의 네 쟁점을 논의한다.

**주제어**: 골든 데이터셋, 평가 데이터셋, 대형 언어모델, 검색 증강 생성, 라벨 품질, 벤치마크 타당도

## Abstract

Teams building large language model (LLM) and retrieval-augmented generation (RAG) applications use evaluation sets, often called golden datasets, for regression testing, model selection, and judge calibration, yet there is no agreed definition of what makes a set "golden." Audits of widely used public benchmarks have reported errors in a few percent of all items and, in one subject area, in more than half of the analyzed items. This mini review synthesizes literature, mainly from 2015 to 2026, on how evaluation sets are built, how they are validated, and when they can be called golden. We argue that none of the four construction methods (expert authoring, curation of user logs, LLM-based synthesis, and adversarial collection) achieves correctness, realism, and low cost simultaneously, and RAG, agent, safety, and multilingual sets add their own requirements. Validation can be organized into five dimensions (construct validity, label reliability, error auditing, statistical adequacy, and control of contamination and reproducibility), and sets that had been checked on one dimension have been found deficient on another. We propose that "golden" denote a state in which, for a stated purpose and version, documented evidence shows that seven conditions are met, give minimum criteria for each condition, and apply them to one public set. We examine a two-tier design, in which an audited core set calibrates automatic judgments on a larger auxiliary set, in light of prediction-powered inference and its limits, and we discuss four controversies: scale versus quality, a single answer versus perspectivism, replacing human labels with LLM labels, and static versus dynamic sets.

**Keywords**: golden dataset, evaluation dataset, large language models, retrieval-augmented generation, label quality, benchmark validity

## 1. 서론

LLM 애플리케이션 개발에서 평가셋은 프롬프트, 모델, 검색기를 바꿀 때마다 결과를 비교하는 기준이다. OpenAI 문서는 사람이 제공한 정답 라벨로 기대 동작을 먼저 명세하고 변경을 검사하는, 행동 주도 개발과 비슷한 절차를 제시하며[1], Anthropic 문서는 실제 과제 분포를 반영한 과제 특화 평가를 권고한다[2]. 실무에서는 이런 기준 집합을 골든 데이터셋(golden dataset, 이하 골든셋)이라 부르지만, 그 이름이 어떤 품질을 보장하는지는 합의되어 있지 않다.

정답 자체가 틀릴 수 있다는 점은 공개 벤치마크에서 거듭 확인되었다. 널리 쓰이는 평가셋 10종의 라벨 오류율은 평균 3.3% 이상으로 추정되었고, 수정된 ImageNet 라벨에서 원래 오표기 문항의 비율이 약 6%p 늘면 ResNet-18이 ResNet-50을 앞섰다[3]. MMLU에서는 문항·선지 불명확, 정답 없음, 복수 정답, 정답 오표기를 포함한 오류가 전체 문항의 6.49%, Virology 하위 영역에서는 분석 문항의 57%로 추정되었다[4]. GSM8K를 재검수하자 원래 평가셋에서 똑같이 45개를 틀린 두 모델이 각각 2개와 17개를 틀려, 라벨 잡음이 모델 간 차이를 가리고 있었음이 드러났다[5]. 공개 검수가 없는 사내 평가셋에는 같은 오류가 발견되지 않은 채 남을 수 있다.

기존 서베이와 벤치마크 품질 연구는 이 문제를 주로 평가 방법 일반이나 공개 벤치마크의 관점에서 다루었다. LLM 평가[6], RAG 평가[7], 오염[8] 서베이는 각각 평가 방법, 지표와 벤치마크, 학습 데이터 유출을 정리하였다. 벤치마크 품질 연구는 갖출 기준을 제시하거나[9] 공개 벤치마크의 모범 사례와 구성 타당도를 평가하였다[10,11]. 특정 애플리케이션의 평가셋을 만들고 검증하며 골든이라 부를 조건까지 묶은 리뷰는 본고의 검색 범위에서 확인되지 않았다.

본고는 (Q1) LLM·RAG 평가셋은 어떤 방식으로 구축되며 각 방식의 위험은 무엇인가, (Q2) 어떤 측면에서 검증되는가, (Q3) 어떤 조건을 갖추면 골든이라 부를 수 있는가를 다룬다. 평가셋(evaluation set)은 출력을 채점하는 문항과 정답의 집합, 벤치마크는 공개되어 여러 연구가 공유하는 평가셋, 시험 모음(test collection)은 정보검색에서 질의, 문서, 관련성 판정으로 이루어진 평가셋을 가리킨다.

문헌은 2026년 10월에 arXiv, ACL Anthology, 주요 학회 논문집, 개발사 문서에서 평가셋 구축, 라벨 품질, 오염, 검정력, 문서화를 주제어로 검색하고 인용을 추적하여 모았다. 대상은 주로 2015–2026년 문헌이며 개념의 기원은 2000–2010년 문헌으로 보충하였다. 구축·검증 절차를 정량 보고한 문헌을 우선하였고, 개발사 문서와 블로그는 회색 문헌으로 구분하였다. 중복 포함 약 120건의 출처 기록을 검토하였으며 원문 대조 기록은 보충 자료로 공개한다. 본고는 체계적 문헌고찰이 아닌 서술형 미니 리뷰이다.

## 2. 구축: 네 가지 출처와 애플리케이션별 요건

평가셋의 문항과 정답은 네 출처 또는 그 조합에서 나오며, 표 1은 각 방식과 애플리케이션별 요건을 비교한다.

<!-- wide -->
**표 1.** 평가셋 구축 방식과 애플리케이션별 요건의 장점, 위험, 문헌에서 확인한 보완책

| 구축 방식·요건 | 장점 | 주요 위험 | 보완책(대표 사례) |
| --- | --- | --- | --- |
| 전문가 작성 | 정답 정확성, 고난도 문항 | 높은 비용, 전문가 간 불일치, 보상 구조가 낳는 오류 | 다단계 전문가 검토와 합의 기준 등급화(GPQA), 독립 작성자 2인 일치와 제3자 재풀이(SimpleQA) |
| 실사용 로그 | 배포 분포 반영 | 저가치 문항 다수, 선별에 따른 분포 변화, 개인정보 | 군집화 후 품질 채점과 선별 기준 기록(BenchBuilder), 수집 동의·비식별화 |
| LLM 합성 | 저비용, 범위 확대 | 정답 오류, 생성·판정 모델의 자기 선호 | 왕복 일관성 필터와 사람 라벨 보정(ARES), 생성 후 다수 주석자 선별(MT-Bench-101) |
| 적대적 수집 | 높은 변별력, 쉬운 단서 회피 | 정답 모호성·오류 | 작성자와 독립된 검증자 다수결(ANLI) |
| RAG | 검색·생성 오류의 분리 진단 | 판정 누락 문서, 근거 귀속 자동 판정의 제한된 일치도(인용 정밀도 κ 0.53, 재현율 0.70) | 판정 구멍 측정과 추가 판정(BEIR), 층화와 답 없는 질의(CRAG, MultiHop-RAG) |
| 에이전트·안전성·다국어 | 배포 행동과 언어·문화 맥락의 직접 측정 | 반복 실행 변동, 거부 오류의 비대칭 비용, 번역 품질·문화 편향 | 최종 상태 판정과 pass<sup>k</sup>(τ-bench), 안전·유해 대조 문항(XSTest), 원어 시험 기반 구축(KMMLU) |

### 2.1 전문가 작성

전문가가 문항과 정답을 작성하는 방식은 정확성을 우선하지만 비용이 크고 전문가 라벨에도 잡음이 남는다. GPQA는 박사급 전문가가 쓴 문항을 다른 전문가 두 명이 차례로 검토하고 웹 검색을 허용한 비전문가 세 명이 풀게 하여, 전문가 검토를 통과하고 비전문가 정답률이 1/3 이하인 198문항을 최고 품질 부분집합으로 분리하였으며, 참여 전문가에게 시간당 평균 약 95달러를 지급하였다[12]. HealthBench에서 의사 262명이 작성한 합의 기준의 의사 간 일치도(macro F1)는 7개 주제별로 0.569–0.730으로, GPT-4.1 판정 모델(0.709)이 의사 수준이라는 근거이자 전문가 라벨의 변이가 크다는 뜻이었다[13]. 보상 구조가 오류를 낳는다는 지적도 있다. 최신 LLM이 틀린 문항만 접수하고 상금을 내건 Humanity's Last Exam(HLE)은 두 차례 전문가 검토를 거쳤지만 출시 전 감사에서 공개셋의 전문가 불일치율이 15.4%로 추정되었고[14], 외부 감사자는 화학·생물 문항의 오류가 이 보상 구조에서 비롯되었다고 보았다(3.3절)[15]. SimpleQA는 상금 대신 고용된 작업자가 GPT-4가 틀리는 문항을 작성하게 하였고, 두 작성자의 독립 답이 일치하는 문항만 남기고 제3의 작성자가 1,000문항을 다시 풀게 하여 오류율을 약 3%로 추정하였다[16].

### 2.2 실사용 로그

실제 사용자 질의는 해당 서비스의 배포 분포를 반영하지만 평가 가치가 낮은 문항이 많고, 정답은 별도로 붙여야 한다. Arena-Hard의 BenchBuilder는 Chatbot Arena 질의 20만 개에서 중복과 다중 턴·비영어 질의를 걸러 내고 4,000개 주제로 군집화한 뒤, LLM으로 구체성, 복잡성 등 일곱 가지 품질 기준을 채점하여 500개를 선별하였다[17]. 선별은 원래 분포를 바꾸므로 선별 기준을 기록해야 하며, 로그 사용은 수집 동의를 전제로 한다.

### 2.3 LLM 합성

LLM 합성은 적은 비용으로 규모와 범위를 확보하지만 정답의 정확성과 생성 모델의 편향을 따로 검증해야 한다. 학습용 지시문을 합성한 Self-Instruct에서 표본 200개 중 입력과 출력까지 모두 올바른 항목은 54%였고[18], 이는 평가셋 합성에도 같은 위험이 있음을 시사한다. 생성 모델이 판정 모델을 겸하면 편향이 더해질 수 있는데, 판정 모델로 쓰인 GPT-4와 Llama 2는 자신의 출력을 구별하였고, 미세조정으로 자기 인식 능력을 바꾸자 자기 선호의 강도가 선형으로 함께 변하였다[19]. 보완 절차로, ARES는 생성 질의가 자신의 원문 단락을 1위로 검색하는 경우만 남긴 뒤 사람 라벨 150–300개로 판정 모델을 보정하였다[20]. MT-Bench-101은 GPT-4가 생성한 대화 중 주석자 다섯 명 모두가 고품질로 판정한 것만 남겼다[21].

### 2.4 적대적 수집

모델을 틀리게 하는 문항을 사람이 작성하는 적대적 수집은 난이도를 높이지만, 모델을 속인 것으로 보이는 문항에 정답이 모호하거나 틀린 문항이 많이 섞인다. 이 방식은 군중 작성 데이터의 주석 흔적(가설 문장만으로 SNLI의 약 67%를 맞힘)[22]에 대응하는 방법의 하나로 쓰였다. 그러나 ANLI에서 모델을 속인 것으로 보인 사례의 비율은 세 라운드 합계 기준 18.54%에서 사람 검증 후 9.52%로 줄어(1라운드 29.68%→18.33%), 그런 문항의 약 절반이 독립 검증자의 동의를 얻지 못하였다[23].

### 2.5 RAG 평가셋

RAG 평가셋은 질의, 근거 문서, 정답의 삼중 구조를 가지며, 관련성 라벨의 불완전성이 결과를 바꿀 수 있다. BEIR의 여러 데이터셋은 어휘 기반 검색 후보만 판정하여, TREC-COVID에서 밀집 검색기 상위 10개 결과의 최대 31.8%가 판정되지 않은 문서였다. 980건을 추가 판정하자 DPR의 nDCG@10이 0.332에서 0.445로 오르고 ANCE가 BM25를 앞섰다[24]. 근거 귀속을 NLI 모델로 자동 판정한 ALCE의 사람 일치도는 인용 재현율 κ 0.698, 인용 정밀도 0.525였다[25].

질의 범위는 층화와 답할 수 없는 질의로 설계할 수 있다. CRAG는 4,409개 질의를 영역, 유형, 개체 인기도, 시간 변동성으로 층화하여 인기도가 낮고 변동이 큰 층의 낮은 정확도를 드러냈고[26], MultiHop-RAG는 답할 수 없는 질의 301개로 응답 거부를 평가하였다[27].

### 2.6 에이전트, 안전성, 다국어 평가셋

에이전트 평가에서 τ-bench는 대화 후 데이터베이스 상태를 기대 상태와 비교하여 채점하고, k번의 독립 시행이 모두 성공할 확률인 pass<sup>k</sup>를 정의하였다. GPT-4o의 소매 영역 성공률은 pass<sup>1</sup> 약 61%에서 pass<sup>8</sup> 약 25%로 떨어졌다[28]. 여기서는 최종 상태가 정답이고 반복 실행의 일관성도 측정 대상이다.

안전성 평가셋에서는 거부해야 할 문항과 거부하면 안 되는 문항의 비용이 다르다. HarmBench는 공격 성공 분류기를 사람 라벨과 대조하였고[29], XSTest는 응해야 할 안전한 프롬프트 250개와 대조용 위험 프롬프트 200개를 손으로 작성하였다[30]. OR-Bench는 LLM 세 개의 다수결로 과잉 거부 문항 8만 개를 라벨링하였다. 군중 작업자 3명, 앙상블, 저자 1명의 다수결을 기준으로 한 100문항 검증에서 앙상블의 정확도(93.0%)는 군중 작업자 모두보다 높고 저자(94.0%)에 근접하였으며, 저자들은 이를 LLM 라벨의 근거로 제시하였다. 다만 소수인 유해 범주에서 잰 위양성률은 16.0%로 저자(8.0%)의 두 배였다[31].

다국어 평가셋에서는 번역 품질과 문화적 편향이 별도의 검증 대상이다. KMMLU는 번역 대신 한국 원어 시험으로 35,030문항을 구축하고 공개 후 741개 문항을 수정하였다[32]. Global-MMLU의 주석 표본에서는 MMLU 문항의 28%가 서구 문화 지식을 요구하였고, 41개 비영어 언어 중 14개만 전문 번역 후 교정을 거쳤다[33].

### 2.7 종합

전문가 작성과 적대적 수집은 정확성이나 변별력을 얻는 대신 비용과 모호성을 지고, 로그는 현실성을 얻는 대신 분포 변화와 개인정보 관리를, 합성은 규모를 얻는 대신 정답 검증을 떠안으며, 애플리케이션별 요건은 정답의 형식과 채점 단위를 바꾼다. 따라서 본고는 어느 방식도 정확성, 현실성, 비용을 함께 만족하지 못하며, 구축 출처만으로는 품질을 판단할 수 없으므로 어떤 평가셋이든 3장의 검증을 거쳐야 한다고 본다.

## 3. 검증: 다섯 측면

본고는 평가셋 검증을 구성 타당도, 라벨 신뢰도, 오류 감사, 통계적 충분성, 오염·재현성 통제의 다섯 측면으로 정리한다. 이들은 병렬 점검 대상이며(구성 타당도만 논리적으로 먼저 온다), 한 측면의 점검이 다른 측면의 결함을 배제하지 않는다. 전문 개발자의 선별로 오류 감사(3.3절)를 거친 SWE-bench Verified에서는 2026년 분석에서 오염(3.5절)이 드러났다. OpenAI는 시험한 최신 모델 세 개가 모두 일부 과제에서 정답 패치나 문제 서술의 세부를 그대로 재현하였다고 보고하고 이 벤치마크를 평가에서 제외하였다[34]. GSM8K도 라벨 재검수에서 오류 문항이 확인되었고(3.3절)[5], 이와 별개로 같은 분포의 새 평가셋에서 오염의 흔적이 드러났다(3.5절)[35].

### 3.1 구성 타당도

라벨이 정확하고 표본이 충분해도 평가셋이 의도한 능력을 측정하지 않으면 골든이 아니다. LLM 벤치마크 445개를 검토한 연구에서 측정 대상을 정의한 벤치마크는 78.2%였으나 그 정의의 47.8%는 합의되지 않은 개념이었다[11]. BetterBench는 설계부터 폐기까지 46개 모범 사례를 제시하였다[10]. 애플리케이션 평가셋에서는 배포될 과제가 측정 대상이므로 과제 정의서와 층별 문항 구성이 증거가 된다.

### 3.2 라벨 신뢰도

주석자 간 일치도는 기준값과 함께 불일치 문항의 성격을 보고해야 해석할 수 있다. Krippendorff는 α 0.800 이상을 요구하고, 잠정적 결론에는 0.667 이상을 하한으로 제시하였다[36]. Artstein과 Poesio는 단일 기준값이 모든 목적에 맞는지 의문을 제기하고, 범주 분포가 치우치면 관측 일치율이 0.96이어도 우연 보정 계수 K가 0.65에 그치는 예를 보였다[37]. 불일치는 주석자를 늘려도 남았고[38], 이를 잡음이 아닌 신호로 보아야 한다는 주장도 있다(5.1절)[39–41].

### 3.3 오류 감사

일치도가 높아도 모두가 같은 오류를 범할 수 있으므로 정답 자체를 감사해야 하며, 모델 불일치로 찾은 오류 수는 오류율의 하한으로 해석해야 한다. 플래티넘 벤치마크 연구는 15개 벤치마크의 부분집합에서 최신 LLM 중 하나라도 틀린 문항을 사람이 재검토하였고[42], GSM8K 평가셋 전체에서는 모델 오답으로 표시된 219문항을 검토하여 110문항을 제거하고 10문항의 정답을 고쳤다[5]. 저자들은 모든 모델이 틀린 정답에 동의하는 문항은 이 절차로 찾을 수 없으므로 찾은 오류 수가 하한이라고 밝혔다[42]. 문항 반응 이론(IRT)의 음의 변별도는 주석 오류를 시사하였고[43], 문항 통계와 LLM 1차 선별의 결합은 벤치마크 9종에서 최대 84%의 정밀도로 문제 문항을 찾았다[44]. 다만 주석 오류 탐지 방법 18종을 9개 데이터셋에서 비교한 연구에서는 실제 코퍼스의 성능이 인공 오류 실험보다 크게 떨어졌다[45]. 같은 측면의 재감사가 결함을 추가로 찾은 사례도 있다. HLE는 출시 전 감사(2.1절) 뒤 외부 감사에서 텍스트 전용 화학·생물 문항의 29±3.7%(95% 신뢰구간)가 동료 심사 문헌과 직접 충돌하는 답을 가진 것으로 추정되었고[15], 이 제안에 따른 생물·화학·보건 부분집합 검토에서 전문가 불일치율은 약 18%였다[14]. 따라서 모델 불일치 기반 감사는 모든 모델이 공유하는 오류를 놓치며, 무작위 표본 감사와 함께 써야 오류율을 추정할 수 있다.

정답을 판정하는 기준 자체도 감사 대상이다. HumanEval의 테스트를 80배로 늘리자 pass@k가 최대 19.3–28.9% 떨어져, 기존 테스트가 잘못된 코드를 통과시켰음이 확인되었다[46]. SWE-bench Verified는 개발자 93명이 표본 1,699개 중 부적격 항목(68.3%)을 걸러 500개를 선정하였으나[47], 2026년 재감사에서는 64회 독립 실행에서 o3가 매번 풀지는 못한 138문항(27.6%) 중 최소 59.4%에 테스트 설계나 문제 서술의 중대한 결함이 있었다[34].

### 3.4 통계적 충분성

평가셋의 크기는 구분하려는 성능 차이에 맞추어 정해야 한다. NLP 비교 실험의 상당수는 검정력이 부족하였고, 문장 2,000개의 기계번역 평가셋도 BLEU 1점 차이를 약 75%의 검정력으로만 탐지하였다[48]. Miller는 쌍체 비교와 함께 묶인 문항에 군집 표준오차를 쓰도록 권고하였고, DROP에서 군집 표준오차는 단순 표준오차의 약 3.05배였다. [0,1] 연속 점수를 가정한 예시에서 쌍체 차이의 문항 간 분산을 1/9, 반복 표집 분산을 0으로 두면 3%p 차이를 유의수준 0.05, 검정력 80%로 탐지하는 데 약 969문항이 필요하였고, 저자는 새 평가셋에 최소 1,000문항을 권고하였다[49]. IRT로 고른 과제별 100문항은 전체 점수를 평균 약 2% 오차로 추정하였는데, 정답 패턴 기반 앵커는 전문화된 모델에서 추정이 나빠진 반면 IRT 기반 앵커는 약간만 영향을 받았다[50]. 본고는 이런 부분집합을 상시 모니터링에만 쓸 것을 권한다. 잡음 대비 모델 간 점수 퍼짐(신호)의 비가 높은 벤치마크일수록 의사결정이 정확하였다는 보고도 있다[51]. 그러나 벤치마크 445개 중 불확실성 추정이나 통계 검정을 쓴 것은 16.0%에 그쳐[11], 이 측면은 공개 벤치마크에서도 자주 생략된다.

### 3.5 오염·재현성 통제

평가 문항이 학습 데이터에 들어가면 점수가 부풀고 잘못된 결론이 출판될 수 있다[8,52]. 원래 문항 순서의 우도가 섞은 순서보다 유의하게 높은지 보는 검정은 학습 데이터 없이 오염을 탐지하였고[53], BIG-bench는 학습 데이터에서 걸러 낼 수 있도록 카나리아 문자열을 넣었다[54]. GSM8K와 같은 분포로 새로 만든 GSM1k에서는 정확도가 최대 8%p 떨어진 모델이 있었고, GSM8K 문항의 생성 확률과 하락 폭 사이에 중간 정도의 양의 관계(Spearman r²=0.36)가 있었다[35]. LiveBench는 문항을 매월 갱신하고 LiveCodeBench는 공개 시점을 기록하여 학습 시점 이후 문항만 평가할 수 있게 하였다[55,56].

오염이 없어도 점수가 재현되지 않을 수 있다. SWE-bench Verified 500문항 중 16문항은 다른 기관의 실행 환경에서 안정적으로 실행되지 않았고[57], 프롬프트와 채점 구현의 차이도 점수를 바꾸어 프롬프트와 평가 코드의 공개가 권고되었다[58]. 본고는 문헌이 권고하거나 적용한 비공개 보존 분할과 공개 시점 기록[11,56]에 더해 실행 환경과 평가 코드의 고정을 이 측면의 점검 항목으로 제안한다.

## 4. 골든의 정의와 적용

### 4.1 개념의 변천

정보검색의 시험 모음 전통에서 "골드 표준"은 절대적 정답을 뜻하지 않았다. TREC 시험 모음에서는 평가자마다 관련성 판정이 크게 달랐지만 시스템 순위는 높은 상관을 유지하였고, 이 순위 안정성이 실험 도구로 쓰는 근거였다[59]. 이후 CALBC는 여러 자동 태거의 출력을 합의로 통합한 코퍼스를 은 표준(silver standard)이라 불렀고[60], Vendrow 등은 라벨 오류와 모호성을 최소화하도록 재검수한 벤치마크를 플래티넘이라 부를 것을 제안하였다[42]. Aroyo와 Welty는 "단일 정답", "한 번 만들면 영원히 유효하다" 등 주석의 신화를 비판하였다[40]. 본고는 이에 따라 골든을 고정된 속성이 아니라 목적과 시점에 따른 상태로 본다.

### 4.2 정의와 일곱 조건

본고는 골든셋을 **명시된 평가 목적과 버전에 대해 표 2의 일곱 조건을 충족한다는 증거가 문서로 남은 평가셋**으로 정의할 것을 제안한다. 조건 C1–C5는 3장의 다섯 측면에 차례로 대응하고, C6과 C7은 그 증거를 남기고 갱신하는 절차이다. 2장의 구축 방식은 정의의 조건이 아니라 주로 C1–C3에서 점검할 위험의 출처이다. 최소 판정 기준은 문헌의 기준값이 있으면 그것을 쓰고, 없으면 무엇을 보고해야 하는지를 정한 본고의 제안이다. C3의 기준은 라벨 오류가 측정된 모델 간 차이를 최대 오류율만큼 왜곡할 수 있다는 데서 나왔다. 오류율이 비교할 차이에 가까우면 오류만으로 순위가 바뀌므로(1장)[3], 오류율의 95% 신뢰구간(Wilson) 상한이 목표 차이 δ의 절반 이하일 것을 요구한다. 독립 작성자의 답이 일치한 문항만 남기는 합의 선별 설계에서는 선별 후 독립 재주석 표본의 일치율을 C2의 대체 증거로 인정한다.

표 2의 마지막 열이 보여 주듯 조건 대부분은 Bowman과 Dahl의 네 기준(타당성, 정확하고 일관된 라벨, 충분한 검정력, 사회적 편향을 드러내고 편향된 시스템의 유인을 주지 않을 것)[9], BetterBench[10], Bean 등의 권고[11]와 겹친다. 본고는 여기에 판정 단위를 목적과 버전으로 한정하고, 실행 환경·평가 코드 고정(C5)과 채점 기준의 동시 버전 관리(C7)를 명시하며, 조건마다 최소 판정 기준을 두었다.

<!-- wide -->
**표 2.** 골든셋의 일곱 조건: 운영 점검, 최소 판정 기준, 문헌 근거, 기존 기준과의 대응

| 조건 | 운영 점검과 남길 증거 | 최소 판정 기준(본고 제안) | 문헌 근거 | 기존 기준 대응 |
| --- | --- | --- | --- | --- |
| C1 구성 타당도 | 과제 정의서, 배포 과제·위험 영역별 층과 층별 문항 수 | 정의서가 있고, 결론을 내릴 각 층에서 목표 차이를 검정력 80%로 탐지하는 문항 수 | 정의한 벤치마크의 47.8%가 합의되지 않은 개념[11]; 층별 성능 차이[26] | BD 1·4; BB 설계; Bean 1–4·8 |
| C2 라벨 신뢰도 | 다중 주석 표본, 우연 보정 일치도, 중재 기록, 비집계 라벨 | α≥0.800, 잠정 결론은 α≥0.667. 합의 선별 설계는 선별 후 독립 재주석 일치율로 대체. 미달 시 불일치가 큰 문항은 분포형으로 분류하거나 제외 | 기준값[36]; 단일 기준값의 한계[37] | BD 2 |
| C3 오류 감사 | 모델 불일치 재검토와 무작위 표본 감사, 수정·제거 목록 | 무작위 표본 오류율의 95% 신뢰구간(Wilson) 상한 ≤ δ/2 | 평가셋 10종 평균 오류율 ≥3.3%[3]; 감사 결과는 하한[42] | BD 2; Bean 7 |
| C4 통계적 충분성 | 최소 탐지 차이, 검정력 계산, 군집·쌍체 신뢰구간 | 목표 차이를 검정력 80%로 탐지하는 문항 수 | 연속 점수 예시 가정에서 3%p 탐지에 약 1,000문항[49] | BD 3; BB 문서화; Bean 6 |
| C5 오염·재현성 통제 | 비공개 분할, 공개 시점, 카나리아, 오염 검정, 실행 환경·코드 고정 | 비공개 분할 또는 학습 시점 이후 문항이 있고, 재실행 점수가 신뢰구간 안에 듦 | GSM1k에서 최대 8%p 하락[35]; 순서 검정[53] | Bean 5 |
| C6 문서화 | 구축 출처, 선별 기준, 주석자, 라이선스, 한계 | 데이터시트의 필수 항목과 기계 판독 메타데이터 | 데이터시트·데이터 카드[61,62]; Croissant-RAI[63] | BB 문서화 |
| C7 유지·버전 | 버전 식별자, 정오표, 재감사 주기, 채점 기준 동시 버전, 폐기 기준 | 버전마다 C1–C6 증거를 다시 기록 | 한 번 만들면 영원히 유효하다는 신화[40]; 기준 표류[64] | BB 유지·폐기 |

주: BD는 Bowman과 Dahl의 기준 번호[9], BB는 BetterBench의 수명 주기 단계[10], Bean은 Bean 등의 권고 번호[11]이다. BD 4(사회적 편향)는 위험 영역별 층 설계로 C1에 포함하였다. δ는 평가 목적이 정한 목표 차이이다.

C6과 C7의 증거는 기존 도구로 남길 수 있다. 문서화 항목은 Datasheets와 Data Cards가 제시하였고[61,62], Croissant의 책임 있는 AI 확장은 기계 판독 형식을 제공하며[63], NeurIPS 2026 데이터셋 투고는 한계, 편향, 의도된 용도를 이 형식에 담도록 요구한다[65]. 버전 관리는 데이터셋 저장소의 버전과 데이터 카드 기능으로 구현할 수 있고[66], 폐기 절차는 데이터셋 폐기 틀을 참고할 수 있다[67]. 채점 기준도 유지 대상이다. 참여자 9명의 사용자 연구에서 출력을 채점하며 채점 기준을 바꾸는 기준 표류(criteria drift)가 관찰되었다[64].

### 4.3 적용 예: SimpleQA

SimpleQA[16]를 두 모델의 단답형 사실성 정답률 차이를 3%p(δ) 수준에서 판정하는 목적에 비추어 표 2로 판정한다. C1에서 측정 대상은 명시되어 있으나 10개 주제는 출간 뒤 ChatGPT로 붙인 사후 태그이고, 가장 작은 주제(135문항)에서는 약 17%p 차이만 탐지할 수 있어 층 설계의 증거가 없다(본고 계산). C2에서는 두 작성자의 답이 일치한 문항만 남겼으므로 대체 규칙을 적용하며, 제3 작성자의 독립 재풀이 일치율 94.4%는 우연 일치가 거의 없는 단답형에서 기준을 충족한다. C3에서 재풀이로 찾은 오류율 2.8%는 불일치로 찾은 값이므로 하한이다. 그 Wilson 상한(약 4.0%)도 이미 δ/2를 넘어 기준을 충족하지 못한다(본고 계산). 실제로 후속 재감사인 SimpleQA Verified는 부정확한 라벨, 주제 편향, 중복 문항을 지적하고 문항을 1,000개로 줄였다[68]. C4에서 4,326문항은 최악 가정(정답률 50%, 독립 표본)에서도 약 3.0%p 차이를 탐지할 수 있어 기준을 충족한다(본고 계산). C5–C7의 비공개 분할, 데이터 카드, 버전별 정오표는 논문과 공개 저장소에서 확인되지 않았다. 따라서 SimpleQA는 이 목적에 대해 C2와 C4만 충족하여 본고의 정의로는 골든셋이 아니며, 재감사가 다른 기관의 별도 벤치마크로 이루어졌다는 점은 유지 절차(C7)의 공백을 보여 준다.

### 4.4 2단 구성과 핵심셋 설계

2단 구성은 표 2의 조건을 갖춘 골든 핵심셋(이하 핵심셋)으로 합성·로그 기반 은 표준 보조셋(이하 보조셋)의 자동 판정을 보정하는 설계이며, 근거는 소규모 정답 라벨로 대규모 예측의 편향을 보정하는 예측 기반 추론(PPI)이다[69]. AutoEval은 GPT-4 실험에서 사람 라벨의 유효 표본 크기를 최대 50% 늘렸고[70], 층화 PPI는 층별로 보정하여 효율을 더 높였다[71]. 그러나 PPI는 정답 라벨 표본과 예측 표본이 같은 분포에서 독립적으로 추출되었다고 가정한다[69]. 따라서 PPI 보정용 핵심셋은 보조셋 모집단에서 무작위로, 또는 층 가중치를 아는 층화 표집으로 뽑아 정답을 붙여야 하며, 별도로 큐레이션한 핵심셋은 PPI 보정이 아니라 판정 모델 승인과 모델 비교에 써야 한다. 이득에는 상한도 있다. 판정 모델이 평가 대상보다 정확하지 않으면 어떤 편향 보정도 필요한 정답 라벨을 절반 넘게 줄이지 못하였고, 최신 모델 실험에서 층화 PPI가 표준 층화 표집보다 표본 효율을 두 배 넘게 높인 경우는 드물었다[72].

판정 모델 보정은 ARES처럼 150–300문항에서 출발할 수 있으나[20], 승인에는 일치율과 점수 차이를 함께 측정해야 한다. GPT-4 판정의 사람 일치율이 80%를 넘은 연구도 있지만[73], TriviaQA 400문항 설정에서는 정렬도가 가장 높은 판정 모델(GPT-4 Turbo, Llama-3 70B)도 사람 점수와 최대 5점, 일치율이 높은 다른 판정 모델은 10–20점까지 달랐다. 이 연구는 우연 보정 지표를 함께 쓸 것을 권고하였고[74], 일치도는 평가 속성과 주석자 전문성에 따라서도 달랐다[75].

모델 비교에 쓰는 핵심셋의 규모는 C4로 정한다. 같은 n문항을 정오(0/1)로 채점하여 두 모델을 쌍체 비교하면, 한 모델만 맞힌 문항의 비율을 p<sub>d</sub>라 할 때 필요한 문항 수는 대략 (z<sub>α/2</sub>+z<sub>β</sub>)<sup>2</sup>(p<sub>d</sub>−δ<sup>2</sup>)/δ<sup>2</sup>이다. δ=3%p에서 p<sub>d</sub>가 0.10이면 약 864문항, 0.05이면 약 428문항이 필요하다(본고 계산). p<sub>d</sub>는 δ보다 작을 수 없고 작을 때는 McNemar 정확 검정을 써야 한다. Miller의 969문항은 연속 점수 예시이므로, 정오 평가에서는 예비 실행으로 p<sub>d</sub>를 추정하여 이 식으로 계산해야 한다.

## 5. 논의

### 5.1 쟁점

첫째 쟁점은 규모와 품질이며, 본고는 2단 구성으로 두 입장을 결합하되 그 이득에 상한이 있다고 본다. 규모 쪽에서는 Anthropic 문서가 신호가 다소 약한 자동 채점 문항을 많이 두라고 권고하였고[2], AutoEval과 층화 PPI는 자동 판정으로 사람 라벨의 효용을 높였다[70,71]. 품질 쪽에서는 벤치마크 연구가 철저히 검증되고 모호하지 않은 문항을 요구하였다[9,42]. 정답 라벨 절감이 최대 절반이라는 상한[72]은 라벨 비용을 줄인다는 점에서 의미가 있다. 그러나 필요 문항 수는 1/δ<sup>2</sup>로 늘므로, 차이가 작은 비교에서는 절반의 절감으로도 감당하기 어렵고 핵심셋 자체를 키워야 한다.

둘째 쟁점은 단일 정답과 관점주의이며, 본고는 문항을 정답형과 분포형으로 나누는 절충을 제안한다. 주관적 판단이 들어가는 평가에서는 다수결 라벨보다 라벨 분포를 보존하는 편이 타당하다는 주장이 있으나[38,39,41], 회귀 검사는 합격 여부를 정하는 고정된 기준을 요구한다. 정답형 문항은 단일 정답으로 채점하고, 분포형 문항은 비집계 라벨을 보존하여 모델 응답에 동의한 주석자 비율로 채점한다. 이 점수는 연속값이므로 회귀의 합격 임계값을 따로 정해야 하고, 생성형 응답이 어느 주석자 라벨과 같은지 판단하는 데 판정 모델이 다시 개입한다는 한계가 있다.

셋째 쟁점은 출력 채점이 아닌 정답 라벨 생성에서 사람을 LLM으로 대체하는 문제이며, 본고는 LLM 라벨을 사람 라벨로 검증된 은 표준으로 한정할 것을 제안한다. 지지 근거는 강하다. ChatGPT의 영점 주석 정확도는 군중 작업자보다 평균 약 25%p 높았고 비용은 약 30분의 1이었으며[76], Bing 관련성 판정과 OR-Bench에서도 LLM이 제3자·군중 작업자보다 정확하였다(2.6절)[31,77]. 반대 근거는 과제별 변동에 있다. 27개 주석 과제에서 LLM의 중앙 정확도는 0.850이었으나 9개 과제에서는 정밀도나 재현율이 0.5 미만이었고, 저자들은 과제마다 사람 검증이 필요하다고 결론지었다[78]. 따라서 LLM 라벨은 과제마다 사람 라벨로 검증한 뒤 은 표준으로 쓰고, 핵심셋의 정답은 사람이 확정한다. 판정에서 보고된 자기 선호[19]가 같은 계열 모델의 라벨 생성에도 나타나는지는 확인한 문헌에 없었다.

넷째 쟁점은 정적 평가셋과 동적 평가셋이며, 본고는 고정 스냅숏과 갱신 분할을 함께 두는 절충을 제안한다. LiveBench, LiveCodeBench, HLE의 주기적 갱신·개정은 오염과 포화를 늦추려는 설계이나[14,55,56], 회귀 검사는 시점이 다른 모델을 같은 척도로 비교하는 정적 평가셋에 의존한다. 고정 스냅숏을 회귀 기준으로, 갱신 분할을 별도 버전으로 두고 두 점수를 함께 보고하는 방식이며, 이는 C5와 C7의 운영 방식이기도 하다. 갱신 주기가 짧으면 기준을 자주 바꾸어야 하는 부담이 남는다.

### 5.2 연구 공백과 향후 과제

네 가지 공백이 남아 있다. 첫째, 평가셋 오류가 실제 배포 결정을 얼마나 바꾸는지 정량화한 연구는 공개 벤치마크의 순위 역전과 차이 은폐 사례[3,5]를 넘지 못하였다. 사내 평가셋에 오류를 주입하여 모델 선택이 바뀌는 오류율을 측정하는 연구가 필요하다. 둘째, RAG 지식 베이스 문서가 갱신될 때 정답과 근거 라벨을 함께 갱신하는 절차는 확인하지 못하였으며, 질의 수준의 시간 변동 층화[26]를 넘어 문서 버전과 정답 버전을 연결하는 방법이 필요하다. 셋째, 한국어에서는 원어 시험 기반 구축과 공개 후 오류 수정 사례가 있으나[32], 한국어 RAG·에이전트 평가셋에서 일치도 기준값과 필요 문항 수를 실증한 연구는 드물었다. 넷째, 본고의 일곱 조건과 최소 판정 기준은 문헌 종합에서 도출한 제안이므로, 여러 평가셋에 적용하여 조건 충족과 평가 결론의 안정성 사이의 관계를 실증해야 한다.

### 5.3 본고의 한계

서술형 종합이므로 누락된 문헌이 있을 수 있고, 검색과 요약에 LLM 에이전트를 활용하였으며 일부 출처는 웹 아카이브 사본으로 확인하였다. 회색 문헌은 개정·폐기될 수 있으며, 인용한 OpenAI Evals 문서도 2026년 11월 30일 플랫폼 종료를 공지하고 있다[1].

## 6. 결론

본고는 골든이라는 이름이 평가셋을 만든 방식이 아니라 명시된 목적과 버전에 대한 검증 증거에 붙어야 한다고 결론짓는다. 첫째, 네 구축 방식은 성격이 다른 위험을 지며 어느 것도 정확성, 현실성, 비용을 함께 만족하지 못한다고 판단되고, RAG, 에이전트, 안전성, 다국어 평가셋은 정답의 형식과 채점 단위에 요건을 더한다. 둘째, 다섯 검증 측면은 따로 점검해야 한다. 오류 감사를 거친 평가셋에서 오염이 드러났고, 재감사가 앞선 감사의 누락을 찾아 감사 결과가 하한임을 보였으며, 통계적 충분성은 공개 벤치마크에서도 드물게 점검되었다. 셋째, 일곱 조건과 최소 판정 기준은 감사 점검표로 쓸 수 있으며, SimpleQA는 3%p 수준의 비교 목적에서 골든셋으로 판정되지 않았다. 쟁점에 대해서는 PPI 보정용 핵심셋을 보조셋 모집단의 확률 표본으로 뽑고 작은 차이의 판정에는 검정력에 맞는 핵심셋을 둘 것, 분포형 문항은 비집계 라벨로, LLM 라벨은 과제별로 검증한 은 표준으로, 동적 갱신은 고정 스냅숏과 병행할 것을 제안하였다. 제안의 유효성은 영어 이외의 평가셋과 실제 배포 결정에서 검증되어야 한다.

## 저자 기여, 연구비, 이해상충, 데이터 가용성

**저자 기여**: [추후 기입]. **연구비**: [추후 기입]. **이해상충**: [추후 기입]. **데이터 가용성**: 새로운 데이터를 생성하지 않았다. 검색 주제, 출처별 확인 기록, 원문 대조 결과, 퇴고와 심사 기록은 프로젝트 저장소(github.com/Pseudo-Lab/no-more-slops, tracks/auto-paper/projects/golden-dataset-review)에 보충 자료로 두며, 영속 식별자(DOI)는 [추후 기입]이다.

## 생성형 AI 사용 고지

저자는 문헌 검색과 요약, 출처 확인, 초안 작성과 퇴고에 Anthropic Claude(Claude Code, claude-opus-5-5)를 사용하였다. 인용 문헌의 수치는 Claude 에이전트가 원문, 초록 또는 웹 아카이브 사본과 대조하였고, "본고 계산"으로 표시한 수치(4.3, 4.4절)는 Claude가 산식에 따라 계산하였고, 별도의 에이전트와 심사 과정에서 산술과 전제(예: 정오 채점에서의 분산 하한)를 검증하였다. 저자가 원문을 직접 대조한 범위는 [추후 기입]이며, 최종 내용의 책임은 저자에게 있다.

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
14. Center for AI Safety, Scale AI, HLE Contributors Consortium. A benchmark of expert-level academic questions to assess AI capabilities. Nature. 2026;649(8099):1139–1146. doi:10.1038/s41586-025-09962-4.
15. Skarlinski M, Laurent J, Bou A, White A. About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong [Internet]. FutureHouse; 2025 Jul 23 [updated 2025 Sep 16; cited 2026 Oct 25]. Available from: https://www.futurehouse.org/research-announcements/hle-exam
16. Wei J, Karina N, Chung HW, Jiao YJ, Papay S, Glaese A, et al. Measuring short-form factuality in large language models. arXiv:2411.04368. 2024.
17. Li T, Chiang WL, Frick E, Dunlap L, Wu T, Zhu B, et al. From crowdsourced data to high-quality benchmarks: Arena-Hard and BenchBuilder pipeline. In: Proc ICML; 2025. arXiv:2406.11939.
18. Wang Y, Kordi Y, Mishra S, Liu A, Smith NA, Khashabi D, et al. Self-Instruct: aligning language models with self-generated instructions. In: Proc ACL; 2023. p. 13484–13508. doi:10.18653/v1/2023.acl-long.754.
19. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. In: Proc NeurIPS; 2024. arXiv:2404.13076.
20. Saad-Falcon J, Khattab O, Potts C, Zaharia M. ARES: an automated evaluation framework for retrieval-augmented generation systems. In: Proc NAACL; 2024. p. 338–354. doi:10.18653/v1/2024.naacl-long.20.
21. Bai G, Liu J, Bu X, He Y, Liu J, Zhou Z, et al. MT-Bench-101: a fine-grained benchmark for evaluating large language models in multi-turn dialogues. In: Proc ACL; 2024. p. 7421–7454. doi:10.18653/v1/2024.acl-long.401.
22. Gururangan S, Swayamdipta S, Levy O, Schwartz R, Bowman S, Smith NA. Annotation artifacts in natural language inference data. In: Proc NAACL; 2018. p. 107–112. doi:10.18653/v1/N18-2017.
23. Nie Y, Williams A, Dinan E, Bansal M, Weston J, Kiela D. Adversarial NLI: a new benchmark for natural language understanding. In: Proc ACL; 2020. p. 4885–4901. doi:10.18653/v1/2020.acl-main.441.
24. Thakur N, Reimers N, Rücklé A, Srivastava A, Gurevych I. BEIR: a heterogenous benchmark for zero-shot evaluation of information retrieval models. In: Proc NeurIPS Datasets and Benchmarks Track; 2021. arXiv:2104.08663.
25. Gao T, Yen H, Yu J, Chen D. Enabling large language models to generate text with citations. In: Proc EMNLP; 2023. p. 6465–6488. doi:10.18653/v1/2023.emnlp-main.398.
26. Yang X, Sun K, Xin H, Sun Y, Bhalla N, Chen X, et al. CRAG – comprehensive RAG benchmark. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2406.04744.
27. Tang Y, Yang Y. MultiHop-RAG: benchmarking retrieval-augmented generation for multi-hop queries. In: Proc COLM; 2024. arXiv:2401.15391.
28. Yao S, Shinn N, Razavi P, Narasimhan K. τ-bench: a benchmark for tool-agent-user interaction in real-world domains. In: Proc ICLR; 2025. arXiv:2406.12045.
29. Mazeika M, Phan L, Yin X, Zou A, Wang Z, Mu N, et al. HarmBench: a standardized evaluation framework for automated red teaming and robust refusal. In: Proc ICML (PMLR 235); 2024. p. 35181–35224. arXiv:2402.04249.
30. Röttger P, Kirk H, Vidgen B, Attanasio G, Bianchi F, Hovy D. XSTest: a test suite for identifying exaggerated safety behaviours in large language models. In: Proc NAACL; 2024. p. 5377–5400. doi:10.18653/v1/2024.naacl-long.301.
31. Cui J, Chiang WL, Stoica I, Hsieh CJ. OR-Bench: an over-refusal benchmark for large language models. In: Proc ICML (PMLR 267); 2025. p. 11515–11542. arXiv:2405.20947.
32. Son G, Lee H, Kim S, Kim S, Muennighoff N, Choi T, et al. KMMLU: measuring massive multitask language understanding in Korean. In: Proc NAACL; 2025. p. 4076–4104. doi:10.18653/v1/2025.naacl-long.206.
33. Singh S, Romanou A, Fourrier C, Adelani DI, Ngui JG, Vila-Suero D, et al. Global MMLU: understanding and addressing cultural and linguistic biases in multilingual evaluation. In: Proc ACL; 2025. p. 18761–18799. doi:10.18653/v1/2025.acl-long.919.
34. OpenAI. Why SWE-bench Verified no longer measures frontier coding capabilities [Internet]. OpenAI; 2026 Feb 23 [cited 2026 Oct 25]. Available from: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
35. Zhang H, Da J, Lee D, Robinson V, Wu C, Song W, et al. A careful examination of large language model performance on grade school arithmetic. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2405.00332.
36. Krippendorff K. Reliability in content analysis: some common misconceptions and recommendations. Hum Commun Res. 2004;30(3):411–433. doi:10.1111/j.1468-2958.2004.tb00738.x.
37. Artstein R, Poesio M. Inter-coder agreement for computational linguistics. Comput Linguist. 2008;34(4):555–596. doi:10.1162/coli.07-034-R2.
38. Pavlick E, Kwiatkowski T. Inherent disagreements in human textual inferences. Trans Assoc Comput Linguist. 2019;7:677–694. doi:10.1162/tacl_a_00293.
39. Plank B. The "problem" of human label variation: on ground truth in data, modeling and evaluation. In: Proc EMNLP; 2022. p. 10671–10682. doi:10.18653/v1/2022.emnlp-main.731.
40. Aroyo L, Welty C. Truth is a lie: crowd truth and the seven myths of human annotation. AI Mag. 2015;36(1):15–24. doi:10.1609/aimag.v36i1.2564.
41. Cabitza F, Campagner A, Basile V. Toward a perspectivist turn in ground truthing for predictive computing. Proc AAAI Conf Artif Intell. 2023;37(6):6860–6868. doi:10.1609/aaai.v37i6.25840.
42. Vendrow J, Vendrow E, Beery S, Madry A. Do large language model benchmarks test reliability? arXiv:2502.03461. 2025.
43. Rodriguez P, Barrow J, Hoyle AM, Lalor JP, Jia R, Boyd-Graber J. Evaluation examples are not equally informative: how should that change NLP leaderboards? In: Proc ACL; 2021. p. 4486–4503. doi:10.18653/v1/2021.acl-long.346.
44. Truong S, Tu Y, Hardy M, Reuel A, Tang Z, Burapacheep J, et al. Fantastic bugs and where to find them in AI benchmarks. In: Proc NeurIPS Datasets and Benchmarks Track; 2025. arXiv:2511.16842.
45. Klie JC, Webber B, Gurevych I. Annotation error detection: analyzing the past and present for a more coherent future. Comput Linguist. 2023;49(1):157–198. doi:10.1162/coli_a_00464.
46. Liu J, Xia CS, Wang Y, Zhang L. Is your code generated by ChatGPT really correct? Rigorous evaluation of large language models for code generation. In: Proc NeurIPS; 2023. arXiv:2305.01210.
47. OpenAI. Introducing SWE-bench Verified [Internet]. OpenAI; 2024 Aug 13 [cited 2026 Oct 25]. Available from: https://openai.com/index/introducing-swe-bench-verified/
48. Card D, Henderson P, Khandelwal U, Jia R, Mahowald K, Jurafsky D. With little power comes great responsibility. In: Proc EMNLP; 2020. p. 9263–9274. doi:10.18653/v1/2020.emnlp-main.745.
49. Miller E. Adding error bars to evals: a statistical approach to language model evaluations. arXiv:2411.00640. 2024.
50. Maia Polo F, Weber L, Choshen L, Sun Y, Xu G, Yurochkin M. tinyBenchmarks: evaluating LLMs with fewer examples. In: Proc ICML (PMLR 235); 2024. p. 34303–34326. arXiv:2402.14992.
51. Heineman D, Hofmann V, Magnusson I, Gu Y, Smith NA, Hajishirzi H, et al. Signal and noise: a framework for reducing uncertainty in language model evaluation. In: Proc NeurIPS; 2025. arXiv:2508.13144.
52. Sainz O, Campos JA, García-Ferrero I, Etxaniz J, Lopez de Lacalle O, Agirre E. NLP evaluation in trouble: on the need to measure LLM data contamination for each benchmark. In: Findings of EMNLP; 2023. p. 10776–10787. doi:10.18653/v1/2023.findings-emnlp.722.
53. Oren Y, Meister N, Chatterji N, Ladhak F, Hashimoto TB. Proving test set contamination in black-box language models. In: Proc ICLR; 2024. arXiv:2310.17623.
54. Srivastava A, Rastogi A, Rao A, Shoeb AAM, Abid A, Fisch A, et al. Beyond the imitation game: quantifying and extrapolating the capabilities of language models. Trans Mach Learn Res. 2023. arXiv:2206.04615.
55. White C, Dooley S, Roberts M, Pal A, Feuer B, Jain S, et al. LiveBench: a challenging, contamination-limited LLM benchmark. In: Proc ICLR; 2025. arXiv:2406.19314.
56. Jain N, Han K, Gu A, Li WD, Yan F, Zhang T, et al. LiveCodeBench: holistic and contamination free evaluation of large language models for code. In: Proc ICLR; 2025. arXiv:2403.07974.
57. Epoch AI. SWE-bench Verified [Internet]. Epoch AI Benchmarking Hub; n.d. [cited 2026 Oct 25]. Available from: https://epoch.ai/benchmarks/swe-bench-verified
58. Biderman S, Schoelkopf H, Sutawika L, Gao L, Tow J, Abbasi B, et al. Lessons from the trenches on reproducible evaluation of language models. arXiv:2405.14782. 2024.
59. Voorhees EM. Variations in relevance judgments and the measurement of retrieval effectiveness. Inf Process Manag. 2000;36(5):697–716. doi:10.1016/S0306-4573(00)00010-8.
60. Rebholz-Schuhmann D, Jimeno Yepes AJ, van Mulligen EM, Kang N, Kors J, Milward D, et al. CALBC silver standard corpus. J Bioinform Comput Biol. 2010;8(1):163–179. doi:10.1142/S0219720010004562.
61. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé III H, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86–92. doi:10.1145/3458723.
62. Pushkarna M, Zaldivar A, Kjartansson O. Data cards: purposeful and transparent dataset documentation for responsible AI. In: Proc ACM FAccT; 2022. p. 1776–1826. doi:10.1145/3531146.3533231.
63. Jain N, Akhtar M, Giner-Miguelez J, Shinde R, Vanschoren J, Vogler S, et al. A standardized machine-readable dataset documentation format for responsible AI. arXiv:2407.16883. 2024.
64. Shankar S, Zamfirescu-Pereira JD, Hartmann B, Parameswaran A, Arawjo I. Who validates the validators? Aligning LLM-assisted evaluation of LLM outputs with human preferences. In: Proc ACM UIST; 2024. doi:10.1145/3654777.3676450.
65. NeurIPS. Responsible AI metadata requirements for the Evaluations and Datasets Track, NeurIPS 2026 [Internet]. NeurIPS blog; 2026 May 4 [cited 2026 Oct 25]. Available from: https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/
66. Lhoest Q, Villanova del Moral A, Jernite Y, Thakur A, von Platen P, Patil S, et al. Datasets: a community library for natural language processing. In: Proc EMNLP System Demonstrations; 2021. p. 175–184. doi:10.18653/v1/2021.emnlp-demo.21.
67. Luccioni AS, Corry F, Sridharan H, Ananny M, Schultz J, Crawford K. A framework for deprecating datasets: standardizing documentation, identification, and communication. In: Proc ACM FAccT; 2022. p. 199–212. doi:10.1145/3531146.3533086.
68. Haas L, Yona G, D'Antonio G, Goldshtein S, Das D. SimpleQA Verified: a reliable factuality benchmark to measure parametric knowledge. arXiv:2509.07968. 2025.
69. Angelopoulos AN, Bates S, Fannjiang C, Jordan MI, Zrnic T. Prediction-powered inference. Science. 2023;382(6671):669–674. doi:10.1126/science.adi6000.
70. Boyeau P, Angelopoulos AN, Li T, Yosef N, Malik J, Jordan MI. AutoEval done right: using synthetic data for model evaluation. In: Proc ICML (PMLR 267); 2025. p. 5276–5290. arXiv:2403.07008.
71. Fisch A, Maynez J, Hofer RA, Dhingra B, Globerson A, Cohen WW. Stratified prediction-powered inference for effective hybrid evaluation of language models. In: Proc NeurIPS; 2024. p. 111489–111514. doi:10.52202/079017-3541.
72. Dorner FE, Nastl VY, Hardt M. Limits to scalable evaluation at the frontier: LLM as judge won't beat twice the data. In: Proc ICLR; 2025. arXiv:2410.13341.
73. Zheng L, Chiang WL, Sheng Y, Zhuang S, Wu Z, Zhuang Y, et al. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In: Proc NeurIPS Datasets and Benchmarks Track; 2023. arXiv:2306.05685.
74. Thakur AS, Choudhary K, Ramayapally VS, Vaidyanathan S, Hupkes D. Judging the judges: evaluating alignment and vulnerabilities in LLMs-as-judges. In: Proc GEM² Workshop; 2025. p. 404–430. arXiv:2406.12624.
75. Bavaresco A, Bernardi R, Bertolazzi L, Elliott D, Fernández R, Gatt A, et al. LLMs instead of human judges? A large scale empirical study across 20 NLP evaluation tasks. In: Proc ACL (Short Papers); 2025. p. 238–255. doi:10.18653/v1/2025.acl-short.20.
76. Gilardi F, Alizadeh M, Kubli M. ChatGPT outperforms crowd workers for text-annotation tasks. Proc Natl Acad Sci U S A. 2023;120(30):e2305016120. doi:10.1073/pnas.2305016120.
77. Thomas P, Spielman S, Craswell N, Mitra B. Large language models can accurately predict searcher preferences. In: Proc SIGIR; 2024. p. 1930–1940. doi:10.1145/3626772.3657707.
78. Pangakis N, Wolken S, Fasching N. Automated annotation with generative AI requires validation. arXiv:2306.00176. 2023.
