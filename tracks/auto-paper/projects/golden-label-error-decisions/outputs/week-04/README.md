# Week 04 결과물

| 결과물 | 파일 | 상태 |
| --- | --- | --- |
| 논문 초안 | [paper.md](paper.md), [fig/](fig/) | 실험 결과 반영 1차 초안. 심사·퇴고 전 |

## 검증

- 수치는 `app/analyze.py`의 재실행 결과(`results/*.csv`, `e1_summary.json`)에서 가져왔습니다(이 브랜치에서 재실행 확인).
- 문항 결합: 5,690/5,700문항, 리더보드 정답과 Redux 원래 정답 일치율 100%.
- 모델 40종 포함, 6종 제외(OLMo-7B, deepseek-llm-7b-base, internlm2-7b는 데이터셋 접근 제한, Llama-2 chat 3종은 전체 MMLU 실행 없음).

## 데이터 출처와 라이선스

- MMLU-Redux 2.0: `edinburgh-dawg/mmlu-redux-2.0` (CC BY 4.0). 저장소에는 복사하지 않고 스크립트로 내려받습니다.
- Open LLM Leaderboard v1 details: `open-llm-leaderboard-old/details_*`. 저장소에는 복사하지 않습니다.
