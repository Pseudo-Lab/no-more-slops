# 설정 형식

설정은 JSON 두 개다. **프로젝트 설정**(컷·룩·소리)과 **제품 프로필**(용기 모양·라벨). 상대 경로는 그 파일이 있는 폴더 기준이다. 예시는 [`../assets/example-project.json`](../assets/example-project.json)과 [`../assets/test-bottle.json`](../assets/test-bottle.json)이다.

## 프로젝트 설정

| 키 | 형식 | 기본 | 뜻 |
|---|---|---|---|
| `fps` | 정수 | 30 | |
| `size` | [w, h] | [1080, 1920] | 최종 해상도. 이보다 작게 렌더하면 미리보기로 표시된다 |
| `product` | 경로 또는 객체 | — | 제품 프로필 |
| `cuts_dir` | 경로 | `cuts` | 컷 영상 폴더. 컷 파일 = `<cuts_dir>/<id>.mp4` (컷의 `file`로 바꿀 수 있다) |
| `assembly_out` | 경로 | `video/assembly-latest.mp4` | 조립본 |
| `look` | 객체 | 아래 | 세계(룩). 생략한 값은 기본값 |
| `cuts` | 목록 | — | 콘티 순서대로 |
| `audio` | 객체 | — | 효과음 믹스 |

### 컷

| 키 | 뜻 |
|---|---|
| `id` | 컷 이름 (예 `c01`, `c22-23`). 숫자만 쓰지 않는다 |
| `duration` | 초. 조립에서 이 길이로 자르고, 짧으면 마지막 프레임을 늘린다 |
| `desc` | 한 줄 설명. 자리 표시 카드에 나온다 |
| `file` | 컷 영상 경로 (없으면 `cuts_dir/<id>.mp4`) |
| `text` | 메모용: `{"html", "start", "query"}`. 오버레이 명령에 그대로 옮긴다 |
| `blender` | 아래 |

### `blender` (render_cut.py)

| 키 | 형식 | 뜻 |
|---|---|---|
| `frames` | 정수 | 없으면 `duration × fps` |
| `fov` | 도 | 세로 화각 기본값 |
| `motion_blur` | 0~1 | 셔터. 0 또는 없음 = 끔 |
| `blur_position` | START·CENTER·END | END면 각 프레임이 직전 움직임으로 흐려진다(마지막 프레임까지 빠르게 끝나는 루프 컷) |
| `camera` | 키 목록 | `target` [x,y,z], `yaw`(0 = 정면 −y), `pitch`, `dist`, `fov`, `fstop`, `focus`(없으면 `dist`) |
| `bottle` | 키 목록 | `yaw`(도), `z` |
| `closure` | 키 목록 | `lift`(0 = 꽂힘/닫힘), `hide` |
| `bg_tint` | 키 목록 | `v` 0~1. 배경을 `look.studio.loop_mul`만큼 곱한다 (루프 이음매에서 첫 컷 배경값으로 옮겨 가기) |
| `jiggle` | 객체 | 충격 뒤 수면 큰 기포 띠 흔들림 `{"f0", "amp", "decay", "until"}` |
| `budget_min` | 분 | 첫 프레임으로 잰 예상이 넘으면 멈춤 |

키: `{"f": 프레임, 값…, "ease": "linear|in|out|inout|smooth"}`. 필드마다 그 필드가 있는 키끼리 보간하고, 구간 이징은 뒤쪽 키의 `ease`(기본 smooth). 첫 키 앞·마지막 키 뒤는 그 값을 유지한다. 리스트 값은 성분별로 보간한다.

움직임 요령 (실측):
- 꽂힘: 감속 하강으로 입구 위에서 늦춘 뒤 마지막 3~4프레임은 **가속**해 "탁" 닿게 한다. 다음 컷 첫 2~3프레임에 0.02~0.03 눌렸다 돌아오는 반동
- 회전 정지: 1~2° 지나쳤다 돌아와 박(beat) 프레임에 정확히 0°. 회전만 하면 턴테이블처럼 보인다
- 연속 두 컷의 샷 크기 차는 1.5배 이상. 같은 배경·구도에서 1.16배 차이는 점프컷으로 보였다

### `audio` (audio.py)

| 키 | 기본 | 뜻 |
|---|---|---|
| `duration` | 컷 합계 | 믹스 길이 |
| `normalize` | `loudness` | `loudness`(2패스 loudnorm) · `peak` · `none` |
| `lufs`, `true_peak` | −14, −1.5 | 목표 통합 음량, 트루 피크 상한 |
| `loop_tail` | false | 끝을 넘는 꼬리를 0초에 겹친다 |
| `sfx[]` | — | `file`, `at`(초), `gain_db`, `trim` [시작, 끝], `fade_in`, `fade_out`, `license`(CC0·own·public-domain), `source` |
| `out` | `audio/mix.wav` | |

## look (세계)

