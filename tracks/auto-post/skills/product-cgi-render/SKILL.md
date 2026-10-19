---
name: product-cgi-render
description: 사람 없이 제품만 나오는 세로 CGI 릴스(9:16, 30초 이내)를 확정된 콘티에서 만든다. 유리병·스포이트·뚜껑처럼 회전체 용기를 단면 점으로 모델링해 Blender(Cycles)로 굴절·라벨·스튜디오 룩을 렌더하고, 공통 마감·글자 오버레이·CC0 효과음 믹스·콘티 순서 조립·측정 QC(255 픽셀, 같은 세계 평균색, 루프 이음매)까지 한다. 제품과 무관하게 설정 JSON으로 움직인다. 촬영 영상 편집이나 사진 캐러셀에는 쓰지 않는다
---

# 제품 CGI 릴스 렌더

확정된 콘티(컷 목록)를 **한 세계로 보이는** 제품 CGI 릴스로 만든다. 핵심은 세 가지다.

1. 라벨 글자가 보이는 화면은 **3D 렌더로만** 만든다. AI 영상은 0.5초 안에 작은 글자를 바꾼다.
2. 모든 컷을 같은 룩(스튜디오 색, 액체 색, 그레인, 아래 그레이드)과 같은 마감 단계로 만든다.
3. "좋아 보인다" 대신 **수치로 통과**시킨다. 255 픽셀 0개, 기준 컷 대비 평균색 채널당 10 이하, 루프 이음매 10 이하.

배운 점과 근거는 [references/lessons.md](references/lessons.md), 설정 전체 형식은 [references/config.md](references/config.md)에 있다.

## 언제 쓰나

| 상황 | 쓸 스킬 |
|---|---|
| 제품 광고 아이디어·스토리라인·콘티를 짠다 | `ad-planning` (이 스킬의 앞 단계) |
| **콘티가 확정됐고, 제품(병·스포이트·뚜껑)이 나오는 CGI 컷을 렌더해 릴스로 조립한다** | **이 스킬** |
| JSON 장면으로 사진 캐러셀·인포그래픽 릴스를 만든다 | `instagram-content` |
| 촬영한 영상을 잘라 세로 릴스로 편집한다 (자막·음량) | `instagram-reel` |

`instagram-content`는 장면 JSON → 평면 그래픽(카드·캐러셀), `instagram-reel`은 실제 촬영 영상 편집이다. 이 스킬은 **3D 제품 모델과 물리 기반 렌더**(유리 굴절, 액체, 인쇄 라벨, 그림자)를 다룬다는 점이 다르다. 입력은 콘티와 제품 단면·라벨 PNG이고, 출력은 컷 영상과 조립본, QC 표다.

쓰지 않는 경우: 사람·손·얼굴이 나와야 하는 컷, 회전체가 아닌 복잡한 용기(튜브·펌프 디스펜서의 비대칭 부품. 회전체 부품만 이 도구로 만든다), 실제 촬영본 보정.

## 입력과 출력

**입력**
- 확정된 콘티: 컷마다 번호·길이·동작·카메라·글자 (`ad-planning` 6절 형식). 사람 승인(G2) 전에는 이미지·영상을 만들지 않는다
- 제품 프로필 JSON: 병 단면 점, 액체 높이, 라벨 위치, 뚜껑·스포이트 부품 단면 ([assets/test-bottle.json](assets/test-bottle.json) 형식)
- 라벨 PNG: 투명 바탕 인쇄 글자. **사람이 실제 제품과 글자 단위로 같게** 준비한다. 브랜드 로고·라벨 PNG는 이 스킬에 넣지 않는다
- 프로젝트 설정 JSON: look(세계), 컷 목록과 키프레임, 효과음 ([assets/example-project.json](assets/example-project.json))
- 효과음: CC0 또는 직접 녹음·합성한 것만

**출력** (설정 폴더 기준, 위치는 설정으로 바꾼다)
- `frames/<컷>/f0000.png …` 보정본, `raw/` 보정 전, `render.json` (샘플·크기·미리보기 여부·시간)
- `cuts/<컷>.mp4` + `-sheet.png` 접촉 시트 + `.render.json`
- `audio/mix.wav`, `video/assembly-latest.mp4` + `.json` (컷별 상태, 최종 여부)
- QC 표 (터미널 출력, `--json` 가능) → `review.md`·제작 기록에 붙인다

