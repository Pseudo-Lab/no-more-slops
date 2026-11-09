---
name: kakao-login-console
description: Supabase 서비스에 카카오 로그인을 붙일 때 카카오 개발자 콘솔 설정을 화면 순서대로 안내하고(앱 등록·아이콘·REST API 키·Client Secret·Redirect URI·카카오 로그인 활성화·동의항목), 키는 채팅에 남기지 않고 숨김 입력 스크립트로 supabase/.env에 넣은 뒤 config push로 운영에 반영하고 점검 스크립트로 확인한다. "카카오 로그인", "카카오 SSO", "kakao OAuth", "카카오 콘솔 어디서", "KOE 오류", "REST API 키 어디", "Redirect URI 뭐 넣어"처럼 카카오 로그인 설정 요청이면 이 스킬을 쓴다. 뼈대 전체는 skeleton-on-prod, 로컬/운영 분리는 env-split.
---

# kakao-login-console

카카오 콘솔은 메뉴가 많고 이름이 비슷하다(REST API 키 vs JavaScript 키, 로그인 Redirect URI vs 로그아웃 Redirect URI). 사람이 화면을 하나씩 열 때 **지금 어느 화면의 어느 칸인지**만 한 번에 하나씩 알려 준다. 키 값은 절대 채팅으로 받지 않는다.

## 입력
- Supabase 프로젝트 ref(운영 URL `https://<ref>.supabase.co`), 서비스 운영 주소(예: `https://myservice.kro.kr`).
- 앱 아이콘 이미지(JPG/PNG). 없으면 로고 SVG에서 512px JPG를 먼저 뽑는다.
- 사람이 직접 할 것: 카카오 계정으로 developers.kakao.com 로그인. 콘솔 조작은 전부 사람 몫이다(대신 로그인하지 않는다).

## 절차

### 1. 콘솔 (사람이 화면을 열고, 한 단계씩 확인받으며 진행)
| 순서 | 화면 | 넣을 값 |
|---|---|---|
| 1 | 내 애플리케이션 → 애플리케이션 추가 | 앱 이름(서비스명), 회사명(개인이면 본인 이름), 카테고리, 앱 아이콘 |
| 2 | 앱 설정 → 플랫폼 키 → **REST API 키** | 이 32자 값이 `client_id`. JavaScript 키·네이티브 앱 키가 아니다 |
| 3 | REST API 키 상세 → **카카오 로그인 Redirect URI** | `https://<ref>.supabase.co/auth/v1/callback` 한 줄. 로컬도 쓰면 로컬 Supabase 콜백(`http://127.0.0.1:<auth 포트>/auth/v1/callback`)을 한 줄 더. **로그아웃 Redirect URI 칸이 아니다** |
| 4 | REST API 키 상세 → **Client Secret** | 코드 생성 → 활성화 "사용함". 이 값이 `secret` |
| 5 | 카카오 로그인 → 사용 설정 | 상태 ON |
| 6 | 카카오 로그인 → **동의항목** | 닉네임, 프로필 사진, **카카오계정(이메일)** 을 켠다. Supabase가 `account_email profile_image profile_nickname`를 요청하므로 하나라도 빠지면 KOE205. 이메일 항목이 잠겨 있으면 콘솔이 안내하는 전환(비즈 앱 등)을 따른다 |
| 7 | 동의항목 → 동의 목적 | 한 줄. 예) "로그인한 사람을 구분하고 기기를 바꿔도 같은 기록을 보여 주기 위해" |

사람이 스크린샷을 보내면 그 화면이 표의 몇 번인지 먼저 말하고, 다른 화면이면(예: 로그아웃 Redirect URI) 어디로 가야 하는지만 짚는다.

### 2. 키 넣기 (채팅 금지)
- 사람이 직접 실행: `bash <skill-dir>/scripts/set-kakao-keys.sh supabase/.env` — `read -s`로 받아 파일(권한 600)에만 쓰고 길이만 출력한다. 두 값 모두 32자면 정상.
- `supabase/.env`는 `.gitignore`에 있는지 확인한다.

### 3. Supabase 반영
- `supabase/config.toml`:
  ```toml
  [auth.external.kakao]
  enabled = true
  client_id = "env(SUPABASE_AUTH_EXTERNAL_KAKAO_CLIENT_ID)"
  secret = "env(SUPABASE_AUTH_EXTERNAL_KAKAO_SECRET)"

  [remotes.production.auth]
  site_url = "https://<운영 주소>"
  additional_redirect_urls = ["https://<운영 주소>/**", "https://<프로젝트>.vercel.app/**"]
  enable_anonymous_sign_ins = false
  ```
- **먼저 `supabase config diff`** 로 운영과 다른 값을 본다. 로컬 개발용 값(이메일 확인 끔, MFA, 풀러 크기 등)이 운영에 덮어써지면 안 되므로, diff에 나온 운영 값은 `[remotes.production.*]`에 지금 값 그대로 고정한 뒤 `supabase config push --yes`.
- 클라이언트는 supabase-js PKCE: `createClient(url, key, { auth: { flowType: "pkce" } })`, `signInWithOAuth({ provider: "kakao", options: { redirectTo: location.origin + next } })`. 돌아온 `?code=`는 `getSession()`이 세션으로 바꾼다.

### 4. 확인
- `node <skill-dir>/scripts/check-kakao.mjs https://<ref>.supabase.co https://<운영 주소>` — Supabase가 카카오로 넘기는 주소에서 client_id 길이(32), redirect_uri, scope를 본다.
- KOE 오류는 **카카오 로그인을 마친 뒤에만** 나와서 스크립트로 못 잡는다. 사람이 운영 주소에서 실제로 로그인해 본다.

## 오류표 (로그인 후 카카오 화면에 뜨는 것)
| 코드 | 뜻 | 고칠 곳 |
|---|---|---|
| KOE006 | redirect_uri가 등록돼 있지 않음 | 1-3번 칸에 `…/auth/v1/callback`을 글자 그대로 |
| KOE101 | 앱 키가 틀림 | REST API 키를 넣었는지(2번), 스크립트 다시 실행 |
| KOE205 | 요청한 동의항목이 꺼져 있음 | 6번 동의항목, 특히 이메일 |
| 로그인 뒤 사이트로 안 돌아옴 | site_url/additional_redirect_urls에 운영 주소 없음 | 3단계 config push |

## 멈추는 지점 (사람 몫)
- 콘솔 로그인과 모든 콘솔 입력, 키 스크립트 실행, 실제 카카오 로그인 확인.
- 이메일 동의항목이 비즈 앱 전환 등을 요구할 때 그 결정.

## 산출물
카카오 로그인되는 운영 주소, `config.toml`의 kakao·`[remotes.production]` 블록, 커밋되지 않은 `supabase/.env`, 점검 스크립트 출력.
