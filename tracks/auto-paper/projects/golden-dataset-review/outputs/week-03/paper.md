---
type: Mini Review
title: LLM·RAG 애플리케이션 평가용 골든 데이터셋의 구축과 검증: 미니 리뷰
title_en: Building and Validating Golden Evaluation Datasets for LLM and RAG Applications: A Mini Review
authors: [저자명 추후 기입]
affiliation: [소속 추후 기입] · 교신 저자: [연락처 추후 기입]
---

## 초록

LLM·RAG 애플리케이션의 평가셋은 흔히 골든 데이터셋이라 불리지만, 무엇이 평가셋을 "골든"으로 만드는지에 대한 합의된 정의는 없다. 본고는 주로 2015–2026년 문헌을 종합하여 구축 방식 네 가지와 애플리케이션별 요건, 검증의 다섯 측면을 정리하고, 골든을 명시된 목적과 버전에 대해 일곱 조건의 충족 증거가 문서로 남은 상태로 정의한다. 조건별 최소 판정 기준을 SimpleQA에 적용하고(3%p 비교 목적에서 골든셋 아님), 사람 라벨을 보조셋의 자동 판정을 보정하는 확률 표본과 판정 모델 승인·모델 비교에 쓰는 큐레이션 핵심셋으로 나누는 2단 구성과 네 쟁점을 논의한다.

**주제어**: 골든 데이터셋, 평가 데이터셋, 대형 언어모델, 검색 증강 생성, 라벨 품질, 벤치마크 타당도

## Abstract

Evaluation sets for LLM and RAG applications are often called golden datasets, yet no agreed definition exists. Synthesizing literature mainly from 2015 to 2026, we review four construction methods, application-specific requirements, and five validation dimensions; we propose that "golden" denote a documented state in which seven conditions are met for a stated purpose and version, apply minimum criteria to SimpleQA (which does not qualify for comparisons at a 3-percentage-point resolution), and discuss four controversies and a two-tier design that splits human labels between a sample that calibrates automatic judgments on an auxiliary set and a curated core set for judge approval and model comparison.

**Keywords**: golden dataset, evaluation dataset, large language models, retrieval-augmented generation, label quality, benchmark validity

## 1. 서론

LLM 애플리케이션 개발에서 평가셋은 프롬프트, 모델, 검색기를 바꿀 때마다 결과를 비교하는 기준이며, 실무에서는 이를 골든 데이터셋(이하 골든셋)이라 부른다[1,2]. 그러나 정답 자체가 틀릴 수 있다. 널리 쓰이는 평가셋 10종의 라벨 오류율은 평균 3.3% 이상으로 추정되었고[3], MMLU 문항의 6.49%가 오류(모호 문항 포함)로 추정되었으며[4], GSM8K를 재검수하자 원래 똑같이 45개를 틀린 두 모델이 각각 2개와 17개를 틀렸다[5]. 기존 서베이와 벤치마크 품질 연구는 평가 방법 일반이나 공개 벤치마크를 다루었고[6–10], 특정 애플리케이션의 평가셋을 만들고 검증하며 골든이라 부를 조건까지 묶은 리뷰는 확인되지 않았다. 본고는 (Q1) 구축 방식과 위험, (Q2) 검증 측면, (Q3) 골든의 조건과 운영을 다룬다. 문헌은 2026년 10월에 arXiv, ACL Anthology, 학회 논문집, 개발사 문서에서 검색하고 인용을 추적하여 모았으며(출처 기록 약 120건), 회색 문헌은 구분하였다.

## 2. 구축: 네 가지 출처와 애플리케이션별 요건

<!-- wide -->
<!-- cols: 15, 17, 31, 37 -->
**표 1.** 평가셋 구축 방식과 애플리케이션별 요건

| 구축 방식·요건 | 장점 | 주요 위험 | 보완책(대표 사례) |
| --- | --- | --- | --- |
| 전문가 작성 | 정확성, 고난도 | 비용, 전문가 간 불일치, 보상 구조의 오류 | 다단계 검토(GPQA), 2인 독립 일치(SimpleQA) |
| 실사용 로그 | 배포 분포 반영 | 저가치 문항, 선별에 따른 분포 변화, 개인정보 | 군집화와 선별 기준 기록(BenchBuilder) |
| LLM 합성 | 저비용, 범위 확대 | 정답 오류, 자기 선호 | 왕복 필터와 사람 라벨 보정(ARES) |
| 적대적 수집 | 변별력 | 정답 모호성·오류 | 독립 검증자 다수결(ANLI) |
| RAG | 검색·생성 오류 분리 | 판정 누락 문서, 귀속 판정의 제한된 일치도 | 추가 판정(BEIR), 층화와 답할 수 없는 질의(CRAG) |
| 에이전트·안전성·다국어 | 배포 행동·문화 맥락 측정 | 반복 실행 변동, 거부 오류 비용, 번역 편향 | pass<sup>k</sup>(τ-bench), 대조 문항(XSTest), 원어 구축(KMMLU) |

