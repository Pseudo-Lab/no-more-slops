# 사용한 스킬·에이전트 기록

요청 조건에 따라 `tracks/auto-post/skills/`와 그 밖에서 사용한 스킬을 무엇에, 어떻게 썼는지 기록한다. 라운드가 진행될 때마다 갱신한다.

## tracks/auto-post/skills/ 검토 결과

| 스킬 | 사용 | 사용 방식 / 사용하지 않은 이유 |
| --- | --- | --- |
| `design-punctuation` | 부분 사용 | 제목·장·절 제목·표 캡션의 끝마침표 규칙만 적용했다. 제목과 절 제목에는 마침표를 붙이지 않고, 캡션은 "**표 N.** 명사구" 형식으로 끝마침표를 생략했다. 스킬 설명대로 장문 본문의 문장부호에는 적용하지 않았다. |
| `instagram-content` | 미사용 | Instagram 카드뉴스·브랜딩용이며 학술 원고와 입력·출력이 다르다. |
| `instagram-reel` | 미사용 | 영상 편집용. |
| `family-reel-meme-preflight` | 미사용 | 릴스 밈 조사용. |
| `phantom-images`, `phantom-weekly` | 미사용 | `phantom-report` 프로젝트 전용 파이프라인이다. 다만 `phantom-weekly`의 "후보 수집 → 1차 출처 확인 → 원고 → 최종 대조" 구조와 단계 간 기록 파일을 감사 추적으로 쓰는 방식을 참고해, 이 프로젝트도 조사 기록(`research/`), 라운드별 심사·응답(`reviews/round-N/`)을 파일로 남겼다. 스킬 자체는 실행하지 않았다. |

## 퇴고: toego 플러그인 (`toego:revise`)

| 구성 요소 | 사용 방식 |
| --- | --- |
| `toego:revise` 절차 | 1단계 추출·린트 → 3단계 문장 → 4–7단계 문단·절·전체 흐름 → 8단계 사실 검증 → 9단계 비교 HTML 순서를 그대로 따랐다. |
| `hwp_extract.py` | 사용하지 않았다. 원고가 HWP가 아니라 Markdown이므로 같은 출력 형식(`paragraphs.json`, `tables.json`, `captions.json`)을 만드는 `app/md_extract.py`를 새로 작성했다. |
| `lint_ko.py` | 변경 없이 실행했다(`reviews/round*/lint.json`). |
| `toego:sentence-auditor` 에이전트 | 절 묶음별 3개를 병렬로 실행했다(`reviews/round*/sent-*.json`). |
| `toego:paragraph-auditor` 에이전트 | 원고 전체의 괄식·논증 사슬·질문–결론 대응을 검토했다(`reviews/round*/para.md`; 에이전트에 쓰기 도구가 없어 반환 보고를 옮겨 적음). |
| `toego:fact-checker` 에이전트 | 수정안의 수치·사실 주장을 조사 기록(`research/`)과 대조했다. |
| `build_html.py` | 변경 없이 실행해 수정 전/후 비교 HTML을 만들었다(`reviews/round*/퇴고_비교.html`). 라운드별 감사 결과를 `review.json`으로 묶는 `app/assemble_review.py`를 새로 작성했다. |

라운드별 toego 실행 내역:

| 라운드 | 린트 | 문장 감사 | 문단 감사 | 사실 검증 | 비교 HTML |
| --- | --- | --- | --- | --- | --- |
| 1 | 32건 | 3개 병렬, 83건 | 구조 12항목 | 16건 | `reviews/round1/퇴고_비교.html` |
| 2 | 53건 | 3개 병렬, 58건 | 구조 8건(minor) | 13건 | `reviews/round2/퇴고_비교.html` |
| 3 | 57건 | 2개 병렬, 29건 | 구조 8건(minor) | 8건 | `reviews/round3/퇴고_비교.html` |
| 4 | — | — | — | 재심 심사위원이 재계산·Crossref 확인 | — |

## 그 밖의 스킬·에이전트

| 이름 | 사용 방식 |
| --- | --- |
| general-purpose 서브에이전트 | 문헌 조사(R1: 3개 주제 병렬), 원문 재확인(R2–R5), 라운드별 심사위원(Frontiers Mini Review 심사 역할, 원문 직접 대조). |
| `app/normalize_refs.py` | arXiv API·Crossref로 참고문헌 저자 표기를 ICMJE 6인 규칙에 맞춤(초기 버전의 쪽 범위 치환 버그로 DOI 두 건이 손상되었고 Round 2에서 발견·복구). |
| Claude Code (claude-opus-5-5) | 원고 작성, 빌드 스크립트 작성, 심사 의견 반영. |
