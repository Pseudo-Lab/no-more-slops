# 학술 영어 문체와 용어 대응

번역 단계에서 참고한다. 대응표는 출발점이다. 원고가 인용한 논문의 용어가 이 표와 다르면 인용 논문의 용어를 따른다.

## 목차

1. 문체 규칙
2. 논문 상용 표현
3. 한정 표현의 세기 대응
4. 표기 규칙
5. 분야 공통 용어(실험·통계)
6. 머신러닝·컴퓨터 비전 용어
7. 다른 분야의 원고

## 1. 문체 규칙

- **인칭:** "본 연구는", "우리는", "본 논문에서는"은 "we" 또는 "this work"로 쓴다. 한 원고 안에서 "the authors"와 섞지 않는다.
- **시제:** 수행한 실험과 관찰 결과는 과거형(we measured, was observed), 표·그림이 보여 주는 내용과 일반적 사실, 논문의 구성은 현재형(Table 1 shows, the rule returns)으로 쓴다. 선행연구 소개는 현재형이 기본이다.
- **주어를 앞에:** "~한 결과 ~임을 확인하였다"는 "We find that ..." 또는 결과를 주어로 세운다. "It was confirmed that"으로 시작하지 않는다.
- **명사화를 풀기:** "성능 향상의 달성이 가능하다" → "improves performance". "~에 대한 분석을 수행하였다" → "we analyze".
- **문장 나누기:** 한국어의 "~하며, ~하고, ~하였다" 연쇄는 두세 문장으로 나누거나 세미콜론으로 묶는다.
- **나열:** 가운뎃점(·)과 빗금 나열은 쉼표와 "and"로 푼다. "2·3단계" → "2- and 3-step".
- **복합 수식어의 하이픈:** 명사 앞에서 꾸밀 때 붙인다. "training-free method", "32-step trajectory", "per-video stopping step". 서술어 위치에서는 붙이지 않는다.
- **관사:** 처음 소개하는 개념은 a/an, 다시 가리킬 때와 유일한 대상은 the. 방법 이름과 데이터셋 이름에는 관사를 붙이지 않는다.
- **과장 금지:** 원문에 없는 "novel", "significantly", "state-of-the-art", "remarkably"를 넣지 않는다. "significant"는 통계적 유의성을 뜻할 때만 쓴다.

## 2. 논문 상용 표현

| 한국어 | 영어 |
|---|---|
| 본 연구는 ~를 제안한다 | We propose ... |
| ~를 검토한다 / 분석한다 / 평가한다 | We examine / analyze / evaluate ... |
| ~에 초점을 맞춘다 | We focus on ... |
| ~와 달리 | Unlike ..., / In contrast to ... |
| 반면 / 반대로 | In contrast, / Conversely, |
| 따라서 | Therefore, / Thus, / We therefore ... |
| 다만 / 그러나 | However, |
| ~로 정의한다 / 표시한다 | We define ... as / We denote by ... |
| 다음과 같다 | is given by / can be written as follows |
| 여기서 ~는 | Here, ... / where ... |
| ~를 기준으로 / ~ 대비 | relative to ... / over ... / compared with ... |
| ~를 구분한다 | We distinguish between A and B |
| ~에 한정된다 | is limited to ... |
| ~를 주장하지 않는다 | We do not claim ... |
| 기여 | contribution |
| 한계 | limitation |
| 향후 연구 | future work |
| 선행 연구 / 관련 연구 | prior work / related work |

## 3. 한정 표현의 세기 대응

원문의 세기와 같은 줄의 표현을 고른다. 위아래 줄로 옮기지 않는다.

| 세기 | 한국어 | 영어 |
|---|---|---|
| 단정 | ~이다, ~를 보였다, ~를 확인하였다 | is, shows, we confirm |
| 관찰 | ~가 관찰되었다, ~로 나타났다 | was observed, we observe |
| 지지 | ~를 지지한다, ~를 시사한다 | supports, suggests, indicates |
| 가능 | ~할 수 있다, ~할 여지가 있다 | can, may, there is room to |
| 부정 한정 | ~를 보장하지 않는다, ~라고 결론 내릴 수 없다 | does not guarantee, does not warrant the conclusion that |
| 미확정 | ~는 확정할 수 없다 | cannot be established |