기본값은 [`../scripts/cgi_config.py`](../scripts/cgi_config.py)의 `DEFAULT_LOOK`. 모든 컷이 **같은 look**을 써야 한 세계로 보인다. 다른 제작자와 나눠 만들 때는 look을 한 파일로 두고 서로 고치지 않는다.

| 키 | 뜻 |
|---|---|
| `studio.base`, `studio.sky`, `studio.wall_glow` | 벽 아래·위 색과 발광 세기. 화면 배경 ≈ 색 × 세기 |
| `studio.floor_white`, `studio.floor_tint` | 앞 바닥 확산(그림자를 받는다) |
| `studio.softbox` | 벽의 흐린 소프트박스 하나 `{location, scale, add}` |
| `studio.loop_mul`, `loop_floor_mul` | `bg_tint` 1일 때 곱 (루프 이음매) |
| `world` | 카메라에 보이는 하늘 / 조명용 하늘 색·세기 |
| `liquid.rgb`, `liquid.ior`, `liquid.shadow_rgb` | 액체 투과색(경계면마다 곱해진다: 병 한 번 통과 ≈ rgb²), IOR, 투과 그림자 색 |
| `glass.ior`, `glass.shadow_amount` | |
| `lights.rim/front/sun/flags/back_flags` | 세로 띠 2개, 높은 앞 소프트박스, 뒤에서 오는 해, 좌우 회색 판 |
| `lights.edges` | 가장자리 장치: `az_deg`(카메라 기준 ±, 150 권장), `gap_deg`, `width`, `strength`, `bright_energy`, `radius` |
| `lights.closure_key` | 불투명 뚜껑 부품만 비추는 키 |
| `grade.white_knee`, `white_max`, `grain` | 렌더 뒤 하이라이트 어깨, Blender 단계 그레인(0이면 compose에서) |
| `render.samples`, `bounces`, `diffuse_bounces`, `denoise`, `min_final_samples`, `persistent_data` | `min_final_samples`보다 적으면 미리보기 표시. persistent data는 끈다 |
| `closure_shadow_fade` | [lo, hi]: lift가 이 사이에서 그림자가 사라진다 |

## 제품 프로필

```jsonc
{
  "name": "…",
  "bottle": {
    "outer": [[0,0], [0.52,0], …, [0.285,2.25]],   // 바깥 단면 (r, z). 바닥 축(0,0)에서 입구 끝까지, z는 늘어나는 순서
    "inner": null,                                // 직접 줄 때는 위(입구 안쪽)→아래(축 바닥) 순서. 없으면 outer에서 wall·base로 자동
    "wall": 0.03, "base": 0.04,
    "fill_level": 1.80,                           // 액체 윗면 높이. null이면 빈 병
    "threads": {"z0": 2.08, "z1": 2.18, "turns": 1.3, "r": 0.286, "thickness": 0.012}
  },
  "label": {
    "png": "label.png",                           // 투명 바탕 인쇄 글자. 이 파일 기준 경로
    "z0": 0.35, "z1": 1.60,                       // PNG 아래·위가 붙는 높이
    "arc_deg": 160,                               // 막이 덮는 각도 (정면 기준 ±80°)
    "projection": "front",                        // front = 정면 투영(정면에서 PNG 그대로), wrap = 둘레 감싸기
    "ink_rgb": [0.02, 0.02, 0.025], "use_png_color": false,
    "back_ink": 0.38,                             // 뒷면 거울 글자가 비치는 정도 (0 = 안 보임)
    "offset": 0.0015, "lens": 1.3                 // 유리면에서 띄우는 거리, 기포 피하기 계산의 원통 렌즈 배율
  },
  "closure": {
    "seat_z": 0.0,
    "parts": [{"name": "collar", "material": "matte_white", "profile": [[r, z], …]},
              {"name": "pipette", "material": "pipette", "steps": 96, "profile": […]}]
  },
  "bubbles": {"top": 30, "body": 20, "seed": 5, "r_top": [0.02, 0.06], "r_body": [0.008, 0.022], "avoid_label": true}
}
```

- 부품 재질: `matte_white`(무광 PP, 거칠기 0.58), `inner_white`(칼라 안쪽, 약한 발광: 어깨 유리 너머로 회색 기둥처럼 보이지 않게), `gloss_white`, `matte_black`, `gloss_black`, `glass`, `pipette`(액체 높이 아래·위 IOR 전환), 또는 `{"base_color", "roughness", "metallic"}`.
- 유리·`pipette` 부품은 굴절 경계면으로 만든다(법선 정리). 속이 빈 관은 바깥면 → 끝 입술 → 안쪽면을 한 단면으로 이어 유리 부피를 닫는다.
- 단위는 자유. 몸통 반지름을 사진 px로 재 비율을 맞춘다. 조명·카메라 기본값은 병 높이 약 2~3 단위에 맞춰져 있다(다르면 `lights`·카메라 거리를 함께 바꾼다).