평가셋의 문항과 정답은 네 출처 또는 그 조합에서 나오며, 표 1은 각 방식과 애플리케이션별 요건을 비교한다.

### 2.1 전문가 작성

전문가가 문항과 정답을 작성하는 방식은 정확성을 우선하지만 비용이 크고, 전문가 라벨의 잡음과 보상 구조에 따른 오류가 남는다. GPQA는 전문가 두 명의 검토를 통과하고 비전문가 정답률이 1/3 이하인 198문항을 분리하였고 시간당 약 95달러를 지급하였다[11]. HealthBench 합의 기준 34개의 의사 간 일치도(macro F1)는 7개 주제별로 0.569–0.730이었다[12]. 최신 LLM이 틀린 문항만 접수하고 상금을 내건 Humanity's Last Exam(HLE)은 두 차례 전문가 검토를 거쳤지만 출시 전 감사에서 공개셋의 전문가 불일치율이 15.4%로 추정되었고[13], 외부 감사자는 화학·생물 문항의 오류가 이 보상 구조에서 비롯되었다고 보았다(3장)[14]. SimpleQA는 상금 대신 고용된 작업자가 GPT-4가 틀리는 문항을 작성하게 하였고, 두 작성자의 독립 답이 일치하는 문항만 남기고 제3의 작성자가 1,000문항을 다시 풀게 하여 오류율을 약 3%로 추정하였다(본고는 하한으로 봄, 4장)[15].

### 2.2 실사용 로그

실제 사용자 질의는 배포 분포를 반영하지만 평가 가치가 낮은 문항이 많고 정답은 별도로 붙여야 한다. BenchBuilder는 Chatbot Arena 질의 20만 개를 걸러 4,000개 주제로 군집화하고 LLM으로 일곱 가지 품질 기준을 채점하여 Arena-Hard의 500개를 선별하였다[16]. 선별은 분포를 바꾸므로 선별 기준을 기록하고, 로그 사용은 수집 동의를 전제로 한다.

### 2.3 LLM 합성

LLM 합성은 적은 비용으로 규모와 범위를 확보하지만 정답의 정확성과 생성 모델의 편향을 따로 검증해야 한다. 학습용 지시문을 합성한 Self-Instruct에서도 표본 200개 중 모두 올바른 항목은 54%였다[17]. 생성 모델이 판정 모델을 겸하면 편향이 더해질 수 있는데, 판정 모델로 쓰인 GPT-4와 Llama 2는 자신의 출력을 구별하였고, 미세조정으로 자기 인식 능력을 바꾸자 자기 선호의 강도가 선형으로 함께 변하였다[18]. 보완 절차로, ARES는 생성 질의가 자신의 원문 단락을 1위로 검색하는 경우만 남긴 뒤 사람 라벨 150–300개로 판정 모델을 보정하였다[19]. MT-Bench-101은 GPT-4 생성 대화 중 주석자 다섯 명 모두가 승인한 것만 남겼다[20].

### 2.4 적대적 수집

모델을 틀리게 하는 문항을 사람이 작성하는 적대적 수집은 난이도를 높이지만, 모델을 속인 것으로 보이는 문항에는 정답이 모호하거나 틀린 것이 섞일 수 있다. 이 방식은 군중 작성 데이터의 주석 흔적(가설 문장만으로 SNLI의 약 67%를 맞힘)[21]에 대응하는 방법의 하나로 쓰였다. 그러나 ANLI에서 모델을 속인 것으로 보인 사례의 비율은 세 라운드 합계 기준 18.54%에서 사람 검증 후 9.52%로 줄어(1라운드 29.68%→18.33%), 그런 문항의 약 절반이 독립 검증자의 동의를 얻지 못하였다[22].

### 2.5 RAG 평가셋

RAG 평가셋은 질의, 근거 문서, 정답으로 이루어지며, 관련성과 근거 귀속 판정의 불완전성이 결과를 바꿀 수 있다. 어휘 기반 후보만 판정한 BEIR의 TREC-COVID에서 밀집 검색기 상위 10개 결과의 최대 31.8%가 판정되지 않은 문서였다. 980건을 추가 판정하자 DPR의 nDCG@10이 0.332에서 0.445로 오르고 ANCE가 BM25를 앞섰다[23]. 근거 귀속을 NLI 모델로 자동 판정한 ALCE의 사람 일치도는 인용 재현율 κ 0.698, 인용 정밀도 0.525였다[24].

질의 범위는 층화와 답할 수 없는 질의로 설계한다. CRAG는 4,409개 질의를 영역, 유형, 인기도, 시간 변동성으로 층화하여 인기도가 낮고 변동이 큰 층의 낮은 정확도를 드러냈고[25], MultiHop-RAG는 답할 수 없는 질의 301개로 응답 거부를 평가하였다[26].

### 2.6 에이전트, 안전성, 다국어 평가셋

에이전트 평가셋에서는 최종 상태가 정답이고 반복 실행의 일관성도 측정 대상이다. τ-bench는 대화 후 데이터베이스 상태로 채점하고, k번의 독립 시행이 모두 성공할 확률인 pass<sup>k</sup>를 정의하였다. GPT-4o의 소매 영역 성공률은 pass<sup>1</sup> 약 61%에서 pass<sup>8</sup> 약 25%로 떨어졌다[27].

