# 스킬 역할 안내

새 스킬을 만들기 전에 같은 입력·목적·출력을 담당하는 스킬과 열린 PR을 확인합니다. 아래 목록은 최초 정리 PR들의 등록 대상입니다. 링크 대상은 해당 PR이 병합되면 기본 브랜치에 나타납니다. 현재 체크아웃의 실제 목록은 `python3 scripts/check_repository.py --catalog`로 확인합니다. 새 스킬을 추가하거나 범위를 바꿀 때 이 안내도 갱신합니다.

`research-pipeline`은 #1에서 시작해 #12에서 개선되었습니다. 병합 순서에 따라 내용이 달라지지 않도록 공통 개선본을 두 PR에 동일하게 반영합니다. 별도 연구 지침인 #11은 `evidence-tracked-research`로 이름을 구분했습니다. 같은 분야를 다루는 스킬도 입력 형식·단계·검증 목적이 다르면 유지하며, 사용자가 어느 것을 선택할지 위 기준으로 설명합니다.

## Auto-Paper

| 스킬 | 적용 범위 | 최초 정리 PR |
| --- | --- | --- |
| [audit-paper-citations](../tracks/auto-paper/skills/audit-paper-citations/SKILL.md) | 인용 문장·참고문헌과 원문의 부합성을 검사합니다. | [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4) |
| [benchmark-finder](../tracks/auto-paper/skills/benchmark-finder/SKILL.md) | 연구 질문에 맞는 공개 벤치마크와 평가 기준을 찾습니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [compute-planner](../tracks/auto-paper/skills/compute-planner/SKILL.md) | 사용 가능한 계산 자원과 기간 안에서 실험 가능성을 판단합니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [draft-conference-paper](../tracks/auto-paper/skills/draft-conference-paper/SKILL.md) | 실험 전 학회 논문의 Abstract·Introduction·Related Work를 작성합니다. | [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4) |
| [evidence-driven-paper](../tracks/auto-paper/skills/evidence-driven-paper/SKILL.md) | 공정한 비교·기여 귀속·근거 중심 집필과 쌍별 결과 검증 하네스를 제공합니다. | [#6](https://github.com/Pseudo-Lab/no-more-slops/pull/6) |
| [evidence-tracked-research](../tracks/auto-paper/skills/evidence-tracked-research/SKILL.md) | 출처·비용·독립 주장 검토·스킬 개선 근거를 관리하는 연구 지침. 연구 계획 조합과 구분합니다. | [#11](https://github.com/Pseudo-Lab/no-more-slops/pull/11) |
| [experiment-report-to-paper](../tracks/auto-paper/skills/experiment-report-to-paper/SKILL.md) | 완료된 실험 Markdown 보고서를 학회 형식 Word 논문으로 작성합니다. | [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4) |
| [experiment-runner](../tracks/auto-paper/skills/experiment-runner/SKILL.md) | 확정한 계획에 따라 대조군을 갖춘 실험 실행을 지원합니다. | [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [experiment-to-paper](../tracks/auto-paper/skills/experiment-to-paper/SKILL.md) | 저장된 JSON 실험 결과를 근거 표로 내보내고 원고를 작성합니다. | [#8](https://github.com/Pseudo-Lab/no-more-slops/pull/8) |
| [paper-results-reviser](../tracks/auto-paper/skills/paper-results-reviser/SKILL.md) | 완료된 실험 결과와 원고의 주장·수치를 대조하고 수정합니다. | [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [paper-review-local](../tracks/auto-paper/skills/paper-review-local/SKILL.md) | 로컬 원고·인용 키·그림·PDF 및 텍스트 중복을 검사합니다. | [#8](https://github.com/Pseudo-Lab/no-more-slops/pull/8) |
| [paper-to-latex](../tracks/auto-paper/skills/paper-to-latex/SKILL.md) | 원고를 LaTeX 프로젝트로 변환하고 내용·빌드 결과를 검사합니다. | [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [paper-visuals](../tracks/auto-paper/skills/paper-visuals/SKILL.md) | 논문에 필요한 도표와 시각 자료를 구성합니다. | [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [paper-writer](../tracks/auto-paper/skills/paper-writer/SKILL.md) | 하나의 연구 프로젝트를 실험 전·후 원고로 구성합니다. | [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [prior-work-checker](../tracks/auto-paper/skills/prior-work-checker/SKILL.md) | 기존 연구와의 중복·참신성·SOTA 비교 조건을 확인합니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [research-pipeline](../tracks/auto-paper/skills/research-pipeline/SKILL.md) | 연구 질문·벤치마크·선행연구·계산 예산을 연결하는 연구 흐름 조합. #12에서 실험·집필 단계로 확장합니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [research-planner](../tracks/auto-paper/skills/research-planner/SKILL.md) | 질문을 비교 기준과 실행 가능한 연구 계획으로 구체화합니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [research-question-parser](../tracks/auto-paper/skills/research-question-parser/SKILL.md) | 문서에서 연구 질문과 검증 가능한 가설을 추출합니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [research-readiness-advisor](../tracks/auto-paper/skills/research-readiness-advisor/SKILL.md) | 연구 계획의 준비 상태와 진행 조건을 검토합니다. | [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) · [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) |
| [research-related-work](../tracks/auto-paper/skills/research-related-work/SKILL.md) | 선행연구의 출처와 BibTeX를 정리합니다. | [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4) |
| [translate-paper-to-english](../tracks/auto-paper/skills/translate-paper-to-english/SKILL.md) | 한국어 Word 논문을 구조를 보존한 영문 Word로 번역합니다. | [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4) |

## Auto-Application

| 스킬 | 적용 범위 | 최초 정리 PR |
| --- | --- | --- |
| [app-design-review](../tracks/auto-application/skills/app-design-review/SKILL.md) | 네이티브 앱의 디자인 토큰·시각 요소·실제 상호작용을 검토합니다. | [#7](https://github.com/Pseudo-Lab/no-more-slops/pull/7) |
| [app-store-release](../tracks/auto-application/skills/app-store-release/SKILL.md) | iOS 앱의 스토어 메타데이터·스크린샷·심사 제출 묶음을 준비합니다. | [#7](https://github.com/Pseudo-Lab/no-more-slops/pull/7) |
| [constitution-first](../tracks/auto-application/skills/constitution-first/SKILL.md) | 서비스의 개발 원칙과 사람의 의사결정 경계를 먼저 정합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [core-feature-with-review](../tracks/auto-application/skills/core-feature-with-review/SKILL.md) | 핵심 기능에 사람이 결과를 확인하는 단계를 포함합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [env-split](../tracks/auto-application/skills/env-split/SKILL.md) | 개발·운영 환경과 비밀 설정을 분리합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [glance-and-guardrails](../tracks/auto-application/skills/glance-and-guardrails/SKILL.md) | 웹 서비스의 정보 위계와 파괴적 동작·사용량 보호 장치를 정리합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [global-localization](../tracks/auto-application/skills/global-localization/SKILL.md) | 앱의 언어별 문자열·레이아웃·지역 기본값을 점검합니다. | [#7](https://github.com/Pseudo-Lab/no-more-slops/pull/7) |
| [ios-verify-harness](../tracks/auto-application/skills/ios-verify-harness/SKILL.md) | iOS 시뮬레이터·기기 동작과 무반응 상호작용을 검증합니다. | [#7](https://github.com/Pseudo-Lab/no-more-slops/pull/7) |
| [launch-basics](../tracks/auto-application/skills/launch-basics/SKILL.md) | 웹 서비스의 공개 준비·법적 표기·계정 삭제·퍼널을 점검합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [micro-saas-audit](../tracks/auto-application/skills/micro-saas-audit/SKILL.md) | 위 단계의 산출물을 증거에 따라 평가합니다. 현재 스크립트에는 오래오래 전용 경로가 포함됩니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [micro-saas-week](../tracks/auto-application/skills/micro-saas-week/SKILL.md) | 서비스 제작 단계 스킬을 연결하는 주간 조합 스킬입니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [model-bakeoff](../tracks/auto-application/skills/model-bakeoff/SKILL.md) | 같은 입력으로 후보 모델을 비교해 품질·비용을 확인합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [ship-loop](../tracks/auto-application/skills/ship-loop/SKILL.md) | 단계마다 변경·검증·배포 기록을 반복합니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |
| [skeleton-on-prod](../tracks/auto-application/skills/skeleton-on-prod/SKILL.md) | 운영 환경에서 동작하는 서비스 골격을 먼저 만듭니다. | [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) |

## Auto-Post

| 스킬 | 적용 범위 | 최초 정리 PR |
| --- | --- | --- |
| [design-punctuation](../tracks/auto-post/skills/design-punctuation/SKILL.md) | 제목·캡션 같은 짧은 시각 문구의 불필요한 끝마침표를 정리합니다. 다른 트랙에서도 링크로 재사용합니다. | [#5](https://github.com/Pseudo-Lab/no-more-slops/pull/5) |
| [family-reel-meme-preflight](../tracks/auto-post/skills/family-reel-meme-preflight/SKILL.md) | 릴스 편집 전에 국가·플랫폼별 밈 근거와 아기 안전을 선별합니다. | [#9](https://github.com/Pseudo-Lab/no-more-slops/pull/9) |
| [instagram-content](../tracks/auto-post/skills/instagram-content/SKILL.md) | 계정 설정과 출처를 바탕으로 캐러셀·프로필·무음 인포그래픽 릴스를 제작합니다. JSON 장면과 도식에서 시작하며, 촬영 영상 중심의 `instagram-reel` 편집과 구분합니다. | [#5](https://github.com/Pseudo-Lab/no-more-slops/pull/5) |
| [instagram-reel](../tracks/auto-post/skills/instagram-reel/SKILL.md) | 가족 촬영 영상을 세로 릴스로 편집하고 자막·음량·화질을 확인합니다. | [#9](https://github.com/Pseudo-Lab/no-more-slops/pull/9) · [#15](https://github.com/Pseudo-Lab/no-more-slops/pull/15) |
| [phantom-images](../tracks/auto-post/skills/phantom-images/SKILL.md) | Phantom Report의 프로젝트 규칙에 맞춘 사건 이미지와 캐러셀을 제작합니다. | [#3](https://github.com/Pseudo-Lab/no-more-slops/pull/3) |
| [phantom-weekly](../tracks/auto-post/skills/phantom-weekly/SKILL.md) | Phantom Report의 주간 수집·사실 확인·집필·이미지 제작을 조합합니다. | [#3](https://github.com/Pseudo-Lab/no-more-slops/pull/3) |
