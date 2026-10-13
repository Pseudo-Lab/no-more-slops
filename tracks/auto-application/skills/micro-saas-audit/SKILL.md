---
name: micro-saas-audit
description: micro-saas-week(단계 스킬 7개 + ship-loop)로 만든 서비스를 각 단계의 산출물 기준으로 채점한다. 코드·마이그레이션·PR 메타데이터·운영 URL에서 scripts/audit.sh로 증거를 모으고, 증거가 있는 항목만 통과/실패로 적고 나머지는 미확인으로 둔다. "프로젝트 평가해줘", "제출 전 점검", "뭐가 빠졌는지 봐줘", "리뷰 받기 전에 확인"처럼 만든 결과물을 평가하라는 요청이면 이 스킬을 쓴다. 산출물은 EVALUATION.md(항목별 판정 + 증거 + 되돌아갈 스킬).
---

# micro-saas-audit

만드는 스킬 7개가 각각 "나가는 것"을 약속한다. 이 스킬은 그 약속이 **지금 레포와 운영 URL에 실제로 있는지**만 본다. 인상 평가는 하지 않는다.

## 입력
- 레포 경로(헌법 `.specify/memory/constitution.md`, `specs/`, `supabase/migrations/`, `src/`가 있는 곳), 운영 URL.
- `gh`가 그 레포에 로그인돼 있을 것(PR·이슈 메타데이터).
- 제출 문서가 레포 밖에 있으면 그 경로(비교표·퍼널표를 거기서 찾는다).

## 절차
1. **증거 수집** — `scripts/audit.sh <레포> <운영 URL>`. 한 줄에 사실 하나(`항목: 값`)만 찍는다. 느린 항목은 tsc·lint·git 히스토리 검색뿐이다.
2. **채점** — 아래 표의 기준으로 항목마다 통과 / 실패 / 미확인 중 하나. 판정 옆에 스크립트 출력 한 줄을 그대로 붙인다. 스크립트로 못 보는 항목(목업 승인, 법률 검토, 실제 GA 수집)은 미확인으로 두고 사람 몫에 적는다.
3. **실패마다 되돌아갈 스킬** — 실패는 그 단계 스킬 이름과 고칠 일 한 문장으로 끝낸다. 점수를 매기지 않는다. 통과 n / 실패 n / 미확인 n만 센다.
4. **보고서** — `EVALUATION.md`: 요약 세 줄(가장 큰 실패, 바로 고칠 것, 사람 몫) → 단계별 표 → 사람 몫 체크리스트. 보고서는 deslop-ko로 한 번 점검한다.

## 채점표

| 단계 | 항목 | 통과 기준 |
|---|---|---|
| 1 constitution-first | C1 | 헌법 파일이 있고 "안 할 것"(MUST NOT)이 1개 이상 |
| | C2 | 모든 `specs/*/spec.md`에 Constitution Check 절 |
| | C3 | 머지된 PR 본문에 Constitution Check |
| 2 skeleton-on-prod | S1 | 운영 URL의 로그인 페이지 200 |
| | S2 | `create table` 수 = `enable row level security` 수 |
| | S3 | `src/`에 service_role 문자열 없음 |
| | S4 | tsc·lint 통과 |
| 3 launch-basics | L1 | /terms /privacy 200, 처리방침에 "무엇을 저장하지 않는지" |
| | L2 | 탈퇴 RPC(security definer) |
| | L3 | error.tsx · not-found.tsx |
| | L4 | 선언한 퍼널 이벤트가 전부 `track()` 호출됨, 경로 마스킹 |
| | L5 | HSTS, OG 이미지 200 |
| 4 core-feature-with-review | F1 | AI 출력 `json_schema strict` + `store:false` |
| | F2 | 저장 전 확인 화면(사람이 고친 값으로 저장) |
| | F3 | 원본 저장 호출 없음, 결과지 파일이 git에 없음 |
| | F4 | 키 없이 로컬 샘플 모드 |
| 5 model-bakeoff | M1 | 같은 입력으로 3개 이상 모델 비교표가 **레포 안에** 있음 |
| | M2 | 운영 모델과 건당 비용이 적혀 있음 |
| | M3 | 남용 상한 RPC(일일 한도 또는 크레딧) |
| 6 glance-and-guardrails | G1 | `glance()` 순수 함수 하나가 점·문장·개수를 만듦 |
| | G2 | 삭제·탈퇴·로그아웃이 `<dialog>` 확인 컴포넌트를 씀 |
| | G3 | 크레딧은 원장(delta 합) + advisory lock |
| 7 env-split | E1 | `.env.example` + `.env.development.local` |
| | E2 | 로컬 Supabase에 로그인 provider 설정 |
| | E3 | 로컬 env에 운영 AI 키 없음 |
| ship-loop | P1 | 머지된 PR 전부 base = main |
| | P2 | PR 본문에 `Closes #N` |
| | P3 | 브랜치 `NNN-name` |
| | P4 | 기능 PR마다 spec (버그 수정은 제외) |
| | P5 | 끝난 일이 열린 이슈로 남아 있지 않음 |
| 공통 가드레일 | X1 | git 히스토리에 비밀 키 패턴 없음 |
| | X2 | why-주석(Business/History/Constraint/Future) 있음 |
| | X3 | 자동 테스트 또는 assert 자체 점검 |

## 멈추는 지점 (사람 몫)
- 약관·처리방침 법률 검토, 목업·"주의" 기준 승인, 실제 GA 수집 확인(로그인 필요), 운영 모델 비용의 월 상한.
- 실패 항목을 지금 고칠지 다음 주로 넘길지.

## 산출물
`EVALUATION.md` — 통과/실패/미확인 수, 실패마다 되돌아갈 스킬, 사람 몫 체크리스트. 고치기로 한 항목은 `ship-loop`로 하나씩.
