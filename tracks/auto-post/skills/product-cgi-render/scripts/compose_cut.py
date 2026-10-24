#!/usr/bin/env python3
"""컷 합성: 렌더 프레임(또는 영상) → 공통 마감 → cNN.mp4 + 접촉 시트.
마감 순서: 크기 맞춤 → 아래 그레이드 PNG → 글자 오버레이 프레임 → 단색 그레인 → 채널 상한 → H.264.
모든 컷(Blender·AI 영상·코드 그래픽)을 이 한 단계로 마감해야 한 세계로 보인다.

사용법:
  python3 compose_cut.py <프레임 폴더 | 영상> <out.mp4> [--fps 30] [--size 1080x1920]
         [--grade grade.png] [--overlay 오버레이폴더 --overlay-start 0.25] [--grain 6] [--cap 245]
         [--no-sheet] [--preview]
  --cap: 인코딩 전 R·G·B 상한. H.264 디코드에서 245가 255로 넘치는 일을 막는다 (글자 얹은 판은 240 권장)
  --grain: ffmpeg noise 세기 (0~100, 6 ≈ 2%)
  프레임 폴더에 render.json(render_cut.py가 남김)이 있으면 <out>.render.json으로 옮겨 적는다.
  "preview": true 인 컷은 assemble.py가 최종 조립에서 뺀다.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"실패: {' '.join(cmd[:8])} …\n{r.stderr[-1500:]}")
    return r.stdout


def frame_input(src, fps):
    """프레임 폴더면 이미지 시퀀스 입력 인자, 영상이면 그대로."""
    if not os.path.isdir(src):
        return ["-i", src]
    files = sorted(f for f in glob.glob(os.path.join(src, "*.png")))
    if not files:
        raise SystemExit(f"{src}: PNG 프레임이 없다")
    m = re.match(r"(.*?)(\d+)\.png$", os.path.basename(files[0]))
    if not m:
        raise SystemExit(f"{files[0]}: 프레임 이름은 접두어 + 번호 (예: f0000.png)")
    prefix, num = m.group(1), m.group(2)
    return ["-framerate", str(fps), "-start_number", str(int(num)), "-i", os.path.join(src, f"{prefix}%0{len(num)}d.png")]


def main(argv=None):
    p = argparse.ArgumentParser(description="컷 합성 (공통 마감)")
    p.add_argument("src")
    p.add_argument("out")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--size", default="1080x1920")
    p.add_argument("--grade")
    p.add_argument("--overlay")
    p.add_argument("--overlay-start", type=float, default=0.0)
    p.add_argument("--grain", type=float, default=0.0)
    p.add_argument("--cap", type=int, default=245)
    p.add_argument("--crf", type=int, default=16)
    p.add_argument("--no-sheet", action="store_true")
    p.add_argument("--preview", action="store_true", help="미리보기 화질로 표시 (최종 조립에서 빠진다)")
    a = p.parse_args(argv)
    w, h = (int(v) for v in a.size.split("x"))

    ins = frame_input(a.src, a.fps)
    fc = [f"[0:v]scale={w}:{h}:flags=lanczos,setsar=1,fps={a.fps},format=rgb24[b0]"]
    cur, k = "b0", 1
    if a.grade:
        ins += ["-i", a.grade]
        fc.append(f"[{k}:v]scale={w}:{h}[g];[{cur}][g]overlay=0:0:format=auto[b1]")
        cur, k = "b1", k + 1
    if a.overlay:
        ov = frame_input(a.overlay, a.fps)
        ins += ov
        fc.append(f"[{k}:v]setpts=PTS+{a.overlay_start}/TB[o];[{cur}][o]overlay=0:0:eof_action=pass:format=auto[b2]")
        cur, k = "b2", k + 1
    tail = "format=rgb24"
    if a.grain > 0:
        tail += f",noise=c0s={a.grain:g}:c1s={a.grain:g}:c2s={a.grain:g}:c0f=t+u:c1f=t+u:c2f=t+u:all_seed=7"
    if a.cap < 255:
        tail += f",lutrgb=r='min(val,{a.cap})':g='min(val,{a.cap})':b='min(val,{a.cap})'"
    fc.append(f"[{cur}]{tail},format=yuv420p[v]")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "libx264", "-profile:v", "high",
         "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-r", str(a.fps), "-movflags", "+faststart", a.out])
    n = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", a.out]).strip()
    if not a.no_sheet:
        sheet = os.path.splitext(a.out)[0] + "-sheet.png"
        run(["ffmpeg", "-y", "-v", "error", "-i", a.out, "-vf", f"select='not(mod(n\\,5))',scale={w // 5}:{h // 5},tile=8x2:padding=4:color=white",
             "-frames:v", "1", sheet])
    meta = {}
    src_meta = os.path.join(a.src, "render.json") if os.path.isdir(a.src) else a.src + ".render.json"
    if os.path.exists(src_meta):
        with open(src_meta, encoding="utf-8") as f:
            meta = json.load(f)
    meta["preview"] = bool(meta.get("preview")) or a.preview
    meta["compose"] = {"size": [w, h], "fps": a.fps, "grade": bool(a.grade), "overlay": bool(a.overlay), "grain": a.grain, "cap": a.cap, "frames": int(n or 0)}
    with open(a.out + ".render.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(f"{a.out}: {n}프레임" + (" (미리보기 화질 — 최종 조립에서 빠짐)" if meta["preview"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
