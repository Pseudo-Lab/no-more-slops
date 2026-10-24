#!/usr/bin/env python3
"""측정 가능한 영상미 QC. 결과를 표로 찍고, 하나라도 실패하면 종료 코드 1.

입력은 PNG/JPG 한 장, 프레임 폴더(f0000.png …), 영상(mp4·mov) 어느 것이든 된다. 디코드는 ffmpeg가 한다.
numpy가 있으면 쓰고, 없으면 표준 라이브러리로 계산한다(조금 느리다).

사용법:
  python3 qc.py white  <입력...> [--max 0]
      R=G=B=255 픽셀 수. 프레임별 최대, 합계. 기본 기준: 합계 0
  python3 qc.py means  <입력...> --ref <기준> [--tol 10] [--frame first|mid|last] [--ref-frame first|mid|last]
      위 띠·가운데 1/3·아래 띠 평균 RGB를 기준과 비교. 기본 기준: 채널당 차이 10 이하 (같은 세계)
  python3 qc.py loop   <영상> [--next <다음 영상, 기본 같은 영상>] [--tol 10]
      마지막 프레임 ↔ (다음 영상의) 첫 프레임 평균색 차이. 반복 재생 이음매
  python3 qc.py highlight <이미지> --roi x,y,w,h [--thresh 250] [--max-count 1] [--max-ratio 0.1]
      ROI 안 밝은 점(덩어리) 개수와 가장 큰 점 지름 / ROI 지름. 기본 기준: 점 1개 이하, 지름 1/10 이하
공통: --band 200 (1920 높이 기준 위·아래 띠 px, 해상도에 비례), --json (표 대신 JSON)
"""
import argparse
import glob
import json
import os
import subprocess
import sys

try:
    import numpy as np  # 있으면 빠르다
except ImportError:  # pragma: no cover - 환경에 따라
    np = None

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


# ───────────────────────── 디코드 ─────────────────────────
def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    dur = float(d.get("format", {}).get("duration") or 0)
    return int(s["width"]), int(s["height"]), dur


def is_image(path):
    return os.path.splitext(path)[1].lower() in IMAGE_EXT


def expand(inputs):
    """프레임 폴더는 안의 PNG/JPG를 이름순으로 펼친다."""
    out = []
    for p in inputs:
        if os.path.isdir(p):
            files = sorted(f for f in glob.glob(os.path.join(p, "*")) if is_image(f))
            if not files:
                raise SystemExit(f"{p}: 이미지가 없다")
            out.append((p, files))
        else:
            out.append((p, [p]))
    return out


