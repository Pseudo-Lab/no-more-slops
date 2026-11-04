# Week 02 결과물

- 작성자: @sooyoung-wind
- 트랙: Auto-Paper
- 원본 PR: 미정 (아직 열지 않음)
- 결과물: [논문 초안](paper.pdf) (A4 71쪽, 한국어)
- 상태: 초안. 사실 검토와 퇴고를 한 차례 거쳤지만 사람이 원고 전체를 검수하지는 않았다.
- 사용한 스킬: toego 퇴고 절차(`toego:revise`, 저장소 밖 플러그인)를 마크다운 원고에 적용했다. 이 저장소의 스킬은 추가하거나 바꾸지 않았다.

## 내용

LLM-as-a-Judge 문헌(2023-01–2026-10) 2,185편을 판정 구성, 신뢰성과 편향, 개선 기법, 응용 분야, 보안의 다섯 축으로 분류했다. 비교 질문 12개에 대한 주장 928개를 지지·반박·조건부·효과 없음으로 집계했고, 결과가 갈린 7개 질문은 독립 평가 주장 99개를 본문으로 확인했다. 9장은 조건 변수와 근거의 치우침을 종합하고, 10장은 연구 의제 7개(A1–A7)를 제시한다.

## 재현

```sh
cd tracks/auto-paper/projects/llm-as-judge-survey/app
uv run manuscript.py refs     # 인용 키 검사, 참고문헌 생성
uv run manuscript.py render   # manuscript/build/paper.md (번호 인용)
uv run pdf.py                 # manuscript/build/paper.pdf (Chromium 필요)
```

## 검증 (이번에 실행한 것)

- 인용 643개, 논문 355편, 포함 목록에 없는 인용 0건 (`manuscript.py refs`)
- 장별 독립 사실 검토 a1: 지적 69건 반영 (`data/audit/a1-*`)
- 퇴고 t1: 문장·문단·흐름 검토 후 반영, 바뀐 문장 사실 검증 지적 15건 반영 (`data/audit/t1/`, 요약은 [docs/outline.md](../../docs/outline.md))
- `python3 scripts/check_repository.py`, `git diff --check` 통과

## 미확인 범위

- 선별·추출·주장 기록·본문 확인은 LLM 서브에이전트가 했고, 사람 검수는 선별 표본 200편(일치 98.5%)뿐이다.
- 주장은 초록 기준이며 본문 확인은 99개 주장에 한정된다. Q-HARD·Q-ATTACK·Q-SELF·Q-FT·Q-DEBIAS는 본문 확인을 하지 않았다.
- 애매로 남은 1,868편은 검토하지 않았다.
