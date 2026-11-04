# Tonlit · Week 1 결과물

- 트랙: Auto-Application
- 작성자: [gogoymh](https://github.com/gogoymh)
- 원본 제출: [PR #7](https://github.com/Pseudo-Lab/no-more-slops/pull/7)
- 전체 제작 기록, 지표와 재현 방법: [프로젝트 README](../../README.md)

## 제출한 결과

Tonlit은 12개 언어를 지원하는 유료 피부톤 보정 iOS 앱이며, 원본 PR에는 2026-10-11 App Store 심사 제출(1.0, 빌드 21)이 기록되어 있다. 공개 App Store URL은 원본에 없으므로 새로 추정하지 않는다.

| 결과물 | 위치 |
|---|---|
| 언어별 스크린샷 예시 | [locale-screenshots.jpg](../../../../skills/app-store-release/assets/locale-screenshots.jpg) |
| 제출용 붙여넣기 시트 예시 | [HTML](../../../../skills/app-store-release/assets/paste-sheet.html), [미리보기](../../../../skills/app-store-release/assets/paste-sheet-preview.jpg) |
| 다국어 탭 겹침 수정 사례 | [tab-overflow-fix.jpg](../../../../skills/global-localization/assets/tab-overflow-fix.jpg) |
| 기능별 무변화 감사 사례 | [noop-audit-sample.jpg](../../../../skills/ios-verify-harness/assets/noop-audit-sample.jpg) |
| 홈 화면 디자인 전후 | [before-after.jpg](../../../../skills/app-design-review/assets/before-after.jpg) |

위 파일은 재사용 스킬을 설명하는 예제 자산이므로 해당 스킬의 `assets/` 한 곳에 보존한다. 이후 제출하는 앱별 최종 발표 자료, 보고서, 배포 결과 파일은 이 폴더에 두고 기록한다. 원본 스토어 제출물 전체는 공개 저장소에 제출되지 않았다.

## 스킬 역할과 경계

| 원본 스킬 | 맡는 범위 |
|---|---|
| [ios-verify-harness](../../../../skills/ios-verify-harness/SKILL.md) | iOS 화면 진입, 시뮬레이터·실기기 검증, 기능별 렌더 차이 감사 |
| [app-design-review](../../../../skills/app-design-review/SKILL.md) | 네이티브 앱 디자인 토큰과 보이는 상호작용 검토 |
| [global-localization](../../../../skills/global-localization/SKILL.md) | 앱 문자열·지역 기준·언어별 레이아웃과 Xcode 카탈로그 검증 |
| [app-store-release](../../../../skills/app-store-release/SKILL.md) | iOS 스토어 출시 키트, 언어별 제출 자료, 업로드·심사 안내 |

웹 서비스의 정보 우선순위와 삭제·크레딧 가드는 `glance-and-guardrails`, 웹 약관·계정 탈퇴·퍼널·도메인 준비는 `launch-basics`의 범위다. 스킬을 프로젝트 아래로 복사하지 않는다.

## 검증 기록

- 원본 보고: 스토어 12개 언어, 스크린샷 72장, 지원·개인정보·소개 페이지 36개, 문자열 336개 × 11개 언어. 자세한 측정 조건과 제한은 프로젝트 README에 보존했다.
- 정리 후 재검증(2026-10-13): 새 스킬 경로에서 출시 키트 11개, 문자열 카탈로그 11개, iOS 검증 도구 6개 등 기존 테스트 28개가 모두 통과했다. iOS 검증 도구 테스트는 Pillow가 설치된 Python 환경에서 실행했다. 이동한 문서의 상대 링크도 확인했다.
- 이번 정리에서 App Store 심사 상태, 운영 사이트 응답, 실제 기기 설치·빌드 업로드는 다시 확인하지 않았다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