## 작업 순서

```
콘티 확정(G2) → ① 제품 프로필·라벨 → ② 설정(look·컷) → ③ 저샘플 정지 확인 → ④ 키 프레임 확인
→ ⑤ 예산 → ⑥ 최종 렌더(1회 + 재렌더 1회) → ⑦ 공통 마감 + 글자 → ⑧ QC → ⑨ 효과음 → ⑩ 조립 → ⑪ 루프 확인
```

1. **제품 프로필.** 공식 정면 사진에서 몸통 반지름을 기준 단위로 정하고(예: 145px = 0.62), 바깥 단면 점 `(r, z)`를 바닥 축에서 입구까지 잰다. 유리 두께·바닥 두께·액체 높이를 적는다. 안쪽 단면은 자동(법선 방향 오프셋)이지만 모서리가 많으면 직접 준다. 라벨은 사진에서 글자 위치를 재 HTML/SVG로 다시 조판해 투명 PNG로 뽑는다(가장 작은 줄이 최종 화면에서 2,000px 이상, 매크로 컷은 2배 판).
2. **설정.** `assets/example-project.json`을 작업 폴더(예: `posts/<id>/production/`)에 복사해 컷을 콘티대로 적는다. look은 한 번 정하면 모든 컷이 같은 값을 쓴다.
3. **정지 확인 (저샘플).** 장면 하나를 540×960, 8~16샘플로 렌더해 라벨 철자·용량 줄·병 목·바닥 그림자를 사진 옆에 놓고 본다.
4. **키 프레임 확인.** 컷마다 첫·가운데·마지막 프레임만 저샘플로 렌더한다(`--frames 0,22,44 --samples 8 --size 540x960`). 이 결과는 자동으로 "미리보기"로 표시되어 최종 조립에 들어가지 않는다.
5. **예산.** 첫 프레임 시간 × 프레임 수로 컷별 시간을 적고 합계가 예산 안인지 본다. 컷 설정 `budget_min`을 넘으면 렌더가 멈춘다.
6. **최종 렌더.** 컷마다 최종 1회 + 재렌더 1회까지. 그래도 QC를 못 넘으면 콘티의 "실패 시 대체"로 간다.
7. **공통 마감.** `compose_cut.py`로 모든 컷(Blender·AI 영상·코드 그래픽)에 같은 그레이드 PNG·그레인·채널 상한을 건다. 글자는 `overlay.mjs`로 투명 프레임을 뽑아 같은 단계에서 얹는다.
8. **QC.** `qc.py white`(255 픽셀 0개), `qc.py means --ref <기준 컷>`(같은 세계), 굴절 컷은 `qc.py highlight`(점 하나, 지름 1/10 이하). 라벨 글자 대조는 사람이 크롭으로 한다.
9. **효과음.** 컷마다 소리 하나(톡·탁·팅). `audio.py`가 시각에 맞춰 얹고 음량을 맞춘다. 반복 재생이면 `loop_tail`.
10. **조립.** `assemble.py`가 콘티 순서대로 잇고 없는 컷은 자리 표시 카드로 채운다. 컷이 완성될 때마다 다시 돌린다.
11. **루프.** `qc.py loop`로 마지막 프레임 ↔ 첫 프레임 평균색을 잰다. 소리 꼬리가 이음매를 넘어 끊기지 않는지 들어 본다.

## 명령

스킬 폴더를 `$SK`로 둔다. Blender는 **한 번에 하나**, 항상 `nice -n 19`로 돌린다. 다른 Blender가 돌고 있으면 기다린다.

