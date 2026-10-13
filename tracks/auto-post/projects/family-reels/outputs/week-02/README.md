# 2주차 · 밈 사전 기획과 파이프라인 화면

- 작성자: [임경태 · darkwingduck-code](https://github.com/darkwingduck-code)
- 원본 PR: [#9](https://github.com/Pseudo-Lab/no-more-slops/pull/9)
- 선행 PR: [1주차 #15](https://github.com/Pseudo-Lab/no-more-slops/pull/15). PR의 기반 브랜치 관계를 유지합니다.
- 결과물: [instagram-automation-pipeline.html](instagram-automation-pipeline.html)
- 제작 절차: [family-reel-meme-preflight](../../../../skills/family-reel-meme-preflight/SKILL.md), [instagram-reel](../../../../skills/instagram-reel/SKILL.md)

저장소 루트에서 `python -m http.server 8000`을 실행하고 다음 주소를 엽니다.

```text
http://localhost:8000/tracks/auto-post/projects/family-reels/outputs/week-02/instagram-automation-pipeline.html
```

화면은 1·2주차 흐름, Three.js 보물상자와 단계별 진행 시연, Instagram·YouTube·TikTok·X × 한국·일본·미국의 12개 조합 상태판, 로컬 `trend-plan.json` 읽기를 제공합니다. 진행 체험은 화면 시연이며 플랫폼 API·Python·FFmpeg를 직접 실행하지 않습니다. JSON은 브라우저 안에서 읽고 서버에 업로드하지 않습니다. 버전을 고정한 Three.js CDN 모듈이 로드되지 않으면 2D 대체 화면이 남습니다.

원본 PR에는 스킬 형식 검사, 별도 선별기 테스트 4개, 브라우저 렌더 및 스크립트 구문 검사를 수행했다고 기록되어 있습니다. 해당 선별기·영상 렌더 스크립트, 5분 발표 PPTX, 대본·예상 Q&A는 별도 제작 저장소에 있으며 이 저장소에 포함되지 않습니다.

현재 12개 조합은 확인된 원본 조회수·안전 검토 근거가 부족해 후보 선정을 보류한 상태입니다. 공개 지표 자동 수집은 연결되지 않았으며 조회수 증가를 보장하지 않습니다. 1주차 영상 링크는 [1주차 결과물](../week-01/README.md)에 보관합니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
