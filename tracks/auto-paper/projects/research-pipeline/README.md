# research-pipeline

Auto-Paper 트랙의 [chewonc](https://github.com/chewonc) 기여입니다. 원 PR: [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12).

[1주차 결과물과 검증 범위](outputs/week-01/README.md)를 확인하세요.

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [benchmark-finder](../../skills/benchmark-finder/SKILL.md) | 벤치마크·데이터셋 탐색과 벤치마크 중심 선행연구 기록 |
| [compute-planner](../../skills/compute-planner/SKILL.md) | 사용자의 시간·경험·하드웨어에 따른 연구 계산 비용과 수행 가능성 판단 |
| [experiment-runner](../../skills/experiment-runner/SKILL.md) | 사전에 고정한 단일 논문의 실험 계획 실행과 결과 저장 |
| [paper-results-reviser](../../skills/paper-results-reviser/SKILL.md) | 완료된 결과에 맞춰 기존 논문 주장과 원고 수정 |
| [paper-to-latex](../../skills/paper-to-latex/SKILL.md) | 기존 원고를 내용 보존하여 LaTeX·Overleaf 프로젝트로 변환 |
| [paper-visuals](../../skills/paper-visuals/SKILL.md) | 기존 원고와 근거에 맞춘 재현 가능한 표·그림 제작 |
| [paper-writer](../../skills/paper-writer/SKILL.md) | 단일 연구 계획의 실험 전·후 전체 원고 작성 |
| [prior-work-checker](../../skills/prior-work-checker/SKILL.md) | 벤치마크 기반 연구 질문의 선행연구 중복·신규성 확인 |
| [research-pipeline](../../skills/research-pipeline/SKILL.md) | 연구 질문, 벤치마크, 선행연구, 수행 가능성과 계획을 연결하는 연구 기획 조정 |
| [research-planner](../../skills/research-planner/SKILL.md) | 벤치마크 기반 질문을 실행 가능한 연구 계획으로 구체화 |
| [research-question-parser](../../skills/research-question-parser/SKILL.md) | 파일과 노트에서 연구 질문·아이디어 추출 |
| [research-readiness-advisor](../../skills/research-readiness-advisor/SKILL.md) | 사용자 조건과 논문 완성 가능성을 기준으로 연구 후보 검토 |

같은 이름의 스킬을 주차별로 복사하지 않고 `tracks/auto-paper/skills/`의 기존 스킬을 개선합니다. 비슷한 스킬은 위 입력·역할 범위를 기준으로 선택합니다.

## PR 관계

기초 연구 기획 스킬은 [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1), 실험·집필·변환 단계와 기획 개선은 후속 [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12)에서 제공합니다. #12는 #1의 후속 변경이며 같은 스킬을 별도 사본으로 등록하지 않습니다.
