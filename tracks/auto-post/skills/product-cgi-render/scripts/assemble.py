#!/usr/bin/env python3
"""릴스 조립: 설정의 컷 목록 순서대로 완성 컷을 이어 붙이고, 아직 없는 컷은 자리 표시 카드로 채운다.
컷이 하나씩 완성될 때마다 다시 돌리면 조립본이 완성본으로 바뀌어 간다.

사용법:
  python3 assemble.py --config project.json [--out video/assembly.mp4] [--dry-run]
                      [--size 1080x1920] [--fps 30] [--audio mix.wav]
                      [--placeholder auto|chrome|bitmap] [--allow-preview]

컷 파일: 컷의 "file" (설정 폴더 기준), 없으면 <cuts_dir>/<id>.mp4 (cuts_dir 기본 "cuts").
미리보기 화질 표시: 컷 파일 옆 <file>.render.json 의 "preview": true (compose_cut.py가 남긴다).
  미리보기 컷은 기본으로 쓰지 않고 자리 표시로 바꾼다. --allow-preview면 쓰되 화면에 PREVIEW 표시를 얹는다.
출력: mp4 (H.264 + AAC 48kHz 스테레오) + 같은 이름의 .json (컷별 상태). 자리 표시·미리보기가 하나라도 있으면 "최종 아님".
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cgi_config import Config  # noqa: E402
from pngio import Canvas  # noqa: E402

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or "",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def run(*a):
    r = subprocess.run(a, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        raise SystemExit(f"실패: {' '.join(a[:6])} …\n{r.stderr[-1500:]}")


def has_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout
    return bool(out.strip())


# ───────────────────────── 자리 표시 카드 ─────────────────────────
BG, INK, SUB = (226, 232, 240), (30, 42, 74), (110, 122, 145)


def card_bitmap(cut, idx, w, h, out):
    """외부 도구 없이 그리는 카드: 컷 번호·길이·PLACEHOLDER. 설명은 ASCII만 그린다(한글은 chrome 모드에서)."""
    c = Canvas(w, h, BG)
    s = max(2, w // 110)
    c.fill_rect(0, 0, w, max(2, h // 160), INK)
    c.fill_rect(0, h - max(2, h // 160), w, max(2, h // 160), INK)
    lines = [(f"CUT {cut['id']}", s * 2, INK), (f"{float(cut['duration']):.2f} S  #{idx + 1}", s, SUB), ("PLACEHOLDER", s, SUB)]
    raw = str(cut.get("desc", ""))
    desc = raw.strip() if raw and all(ord(ch) < 128 for ch in raw) else ""   # 비ASCII(한글 등) 설명은 그리지 않는다
    if desc:
        per = max(8, (w - 2 * s * 6) // (6 * s))
        words, cur, rows = desc.split(), "", []
        for wd in words:
            if len(cur) + len(wd) + 1 > per:
                rows.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        rows.append(cur)
        lines += [(r, s, INK) for r in rows[:4]]
    total = sum(7 * sc + sc * 6 for _, sc, _ in lines)
    y = (h - total) // 2
    for text, sc, col in lines:
        x = (w - Canvas.text_width(text, sc)) // 2
        c.text(max(s, x), y, text, sc, col)
        y += 7 * sc + sc * 6
    c.save(out)


def card_chrome(cut, idx, w, h, out, chrome):
    """Chrome 스크린샷 카드: 한글 설명까지 그린다 (시스템 글꼴)."""
    import html as H
    desc = H.escape(str(cut.get("desc", "")))
    page = f"""<!doctype html><meta charset="utf-8"><style>
