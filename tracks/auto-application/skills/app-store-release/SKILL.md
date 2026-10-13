---
name: app-store-release
description: "iOS 앱을 App Store에 출시할 때 쓴다. 출시 키트(kit.json) 하나로 언어별 스토어 문구 검사, 시뮬레이터 스크린샷, 지원·개인정보 페이지, App Store Connect 붙여넣기 시트, 빌드 업로드를 만들고, App Store Connect 화면을 단계별로 안내한다. '출시 준비해줘', '앱스토어에 뭐라고 넣어', '빌드 올려줘', 스크린샷 크기 오류, 심사 제출 질문에 사용한다. Android·Google Play는 다루지 않는다."
---

# iOS 앱 App Store 출시

앱 하나의 출시 자료를 `kit.json` 하나로 묶어 두고, 아래 단계를 그 키트로 반복한다. 앱 이름, 번들 ID, 언어, 가격, 연락처는 모두 작업별 입력값이며 이 스킬에 기본값으로 들어 있지 않다. 예시는 [references/example](references/example/kit.json)(Tonlit 1.0, 영어·한국어)에 있다.

## 키트 준비

앱 저장소 안에 `docs/app-store/`를 만들고 [references/kit.md](references/kit.md)의 형식으로 `kit.json`, `metadata/<locale>.md`, `site-strings.json`, `review-notes.md`를 둔다. 이미 정한 값(앱 이름, 지원 이메일, 언어, 가격)은 대화에서 가져오고, 없는 값만 묻는다.

- 스토어 언어는 앱이 지원하는 언어를 모두 넣는 것이 기본이다. 언어마다 이름·부제·설명·키워드·스크린샷·지원 페이지를 그 언어로 만든다. 영어 이름을 그대로 두지 않는다.
- 이름은 `브랜드: 하는 일` 형태로 30자 안에서 언어별로 쓴다. 같은 이름의 앱이 이미 있으면 App Store Connect가 거부하므로 후보를 두세 개 준비한다.
- 스토어 문구는 앱 화면의 용어를 그대로 쓴다(앱의 문자열 카탈로그에서 가져온다). 앱에 없는 기능, 의학적 효과, 가격·순위 표현("무료", "최고", "#1")은 쓰지 않는다.
- 기계 번역이면 사용자에게 알리고 원어민 검수 대상으로 표시한다.

## 단계

1. **스토어 문구:** `python3 scripts/check_store_metadata.py kit.json`. 글자 수 한도, 키워드 쉼표 뒤 공백·중복, 이름·부제와 겹치는 키워드를 잡는다. FAIL이 0이 될 때까지 고친다.
2. **스크린샷:** App Store Connect의 스크린샷 칸이 요구하는 크기를 먼저 확인한다(2026-10 기준 필수 칸 "Dynamic Island 지원 iPhone (중형 디스플레이)" = 1206×2622, iPhone 17 Pro 시뮬레이터). 화면마다 DEBUG 실행 인수를 만들어 두고(ios-verify-harness 스킬) `python3 scripts/capture_screenshots.py kit.json --device <UDID>`로 언어별로 찍는다. 전부 열어 보고, 긴 언어에서 글자가 겹치거나 잘린 화면은 앱을 고친 뒤 다시 찍는다(global-localization 스킬).
3. **지원·개인정보·소개 페이지:** `python3 scripts/build_support_site.py build kit.json`. 개인정보 처리방침은 앱 안의 방침, App Store Connect의 개인정보 답변과 같은 내용이어야 한다. 게시(GitHub Pages 등)는 사용자가 요청하거나 승인했을 때만, 그 저장소에 맞는 git 계정으로 푸시한다. 게시 뒤 `build_support_site.py verify kit.json`로 모든 언어의 페이지가 200, 올바른 `lang`, 지원 이메일 포함인지 확인하고 `site.live`를 `true`로 바꾼다.
4. **붙여넣기 시트:** `python3 scripts/paste_sheet.py kit.json`. 언어를 고르면 언어별 값이 바뀌고 복사 버튼과 글자 수가 있는 HTML 한 장이 나온다. 사용자에게 열어 주거나 비공개 페이지로 게시한다.
5. **App Store Connect 입력 안내:** [references/app-store-connect.md](references/app-store-connect.md)를 읽고 화면 순서대로 안내한다. 사용자가 화면 캡처를 보내면 그 화면의 칸 이름 그대로, 칸마다 넣을 값을 답한다. 어느 칸이 어느 페이지에 있는지는 캡처와 이 문서로 확인하고 추측하지 않는다.
6. **빌드 업로드:** 사용자가 업로드를 요청하면 [references/upload-and-review.md](references/upload-and-review.md)대로 `scripts/upload_build.sh`를 실행한다. Xcode에 Apple 계정이 없으면 스크립트가 멈추고, 사용자가 직접 로그인해야 한다. 업로드할 때마다 빌드 번호를 올린다.
7. **빌드 선택과 심사 제출:** 처리(10~30분)가 끝나면 버전 페이지의 빌드 칸에서 고르고, 앱 심사 정보를 채운 뒤 제출한다. 거절되면 사유를 그대로 받아 고친다.

## 지켜야 할 것

- 사용자의 언어로 답한다. 영어 화면을 쓰는 사용자에게만 영어 칸 이름을 쓰고, 그 밖에는 사용자가 보는 칸 이름 그대로 쓴다.
- 로그인, 2단계 인증, 계약·세금·은행, 가격과 판매 국가 결정, 심사 제출 버튼은 사용자가 한다. 사이트 푸시와 빌드 업로드는 요청을 받은 뒤에만 한다.
- 공개되는 이메일·주소는 사용자가 고른 것만 쓴다. 전화번호는 키트에 넣지 않고 사용자가 직접 입력하게 한다.
- 샘플 인물 사진이 실제 인물인지 생성 이미지인지 묻는다. 실제 인물이면 촬영 대상과 촬영자의 상업적 이용 동의가, 생성 이미지면 생성 서비스 약관의 상업적 이용 허용이 필요하다. 콘텐츠 권한 질문의 답도 이에 따라 달라진다.
- 잘못 안내한 것을 알게 되면 바로 정정하고, 키트와 참고 문서에도 반영한다.
- 남은 사용자 몫(계약, 동의, 원어민 검수 등)은 마지막에 목록으로 알려 준다.

## 결과물

- `check_store_metadata.py`가 모든 언어에서 PASS
- 언어별 스크린샷 폴더(칸 규격 크기, 화면 순서 고정)
- 언어별 지원·개인정보·소개 페이지와 `verify` 통과 기록
- 붙여넣기 시트, 심사 메모, `kit.json`의 `common`에 기록한 공통 답변(카테고리, 연령 등급, 개인정보, 가격, 판매 국가)
- 업로드한 버전과 빌드 번호
