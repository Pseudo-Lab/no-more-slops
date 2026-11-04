---
name: env-split
description: 로컬 개발과 운영을 분리한다 — 로컬 Supabase(supabase start)와 마이그레이션 동기화, .env.development.local / .env.local 역할 구분, OAuth Redirect URI 두 줄, 로컬에서 외부 AI를 키 없이 돌리는 대체 경로(Codex SDK 등). "로컬 DB", "개발/운영 분리", "로컬에서 테스트하고 싶다", "로컬 로그인 안 돼", "키 없이 로컬에서"처럼 환경 요청이면 이 스킬을 쓴다.
---

# env-split

운영 DB에 테스트 데이터를 넣기 시작하면 돌아오기 어렵다. 핵심 기능이 돌아간 직후, 두 번째 사람이 쓰기 전에 나눈다.

## 입력
- Docker 런타임(OrbStack 등)이 있는지. 없으면 설치는 사람 몫.
- OAuth 앱 콘솔 접근(Redirect URI 추가는 사람), provider secret(`supabase/.env`에만, gitignore).

## 절차
1. **로컬 DB** — `npx supabase start` → 마이그레이션 자동 적용. `supabase status -o env`로 값 확인. 쿼리는 `supabase db query --local "<한 문장>"`(한 번에 한 문장이 확실하다).
2. **config.toml** — `[auth.external.<provider>]` enabled + `env()` 참조. 값은 `supabase/.env`. **`supabase config push`는 하지 않는다**(운영 설정을 덮어쓴다).
3. **환경 파일** — `.env.development.local`: 로컬 URL·키(dev만 읽음). `.env.local`: 운영 값(build·Vercel). `.env.example`에 역할 주석. 둘 다 gitignore.
4. **OAuth** — 콘솔에 Redirect URI 두 줄(운영 콜백 + `http://127.0.0.1:54321/auth/v1/callback`). 앱은 하나를 공유한다; 동의 항목 실험이 필요해질 때만 dev 앱을 나눈다.
5. **외부 AI 대체 경로** — 로컬에서 유료 키 없이 돌리려면 플래그(`EXTRACT_VIA=codex`)로 Codex SDK 등 구독 경로를 쓴다. 프롬프트·스키마는 운영과 같은 파일. 임시 파일·세션 기록은 호출 직후 삭제.
6. **가상 데이터** — 로컬 DB에만 가상 레코드를 넣어 화면을 확인한다. 실제 개인 데이터는 넣지 않는다.
7. `ship-loop`로 PR(설정 변경이라 spec 생략 가능).

## 자주 막히는 곳
- "provider is not enabled": config 블록이 작업 중인 브랜치에 없거나 `supabase stop/start`를 안 했다.
- OAuth 오류 코드(카카오 KOE006 등): Redirect URI 불일치.
- 개발 서버 포트: 콜백·북마크가 기대하는 포트로 고정해서 띄운다.

## 멈추는 지점 (사람 몫)
- Redirect URI 추가, `supabase/.env` 값 입력, Docker 설치.

## 산출물
로컬에서 로그인·핵심 기능까지 도는 환경, `.env.example` 설명. 트랙의 마지막 단계.
