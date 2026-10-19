# 컷 렌더 (Blender headless): 설정의 컷 하나를 scene.py 장면으로 만들고, 컷의 "blender" 키프레임대로 움직여 프레임을 뽑는다.
# 컷마다 스크립트를 새로 쓰지 않고 설정만 바꾸는 패턴이다. 키로 표현이 안 되는 움직임(액체 모양 변형 등)은
# 이 파일을 본떠 컷 스크립트를 따로 쓰고 scene.Stage를 import 한다.
#
# 사용법:
#   nice -n 19 blender -b --factory-startup -P scripts/render_cut.py -- --config project.json --cut c03 --out frames/c03
#        [--samples 64] [--size 1080x1920] [--frames 0-29 | 0,15,29] [--device AUTO|METAL|OPTIX|CUDA|HIP|CPU]
#        [--preview] [--over-budget-ok]
# 출력: <out>/f0000.png … (보정본), <out>/raw/ (보정 전), <out>/render.json (샘플·크기·미리보기 여부·시간)
#
# 컷 설정 "blender" (모든 키 선택. 키 목록은 {"f": 프레임, 값…, "ease": "linear|in|out|inout|smooth"}):
#   frames        프레임 수 (없으면 duration × fps)
#   fov           카메라 세로 화각(도), 키 "fov"로 바꿀 수 있다
#   motion_blur   셔터(프레임 비율, 0이면 끔), blur_position: START|CENTER|END
#   camera        키: target [x,y,z], yaw(0 = 정면), pitch, dist, fov, fstop, focus(없으면 dist)
#   bottle        키: yaw(도), z
#   closure       키: lift(0 = 꽂힘/닫힘), hide(true면 렌더에서 숨김)
#   bg_tint       키: v (0~1, 루프 이음매 배경 곱. look.studio.loop_mul)
#   jiggle        {"f0": 충격 프레임, "amp": 0.012, "decay": 4, "until": 12} 수면 큰 기포 띠 흔들림
#   budget_min    예산(분). 첫 프레임으로 잰 예상 시간이 넘으면 멈춘다 (--over-budget-ok로 무시)
import argparse
import json
import math
import os
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene as S  # noqa: E402
from cgi_config import Config, cut_frames, interp, parse_frames  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(prog="render_cut.py")
ap.add_argument("--config", required=True)
ap.add_argument("--cut", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--samples", type=int)
ap.add_argument("--size")
ap.add_argument("--frames", default="")
ap.add_argument("--device", default="AUTO")
ap.add_argument("--preview", action="store_true")
ap.add_argument("--over-budget-ok", action="store_true")
a = ap.parse_args(argv)

cfg = Config(a.config)
cut = cfg.cut(a.cut)
B = cut.get("blender") or {}
N = cut_frames(cut, cfg.fps)
size = tuple(int(v) for v in a.size.split("x")) if a.size else tuple(cfg.size)
samples = a.samples or cfg.look["render"]["samples"]
preview = bool(a.preview or samples < cfg.look["render"]["min_final_samples"] or size[0] < cfg.size[0] or size[1] < cfg.size[1])

st = S.Stage(cfg).build(B.get("fov", 26))
device = st.render_setup(samples, size, a.device)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 0, N - 1
if B.get("motion_blur"):
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = float(B["motion_blur"])
    sc.render.motion_blur_position = B.get("blur_position", "CENTER")

cyc = bpy.data.materials["cyc"].node_tree.nodes
bg_nodes = [cyc["BG_TINT"], cyc["BG_TINT_FLOOR"]]
height = max(z for _, z in cfg.product["bottle"]["outer"])
top_bubbles = [o for o in st.bottle.children if o.name.startswith("bubble_top")]
jig = B.get("jiggle")

# ── 매 프레임 키: 직선 보간으로 넣어 모션 블러가 앞뒤 프레임을 정확히 본다 ──
for f in range(N):
    st.bottle.rotation_euler.z = math.radians(interp(B.get("bottle"), f, "yaw", 0.0))
    st.set_bottle_z(interp(B.get("bottle"), f, "z", 0.0))
    st.bottle.keyframe_insert("rotation_euler", index=2, frame=f)
    st.bottle.keyframe_insert("location", index=2, frame=f)
    for n in st.pipette_level_nodes:
        n.inputs[1].keyframe_insert("default_value", frame=f)
    if st.closure:
        st.set_lift(interp(B.get("closure"), f, "lift", 0.0))
        st.closure.keyframe_insert("location", index=2, frame=f)
        hide = bool(interp(B.get("closure"), f, "hide", False))
        for o in st.closure.children:
            o.keyframe_insert('["sfade"]', frame=f)
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=f)
    v = interp(B.get("bg_tint"), f, "v", 0.0)
    for nd in bg_nodes:
        S.sock(nd.inputs, "Factor").default_value = v
        S.sock(nd.inputs, "Factor").keyframe_insert("default_value", frame=f)
    if jig:
        k = f - jig.get("f0", 0)
        for i, o in enumerate(top_bubbles):
            d = jig.get("amp", 0.012) * math.exp(-k / jig.get("decay", 4.0)) * math.sin(k * 1.9 + i * 1.3) if 0 <= k <= jig.get("until", 12) else 0.0
            o.location.z = o["z0"] + d
            o.keyframe_insert("location", index=2, frame=f)
    ck = B.get("camera") or [{"f": 0}]
    tgt = interp(ck, f, "target", [0, 0, height * 0.6])
    dist = interp(ck, f, "dist", 12.0)
    st.aim(tgt, interp(ck, f, "yaw", 0.0), interp(ck, f, "pitch", 8.0), dist, interp(ck, f, "focus", None))
    st.cam.data.angle = math.radians(interp(ck, f, "fov", B.get("fov", 26)))
    st.cam.data.dof.aperture_fstop = interp(ck, f, "fstop", 8.0)
    st.cam.keyframe_insert("location", frame=f)
    st.cam.keyframe_insert("rotation_euler", frame=f)
    st.cam.data.dof.keyframe_insert("focus_distance", frame=f)
    st.cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
    st.cam.data.keyframe_insert("lens", frame=f)   # 화각(angle)은 lens로 저장된다
    st.edge_rig.keyframe_insert("rotation_euler", index=2, frame=f)
