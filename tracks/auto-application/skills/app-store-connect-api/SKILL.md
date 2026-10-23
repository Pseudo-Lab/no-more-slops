---
name: app-store-connect-api
description: "App Store Connect API 키로 iOS 앱의 App Store Connect 설정을 직접 한다. 연령 등급·콘텐츠 권한·가격·판매 국가, 구독·앱 내 구입 상품(국가별 가격·첫 구매 혜택·전 언어 현지화·상품별 심사 스크린샷), 배포 프로파일과 빌드 업로드, 스토어 문구·스크린샷 업로드, TestFlight 내부 테스트, 버전에 빌드 연결과 제출 전 점검을 API로 처리한다. 'API로 올려줘', '결제 상품 만들어줘', '가격·판매 국가 설정', '빌드 업로드가 서명에서 막힘', 'TestFlight에 올려줘'에 사용한다. 스토어 문구·스크린샷·지원 페이지를 만드는 일은 하지 않는다."
---

# App Store Connect API로 출시 설정하기

출시 자료(스토어 문구 35개 언어, 스크린샷, 개인정보처리방침 URL)가 준비된 iOS 앱을, 사람이 웹 화면에 붙여 넣는 대신 App Store Connect API로 설정한다. 앱 이름·번들 ID·가격·국가·상품은 모두 작업별 입력값이며 이 스킬에 기본값으로 들어 있지 않다. 예시는 Fewshot 1.0의 실제 명세([references/example/iap-spec.json](references/example/iap-spec.json))다.

## API로 되는 것과 안 되는 것

먼저 [references/api-coverage.md](references/api-coverage.md)를 읽는다. 요약하면:

- **사람이 웹에서:** 앱 레코드 만들기(새로운 앱), 계약·세금·은행, 앱 개인정보(App Privacy) 설문, 배포 인증서 만들기(Xcode › Settings › Accounts), 심사 제출 버튼
- **API로:** 그 밖의 설정과 업로드 전부

사용자가 할 일은 화면 경로와 넣을 값까지 적어서 한 번에 알려 준다. 캡처를 보내면 그 화면의 칸 이름 그대로 답한다.

## 준비

1. **API 키:** App Store Connect › 사용자 및 액세스 › 통합 › App Store Connect API › 팀 키. 키 ID, Issuer ID(페이지 맨 위 UUID — 키 이름과 헷갈리기 쉽다), `.p8`(한 번만 받을 수 있음)을 받는다. `.p8`은 저장소 밖에 두고 `.gitignore`에 `*.p8`을 넣는다. 키 내용을 출력하지 않는다.
2. 환경 변수 `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_PATH`를 설정하고 `python3 -I scripts/app_setup.py check --bundle-id <번들 ID>`로 접속·앱·번들 ID·빌드·상품 상태를 본다.
3. **이름 겹침:** 앱 레코드를 만들기 전에 `python3 -I scripts/app_name_check.py <후보…> --countries us kr jp de gb`. 제목 **어디에든** 후보가 단어로 들어 있으면 겹친다고 본다("Swipe Photo Sorting - Albumate"처럼 브랜드를 뒤에 붙이는 앱이 많다). 띄어 쓴 형태도 확인한다. App Store Connect는 이름 전체가 같을 때만 거부하므로, 이 확인 없이 만들면 같은 기능의 앱과 브랜드가 겹칠 수 있다.

## 단계

