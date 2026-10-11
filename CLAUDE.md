## 하네스: Phantom Report 주간 호 제작

**목표:** 매주 AI 사건 캐러셀을 틀린 사실 없이 만든다.

**트리거:** 주간 호 제작이나 그 일부(수집, 채택, 팩트체크, 원고, 최종 대조)를 요청하면 `phantom-weekly` 스킬을 쓴다. 이미지·PNG만이면 `phantom-images`. 단순 질문은 바로 답한다.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-10-11 | 초기 구성 (scout, fact-checker, writer, phantom-weekly) | 전체 | FILE 01 수동 제작에서 사실 오류 4건이 늦게 잡힘 |
| 2026-10-11 | 호 번호를 ISO 주차에서 FILE NN(첫 발행 10/10 기준)으로, 원고 규칙을 2안(이미지 크게·요약 1문장)으로, render.py에 넘침 경고 추가 | README, writer, scout, fact-checker, phantom-weekly, phantom-images, scripts | 1안 규칙으로 쓰면 2안 템플릿에서 글이 넘침 |
