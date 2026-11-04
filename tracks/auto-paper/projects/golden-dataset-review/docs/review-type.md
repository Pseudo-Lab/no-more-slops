# 리뷰 유형 결정: survey가 아니라 mini review

## 질문

이전 작업(`auto-paper/llm-as-judge-survey` 브랜치)은 2023–2026년 문헌 2,185편을 망라한 서베이였다. 이번에는 4쪽 분량으로 한 주제(평가용 골든 데이터셋의 구축·검증·기준)에 집중한다. 이 경우에도 "survey review"가 맞는가?

## 결론

**맞지 않다. Mini review(초점 리뷰)가 맞다.**

| 구분 | Survey / comprehensive review | Systematic·scoping review | Mini review |
| --- | --- | --- | --- |
| 목적 | 분야 전체를 망라하고 분류 체계 제시 | 정해진 질문에 대해 재현 가능한 검색·선별·추출 | 좁은 주제의 최근 발전을 종합하고 쟁점·공백 제시 |
| 분량 | 수십 쪽, 참고문헌 수백 편 | 보고 지침(PRISMA, PRISMA-ScR)이 분량을 좌우 | 3,000단어 내외, 그림·표 2개 이내 |
| 방법 절 | 선택 | 필수(검색식, 흐름도, 선별 기준) | 문헌 확인 방법을 짧게 서술 |
| 이번 작업과의 적합성 | 분량 초과 | 4쪽 안에 흐름도·검색 기록이 들어가지 않음 | 적합 |

- 근거: Frontiers in Artificial Intelligence / Frontiers in Big Data의 article types 페이지는 Mini Review를 "현재 연구 영역의 초점이 맞춰진 측면과 최근 발전을 다루는" 동료 심사 논문으로 정의하고, 최대 3,000단어, 그림·표 2개 이내, Abstract → Introduction → 주제별 소절 → Discussion 구조를 요구한다. Discussion에는 서로 다른 학파·논쟁, 현재 연구 공백, 향후 발전 방향이 들어가야 한다. 미발표 자료는 넣을 수 없다. (2026-10-25 확인, [research/r1-definition-format.md](../research/r1-definition-format.md) Part B)
- "특정 도메인 집중"은 이번 리뷰에서 **LLM·RAG 애플리케이션 평가용 골든 데이터셋**으로 한정했다(사용자 선택, 2026-10-25).

## 적용한 형식

- 기준 학술지 형식: Frontiers Mini Review (본문 단어 제한·그림/표 2개·필수 절 구조·생성형 AI 사용 고지).
- 인용 방식: 번호식(Vancouver). Frontiers는 학술지에 따라 Harvard 또는 Vancouver를 쓴다. 4쪽 2단 조판에서 본문 길이를 줄이기 위해 번호식을 택했다.
- 조판: A4 2단, 참고문헌 포함 4쪽. 국문 초록과 영문 초록을 함께 둔다(국내 학술지 관행).
- 언어: 한국어.
