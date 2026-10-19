# 정보 추출 항목

4단계에서 포함 논문마다 아래 항목을 뽑는다. 1차 추출은 제목·초록만 쓴다. 초록에 없는 항목은 `null`로 두고 추측하지 않는다. 분류 체계는 이 표를 모은 뒤 [범위 정의](scope.md)의 초안을 다시 다듬어 확정한다.

## 항목

| 필드 | 형식 | 내용 |
| --- | --- | --- |
| `key` | 문자열 | `candidates.csv`의 키 |
| `contribution` | 목록 | 주된 기여. `method`(판정 방식 제안), `analysis`(신뢰성·편향 분석), `training`(판정 모델 학습·개선), `benchmark`(판정 벤치마크·메타평가), `application`(분야 적용·검증), `security`(공격·방어), `survey`(서베이·포지션) |
| `judge_format` | 목록 | `pointwise`(점수), `pairwise`(쌍비교), `listwise`(순위), `binary`(합격·불합격), `rubric`(루브릭 기반), `reference`(정답 참조), `critique`(서술형 비평) |
| `judge_setup` | 목록 | `single`(단일 판정 모델), `ensemble`(여러 모델 집계·배심원), `debate`(토론·다중 에이전트), `reasoning`(추론·사고 과정 판정), `agent`(도구 사용 에이전트 판정), `finetuned`(판정 전용 학습 모델) |
| `judge_models` | 목록 | 초록에 이름이 나온 판정 모델 (예: GPT-4o, Claude 3.5 Sonnet, Prometheus 2) |
| `domain` | 목록 | `general`, `code`, `math`, `medical`, `legal`, `education`, `science`, `finance`, `ir_rag`(검색·RAG), `dialogue`, `summarization`, `translation`, `safety`, `agent`, `multimodal`, `creative`, `other` |
| `language` | 목록 | 다룬 언어. 영어만이면 `["en"]`, 다국어면 언어 코드 나열 또는 `multilingual` |
| `human_comparison` | 객체 | `{"done": true/false, "metric": ["spearman", "pearson", "kendall", "kappa", "accuracy", "agreement", ...], "reported": "초록에 나온 수치 그대로"}` |
| `biases` | 목록 | 다룬 편향·실패 유형: `position`, `verbosity`, `self_preference`, `authority`, `sycophancy`, `inconsistency`, `prompt_sensitivity`, `leakage`, `adversarial`, `other` |
| `mitigation` | 목록 | 제안한 개선책: `swap`(순서 교환), `calibration`, `ensemble`, `fine_tuning`, `rubric`, `cot`, `reference`, `other` |
| `finding` | 문자열 | 주요 결과 한 문장 (한국어, 초록에 있는 내용만) |
| `taxonomy_note` | 문자열 | 위 항목으로 담기 어려운 특징 (선택) |

## 결과 기록 형식

배치마다 JSONL 한 줄에 논문 하나씩 기록한다. 결과 파일은 `data/extraction/results/<batch>.jsonl`이다.

```json
{"key": "arxiv:2306.05685", "contribution": ["benchmark", "analysis"], "judge_format": ["pairwise", "pointwise"], "judge_setup": ["single"], "judge_models": ["GPT-4"], "domain": ["general", "dialogue"], "language": ["en"], "human_comparison": {"done": true, "metric": ["agreement"], "reported": "GPT-4 판정이 전문가·크라우드 선호와 80% 넘게 일치"}, "biases": ["position", "verbosity", "self_preference"], "mitigation": ["swap", "cot", "reference"], "finding": "강한 LLM 판정은 사람 선호와 사람끼리의 일치 수준으로 맞는다.", "taxonomy_note": null}
```
