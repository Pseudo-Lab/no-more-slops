# 2026년 10월 기존 PR 정리

열린 PR #1–#15의 내용과 기여 이력을 유지하면서 경로·설명·연결을 통일합니다. 이 문서는 정리 대상과 의존 관계를 기록하며, 병합 실행을 의미하지 않습니다.

## 위치

| PR | 작성자 | 프로젝트 경로 | 보존하는 내용 |
| --- | --- | --- | --- |
| [#1](https://github.com/Pseudo-Lab/no-more-slops/pull/1) | @chewonc | `tracks/auto-paper/projects/research-pipeline/` | 7개 기초 스킬 |
| [#2](https://github.com/Pseudo-Lab/no-more-slops/pull/2) | @bea-kang | `tracks/auto-application/projects/pawstamp/` | 앱 소스·템플릿·서비스 기록 |
| [#3](https://github.com/Pseudo-Lab/no-more-slops/pull/3) | @yongukpark | `tracks/auto-post/projects/phantom-report/` | 프로젝트·주간 제작 스킬·첫 호 |
| [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4) | @YOOHYOJEONG | `tracks/auto-paper/projects/boundary-stability/` | 5개 스킬·논문 |
| [#5](https://github.com/Pseudo-Lab/no-more-slops/pull/5) | @gogoymh | `tracks/auto-post/projects/instagram-production/` | 제작 스킬·예시·하네스 |
| [#6](https://github.com/Pseudo-Lab/no-more-slops/pull/6) | @gogoymh | `tracks/auto-paper/projects/shared-regularization/` | 논문·근거 검증 스킬 |
| [#7](https://github.com/Pseudo-Lab/no-more-slops/pull/7) | @gogoymh | `tracks/auto-application/projects/tonlit/` | 4개 iOS 출시 스킬·출시 기록 |
| [#8](https://github.com/Pseudo-Lab/no-more-slops/pull/8) | @11kkw | `tracks/auto-paper/projects/dcsm-spatial/` | 논문·작성 및 검토 스킬 |
| [#9](https://github.com/Pseudo-Lab/no-more-slops/pull/9) | @darkwingduck-code | `tracks/auto-post/projects/family-reels/` | 2주차 사전 기획·파이프라인 화면 |
| [#10](https://github.com/Pseudo-Lab/no-more-slops/pull/10) | @Woo-Yeol | `tracks/auto-application/projects/oraeorae/` | 10개 서비스 제작·평가 스킬·발표 |
| [#11](https://github.com/Pseudo-Lab/no-more-slops/pull/11) | @darkwingduck-code | `tracks/auto-paper/projects/evidence-tracked-research/` | 이름이 겹친 연구 지침 스킬 |
| [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12) | @chewonc | `tracks/auto-paper/projects/research-pipeline/` | 기초 스킬 개선·5개 후속 스킬 |
| [#13](https://github.com/Pseudo-Lab/no-more-slops/pull/13) | @sooyoung-wind | `tracks/auto-paper/projects/rag-judge-order-bias/` | 연구 초안·발표 HTML |
| [#14](https://github.com/Pseudo-Lab/no-more-slops/pull/14) | @darkwingduck-code | `tracks/auto-paper/projects/skill-studies/` | 연구 설계 논문·해설서·재현 묶음 |
| [#15](https://github.com/Pseudo-Lab/no-more-slops/pull/15) | @darkwingduck-code | `tracks/auto-post/projects/family-reels/` | 1주차 릴스 제작 스킬·영상 링크 |

재사용 스킬은 해당 트랙의 `skills/`로 이동합니다. 결과물은 각 프로젝트의 `outputs/week-01/` 또는 `outputs/week-02/`에 모읍니다. 외부 결과물은 주차 README에서 원래 링크와 접근 조건을 유지합니다. 기존 root README의 개별 제작 안내는 프로젝트 README나 docs로 보관하고 루트는 트랙 안내에 사용합니다.

## 의존 관계와 병합 시점

1. 공통 기여 규칙 PR을 먼저 검토합니다. 기본 브랜치에 반영되어야 새 PR에도 템플릿과 구조 검사 워크플로가 적용됩니다.
2. #1 다음에 #12를 병합합니다. #12는 #1의 스킬을 개선하는 후속 PR이므로 두 기여를 독립 사본으로 취급하지 않습니다. 포크에 있는 두 브랜치의 PR 대상은 현재 모두 `main`입니다.
3. #15 다음에 #9를 병합합니다. #9는 #15 브랜치를 대상으로 합니다. #15 병합 후 #9의 대상이 `main`으로 전환되었는지 확인합니다.
4. 나머지 기여 사이에는 이 정리로 인한 선행 순서가 없습니다.

## 스킬 이름과 범위

#1·#12의 `research-pipeline`은 기존 이름을 유지합니다. #11은 `evidence-tracked-research`로 이름을 바꾸어 출처·비용·주장 검토 중심 지침임을 드러냅니다. 원래 스킬 지침은 보존합니다.

그 외 비슷한 집필·검토 스킬은 입력 형식·연구 단계·검증 목적을 [역할 안내](skill-catalog.md)에 구분합니다. 세 트랙을 합쳐 41개 고유 스킬이 등록 대상이며, 새 사본을 만들기 전에 기존 스킬 개선 여부를 검토합니다.

문서·코드 경로를 바꾸면 설치 명령·상대 링크·워크플로·테스트도 함께 수정합니다. 연구 결과, 저작자, 라이선스, 원본 검증 기록과 결과물 파일의 내용은 유지합니다.
