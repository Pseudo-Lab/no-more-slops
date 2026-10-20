# agent-report-audit

auto-paper 트랙의 [@xiyoon](https://github.com/xiyoon) 기여입니다. 원 PR: [#22](https://github.com/Pseudo-Lab/no-more-slops/pull/22).

도구를 쓰는 AI 에이전트가 사용자 요청으로 운영 규칙을 어겼을 때, 감독자에게 보내는 보고서가 그 위반을 밝히는지 측정한 짧은 논문입니다. 역할별 AI 에이전트가 초안과 근거를 만들고, 연구 질문·실험 범위·투고는 사람이 정합니다.

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [paper-readability-pass](../../skills/paper-readability-pass/SKILL.md) | 빌드된 짧은 논문 PDF를 회차마다 새 리뷰어에게 읽히고, 숫자는 그대로 둔 채 글과 캡션만 고칩니다. |

## 주차별 결과물

- [Week 02](outputs/week-02/README.md): 원고 PDF, 가독성 점검 스킬

## 실행 방법

- 에이전트 구성과 승인 게이트: [docs/pipeline.md](docs/pipeline.md)
- 스킬 사용법: [SKILL.md](../../skills/paper-readability-pass/SKILL.md)
- 실험 코드와 결과 로그는 투고 심사가 끝난 뒤 공개 여부를 정합니다.
