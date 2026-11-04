# 제작 (제작 설계 · 키프레임 · 영상)

- **하는 일:** 콘티를 실제로 만들 방법을 정하고 키프레임과 릴스를 만든다
- **읽을 것:** `CLAUDE.md`, `brand/channels.md`, `skills/`, `posts/<id>/product.md`, `product-ref/`, `storyboard.md`
- **쓸 것:** `production.md`, `keyframes/`, `video/`, `sources.md`(미디어 권리 칸), `status.yaml`(production, keyframes, video), `cost.md`
- **도구:** 코드 3D 렌더(Three.js + headless Chrome), ffmpeg. 유료 생성 API는 사람이 승인한 것만

## 규칙
- G2 승인 전에는 `production.md`만 쓰고 생성하지 않는다.
- **유료 API(OpenAI 등)는 사람이 명시적으로 승인하기 전에는 키를 읽지도, 호출하지도 않는다.** 승인 전에는 무료 경로로 만들거나 프롬프트만 남긴다.
- 컷마다 다시 돌릴 수 있게 프롬프트, 설정, 스크립트 경로를 `production.md`에 남긴다.
- 키프레임을 먼저 만들어 사람에게 보여 준 뒤 영상으로 넘어간다.
- 결과물은 렌더한 뒤 반드시 직접 열어서 확인한다(로고, 글자, 비율).
- 최종 릴스: `video/final.mp4`, 9:16 1080×1920, H.264, 30초 이내.

## 보고
만든 파일 목록, 컷별 방식, 규격 충족 여부, 실제와 다르게 나온 부분, 소요 시간과 비용.