for o in [st.bottle, st.cam, st.cam.data, st.edge_rig] + top_bubbles + ([st.closure] + list(st.closure.children) if st.closure else []):
    S.linear_keys(o)

# ── 렌더 ──
frames = parse_frames(a.frames, N)
os.makedirs(os.path.join(a.out, "raw"), exist_ok=True)
t0 = time.time()
budget = B.get("budget_min")
for i, f in enumerate(frames):
    sc.frame_set(f)
    S.render_still(os.path.join(a.out, f"f{f:04d}.png"), cfg.look["grade"], seed=1000 + f)
    el = time.time() - t0
    print(f"FRAME {a.cut} {f} {el:.1f}s", flush=True)
    if i == 0 and len(frames) > 1:
        est = el * len(frames) / 60
        print(f"예상 {est:.1f}분 ({len(frames)}프레임, 프레임당 {el:.1f}초)" + (f", 예산 {budget}분" if budget else ""), flush=True)
        if budget and est > budget and not a.over_budget_ok:
            print("예산 초과: 멈춘다. 샘플·크기·프레임 수를 줄이거나 --over-budget-ok", flush=True)
            break
done = [f for f in frames if os.path.exists(os.path.join(a.out, f"f{f:04d}.png"))]
complete = len(done) == N
meta = {"cut": a.cut, "frames_total": N, "frames_rendered": done, "complete": complete, "samples": samples, "size": list(size), "device": device,
        "preview": preview or not complete, "seconds": round(time.time() - t0, 1), "blender": bpy.app.version_string,
        "config": os.path.relpath(cfg.path, os.path.abspath(a.out))}
with open(os.path.join(a.out, "render.json"), "w", encoding="utf-8") as fh:
    json.dump(meta, fh, ensure_ascii=False, indent=1)
print(f"RENDER_DONE {a.cut} samples={samples} size={size[0]}x{size[1]} preview={meta['preview']} seconds={meta['seconds']}")
