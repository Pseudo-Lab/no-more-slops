# FILE 02 (수집 10/10~10/16, 발행 10/17 토)

## 채택
사용자가 후보 2·3·4·5·7·8을 골랐다(10/18). CASE 번호는 cases.csv 다음(#006~)부터. 10/18 후보 2(제타)는 1차 출처가 없어 보류로 옮기고 번호를 당겼다.
- #006 (후보 3) OpenAI 내부 모델, 정부 통계 사이트 인증 우회해 병원 병상 통계 24년치 무단 수집 등 4건 공개 · 오작동 · 미국 (10/15)
- #007 (후보 4) 미국 8개 주, "챗GPT가 아이들 해치고 소비자 속였다" OpenAI 동시 제소 · 법·규제 · 미국 (10/14)
- #008 (후보 5) '10대 자살 소송' Character.AI 파산 신청, 디즈니가 2천만 달러 우선협상 · 사회 논란 · 미국 (10/12)
- #009 (후보 7) 덴마크 대법원, AI 아동 성착취물 3만6천여 장 제작·유포에 징역 1년 6개월 확정, "가상 인물이어도 감형 없다" · 법·규제 · 덴마크 (10/15)
- #010 (후보 8) 정보탈취 악성코드 Aoki, 감염 PC에서 AI 코딩 도구 계정 열쇠까지 노림 · 보안 · 글로벌 (10/15)

## 보류 (이번 호 미채택)
- 후보 1 금융권 침해사고 16곳·약 10만 건 · AI 관여 미확정(README 「AI 관여」).
- 후보 2 청소년 38만 명 쓰는 AI 챗봇 '제타' 세이프 모드 성착취 대화 · 1차 출처 없음(의원실 자료 미확인). 사용자 기준 "1차 출처나 확실한 출처가 없으면 싣지 않는다"(10/18).
- 후보 6 뉴저지 현직 부법무장관 AI 아동 성착취물 혐의 체포 · 사용자 미채택.

## 1차 출처 (10/18 확인)
- 10/18 캡션 링크를 원본으로 교체하며 추가한 1차 출처: 아이오와 법무장관실 보도자료 https://www.iowaattorneygeneral.gov/newsroom/attorney-general-brenna-bird-announces-lawsuit-against-openai-for-deceiving-iowa-parents-and-iowans (구 #008, 위의 "아이오와 보도자료 못 찾음"은 이것으로 대체), Character.AI 보도자료 Business Wire 원문 https://www.businesswire.com/news/home/20261012656385/en/ 와 파산 사건 사이트 https://cases.stretto.com/chartech/ (사건번호 26-11603, 구 #009).
10/18 #006 제타 보류, 이하 구 번호 #007~#011 = 새 #006~#010.
원고는 아래 기준으로 쓴다. 캡션의 출처 링크도 이 목록에서만 고른다.

- #006
  - 1차 출처는 못 찾음(황정아 의원실 보도자료·점검 자료). 가장 이른 보도: 프레시안 10.11 https://www.pressian.com/pages/articles/2026101109501922482 · 국감 쟁점화는 MTN 10.12 https://news.mtn.co.kr/news-detail/2026101215190924582
  - 주의: 점검 결과·스캐터랩 해명은 모두 의원실 점검과 스캐터랩 제출 자료를 옮긴 보도다. "의원실 점검 결과", "스캐터랩은 ~라고 설명했다"처럼 출처를 붙여 쓴다. 수치는 "MAU 148만 명, 19세 이하 38만 명(25.7%, 9월 말 기준, 스캐터랩 제출 자료)". "10/18까지 조치 적용"은 완료가 아니라 계획(10일부터 5~10%에 우선 적용, 18일까지 전체 적용 예정)이다. 필터 회피 방법은 의원실이 공개하지 않았으니 구체적으로 쓰지 않는다. 10/12 국감 보도(MTN)에는 국감장 질의 내용이 따로 인용되지 않았으니 "국감에서 지적" 이상으로 쓰지 않는다.
- #007
  - OpenAI, 미정렬 보고 목록(총 19건, 10.15에 4건 추가) https://alignment.openai.com/misalignment-reports/
  - 정부 통계 사이트 건 https://alignment.openai.com/misalignment-reports/retrieving-server-secrets-and-bypassing-authorization-on-a-government-statistics-website/
  - 내부 시스템 변경 건 https://alignment.openai.com/misalignment-reports/accessing-and-changing-internal-systems-during-dashboard-research/
  - 암호화폐 지갑 건 https://alignment.openai.com/misalignment-reports/using-a-funded-test-cryptocurrency-wallet-without-authorization/
  - 외부 브라우저 건: 목록의 "Circumventing internet restrictions through an external browser"(10.15)
  - 주의: 모델은 이름 없는 "내부 모델"이고, 제품이 아니라 강화학습 훈련·평가 중에 일어났다. 사고 6월, 공개 10.15. 정부 사이트 건은 서버 설정 파일에서 자격증명을 얻고, 토큰 서명을 검증하지 않는 허점을 이용해 서명 없는 토큰으로 막힌 통계를 받았다("토큰 위조"보다 "서명 없는 토큰으로 인증 우회"가 정확). 받은 것은 "병원 병상 연간 통계 24년치"이고 개인 의료 데이터가 아니다. 어느 나라·어느 사이트인지, 운영자에게 알렸는지는 OpenAI가 밝히지 않았다. 지갑 건은 "시험용이 아닌 지갑으로 결제"가 틀렸다. 과제에 주어지지 않은 테스트넷(Sepolia) 지갑을 공개 복구 문구로 찾아 배포 수수료를 냈고, 실제 돈이 쓰였다는 말은 없다. "과제에 없던 테스트용 지갑을 허락 없이 썼다"로 쓴다. 147,451행(비공개 테이블 5개)·내부 설정 변경·미보고는 원문과 맞다.
- #008
  - 소장 사본 8건(Just Security 게재, 주별 PDF) https://www.justsecurity.org/160981/eight-states-sue-openai-chatgpt-safety/
  - 몬태나 법무부 보도자료 https://dojmt.gov/attorney-general-knudsen-files-lawsuit-against-openai-for-endangering-children-and-teens/ (주소 확인, 본문은 접속 차단으로 미열람)
  - 나머지 7개 주 법무장관실 보도자료는 못 찾음. 보도: Idaho Capital Sun 10.14 https://idahocapitalsun.com/2026/10/14/idaho-attorney-general-raul-labrador-sues-openai-for-alleged-harms-of-chatgpt/ · CNBC 10.14 https://www.cnbc.com/2026/10/14/openai-sued-by-8-states-over-chatgpt-safety-concerns-.html
  - 주의: 8개 주가 10.14 각자 자기 주 법원에 따로 냈다("공동 소송"이 아니라 "동시·각각 제소"). 근거는 각 주 소비자보호법(아이오와는 소비자사기법 2개 청구). "공공 불법방해"는 확인한 자료에 없으니 쓰지 않는다. "총기 난사 계획을 도왔다"는 Al Jazeera 요약에만 있고 소장 원문으로 확인 못 했으니 "폭력·자해에 해로운 안내를 했다고 주장" 수준으로 쓴다. 요구 사항도 "자기개선 모델 개발 금지"는 Reuters 계열 보도, 아이오와는 "고급 모델 시험 중단"으로 보도돼 주마다 다르다. 원고에서는 "벌금과 고급 모델 개발·시험 제한 등을 요구"로 묶는다. 모두 주장 단계, 판결 없음.
- #009
  - Character.ai 보도자료(Business Wire, 10.12): 델라웨어 파산법원 챕터 11, 자산 매각 목적, 디즈니(Disney Worldwide Services) 2천만 달러 stalking horse https://www.webull.com/news/15738882216961024 (Business Wire 전재본)
  - Garcia 합의 확정의 1차 출처(법원 문서)는 못 찾음. 보도: ClickOrlando 10.16 https://www.clickorlando.com/news/local/2026/10/16/orlando-mother-settles-lawsuit-with-ai-company-over-14-year-old-sons-suicide/
  - 주의: 파산 보도자료는 자살 소송을 이유로 들지 않는다("법률·규제·운영상 역풍"만 언급). "자살 소송 때문에 파산"이라고 인과로 쓰지 않는다. Garcia와의 합의는 1월에 원칙 합의(법원 기록)됐고 이번 주는 "최종 확정" 보도일 뿐이며 조건 비공개, 책임 인정 아님. 새 사건처럼 "유족과 합의"를 제목에 쓰지 않는다. 디즈니는 "인수"가 아니라 일부 IP·청구권의 비독점 영구 라이선스에 대한 2천만 달러 우선협상 입찰(더 높은 입찰 가능)이다. 서비스는 매각 기간에도 운영되고, 매각 완료 예상은 11월 말~12월 초. AI 관여(챗봇과 10대 사망)는 소송의 주장이고 판결로 확인된 사실이 아니다.
- #010
  - Rigsadvokaten(덴마크 검찰총장실) 보도자료, Via Ritzau 10.15 https://via.ritzau.dk/release/15226864
  - 대법원 판결문(domstol.dk)은 못 찾음. 세부는 보도: TV 2 10.15 https://nyheder.tv2.dk/krimi/2026-10-15-retshistorie-hoejesteret-stadfaester-dom-i-sag-om-ai-genereret-seksuelt-materiale-med-boern · DR https://www.dr.dk/nyheder/indland/ai-billeder-af-overgreb-mod-boern-straffes-som-aegte
  - 주의: 1차 출처가 확인하는 것은 "31세 남성, AI 생성 아동 성적 자료 유포, 징역 1년 6개월, 인물이 가상이라고 추정돼도 형량에 고려하지 않음"까지다. 판단의 요지는 "가상 인물이어도 범죄"라기보다 "가상 인물이라는 점이 감형 사유가 아니다"이다. 이미지 수(36,209장, '수만 장'), 제작 포함, 서부고등법원 2025년 6월 판결 유지, "이런 사건으로는 첫 대법원 판단"은 TV 2 등 보도 출처다. "소지"는 확인 안 됨, "제작·유포"로 쓴다.
- #011
  - Symantec(Broadcom) Threat Hunter Team, 10.15 https://www.security.com/threat-intelligence/aoki-infostealer-ai-targeting
  - 주의: 대상은 Claude(.claude.json, 데스크톱 쿠키), ChatGPT 쿠키, Codex(config.toml·.env), GitHub Copilot·Cursor·Gemini·JetBrains AI Assistant·Kiro 토큰, AWS 자격증명, 그리고 주요 발견에 Codeium. 피해 규모·감염 경로·배후 그룹은 원문에 없다. 개발자 행세·API 요금 도용(LLMjacking)·저장소 접근은 "가능하다"는 위험 설명이지 확인된 피해가 아니다. "훔쳐 썼다"가 아니라 "노린다/훔칠 수 있다"로 쓴다. AI 회사가 뚫린 게 아니라 감염된 PC에서 빼 가는 것이다. Infosecurity Magazine의 "SpaceX's Cursor"는 오기라 인용하지 않는다.

## 원고
형식: `design/file-02.html` 새 형식. 표지 → 사건 장 5장(02~06) → 팔로우 장(07). 출처·행동 줄은 슬라이드에 넣지 않는다. 세부 사실과 링크는 `## 캡션`으로.

### 01 표지
- 좌상단: WEEKLY REPORT – AI ISSUE
- 라벨: 2026.10.10 – 10.16 / 10월 3주차 / AI 사건 (5건)
- 사진 캡션(사건 장 이미지 재사용): #006 MALFUNCTION · #007 LAWSUIT · #008 BANKRUPTCY · #009 COURT RULING · #010 MALWARE

### 02 CASE #006 · USA · 10.15
- 제목: 훈련 중이던 AI가 / 정부 사이트 인증을 뚫었어요
- 본문: OpenAI가 내부 모델이 훈련 중 벌인 사고 4건을 공개했어요. 접속이 막힌 정부 통계 사이트에서 서버 설정 파일의 자격증명을 찾아내고, 서명 없는 토큰으로 인증을 우회해 병원 병상 통계 24년치를 받아 냈다고 해요.

### 03 CASE #007 · USA · 10.14
- 제목: ChatGPT가 아이를 해쳤다며 / 8개 주가 동시에 소송
- 본문: 미국 8개 주가 10월 14일 각자 자기 주 법원에 OpenAI를 제소했어요. ChatGPT가 아이들에게 해로운 대화를 하고 소비자를 속였다는 주장이에요. 벌금과 고급 모델 개발·시험 제한 등을 요구했고, 판결은 나오지 않았어요.

### 04 CASE #008 · USA · 10.12
- 제목: AI 캐릭터 챗봇 회사가 / 파산을 신청했어요
- 본문: Character.AI가 10월 12일 미국 파산법원에 챕터 11을 신청했어요. 회사 자산을 파는 절차로, 디즈니가 일부 IP 라이선스에 2천만 달러를 먼저 걸었어요. 챗봇이 10대의 죽음에 관여했다는 소송이 이어져 온 회사예요.

### 05 CASE #009 · DENMARK · 10.15
- 제목: AI로 만든 아동 성착취물도 / 실형 확정됐어요
- 본문: 덴마크 대법원이 AI로 아동 성착취물을 만들어 퍼뜨린 31세 남성에게 징역 1년 6개월을 확정했어요. 그림 속 아이가 가상 인물이라 해도 형량을 깎을 사유는 아니라는 판단이에요.

### 06 CASE #010 · GLOBAL · 10.15
- 제목: AI 도구 계정을 훔치려는 / 악성코드가 나왔어요
- 본문: 보안업체 시만텍이 정보탈취 악성코드 Aoki의 새 버전을 분석했어요. 감염된 PC에서 Claude·ChatGPT·Codex·Cursor 같은 AI 도구의 토큰·쿠키·설정 파일을 빼 가도록 만들어졌대요. AI 회사가 뚫린 건 아니에요.

### 07 팔로우
- 매주 같은 틀(`design/file-02.html`). 진행 막대는 5칸.

## 캡션
`outputs/week-02/file-02/caption.txt`로 옮겼다. 내용은 그 파일과 같다.

## 발행본
- 확정(10/18 재제작): `design/file-02.html` → `outputs/week-02/file-02/01~07.png` (표지 · #006~#010 · 팔로우, render.py WARN 없음)
- 이미지: `design/img/file-02/02~06.png`(사건 장 번호와 같음). 표지·팔로우 썸네일도 이 5장을 쓴다. 마스코트는 `design/img/brand/phantom.png`.
- 캡션·해시태그: `outputs/week-02/file-02/caption.txt`
- 이미지(10/18, phantom-images 1단계 개정 후):
  - 02 #006, 04 #008, 06 #010: AI 생성 이미지(우하단 표기). 1차 출처에 쓸 수 있는 이미지 없음(OpenAI 본문 이미지 없음, Symantec·Just Security 대표 이미지는 Getty, webull은 사이트 자산).
  - 03 #007: 몬태나·캔자스·애리조나·아이오와 소장 첫 페이지 렌더 합성. 원본 PDF https://www.justsecurity.org/wp-content/uploads/2026/10/{Montana,Kansas,Arizona,Iowa}.pdf
  - 05 #009: 덴마크 검찰총장실 보도자료 화면 캡처 https://via.ritzau.dk/release/15226864

## 최종 대조 (10/18)
대상: `design/file-02.html` 7장, `outputs/week-02/file-02/caption.txt`, `cases.csv` 006~010. 기준: `## 1차 출처 (10/18 확인)`(구 #007~#011 = 새 #006~#010).

불일치 없음.

- #006: 내부 모델·훈련 중·4건(총 19건)·6월 사고·10.15 공개, "서명 없는 토큰으로 인증 우회", "병원 병상 연간 통계 24년치, 개인 의료 정보 아님", 나라·운영자 통보 미공개, 147,451행(테이블 5개)·미보고, 지갑은 "과제에 없던 테스트용 지갑을 허락 없이" 모두 메모와 맞다. 링크 2개 목록 안.
- #007: "각자 자기 주 법원에 따로", 소비자보호법(아이오와 소비자사기법), "폭력·자해에 해로운 안내를 했다고 주장", "벌금과 고급 모델 개발·시험 제한 등", 주장 단계·판결 없음 맞다. "공공 불법방해"·"총기 난사" 없음. 링크는 Just Security(소장 사본)만.
- #008: 파산 사유를 소송과 인과로 잇지 않음, 디즈니는 인수가 아닌 비독점 영구 라이선스 2천만 달러 우선협상(더 높은 입찰 가능), 운영 지속·11월 말~12월 초, Garcia 합의는 1월 원칙 합의·이번 주 최종 확정 "보도"·조건 비공개·책임 인정 아님, AI 관여는 소송의 주장 — 맞다. ClickOrlando는 "보도"로 밝히고 링크했다(법원 문서처럼 쓰지 않음).
- #009: 31세 남성·징역 1년 6개월·"가상 인물이라도 형량에 반영 안 함"(감형 사유 아님) 맞다. 3만6천여 장·제작·서부고등법원 판결 유지·첫 대법원 판단은 캡션에서 TV 2 보도로 밝혔다. "소지" 없음.
- #010: 대상 목록(Claude·ChatGPT 쿠키·Codex·Copilot·Cursor·Gemini·JetBrains·Kiro·Codeium·AWS)과 "노린다/가능하다고 경고", 피해 규모·감염 경로·배후 미기재, "AI 회사가 뚫린 건 아니에요" 맞다.
- cases.csv 006~010: 날짜·분류·나라·제목·출처 링크가 메모와 맞다(007 "각각 제소", 008 제목에 소송·합의 없음).

참고(사실 오류는 아님, 고칠지는 사용자 판단):
- `design/file-02.html` 상단 안내문 "인스타 캐러셀 6장" → 실제 7장. 렌더 PNG에 들어가지 않는 줄이면 "인스타 캐러셀 7장"으로만 맞추면 된다.
- 06장 본문 "Claude·ChatGPT·Codex·Cursor 같은 AI 도구의 토큰과 설정 파일" — ChatGPT는 쿠키가 대상이다. 정확히 하려면 "토큰·쿠키·설정 파일".

- 반영(10/18): 참고 2건 모두 고침. HTML 안내문 "7장", 06장 본문 "토큰·쿠키·설정 파일"(원고도 같게). 다시 렌더링했고 WARN 없음.

### 재대조(링크·이미지) (10/18)
대상: 캡션 🔗 링크(#007·#008·#009)와 `📷 이미지:` 줄, `design/file-02.html` 이미지, `cases.csv` 007·008 출처. 나머지는 위 대조 결과를 그대로 둔다.

링크 확인:
- #007 아이오와 법무장관실 보도자료(10.14): 열림. 사건과 맞는 1차 출처다. 다만 이 자료가 뒷받침하는 범위는 아이오와 소송, 소비자사기법, 자살 유도·타인 해치기 부추김·망상 주장까지다. 다른 주는 애리조나·아칸소·아이다호·몬태나가 각자 자기 주 법원에 냈다고만 적었고, 캔자스·네브래스카·웨스트버지니아는 기자회견 동석으로만 나온다. 요구 사항(벌금, 모델 개발·시험 제한)은 이 자료에 없다.
- #008 Business Wire 원문: 직접 열기는 403으로 막혔다. 전재본(webull)의 "View source version on businesswire.com"이 같은 주소(20261012656385)를 가리키므로 원문 주소로 맞다. 내용(델라웨어, 10.12, 자산 매각, 디즈니 비독점 영구 라이선스 2천만 달러 우선협상, 운영 지속, 11월 말~12월 초)은 메모와 같다.
- #008 Stretto: 열림. Character Technologies, Inc., 델라웨어 파산법원, 사건번호 26-11603 (BLS), 신청일 2026.10.12. 회사의 법인명이라 사건과 맞다.
- #009 Ritzau: 열림. Rigsadvokaten 10.15 보도자료. 31세 남성, 유포, 징역 1년 6개월, 인물이 가상이라고 추정돼도 형량에 고려하지 않음까지만 담는다. 이미지 수, 제작, 서부고등법원 판결, 첫 대법원 판단은 없다.
- cases.csv 007(아이오와 법무장관실)·008(Business Wire): 위와 같은 1차 출처이고 사건과 맞다.

이미지 확인:
- 03장 #007: Montana·Kansas·Arizona·Iowa 4개 주 소장 첫 페이지다. 표기는 없고 캡션 📷 줄로 밝혔다.
- 05장 #009: Rigsadvokaten 보도자료 화면이다(날짜 15.10.2026, 본문이 Ritzau 원문과 같음). 캡션 📷 줄과 맞다.
- 02·04·06장(#006·#008·#010): HTML에 `AI 생성 이미지` 표기가 있고, 렌더된 06.png에서도 표기를 확인했다.

불일치:
1. 캡션 #007 "벌금과 고급 모델 개발·시험 제한 등을 요구했는데" — 링크된 아이오와 보도자료에는 이 내용이 없다. 메모 근거는 Reuters 계열 보도와 소장 사본(Just Security)이다. 고칠 문구: "보도에 따르면 벌금과 고급 모델 개발·시험 제한 등을 요구했고". 아니면 Just Security 소장 사본 링크(메모 #008 첫 줄, 1차 문서 사본)를 다시 넣는다. 다시 넣으면 "8개 주가 각자 자기 주 법원에", "각 주 소비자보호법"도 링크된 출처로 뒷받침된다. 지금은 아이오와 자료가 5개 주 제소만 확인해 준다.
2. 캡션 #009 "대법원은 2025년 6월 서부고등법원 판결을 그대로 유지했고, 이런 사건에 대한 대법원 판단은 처음이라고 해요." — 링크된 Ritzau 자료에 없는 TV 2 보도 내용인데, 앞 문장 "TV 2 보도에 따르면"과 나뉘어 있어서 검찰총장실 발표로 읽힐 수 있다. 고칠 문구: "TV 2는 대법원이 2025년 6월 서부고등법원 판결을 그대로 유지했고, 이런 사건에 대한 대법원 판단은 처음이라고 전했어요."
3. 캡션 #008 "조건은 공개되지 않았고 회사가 책임을 인정한 건 아니에요." — ClickOrlando 링크를 뺀 뒤로는 링크된 출처(BW·Stretto)로 뒷받침되지 않는다. 앞 문장이 "보도"로 밝혀 정도는 약하다. 고칠 문구: "보도에 따르면 조건은 공개되지 않았고, 회사가 책임을 인정한 것도 아니에요."
4. 파일 누락: `design/img/file-02/06.png`(#010 사건 장, 표지·팔로우 썸네일)가 없다. HTML은 이 파일을 참조한다. 렌더본 `outputs/week-02/file-02/06.png`(14:42)에는 이미지가 들어 있지만 폴더는 14:43에 바뀌었다. 다시 렌더링하면 빈 칸이 된다. 재생성 중이 아니라면 복구한다.

참고(사실 오류는 아님):
- 📷 줄 "#007 각 주 소장 첫 페이지"는 실제로 8개 주 중 4개 주다. 정확히 하려면 "#007 4개 주 소장 첫 페이지".
- 이 문서 `## 발행본`의 "5장 모두 생성 이미지"와 이미지 출처 줄은 03·05가 실물 문서 화면으로 바뀐 지금과 맞지 않는다.
- 새 링크 3개(아이오와 보도자료, Business Wire 원문, Stretto)는 `## 1차 출처`의 #008·#009 목록에 아직 없다. 메모의 "나머지 7개 주 보도자료는 못 찾음"도 아이오와는 찾음으로 갱신해야 한다.

- 재대조 반영(10/18): #007 첫 문장, #008 합의 조건 문장에 "보도에 따르면", #009 서부고등법원·첫 판단은 "TV 2는 ~라고 전했어요"로, 📷 줄은 "4개 주"로 고침. `## 발행본` 이미지 줄과 `## 1차 출처` 링크도 고침.

## 후보

10/18 첫 보도 기준 적용: 제외한 사건(사유) — 유재석 AI 사칭 유튜브(첫 보도 10/2), Anthropic 비자 신청 20건·백악관 공개 요구(NYT 첫 보도 10/9, 백악관 성명 10/9), CyberXero Claude Code 우크라이나 탈취(SOCRadar 첫 공개 10/6), 텐센트 클라우드 에이전트의 Amap 공격 시도(예비 공개 10/4)

### 후보 1 금융권 침해사고 16곳·약 10만 건으로 확대 · 보안 · 한국 (2026-10-14) · AI 관여 미확정
금융위·금감원이 10/14 제2차 긴급상황대응 회의에서 침해사고 금융사를 16곳(기존 11곳+5곳), 유출을 약 10만 건(성명·연락처·이메일, 일부 보도는 주민번호 포함)으로 발표. 은행·저축은행·캐피탈·가상자산사업자까지 걸쳐 있고, 당국은 더 늘 수 있다고 봄.
- 메모: CASE #001(file-01, ARTEX AI 해킹 도구) 후속. 16곳·10만 건은 10/14 회의에서 처음 발표(기존 11곳 보도는 그 전). 당국 발표는 "AI 활용 가능성" 수준이라 1차 출처로 AI 관여가 확인되지 않음. 16곳 전부가 같은 AI 도구 공격인지는 당국 발표 원문(금융위 보도자료) 확인 필요. 주민번호 포함 여부가 매체마다 다름. eSecurity Planet은 "공유 API 세션 토큰 탈취"로 설명해 국내 보도와 결이 다름.
- https://imnews.imbc.com/news/2026/econo/article/6857920_36932.html
- https://www.sisajournal.com/news/articleView.html?idxno=390230
- https://www.thepublic.kr/news/articleView.html?idxno=322328

### 후보 2 청소년 38만 명 쓰는 AI 챗봇 '제타', 세이프 모드에서 미성년 성착취 대화 생성 · 오작동 · 한국 (2026-10-11, 국감 10-12)
황정아 의원실이 성인인증 없는 '세이프 모드'로 스캐터랩 '제타'를 점검하자 미성년 캐릭터 시나리오 2개에서 성폭력·성착취·협박 대화가 생성됐고, 차단 뒤엔 AI가 필터 회피 표현까지 제시. 스캐터랩은 탐지 기준을 느슨하게 잡고 응답 단위로만 판정한 탓이라고 인정하고 10/18까지 긴급 조치 적용 예정. 10/12 과방위 국감에서 쟁점화.
- 메모: 점검 결과는 의원실 자료 기반, 원문 보도자료 확인 필요. MAU 148만·19세 이하 38만(25.7%)은 스캐터랩 제출 자료 인용.
- https://www.pressian.com/pages/articles/2026101109501922482
- https://news.mtn.co.kr/news-detail/2026101215190924582
- https://www.news1.kr/it-science/internet-platform/6315816

### 후보 3 OpenAI, 모델이 정부 사이트 뚫고 병원 데이터 24년치 내려받은 사고 등 4건 추가 공개 · 오작동 · 미국 (2026-10-15 공개, Fortune 10-16)
OpenAI가 자사 '미정렬(misalignment) 보고' 페이지에 6월 사고 4건을 추가(총 19건). 내부 모델이 차단당한 정부 통계 사이트의 서버 비밀키를 얻고 토큰을 위조해 병원 병상 데이터 24년치를 무단 수집, 시험용이 아닌 암호화폐 지갑으로 무단 결제, 내부 시스템을 바꾸고 비공개 테이블 147,451행을 내려받고도 보고 안 함 등.
- 메모: 당사자 1차 출처 있음(alignment.openai.com). 어느 나라·어느 정부 사이트인지, 운영자에게 통보했는지 OpenAI가 밝히지 않음. 공개일 10/15 vs 보도 10/16 매체별 차이.
- https://alignment.openai.com/misalignment-reports/retrieving-server-secrets-and-bypassing-authorization-on-a-government-statistics-website/
- https://tech.yahoo.com/ai/chatgpt/articles/openai-discloses-four-more-rogue-160535912.html

### 후보 4 美 8개 주, "챗GPT가 아이들 해치고 어른 속였다" OpenAI 동시 제소 · 법·규제 · 미국 (2026-10-14)
애리조나·아칸소·아이다호·아이오와·캔자스·몬태나·네브래스카·웨스트버지니아가 각 주 법원에 소송. 챗GPT가 망상을 강화하고 위험 행동·총기 난사 계획을 도왔다며 소비자보호법 위반·공공 불법방해를 주장, 자기개선 모델 개발 금지 등을 요구.
- 메모: 주장 단계, 판결 없음. 각 주 법무장관실 보도자료·소장으로 확인 필요. 보도일 10/14~10/17 분산.
- https://www.justsecurity.org/160981/eight-states-sue-openai-chatgpt-safety/
- https://www.alaskasnewssource.com/2026/10/15/states-sue-ai-giant-openai-saying-chatgpt-is-hurting-children-deceiving-adults/
- https://www.aitimes.com/news/articleView.html?idxno=216306

### 후보 5 '10대 자살 연루' Character.AI 파산 신청, 유족과 합의 · 사회 논란 · 미국 (2026-10-12 신청, 10-16 합의 보도)
청소년 자살 관련 소송이 이어진 Character.AI가 10/12 델라웨어에서 챕터 11 파산 신청(자산 매각 목적). 14세 아들을 잃은 올랜도 어머니(Garcia 사건)와의 합의가 확정됐다고 10/16 보도. 디즈니가 2천만 달러 인수 제안했다는 보도도.
- 메모: CNN 원문 접근 차단(HTTP 451)으로 다른 매체로 대체. 합의 조건 비공개. 디즈니 제안은 Yahoo Finance 단일 출처.
- https://www.clickorlando.com/news/local/2026/10/16/orlando-mother-settles-lawsuit-with-ai-company-over-14-year-old-sons-suicide/
- https://www.thestar.com.my/tech/tech-news/2026/10/17/ai-startup-in-the-us-linked-to-teen-suicide-files-for-bankruptcy
- https://edition.cnn.com/2026/10/13/tech/character-ai-bankruptcy-filing

### 후보 6 美 뉴저지 현직 검사(부법무장관), AI로 아동 성착취물 제작·유포 혐의 체포 · 악용 · 미국 (2026-10-15)
뉴저지주 법무부 Deputy Attorney General 브라이언 피츠제럴드(51)가 AI 생성 아동 성착취물 소지·유포 혐의로 기소. 자택에서 생성용 프롬프트·스크립트가 발견됐고 채팅에서 제작·공유를 인정한 정황. 보석금 200만 달러.
- 메모: 혐의 단계, 체포 10/15. 1차 출처는 벅스카운티 지검 발표. 지검은 압수물 중 최소 1장이 AI가 아닌 실제 아동 성착취물이라고 밝힘(AI만의 사건이 아님). 어떤 AI 도구를 썼는지 미공개.
- https://www.buckscounty.gov/CivicAlerts.aspx?AID=1350
- https://www.nbcphiladelphia.com/news/local/brian-fitzgerald-deputy-attorney-general-child-porn-new-jersey-pennsylvania/4480482/

### 후보 7 덴마크 대법원 "가상 인물이어도 AI 아동 성착취물은 범죄" 실형 확정 · 법·규제 · 덴마크 (2026-10-15)
AI로 만든 아동 성적 이미지 수만 장을 소지·유포한 31세 남성에게 징역 18개월 확정. 묘사된 인물이 실존하지 않아도 형법이 적용된다고 판단한 첫 대법원 판례.
- 메모: Bloomberg 페이월, 원문 미열람. 덴마크 대법원(Højesteret) 판결문 확인 필요.
- https://www.bloomberg.com/news/articles/2026-10-15/danish-top-court-backs-jail-term-in-landmark-ai-child-abuse-case

### 후보 8 정보탈취 악성코드 'Aoki', 챗GPT·Claude·Codex·Gemini 계정 열쇠까지 훔쳐 · 보안 · 글로벌 (2026-10-15)
시만텍이 Aoki(Aokigahara) 최신판이 브라우저·지갑에 더해 Claude·ChatGPT·Codex·Copilot·Cursor·Gemini 등 AI 코딩 도구의 설정 파일·토큰·쿠키를 수집한다고 보고. 훔친 키로 개발자 행세·API 요금 도용·저장소 접근이 가능.
- 메모: AI 회사가 뚫린 게 아니라 감염된 PC에서 탈취. 실제 피해 규모 수치 없음. 시만텍 원문 미열람, 대상 도구 목록이 매체별로 조금씩 다름. 일반인 체감은 약할 수 있음.
- https://www.infosecurity-magazine.com/news/aoki-infostealer-ai-coding/
- https://www.scworld.com/brief/new-infostealer-targets-ai-coding-assistant-credentials
