---
name: micro-saas-week
description: 아이디어 한 문장에서 상용 배포까지 1주. 헌법 → 뼈대 → 상용 기본기 → 핵심 기능 → 실측 → 안전장치·가독성 → 환경 분리 순서로, 이슈 1 = 브랜치 1 = spec 1 = PR 1로 진행하고 사람 몫은 체크리스트로 멈춘다. 새 웹 서비스를 빠르게 출시해야 할 때 쓴다.
---

# micro-saas-week

오래오래(가족 건강검진 기록장)를 1주 만에 배포한 트랙을 스킬로 옮긴 초안. 원본 과정은 `../../PROCESS.md`.

## 입력 (시작 전에 받는다)
- 문제 한 문장: "___를 위해 ___를 만든다"
- 핵심 사용자 1명과 첫 화면 3개
- 절대 안 할 것 (예: 원본 파일 저장 안 함, 진단 안 함)
- 스택 기본값: Next.js App Router 서버 액션 + Supabase(RLS) + Vercel + 외부 AI 1회 호출. 다른 스택이면 2단계만 바꾼다.

## 단계
각 단계는 **이슈 1개 → 브랜치 `NNN-name` → `specs/NNN-name/spec.md` → 구현 → PR "Closes #N" + Constitution Check → 운영 URL에서 확인**으로 끝낸다. 버그 수정은 spec을 생략한다.

1. **헌법** — `speckit-constitution`으로 원칙 5개 이내. 이후 판단이 갈릴 때 사용자에게 묻지 않고 여기에 비춘다.
2. **뼈대** — 로그인(OAuth) → 테이블 1개 + RLS → 빈 홈이 운영 URL에서 동작. service-role 클라이언트는 만들지 않는다.
3. **상용 기본기** — 랜딩, 약관, 처리방침, 탈퇴(RPC), 에러·빈 화면, 분석 이벤트(개인정보 없이 단계 이름만), 도메인.
4. **핵심 기능** — 서비스가 약속한 한 가지. 외부 AI는 구조화 출력(json_schema) + 데이터 미보관 옵션 + 서버 전용 키. 사람이 확인하는 단계를 사이에 둔다.
5. **실측** — 같은 입력으로 모델·프롬프트 2개 이상을 돌려 정확도·토큰·비용 표를 만든 뒤 결정. 남용 상한(크레딧·일일 제한·월 한도)을 같이 정한다.
6. **안전장치·가독성** — 되돌릴 수 없는 동작에 확인 모달, 긴 목록은 "요약 한 줄 + 접기", 레퍼런스 3곳 조사 → 목업 → 구현.
7. **환경 분리** — 로컬 DB(`supabase start`)와 운영 분리, OAuth Redirect URI 2줄, `.env.development.local` / `.env.local` 구분.

## 멈추고 사람에게 넘기는 것 (체크리스트로 출력)
- 외부 콘솔 계정·키: OAuth 앱, DB 대시보드 provider 설정, AI API 키, 분석 속성, 도메인·DNS
- 법적·제품 결정: 서비스명, 개인정보 담당 표기, 요금·제한 수치, 환불 정책
- 로그인·2단계 인증이 필요한 모든 확인
- PR 머지, 운영 DB 마이그레이션 push, 운영 배포(환경 정책에 따라)
- 테스트용 개인 데이터 제공과 폐기 지시

## 가드레일
- 키·비밀은 채팅에 적지 않는다. `.env.local`, 호스팅의 Sensitive 환경변수, `supabase/.env`에만.
- 개인 테스트 데이터는 scratchpad에만. 레포·노트·목업에는 가상 데이터.
- 마법 숫자와 비자명 로직은 사용자에게 묻고 why-주석(Business / History / Constraint / Future)을 남긴다.
- 에이전트·CLI 실행은 세션을 남기지 않는다(`--ephemeral`, `persistSession: false`).
- MCP보다 CLI: GitHub·Vercel·Supabase는 `gh`·`vercel`·`supabase`. MCP는 브라우저·데스크톱처럼 CLI가 없는 곳에만.
- 매 PR 끝에 운영 URL 상태 코드와 화면 캡처(다크/라이트, 폰/PC)를 확인한다.

## 산출물
- `.specify/memory/constitution.md`, `specs/NNN-*/spec.md`
- 운영 URL, 도메인, 분석 퍼널 정의
- 발표 노트: 서비스 / 만든 방법 / 사람 vs 자동 표
- 아키텍처 노트: 기능 흐름·시스템·ER·핵심 파이프라인 시퀀스·운영 경계 (mermaid)

## 이 초안에서 아직 없는 것
- 단계별 프롬프트 템플릿(spec 본문, PR 본문, 발표 노트)
- 실측 스크립트 공통화(Agent SDK · Codex CLI · 직접 API 호출을 같은 입력·스키마로)
- 결제 단계(사업자 등록·PG 심사)
