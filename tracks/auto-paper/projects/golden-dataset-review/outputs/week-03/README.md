# Week 03 결과물

LLM·RAG 애플리케이션 평가용 골든 데이터셋의 구축과 검증을 다룬 미니 리뷰입니다(한국어, 영문 초록 병기).

| 결과물 | 파일 | 상태 |
| --- | --- | --- |
| **최종 원고 (A4 2단 4쪽)** | [paper.pdf](paper.pdf), [paper.md](paper.md) | 주 결과물. 확장판을 4쪽으로 압축한 뒤 별도 심사 3회(1차 Major: 필수 3·권고 14, 재심 Minor: 필수 4·권고 6, 최종 확인 Minor: 필수 1·권고 5)를 모두 반영: [reviews/4p/](../../reviews/4p/). 원본 `manuscript/source-4p.md`. 빌드: `uv run build.py --src source-4p.md --out paper-4p.md && uv run pdf.py --keep-all --src ../manuscript/paper-4p.md --out ../outputs/week-03/paper.pdf` |
| 확장판 (A4 2단 6쪽) | [paper-extended.pdf](paper-extended.pdf), [paper-extended.md](paper-extended.md) | 본 심사 4라운드를 모두 반영한 전체 원고(본문 3,000어절, 참고문헌 79편). 원본 `manuscript/source.md`. 빌드: `uv run build.py && uv run pdf.py --out ../outputs/week-03/paper-extended.pdf` |
| 중간 원고 PDF | [drafts/](drafts/) | v2–v7. 심사 기록의 `reviews/roundN/paper-vX.pdf` 경로는 이 폴더의 같은 파일명을 가리킨다 |

저자 정보, 연구비, 이해상충, 데이터 DOI는 `[추후 기입]`으로 남아 있다.

## 형식과 분량

- 형식: Frontiers Mini Review(Abstract → Introduction → 주제 소절 → Discussion), 근거는 [docs/review-type.md](../../docs/review-type.md)
- 분량: 최종 원고 4쪽(참고문헌 62편, 표 2개). 확장판은 본문 3,000어절, 참고문헌 79편, 6쪽

## 진행 기록(End-to-End 4회)

| 라운드 | toego 퇴고 | 심사 판정 | 기록 |
| --- | --- | --- | --- |
| 1 | 린트 32건, 문장 83건, 구조 12항목, 사실 16건 | Major revision (M7, m27) | [reviews/round1/](../../reviews/round1/) |
| 2 | 린트 53건, 문장 58건, 구조 8건, 사실 13건 | Major revision (M5, m22) | [reviews/round2/](../../reviews/round2/) |
| 3 | 린트 57건, 문장 29건, 구조 8건, 사실 8건 | Minor revision (M3, m16) | [reviews/round3/](../../reviews/round3/) |
| 4 | — (재심) | Minor revision (필수 3, 권고 4) → 반영 후 편집자 확인 수준 | [reviews/round4/](../../reviews/round4/) |

각 라운드 폴더에는 심사보고서(`referee.md`), 항목별 응답서(`response.md`), toego 비교 HTML(`퇴고_비교.html`)이 있습니다. 심사위원이 요청한 추가 문헌 조사는 [research/](../../research/)의 r2–r5에 있습니다.

## 검증

- 인용 수치: 라운드마다 toego fact-checker와 심사위원이 원문(arXiv, ACL Anthology, Crossref, 공식 페이지, 웹 아카이브)과 대조. 3차 심사에서 DOI 35개 전수 Crossref 확인.
- 본고 계산 수치(확장판 4.3·4.4절, 4쪽판 4장·5.1): 별도 에이전트와 심사위원이 재계산(17%p, 4,361문항, p_d 약 0.497, Wilson 하한 1.9%, δ/4 기준 509문항, 864/428문항, Connor 식 870/434).
- 재실행한 검사: `uv run build.py`, `uv run pdf.py`, `uv run check_pdf.py`(4쪽판 4쪽, 확장판 6쪽 확인), 저장소 검사 `scripts/check_repository.py`.

## 미확인·남은 사항

- 저자명·소속·교신 연락처, 저자 기여, 연구비, 이해상충, 보충 자료 DOI, 저자가 원문을 직접 대조한 범위는 저자가 기입해야 한다.
- 일부 출처(OpenAI 블로그 2건)는 원 사이트가 403을 반환하여 웹 아카이브 사본으로 확인하였다.
- OpenAI Evals 문서는 2026-10-31 읽기 전용, 2026-11-30 종료 예정이다.
