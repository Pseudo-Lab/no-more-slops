---
name: phantom-images
description: Phantom Report 주간 호의 슬라이드 이미지를 만들고 인스타 캐러셀 PNG(1080x1350)로 뽑을 때 쓴다. "이미지 만들어", "캐러셀 뽑아", "PNG로" 같은 요청.
---

호 `F`(예: file-01) 기준, 프로젝트 루트에서:

1. 프롬프트: `issues/F.prompts.json`에 슬라이드 번호("01"~)별 장면 묘사를 영어로 쓴다.
   - 공통 스타일(흑백 증거 사진, 글자·로고·실존 인물 얼굴 없음)은 `scripts/gen_images.py`의 STYLE에 있다. 장면만 쓴다.
   - 성범죄 사건은 증거물·사물로만 은유한다.
2. 생성: `python3 scripts/gen_images.py issues/F.prompts.json design/img/F`
   - Codex CLI(ChatGPT 로그인)로 만든다. 401·토큰 오류면 사용자에게 `! codex logout && codex login --device-auth`를 부탁한다.
   - 이미 있는 png는 건너뛴다. 다시 만들려면 그 파일을 지운다.
3. 슬라이드: 직전 호 `design/*.html`을 복사해 `design/F.html`로 만든다. 표지·사건 장은 `.exh`(증거 사진 크게), 목록·마무리는 `.ph faint`가 `img/F/NN.png`를 배경으로 쓴다.
4. PNG: `python3 scripts/render.py design/F.html out/F` → `out/F/01.png`…
5. render.py가 글이 넘친 장을 `WARN`으로 알려 준다(종료 코드 1). 넘치면 그 장의 문구를 줄이고 다시 뽑는다. 그다음 PNG 몇 장을 직접 열어 이미지와 글자 가독성을 본다.
