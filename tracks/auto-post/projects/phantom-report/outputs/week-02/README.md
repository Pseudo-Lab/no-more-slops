# 2주차 · Phantom Report FILE 02

- 작성자: [박용욱 · yongukpark](https://github.com/yongukpark)
- 원본 PR: 아직 없음
- 발행 기록: FILE 02, 2026-10-17(토) 발행분(10/18 제작), 사건 5건(CASE #006~#010)·슬라이드 7장.
- 게시용 캡션: [file-02/caption.txt](file-02/caption.txt)
- 편집 가능한 원본: [디자인 HTML](../../design/file-02.html), [장별 이미지](../../design/img/file-02/), [이미지 프롬프트](../../issues/file-02.prompts.json), [원고·출처·최종 대조](../../issues/file-02.md)
- 제작 과정: [2주차 개선 기록](../../devlog/week-02.md)
- 발표 자료: [phantom_report_week_2.pptx](phantom_report_week_2.pptx)

프로젝트 폴더에서 아래 명령으로 게시용 PNG를 다시 만듭니다. Python과 Playwright Chromium이 필요합니다. 재생성할 수 있는 PNG는 기존 방침대로 커밋하지 않습니다.

```sh
python3 scripts/render.py design/file-02.html outputs/week-02/file-02
```

이번 호는 하네스(`phantom-weekly`)로 수집부터 최종 대조까지 다시 만들었습니다(10/18). 채택과 원고 승인은 사용자가 했습니다. 과정에서 규칙 세 가지를 고쳤습니다. 수집 기간은 첫 보도일 기준으로 판단하고, AI 관여가 확인되지 않은 사건은 제목에 미확정이라고 표시하고, 1차 출처를 못 찾은 사건은 보류합니다. 그래서 금융권 침해사고(AI 관여 미확정)와 제타 챗봇(1차 출처 없음)은 싣지 않았습니다. 최종 대조 결과는 "불일치 없음"이고, 참고로 나온 2건도 고쳤습니다. 공개 게시는 하지 않았습니다.