```sh
SK=skills/product-cgi-render          # 이 스킬 폴더
CFG=posts/<id>/production/project.json

# ③ 정지 한 장 (저샘플)
nice -n 19 blender -b --factory-startup -P $SK/scripts/scene.py -- --config $CFG --out still.png --samples 12 --size 540x960 --yaw 0 --lift 0

# ④ 키 프레임만 (자동으로 미리보기 표시)
nice -n 19 blender -b --factory-startup -P $SK/scripts/render_cut.py -- --config $CFG --cut c02 --out frames/c02-test --frames 0,30,59 --samples 8 --size 540x960

# ⑥ 최종 렌더
nice -n 19 blender -b --factory-startup -P $SK/scripts/render_cut.py -- --config $CFG --cut c02 --out frames/c02

# ⑦ 공통 마감 (그레이드 PNG는 한 번 만들어 모든 컷에 같은 것을)
python3 $SK/scripts/make_grade.py grade-bottom.png --color 26,42,60 --fraction 0.25 --alpha 24
node $SK/scripts/overlay.mjs $SK/assets/overlay-type-a.html ov/c04 --seconds 1.25 --root . --query "text=첫 줄|둘째 줄&size=118&y=290"
python3 $SK/scripts/compose_cut.py frames/c04 cuts/c04.mp4 --grade grade-bottom.png --overlay ov/c04 --overlay-start 0.25 --grain 6 --cap 240

# ⑧ QC
python3 $SK/scripts/qc.py white cuts/*.mp4
python3 $SK/scripts/qc.py means cuts/c01.mp4 cuts/c02.mp4 cuts/c04.mp4 --ref cuts/c03.mp4
python3 $SK/scripts/qc.py highlight frames/c01/f0030.png --roi 380,820,320,320

# ⑨ 효과음, ⑩ 조립, ⑪ 루프
python3 $SK/scripts/audio.py --config $CFG
python3 $SK/scripts/assemble.py --config $CFG --dry-run
python3 $SK/scripts/assemble.py --config $CFG --audio audio/mix.wav
python3 $SK/scripts/qc.py loop video/assembly-latest.mp4
```

`overlay.mjs`는 `puppeteer-core`가 필요하다. 스킬 폴더에서 `npm install`(설치 결과는 커밋하지 않는다), 또는 이미 설치된 곳을 `PUPPETEER_CORE_DIR=<node_modules가 있는 폴더>`로 준다. Chrome 경로는 `CHROME_PATH`.

## 설정 요약

```jsonc
{
  "fps": 30, "size": [1080, 1920],
  "product": "test-bottle.json",          // 제품 프로필 파일 (또는 객체)
  "cuts_dir": "cuts", "assembly_out": "video/assembly-latest.mp4",
  "look": { ... },                         // 생략한 값은 기본 룩 (scripts/cgi_config.py DEFAULT_LOOK)
  "cuts": [
    {"id": "c02", "duration": 2.0, "desc": "반 바퀴 돌아 정면에 멈춘다",
     "blender": {"motion_blur": 0.5, "budget_min": 30,
                 "camera": [{"f": 0, "target": [0,0,1.68], "yaw": 0, "pitch": 4, "dist": 10.1, "fov": 27},
                            {"f": 59, "dist": 9.3, "ease": "linear"}],
                 "bottle": [{"f": 0, "yaw": -180}, {"f": 30, "yaw": 0, "ease": "out"}],
                 "closure": [{"f": 0, "lift": 0}]}}
  ],
  "audio": {"lufs": -14, "true_peak": -1.5, "loop_tail": true,
            "sfx": [{"file": "sfx/tap.wav", "at": 1.0, "gain_db": -3, "license": "CC0", "source": "…"}]}
}
```

키는 `{"f": 프레임, 값…, "ease": linear|in|out|inout|smooth}`. 값이 있는 키끼리 보간하고 구간 이징은 뒤쪽 키가 정한다. 키로 표현이 안 되는 움직임(액체 모양 변형, 방울 낙하, 수면 물결)은 `render_cut.py`를 본떠 컷 스크립트를 따로 쓰고 `scene.Stage`를 import 한다. 전체 형식은 [references/config.md](references/config.md).

## 파일

