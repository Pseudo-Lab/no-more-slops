# 오래오래 · Week 1 결과물

- 트랙: Auto-Application
- 작성자: [Woo-Yeol](https://github.com/Woo-Yeol)
- 원본 제출: [PR #10](https://github.com/Pseudo-Lab/no-more-slops/pull/10)
- 전체 제작 기록: [프로젝트 README](../../README.md)
- 제작 기간: 2026-10-07 ~ 10-12

## 제출한 결과

| 결과물 | 위치 |
|---|---|
| 가족 건강검진 기록 서비스 | https://oraeorae.kro.kr |
| 1주차 발표 자료, 15장·5분 | [presentation-week1.pdf](presentation-week1.pdf) |
| 구조와 개발 과정 | [ARCHITECTURE.md](../../ARCHITECTURE.md), [PROCESS.md](../../PROCESS.md) |
| 프로젝트 평가 | [EVALUATION.md](../../EVALUATION.md) |

서비스 소스 코드는 원저자의 비공개 저장소에 유지한다. 추가 발표 자료나 최종 결과 파일은 이 주차 폴더에 두며 건강검진 원본·개인정보·키는 제출하지 않는다. 기존 PDF 파일의 내용은 변경하지 않았다.

## 스킬 역할과 경계

원본 스킬은 모두 Auto-Application 트랙의 `skills/`에 한 번만 등록한다.

| 스킬 | 맡는 범위 |
|---|---|
| [micro-saas-week](../../../../skills/micro-saas-week/SKILL.md) | 단계 스킬을 순서대로 연결하는 조합 |
| [constitution-first](../../../../skills/constitution-first/SKILL.md) | 서비스 시작 전에 원칙과 제외 범위 고정 |
| [skeleton-on-prod](../../../../skills/skeleton-on-prod/SKILL.md) | 로그인·DB·RLS가 있는 첫 운영 뼈대 |
| [launch-basics](../../../../skills/launch-basics/SKILL.md) | 웹 서비스 약관·탈퇴·퍼널·도메인·공개 준비 |
| [core-feature-with-review](../../../../skills/core-feature-with-review/SKILL.md) | AI 핵심 기능과 사람의 확인 흐름 |
| [model-bakeoff](../../../../skills/model-bakeoff/SKILL.md) | 같은 입력·스키마로 모델 비용과 정확도 비교 |
| [glance-and-guardrails](../../../../skills/glance-and-guardrails/SKILL.md) | 웹 정보 우선순위, 삭제 확인, 크레딧 가드 |
| [env-split](../../../../skills/env-split/SKILL.md) | 로컬·운영 환경과 데이터베이스 분리 |
| [ship-loop](../../../../skills/ship-loop/SKILL.md) | 한 기능의 이슈·spec·PR·운영 확인 흐름 |
| [micro-saas-audit](../../../../skills/micro-saas-audit/SKILL.md) | 앞선 단계의 산출물과 증거 평가 |

`launch-basics`는 iOS 스토어 제출 키트를 만드는 `app-store-release`와 역할이 다르다. `glance-and-guardrails`는 네이티브 앱 디자인 토큰을 검토하는 `app-design-review`와 구분한다. 이 프로젝트에는 공용 스킬 복사본을 두지 않는다.

## 검증 기록

- 원본 보고: 평가 통과 25·실패 8·미확인 3, 커밋 53·PR 16·이슈 32·spec 10·스킬 10. 실사용자 모집 전 측정 준비 상태이며 상세 결과는 EVALUATION과 프로젝트 README에 보존했다.
- 정리 후 재검증(2026-10-13): 원본 PDF와 이동한 PDF의 바이트가 같음을 확인했다. 이동한 저장소 문서의 상대 링크와 `micro-saas-audit/scripts/audit.sh`의 셸 문법 검사도 통과했다.
- `audit.sh`는 오래오래의 파일 경로와 운영 구조를 전제로 한 증거 수집기다. 다른 앱에서 쓸 때는 해당 경로를 맞춘다. 이번 정리에서는 비공개 앱 저장소나 운영 서비스를 다시 평가하지 않았다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