안전성 평가셋은 오류 비용이 다른 두 유형, 곧 거부해야 할 문항과 거부하면 안 되는 문항을 함께 두며, 대규모 셋에서는 라벨의 출처도 검증 대상이다. HarmBench는 공격 성공 분류기를 사람 라벨과 대조하였고[28], XSTest는 응해야 할 안전한 프롬프트 250개와 대조용 위험 프롬프트 200개를 손으로 작성하였다[29]. OR-Bench는 LLM 세 개의 다수결로 과잉 거부 문항 8만 개를 라벨링하였다. 100문항 검증에서 앙상블의 정확도(93.0%)는 군중 작업자 모두보다 높고 저자(94.0%)에 근접하였으나, 소수인 유해 범주의 위양성률은 16.0%로 저자(8.0%)의 두 배였다[30].

다국어 평가셋에서는 번역 품질과 문화적 편향이 별도의 검증 대상이다. KMMLU는 번역 대신 한국 원어 시험으로 35,030문항을 구축하고 공개 후 741개 문항을 수정하였다[31]. Global-MMLU 주석 표본에서는 문항의 28%가 서구 문화 지식을 요구하였다[32].

### 2.7 종합

네 방식은 각기 다른 대가를 지므로, 본고는 어느 방식도 정확성, 현실성, 저비용을 함께 갖추지 못한다고 본다. 애플리케이션별 요건은 정답의 형식과 채점 단위를 바꾸고 구축 출처만으로는 품질을 판단할 수 없으므로, 어떤 평가셋이든 3장의 검증을 거쳐야 한다.

## 3. 검증: 다섯 측면

본고는 검증을 구성 타당도, 라벨 신뢰도, 오류 감사, 통계적 충분성, 오염·재현성 통제의 다섯 측면으로 정리하며, 한 측면의 점검이 다른 측면의 결함을 배제하지 않는다. 선별을 거친 SWE-bench Verified에서도 2026년 분석에서 오염이 드러났고 OpenAI는 이를 자사 평가에서 제외하였다[33].

**구성 타당도.** 벤치마크 445개 중 측정 대상을 정의한 78.2%에서도 정의의 47.8%는 합의되지 않은 개념이었다[10]. 애플리케이션 평가셋에서는 과제 정의서와 층별 구성이 증거이다. **라벨 신뢰도.** Krippendorff는 α 0.800 이상(잠정 0.667)을 제시하였으나[34], 단일 기준값은 범주 분포가 치우치면 일치율 0.96에서도 우연 보정 계수 K가 0.65에 그치는 한계가 있다[35]. 불일치를 신호로 보아야 한다는 주장도 있다[36,37]. **오류 감사.** 모델 불일치로 찾은 오류는 모든 모델이 공유하는 오류를 놓치므로 하한이다[38]. 재감사가 결함을 더 찾은 사례도 있다. HLE의 텍스트 전용 화학·생물 문항은 외부 감사에서 29±3.7%(95% CI)가 문헌과 충돌하는 것으로 추정되었고[14], SWE-bench Verified에서 o3가 매번 풀지는 못한 138문항 중 59.4%에 결함이 있었다[33]. 따라서 오류율은 무작위 표본의 모든 문항에서 라벨을 보지 않은 전문가가 정답을 다시 도출하고 기존 라벨과 일치한 문항까지 제3자가 판정하는 독립 재도출 감사로 추정해야 한다. **통계적 충분성.** 3%p 차이에 약 1,000문항이 필요하다는 연속 점수 예시가 있고[39], NLP 비교의 상당수는 검정력이 부족하였으며[40], 벤치마크의 16.0%만 불확실성 추정·검정을 썼다[10]. **오염·재현성.** 새 평가셋 GSM1k에서 최대 8%p 하락한 모델이 있었고(최신 모델 다수는 소폭)[41], 갱신(LiveBench)과 공개 시점 기록(LiveCodeBench)이 대응책이며[42,43], 실행 환경과 프롬프트도 점수를 바꾸었다[44,45].

## 4. 골든의 정의와 적용

"골드 표준"은 절대 정답이 아니라 순위 안정성에 기댄 기준이었고[46], 이후 은 표준과 플래티넘이 구분되었으며[38,47], 영원한 정답이라는 주석의 신화도 비판되었다[48]. 따라서 본고는 골든셋을 **명시된 평가 목적과 버전에 대해 표 2의 일곱 조건을 충족한다는 증거가 문서로 남은 평가셋**으로 정의한다. 라벨 오류율이 e이면 한 모델은 참 정답을, 다른 모델은 잘못된 라벨과 같은 답을 내는 문항 때문에 두 모델의 정답률 차이가 최대 2e 왜곡될 수 있다. 이 왜곡을 목표 차이 δ의 절반 이하로 두기 위해 C3는 독립 재도출 오류율의 95% Wilson 상한이 δ/4 이하일 것을 요구한다. 독립 작성자 일치 문항만 남기는 합의 선별 설계에서는 우연 일치가 무시할 만한 과제에 한해 선별 후 독립 재주석 일치율을 C2의 대체 증거로 인정한다.

