# 출시 키트 형식

키트는 앱 저장소의 `docs/app-store/` 같은 폴더 하나다. `kit.json` 안의 경로는 모두 `kit.json` 기준 상대 경로다. 완성된 예시는 [example/](example/kit.json)에 있다.

```
docs/app-store/
  kit.json              앱 정보, 언어, 사이트, 스크린샷, 심사 연락처, 공통 답변
  metadata/<locale>.md  언어별 스토어 문구
  site-strings.json     언어별 지원·개인정보·소개 페이지 문구
  review-notes.md       앱 심사 정보 › 메모 (영어)
  screenshots/<칸>/<locale>/<번호-화면>.jpg   capture_screenshots.py가 만든다
  site/                 build_support_site.py가 만든다
  paste-sheet.html      paste_sheet.py가 만든다
```

## kit.json

| 키 | 내용 |
|---|---|
| `app.name`, `app.bundleId`, `app.version`, `app.build` | 시트 머리말과 스크린샷 실행에 쓴다. 빌드 번호는 업로드할 때마다 올린다 |
| `app.primaryLocale` | App Store Connect의 기본 언어. hreflang `x-default`도 이 언어를 가리킨다 |
| `app.brandPrefixes` | 선택. 언어별 이름이 이 중 하나로 시작하지 않으면 경고 |
| `metadataDir` | 기본 `metadata` |
| `locales[]` | `code`(App Store 언어 코드, 메타데이터 파일 이름), `label`(App Store Connect 언어 메뉴의 이름), `folder`(사이트 폴더, 기본 언어는 `""`), `lang`(HTML lang), `appLanguage`·`region`(시뮬레이터 `-AppleLanguages`·`-AppleLocale`) |
| `site.baseUrl` | 게시 주소. 언어별 URL = baseUrl + folder + 페이지 |
| `site.email` | 지원 페이지에 공개되는 문의 이메일. 사용자가 고른 주소만 쓴다 |
| `site.strings`, `site.out`, `site.mark`, `site.css` | 문구 파일, 출력 폴더(기본 `site`), 머리 글자, CSS 교체(선택) |
| `site.live` | `verify`가 통과하면 `true`. 시트의 "게시 확인 전" 표시가 사라진다 |
| `screenshots.dir`, `slot`, `size` | 출력 폴더, App Store Connect 칸 이름, 칸 규격(`1206x2622`). 크기가 다르면 캡처 스크립트가 실패한다 |
| `screenshots.launchArgs` | 모든 장면에 붙는 실행 인수(예: 약관 자동 동의 `-acceptTerms`) |
| `screenshots.shots[]` | `name`, `wait`(초), `args`(그 화면을 여는 DEBUG 실행 인수). 순서가 스토어 순서다 |
| `review` | `firstName`, `lastName`, `email`, `signInRequired`, `notes`(메모 파일). 전화번호는 비워 두고 사용자가 직접 넣는다 |
| `common[]` | 모든 언어 공통 답변. `page`, `field`, `value`, `hint`, `copy`(복사 버튼 여부). 시트에 페이지별로 묶여 나온다 |

## metadata/<locale>.md

```markdown
# ko

## Name
톤릿: 피부톤 보정

## Subtitle
내 피부톤을 읽고 원하는 톤으로

## Promotional text
…

## Keywords
피부보정,톤업,셀카,…

## Description
…

## What's New
(업데이트 버전에서만)
```

제목은 영어 그대로 둔다. 한도: 이름·부제 30자, 프로모션 텍스트 170자, 키워드 100자, 설명·새로운 기능 4,000자. 이름·키워드·설명은 필수, 부제·프로모션 텍스트는 선택이지만 비우지 않는 편이 낫다.

- 키워드는 쉼표로만 구분하고 띄어쓰기를 넣지 않는다. 이름·부제에 있는 단어는 이미 검색되므로 반복하지 않는다. 다른 회사 상표나 앱 이름은 넣지 않는다.
- 설명의 문단 제목은 마침표 없이, 목록은 `•`로 쓴다. 진단·치료 같은 의학적 표현이 필요하면 "진단이 아님"을 함께 쓴다.

## site-strings.json

언어 코드마다 객체 하나. 필수 키: `native`(언어 메뉴에 보일 그 언어 이름), `languages`(언어 메뉴 접근성 이름), `indexDesc`, `headline`, `lead`, `supportTitle`, `supportDocTitle`, `supportDesc`, `faq`(`[질문, 답]` 목록), `contactTitle`, `contact`(`{email}` 포함), `privacyTitle`, `privacyDocTitle`, `privacyDesc`, `privacyUpdated`, `privacy`(`[제목, 본문]` 목록), `footer`. 선택: `supportMeta`, `indexTitle`(기본은 그 언어의 스토어 이름).

`{email}`은 메일 링크로, `{refund}`는 Apple 환불 페이지 링크로 바뀐다. 개인정보 처리방침 본문은 앱 안의 방침 문자열에서 그대로 가져와 두 곳이 어긋나지 않게 한다.

## 언어 표

App Store Connect 언어 메뉴의 이름과 코드. 앱 언어 목록에 맞춰 고른다.

| App Store Connect | code | folder | lang | appLanguage | region |
|---|---|---|---|---|---|
| 영어(미국) | en-US | (루트) | en | en | en_US |
| 영어(영국) | en-GB | en-gb | en-GB | en-GB | en_GB |
| 한국어 | ko | ko | ko | ko | ko_KR |
| 일본어 | ja | ja | ja | ja | ja_JP |
| 중국어(간체) | zh-Hans | zh-hans | zh-Hans | zh-Hans | zh_CN |
| 중국어(번체) | zh-Hant | zh-hant | zh-Hant | zh-Hant | zh_TW |
| 스페인어(스페인) | es-ES | es | es | es | es_ES |
| 스페인어(멕시코) | es-MX | es-mx | es-MX | es-MX | es_MX |
| 포르투갈어(브라질) | pt-BR | pt-br | pt-BR | pt-BR | pt_BR |
| 프랑스어 | fr-FR | fr | fr | fr | fr_FR |
| 독일어 | de-DE | de | de | de | de_DE |
| 이탈리아어 | it | it | it | it | it_IT |
| 태국어 | th | th | th | th | th_TH |
| 베트남어 | vi | vi | vi | vi | vi_VN |
| 인도네시아어 | id | id | id | id | id_ID |

간체 중국어 문구는 중국 본토 판매를 빼도 싱가포르·말레이시아에서 보인다.
