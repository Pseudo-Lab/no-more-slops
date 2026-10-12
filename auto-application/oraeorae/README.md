# 오래오래 — 가족 건강검진 기록장

가족의 건강검진 결과지(사진·PDF)를 올리면 AI가 수치·판정·소견을 읽어 주고, 사람이 확인해 저장하면 가족끼리 함께 보는 웹 서비스.

- **서비스**: https://oraeorae.kro.kr (카카오 로그인, 모바일 우선)
- **기간**: 2026-10-07 ~ 10-12 (1주차)
- **스택**: Next.js 16 App Router · Supabase(서울, RLS) · Vercel · OpenAI Responses API · GA4
- **코드**: `app/` — 개발은 비공개 저장소에서 하고, 제출 때마다 `git archive origin/main`으로 스냅샷을 이 폴더에 미러한다.

## 문제
부모님 검진 결과는 종이와 PDF로 흩어져 있고, 걱정하는 자녀가 모아서 보기 어렵다. 공공 앱(나의건강기록)은 본인 열람용이라 성인 가족끼리 계속 함께 보는 기능이 없다.

## 흐름
카카오 로그인 → 동의 3종(민감정보·가족 공유·국외 이전) → 가족 만들기 / 초대 링크 → 결과지 올리기 → AI 판독(크레딧 1회) → 확인·수정 → 가족 홈(사람마다 점 하나 + 한 문장) → 사람 화면(주의 항목·참고치 막대·소견·연도별 추이)

## 원칙 (헌법)
1. 건강정보 최소화: 원본 결과지는 저장하지 않는다. 분석 도구에는 단계 이름만 보낸다.
2. 처리 전 동의: 민감정보·가족 공유·국외 이전(OpenAI) 각각 따로.
3. 기록만, 진단 안 함: 판정·H/L·참고치는 결과지에 인쇄된 것만 옮긴다.
4. 경계 보안: RLS + security definer RPC, service-role 클라이언트 없음.
5. 가장 작은 배포 단위: 이슈 1 = 브랜치 1 = spec 1 = PR 1, 매번 운영 URL 확인.

## 재현 방법
```bash
cd app && npm install
cp .env.example .env.local        # Supabase URL·publishable key (OPENAI_API_KEY 없으면 예시 값 모드)
npx supabase start                # 로컬 DB + 마이그레이션 8개 (Docker 필요)
npm run dev                       # http://localhost:3200
```
카카오 로그인은 Kakao Developers 앱의 REST API 키·Client Secret을 `supabase/.env`에 넣고 Redirect URI `http://127.0.0.1:54321/auth/v1/callback`을 등록해야 동작한다. 자세한 것은 `app/README.md`.

## 써 보기
1. https://oraeorae.kro.kr 에서 카카오 로그인 → 동의 → 가족 만들기.
2. 결과지 올리기에서 검진 결과지 사진이나 PDF 선택(36쪽 종합검진 PDF도 됨). 새 계정은 판독 3회.
3. 확인 화면에서 틀린 값을 고치거나 지우고 저장 → 가족 홈과 사람 화면 확인.
4. 설정 → 탈퇴로 모든 데이터 삭제.

테스트용 결과지가 없으면 OpenAI 키 없이 돌아가는 예시 값 모드가 있어 흐름은 볼 수 있다(운영에서는 실제 판독).

## 1주차 기술 포인트
- **긴 PDF를 휴대폰에서 처리**: pdfjs로 전체 쪽 글자 추출, 주민번호 가림, 결과가 가장 많은 쪽 + 글자 없는 쪽만 이미지(≤4MB). 7.6MB PDF가 수백 KB로.
- **판독 규칙**: 인쇄된 것만, 판정은 체크된 칸에서만, 한 칸에 검사 여러 개면 항목을 나눔. 모델이 참고치로 "정상"을 지어내던 문제를 규칙으로 막음.
- **전수 추출**: 국가검진 17개 항목만 읽던 것을 결과지의 모든 항목(종합검진 약 137개 + 소견 12개)으로 확장. 저장 스키마는 항목 종류를 가리지 않게 변경.
- **모델 실측** (같은 결과지, 17개 항목 기준):