<!-- wide -->
<!-- cols: 11, 20, 53, 16 -->
**표 2.** 골든셋의 일곱 조건과 최소 판정 기준(본고 제안)

| 조건 | 남길 증거 | 최소 판정 기준 | 기존 기준 |
| --- | --- | --- | --- |
| C1 구성 타당도 | 과제 정의서, 위험 영역별 층과 문항 수 | 정의서, 모델 의존 선별의 기록·편향 평가, 결론을 낼 층에서 δ를 검정력 80%로 탐지 | BD 1·4; Bean 1–4·8 |
| C2 라벨 신뢰도 | 우연 보정 일치도, 비집계 라벨 | α≥0.800(잠정 0.667), 합의 선별 설계는 우연 일치가 무시할 만하면 독립 재주석 일치율로 대체, 미달 문항은 분포형 | BD 2 |
| C3 오류 감사 | 독립 재도출 감사, 수정 목록 | 오류율 95% Wilson 상한 ≤ δ/4(δ=3%p면 오류 0건에도 509문항) | BD 2; Bean 7 |
| C4 통계적 충분성 | 검정력 계산, 쌍체 신뢰구간 | δ를 검정력 80%로 탐지하는 문항 수 | BD 3; Bean 6 |
| C5 오염·재현성 | 비공개 분할, 실행 환경 고정 | 비공개 또는 학습 이후 문항, 재실행 차이의 95% 신뢰구간 ⊂ ±δ/2 | Bean 5 |
| C6 문서화 | 데이터시트, 기계 판독 메타데이터 | 필수 항목과 기계 판독 형식[49,50] | BB 문서화 |
| C7 유지·버전 | 정오표, 채점 기준 버전 | 버전마다 C1–C6 증거 재기록[51] | BB 유지 |

주: BD=Bowman과 Dahl[8], BB=BetterBench[9], Bean=Bean 등[10]. BD 4(사회적 편향)는 위험 영역별 층으로 C1에 포함.

SimpleQA[15]는 전체 정답률 차이를 3%p 수준에서 판정하는 목적에 대해 C2만 충족하고 C4는 조건부로 충족하여 골든셋이 아니다. C2는 우연 일치가 거의 없는 단답형이므로 독립 재풀이 일치율 94.4%(채점기 기준)를 α 기준에 견주어 충족으로 보되, 선별 후 값이라 신뢰도를 과대평가할 수 있다. C4에서 4,326문항이 3%p를 검정력 80%로 탐지하려면 한 모델만 맞힌 비율(p<sub>d</sub>)이 약 0.497 이하여야 하며(본고 계산), 이는 두 모델의 정오가 양의 상관이면 대체로 성립하나 독립이고 정답률이 약 46–54%이면 근소하게 깨진다. C1은 적대적 선별의 GPT-4 계열 편향이 평가되지 않았고 주제 편향이 지적되어[52], C6은 기계 판독 메타데이터가 없어 부분 충족이다. C3는 불일치 문항만 검토한 오류율 2.8%가 하한이고 그 Wilson 하한(1.9%, 본고 계산)도 δ/4(0.75%)를 넘어 미충족이며, C5·C7의 증거는 확인되지 않았다.

운영에서는 사람 라벨을 두 역할로 나눈다. 하나는 합성·로그 기반 보조셋의 자동 판정을 예측 기반 추론(PPI)으로 보정하는 확률 표본이다[53,54]. PPI는 라벨 표본과 예측 표본이 같은 분포에서 독립적으로 추출되었다고 가정하므로 이 표본은 보조셋 모집단에서 무작위 또는 층 가중치를 아는 층화 표집으로 뽑으며, 생성형 과제에서는 라벨이 정답이 아니라 모델 출력의 판정이므로 새 모델마다 다시 판정한다. 다른 하나는 판정 모델 승인과 모델 비교에 쓰는 큐레이션 핵심셋으로, 승인에는 일치율과 점수 차이를 함께 본다[55]. 핵심셋은 큐레이션된 분포를 추정하므로 선별·제외로 포함 확률이 달라지면 보정용 표본을 대신할 수 없으나, 층 가중치를 알고 오류를 수정한 층화 확률 표본은 두 역할을 겸할 수 있다. C4의 문항 수는 정오 쌍체 비교(α=0.05, 검정력 80%)에서 한 모델만 맞힌 비율을 p<sub>d</sub>라 할 때 대략 (z<sub>α/2</sub>+z<sub>β</sub>)<sup>2</sup>(p<sub>d</sub>−δ<sup>2</sup>)/δ<sup>2</sup>로, δ=3%p, p<sub>d</sub>=0.10이면 약 864문항이고(표준 식으로는 약 870[56], 본고 계산) p<sub>d</sub>는 예비 실행으로 추정한다.

## 5. 논의

### 5.1 쟁점

