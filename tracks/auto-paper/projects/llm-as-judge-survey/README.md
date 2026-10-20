# LLM-as-a-Judge 서베이

- 작성자: @sooyoung-wind
- 트랙: Auto-Paper
- 상태: 초안 완료 (Week 02)
- 원고 언어: 한국어 (검수용)

LLM이 평가자·판정자 역할을 하는 연구(LLM-as-a-Judge)를 2023–2026년 범위에서 망라하는 서베이 논문 작업입니다. 기존 일반 서베이가 2024년 말에 머물러 있고 2025–2026년 연구는 의료·코드·보안 등 분야별로만 정리되어 있어, 그 기간 전체를 다시 묶는 것을 목표로 합니다.

## 진행 단계

| 단계 | 내용 | 산출물 | 상태 |
| --- | --- | --- | --- |
| 1 | 주제·범위 정의 | [docs/scope.md](docs/scope.md) | 완료 |
| 2 | 문헌 검색 | [data/search_log.csv](data/search_log.csv), [data/candidates.csv](data/candidates.csv) (10,273편) | 완료 (2026-10-19) |
| 3 | 선별 | [docs/screening.md](docs/screening.md), [data/screening.csv](data/screening.csv) | 완료 (포함 2,185편) |
| 4 | 추출·종합 | [docs/extraction.md](docs/extraction.md), 논문별 추출표, 분류 체계 | 완료, [종합 초안](docs/findings.md) |
| 5 | 집필 | [원고](manuscript/), [초안 PDF](outputs/week-02/paper.pdf) | 초안 완료 |
| 6 | 검증·퇴고 | [사실 검토·퇴고 기록](docs/outline.md), data/audit/ | 1차 완료 |

## 문헌 검색 실행 (2단계)

`app/`은 외부 패키지 없이 표준 라이브러리만 사용합니다. 검색식은 `app/queries.json`에 있습니다.

```sh
cd app
uv run search.py              # OpenAlex·arXiv·Semantic Scholar 키워드 검색
uv run snowball.py            # Awesome 목록 시드 + 기존 서베이 참고문헌·인용 1단계 추적 + arXiv HTML 참고문헌 보완
uv run merge.py               # 중복 제거 → data/candidates.csv
```

- 원자료: `data/raw/<step>/<source>/<query>.jsonl` (용량 때문에 커밋하지 않음, 스크립트로 재생성)
- 실행 기록: `data/search_log.csv` (실행 시각, 출처, 검색식, 건수)
- 선택 환경 변수: `OPENALEX_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY`. 키가 없으면 공용 한도를 공유하므로 OpenAlex는 401, Semantic Scholar는 429로 중단·지연될 수 있습니다.

## 제목·초록 선별 (3단계)

```sh
cd app
uv run screen.py prepare --round r1 --title-hit   # 미선별 후보를 배치로 분할
# 배치별로 서브에이전트가 docs/screening.md 기준으로 판정 → data/screening/results/<batch>.jsonl
uv run screen.py collect                          # data/screening.csv 갱신, 검수 표본 추출
```

- 1차 선별자: Claude Code 서브에이전트 (Sonnet), 배치당 약 140편
- 사람 검수: 포함·제외 각 50편 무작위 표본을 검수 페이지(`uv run audit_page.py OUT.html`로 생성, claude.ai 아티팩트로 게시)에서 판정한다. 판정은 아티팩트 저장소의 `audit` 컬렉션에 저장되고, 내보낸 뒤 `uv run screen.py audit-import EXPORT_DIR`로 `data/screening/audit.csv`에 반영한다. `maybe`는 전문 검토 단계에서 처리한다.
- 배치 파일은 `candidates.csv`에서 재생성되므로 커밋하지 않는다.

## 정보 추출 (4단계)

```sh
cd app
uv run extract.py prepare --round e1 --size 70   # 포함 논문 중 미추출분을 배치로 분할
# 배치별로 서브에이전트가 docs/extraction.md 항목대로 추출 → data/extraction/results/<batch>.jsonl
uv run extract.py collect                        # 형식 검사, who 추가, data/extraction.jsonl 갱신
```

- 논문마다 PMDRL 요약(Who, Problem, Method, Data, Result, Limitation, Gap)과 분류 코드를 기록한다.
- 추출자: Claude Code 서브에이전트 (Sonnet), 배치당 70편, 제목·초록 기준

## 사용한 스킬·도구

- OpenAlex, arXiv, Semantic Scholar 공개 API (`app/`의 스크립트)

## 관련 프로젝트

- [rag-judge-order-bias](../rag-judge-order-bias/README.md) ([#13](https://github.com/Pseudo-Lab/no-more-slops/pull/13)): 같은 작성자의 LLM 판정 모델 순서 편향 실험.
