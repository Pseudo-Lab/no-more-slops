# FILE 01 (수집 10/3~10/9, 발행 10/10 토)

## 구성
- 주간 묶음 (8장): 표지(CASE #003 헤드라인) → 목록 → #001~#005 → 마무리

## 채택

### #001 국내 은행 연쇄 해킹에 AI 해킹 도구 사용 · 보안 · 한국
9월 말~10월 초 신한·KB국민·하나·BNK부산은행, 예가람저축은행 등이 잇달아 해킹당했다. 대출모집인 페이지나 직원용 시스템처럼 관리가 허술한 곳이 뚫렸다. 크라우드스트라이크(10/7)는 해커가 중국 오픈소스 해킹 도구 ARTEX와 Claude Code, DeepSeek를 함께 썼다고 분석했다. 해커는 AI 대화 기록에 자기 이력서를 남겼다. 금융위원장은 10/4 긴급회의에서 2차 피싱을 경고했다.
- 확인 필요: 피해 규모가 출처마다 다름(7곳/9곳, 신한 약 2.5만 명 / 7곳 약 7만 명). 확정된 수치만 쓴다.
- https://www.theregister.com/cyber-crime/2026/10/08/crowdstrike-finds-possible-bank-hackers-cv-among-exposed-ai-logs/5301908
- https://news.bizwatch.co.kr/article/finance/2026/10/04/0003
- https://www.digitaltoday.co.kr/news/articleView.html?idxno=705760

### #002 현직 경찰관, 지인 사진으로 AI 성착취 합성물 400개 · 악용 · 한국 (10/7)
부산의 현직 경찰관이 2022.3~2026.8 지인 얼굴로 성적 허위영상물 약 400개를 만들고, 그중 약 50개를 유포했다. 디지털 성범죄물 5,600여 개도 갖고 있었다. 구속기소됐다.
- https://segye.com/newsView/20261007503427

### #003 Anthropic AI가 테스트 중 경찰에 가짜 살인 제보 · 오작동 · 미국 (10/9)
Claude 모델이 자동 테스트 중에 필라델피아 경찰 제보 사이트에 지어낸 목격담을 냈다(7/18). 제보는 스팸으로 걸러졌다. Anthropic은 9/28에야 알아챘고 10/7 경찰에 알렸다. 경찰은 "용납할 수 없다"고 했다.
- 확인 필요: 어느 모델이었는지 보도마다 다름(Haiku 4.5 / Opus 5). 모델명은 쓰지 않는다.
- https://www.foxbusiness.com/technology/anthropics-claude-ai-fabricates-eyewitness-account-submits-false-murder-tip-police-website
- https://www.scmp.com/news/world/united-states-canada/article/3370414/anthropic-ai-model-sent-fake-murder-tip-us-police-hit-government-sites

### #004 대학병원 의사·앵커 딥페이크 '기적의 치료제' 광고 · 악용 · 프랑스 (10/5~6)
파리 공립병원(AP-HP) 의사와 TF1 앵커의 얼굴과 목소리를 복제한 가짜 뉴스 영상이 페이스북에 퍼졌다. 병원은 형사 고소와 Meta 삭제 요청을 했지만 비슷한 영상이 다시 올라오고 있다.
- https://next.ink/260113/nouvelle-alerte-sur-la-proliferation-de-deepfakes-nourrissant-la-desinformation-en-sante/

### #005 Claude를 일기장처럼 썼다가 신고·기소 · 보안 · 미국 (10/5 확산, 첫 보도 9/30)
플로리다 여성이 Claude 대화에 보안관실을 향한 위협성 글을 썼다. 안전 시스템이 걸러내고 사람 검토를 거쳐 경찰에 신고돼 중범죄로 기소됐다. AI 대화를 회사가 읽고 신고할 수 있느냐는 프라이버시 논쟁이 일었다.
- https://www.businesstoday.in/technology/artificial-intelligence/story/florida-woman-used-claude-as-a-diary-what-happened-next-landed-her-in-trouble-559584-2026-10-05
- https://decrypt.co/380119/florida-woman-claude-diary-anthropic-reported-police

## 1차 출처 (10/11 확인)
원고는 아래 기준으로 고쳤다. 슬라이드 하단 SRC 줄도 이 기준.

- #001
  - CrowdStrike, "Unknown Threat Actor Uses AI-Driven ARTEX to Target South Korean Finance" (10.07) https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/
  - 금융위원회, 全금융권 긴급 점검회의 (10.04 회의, 10.06 게시) https://www.fsc.go.kr/no010101/87876
  - 금융위원회, 개인정보 유출에 따른 보이스피싱·스미싱 주의 (10.06) https://www.fsc.go.kr/no010101/87882
  - 주의: CrowdStrike 보고서에는 은행 이름이 없다. 공식 문서에 실명으로 나오는 곳은 신한은행뿐이고, 나머지 은행 명단과 피해 인원은 언론 보도(Korea Times 10.08 등)가 출처다.
- #002
  - 1차 출처는 못 찾음(부산지방공소청 보도자료). 가장 이른 보도: 세계일보 10.07 https://segye.com/newsView/20261007503427 · 부산일보 10.07 https://www.busan.com/view/busan/view.php?code=2026100710233851911
  - 주의: 피의자는 서울 동대문서 소속 경장이고, 부산경찰청이 텔레그램 잠입수사로 붙잡았다. "부산의 경찰관"이 아니다.
- #003
  - Anthropic, "Investigating unintended model actions in our evaluations and internal use" (10.09) https://www.anthropic.com/research/investigating-unintended-model-actions
  - PPD 성명 원문은 못 찾음. Reuters(CP24 전재) https://www.cp24.com/news/world/2026/10/09/anthropic-ai-model-submits-false-homicide-tip-to-police-website/ · CBS https://www.cbsnews.com/news/philadelphia-police-anthropic-ai-false-homicide-tip/
  - 모델은 Claude Haiku 4.5(Anthropic 원문). 경찰 통보일은 경찰 측 10.07, Anthropic 측 10.08.
- #004
  - AP-HP·소르본대, deepfake 경고문 (10.05) https://www.aphp.fr/espace-medias/liste-ressources-presse/lap-hp-et-sorbonne-universite-alertent-sur-la-dangerosite-des
  - 주의: TF1 앵커 도용은 AP-HP 원문에 없고 언론 보도(Le Parisien 인용)만 있어서 원고에서 뺐다.
- #005
  - WINK News 첫 보도 (09.30) https://www.winknews.com/news/woman-arrested-after-ai-threat-against-lee-county-sheriffs-office-investigators/article_3d4c5915-7015-43c0-b86a-d7fa5eadf958.html
  - Straight Arrow News, 진술서 보도 (10.08) https://san.com/cc/a-chatbot-message-led-to-a-felony-charge-experts-say-it-may-not-hold-up/
  - Anthropic 개인정보처리방침 3절 https://www.anthropic.com/legal/privacy
  - 주의: 진술서에 따르면 피의자는 쓴 플랫폼이 Perplexity라고 말했다. 그래서 원고에서는 "AI 챗봇"으로만 쓴다. 정식 기소 전이므로 "기소"가 아니라 "중범죄 혐의로 체포"라고 쓴다.

## 보류 (이번 호 미채택)
- 다크웹 AI 범죄 도구 시세 (ChatGPT 계정 10센트, 딥페이크 80달러) · 악용 · 원문 미확인. https://supple.kr/news/cmuxt9qma00iytez8adovzfm1
- 소니뮤직, AI 가짜 곡 26만 개 삭제 요청 · 악용. https://www.musicweek.com/labels/read/report-sony-music-doubles-ai-deepfake-takedowns-to-more-than-260-000/
- AI 챗봇 청소년 유해 민원 64% 미처리, 담당 1명 [국감] · 논란. https://www.newscj.com/news/articleView.html?idxno=3438751
- 멜로니 총리, 자기 목소리 상표 출원 · 법. https://ny1.com/nyc/all-boroughs/ap-top-news/2026/10/05/italys-meloni-follows-pop-stars-in-seeking-to-trademark-her-voice-to-combat-ai-deepfakes
- 법정 'AI 부활 피해자 영상', 항소심 재선고 명령 · 논란. https://404media.co/her-ai-generated-video-swayed-the-judge-the-court-said-it-carried-undue-emotional-weight
- USA투데이 등 신문사 20곳, OpenAI에 2.5억 달러 소송 · 법. https://www.newsbytesapp.com/news/business/usa-today-co-sues-openai-local-papers-seek-over-250-million/tldr
- 미국 중간선거 AI 딥페이크 광고 8천만 달러+ · 논란 · 본문 미확인. https://www.aljazeera.com/economy/2026/10/9/ai-deepfake-ads-grow-more-popular-in-us-midterm-campaigns-blurring-truth
- 딥페이크 기소 1년 새 3.5배(273명) · 통계 출처 불명. https://newsedu.co.kr/news/articleView.html?idxno=101859

## 원고
말투: 헤드라인·요약은 보고서체, `→` 행동 줄은 해요체. 세부 사실은 캡션(`out/file-01/caption.txt`)으로.

### 1 표지
- PHANTOM REPORT · FILE 01 · 2026.10.03–10.09
- 이미지 태그: EXHIBIT #003 · 도장: CLASSIFIED
- CASE #003 · AI MALFUNCTION
- 헤드라인: AI가 경찰에 가짜 살인 제보를 넣었다
- 서브: 이번 주 AI 사건 5건 보고

### 2 사건 목록 (CASE INDEX)
- #001 DATA BREACH: 국내 은행 연쇄 해킹, 범인은 AI를 썼다
- #002 DEEPFAKE ABUSE: 현직 경찰관이 만든 합성물 400개
- #003 AI MALFUNCTION: AI가 지어낸 살인 목격담
- #004 DEEPFAKE SCAM: 대학병원 의사가 파는 '기적의 치료제'
- #005 PRIVACY: AI에게 쓴 일기, 경찰이 읽었다
- 하단: 5 CASES · 2 / 8

### 3 CASE #001 · DATA BREACH · KOREA · 10.07
- 헤드라인: 국내 은행 연쇄 해킹, / 범인은 AI를 썼다
- 요약: AI 해킹 도구를 쓴 해커에게 국내 금융사들이 잇달아 뚫렸다.
- →: '유출 확인' 문자 속 링크는 누르지 마세요.
- SRC: CrowdStrike 블로그(10.07) · 금융위원회 보도자료(10.06)

### 4 CASE #002 · DEEPFAKE ABUSE · KOREA · 10.07
- 헤드라인: 현직 경찰관이 만든 / 합성물 400개
- 요약: 현직 경찰관이 지인 사진으로 AI 성적 허위영상물 400여 개를 만들어 구속기소됐다.
- →: SNS 사진의 공개 범위를 좁혀 두세요.
- SRC: 부산지방공소청 발표(10.07) · 세계일보·부산일보 보도

### 5 CASE #003 · AI MALFUNCTION · USA · 10.09
- 헤드라인: AI가 지어낸 / 살인 목격담
- 요약: 테스트 중이던 AI가 경찰 제보 사이트에 지어낸 목격담을 냈다. 회사는 두 달 넘게 몰랐다.
- →: AI가 무언가 제출할 땐 사람이 마지막에 확인하세요.
- SRC: Anthropic 보고서(10.09) · 필라델피아 경찰 성명(Reuters 인용)

### 6 CASE #004 · DEEPFAKE SCAM · FRANCE · 10.05
- 헤드라인: 대학병원 의사가 파는 / '기적의 치료제'
- 요약: 병원 교수의 얼굴과 목소리를 복제한 AI 영상이 근거 없는 약을 팔았다.
- →: '기적의 치료제'는 일단 의심하세요.
- SRC: AP-HP·소르본대 공동 경고문(10.05)

### 7 CASE #005 · PRIVACY · USA · 09.30
- 헤드라인: AI에게 쓴 일기, / 경찰이 읽었다
- 요약: AI 챗봇에 남긴 위협 글이 회사 검토를 거쳐 신고됐고, 작성자는 체포됐다.
- →: AI 채팅은 비밀 일기장이 아니에요.
- SRC: WINK News(09.30) · 법원 기록 보도(Straight Arrow News, 10.08)

### 8 마무리
- END OF REPORT · FILE 01
- 5 · CASES CLOSED IN THIS FILE
- 이 보고서를 저장하고, 가족에게 공유하세요.
- 모르면 당하는 AI 사건, 매주 토요일 보고합니다.
- NEXT REPORT: 10.17 SAT

## 발행본
- 확정: `design/file-01.html` → `out/file-01/01~08.png`
- 캡션·해시태그: `out/file-01/caption.txt`

## 최종 대조 (10/11)
대상: `design/file-01.html` 8장, `out/file-01/caption.txt`. 기준: `## 1차 출처 (10/11 확인)`. 캡션에서 메모 밖으로 나간 세부(#001 ARTEX·이력서, #004 교수·기생충 제거제)는 CrowdStrike·AP-HP 원문을 직접 열어 확인했고 문제없다.

1. **슬라이드 4 (CASE #002) SRC 줄**
   - 문장: "SRC: 부산지방공소청 발표(10.07) · 세계일보·부산일보 보도"
   - 근거: #002 메모에 "1차 출처는 못 찾음(부산지방공소청 보도자료)"이라고 적혀 있다. 못 찾은 자료를 출처처럼 적었다.
   - 고칠 문구: "SRC: 세계일보·부산일보 보도(10.07)"
2. **캡션 CASE #002**
   - 문장: "…붙잡혀 10월 7일 구속기소됐어요."
   - 근거: 10.07은 첫 보도 날짜다(세계일보·부산일보). 기소 날짜는 1차 출처를 못 찾아서 확인되지 않았다.
   - 고칠 문구: "…붙잡혀 구속기소됐어요." (날짜 삭제)
3. **슬라이드 5 (CASE #003) SRC 줄** (경미)
   - 문장: "SRC: Anthropic 보고서(10.09) · 필라델피아 경찰 성명(Reuters 인용)"
   - 근거: #003 메모에 "PPD 성명 원문은 못 찾음"이라고 적혀 있다. 실제 출처는 Reuters·CBS 보도다. 괄호로 인용이라고 밝히긴 했지만 경찰 성명이 출처처럼 읽힌다.
   - 고칠 문구: "SRC: Anthropic 보고서(10.09) · Reuters·CBS 보도(10.09)"

참고(대조 범위 밖): `## 채택`의 #002·#005 요약에는 정정 전 내용("부산의 현직 경찰관", "Claude 대화", "중범죄로 기소")이 남아 있다. 검증 모드 4번에 따라 고쳐야 한다.
