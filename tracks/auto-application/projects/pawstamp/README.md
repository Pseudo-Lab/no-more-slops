# Pawstamp — 쉬었음 PM 서비스 런칭기 #1

강아지랑 다녀온 곳에 사진을 남기는 지도 웹앱. 버튼 이름은 "꼬순내 남기기".

- **결과물**: https://pawstamp.vercel.app (설치 없이 링크로 바로 열림)
- **트랙**: Auto-Application
- **작성자**: [bea-kang](https://github.com/bea-kang)
- **제출 PR**: [#2](https://github.com/Pseudo-Lab/no-more-slops/pull/2)
- **결과물 위치**: [outputs/week-01/](outputs/week-01/README.md)
- **제작 기간**: 2026-10-09 ~ 10-10 (MVP 배포까지 약 1시간, 이후 사용자 반응 보며 고도화)
- **제작 방식**: Claude Code와 대화로 기획·구현·배포

## 무엇을 하나

| 기능 | 설명 |
|---|---|
| 사진 올리기 | 사진 속 GPS로 장소를 자동으로 찾고, 없으면 카카오 장소 검색이나 지도 클릭으로 고른다 |
| 누구랑? | 기본은 "내 강아지". "길에서 만난 친구"(길고양이 5종)는 등록 없이 올린다 |
| 지도 | 멀리서 보면 견종 캐릭터로 묶여 보이고(견종별 수), 가까이 가면 사진 핀 |
| 같이 남기기 | 하트, 같은 장소에 "우리도 꼬순내 남기기" |
| 강아지 프로필 | 21종 견종 캐릭터 + 기타·믹스, 등록 후 수정 가능 |
| 안전장치 | 욕설 필터(브라우저 + DB 트리거), 사람 얼굴 자동 모자이크, 길고양이 위치 100m 흐리게, 사진 저장 막기 |

## 제작 코드

```
app/
  src/main.js         화면·지도·올리기 흐름
  src/map.js          카카오맵 래퍼 (마커, 장소 검색)
  src/store.js        Supabase 저장소 (키가 없으면 localStorage)
  src/moderation.js   욕설 필터, 얼굴 감지·모자이크 (MediaPipe)
  src/breeds.js       견종·고양이 프리셋과 캐릭터 이미지
  supabase/schema.sql 테이블, RLS, 하트·수정 RPC, 욕설 트리거
CHARACTER_PROMPTS.md  견종 캐릭터 이미지 생성 프롬프트 27종
content/              인스타 카드뉴스 HTML 템플릿(레슨런, 감성 소개), 릴스 영상 스크립트
outputs/week-01/      결과물 안내, 최종 카피(LESSONS-insta.md), 주차별 최종 제출 위치
LESSONS.md            만들면서 배운 것 (상세)
DECISIONS.md          로그인·얼굴 처리 의사결정 메모
```

스택: Vite(바닐라 JS) · Supabase(Postgres + Storage) · Kakao Maps JS SDK · MediaPipe Face Detector · Vercel

## 재현 방법

```bash
cd app
npm install
npm run dev          # .env 없으면 브라우저 저장소 모드로 바로 실행
```

여럿이 같이 쓰려면:

1. Supabase 프로젝트를 만들고 SQL Editor에서 `supabase/schema.sql` 실행
2. 카카오 개발자 콘솔에서 앱 생성 → JavaScript 키 발급 → 사이트 도메인(로컬·배포 주소) 등록 → 카카오맵 사용 설정 ON
3. `.env.example`을 `.env`로 복사해 세 값 입력 (`VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_KAKAO_MAP_KEY`)
4. `npx vercel deploy --prod`

카드뉴스와 릴스:

1. `content/deck.html?t=A&d=lesson&s=1`(레슨런), `content/deck-intro-emotional.html?s=1`(소개)을 1080×1350으로 캡처 (헤드리스 크롬 `--screenshot`)
2. `python3 content/reel/frames.py <폴더> '#161413' slide1.png:2.5 slide2.png:6 ...` 로 9:16 프레임과 목록 생성
3. `mkdir -p outputs/week-01` 후 `swiftc content/reel/mkvideo.swift -o <폴더>/mkvideo && <폴더>/mkvideo <폴더>/manifest.txt outputs/week-01/reel.mp4` (ffmpeg 없이 macOS AVFoundation으로 mp4 생성)

카드뉴스 템플릿이 참조하는 사진은 저작권·개인정보 때문에 포함하지 않았다. 앱에서 사용하는 견종 캐릭터 파일은 `app/src/assets/characters/`에 포함되어 있다. 완성한 카드뉴스 PNG와 릴스 MP4를 추가 제출할 때는 `outputs/week-01/`에 두고 이 폴더의 README에 기록한다.

## 지표 (2026-10-10 기준, 지인 대상 공개 첫날)

| 지표 | 값 |
|---|---|
| 등록된 장소 | 8 |
| 올라온 사진(꼬순내) | 9 |
| 등록된 강아지 | 8 |
| 강아지를 등록한 기기 | 7 |
| 하트 | 4 |
| MVP 첫 배포까지 | 약 1시간 (목표 30분) |
| 커밋 / 코드 | 19개 / 약 1,600줄 |

다음에 볼 지표: 첫 방문 → 첫 사진 업로드 전환율, 같은 장소 "같이 남기기" 비율, 업로드 실패율(폰 인앱 브라우저).

## 레슨런 요약

1. **조립 과정에서 커지는 비즈니스가 있다** — 저장(Supabase), 지도(카카오), 배포(Vercel)를 다 빌려서 조립했다. 조립을 돕는 인프라(API·BaaS) 사업이 잘되겠다.
2. **제일 쉬운 길을 우선 찾는 AI** — 기준 없이 맡기니 키 없이 바로 붙는 지도를 골랐다. 품질 기준과 "가입·키 발급은 내가 할게"를 같이 줘야 한다.
3. **쌓여야 보이는 기능은 뒤로 미루기** — 동네 인기 견종, 인기 장소는 데이터가 쌓인 뒤로.
4. **엣지 케이스 대응** — 링크를 받자마자 욕설과 얼굴 사진이 들어왔다. 욕설 필터, 얼굴 모자이크, 길고양이 위치 흐리기를 추가했다.

자세한 내용은 [LESSONS.md](LESSONS.md).

## 동료 리뷰

리뷰어를 지정해 이 PR에서 받는다.

---

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