def decode(path, which="all"):
    """(w, h, frame_bytes) 를 차례로 내보낸다. which = all | first | mid | last."""
    w, h, dur = probe(path)
    pre = []
    if not is_image(path):
        if which == "mid" and dur > 0:
            pre = ["-ss", f"{dur / 2:.3f}"]
        elif which == "last":
            pre = ["-sseof", "-0.5"]
    post = ["-frames:v", "1"] if which in ("first", "mid") else []
    cmd = ["ffmpeg", "-v", "error", *pre, "-i", path, *post, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    size = w * h * 3
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    last = None
    try:
        while True:
            buf = proc.stdout.read(size)
            if len(buf) < size:
                break
            if which == "last":
                last = buf
            else:
                yield w, h, buf
    finally:
        proc.stdout.close()
        proc.wait()
    if which == "last" and last is not None:
        yield w, h, last


def frames_of(files, which="all"):
    """파일 목록(프레임 폴더면 여러 장)에서 프레임을 내보낸다."""
    if len(files) == 1:
        yield from decode(files[0], which)
        return
    pick = {"all": files, "first": files[:1], "mid": files[len(files) // 2:len(files) // 2 + 1], "last": files[-1:]}[which]
    for f in pick:
        yield from decode(f, "first")


def one_frame(files, which):
    for fr in frames_of(files, which):
        return fr
    raise SystemExit(f"{files[0]}: 프레임을 읽지 못했다")


# ───────────────────────── 계산 ─────────────────────────
def white_count(buf):
    """R=G=B=255 픽셀 수."""
    if np is not None:
        a = np.frombuffer(buf, np.uint8).reshape(-1, 3)
        return int(np.all(a == 255, axis=1).sum())
    n = len(buf) // 3
    r = int.from_bytes(buf[0::3], "big")
    g = int.from_bytes(buf[1::3], "big")
    b = int.from_bytes(buf[2::3], "big")
    return (r & g & b).to_bytes(n, "big").count(255)


def region_means(w, h, buf, band=200):
    """위 띠, 가운데 1/3, 아래 띠의 평균 RGB. 띠 높이는 1920 기준 band px를 해상도에 맞춰 줄인다."""
    bh = max(1, round(band * h / 1920))
    regions = {"top": (0, bh), "mid": (h // 3, 2 * h // 3), "bottom": (h - bh, h)}
    out = {}
    for name, (y0, y1) in regions.items():
        seg = buf[y0 * w * 3:y1 * w * 3]
        n = len(seg) // 3
        if np is not None:
            a = np.frombuffer(seg, np.uint8).reshape(-1, 3)
            out[name] = [round(float(x), 1) for x in a.mean(axis=0)]
        else:
            out[name] = [round(sum(seg[c::3]) / n, 1) for c in range(3)]
    return out


def max_diff(a, b):
    return max(abs(x - y) for r in a for x, y in zip(a[r], b[r]))


def blobs(w, h, buf, roi, thresh):
    """ROI 안에서 세 채널 모두 thresh 이상인 픽셀의 연결 덩어리(4-이웃). [(픽셀 수, 지름 근사), ...] 큰 순."""
    x0, y0, rw, rh = roi
    x0, y0 = max(0, x0), max(0, y0)
    rw, rh = min(rw, w - x0), min(rh, h - y0)
    mask = bytearray(rw * rh)
    for yy in range(rh):
        row = buf[((y0 + yy) * w + x0) * 3:((y0 + yy) * w + x0 + rw) * 3]
        for xx in range(rw):
            i = xx * 3
            if row[i] >= thresh and row[i + 1] >= thresh and row[i + 2] >= thresh:
                mask[yy * rw + xx] = 1
    seen = bytearray(rw * rh)
    found = []
    for start in range(rw * rh):
        if not mask[start] or seen[start]:
            continue
        stack, n, xs, ys = [start], 0, [], []
        seen[start] = 1
        while stack:
            p = stack.pop()
            n += 1
            py, px = divmod(p, rw)
            xs.append(px)
            ys.append(py)
            for q in ((p - 1) if px > 0 else -1, (p + 1) if px < rw - 1 else -1, p - rw, p + rw):
                if 0 <= q < rw * rh and mask[q] and not seen[q]:
                    seen[q] = 1
                    stack.append(q)
        diam = max(max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
        found.append((n, diam))
    found.sort(reverse=True)
    return found


# ───────────────────────── 명령 ─────────────────────────
def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines)


def fmt(rgb):
    return "(" + ", ".join(f"{v:.0f}" for v in rgb) + ")"


def cmd_white(a):
    rows, res = [], []
    for name, files in expand(a.inputs):
        n = tot = worst = 0
        worst_i = -1
        for i, (w, h, buf) in enumerate(frames_of(files)):
            c = white_count(buf)
            n += 1
            tot += c
            if c > worst:
                worst, worst_i = c, i
        ok = tot <= a.max
        res.append({"input": name, "frames": n, "white255_total": tot, "worst_frame": worst_i, "worst_count": worst, "pass": ok})
        rows.append([name, n, tot, f"{worst} (프레임 {worst_i})" if worst else "0", "PASS" if ok else "FAIL"])
    return res, table(["입력", "프레임", "255 픽셀 합계", "최악 프레임", "판정"], rows)


def cmd_means(a):
    ref_name, ref_files = expand([a.ref])[0]
    w, h, buf = one_frame(ref_files, a.ref_frame)
    ref = region_means(w, h, buf, a.band)
    rows = [[f"기준: {ref_name} ({a.ref_frame})", fmt(ref["top"]), fmt(ref["mid"]), fmt(ref["bottom"]), "—", "—"]]
    res = []
    for name, files in expand(a.inputs):
        w, h, buf = one_frame(files, a.frame)
        m = region_means(w, h, buf, a.band)
        d = max_diff(m, ref)
        ok = d <= a.tol
        res.append({"input": name, "frame": a.frame, "means": m, "ref": ref, "max_diff": d, "pass": ok})
        rows.append([f"{name} ({a.frame})", fmt(m["top"]), fmt(m["mid"]), fmt(m["bottom"]), f"{d:.1f}", "PASS" if ok else "FAIL"])
    return res, table(["입력", "위 띠", "가운데", "아래 띠", f"최대 차이 (≤{a.tol:g})", "판정"], rows)


def cmd_loop(a):
    _, files = expand([a.video])[0]
    _, nfiles = expand([a.next or a.video])[0]
    w, h, last = one_frame(files, "last")
    w2, h2, first = one_frame(nfiles, "first")
    if (w, h) != (w2, h2):
        raise SystemExit(f"해상도가 다르다: {w}x{h} vs {w2}x{h2}")
    ml, mf = region_means(w, h, last, a.band), region_means(w, h, first, a.band)
    d = max_diff(ml, mf)
    ok = d <= a.tol
    rows = [["마지막 프레임", fmt(ml["top"]), fmt(ml["mid"]), fmt(ml["bottom"]), "", ""],
            ["첫 프레임" + (f" ({a.next})" if a.next else ""), fmt(mf["top"]), fmt(mf["mid"]), fmt(mf["bottom"]), f"{d:.1f}", "PASS" if ok else "FAIL"]]
    res = [{"input": a.video, "next": a.next or a.video, "last": ml, "first": mf, "max_diff": d, "pass": ok}]
    return res, table(["이음매", "위 띠", "가운데", "아래 띠", f"최대 차이 (≤{a.tol:g})", "판정"], rows)


def cmd_highlight(a):
    _, files = expand([a.image])[0]
    w, h, buf = one_frame(files, "first")
    roi = [int(v) for v in a.roi.split(",")]
    bl = blobs(w, h, buf, roi, a.thresh)
    big = [b for b in bl if b[0] >= a.min_px]
    roi_d = min(roi[2], roi[3])
    ratio = (big[0][1] / roi_d) if big else 0.0
    ok = len(big) <= a.max_count and ratio <= a.max_ratio
    res = [{"input": a.image, "roi": roi, "count": len(big), "largest_diam_px": big[0][1] if big else 0, "ratio": ratio, "pass": ok}]
    rows = [[a.image, a.roi, len(big), big[0][1] if big else 0, f"{ratio:.3f}", "PASS" if ok else "FAIL"]]
    return res, table(["입력", "ROI", f"밝은 점 수 (≤{a.max_count})", "가장 큰 점 지름 px", f"지름 비 (≤{a.max_ratio:g})", "판정"], rows)


def main(argv=None):
    p = argparse.ArgumentParser(description="영상미 QC (255 픽셀, 같은 세계 평균색, 루프 이음매, 하이라이트)")
    sub = p.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--band", type=int, default=200)
    common.add_argument("--json", action="store_true")
    s = sub.add_parser("white", parents=[common])
    s.add_argument("inputs", nargs="+")
    s.add_argument("--max", type=int, default=0)
    s = sub.add_parser("means", parents=[common])
    s.add_argument("inputs", nargs="+")
    s.add_argument("--ref", required=True)
    s.add_argument("--tol", type=float, default=10)
    s.add_argument("--frame", default="mid", choices=["first", "mid", "last"])
    s.add_argument("--ref-frame", default="mid", choices=["first", "mid", "last"])
    s = sub.add_parser("loop", parents=[common])
    s.add_argument("video")
    s.add_argument("--next")
    s.add_argument("--tol", type=float, default=10)
    s = sub.add_parser("highlight", parents=[common])
    s.add_argument("image")
    s.add_argument("--roi", required=True)
    s.add_argument("--thresh", type=int, default=250)
    s.add_argument("--min-px", type=int, default=4, help="이보다 작은 점은 노이즈로 보고 센다에서 뺀다")
    s.add_argument("--max-count", type=int, default=1)
    s.add_argument("--max-ratio", type=float, default=0.1)
    a = p.parse_args(argv)
    res, txt = {"white": cmd_white, "means": cmd_means, "loop": cmd_loop, "highlight": cmd_highlight}[a.cmd](a)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else txt)
    return 0 if all(r["pass"] for r in res) else 1


if __name__ == "__main__":
    sys.exit(main())