| 모델 | 수치 | 판정 | 건당 비용 | 경로 |
|---|---|---|---|---|
| gpt-5.6-luna | 17/17 | 17/17 | ≈ 5원 (전수 추출은 ≈ 25원) | OpenAI API, Codex CLI |
| gpt-5.4-mini | 17/17 | 16~17/17 | ≈ 19원 | OpenAI API |
| gpt-6-sol | 17/17 | 17/17 | — | Codex CLI |
| Claude Sonnet 5.5 | 17/17 | 17/17 | — | Agent SDK |
| Claude Haiku 4.5 | 17/17 | 14/17 | — | Agent SDK |

→ 운영은 gpt-5.6-luna. 남용은 계정당 크레딧(가입 3회)과 OpenAI 월 한도로 막는다.

- **한눈에 보기 UI**: Function Health·건강보험공단 결과 조회·Apple Health 건강 기록의 공통 패턴(범위 밖 개수부터, 신호등 한 점, 참고 범위 막대 + 내 값 점, 나머지 접기)을 적용.

## 지표
실사용자 모집 전이라 숫자 대신 **측정 준비 상태**를 낸다. GA4 퍼널 이벤트(단계 이름만, 건강정보·id 없음):

| 단계 | 이벤트 |
|---|---|
| 랜딩 방문 | `page_view` |
| 카카오 로그인 | `login_click` |
| 가족 만들기 / 참여 | `family_create` / `family_join` |
| 결과지 선택 → 제출 | `upload_file_selected` → `upload_submit` |
| 판독 실패 | `extract_error` |
| 저장 | `exam_save` / `exam_save_error` |
| 초대(확산) | `invite_share` / `invite_copy` |

제작 지표: 커밋 53, PR 16, 이슈 32, spec 10, 스킬 9, 판독 비용 ≈ 25원/건.

## 문서
- `app/` — 서비스 전체(소스, Supabase 마이그레이션, spec-kit 헌법·spec 9개, 이슈 노트)
- [ARCHITECTURE.md](ARCHITECTURE.md) — 기능 흐름·시스템·데이터 모델·판독 파이프라인·운영 경계 다이어그램
- [PROCESS.md](PROCESS.md) — 1주 제작 트랙: 단계별로 사람이 한 것 / Claude가 스킬·CLI·MCP로 한 것
- `skills/micro-saas-week/SKILL.md` — 위 트랙을 스킬 8개의 **조합**으로 쓴 것. 단계 스킬 7개를 순서대로 호출하고 매 단계 끝을 `ship-loop`로 닫는다
- 단계 스킬: [`constitution-first`](skills/constitution-first/SKILL.md) → [`skeleton-on-prod`](skills/skeleton-on-prod/SKILL.md) → [`launch-basics`](skills/launch-basics/SKILL.md) → [`core-feature-with-review`](skills/core-feature-with-review/SKILL.md) → [`model-bakeoff`](skills/model-bakeoff/SKILL.md) → [`glance-and-guardrails`](skills/glance-and-guardrails/SKILL.md) → [`env-split`](skills/env-split/SKILL.md), 공통 [`ship-loop`](skills/ship-loop/SKILL.md). 각각 입력 / 절차 / 멈추는 지점(사람 몫) / 산출물이 있어 단독으로도 쓴다

## 다음 주
- 결제: 토스페이먼츠로 크레딧 구매(5회 3,000원 / 10회 5,000원), 사업자·통신판매업 신고 선행
- 판독 정확도 평가 세트(여러 병원 양식)와 운영 실측
- 지인 가족 대상 첫 사용자 모집 → 퍼널 숫자

---
This work was created as part of the No-More-Slops group activities at Pseudo Lab.