첫째 쟁점은 규모와 품질이며, 2단 구성으로 두 입장을 결합하되 그 이득에 상한이 있다고 본다. 규모 쪽에서는 Anthropic 문서가 신호가 다소 약한 자동 채점 문항을 많이 두라고 권고하였고[2], AutoEval은 GPT-4 실험에서 PPI로 사람 라벨의 유효 표본 크기를 최대 50% 늘렸다[57]. 품질 쪽에서는 벤치마크 연구가 철저히 검증되고 모호하지 않은 문항을 요구하였다[8,38]. 판정 모델이 평가 대상보다 정확하지 않으면 줄일 수 있는 사람 라벨은 최대 절반이지만[58], 그만큼도 비용 면에서는 의미가 있다. 그러나 필요 문항 수가 1/δ<sup>2</sup>로 늘므로, 차이가 작은 비교에서는 확률 표본이든 핵심셋이든 사람 라벨 표본 자체를 키워야 한다.

둘째 쟁점은 단일 정답과 관점주의이며, 문항을 정답형과 분포형으로 나누는 절충을 제안한다. 주관적 평가에서는 라벨 분포를 보존하는 편이 타당하다는 주장이 있으나[36,37,59], 회귀 검사는 고정된 합격 기준을 요구한다. 정답형 문항은 단일 정답으로 채점하고, 일치도가 낮은 분포형 문항(C2 미달)은 비집계 라벨을 보존하여 모델 응답에 동의한 주석자 비율로 채점한다. 이 점수는 합격 임계값을 따로 정해야 하고, 응답과 라벨의 일치 판단에 판정 모델이 다시 개입한다는 한계가 있다.

셋째 쟁점은 출력 채점이 아닌 정답 라벨 생성에서 사람을 LLM으로 대체하는 문제이며, LLM 라벨을 사람 라벨로 검증된 은 표준으로 한정할 것을 제안한다. 지지 근거로, ChatGPT의 제로샷 주석 정확도는 군중 작업자보다 평균 약 25%p 높았고 비용은 약 30분의 1이었으며[60], Bing 관련성 판정[61]과 OR-Bench(2.6절, 유해 범주의 위양성 제외)[30]에서도 LLM이 제3자·군중 작업자보다 정확하였다. 반대 근거는 과제별 변동에 있다. 27개 주석 과제에서 LLM의 중앙 정확도는 0.850이었으나 9개 과제에서는 정밀도나 재현율이 0.5 미만이었고, 저자들은 과제마다 사람 검증이 필요하다고 결론지었다[62]. 따라서 LLM 라벨은 과제마다 사람 라벨로 검증한 뒤 은 표준으로 쓰고, 핵심셋의 정답은 사람이 확정한다. 판정의 자기 선호[18]가 라벨 생성에도 나타나는지는 확인한 문헌에 없었다.

넷째 쟁점은 정적 평가셋과 동적 평가셋이며, 고정 스냅숏과 갱신 분할을 함께 두는 절충을 제안한다. LiveBench, LiveCodeBench, HLE의 주기적 갱신·개정은 오염과 포화를 늦추려는 설계이나[13,42,43], 회귀 검사는 시점이 다른 모델을 같은 척도로 비교하는 정적 평가셋에 의존한다. 고정 스냅숏을 회귀 기준으로, 갱신 분할을 별도 버전으로 두고 두 점수를 함께 보고하며, 이는 C5와 C7의 운영 방식이다. 갱신이 잦으면 기준 교체 부담이 남는다.

### 5.2 연구 공백과 향후 과제

네 가지 공백이 남아 있다. 첫째, 확인한 범위에서 평가셋 오류가 배포 결정을 얼마나 바꾸는지는 라벨 오류가 순위나 모델 간 차이를 바꾼 사례[3,5]를 넘어 정량화되지 않았으므로, 사내 평가셋에 오류를 주입하는 연구가 필요하다. 둘째, RAG 지식 베이스 문서가 갱신될 때 정답과 근거 라벨을 함께 갱신하는 절차는 확인하지 못하였으며, 질의 수준의 시간 변동 층화[25]를 넘어 문서 버전과 정답 버전을 연결하는 방법이 필요하다. 셋째, 한국어에서는 원어 시험 기반 구축과 공개 후 오류 수정 사례가 있으나[31], 한국어 RAG·에이전트 평가셋에서 일치도 기준값과 필요 문항 수를 실증한 연구는 드물었다. 넷째, 일곱 조건과 최소 판정 기준은 문헌 종합에서 도출한 제안이다. δ=3%p에서 C3는 독립 재도출 오류율의 95% 상한 0.75% 이하(1,000문항 감사에서 오류 2건 이하)를 요구하지만 공개 평가셋 10종의 평균 오류율은 3.3% 이상이었으므로[3], 이 엄격성과 평가 결론의 안정성 사이의 관계를 실증하고, 판정 모델 승인의 기준값도 정해야 한다.

### 5.3 본고의 한계

서술형 종합이라 누락 문헌이 있을 수 있고, 검색과 요약에 LLM 에이전트를 썼으며, 회색 문헌은 바뀔 수 있다(OpenAI Evals는 2026년 11월 30일 종료 예정[1]).

