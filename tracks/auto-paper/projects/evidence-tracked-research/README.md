# evidence-tracked-research

Auto-Paper 트랙의 [darkwingduck-code](https://github.com/darkwingduck-code) 기여입니다. 원 PR: [#11](https://github.com/Pseudo-Lab/no-more-slops/pull/11).

[1주차 결과물과 검증 범위](outputs/week-01/README.md)를 확인하세요.

2026-10-18 개정은 세 연구의 평가 경계, 원문 기반 방법 비교, 정량 그림, 원고·동일 버전 해설의 연결, 공개 저술 관점의 주석과 스킬 후보 평가 규칙을 반영합니다. 로컬 활성 스킬을 변경하거나 새 모델 실험을 수행한 결과가 아닙니다.

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [evidence-tracked-research](../../skills/evidence-tracked-research/SKILL.md) | 출처·예산·주장 검토와 스킬 개선 후보 평가를 연결하는 연구 실행 지침 |

같은 이름의 스킬을 주차별로 복사하지 않고 `tracks/auto-paper/skills/`의 기존 스킬을 개선합니다. 비슷한 스킬은 위 입력·역할 범위를 기준으로 선택합니다.

## 이름과 역할

기존 `research-pipeline` 이름은 벤치마크 중심 연구 기획 스킬과 충돌하여 `evidence-tracked-research`로 바꿨습니다. 원 스킬의 연구 절차와 Research Forge 출처 표기는 유지했습니다.

| 비교한 기존 기여 | 입력·출력·적용 범위의 차이 |
| --- | --- |
| `research-pipeline` · PR #1/#12 | 벤치마크 탐색과 연구 계획 조합이 중심입니다. 이 스킬은 선택된 질문·계획·근거·실행 기록을 받아 평가 권한, 주장 검토, 문서 판본과 후보 개선 상태를 관리합니다. 기존 기획안이나 해당 스킬의 선택 절차를 대체하지 않습니다. |
| `evidence-driven-paper` · PR #6 | 완료 결과와 리뷰로 경험적 논문의 기여 귀속·대조군·집필을 수정합니다. 이 스킬은 그 전후의 입력·소비 코드·노출·비용·판본·스킬 후보 평가까지 잇는 실행 지침이며 별도의 실험 runner나 평가 하네스는 제공하지 않습니다. |

## 관련 PR과 독립 적용

논문 PR [#14](https://github.com/Pseudo-Lab/no-more-slops/pull/14)와 공유하는 파일은 `tracks/auto-paper/skills/evidence-tracked-research/SKILL.md` 하나이며 최종 bytes를 일치시킵니다. 이 PR의 고유 기여는 스킬 사용 범위·기존 스킬 비교·검증 기록입니다. 논문 파일이 없어도 이 지침을 읽고 기존 실행기에 적용할 수 있으며, #14는 이 파일을 함께 포함해 #11의 선행 병합을 요구하지 않습니다. 일반 병합과 squash의 두 순서 검증은 제출 PR의 검증 기록에 남깁니다.

이 기여는 저장소의 MIT License를 따릅니다. This work was created as part of the No-More-Slops group activities at Pseudo Lab.