## 4. 표기 규칙

- 표·그림·식·절: Table 1, Figure 1(캡션과 본문 모두), Eq. (1), Section 3.
- 캡션 머리: "표 1." → "Table 1.", "그림 1." → "Figure 1."
- `%p` → `pp`. 첫 등장에서 "percentage points (pp)".
- "n회", "n개"의 단위 명사는 문맥에 맞는 영어 명사로 쓴다(runs, videos, transitions). 한 자리 수는 철자로 써도 되지만 수치·설정값·표와 대응되는 숫자는 아라비아 숫자를 유지한다.
- 신뢰구간: "95% 신뢰구간(CI)" → "95% confidence interval (CI)". 이후 "CI".
- 범위는 en dash(2.5–97.5%), 음수는 원문의 기호(−)를 그대로 둔다.
- 인용 표기 "(Hwang et al., 2025)", "Hwang et al. (2025)" 형식과 참고문헌 항목은 수정하지 않는다.
- 약어는 처음 나올 때 풀어 쓴다. 초록과 본문에서 각각 한 번씩 정의한다.

## 5. 분야 공통 용어(실험·통계)

| 한국어 | 영어 |
|---|---|
| 사전 학습된 / 가중치 고정 | pretrained / with frozen weights |
| 학습 없는 / 재학습 없이 | training-free / without retraining |
| 추론 시간 / 지연 / 실제 시간 | inference time / latency / wall-clock time |
| 계산량 / 계산 비용 | amount of computation / computational cost |
| 정답 / 주석 / 주석자 | ground truth / annotation / annotator |
| 임계값 / 허용 범위 | threshold / tolerance |
| 후처리 / 전처리 | post-processing / preprocessing |
| 검증 집합 / 분할 | validation set / split |
| 대조군 / 대조 실험 | control / control experiment |
| 기준선 | baseline |
| 절제 실험 | ablation study |
| 사후 분석 | post-hoc analysis |
| 사전 조건(사전에 정한 기준) | pre-specified criterion |
| 복원추출 | resampling with replacement |
| 귀무 가정 / 교환 가능 | null hypothesis / exchangeable |
| 순열 / 재배정 | permutation / reassignment |
| 분위수 / 중앙값 | quantile / median |
| 단측 / 양측 | one-sided / two-sided |
| 다중 비교 보정 | correction for multiple comparisons |
| 정확도–시간 교환 | accuracy–time trade-off |
| 재현 | reproduction |
| 일반화 | generalization |
| 경험적 근거 | empirical evidence |

## 6. 머신러닝·컴퓨터 비전 용어

| 한국어 | 영어 |
|---|---|
| 확산 모델 / 잡음 제거 단계 | diffusion model / denoising step |
| 시간표(추론 단계 배치) | (timestep) schedule |
| 시간표를 재구성한 k단계 | respaced k-step |
| 생성 경로 / 궤적 | sampling trajectory |
| 조기 종료 / 적응적 종료 | early stopping (early exit) / adaptive stopping |
| 조건 충실도 | condition fidelity |
| 잡음 예측 | noise prediction |
| 잠재 | latent |
| 특징 / 표현 | feature / representation |
| 주의(메커니즘) | attention |
| 다중 출구 | multi-exit |
| 희소화 / 가지치기 | sparsification / pruning |
| 일반 사건 경계 검출 | generic event boundary detection (GEBD) |
| 경계 / 구간 | boundary / segment |
| 일대일 대응 / 할당 | one-to-one matching / assignment |
| 균등 추출 | uniform sampling |
| 영상별 | per-video |
| 배치 크기 1 | batch size 1 |

## 7. 다른 분야의 원고

이 표에 없는 분야(의학, 화학, 사회과학 등)의 원고는 표를 억지로 적용하지 않는다. 원고의 참고문헌 제목과 인용 논문 초록에서 용어를 수집해 그 원고용 용어집을 먼저 만든다. 분야 표준 보고 지침이 있는 경우(예: 임상 연구의 군·중재·결과 지표 명칭)에는 그 지침의 용어를 따른다.