## 6. 결론

골든이라는 이름은 평가셋을 만든 방식이 아니라 명시된 목적과 버전에 대한 검증 증거에 붙어야 한다. 네 구축 방식은 어느 것도 정확성, 현실성, 저비용을 함께 갖추지 못하고, 다섯 검증 측면은 따로 점검해야 하며, 일곱 조건을 적용한 SimpleQA는 3%p 비교 목적에서 오류율 하한이 C3 기준을 넘고 오염 통제·유지의 증거가 없어 골든셋이 아니었다. 운영에서는 사람 라벨을 보정용 확률 표본과 비교용 핵심셋으로 나눈다. 제안의 유효성은 영어 이외의 평가셋과 실제 배포 결정에서 검증되어야 한다.

## 선언

**저자 기여·연구비·이해상충**: [추후 기입]. **데이터 가용성**: 검색·원문 대조·심사 기록은 프로젝트 저장소(github.com/Pseudo-Lab/no-more-slops, tracks/auto-paper/projects/golden-dataset-review)에 두며 DOI는 [추후 기입]이다. **생성형 AI 사용**: 문헌 검색·요약, 출처 확인, 초안·퇴고에 Anthropic Claude(claude-opus-5-5)를 사용하였다. 인용 수치는 에이전트가 원문과 대조하였고, 본고 계산 수치는 별도 에이전트가 재계산하였다. 저자의 원문 직접 대조 범위는 [추후 기입]이며 최종 책임은 저자에게 있다.

## 참고문헌