1. **앱 정보:** `app_setup.py age-rating --advertising`(광고가 있으면), `content-rights --uses-third-party`(외부 모델·음원·사진을 내려받거나 보여 주면 — 권리가 있을 때만), `pricing --free --exclude CHN`(중국 본토는 ICP 비안 번호가 없으면 심사가 막힌다). 각 결과(연령 등급 문자열, 판매 국가 수)를 사용자에게 보고한다.
2. **결제 상품:** 명세를 만들고 `iap_setup.py spec.json --validate`로 글자 수(이름 30, 설명 45)를 검사한 뒤 실행한다. 현지화는 스토어 문구와 같은 언어 전부로 만든다(영어·한국어만 두지 않는다). 순서와 함정은 아래 "지켜야 할 것".
3. **심사 스크린샷:** 상품마다 **그 요금제를 고른** 결제 화면을 찍는다(버튼 문구도 상품마다 다르다). 구독하지 않은 시뮬레이터에서 영어로 띄우면 샌드박스 상품과 가격이 나온다. 상품이 막 만들어진 직후에는 불러오지 못할 수 있다. 사용자가 이미 구독한 기기에서는 결제 화면에 상품이 안 나온다.
4. **빌드:** Release 아카이브 후 `xcodebuild -exportArchive`(ExportOptions `method` app-store-connect, `destination` upload)에 `-authenticationKeyPath/-authenticationKeyID/-authenticationKeyIssuerID`를 준다. `Cloud signing permission error`가 나면 키 역할로는 클라우드 서명이 안 되는 것이다. 사용자에게 Apple Distribution 인증서를 만들게 하고 `app_store_profile.py`로 프로파일을 만든 뒤 수동 서명으로 내보낸다. 올릴 때마다 빌드 번호를 올린다.
5. **스토어 문구·스크린샷:** fastlane `deliver`에 API 키 JSON(`key_id`, `issuer_id`, `key`)을 주고 `skip_binary_upload`, `submit_for_review false`로 올린다. 문구만 고칠 때는 `--skip_screenshots true`. 올린 뒤 API로 다시 읽어 언어 수·이름·스크린샷 장수(언어 × 장수)를 확인한다.
6. **TestFlight:** `app_setup.py testflight`로 내부 그룹(모든 빌드 자동 배포)과 테스터(App Store Connect 사용자)를 넣는다. 처리(VALID)는 업로드 뒤 보통 5~30분이며, 끝나면 사용자에게 알린다.
7. **제출 직전:** `app_setup.py attach-build --build <번호>`, 다시 `check`. 사용자에게 버전 페이지에서 "앱 내 구입 및 구독"에 상품을 추가하고(첫 구독·상품은 앱 버전과 함께 심사) 제출하게 안내한다. 출시 방식은 수동 출시를 권한다.

## 지켜야 할 것

- **구독은 판매 국가가 가격보다 먼저다.** 가격부터 넣으면 409 "territory is not supported for your subscription and planType".
- **구독 가격·첫 구매 혜택은 국가마다 넣는다.** 기준 국가 가격 포인트의 `equalizations`로 나머지 국가를 채운다. 비소모품은 기준 국가 가격 하나면 자동 환산된다.
- **429가 나면 기다린다.** 수백 건을 한꺼번에 보내면 한동안 모든 요청이 막힌다. 동시 요청은 3개 이하로, 429는 지수적으로 기다렸다 다시 보낸다(`asc.call`).
- **심사 스크린샷은 RGB로.** 투명도 채널이 있으면 크기가 맞아도 `IMAGE_INCORRECT_DIMENSIONS`로 거절된다. 업로드 후 `assetDeliveryState`가 `COMPLETE`인지 확인한다.
- **구독 상태 표시를 믿지 말고 화면을 확인한다.** API의 `MISSING_METADATA`가 남아 있어도 웹 구독 화면에서 "심사에 추가" 버튼이 켜져 있으면 빠진 칸이 없다. 사용자 캡처로 확인하고 추측하지 않는다.
- **판정 문구를 정확히 찾는다.** 자동 확인에서 성공 문구에도 같은 단어가 들어갈 수 있다(예: "No implementation issues found"). 실패를 숫자로 시작하는 문구 등으로 구분하고, 원래 코드에서 실패가 재현되는지 먼저 확인한다.
- **스토어 주장과 스크린샷이 맞는지 본다.** 테스트를 빨리 돌리려고 바꾼 설정(예: 클래스당 3장)이 스크린샷에 찍히면 스토어 이름("사진 5장만")과 어긋난다. 스크린샷은 출시 기본값으로 찍는다.
- 키·인증서·프로파일·상품 가격은 계정에 남는 변경이다. 사용자가 요청했거나 출시 문서로 합의한 값만 쓰고, 한 일과 값(가격, 제외 국가, 연령 등급)을 보고한다. 심사 제출과 출시는 사용자가 한다.

## 결과물

- `check` 출력: 버전 상태, 연결된 빌드, 연령 등급, 콘텐츠 권한, 상품별 상태
- 명세 파일(`iap-spec.json`)과 상품별 심사 스크린샷, 현지화 언어 수
- 업로드한 빌드 번호와 TestFlight 처리 결과
- 사용자에게 남은 일 목록(앱 개인정보 설문, 계약, 심사 제출 등)

관련 스킬: 스토어 문구·스크린샷·지원 페이지를 만들고 웹 입력을 안내하는 `app-store-release`(#7), 언어별 화면 점검 `global-localization`(#7), 시뮬레이터·기기 검증 `ios-verify-harness`(#7). 이 스킬은 그 결과물을 API로 App Store Connect에 반영하며, 어느 것도 먼저 설치돼 있어야 하는 것은 아니다.
