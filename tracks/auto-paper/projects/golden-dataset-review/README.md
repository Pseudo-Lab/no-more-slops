# 골든 데이터셋 미니 리뷰

- 작성자: @sooyoung-wind
- 트랙: Auto-Paper
- 상태: Week 03 결과물 (toego 퇴고와 심사 4라운드, 최종 Minor revision 반영)
- 원고 언어: 한국어 (영문 초록 병기)

LLM·RAG 애플리케이션 평가용 골든 데이터셋을 어떻게 구축하고, 어떤 측면에서 검증하며, 어떤 조건에서 "골든"이라 부를 수 있는지를 정리한 4쪽 미니 리뷰입니다(6쪽 확장판 별도). 이전 작업인 [LLM-as-a-Judge 서베이](https://github.com/Pseudo-Lab/no-more-slops/tree/auto-paper/llm-as-judge-survey/tracks/auto-paper/projects/llm-as-judge-survey)(2,185편 망라 서베이)가 분량이 너무 길었던 점을 반영해, 좁은 주제를 다루는 Frontiers Mini Review 형식을 따랐습니다. 리뷰 유형을 고른 근거는 [docs/review-type.md](docs/review-type.md)에 있습니다.

## 결과물

- [outputs/week-03/README.md](outputs/week-03/README.md): 최종 PDF와 원고, 검증 기록

## 진행 방식

| 단계 | 내용 | 기록 |
| --- | --- | --- |
| 1 | 리뷰 유형·형식 결정 (Frontiers Mini Review, A4 2단) | [docs/review-type.md](docs/review-type.md) |
| 2 | 문헌 조사 (구축·검증·정의 3개 주제 병렬) | [research/](research/), [docs/search-log.md](docs/search-log.md) |
| 3 | 초안 작성 | `manuscript/source.md`, `manuscript/references.md` |
| 4 | toego 퇴고 (린트 → 문장 → 문단·절 → 사실 검증 → 비교 HTML) | `reviews/round*/` |
| 5 | 심사위원 에이전트 심사 → 지적 전부 반영 → 부족한 자료 추가 조사 | `reviews/round*/referee.md`, `response.md` |
| 6 | 4–5단계를 라운드마다 반복(3회 + 확인 재심 1회) | `reviews/round1/`–`round4/` |
| 7 | 4쪽판 압축과 별도 심사 3회 | `reviews/4p/` |
| 8 | Codex·Gemini CLI headless 외부 심사 2라운드(실무 지침성 강화) | `reviews/ext-r1/`, `reviews/ext-r2/`, 확인 심사 `reviews/ext-check/` |

라운드별 산출물은 다음과 같습니다.

- `lint.json`: toego 린터 결과
- `sent-*.json`, `para.md`: toego 문장·문단 감사
- `fact-check.md`: toego 사실 검증
- `퇴고_비교.html`: 수정 전후 비교
- `referee.md`: 심사보고서
- `response.md`: 항목별 반영 내역

## 빌드

`app/`은 [uv](https://docs.astral.sh/uv/)로 실행합니다. PDF 변환에는 Chromium(headless)이 필요합니다.

```sh
cd app
uv run build.py        # source.md + references.md -> manuscript/paper.md (인용 번호 부여, 본문 분량 출력)
uv run pdf.py --out ../outputs/week-03/paper-extended.pdf   # 6쪽 확장판
uv run build.py --src source-4p.md --out paper-4p.md
uv run pdf.py --keep-all --float-wide --src ../manuscript/paper-4p.md --out ../outputs/week-03/paper.pdf   # 4쪽 최종본(표는 쪽 상·하단)
uv run check_pdf.py --png-dir ../reviews/png/final   # 쪽수 확인, 쪽별 PNG
```

보조 도구는 다음과 같습니다.

- `md_extract.py`: 원고를 toego 추출 형식(`paragraphs.json` 등)으로 변환합니다. toego의 `lint_ko.py`와 `build_html.py`를 그대로 쓰기 위한 도구입니다.
- `assemble_review.py`: 라운드별 감사 결과를 toego `review.json`으로 묶고 비교 HTML을 만듭니다.
- `normalize_refs.py`: arXiv API와 Crossref 메타데이터로 참고문헌 저자 표기를 ICMJE 6인 규칙에 맞춥니다. 결과는 `data/authors.json`에 캐시합니다.

본문 글꼴은 Noto Serif KR과 Noto Sans KR(SIL OFL)입니다. 로컬에 있으면 `manuscript/.fonts/`로 복사해 쓰고, 이 폴더는 커밋하지 않습니다.

## 사용한 스킬

[docs/skills-used.md](docs/skills-used.md)에 `tracks/auto-post/skills/` 검토 결과와 toego 사용 내역을 기록했습니다.

## 관련 프로젝트

- [rag-judge-order-bias](../rag-judge-order-bias/README.md): 같은 작성자의 LLM 판정 순서 편향 실험