| 파일 | 하는 일 |
|---|---|
| `scripts/scene.py` | Blender 장면 모듈 `Stage`: 회전체 병, 굴절 경계면 3개, 인쇄 라벨, 뚜껑·스포이트, 스튜디오, 조명·라이트 링킹, 가장자리 장치, 렌더 설정, 렌더 뒤 보정. 단독 실행 시 정지 한 장 |
| `scripts/render_cut.py` | 컷 설정의 키프레임대로 프레임 렌더 + `render.json`. 예산 확인, 미리보기 자동 표시 |
| `scripts/compose_cut.py` | 프레임/영상 → 공통 마감(그레이드·글자·그레인·채널 상한) → mp4 + 접촉 시트 |
| `scripts/overlay.mjs` + `assets/overlay-type-a.html` | 큰 글자 한 덩어리, 박스 없음, 한 색, 블러 등장·상승 0.3초, 페이드 0.2초. 쿼리로 문구·크기·위치 |
| `scripts/audio.py` | 효과음을 시각에 얹고 2패스 loudnorm (기본 −14 LUFS, −1.5 dBTP), 루프 꼬리, 라이선스 확인 |
| `scripts/assemble.py` | 콘티 순서 조립, 없는 컷·미리보기 컷은 자리 표시 카드, 조립 상태 JSON |
| `scripts/qc.py` | 255 픽셀, 같은 세계 평균색, 루프 이음매, 하이라이트 크기 |
| `scripts/make_grade.py`, `make_label_placeholder.py` | 아래 그레이드 PNG, 시험용 라벨 PNG |
| `scripts/cgi_config.py`, `pngio.py` | 설정·단면 계산·키 보간 (bpy 없이), PNG 쓰기·비트맵 글꼴 |
| `assets/test-bottle.json`, `placeholder-label.png`, `example-project.json` | 일반 시험용 병(실제 제품 아님)·시험 라벨·예시 설정 |

## 한계

- 회전체(lathe)만 만든다. 펌프 노즐, 비대칭 뚜껑, 튜브, 각진 병은 따로 모델링해 `Stage` 장면에 넣는다.
- 액체 변형(방울·막·수면 물결)은 키가 아니라 프레임마다 메시를 다시 계산하는 컷 스크립트가 필요하다. 원리와 수치 기준은 lessons.md에 있다.
- 유리관 IOR 전환은 병이 원점에서 z축 회전·z 이동만 할 때 맞다.
- 라벨 재현은 PNG 품질에 달렸다. 이 도구는 PNG를 정확히 붙일 뿐이고, 글자 대조는 사람이 한다.
- GPU 렌더 시간은 기기마다 다르다. 첫 프레임으로 잰 예상 시간만 믿는다.
- 렌더 단계에서는 Blender 내장 numpy를 쓰고, 나머지 스크립트는 표준 라이브러리 + ffmpeg만 쓴다(numpy가 있으면 qc.py가 더 빠르다).

## 권리와 라이선스

- **글꼴:** OFL 등 상업 이용이 허용된 글꼴만. 글꼴 파일은 이 스킬에 넣지 않는다. 쓴 글꼴과 라이선스를 `sources.md`에 적는다.
- **효과음:** CC0 또는 직접 녹음·합성(own)만. `audio.py`는 다른 라이선스를 거부한다. 출처 URL을 설정 `source`와 `sources.md`에 남긴다.
- **라벨·로고:** 실제 제품 라벨 PNG는 게시물 폴더에만 두고 공개 PR에 내보낼지는 사람이 정한다. 이 스킬의 자산은 직접 만든 일반 자산뿐이다.
- **레퍼런스 영상:** 내려받지 않는다. 링크와 메모만.
- 화면에 광고 표기·구매 링크를 넣지 않는다(게시글에 쓴다). 사람·손·피부를 넣지 않는다.

## 시험

```sh
sh skills/product-cgi-render/tests/run_tests.sh                  # 단위 시험 (Blender 없이) + 오버레이(가능할 때)
BLENDER_SMOKE=1 sh skills/product-cgi-render/tests/run_tests.sh  # + 아주 작은 Blender 렌더 (270×480, 4샘플, 1프레임, nice 19)
```

Blender 시험은 Blender가 없거나 다른 Blender 프로세스가 돌고 있으면 건너뛴다. 오버레이 시험은 Node·Chrome·puppeteer-core가 없으면 건너뛴다.
