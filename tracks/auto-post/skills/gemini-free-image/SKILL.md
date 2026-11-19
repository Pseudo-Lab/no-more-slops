---
name: gemini-free-image
description: 무료 Gemini 웹(gemini.google.com)으로 카드·표지용 이미지를 만들고, 브라우저 자동화로 원본에 가까운 해상도로 저장할 때 쓴다. 직접 내려받기가 막힐 때의 화면 확대 캡처 방법과 하루 한도에 걸렸을 때의 대안을 담는다. 유료 API는 쓰지 않는다
---

# 무료 Gemini 이미지 만들기와 저장

## 언제 쓰나

- 남의 브랜드 상품처럼 공식 사진을 쓸 권리가 없는 카드: 용기와 로고 없이 질감·분위기만 그린다(크림 질감, 물방울, 발색, 빛)
- 표지 배경, 무드 이미지

## 프롬프트 원칙

- 용기, 로고, 글자는 그리지 않게 한다: `no bottle, no packaging, no logo, no text`
- 비율을 적는다: `vertical 3:4`
- 카드 아래쪽에 글자가 올라가니 `subject in upper half, soft empty lower area`
- 색은 계정 팔레트로 맞춘다(예: 라일락·연보라 배경)
- 결과물에는 "이미지는 AI 연출" 표기를 카드나 캡션에 넣는다
- Gemini가 넣는 AI 생성 표시(워터마크)는 지우지 않는다

## 저장: 화면 확대 캡처

Gemini 페이지는 보안 정책 때문에 이미지 blob을 가져와 로컬 서버로 보내는 방법이 막힌다. 다운로드 버튼도 자동화에서 잘 안 된다. 대신 이미지를 화면에 크게 띄우고 확대 캡처한다.

1. 이미지가 생성된 탭에서 자바스크립트로 덮개를 띄운다. `innerHTML`은 TrustedHTML 정책으로 막히니 요소를 직접 만들고 `replaceChildren`을 쓴다. 원래 이미지를 복제하면 둥근 모서리가 따라오므로 새 `img`를 만든다

```js
window.__ov = () => {
  const src = [...document.querySelectorAll('img')]
    .filter(i => i.naturalWidth >= 1000).pop().src;   // 가장 최근 큰 이미지
  const d = document.createElement('div');
  d.id = '__ov';
  d.style.cssText = 'position:fixed;inset:0;z-index:2147483647;background:#000;display:flex;align-items:flex-start;justify-content:flex-start';
  const im = document.createElement('img');
  im.src = src;
  im.style.cssText = 'height:100vh;width:auto;border-radius:0;display:block';
  d.replaceChildren(im);
  document.body.appendChild(d);
  return [im.naturalWidth, im.naturalHeight, im.getBoundingClientRect().width, im.getBoundingClientRect().height];
};
__ov();
```

2. 브라우저 도구의 확대(zoom) 기능으로 이미지 영역만 잡아 파일로 저장한다(배율 축소 없이). 예: 화면 높이 약 930px일 때 영역 `[0,0,585,783]` → 약 952×1275 저장
3. 다음 이미지 전에 덮개를 지운다: `document.getElementById('__ov')?.remove()`
4. 저장한 파일의 크기와 내용을 열어서 확인한다(잘림, 검은 여백)

## 하루 한도

무료 계정은 하루 생성 수가 정해져 있다. "한도에 도달" 안내가 뜨면 다음 날 초기화된다.

- 대안 1: 비슷한 카테고리의 이미 만든 이미지를 재사용(예: 같은 선크림 질감)
- 대안 2: 표지를 새로 만들지 않고 안쪽 카드 이미지 여러 장을 이어 붙인 콜라주로
- 유료 API나 요금제 업그레이드는 사람 승인 없이 하지 않는다
- 많이 필요하면 한 번에 몰지 말고 표지·핵심 카드부터 만든다

## 자주 한 실수

- 로컬 서버로 보내려다 포트 충돌, 이어서 보안 정책 차단으로 시간을 버렸다 → 처음부터 확대 캡처
- 덮개를 innerHTML로 만들다 오류 → replaceChildren
- 원본 이미지를 복제해 둥근 모서리가 캡처에 남음 → 새 img, border-radius 0
