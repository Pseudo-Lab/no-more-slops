# Fewshot

- 작성자: @gogoymh
- 트랙: Auto-Application
- 앱: **Fewshot: AI Photo Sorter** (iOS, 번들 ID `com.minhyeong.albumate`, 35개 언어)
- 공개 페이지: <https://goyo-drive.github.io/fewshot/> · [개인정보처리방침](https://goyo-drive.github.io/fewshot/privacy/) · [지원](https://goyo-drive.github.io/fewshot/support/)

## 무엇을 하나요

사진이 수천 장 쌓였지만 정리를 미루는 iPhone 사용자를 위한 앱이다. 내가 정한 클래스(음식, 반려동물, 풍경 등)마다 사진을 5장씩만 직접 분류하면, 기기 안에서 도는 Google EmbeddingGemma 2가 나머지 사진을 그 클래스로 분류한다. 무료 버전은 AI가 고른 사진을 넘기며 검토하고, Pro는 결과가 검토 없이 바로 클래스와 사진 앱 앨범에 들어간다. 사진은 기기 밖으로 나가지 않는다.

## 소스와 실행

앱 소스는 개발자 소유의 비공개 저장소에 있다. 이 폴더에는 주차별 결과물 색인만 둔다. 출시 자동화에 쓴 도구는 아래 스킬로 공개한다.

## 사용한 스킬

- [app-store-connect-api](../../skills/app-store-connect-api/SKILL.md): App Store Connect 설정·상품·업로드·TestFlight를 API로 처리 (Week 02에서 추가)
- `app-store-release`, `global-localization`, `ios-verify-harness`: Tonlit에서 만든 출시·현지화·검증 스킬 ([#7](https://github.com/Pseudo-Lab/no-more-slops/pull/7)). 이 프로젝트에서는 같은 방식으로 스토어 문구·스크린샷·검증을 했으며, 이 PR은 #7이 먼저 병합되지 않아도 적용된다.

## 주차별 결과물

- [Week 02](outputs/week-02/README.md): App Store 제출 직전까지의 출시 준비, TestFlight 빌드, App Store Connect API 스킬

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
