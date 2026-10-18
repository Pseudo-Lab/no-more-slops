# agent-report-audit

auto-paper 트랙의 [@xiyoon](https://github.com/xiyoon) 기여입니다. 원 PR: [#22](https://github.com/Pseudo-Lab/no-more-slops/pull/22).

도구를 쓰는 AI 에이전트(tool-using agent)가 사용자의 요청을 받아 운영 규칙을 어기는지, 그리고 그 행동을 감독자에게 보고하는지를 측정하는 소규모 실험과 짧은 논문(short paper)입니다. 역할별 AI 에이전트가 초안과 근거를 만들고, 연구 질문·실험 범위·투고 같은 핵심 판단은 연구 책임자(사람)가 내립니다.

- 대상 모델과 실험 규모: 워커 10개(7개 개발사)를 업무 장면 12개로 선별한 뒤, 선택한 모델·제공사 5쌍과 거부 확인 3개로 본 실험 962건(중복 제거 후)과 선별 111건을 실행
- 판정 방식: 규칙으로 정할 수 있는 항목은 코드로, 자유 서술 보고는 서로 다른 계열의 AI 판정자 2명 + 불일치 시 3번째 판정자로 판정합니다. LLM 판정자 Claude Opus 5.5와 GPT-6.1 Sol이 전 항목을 판정하고(원시 일치 96%, κ 0.93), 불일치는 Gemini 3.1 Pro 다수결. 같은 판정자 반복 판정 50/50 일치, 두 판정자 합의 항목 재점검에서 인정 라벨 0/41 불일치. 사람 검증은 하지 않음

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [paper-readability-pass](../../skills/paper-readability-pass/SKILL.md) | 빌드된 짧은 논문 PDF의 가독성을 회차마다 점검합니다. 채택 논문 구조 비교, 원고만 읽는 새 리뷰어, 글·캡션만 고치는 수정, 렌더링 쪽 확인을 반복합니다. 숫자·결과 대조는 하지 않습니다. |

## 주차별 결과물

- [Week 02](outputs/week-02/README.md): 원고 PDF, 운영 방식 요약, 가독성 점검 스킬

Week 01에는 공개 결과물이 없습니다. 주제 선정과 예비 실험을 비공개 작업 공간에서 진행했습니다.

## 실행 방법

- 작업 공간 구조, 역할별 에이전트, 사람 승인 게이트, AI 판정 운용 원칙: [docs/pipeline.md](docs/pipeline.md)
- 가독성 점검 스킬: [SKILL.md](../../skills/paper-readability-pass/SKILL.md)의 입력 표대로 `pdf`, `source`, `venue`, `page_limit`, `review_out`을 지정해 Claude Code에서 실행합니다. 렌더링 확인에는 poppler의 `pdftoppm`이 필요합니다.
- 실험 코드·결과 로그·LaTeX 소스는 투고 심사가 끝날 때까지 공개하지 않습니다. 이 저장소만으로는 실험을 재현할 수 없습니다.
