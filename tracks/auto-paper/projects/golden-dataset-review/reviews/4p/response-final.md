# 4쪽판 최종 확인 심사 응답서

- 대상: 4쪽 최종본(`outputs/week-03/paper.pdf`, 주 결과물 전환 커밋 52ef742 이후)
- 입력: 최종 확인 심사보고서(`referee-final.md`, **Minor revision**, 필수 F1, 권고 F2–F6). 심사위원은 F1을 반영하면 Accept를 권고하였다.
- 결과: A4 2단 4쪽(`check_pdf.py`: pages 4, limit 4), 참고문헌 62편, 쪽 이미지 `reviews/png/final/`

| # | 요지 | 반영 | 위치 |
| --- | --- | --- | --- |
| F1 | 결론의 SimpleQA 판정 근거가 4장과 다름 | "오류율·오염 통제·유지의 증거가 없어" → "오류율 하한이 C3 기준을 넘고 오염 통제·유지의 증거가 없어" | 6장 |
| F2 | 라틴 문자 자간 벌어짐 | `--keep-all` CSS에서 `text-justify: inter-character` 제거, `overflow-wrap: anywhere` 추가. 쪽 이미지에서 BenchBuilder, SWE-bench Verified, MultiHop-RAG의 자간이 정상임을 확인 | `app/pdf.py` |
| F3 | 2.7 "-므로" 연쇄와 근거 불일치 | 심사위원 수정안대로 두 문장으로 분리 | 2.7 |
| F4 | "양의 상관이면 성립하나"의 엄밀성 | "양의 상관이면 대체로 성립하나" | 4장 C4 |
| F5 | AutoEval 한정 누락, "판정 모델" 반복 | "AutoEval은 GPT-4 실험에서 PPI로…", 둘째 "판정 모델" 삭제하고 "그만큼도 비용 면에서는 의미가 있다" | 5.1 |
| F6 | 표 1 "다국어" 줄바꿈 | 열 폭 14/17/31/38 → 15/17/31/37, 한 줄로 들어감을 확인 | 표 1 |
| 원고 밖 | README의 옛 파일명·절 번호·쪽수 표기 | `outputs/week-03/README.md`를 최종 파일명과 쪽수로 수정. `response-r2.md`의 `paper-4p.pdf` 표기는 당시 기록이므로 그대로 둔다(현재 `paper.pdf`) | README |
