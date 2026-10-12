# 평가 — micro-saas-audit로 본 오래오래 (2026-10-12)

> [skills/micro-saas-audit/SKILL.md](skills/micro-saas-audit/SKILL.md)의 채점표 33항목을 비공개 저장소(main 9bf8310)와 운영 URL에 적용한 결과. 증거는 `scripts/audit.sh`가 찍은 줄을 그대로 옮겼고, 스크립트로 볼 수 없는 것은 사람 몫에 두었다.

**통과 25 · 실패 8 · 미확인 3**

- 가장 큰 실패: 과정 기록이 코드보다 늦게 따라왔다. 헌법 비준(10/10) 전에 쓴 spec 3개와 PR 13개에 Constitution Check가 없고, 모델 비교표는 제출 README에만 있고 저장소 안에는 없다.
- 바로 고칠 것: spec 3개에 Constitution Check 절 추가, 비교표를 `specs/001-ai-sheet-extraction/bakeoff.md`로 이동, 끝난 이슈 #2 · #3 닫기. 셋 다 코드 변경이 없어 30분 안에 PR 하나로 끝난다.
- 사람 몫: 약관·처리방침 법률 검토(#19), 로그인 뒤 GA4 수집 확인(#20), OpenAI 월 한도 수치.

## 1 constitution-first

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| C1 헌법 + 안 할 것 | 통과 | `exists, MUST NOT=3` (원본 미저장 · 분석 데이터 금지 · 진단 금지) | |
| C2 spec마다 Constitution Check | 실패 | `001-ai-sheet-extraction 002-privacy-officer 003-custom-domain` 3개 누락 (헌법 비준 전 작성) | constitution-first: 세 spec에 절 추가 |
| C3 PR 본문 Constitution Check | 실패 | 머지 16개 중 13개 누락 (`43 42 40 38 36 34 32 30 28 25 23 22 21`), #45부터 적용 | ship-loop 6단계 본문 틀 |

## 2 skeleton-on-prod

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| S1 운영 로그인 페이지 | 통과 | `/login 200` (`/`는 `/login?next=/`로 307) | |
| S2 테이블 = RLS | 통과 | `8 tables / 8 rls` | |
| S3 service_role 없음 | 통과 | `src`에 `none` | |
| S4 tsc · lint | 통과 | `tsc pass`, `lint pass` | |

## 3 launch-basics

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| L1 약관 · 처리방침 | 통과 | `/terms 200 /privacy 200`, 처리방침에 "저장하지 않" 3곳 | |
| L2 탈퇴 RPC | 통과 | `20261010000000_account_lifecycle.sql` security definer | |
| L3 에러 · 빈 화면 | 통과 | `error.tsx not-found.tsx` | |
| L4 퍼널 이벤트 전부 연결 | 통과 | 선언 10개 중 미호출 0, 경로 마스킹(`/member/:id`, `/join/:code`) | |
| L5 HTTPS · OG | 통과 | `hsts=1 og=200` | |

## 4 core-feature-with-review

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| F1 스키마 strict · store:false | 통과 | `extract.ts`: `strict: true`, `store: false` | |
| F2 저장 전 확인 화면 | 통과 | `upload-form.tsx` → `review-form.tsx`, 사람이 고친 값으로 `saveExam` | |
| F3 원본 미저장 | 통과 | `storage calls: 0, pdf in git: 0` | |
| F4 키 없이 샘플 모드 | 통과 | `OPENAI_API_KEY` 없으면 `SAMPLE_EXTRACTED` 반환 | |

## 5 model-bakeoff

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| M1 비교표가 저장소 안에 | 실패 | 저장소 `*.md`에 모델 행 0줄. 표는 제출 README에만 | model-bakeoff: `specs/001-ai-sheet-extraction/bakeoff.md`로 이동 |
| M2 운영 모델 · 건당 비용 | 통과 | 제출 README: gpt-5.6-luna, 전수 추출 ≈ 25원/건 | |
| M3 남용 상한 | 통과 | `take_extract_quota`(일일) + `spend_credit`(크레딧) RPC | |

## 6 glance-and-guardrails

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| G1 glance() 순수 함수 | 통과 | `src/lib/health.ts:35 export function glance` | |
| G2 되돌릴 수 없는 동작에 확인창 | 통과 | `ConfirmButton` 사용 4화면 (설정 · 탈퇴 · 구성원 · 구성원 편집) | |
| G3 크레딧 원장 + lock | 통과 | `sum(delta)` 2곳, `pg_advisory_xact_lock` 1곳 | |

## 7 env-split

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| E1 env 파일 | 통과 | `.env.development.local .env.example` | |
| E2 로컬 Supabase provider | 통과 | `config.toml`에 kakao 1곳 | |
| E3 로컬에 운영 키 없음 | 통과 | `.env.development.local`에 `OPENAI_API_KEY` 0 (Codex SDK 경로) | |

## ship-loop

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| P1 PR base = main | 실패 | `#36 -> 009-credits`. 판독 대기 화면이 운영에 못 들어가 #46으로 다시 올림 | ship-loop 2단계 (base 확인) — 규칙은 이미 추가됨 |
| P2 Closes #N | 실패 | `43 23 21` 3개 누락 | ship-loop 6단계 |
| P3 브랜치 NNN-name | 통과 | 어긋난 브랜치 0 | |
| P4 기능 PR마다 spec | 실패 | spec 10개 / PR 16개. 기능인데 spec 없는 PR: #43(로컬 DB 분리), #48(Codex 로컬 판독) | ship-loop 3단계 |
| P5 끝난 이슈가 열려 있지 않음 | 실패 | 열린 7개 중 #2(AI 판독 연결 — #21로 완료), #3(퍼널 이벤트 — 구현 완료, 측정만 남음) | ship-loop 1단계: 닫거나 "측정" 이슈로 교체 |

## 공통 가드레일

| 항목 | 판정 | 증거 | 되돌아갈 곳 |
|---|---|---|---|
| X1 히스토리에 비밀 키 없음 | 통과 | `sk-` · `sb_secret_` 패턴 0 | |
| X2 why-주석 | 통과 | Business/History/Constraint/Future 34개 | |
| X3 자동 테스트 | 실패 | 테스트 디렉터리 없음. tsc · lint · 헤드리스 캡처만 | ship-loop 5단계: 새 로직마다 assert 자체 점검 (glance · trends · 크레딧 RPC부터) |

## 사람 몫 (미확인 3)

- [ ] 약관 · 개인정보 처리방침 법률 검토 — 이슈 #19
- [ ] 로그인 뒤 가입 → 업로드 → 저장 → 탈퇴 흐름과 GA4 수집을 운영 URL에서 확인 — 이슈 #20
- [ ] OpenAI 월 사용 한도 수치 결정 (크레딧은 계정당 3회, 일일 한도 RPC는 있음)

## 고치는 순서

1. `ship-loop` 한 번: spec 3개에 Constitution Check, 비교표 이동, 이슈 #2 · #3 정리 (코드 변경 없음)
2. `ship-loop` 한 번: `health.ts`의 glance · trends에 assert 자체 점검 파일 추가
3. 다음 주 트랙부터 PR 본문 틀(Closes + Constitution Check)과 spec 생략 기준(버그 수정만)을 ship-loop 그대로 따른다

---
This work was created as part of the No-More-Slops group activities at Pseudo Lab.
