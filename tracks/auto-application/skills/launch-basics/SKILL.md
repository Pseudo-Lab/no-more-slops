---
name: launch-basics
description: 남에게 링크를 보내도 되는 상태를 만든다 — 랜딩, 이용약관, 개인정보 처리방침, 탈퇴(Storage 파일 → 계정 삭제 두 단계), 에러·빈 화면, 퍼널 지표(외부 분석 도구 없이 우리 DB에 단계 이름만), 도메인·OG 이미지. "약관 써 줘", "처리방침", "탈퇴 기능", "GA 달자", "퍼널 이벤트", "도메인 연결", "출시 준비"처럼 상용 기본기 요청이면 이 스킬을 쓴다. 뼈대가 운영에 올라간 직후, 핵심 기능보다 먼저 하는 게 기본 순서다. 끝나면 scripts/check-launch.mjs로 운영 URL을 점검한다.
---

# launch-basics

핵심 기능보다 먼저 한다. 이게 있어야 다음 날부터 매 기능을 "진짜 사용자에게 보내도 되는 상태"에서 확인한다.

## 입력
- 헌법(데이터·동의 원칙), 운영 URL, 서비스명(사람 결정), 개인정보 담당 표기 방식(사람 결정), 지표를 어디에 모을지(사람 결정: 우리 DB / Vercel Analytics / GA).

## 절차
1. **랜딩** — 문제 한 문장 + 약속 한 문장 + 로그인 버튼. OG 이미지 1장.
2. **약관·처리방침** — 적용 법령(개인정보 보호법 제30조 기재 사항, 제28조의8 국외 이전 공개)을 WebFetch로 확인하고 초안. 처리방침에는 **받는 정보 표**(언제 / 무엇 / 어디에 쓰나)와 **받지 않는 정보** 절을 따로 둔다. 호스팅 Supabase·Vercel처럼 해외 회사 서버를 쓰면 서울 리전이라도 국외 이전 표(받는 곳·맡긴 일·옮겨지는 정보·연락처)를 넣는다. AI 비서(MCP) 연결이 있으면 "사용자가 고른 AI 서비스의 방침이 함께 적용된다"를 적는다. 가입 화면 버튼 아래에 "시작하면 약관·처리방침에 동의한 것으로 봐요" 한 줄.
3. **탈퇴** — Supabase Storage 파일은 SQL에서 지울 수 없다. 그래서 두 단계: ① `my_video_paths()`(security definer, 내 파일 경로만) → 앱이 `storage.remove()` ② `delete_my_account()`가 `delete from auth.users where id = auth.uid()` → profiles부터 `on delete cascade`. 파일 삭제가 실패하면 계정은 그대로 두고 알린다. 되돌릴 수 없는 동작이므로 확인 모달. 템플릿: [references/launch-basics.template.sql](references/launch-basics.template.sql).
   - 함수 권한은 `revoke … from public, anon, authenticated` 뒤 `grant … to authenticated`. Supabase는 public 스키마 새 함수에 anon·authenticated 실행 권한을 따로 주기 때문에 `from public`만으로는 안 막힌다.
4. **에러·빈 화면** — `error.tsx`(저장 중이던 기록이 들어갔는지 다시 확인하라는 문구), `not-found.tsx`(초대 링크가 깨졌을 때를 안내), 빈 목록 문구.
5. **퍼널 지표** — 단계마다 이벤트 1개(랜딩 → 로그인 시작 → 가입 → 핵심 행동 → 저장 → 공유). `track(step)` 헬퍼 하나, 실패는 버린다(지표 때문에 화면이 멈추면 안 된다). 보내는 건 단계 이름뿐: 이름·수치·id 금지.
   - 기본값은 **우리 DB**: `events(step check(...), at)` 테이블, insert 정책만(anon·authenticated), select 정책 없음, 숫자는 운영자 함수 `admin_funnel()`로만. 외부 서비스·쿠키가 없어 처리방침이 짧아지고 바로 된다. 한계: 로그인 없이 넣을 수 있어 부풀릴 수 있다(사람이 늘면 하루 상한이나 서버 경유).
   - GA·Vercel Analytics를 고르면 처리방침에 쿠키·국외 이전 항목을 더하고 속성 id는 사람이 만든다.
   - dev에서는 React StrictMode가 effect를 두 번 돌려 랜딩 이벤트가 2건 찍힌다. 운영은 1건.
6. **도메인** — 등록은 사람, DNS 레코드 값은 Claude가 만들고 `vercel api`로 TXT 검증.
7. **점검** — `node scripts/check-launch.mjs <운영 URL> --env .env.production.local` 로 약관·처리방침 200, "받지 않는 정보" 문구, 문의 mailto, 사용자 정의 404, HSTS, 지표 넣기 가능·읽기 차단, 탈퇴 함수 익명 호출 차단을 한 번에 본다. 마이그레이션 → 배포 순서를 지킨다(마이그레이션이 빠지면 화면이 아니라 링크·버튼이 깨진다).
8. 각 항목은 `ship-loop`로 PR 하나씩.

## 멈추는 지점 (사람 몫)
- 서비스명, 개인정보 담당 표기(개인 메일을 공개할지), 지표를 어디에 모을지, 도메인 등록·DNS 입력, 약관·처리방침 법률 검토.

## 산출물
남에게 보낼 수 있는 링크, 퍼널 이벤트 정의표(단계 ↔ 이벤트명), `check-launch.mjs` 출력(항목별 ok/FAIL). 다음 단계는 `core-feature-with-review`.
