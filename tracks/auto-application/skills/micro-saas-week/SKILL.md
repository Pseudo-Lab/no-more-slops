---
name: micro-saas-week
description: 아이디어 한 문장에서 상용 배포까지 1주. 단계 스킬 7개(constitution-first → skeleton-on-prod → launch-basics → core-feature-with-review → model-bakeoff → glance-and-guardrails → env-split)를 이 순서로 호출하고, 매 단계 끝을 ship-loop로 닫는 조합 스킬. "일주일 안에 서비스 만들자", "MVP 출시", "새 micro-SaaS", "처음부터 배포까지"처럼 전체 트랙을 달라는 요청이면 이 스킬을 쓴다. 단계 하나만 필요하면 해당 단계 스킬을 직접 쓴다.
---

# micro-saas-week

오래오래(가족 건강검진 기록장)를 닷새 만에 배포한 트랙. 이 스킬은 **순서와 넘김만** 정한다. 각 단계의 내용은 단계 스킬에 있다.

## 입력 (시작 전에 받는다)
- 문제 한 문장: "___를 위해 ___를 만든다"
- 핵심 사용자 1명과 첫 화면 3개
- 절대 안 할 것
- 스택 기본값: Next.js App Router 서버 액션 + Supabase(RLS) + Vercel + 외부 AI 1회 호출. 다르면 `skeleton-on-prod`만 바꾼다.

## 조합

| 순서 | 스킬 | 들어오는 것 | 나가는 것 | 걸린 시간 |
|---|---|---|---|---|
| 1 | `constitution-first` | 문제 한 문장, 안 할 것 | `constitution.md` | 30분 |
| 2 | `skeleton-on-prod` | 헌법, 화면 3개 | 운영 URL + 로그인되는 빈 홈 | 하루 |
| 3 | `launch-basics` | 운영 URL, 서비스명 | 남에게 보낼 수 있는 링크, 퍼널 이벤트표 | 하루 |
| 4 | `core-feature-with-review` | 약속 한 문장, 키, 시험 입력 | 핵심 기능 PR, 프롬프트·스키마 | 하루 |
| 5 | `model-bakeoff` | 프롬프트·스키마, 정답 기준 | 비교표, 운영 모델, 남용 상한 | 반나절 |
| 6 | `glance-and-guardrails` | 제품 피드백 | 한눈에 보기, 확인 모달, 크레딧 원장 | 하루 |
| 7 | `env-split` | 콘솔 접근 | 로컬 환경 | 반나절 |
| 매 단계 끝 | `ship-loop` | 할 일 한 문장 | 이슈·spec·PR·운영 확인 | — |

순서를 바꾸지 않는 이유 두 가지: 2가 3보다 먼저여야 매 기능을 운영에서 확인하고, 3이 4보다 먼저여야 핵심 기능을 "남에게 보내도 되는 상태"에서 시험한다.

## 넘김 규칙
- 단계 스킬이 "멈추는 지점"을 내면 사용자에게 **체크리스트로** 넘기고 그 단계에서 기다린다. 다음 단계를 미리 당기지 않는다.
- 단계 산출물이 다음 단계 입력이 안 되면(예: 헌법 없이 뼈대) 되돌아가 만든다.
- 단계 안에서 생긴 버그는 그 단계에서 `ship-loop`(spec 생략)로 닫는다.

## 공통 가드레일 (모든 단계 스킬이 지킨다)
- 키·비밀은 채팅에 적지 않는다. `.env.local`, 호스팅 Sensitive, `supabase/.env`에만.
- 개인 테스트 데이터는 scratchpad에만. 레포·노트·목업에는 가상 데이터.
- 마법 숫자·비자명 로직은 묻고 why-주석(Business/History/Constraint/Future).
- 에이전트·CLI 실행은 세션을 남기지 않는다.
- MCP보다 CLI(`gh`·`vercel`·`supabase`). MCP는 브라우저·데스크톱처럼 CLI가 없는 곳에만.
- PR 머지, 운영 DB push, 운영 배포(정책에 따라)는 사람이 누른다.

## 산출물
운영 URL, 도메인, 퍼널 정의, `constitution.md`, `specs/NNN-*`, 아키텍처 노트(mermaid).

## 평가
트랙이 끝나면 `micro-saas-audit`로 단계별 산출물이 실제로 있는지 채점한다(`EVALUATION.md`). 실패 항목은 해당 단계 스킬로 되돌아가 `ship-loop`로 닫는다.

## 아직 없는 것
- 단계별 프롬프트 템플릿(spec 본문, PR 본문)
- 결제 단계(사업자 등록·PG 심사) — 2주차에 `payments-first-sale`로 추가 예정
