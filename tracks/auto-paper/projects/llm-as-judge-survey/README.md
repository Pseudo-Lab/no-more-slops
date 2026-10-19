# LLM-as-a-Judge 서베이

- 작성자: @sooyoung-wind
- 트랙: Auto-Paper
- 상태: 3단계(선별) 대기
- 원고 언어: 한국어 (검수용)

LLM이 평가자·판정자 역할을 하는 연구(LLM-as-a-Judge)를 2023–2026년 범위에서 망라하는 서베이 논문 작업입니다. 기존 일반 서베이가 2024년 말에 머물러 있고 2025–2026년 연구는 의료·코드·보안 등 분야별로만 정리되어 있어, 그 기간 전체를 다시 묶는 것을 목표로 합니다.

## 진행 단계

| 단계 | 내용 | 산출물 | 상태 |
| --- | --- | --- | --- |
| 1 | 주제·범위 정의 | [docs/scope.md](docs/scope.md) | 완료 |
| 2 | 문헌 검색 | [data/search_log.csv](data/search_log.csv), [data/candidates.csv](data/candidates.csv) (10,141편) | 완료 (2026-10-19) |
| 3 | 선별 | 포함·제외 기록, 편수 흐름 | 대기 |
| 4 | 추출·종합 | 논문별 추출표, 분류 체계 | 대기 |
| 5 | 집필 | 원고 초안 | 대기 |
| 6 | 검증·퇴고 | 인용 대조 기록, 수정본 | 대기 |

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

## 사용한 스킬·도구

- OpenAlex, arXiv, Semantic Scholar 공개 API (`app/`의 스크립트)

## 관련 프로젝트

- [rag-judge-order-bias](../rag-judge-order-bias/README.md) ([#13](https://github.com/Pseudo-Lab/no-more-slops/pull/13)): 같은 작성자의 LLM 판정 모델 순서 편향 실험.
