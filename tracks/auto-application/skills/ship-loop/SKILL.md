---
name: ship-loop
description: 기능 하나를 "이슈 1 → 브랜치 NNN-name → specs/NNN-name/spec.md → 구현 → PR(Closes 이슈 + Constitution Check) → 운영 URL 확인"으로 끝내는 가장 작은 배포 단위 루프. 새 기능·개선·버그 수정 요청을 받았을 때, "이슈 만들고 PR까지", "spec 쓰고 구현", "배포까지 해줘"처럼 끝까지 가 달라는 요청이면 사용자가 루프를 말하지 않아도 이 스킬을 쓴다. 다른 서비스 제작 스킬(skeleton-on-prod, launch-basics, core-feature-with-review …)이 매 단계 끝에 이 스킬을 호출한다.
---

# ship-loop

한 번에 하나만 올린다. 되돌릴 단위가 작아야 에이전트가 틀려도 사람이 1분 안에 되돌린다.

## 입력
- 할 일 한 문장과 "왜"(사용자 피드백, 발견한 버그, 발표에서 나온 요구).
- 헌법(`.specify/memory/constitution.md`)이 있으면 읽는다. 없으면 `constitution-first`를 먼저 권한다.

## 절차
1. **이슈** — `gh issue create`. 본문은 "## 왜 / ## 무엇 / ## 나중에" 세 절. 버그면 재현과 원인.
2. **브랜치** — `git checkout -b NNN-name main` (NNN은 다음 번호). base가 main인지 여기서 확인한다. base를 잘못 잡으면 머지돼도 운영에 안 들어간다(실제로 있었던 일).
3. **spec** — 기능이면 `specs/NNN-name/spec.md`: User Story, FR-001…, Constitution Check, 검증. 버그 수정은 spec을 생략한다.
4. **구현** — 파일 수를 spec에 적은 만큼만. 마법 숫자·비자명 로직은 사용자에게 묻고 why-주석(Business/History/Constraint/Future).
5. **검증** — tsc·eslint·build. 새 로직에는 assert 자체 점검 하나. 화면이면 헤드리스 Chrome 캡처(다크/라이트, 폰/PC).
6. **PR** — `gh pr create --base main`, 본문 "Closes #N / 무엇 / Constitution Check / 검증". 머지는 사람이 누른다(명령 한 줄을 건넨다).
7. **운영 확인** — 머지 뒤 `git pull` → 배포 명령 → 운영 URL 상태 코드와 캡처. 마이그레이션이 있으면 사람에게 `db push` 명령을 건넨다.

## 멈추는 지점 (사람 몫)
- PR 머지, 운영 DB push, (정책에 따라) 운영 배포.
- 새 마법 숫자, 제품 결정이 섞인 분기.

## 산출물
이슈 번호, 브랜치, spec 경로, PR URL, 운영 URL 확인 결과 한 줄.