1. OpenAI. Evals [Internet]. OpenAI API documentation; 2026 [cited 2026 Oct 25]. Available from: https://developers.openai.com/api/docs/guides/evals
2. Anthropic. Create strong empirical evaluations [Internet]. Claude documentation; 2026 [cited 2026 Oct 25]. Available from: https://platform.claude.com/docs/en/docs/test-and-evaluate/develop-tests
3. Northcutt CG, Athalye A, Mueller J. Pervasive label errors in test sets destabilize machine learning benchmarks. In: Proc NeurIPS Datasets and Benchmarks Track; 2021. arXiv:2103.14749.
4. Gema AP, Leang JOJ, Hong G, Devoto A, Mancino ACM, Saxena R, et al. Are we done with MMLU? In: Proc NAACL; 2025. p. 5069–5096. doi:10.18653/v1/2025.naacl-long.262.
5. Vendrow E, Vendrow J, Madry A, Beery S. GSM8K-Platinum: revealing performance gaps in frontier LLMs [Internet]. Gradient Science; 2025 Mar 6 [cited 2026 Oct 25]. Available from: https://gradientscience.org/gsm8k-platinum/
6. Chang Y, Wang X, Wang J, Wu Y, Yang L, Zhu K, et al. A survey on evaluation of large language models. ACM Trans Intell Syst Technol. 2024;15(3):1–45. doi:10.1145/3641289.
7. Yu H, Gan A, Zhang K, Tong S, Liu Q, Liu Z. Evaluation of retrieval-augmented generation: a survey. arXiv:2405.07437. 2024.
8. Bowman SR, Dahl G. What will it take to fix benchmarking in natural language understanding? In: Proc NAACL; 2021. p. 4843–4855. doi:10.18653/v1/2021.naacl-main.385.
9. Reuel A, Hardy A, Smith C, Lamparth M, Hardy M, Kochenderfer MJ. BetterBench: assessing AI benchmarks, uncovering issues, and establishing best practices. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2411.12990.
10. Bean AM, Kearns RO, Romanou A, Hafner FS, Mayne H, Batzner J, et al. Measuring what matters: construct validity in large language model benchmarks. In: Proc NeurIPS Datasets and Benchmarks Track; 2025. arXiv:2511.04703.
11. Rein D, Hou BL, Stickland AC, Petty J, Pang RY, Dirani J, et al. GPQA: a graduate-level Google-proof Q&A benchmark. In: Proc COLM; 2024. arXiv:2311.12022.
12. Arora RK, Wei J, Hicks RS, Bowman P, Quiñonero-Candela J, Tsimpourlas F, et al. HealthBench: evaluating large language models towards improved human health. arXiv:2505.08775. 2025.
13. Center for AI Safety, Scale AI, HLE Contributors Consortium. A benchmark of expert-level academic questions to assess AI capabilities. Nature. 2026;649(8099):1139–1146. doi:10.1038/s41586-025-09962-4.
14. Skarlinski M, Laurent J, Bou A, White A. About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong [Internet]. FutureHouse; 2025 Jul 23 [updated 2025 Sep 16; cited 2026 Oct 25]. Available from: https://www.futurehouse.org/research-announcements/hle-exam
15. Wei J, Karina N, Chung HW, Jiao YJ, Papay S, Glaese A, et al. Measuring short-form factuality in large language models. arXiv:2411.04368. 2024.
16. Li T, Chiang WL, Frick E, Dunlap L, Wu T, Zhu B, et al. From crowdsourced data to high-quality benchmarks: Arena-Hard and BenchBuilder pipeline. In: Proc ICML; 2025. arXiv:2406.11939.
17. Wang Y, Kordi Y, Mishra S, Liu A, Smith NA, Khashabi D, et al. Self-Instruct: aligning language models with self-generated instructions. In: Proc ACL; 2023. p. 13484–13508. doi:10.18653/v1/2023.acl-long.754.
18. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. In: Proc NeurIPS; 2024. arXiv:2404.13076.
19. Saad-Falcon J, Khattab O, Potts C, Zaharia M. ARES: an automated evaluation framework for retrieval-augmented generation systems. In: Proc NAACL; 2024. p. 338–354. doi:10.18653/v1/2024.naacl-long.20.
20. Bai G, Liu J, Bu X, He Y, Liu J, Zhou Z, et al. MT-Bench-101: a fine-grained benchmark for evaluating large language models in multi-turn dialogues. In: Proc ACL; 2024. p. 7421–7454. doi:10.18653/v1/2024.acl-long.401.
21. Gururangan S, Swayamdipta S, Levy O, Schwartz R, Bowman S, Smith NA. Annotation artifacts in natural language inference data. In: Proc NAACL; 2018. p. 107–112. doi:10.18653/v1/N18-2017.
22. Nie Y, Williams A, Dinan E, Bansal M, Weston J, Kiela D. Adversarial NLI: a new benchmark for natural language understanding. In: Proc ACL; 2020. p. 4885–4901. doi:10.18653/v1/2020.acl-main.441.
23. Thakur N, Reimers N, Rücklé A, Srivastava A, Gurevych I. BEIR: a heterogenous benchmark for zero-shot evaluation of information retrieval models. In: Proc NeurIPS Datasets and Benchmarks Track; 2021. arXiv:2104.08663.
24. Gao T, Yen H, Yu J, Chen D. Enabling large language models to generate text with citations. In: Proc EMNLP; 2023. p. 6465–6488. doi:10.18653/v1/2023.emnlp-main.398.
25. Yang X, Sun K, Xin H, Sun Y, Bhalla N, Chen X, et al. CRAG – comprehensive RAG benchmark. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2406.04744.
26. Tang Y, Yang Y. MultiHop-RAG: benchmarking retrieval-augmented generation for multi-hop queries. In: Proc COLM; 2024. arXiv:2401.15391.
27. Yao S, Shinn N, Razavi P, Narasimhan K. τ-bench: a benchmark for tool-agent-user interaction in real-world domains. In: Proc ICLR; 2025. arXiv:2406.12045.
28. Mazeika M, Phan L, Yin X, Zou A, Wang Z, Mu N, et al. HarmBench: a standardized evaluation framework for automated red teaming and robust refusal. In: Proc ICML (PMLR 235); 2024. p. 35181–35224. arXiv:2402.04249.
29. Röttger P, Kirk H, Vidgen B, Attanasio G, Bianchi F, Hovy D. XSTest: a test suite for identifying exaggerated safety behaviours in large language models. In: Proc NAACL; 2024. p. 5377–5400. doi:10.18653/v1/2024.naacl-long.301.
30. Cui J, Chiang WL, Stoica I, Hsieh CJ. OR-Bench: an over-refusal benchmark for large language models. In: Proc ICML (PMLR 267); 2025. p. 11515–11542. arXiv:2405.20947.
31. Son G, Lee H, Kim S, Kim S, Muennighoff N, Choi T, et al. KMMLU: measuring massive multitask language understanding in Korean. In: Proc NAACL; 2025. p. 4076–4104. doi:10.18653/v1/2025.naacl-long.206.
32. Singh S, Romanou A, Fourrier C, Adelani DI, Ngui JG, Vila-Suero D, et al. Global MMLU: understanding and addressing cultural and linguistic biases in multilingual evaluation. In: Proc ACL; 2025. p. 18761–18799. doi:10.18653/v1/2025.acl-long.919.
33. OpenAI. Why SWE-bench Verified no longer measures frontier coding capabilities [Internet]. OpenAI; 2026 Feb 23 [cited 2026 Oct 25]. Available from: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
34. Krippendorff K. Reliability in content analysis: some common misconceptions and recommendations. Hum Commun Res. 2004;30(3):411–433. doi:10.1111/j.1468-2958.2004.tb00738.x.
35. Artstein R, Poesio M. Inter-coder agreement for computational linguistics. Comput Linguist. 2008;34(4):555–596. doi:10.1162/coli.07-034-R2.
36. Plank B. The "problem" of human label variation: on ground truth in data, modeling and evaluation. In: Proc EMNLP; 2022. p. 10671–10682. doi:10.18653/v1/2022.emnlp-main.731.
37. Cabitza F, Campagner A, Basile V. Toward a perspectivist turn in ground truthing for predictive computing. Proc AAAI Conf Artif Intell. 2023;37(6):6860–6868. doi:10.1609/aaai.v37i6.25840.
38. Vendrow J, Vendrow E, Beery S, Madry A. Do large language model benchmarks test reliability? arXiv:2502.03461. 2025.
39. Miller E. Adding error bars to evals: a statistical approach to language model evaluations. arXiv:2411.00640. 2024.
40. Card D, Henderson P, Khandelwal U, Jia R, Mahowald K, Jurafsky D. With little power comes great responsibility. In: Proc EMNLP; 2020. p. 9263–9274. doi:10.18653/v1/2020.emnlp-main.745.
41. Zhang H, Da J, Lee D, Robinson V, Wu C, Song W, et al. A careful examination of large language model performance on grade school arithmetic. In: Proc NeurIPS Datasets and Benchmarks Track; 2024. arXiv:2405.00332.
42. White C, Dooley S, Roberts M, Pal A, Feuer B, Jain S, et al. LiveBench: a challenging, contamination-limited LLM benchmark. In: Proc ICLR; 2025. arXiv:2406.19314.
43. Jain N, Han K, Gu A, Li WD, Yan F, Zhang T, et al. LiveCodeBench: holistic and contamination free evaluation of large language models for code. In: Proc ICLR; 2025. arXiv:2403.07974.
44. Epoch AI. SWE-bench Verified [Internet]. Epoch AI Benchmarking Hub; n.d. [cited 2026 Oct 25]. Available from: https://epoch.ai/benchmarks/swe-bench-verified
45. Biderman S, Schoelkopf H, Sutawika L, Gao L, Tow J, Abbasi B, et al. Lessons from the trenches on reproducible evaluation of language models. arXiv:2405.14782. 2024.
46. Voorhees EM. Variations in relevance judgments and the measurement of retrieval effectiveness. Inf Process Manag. 2000;36(5):697–716. doi:10.1016/S0306-4573(00)00010-8.
47. Rebholz-Schuhmann D, Jimeno Yepes AJ, van Mulligen EM, Kang N, Kors J, Milward D, et al. CALBC silver standard corpus. J Bioinform Comput Biol. 2010;8(1):163–179. doi:10.1142/S0219720010004562.
48. Aroyo L, Welty C. Truth is a lie: crowd truth and the seven myths of human annotation. AI Mag. 2015;36(1):15–24. doi:10.1609/aimag.v36i1.2564.
49. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé III H, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86–92. doi:10.1145/3458723.
50. Jain N, Akhtar M, Giner-Miguelez J, Shinde R, Vanschoren J, Vogler S, et al. A standardized machine-readable dataset documentation format for responsible AI. arXiv:2407.16883. 2024.
51. Shankar S, Zamfirescu-Pereira JD, Hartmann B, Parameswaran A, Arawjo I. Who validates the validators? Aligning LLM-assisted evaluation of LLM outputs with human preferences. In: Proc ACM UIST; 2024. doi:10.1145/3654777.3676450.
52. Haas L, Yona G, D'Antonio G, Goldshtein S, Das D. SimpleQA Verified: a reliable factuality benchmark to measure parametric knowledge. arXiv:2509.07968. 2025.
53. Angelopoulos AN, Bates S, Fannjiang C, Jordan MI, Zrnic T. Prediction-powered inference. Science. 2023;382(6671):669–674. doi:10.1126/science.adi6000.
54. Fisch A, Maynez J, Hofer RA, Dhingra B, Globerson A, Cohen WW. Stratified prediction-powered inference for effective hybrid evaluation of language models. In: Proc NeurIPS; 2024. arXiv:2406.04291.
55. Thakur AS, Choudhary K, Ramayapally VS, Vaidyanathan S, Hupkes D. Judging the judges: evaluating alignment and vulnerabilities in LLMs-as-judges. In: Proc GEM² Workshop; 2025. p. 404–430. arXiv:2406.12624.
56. Connor RJ. Sample size for testing differences in proportions for the paired-sample design. Biometrics. 1987;43(1):207–211. doi:10.2307/2531961.
57. Boyeau P, Angelopoulos AN, Li T, Yosef N, Malik J, Jordan MI. AutoEval done right: using synthetic data for model evaluation. In: Proc ICML (PMLR 267); 2025. p. 5276–5290. arXiv:2403.07008.
58. Dorner FE, Nastl VY, Hardt M. Limits to scalable evaluation at the frontier: LLM as judge won't beat twice the data. In: Proc ICLR; 2025. arXiv:2410.13341.
59. Pavlick E, Kwiatkowski T. Inherent disagreements in human textual inferences. Trans Assoc Comput Linguist. 2019;7:677–694. doi:10.1162/tacl_a_00293.
60. Gilardi F, Alizadeh M, Kubli M. ChatGPT outperforms crowd workers for text-annotation tasks. Proc Natl Acad Sci U S A. 2023;120(30):e2305016120. doi:10.1073/pnas.2305016120.
61. Thomas P, Spielman S, Craswell N, Mitra B. Large language models can accurately predict searcher preferences. In: Proc SIGIR; 2024. p. 1930–1940. doi:10.1145/3626772.3657707.
62. Pangakis N, Wolken S, Fasching N. Automated annotation with generative AI requires validation. arXiv:2306.00176. 2023.
