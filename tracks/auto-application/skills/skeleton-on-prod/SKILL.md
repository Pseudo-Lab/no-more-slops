---
name: skeleton-on-prod
description: 기능 0개인 뼈대(OAuth 로그인 → 테이블 1개 + RLS → 빈 홈)를 첫날 운영 URL에 올린다. 스택 기본값은 Next.js App Router 서버 액션 + Supabase(RLS) + Vercel + 외부 OAuth(카카오 등). "프로젝트 세팅", "로그인부터", "배포 먼저 해 두자", "스캐폴드", "Supabase 연결"처럼 서비스의 첫 골격을 세우는 요청이면 이 스킬을 쓴다. 헌법이 있으면 그 원칙(특히 보안·데이터)을 그대로 설계에 반영한다.
---

# skeleton-on-prod

가게 문이 열려 있어야 그 뒤에 뭘 갖다 놓든 손님 눈으로 바로 확인한다. 기능 전에 주소부터.

## 입력
- 헌법(`constitution-first` 산출물). 없으면 먼저 권한다.
- 첫 화면 3개 이름(예: 올리기 · 확인 · 홈). 뼈대는 그중 "홈"을 빈 상태로 만든다.
- 사람이 미리 준비할 것: OAuth 앱(클라이언트 id·secret), Supabase 프로젝트, Vercel 계정. 없으면 체크리스트로 요청하고 멈춘다.

## 절차
1. **스캐폴드** — Next.js App Router. 서버 액션만, API 라우트 없음(검증·키·과금이 한 곳). `proxy.ts`(미들웨어)에서 세션 갱신과 로그인 리다이렉트.
2. **데이터** — 테이블 1~2개와 RLS. 권한 판단 함수 하나(예: `is_family_member(id)`)에 모든 정책을 건다. 여러 테이블을 한 번에 바꾸는 일만 security definer RPC. **service-role 클라이언트는 만들지 않는다.**
3. **로그인** — Supabase Auth + OAuth provider. provider secret은 사람이 대시보드에 넣는다. Redirect URI는 운영·로컬 두 줄.
4. **빈 홈** — 로그인 → (필요하면) 그룹 만들기/초대 → 아무것도 없는 홈. 빈 상태 문구까지.
5. **배포** — `vercel deploy --prod`. 운영 URL에서 로그인까지 사람이 직접 확인.
6. 끝은 `ship-loop`로: 이슈·spec·PR·운영 확인.

## 멈추는 지점 (사람 몫)
- OAuth 앱 등록과 secret 입력, Redirect URI, Vercel 프로젝트 연결, 첫 로그인 확인.

## 산출물
운영 URL 하나, 마이그레이션 파일, RLS 정책, 로그인되는 빈 홈. 다음 단계는 `launch-basics`.
