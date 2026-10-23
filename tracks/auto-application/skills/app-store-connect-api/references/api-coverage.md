# App Store Connect API: 되는 것, 안 되는 것, 실제로 막힌 곳

2026-10 Fewshot 1.0(번들 ID `com.minhyeong.albumate`, 35개 언어, 구독 2개 + 비소모품 1개)을 API로 설정하며 확인한 내용이다. Apple이 API를 자주 바꾸므로 응답이 다르면 응답을 따르고 이 문서를 고친다.

## 사람이 웹에서 해야 하는 것

| 일 | 이유 | 안내 |
| --- | --- | --- |
| 앱 레코드 만들기 | API에 앱 생성이 없다 | 앱 › + › 신규 앱: 플랫폼, 이름(30자), 기본 언어, 번들 ID, SKU(바꿀 수 없음), 전체 액세스 |
| 번들 ID 등록 | API(`/v1/bundleIds`)로도 되지만 보통 Xcode 자동 서명이 이미 했다 | 개발 서명이 와일드카드(`*`) 프로파일이면 등록되지 않았을 수 있다 → `check`로 확인 |
| 계약·세금·은행 | 법적 동의 | 비즈니스 › 유료 앱 계약 |
| 앱 개인정보(App Privacy) | API에 설문이 없다 | 데이터 유형마다 용도(타사 광고·분석 등), 사용자 연결 여부, 추적 여부. 광고 SDK가 있으면 그 SDK의 공개 자료와 대조 |
| 배포 인증서 | 앱 관리 키로는 클라우드 인증서를 못 쓴다 | Xcode › Settings › Accounts › 팀 › Manage Certificates › + › Apple Distribution |
| 심사 제출 | 사용자 결정 | 버전 페이지 › 앱 내 구입 및 구독에 상품 추가 › 심사에 추가 › 제출 |

## API로 한 것

| 일 | 엔드포인트 | 메모 |
| --- | --- | --- |
| 연령 등급 | `PATCH /v1/ageRatingDeclarations/{appInfoId}` | 2026 질문지는 콘텐츠 13개(NONE…)와 기능 11개(true/false). `advertising`이 있다 |
| 콘텐츠 권한 | `PATCH /v1/apps/{id}` `contentRightsDeclaration` | 외부 AI 모델을 내려받아 쓰면 `USES_THIRD_PARTY_CONTENT` |
| 무료 가격 | `POST /v1/appPriceSchedules` | 기준 국가의 0원 가격 포인트 |
| 판매 국가 | `POST /v2/appAvailabilities` | 국가마다 `territoryAvailabilities`. v1 응답은 404 |
| 구독 그룹·상품·현지화 | `/v1/subscriptionGroups`, `/v1/subscriptions`, `/v1/subscriptionLocalizations` | 이름 30자, 설명 45자 |
| 구독 판매 국가 | `POST /v1/subscriptionAvailabilities` | **가격보다 먼저** |
| 구독 가격 | `POST /v1/subscriptionPrices` × 국가 수 | `planType` 기본값 UPFRONT. 기준 가격의 `equalizations`로 나머지 국가 |
| 첫 구매 혜택 | `POST /v1/subscriptionIntroductoryOffers` × 국가 수 | 7일 무료 체험 = `ONE_WEEK`, `FREE_TRIAL` |
| 비소모품 | `POST /v2/inAppPurchases`, `/v1/inAppPurchasePriceSchedules`, `/v1/inAppPurchaseAvailabilities` | 기준 국가 가격 하나면 자동 환산 |
| 상품 심사 스크린샷 | `.../appStoreReviewScreenshots` 예약 → 업로드 → `uploaded: true` | 상품마다 하나. 바꾸려면 지우고 다시 |
| 배포 프로파일 | `POST /v1/profiles` (`IOS_APP_STORE`) | 키체인에 배포 인증서가 있어야 쓸 수 있다 |
| 빌드 업로드 | `xcodebuild -exportArchive` + 키 인수 | 처리 상태는 `/v1/builds?filter[version]=` |
| TestFlight 내부 테스트 | `/v1/betaGroups`, `/v1/betaTesters` | 내부 테스터는 App Store Connect 사용자여야 한다 |
| 버전에 빌드 연결 | `PATCH /v1/appStoreVersions/{id}/relationships/build` | 빌드가 VALID여야 한다 |
| 문구·스크린샷 | fastlane `deliver` | 35개 언어 이름·부제·설명·키워드·URL, 스크린샷 210장, 심사 정보 |

## 실제 오류와 해결

| 오류 | 원인 | 해결 |
| --- | --- | --- |
| `409 The provided territory is not supported for your subscription and planType` | 구독 판매 국가를 정하기 전에 가격을 넣음 | `subscriptionAvailabilities` 먼저 |
| `429 We've received too many requests` | 실패한 요청 수백 건을 8개씩 동시에 보냄 | 1분 쉬고, 동시 3개 이하 + 지수적 재시도 |
| `IMAGE_INCORRECT_DIMENSIONS` (1206×2622인데도) | PNG에 투명도 채널 | RGB로 저장해 다시 올림 |
| `exportArchive Cloud signing permission error` / `No profiles for '<번들 ID>' were found` | 앱 관리 역할 키는 클라우드 인증서·프로파일을 못 만든다 | 사용자가 Apple Distribution 인증서를 만들고, API로 App Store 프로파일을 만든 뒤 수동 서명 |
| `No signing certificate "iOS Distribution" found` | 계정에 배포 인증서가 없음 (`/v1/certificates`로 확인) | 위와 같음 |
| 구독 `MISSING_METADATA`가 계속 남음 | API 상태와 웹 화면이 다름 | 웹 구독 화면에서 "심사에 추가"가 켜져 있으면 준비된 것. 사용자 캡처로 확인 |
| fastlane `Error fetching app store review detail - No data` | 심사 정보가 처음 만들어질 때 나는 메시지 | 종료 코드 0이면 API로 다시 읽어 확인(연락처·메모가 들어감) |
| 시뮬레이터 결제 화면에 상품이 안 나옴 | 상품을 막 만들었거나 StoreKit 설정이 UI 테스트 앱에 적용되지 않음 | 잠시 뒤 샌드박스 상품으로 다시. `SKTestSession`은 UI 테스트의 앱에 적용되지 않았다 |