*{{margin:0}}body{{width:{w}px;height:{h}px;overflow:hidden;background:rgb{BG};color:rgb{INK};
font-family:-apple-system,"Apple SD Gothic Neo","Noto Sans CJK KR","Malgun Gothic",sans-serif;display:flex;flex-direction:column;
justify-content:center;align-items:center;text-align:center;gap:{h // 60}px;border-top:{h // 160}px solid rgb{INK};border-bottom:{h // 160}px solid rgb{INK};box-sizing:border-box}}
.n{{font-size:{w // 7}px;font-weight:800}}.m{{font-size:{w // 24}px;color:rgb{SUB}}}.d{{font-size:{w // 20}px;max-width:80%;line-height:1.35}}
</style><div class="n">컷 {H.escape(str(cut['id']))}</div><div class="m">{float(cut['duration']):.2f}초 · #{idx + 1} · 자리 표시</div><div class="d">{desc}</div>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
    try:
        run(chrome, "--headless", f"--user-data-dir={tempfile.mkdtemp(prefix='chrome-')}", "--disable-gpu", "--hide-scrollbars",
            f"--window-size={w},{h}", f"--screenshot={out}", f"file://{f.name}")
    finally:
        os.unlink(f.name)


def badge_png(w, h, out, text="PREVIEW"):
    """미리보기 컷 위에 얹는 투명 PNG (오른쪽 위 띠)."""
    c = Canvas(w, h, (0, 0, 0, 0), channels=4)
    s = max(2, w // 160)
    tw = Canvas.text_width(text, s)
    x, y = w - tw - 6 * s, int(h * 0.16)
    c.fill_rect(x - 3 * s, y - 3 * s, tw + 5 * s, 13 * s, (200, 40, 40, 220))
    c.text(x, y, text, s, (255, 255, 255, 255))
    c.save(out)


# ───────────────────────── 조립 ─────────────────────────
def plan(cfg, args):
    cuts_dir = cfg.resolve(cfg.data.get("cuts_dir", "cuts"))
    rows = []
    for i, cut in enumerate(cfg.cuts):
        f = cfg.resolve(cut["file"]) if cut.get("file") else os.path.join(cuts_dir, f"{cut['id']}.mp4")
        meta_path = f + ".render.json"
        meta = {}
        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as fh:
                meta = json.load(fh)
        if not os.path.exists(f):
            state = "placeholder"
        elif meta.get("preview"):
            state = "preview" if args.allow_preview else "placeholder(preview)"
        else:
            state = "final"
        rows.append({"index": i, "id": cut["id"], "duration": float(cut["duration"]), "file": f, "state": state, "desc": cut.get("desc", "")})
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(description="컷 목록 순서대로 릴스 조립 (없는 컷은 자리 표시)")
    p.add_argument("--config", required=True)
    p.add_argument("--out")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--size")
    p.add_argument("--fps", type=int)
    p.add_argument("--audio", help="완성 믹스(wav 등)로 소리를 바꾼다 (audio.py 결과)")
    p.add_argument("--placeholder", default="auto", choices=["auto", "chrome", "bitmap"])
    p.add_argument("--allow-preview", action="store_true")
    args = p.parse_args(argv)

    cfg = Config(args.config)
    w, h = (int(v) for v in (args.size.split("x") if args.size else cfg.size))
    fps = args.fps or cfg.fps
    rows = plan(cfg, args)
    total = sum(r["duration"] for r in rows)
    final = all(r["state"] == "final" for r in rows)

    print("| # | 컷 | 길이 | 시작 | 상태 | 설명 |\n|---|---|---|---|---|---|")
    t = 0.0
    for r in rows:
        print(f"| {r['index'] + 1} | {r['id']} | {r['duration']:.2f} | {t:.2f} | {r['state']} | {r['desc']} |")
        t += r["duration"]
    print(f"합계 {total:.2f}초, 완성 컷 {sum(r['state'] == 'final' for r in rows)}/{len(rows)}" + ("" if final else " → 조립 미리보기 (최종 아님)"))
    if total > 30.0 + 1e-6:
        print("경고: 30초를 넘는다 (릴스 목표 30초 이내)")
    if args.dry_run:
        return 0

    out = cfg.resolve(args.out or cfg.data.get("assembly_out", "video/assembly-latest.mp4"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    chrome = find_chrome() if args.placeholder in ("auto", "chrome") else None
    if args.placeholder == "chrome" and not chrome:
        raise SystemExit("Chrome을 찾지 못했다 (CHROME_PATH)")
    tmp = tempfile.mkdtemp(prefix="assemble-")
    vf = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps}"
    enc = ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2"]
    parts = []
    try:
        for r in rows:
            seg = os.path.join(tmp, f"{r['index']:03d}.mp4")
            dur = f"{r['duration']:.3f}"
            if r["state"] in ("final", "preview"):
                src = r["file"]
                aud = has_audio(src)
                ins = ["-i", src] + ([] if aud else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"])
                fc = f"[0:v]{vf},tpad=stop_mode=clone:stop_duration={dur}[v0]"
                if r["state"] == "preview":
                    badge = os.path.join(tmp, "badge.png")
                    if not os.path.exists(badge):
                        badge_png(w, h, badge)
                    ins += ["-i", badge]
                    fc += f";[v0][{1 if aud else 2}:v]overlay=0:0[v]"
                else:
                    fc = fc.replace("[v0]", "[v]")
                run("ffmpeg", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "0:a" if aud else "1:a",
                    "-af", "aresample=48000,aformat=channel_layouts=stereo,apad", "-t", dur, *enc, seg)
            else:
                png = os.path.join(tmp, f"{r['index']:03d}.png")
                if chrome:
                    card_chrome(cfg.cuts[r["index"]], r["index"], w, h, png, chrome)
                else:
                    card_bitmap(cfg.cuts[r["index"]], r["index"], w, h, png)
                run("ffmpeg", "-y", "-loop", "1", "-framerate", str(fps), "-i", png, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-t", dur, "-vf", vf, *enc, seg)
            parts.append(seg)
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w") as f:
            f.writelines(f"file '{s}'\n" for s in parts)
        joined = os.path.join(tmp, "joined.mp4")
        run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, *enc, joined)
        if args.audio:
            run("ffmpeg", "-y", "-i", joined, "-i", cfg.resolve(args.audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-ar", "48000", "-ac", "2", "-af", "apad", "-t", f"{total:.3f}", "-movflags", "+faststart", out)
        else:
            run("ffmpeg", "-y", "-i", joined, "-c", "copy", "-movflags", "+faststart", out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    with open(os.path.splitext(out)[0] + ".json", "w", encoding="utf-8") as f:
        json.dump({"final": final, "duration": total, "size": [w, h], "fps": fps, "cuts": rows}, f, ensure_ascii=False, indent=1)
    print(f"→ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
