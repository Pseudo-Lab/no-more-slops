# 정보 추출 항목

4단계에서는 포함 논문마다 두 가지를 기록한다.

- **PMDRL 요약**: Who, Problem, Method, Data, Result, Limitation, Gap. 논문별 서술과 관련 연구 표의 재료가 된다.
- **분류 코드**: 정해진 값 중에서 고른다. 분류 체계와 통계의 재료가 된다.

1차 추출에는 제목과 초록만 쓴다. 초록에 없는 내용은 `null`로 두고 추측하지 않는다. 분류 체계는 이 결과를 모은 뒤 [범위 정의](scope.md)의 초안을 다시 다듬어 확정한다.

## PMDRL 요약

모두 한국어로 쓰고, 고유명사(모델·데이터셋·지표 이름)는 원문 표기를 따른다.

| 필드 | 작성 주체 | 내용 |
| --- | --- | --- |
| `who` | 스크립트 | 첫 저자 외, 연도, 게재처. `candidates.csv`에서 채우며 서브에이전트는 쓰지 않는다 |
| `problem` | 서브에이전트 | 풀려는 문제 1–2문장 |
| `method` | 서브에이전트 | 제안하거나 사용한 판정 방식·분석 방법 1–2문장 |
| `data` | 서브에이전트 | 사용한 데이터셋·벤치마크·과제, 판정 모델과 평가 대상 모델. 이름이 없으면 초록에 나온 범위만 쓴다 |
| `result` | 서브에이전트 | 주요 결과 1–2문장. 초록에 수치가 있으면 그대로 옮긴다 |
| `limitation` | 서브에이전트 | 논문이 스스로 밝힌 한계. 없으면 `null` |
| `gap` | 서브에이전트 | 논문이 지적한 기존 연구의 공백(연구 동기). 없으면 `null` |

## 분류 코드

| 필드 | 형식 | 값 |
| --- | --- | --- |
| `contribution` | 목록 | 주된 기여. `method`(판정 방식 제안), `analysis`(신뢰성·편향 분석), `training`(판정 모델 학습·개선), `benchmark`(판정 벤치마크·메타평가), `application`(분야 적용·검증), `security`(공격·방어), `survey`(서베이·포지션) |
| `judge_format` | 목록 | `pointwise`(점수), `pairwise`(쌍비교), `listwise`(순위), `binary`(합격·불합격), `rubric`(루브릭 기반), `reference`(정답 참조), `critique`(서술형 비평) |
| `judge_setup` | 목록 | `single`(단일 판정 모델), `ensemble`(여러 모델 집계·배심원), `debate`(토론·다중 에이전트), `reasoning`(추론·사고 과정 판정), `agent`(도구 사용 에이전트 판정), `finetuned`(판정 전용 학습 모델) |
| `judge_models` | 목록 | 초록에 이름이 나온 판정 모델 (예: GPT-4o, Claude 3.5 Sonnet, Prometheus 2) |
| `domain` | 목록 | `general`, `code`, `math`, `medical`, `legal`, `education`, `science`, `finance`, `ir_rag`(검색·RAG), `dialogue`, `summarization`, `translation`, `safety`, `agent`, `multimodal`, `creative`, `other` |
| `language` | 목록 | 다룬 언어. 영어만이거나 언급이 없으면 `["en"]`, 다국어면 언어 코드 나열 또는 `multilingual` |
| `human_comparison` | 객체 | `{"done": true/false, "metric": ["spearman", "pearson", "kendall", "kappa", "accuracy", "agreement", ...], "reported": "초록에 나온 수치 그대로 또는 null"}` |
| `biases` | 목록 | 다룬 편향·실패 유형: `position`, `verbosity`, `self_preference`, `authority`, `sycophancy`, `inconsistency`, `prompt_sensitivity`, `leakage`, `adversarial`, `other` |
| `mitigation` | 목록 | 제안한 개선책: `swap`(순서 교환), `calibration`, `ensemble`, `fine_tuning`, `rubric`, `cot`, `reference`, `other` |
| `taxonomy_note` | 문자열 | 위 항목으로 담기 어려운 특징 (선택) |
| `scope_doubt` | 참·거짓 | 초록상 LLM 판정 연구로 보기 어려우면 `true`. 전문 검토에서 포함 여부를 다시 본다 (선택, 기본 `false`) |

해당 없는 목록은 `[]`로 둔다.

## 결과 기록 형식

배치마다 JSONL 한 줄에 논문 하나씩 기록한다. 결과 파일은 `data/extraction/results/<batch>.jsonl`이다. `app/extract.py collect`가 결과를 검사하고 `who`를 붙여 `data/extraction.jsonl`로 합친다.

```json
{"key": "arxiv:2306.05685",
 "pmdrl": {"problem": "개방형 대화 응답을 사람 대신 강한 LLM이 평가할 수 있는지 불분명하다.",
           "method": "GPT-4를 판정 모델로 써서 쌍비교·점수 판정을 하고, 위치·길이·자기선호 편향과 완화책을 분석한다.",
           "data": "MT-Bench(다중 턴 질문 80개), Chatbot Arena 크라우드 투표",
           "result": "GPT-4 판정은 통제·크라우드 사람 선호와 80% 넘게 일치해 사람끼리의 일치 수준에 이른다.",
           "limitation": "위치·길이·자기선호 편향과 제한된 추론 능력이 남는다.",
           "gap": "기존 벤치마크는 LLM 기반 대화 모델에 대한 사람 선호를 측정하지 못한다."},
 "codes": {"contribution": ["benchmark", "analysis"], "judge_format": ["pairwise", "pointwise"],
           "judge_setup": ["single"], "judge_models": ["GPT-4"], "domain": ["general", "dialogue"],
           "language": ["en"],
           "human_comparison": {"done": true, "metric": ["agreement"], "reported": "over 80% agreement"},
           "biases": ["position", "verbosity", "self_preference"], "mitigation": ["swap", "cot", "reference"],
           "taxonomy_note": null}}
```

결과 파일에서는 한 줄에 한 편씩 쓴다. 위 예시는 읽기 쉽게 줄을 나눴다.

## 1차 추출 기록 (e1·e2·fix)

- 대상: 선별 포함 2,325편 전체
- 추출자: Claude Code 서브에이전트 (Sonnet). 시범 배치 1개(e1-01, 70편)를 먼저 검토한 뒤 e1 33개(70편), e2 13개(약 66편)를 병렬로 돌렸다.
- 점검: `extract.py collect`가 형식(허용값·필수 항목), 배치 안 반복 문장(10% 초과), 배치 간 공유 문장을 검사했다. 반복 경고가 난 배치는 서브에이전트가 논문별로 다시 썼다. 최종 결과 형식 오류 0건.
- 초록 보완: 초록이 없거나 300자 미만인 64편은 `extract.py fill`로 arXiv·OpenAlex·Semantic Scholar에서 다시 찾았다. 4편만 찾아 fix 배치로 다시 추출했다. 병렬 실행 중 Semantic Scholar가 요청 제한(429)을 자주 걸어, e2부터는 서브에이전트가 직접 내려받지 않게 했다.
- 결과: 추출 2,325편, 제목만으로 쓴 기록 59편, `scope_doubt` 170편. 두 집단은 r5로 다시 선별했다([선별 기준](screening.md)의 5차 라운드). 재선별과 중복 제외 후 종합 대상은 2,200편이다.
- 메타데이터 문제: 같은 논문이 두 키로 들어간 사례 20편은 E7로 제외했다. 다른 논문의 초록이 붙은 사례(doi:10.1016/j.bas.2026.106844)는 제목 기준으로 추출했다.
