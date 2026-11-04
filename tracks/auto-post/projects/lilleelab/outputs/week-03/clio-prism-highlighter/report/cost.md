# 비용 기록

단계마다 한 줄씩 남긴다. 웹이 이 표를 합산한다. 모르는 칸은 비워 둔다.
비용(USD)은 유료 API를 쓴 경우만 적고, 구독·무료 도구는 0으로 적는다.

| 날짜 | 단계 | 역할 | 도구/모델 | 입력 토큰 | 출력 토큰 | 생성 건수 | 비용(USD) | 소요(분) | 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-19 | 제품 분석·특징 추출·트렌드/레퍼런스·스토리라인 3안 | planner (서브에이전트) | Claude (구독), WebSearch/WebFetch, 헤드리스 Chrome, ffmpeg(상세 이미지 확인용 이어붙이기) | | | 0 (생성 없음) | 0 | 30 | 올리브영 goodsNo A000000218380 확인, 상세 이미지·고시 열람. 유료 API 없음. 토큰 미계측 |
| 2026-10-19 | 스토리라인 v2 (계정관리 검토 반영: 리빌 5초로, No.03과 세계 나누기, 화면 글자 교체, 레퍼런스 링크 5개) | planner (서브에이전트) | Claude (구독) | | | 0 (생성 없음) | 0 | 10 | 유료 API 없음. 토큰 미계측 |
| 2026-10-19 | 스토리라인 v3 (19초 8비트 꿈 사슬, 레퍼런스 장치 조사, 대안 B 18초 맞춤) | planner (서브에이전트) | Claude (구독), WebSearch/WebFetch (인스타 페이지 글만) | | | 0 (생성 없음) | 0 | 25 | 유료 API 없음. 영상 내려받기 없음. 토큰 미계측 |
| 2026-10-20 | 콘티 v1 (12컷 19초, 컷 표·통과 기준·대체, 시트 2장: 전체 + 휴대폰 크기 확인) | storyboard-artist (서브에이전트) | Claude (구독), Python SVG + headless Chrome(puppeteer-core) | | | 0 (생성 없음, 그림만) | 0 | 40 | 호수 06 → 04 그레이스 오팔 반영(작업 중 사람 결정). 유료 API·Blender 렌더 없음. 토큰 미계측 |
| 2026-10-20 | 콘티 v2 (PM 라운드 1 반영: 광구 주인공, 실물 무늬 지형, 로고·홀로그램 재현, 11컷, 휴대폰 확인 재실행) | storyboard-artist (서브에이전트) | Claude (구독), Python SVG + headless Chrome(puppeteer-core), ffmpeg(확인용 자르기) | | | 0 (생성 없음, 그림만) | 0 | 45 | 유료 API·Blender 렌더 없음. 리뷰 사진은 보기만. 토큰 미계측 |
| 2026-10-20 | 콘티 v3 (PM 라운드 2 반영: 훅 구도·꽃잎 돌기·파편 고리·반짝임 규칙·제작 경로, 휴대폰 확인 재실행, storyboard-v2.md 보관) | storyboard-artist (서브에이전트) | Claude (구독), Python SVG + headless Chrome(puppeteer-core), ffmpeg(확인용) | | | 0 (생성 없음, 그림만) | 0 | 35 | 유료 API·Blender 렌더 없음. 토큰 미계측 |
| 2026-10-20 | 콘티 v4 (사람 방향 전환 "몽환적이고 반짝거리는": 꿈을 찍은 사진 룩, 진주 주인공, 오르골·하트 병·지퍼 꿈 장면, 생성형+Blender 합성 계획, 휴대폰 확인, research.md 레퍼런스 메모, storyboard-v3.md 보관) | storyboard-artist (서브에이전트) | Claude (구독), Python SVG + headless Chrome(puppeteer-core), ffmpeg(확인용) | | | 0 (생성 없음, 그림만) | 0 | 50 | 유료 API·Blender 렌더 없음. 레퍼런스 스크린숏은 보기만. 토큰 미계측 |
| 2026-10-20 | 콘티 v4.1 (PM 라운드 3 반영: 레퍼런스 소재 → 손거울·젤리·로켓, 진주는 케이스 밖, 컷 1·6·7·9 수정, 휴대폰 확인, storyboard-v4.md 보관) | storyboard-artist (서브에이전트) | Claude (구독), Python SVG + headless Chrome(puppeteer-core), ffmpeg(확인용) | | | 0 (생성 없음, 그림만) | 0 | 40 | 유료 API·Blender 렌더 없음. 토큰 미계측 |
| 2026-10-20 | 콘티 v4.2 (PM 라운드 4: 컷 3 진주 테두리 위, 컷 5 젤리 원석 + 보석 쟁반, 컷 6 로켓 15~20° 부감·뚜껑 실루엣·늘어진 체인, 손거울 반사 상 금지, 휴대폰 확인 11/11, storyboard-v4.1.md 보관) | storyboard-artist (서브에이전트) | Claude (구독), Python SVG + headless Chrome(puppeteer-core), ffmpeg(확인용) | | | 0 (생성 없음, 그림만) | 0 | 25 | 유료 API·Blender 렌더 없음. 토큰 미계측 |
| 2026-10-20 | 게시글 (릴스·사진 캡션, 훅 대안 2, 사진 본문 대안 1, 프로필·스토리 문구) | copywriter (서브에이전트) | Claude (구독) | | | 0 (생성 없음) | 0 | 10 | 콘티 v4.2 기준 초안(G2 전). S1·S2 문구만, 새 출처 없음. 유료 API 없음. 토큰 미계측 |
| 2026-10-20 | 제작 준비 (제품 모델·대조 렌더, 룩 합성 파이프라인, 생성형 키트, 컷 뼈대 8개, 효과음 큐, production.md) | producer (서브에이전트) | Claude (구독), Blender 5.2 Cycles GPU(확인용 저해상도만), ffmpeg, numpy(Blender 내장) | | | 0 (AI 생성 없음) | 0 | 120 | Blender 확인 렌더 합계 약 10분(정지 약 20장 + 키프레임 약 30장, 모두 저해상도). 룩 시험 약 3분. 유료 API 없음. 토큰 미계측 |
| 2026-10-22 | 생성형 첫 프레임·컷 5 Flow | main session | Gemini 무료, Flow(보유 크레딧) | | | 이미지 5, 영상 1 | 0 | 30 | 유료 API 없음 |
| 2026-10-22 | 제작: 모델 v2 (조정자 검토 반영) + 시험 컷 8·3 Blender 렌더 + 룩 합성 + 글자 ② | producer (서브에이전트) | Claude (구독), Blender 5.2 Cycles GPU, ffmpeg, numpy, puppeteer(글자) | | | 0 (AI 생성 없음) | 0 | 190 | 렌더: 컷 8 85분(66프레임 64샘플, 볼륨) + 중단분 6분, 컷 3 31분(45프레임), 확인 렌더 약 12분. 합성 약 6분. 유료 API 없음. 토큰 미계측 |
| 2026-10-22 | 제작 라운드 2 준비 (QC 시험 3컷 라운드 1 반영: 진주·팬·광채·눈·배경판 합성·카메라 뒤집힘·심도) + 확인 프레임 | producer (서브에이전트) | Claude (구독), Blender 5.2 Cycles GPU(540×960 확인만), ffmpeg, numpy | | | 0 (AI 생성 없음) | 0 | 60 | Blender 확인 렌더 약 5분. 본 렌더는 조정자 확인 뒤 (예상 컷 8 약 85분 + 컷 3 약 31분). 유료 API 없음 |
| 2026-10-23 | 제작 라운드 3–4 (무늬 v3, 컷 8·3 라운드 3 + 예외 재렌더, 컷 9·7 첫·두 번째 렌더, Flow용 정지 v3–v6, 합성 수정) | producer (서브에이전트) | Claude (구독), Blender 5.2 Cycles GPU, ffmpeg, numpy | | | 0 (AI 생성 없음) | 0 | 900 | 본 렌더: 컷 8 ×3(약 65–70분씩), 컷 3 ×2(약 32분), 컷 9 ×2, 컷 7 ×2, 패치·확인·정지 약 60분. 한 번은 Mac 잠자기로 중단(이후 caffeinate). 유료 API 없음 |
