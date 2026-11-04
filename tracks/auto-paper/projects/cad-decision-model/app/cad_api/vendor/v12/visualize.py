# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.24", "opencv-python-headless>=4.8"]
# ///
"""출력 JSON(objects + relations)을 도면 위에 그린다.

입력 형식 (docs/PLAN.md §6):
    {"image": {"file": "page-016.png", "path"?: "image/page-016.png", ...},
     "objects": [{"id", "class", "bbox", "confidence"?, "class_confidence"?}],
     "relations": [{"id", "type", "a", "a_side", "b", "b_side", "a_point"?, "b_point"?, "path"?, "net"?, "confidence"?}]}
    a_point/b_point 는 선이 박스에 닿는 실제 좌표 [x, y], path 는 선을 따라간 꺾은선 [[x, y], ...] (둘 다 선택).
    path 가 있으면 실제 배선 경로를 그리고, 없으면 두 박스를 직선으로 잇는다. 같은 net 은 같은 색.
정답 파일은 두 형식 모두 된다: experiments/gt_p0.json ("symbols" 목록, 여러 페이지),
experiments/gt_page-016.json (한 페이지의 "objects" + "relations"). 정답에 relations 가 있으면 연결도 채점한다.
같은 폴더에 <이름>_trace.json 이 있으면 시작 박스, 영역 판정(S1), 제외된 후보(S2)도 레이어로 보여 준다.
class 가 "text" 인 객체는 텍스트 박스(보라)로 따로 그리고, type 이 "inside" 인 관계(심볼 안 글자)는 선으로 그리지 않고 목록에만 보인다.

만드는 파일 (출력 JSON 옆, 또는 --out 폴더):
    <이름>.html          확대·이동되는 뷰어 (브라우저로 열기, 인터넷 불필요)
    <이름>_overlay.png   페이지 전체에 박스·관계를 그린 이미지
    <이름>_objects.png   객체마다 잘라서 모은 이미지 (정답 박스가 있으면 함께 표시)

실행 (cad-jev 루트에서):
    uv run experiments/visualize.py experiments/example_output_page-016.json --gt experiments/gt_p0.json
    uv run experiments/visualize.py experiments/gt_page-016.json        # 정답만 확인
    uv run experiments/visualize.py runs/page/<폴더>/                    # 폴더 안의 *_output.json 전부
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# BGR for OpenCV, hex for HTML
C_OUT, H_OUT = (208, 91, 29), "#1d5bd0"      # 출력 박스: 파랑
C_GT, H_GT = (60, 150, 20), "#14963c"        # 정답 박스: 초록
C_START, H_START = (150, 150, 150), "#969696"  # 시작 박스: 회색
C_REL, H_REL = (0, 120, 235), "#eb7800"      # 관계(net 정보가 없을 때): 주황
C_BAD, H_BAD = (40, 40, 220), "#dc2828"      # 틀린/놓친 연결, 제외된 후보: 빨강
H_REGION = "#7b3fbf"
C_TXT, H_TXT = (190, 40, 150), "#9628be"     # 텍스트 박스: 보라
C_WIN, H_WIN = (90, 90, 90), "#5a5a5a"       # 정답이 있는 구역(부분 정답): 진회색
NET_HEX = ["#eb7800", "#0b8f3c", "#1d5bd0", "#c21fc2", "#9a6a00", "#6b3fc8", "#008c8c", "#e0569b", "#5f6b00", "#3a9ad9",
           "#8b4513", "#555555", "#b8860b", "#7b68ee", "#2e7d32", "#d2691e"]   # 빨강은 틀린 연결 표시용이라 뺐다


def hex_bgr(h):
    return int(h[5:7], 16), int(h[3:5], 16), int(h[1:3], 16)


def net_hex(r):
    n = str(r.get("net") or "")
    digits = "".join(ch for ch in n if ch.isdigit())
    return NET_HEX[(int(digits) - 1) % len(NET_HEX)] if digits else H_REL


def is_text(o):
    return o.get("class") == "text"


def short_class(c):
    return (c or "-").split("/")[-1]


# ----------------------------------------------------------------------------- loading

def iou(a, b):
    ix0, iy0, ix1, iy1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    area = lambda r: (r[2] - r[0] + 1) * (r[3] - r[1] + 1)  # noqa: E731
    return inter / float(area(a) + area(b) - inter)


def load_outputs(path: Path) -> list[dict]:
    """Return a list of per-page outputs in the §6 format. Accepts §6 files, gt_p0.json, or a folder."""
    if path.is_dir():
        files = sorted(path.glob("*_output.json"))
        return [dict(json.loads(f.read_text()), _path=f) for f in files]
    data = json.loads(path.read_text())
    if "symbols" in data:  # multi-page ground-truth file -> one output per page
        pages = {}
        for s in data["symbols"]:
            pages.setdefault(s["page"], []).append({"id": s["id"], "class": s["class"], "bbox": s["bbox"]})
        return [{"image": {"file": p}, "objects": objs, "relations": [], "_path": path.with_name(f"{path.stem}_{Path(p).stem}.json")}
                for p, objs in sorted(pages.items())]
    return [dict(data, _path=path)]


def _gt_pages(path: Path | None):
    """-> (objects by page, relations by page, window by page). A window means the GT covers only that part of the page."""
    if not path:
        return {}, {}, {}
    data = json.loads(Path(path).read_text())
    objs, rels, wins = {}, {}, {}
    if "symbols" in data:
        for s in data["symbols"]:
            objs.setdefault(s["page"], []).append(s)
    elif "objects" in data:
        image = data["image"]
        page = Path(image["file"] if isinstance(image, dict) else image).name
        objs[page] = data["objects"]
        rels[page] = data.get("relations", [])
        if data.get("window"):
            wins[page] = data["window"]
        elif len(data.get("windows", [])) == 1:
            wins[page] = data["windows"][0]["bbox"]
    return objs, rels, wins


def load_gt(path: Path | None) -> dict:
    return _gt_pages(path)[0]


def load_gt_relations(path: Path | None) -> dict:
    return _gt_pages(path)[1]


def in_window(b, w):
    if not w:
        return True
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return w[0] <= cx <= w[2] and w[1] <= cy <= w[3]


def closure_pairs(rels, transparent=(), per_net=True):
    """Pairs implied by 'connected' relations. per_net: within one net, every two symbols linked through relations of that
    net (a big P&ID net lists only spanning-tree pairs); relations without a net count as they are. transparent: objects
    that do not count as symbols (an output matching an optional GT mark such as a flange tick): two symbols joined
    through them are joined. -> sorted [(a, b)] without transparent objects."""
    rels = [r for r in rels if r.get("type", "connected") == "connected"]
    out = set()
    if per_net:
        by_net = {}
        for r in rels:
            if r.get("net") is None:
                out.add(tuple(sorted((r["a"], r["b"]))))
            else:
                by_net.setdefault(r["net"], []).append((r["a"], r["b"]))
        for prs in by_net.values():
            parent = {}

            def find(x):
                parent.setdefault(x, x)
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            for a, b in prs:
                parent[find(a)] = find(b)
            groups = {}
            for x in list(parent):
                groups.setdefault(find(x), []).append(x)
            for g in groups.values():
                g.sort()
                out.update((g[i], g[j]) for i in range(len(g)) for j in range(i + 1, len(g)))
    else:
        out = {tuple(sorted((r["a"], r["b"]))) for r in rels}
    transparent = set(transparent)
    if transparent:
        adj = {}
        for a, b in out:
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
        seen = set()
        for t in transparent:
            if t in seen or t not in adj:
                continue
            comp, stack = set(), [t]
            while stack:
                u = stack.pop()
                if u not in comp:
                    comp.add(u)
                    stack.extend(v for v in adj.get(u, ()) if v in transparent)
            seen |= comp
            ends = sorted({v for u in comp for v in adj.get(u, ()) if v not in transparent})
            out.update((ends[i], ends[j]) for i in range(len(ends)) for j in range(i + 1, len(ends)))
        out = {pq for pq in out if pq[0] not in transparent and pq[1] not in transparent}
    return sorted(out)


def match_gt(objects, gts):
    """id가 같으면 그대로, 아니면 IoU가 가장 큰 정답 박스와 짝짓는다 (탐욕적)."""
    by_id = {g["id"]: g for g in gts}
    used, pairs = set(), {}
    for o in objects:
        if o["id"] in by_id:
            pairs[o["id"]] = by_id[o["id"]]
            used.add(o["id"])
    rest = sorted(((iou(o["bbox"], g["bbox"]), o["id"], g["id"]) for o in objects if o["id"] not in pairs
                   for g in gts if g["id"] not in used and is_text(o) == is_text(g)), reverse=True)
    for v, oid, gid in rest:
        if v > 0.1 and oid not in pairs and gid not in used:
            pairs[oid] = by_id[gid]
            used.add(gid)
    return pairs


def check_relations(out, pairs, gt_rels, window=None, closure=False):
    """출력 관계마다 정답에 있는지(True/False), 그리고 정답 중 놓친 관계 목록.
    window: 정답이 있는 구역 (두 끝이 모두 구역 안인 관계만 판정), closure: 같은 net 안에서 이어지는 쌍은 찾은 것으로 본다.
    정답의 '선택' 객체와 짝지어진 출력은 거쳐 가는 점으로 본다 (그것을 사이에 둔 두 심볼은 이어진 것)."""
    if not gt_rels:
        return {}, []
    gset = {(r.get("type", "connected"), frozenset((r["a"], r["b"]))): r for r in gt_rels}
    objs = {o["id"]: o for o in out["objects"]}
    judged = [r for r in out.get("relations", [])
              if all(objs.get(r.get(k)) and in_window(objs[r[k]]["bbox"], window) for k in ("a", "b"))]
    status, found = {}, set()

    def key_of(typ, a, b):
        ga, gb = pairs.get(a), pairs.get(b)
        return (typ, frozenset((ga["id"], gb["id"]))) if ga and gb else None
    for r in judged:
        key = key_of(r.get("type", "connected"), r.get("a"), r.get("b"))
        status[r.get("id")] = key in gset
        if key in gset:
            found.add(key)
    transparent = {o for o, g in pairs.items() if g.get("optional")}
    if closure or transparent:
        for a, b in closure_pairs([r for r in judged if r.get("type", "connected") == "connected"], transparent, per_net=closure):
            key = key_of("connected", a, b)
            if key in gset:
                found.add(key)
    missed = [r for k, r in gset.items() if k not in found]
    return status, missed


def side_point(b, side):
    x0, y0, x1, y1 = b
    return {"left": (x0, (y0 + y1) / 2), "right": (x1, (y0 + y1) / 2),
            "top": ((x0 + x1) / 2, y0), "bottom": ((x0 + x1) / 2, y1)}.get(side, ((x0 + x1) / 2, (y0 + y1) / 2))


def rel_points(r, a, b):
    """관계의 두 끝점. a_point/b_point(선이 닿는 실제 위치)가 있으면 그것을 쓰고,
    없으면 두 박스가 겹치는 높이(좌우 연결) 또는 폭(상하 연결)의 가운데를 쓴다."""
    p, q = side_point(a, r.get("a_side")), side_point(b, r.get("b_side"))
    if r.get("a_side") in ("left", "right") and r.get("b_side") in ("left", "right"):
        lo, hi = max(a[1], b[1]), min(a[3], b[3])
        if lo <= hi:
            p, q = (p[0], (lo + hi) / 2), (q[0], (lo + hi) / 2)
    elif r.get("a_side") in ("top", "bottom") and r.get("b_side") in ("top", "bottom"):
        lo, hi = max(a[0], b[0]), min(a[2], b[2])
        if lo <= hi:
            p, q = ((lo + hi) / 2, p[1]), ((lo + hi) / 2, q[1])
    return tuple(r.get("a_point") or p), tuple(r.get("b_point") or q)


def rel_polyline(r, a, b):
    """관계를 그릴 꺾은선: path 가 있으면 그것, 없으면 두 끝점을 잇는 직선."""
    if r.get("path") and len(r["path"]) >= 2:
        return [tuple(p) for p in r["path"]]
    return list(rel_points(r, a, b))


def load_trace(src: Path, starts_path=None) -> dict:
    for tp in [starts_path, src.with_name(src.name[: -len("_output.json")] + "_trace.json") if src.name.endswith("_output.json") else None]:
        if tp and Path(tp).exists():
            return json.loads(Path(tp).read_text())
    return {}


# ----------------------------------------------------------------------------- PNG renderers

def dashed_rect(img, b, color, t=2, dash=10):
    x0, y0, x1, y1 = [int(v) for v in b]
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        n = max(int(np.hypot(bx - ax, by - ay) / dash), 1)
        for i in range(0, n, 2):
            p = (int(ax + (bx - ax) * i / n), int(ay + (by - ay) * i / n))
            q = (int(ax + (bx - ax) * min(i + 1, n) / n), int(ay + (by - ay) * min(i + 1, n) / n))
            cv2.line(img, p, q, color, t)


def dashed_poly(img, pts, color, t=3, dash=12):
    for p, q in zip(pts, pts[1:]):
        n = max(int(np.hypot(q[0] - p[0], q[1] - p[1]) / dash), 1)
        for i in range(0, n, 2):
            a = (int(p[0] + (q[0] - p[0]) * i / n), int(p[1] + (q[1] - p[1]) * i / n))
            b = (int(p[0] + (q[0] - p[0]) * min(i + 1, n) / n), int(p[1] + (q[1] - p[1]) * min(i + 1, n) / n))
            cv2.line(img, a, b, color, t)


def put_label(img, text, xy, color, scale=0.8, t=2):
    cv2.putText(img, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), t + 3, cv2.LINE_AA)
    cv2.putText(img, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, t, cv2.LINE_AA)


def drawing_scale(out):
    """Letter height of the sheet relative to the logic sheets (18 px): line widths and labels follow it."""
    return ((out.get("meta") or {}).get("text_height") or 18) / 18.0


def render_overlay(page, out, pairs, starts, status=None, missed=(), gt_by_id=None, window=None):
    img = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
    s = drawing_scale(out)
    T = lambda v, lo=1: max(lo, int(round(v * s)))  # noqa: E731
    F = lambda v: max(0.3, v * s)  # noqa: E731
    lt = 2 if s >= 0.75 else 1
    if window:
        dashed_rect(img, (window[0] - 6, window[1] - 6, window[2] + 6, window[3] + 6), C_WIN, 3, 16)
        put_label(img, "GT window", (int(window[0]), max(int(window[1]) - 14, 24)), C_WIN, 0.9)
    objs = {o["id"]: o for o in out["objects"]}
    for r in out.get("relations", []):
        a, b = objs.get(r.get("a")), objs.get(r.get("b"))
        if not a or not b or r.get("type") == "inside":
            continue
        pts = np.array([tuple(int(v) for v in p) for p in rel_polyline(r, a["bbox"], b["bbox"])], np.int32).reshape(-1, 1, 2)
        color = hex_bgr(net_hex(r)) if (status or {}).get(r.get("id"), True) else C_BAD
        cv2.polylines(img, [pts], False, color, T(5, 2), cv2.LINE_AA)
        if r.get("directed"):
            p, q = tuple(pts[-2][0]), tuple(pts[-1][0])
            cv2.arrowedLine(img, p, q, color, T(5, 2), tipLength=min(0.5, 30 / max(1, np.hypot(q[0] - p[0], q[1] - p[1]))))
    for r in missed or ():
        ga, gb = (gt_by_id or {}).get(r["a"]), (gt_by_id or {}).get(r["b"])
        if ga and gb and r.get("type", "connected") == "connected":
            dashed_poly(img, list(rel_points(r, ga["bbox"], gb["bbox"])), C_BAD, T(4, 2), T(12, 6))
    for o in out["objects"]:
        if is_text(o):
            b = o["bbox"]
            g = pairs.get(o["id"])
            if g:
                p4 = T(4)
                dashed_rect(img, (g["bbox"][0] - p4, g["bbox"][1] - p4, g["bbox"][2] + p4, g["bbox"][3] + p4), C_GT, 1, T(6, 3))
            p2 = T(2)
            cv2.rectangle(img, (int(b[0]) - p2, int(b[1]) - p2), (int(b[2]) + p2, int(b[3]) + p2), C_TXT, T(2))
            put_label(img, o["id"], (int(b[0]), int(b[3]) + T(22)), C_TXT, F(0.55), lt)
            continue
        g = pairs.get(o["id"])
        if g:
            p3 = T(3)
            dashed_rect(img, (g["bbox"][0] - p3, g["bbox"][1] - p3, g["bbox"][2] + p3, g["bbox"][3] + p3), C_GT, T(2), T(10, 5))
        if o["id"] in starts:
            dashed_rect(img, starts[o["id"]], C_START, 1, T(6, 3))
        b = o["bbox"]
        cv2.rectangle(img, (int(b[0]) - 1, int(b[1]) - 1), (int(b[2]) + 1, int(b[3]) + 1), C_OUT, T(3))
        label = o["id"] + (f" {short_class(o.get('class'))}" if o.get("class") else "")
        put_label(img, label, (int(b[0]), max(int(b[1]) - T(10), 20)), C_OUT, F(0.7), lt)
    return img


def render_montage(page, out, pairs, starts, cols=5, tile=300):
    tiles = []
    for o in [o for o in out["objects"] if not is_text(o)]:
        boxes = [o["bbox"]] + ([pairs[o["id"]]["bbox"]] if o["id"] in pairs else []) + ([starts[o["id"]]] if o["id"] in starts else [])
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        m = int(max(14, 0.3 * max(x1 - x0, y1 - y0)))
        cx0, cy0 = max(int(x0) - m, 0), max(int(y0) - m, 0)
        cx1, cy1 = min(int(x1) + m, page.shape[1] - 1), min(int(y1) + m, page.shape[0] - 1)
        crop = cv2.cvtColor(page[cy0:cy1 + 1, cx0:cx1 + 1], cv2.COLOR_GRAY2BGR)
        s = min((tile - 10) / crop.shape[1], (tile - 58) / crop.shape[0], 6.0)
        crop = cv2.resize(crop, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_NEAREST)
        P = lambda x, y: (int((x - cx0) * s), int((y - cy0) * s))  # noqa: E731

        def rect(b, color, t, pad=0.5):
            cv2.rectangle(crop, P(b[0] - pad, b[1] - pad), P(b[2] + pad, b[3] + pad), color, t)
        if o["id"] in starts:
            rect(starts[o["id"]], C_START, 1)
        if o["id"] in pairs:
            rect(pairs[o["id"]]["bbox"], C_GT, 2, 1.5)
        rect(o["bbox"], C_OUT, 2)
        t = np.full((tile, tile, 3), 255, np.uint8)
        t[52:52 + crop.shape[0], 5:5 + crop.shape[1]] = crop
        label = o["id"] + (f"  IoU {iou(o['bbox'], pairs[o['id']]['bbox']):.2f}" if o["id"] in pairs else "")
        cv2.putText(t, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if o.get("class") or o["id"] in pairs:
            cls = short_class(o.get("class"))
            if o["id"] in pairs and o.get("class") and pairs[o["id"]].get("class") and pairs[o["id"]]["class"] != o["class"]:
                cls += f" (GT {short_class(pairs[o['id']]['class'])})"
            cv2.putText(t, cls, (5, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (90, 60, 20), 1, cv2.LINE_AA)
        cv2.rectangle(t, (0, 0), (tile - 1, tile - 1), (205, 205, 205), 1)
        tiles.append(t)
    if not tiles:
        return np.full((60, 400, 3), 255, np.uint8)
    rows = []
    for i in range(0, len(tiles), cols):
        row = tiles[i:i + cols] + [np.full((tile, tile, 3), 255, np.uint8)] * (cols - len(tiles[i:i + cols]))
        rows.append(np.concatenate(row, axis=1))
    return np.concatenate(rows, axis=0)


# ----------------------------------------------------------------------------- HTML viewer

VIEWER_CSS = """
:root { --bg:#f3f4f6; --panel:#ffffff; --ink:#16191d; --ink2:#5b636d; --rule:#d7dbe0; --out:%(out)s; --gt:%(gt)s; --start:%(start)s; --rel:%(rel)s; --bad:%(bad)s; --region:%(region)s; --txt:%(txt)s; --win:%(win)s; }
* { box-sizing:border-box; }
html, body { height:100%%; margin:0; }
body { background:var(--bg); color:var(--ink); font:14px/1.5 -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif; display:grid; grid-template-rows:auto 1fr; }
header { display:flex; flex-wrap:wrap; gap:8px 18px; align-items:center; padding:10px 16px; background:var(--panel); border-bottom:1px solid var(--rule); }
header h1 { font-size:15px; margin:0; font-weight:650; }
header .stats { color:var(--ink2); font-size:13px; }
header label { display:inline-flex; gap:6px; align-items:center; font-size:13px; cursor:pointer; user-select:none; }
.sw { width:18px; height:0; border-top:3px solid; display:inline-block; }
header button { font:inherit; font-size:13px; padding:3px 10px; border:1px solid var(--rule); background:#fff; border-radius:5px; cursor:pointer; }
main { display:grid; grid-template-columns:minmax(0,1fr) 400px; min-height:0; }
#viewport { position:relative; overflow:hidden; cursor:grab; background:#e5e7eb; }
#viewport.drag { cursor:grabbing; }
#stage { position:absolute; left:0; top:0; transform-origin:0 0; }
#stage img { display:block; user-select:none; -webkit-user-drag:none; }
#stage svg { position:absolute; left:0; top:0; overflow:visible; }
.box-out { fill:transparent; stroke:var(--out); stroke-width:2.5; vector-effect:non-scaling-stroke; cursor:pointer; }
.box-out:hover, .box-out.sel { stroke-width:5; fill:rgba(29,91,208,.08); }
.box-gt { fill:none; stroke:var(--gt); stroke-width:2; stroke-dasharray:7 5; vector-effect:non-scaling-stroke; pointer-events:none; }
.box-start { fill:none; stroke:var(--start); stroke-width:1.5; stroke-dasharray:2 4; vector-effect:non-scaling-stroke; pointer-events:none; }
.box-rej { fill:transparent; stroke:var(--bad); stroke-width:1.8; stroke-dasharray:3 4; vector-effect:non-scaling-stroke; }
.box-region { fill:none; stroke:var(--region); stroke-width:2; stroke-dasharray:10 6; vector-effect:non-scaling-stroke; pointer-events:none; }
.box-txt { fill:transparent; stroke:var(--txt); stroke-width:1.8; vector-effect:non-scaling-stroke; cursor:pointer; }
.box-txt:hover, .box-txt.sel { stroke-width:4; fill:rgba(150,40,190,.08); }
.lbl-txt { fill:var(--txt); }
.box-win { fill:none; stroke:var(--win); stroke-width:2.5; stroke-dasharray:14 8; vector-effect:non-scaling-stroke; pointer-events:none; }
.lbl-win { fill:var(--win); }
.rel { stroke-width:3.5; vector-effect:non-scaling-stroke; fill:none; cursor:pointer; stroke-linejoin:round; opacity:.9; }
.rel:hover, .rel.sel { stroke-width:7; opacity:1; }
.rel.bad { stroke-dasharray:8 5; }
.rel-miss { stroke:var(--bad); stroke-width:3; stroke-dasharray:4 5; vector-effect:non-scaling-stroke; fill:none; }
.lbl { font-size:calc(var(--lbl, 14) * 1px); font-weight:700; paint-order:stroke; stroke:#fff; stroke-width:calc(var(--lbl, 14) * 0.25px); pointer-events:none; }
.lbl-out { fill:var(--out); } .lbl-region { fill:var(--region); }
aside { background:var(--panel); border-left:1px solid var(--rule); overflow:auto; padding:12px 14px; display:grid; align-content:start; gap:10px; }
aside h2 { font-size:13px; margin:6px 0 0; color:var(--ink2); font-weight:650; letter-spacing:.02em; }
table { border-collapse:collapse; width:100%%; font-size:12.5px; }
td, th { padding:5px 6px; border-bottom:1px solid var(--rule); text-align:left; vertical-align:top; }
th { color:var(--ink2); font-weight:600; font-size:12px; }
tr.row { cursor:pointer; } tr.row:hover, tr.row.sel { background:#eef3ff; }
td.num { font-variant-numeric:tabular-nums; text-align:right; white-space:nowrap; }
td.cls { word-break:break-word; font-size:12px; color:var(--ink2); }
.dot { display:inline-block; width:10px; height:10px; border-radius:50%%; vertical-align:-1px; margin-right:4px; }
.mono { font-family:ui-monospace, Menlo, monospace; font-size:12px; }
.good { color:#0c8048; font-weight:600; } .mid { color:#a86200; font-weight:600; } .bad { color:#c62a1f; font-weight:600; }
#tip { position:fixed; pointer-events:none; background:#16191d; color:#fff; font-size:12px; line-height:1.45; padding:7px 9px; border-radius:6px; max-width:360px; display:none; z-index:10; white-space:pre-line; }
.note { font-size:12.5px; color:var(--ink2); margin:0; }
@media (max-width: 800px) { main { grid-template-columns:1fr; grid-template-rows:60vh auto; } aside { border-left:0; border-top:1px solid var(--rule); } }
"""

VIEWER_JS = r"""
const W = DATA.width, H = DATA.height;
const vp = document.getElementById('viewport'), stage = document.getElementById('stage');
let s = 1, tx = 0, ty = 0;
function apply() {
  stage.style.transform = `translate(${tx}px,${ty}px) scale(${s})`;
  stage.style.setProperty('--lbl', String(Math.min(40, 14 / s)));   // labels stay about 14 screen px at any zoom
}
function fit() {
  const r = vp.getBoundingClientRect();
  s = Math.min(r.width / W, r.height / H) * 0.98;
  tx = (r.width - W * s) / 2; ty = (r.height - H * s) / 2; apply();
}
function zoomAt(f, cx, cy) {
  const ns = Math.min(8, Math.max(0.05, s * f));
  tx = cx - (cx - tx) * (ns / s); ty = cy - (cy - ty) * (ns / s); s = ns; apply();
}
vp.addEventListener('wheel', e => {
  e.preventDefault();
  const r = vp.getBoundingClientRect();
  zoomAt(Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top);
}, { passive: false });
let drag = null;
vp.addEventListener('pointerdown', e => { if (e.button !== 0) return; drag = { x: e.clientX, y: e.clientY, tx, ty, moved: false }; vp.classList.add('drag'); });
window.addEventListener('pointermove', e => {
  if (!drag) return;
  const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
  if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
  tx = drag.tx + dx; ty = drag.ty + dy; apply();
});
window.addEventListener('pointerup', () => { if (!drag) return; vp.classList.remove('drag'); const d = drag; setTimeout(() => { if (drag === d) drag = null; }, 0); });
function focusBox(b) {
  const r = vp.getBoundingClientRect();
  const bw = b[2] - b[0] + 1, bh = b[3] - b[1] + 1;
  s = Math.min(6, Math.min(r.width / (bw * 3.2), r.height / (bh * 3.2)));
  tx = r.width / 2 - ((b[0] + b[2]) / 2) * s; ty = r.height / 2 - ((b[1] + b[3]) / 2) * s; apply();
}
function select(id) {
  document.querySelectorAll('.sel').forEach(el => el.classList.remove('sel'));
  document.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach(el => el.classList.add('sel'));
}
document.querySelectorAll('tr.row').forEach(tr => tr.addEventListener('click', () => {
  const id = tr.dataset.id, o = DATA.index[id];
  if (o) { focusBox(o.bbox); select(id); }
}));
document.querySelectorAll('.box-out, .box-txt, .rel').forEach(el => el.addEventListener('click', () => {
  if (drag && drag.moved) return;
  select(el.dataset.id);
  const tr = document.querySelector(`tr.row[data-id="${CSS.escape(el.dataset.id)}"]`);
  if (tr) tr.scrollIntoView({ block: 'nearest' });
}));
const tip = document.getElementById('tip');
document.querySelectorAll('[data-tip]').forEach(el => {
  el.addEventListener('mousemove', e => { tip.textContent = el.dataset.tip; tip.style.display = 'block'; tip.style.left = (e.clientX + 14) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; });
  el.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
});
for (const cb of document.querySelectorAll('input[data-layer]')) {
  const sync = () => { document.getElementById(cb.dataset.layer).style.display = cb.checked ? '' : 'none'; };
  cb.addEventListener('change', sync); sync();
}
document.getElementById('b-fit').addEventListener('click', fit);
document.getElementById('b-in').addEventListener('click', () => { const r = vp.getBoundingClientRect(); zoomAt(1.5, r.width / 2, r.height / 2); });
document.getElementById('b-out').addEventListener('click', () => { const r = vp.getBoundingClientRect(); zoomAt(1 / 1.5, r.width / 2, r.height / 2); });
window.addEventListener('resize', fit);
fit();
"""


def esc(v) -> str:
    return html.escape(str(v), quote=True)


def iou_class(v):
    return "good" if v >= 0.9 else "mid" if v >= 0.7 else "bad"


def _rect_svg(cls, b, pad=0.5, extra=""):
    return (f'<rect class="{cls}" {extra} x="{b[0] - pad}" y="{b[1] - pad}" '
            f'width="{b[2] - b[0] + 2 * pad}" height="{b[3] - b[1] + 2 * pad}"/>')


def build_html(page_png: bytes, W: int, H: int, out: dict, pairs: dict, starts: dict, title: str,
               trace: dict | None = None, status: dict | None = None, missed=(), gt_by_id=None, window=None) -> str:
    trace, status = trace or {}, status or {}
    all_objs = out["objects"]
    objs = [o for o in all_objs if not is_text(o)]
    texts = [o for o in all_objs if is_text(o)]
    rels = [r for r in out.get("relations", []) if r.get("type", "connected") != "inside"]
    inside = {r["a"]: r["b"] for r in out.get("relations", []) if r.get("type") == "inside"}
    by_id = {o["id"]: o for o in all_objs}
    svg = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">',
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>']
    toggles = []
    if window:
        svg.append('<g id="g-win">' + _rect_svg("box-win", window, 6) +
                   f'<text class="lbl lbl-win" x="{window[0]}" y="{window[1] - 12}">정답 구역 (이 안만 채점)</text></g>')
        toggles.append('<label><input type="checkbox" data-layer="g-win" checked><i class="sw" style="border-color:var(--win);border-top-style:dashed"></i>정답 구역</label>')

    regions = trace.get("regions") or []
    if regions:
        parts = []
        for r in regions:
            b = r["bbox"]
            parts.append(_rect_svg("box-region", b, 8))
            parts.append(f'<text class="lbl lbl-region" x="{b[0]}" y="{b[1] - 14}">{esc(r["id"])} {esc(r.get("kind"))}</text>')
        svg.append('<g id="g-region">' + "".join(parts) + "</g>")
        toggles.append('<label><input type="checkbox" data-layer="g-region"><i class="sw" style="border-color:var(--region);border-top-style:dashed"></i>영역(S1)</label>')
    rejected = [c for c in trace.get("candidates") or [] if not c.get("keep", True)]
    if rejected:
        parts = []
        for c in rejected:
            probs = ", ".join(f"{k} {v:.2f}" for k, v in list((c.get("probs") or {}).items())[:3])
            parts.append(_rect_svg("box-rej", c["bbox"], 1.5, f'data-tip="{esc(c["id"] + " 제외: " + str(c.get("kind")) + chr(10) + probs)}"'))
        svg.append('<g id="g-rej">' + "".join(parts) + "</g>")
        toggles.append('<label><input type="checkbox" data-layer="g-rej"><i class="sw" style="border-color:var(--bad);border-top-style:dotted"></i>제외된 후보(S2)</label>')
    svg.append('<g id="g-start">' + "".join(_rect_svg("box-start", b) for b in starts.values()) + "</g>")
    svg.append('<g id="g-gt">' + "".join(_rect_svg("box-gt", g["bbox"], 2.5) for g in pairs.values()) + "</g>")

    rel_svg, rel_rows = [], []
    for r in rels:
        a, b = by_id.get(r.get("a")), by_id.get(r.get("b"))
        if not a or not b:
            continue
        pts = rel_polyline(r, a["bbox"], b["bbox"])
        ok = status.get(r.get("id"))
        color = net_hex(r) if ok is not False else H_BAD
        t = f'{r.get("id", "")}: {r.get("a")} ({r.get("a_side", "-")}) — {r.get("b")} ({r.get("b_side", "-")})\ntype: {r.get("type", "-")}'
        if r.get("net"):
            t += f'  ·  net {r["net"]}'
        if r.get("confidence") is not None:
            t += f"\nK3 P(연결): {r['confidence']:.2f}"
        if ok is not None:
            t += "\n정답: " + ("있음" if ok else "없음 (틀린 연결)")
        marker = ' marker-end="url(#arr)"' if r.get("directed") else ""
        rel_svg.append(f'<polyline class="rel{"" if ok is not False else " bad"}" data-id="{esc(r.get("id", ""))}" data-tip="{esc(t)}" '
                       f'style="stroke:{color}" points="{" ".join(f"{x},{y}" for x, y in pts)}"{marker}/>')
        conf = "" if r.get("confidence") is None else "%.2f" % r["confidence"]
        mark = "" if ok is None else ('<span class="good">✓</span>' if ok else '<span class="bad">✗</span>')
        rel_rows.append(f'<tr class="row" data-id="{esc(r.get("id", ""))}"><td class="mono"><i class="dot" style="background:{color}"></i>{esc(r.get("id", ""))}</td>'
                        f'<td>{esc(r.get("a"))} <span class="cls">{esc(r.get("a_side", ""))}</span></td>'
                        f'<td>{esc(r.get("b"))} <span class="cls">{esc(r.get("b_side", ""))}</span></td>'
                        f'<td class="num">{conf}</td><td>{mark}</td></tr>')
    svg.append('<g id="g-rel">' + "".join(rel_svg) + "</g>")
    if rels:
        toggles.append('<label><input type="checkbox" data-layer="g-rel" checked><i class="sw" style="border-color:var(--rel)"></i>관계</label>')
    miss_svg, miss_rows = [], []
    for r in missed or ():
        ga, gb = (gt_by_id or {}).get(r["a"]), (gt_by_id or {}).get(r["b"])
        if not ga or not gb:
            continue
        if r.get("type", "connected") == "inside":
            miss_rows.append(f'<tr><td>{esc(r["a"])}</td><td>안: {esc(r["b"])}</td></tr>')
            continue
        (x1, y1), (x2, y2) = rel_points(r, ga["bbox"], gb["bbox"])
        tip = f'놓친 연결 (정답): {r["a"]} ({r.get("a_side", "-")}) — {r["b"]} ({r.get("b_side", "-")})'
        miss_svg.append(f'<line class="rel-miss" data-tip="{esc(tip)}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        miss_rows.append(f'<tr><td>{esc(r["a"])}</td><td>{esc(r["b"])}</td></tr>')
    if miss_svg:
        svg.append('<g id="g-miss">' + "".join(miss_svg) + "</g>")
        toggles.append('<label><input type="checkbox" data-layer="g-miss" checked><i class="sw" style="border-color:var(--bad);border-top-style:dashed"></i>놓친 연결</label>')

    rects, labels = [], []
    for o in objs:
        b = o["bbox"]
        lines = [o["id"], f"class: {o.get('class') or '-'}" + (f" ({o['class_confidence']:.2f})" if o.get("class_confidence") is not None else ""),
                 f"bbox: {b}"]
        if o.get("confidence") is not None:
            lines.append(f"박스 확신도: {o['confidence']:.2f}")
        if o["id"] in pairs:
            g = pairs[o["id"]]
            lines += [f"정답: {g['id']} {g.get('class', '-')}", f"정답 bbox: {g['bbox']}", f"IoU: {iou(b, g['bbox']):.3f}",
                      "변 오차(px) 좌/상/우/하: " + " / ".join(str(int(b[i] - g['bbox'][i])) for i in range(4))]
        if o["id"] in starts:
            lines.append(f"시작 bbox: {list(starts[o['id']])}")
        rects.append(_rect_svg("box-out", b, 0.5, f'data-id="{esc(o["id"])}" data-tip="{esc(chr(10).join(lines))}"'))
        labels.append(f'<text class="lbl lbl-out" x="{b[0]}" y="{b[1] - 6}">{esc(o["id"])}'
                      + (f' {esc(short_class(o.get("class")))}' if o.get("class") else "") + "</text>")
    svg.append('<g id="g-out">' + "".join(rects) + "</g>")
    txt_rects, txt_rows = [], []
    for t in texts:
        b = t["bbox"]
        lines = [t["id"] + " (텍스트)", f"bbox: {b}"]
        if t.get("confidence") is not None:
            lines.append(f"T1 P(글자): {t['confidence']:.2f}")
        if t["id"] in inside:
            lines.append(f"심볼 안: {inside[t['id']]}")
        v = None
        if t["id"] in pairs:
            g = pairs[t["id"]]
            v = iou(b, g["bbox"])
            lines += [f"정답: {g['id']}", f"IoU: {v:.3f}"]
        txt_rects.append(_rect_svg("box-txt", b, 2.5, f'data-id="{esc(t["id"])}" data-tip="{esc(chr(10).join(lines))}"'))
        labels.append(f'<text class="lbl lbl-txt" x="{b[0]}" y="{b[3] + 18}">{esc(t["id"])}</text>')
        iou_txt = "" if v is None else "%.2f" % v
        txt_rows.append(f'<tr class="row" data-id="{esc(t["id"])}"><td class="mono">{esc(t["id"])}</td>'
                        f'<td class="cls">{esc(inside.get(t["id"], ""))}</td><td class="num">{b[2] - b[0] + 1}×{b[3] - b[1] + 1}</td>'
                        f'<td class="num {iou_class(v) if v is not None else ""}">{iou_txt}</td></tr>')
    if texts:
        svg.append('<g id="g-txt">' + "".join(txt_rects) + "</g>")
    svg.append('<g id="g-lbl">' + "".join(labels) + "</g></svg>")

    toggles = (['<label><input type="checkbox" data-layer="g-out" checked><i class="sw" style="border-color:var(--out)"></i>심볼 bbox</label>']
               + (['<label><input type="checkbox" data-layer="g-txt" checked><i class="sw" style="border-color:var(--txt)"></i>텍스트 bbox</label>'] if texts else [])
               + (['<label><input type="checkbox" data-layer="g-gt" checked><i class="sw" style="border-color:var(--gt);border-top-style:dashed"></i>정답 bbox</label>'] if pairs else [])
               + (['<label><input type="checkbox" data-layer="g-start"><i class="sw" style="border-color:var(--start);border-top-style:dotted"></i>시작 bbox</label>'] if starts else [])
               + toggles + ['<label><input type="checkbox" data-layer="g-lbl" checked>id 표시</label>'])

    scored = {k: g for k, g in pairs.items() if not g.get("optional")}   # optional GT objects are not scored
    ious = [iou(o["bbox"], scored[o["id"]]["bbox"]) for o in objs if o["id"] in scored]
    stats = f"심볼 {len(objs)}" + (f" · 텍스트 {len(texts)}" if texts else "") + f" · 연결 {len(rels)}"
    if ious:
        stats += f" · 심볼 정답 대비 평균 IoU {sum(ious) / len(ious):.3f} · IoU≥0.9 {sum(v >= 0.9 for v in ious)}/{len(ious)}"
    tg = sum(1 for t in texts if t["id"] in scored)
    if texts and gt_by_id and any(is_text(g) for g in gt_by_id.values()):
        stats += f" · 텍스트 정답 일치 {tg}/{sum(1 for g in gt_by_id.values() if is_text(g) and not g.get('optional'))}"
    conn_status = {k: v for k, v in status.items() if k in {r.get("id") for r in rels}}
    if conn_status:
        tp = sum(1 for v in conn_status.values() if v)
        stats += f" · 연결 정답 {tp}/{len(conn_status)}, 놓침 {sum(1 for r in missed if r.get('type', 'connected') == 'connected')}"
    rows = []
    for o in objs:
        v = iou(o["bbox"], pairs[o["id"]]["bbox"]) if o["id"] in pairs else None
        cls = o.get("class") or (pairs[o["id"]].get("class", "-") + " (정답)" if o["id"] in pairs else "-")
        wrong = o["id"] in pairs and o.get("class") and pairs[o["id"]].get("class") and pairs[o["id"]]["class"] != o["class"]
        cls_html = esc(cls) + (f' <span class="bad">≠ {esc(pairs[o["id"]]["class"])}</span>' if wrong else "")
        conf_txt = "" if o.get("confidence") is None else "%.2f" % o["confidence"]
        iou_txt = "" if v is None else "%.2f" % v
        iou_cls = iou_class(v) if v is not None else ""
        oid = esc(o["id"])
        rows.append(f'<tr class="row" data-id="{oid}"><td class="mono">{oid}</td><td class="cls">{cls_html}</td>'
                    f'<td class="num">{conf_txt}</td><td class="num {iou_cls}">{iou_txt}</td></tr>')
    rel_table = ('<table><thead><tr><th>id</th><th>a</th><th>b</th><th class="num">K3</th><th></th></tr></thead><tbody>'
                 + "".join(rel_rows) + "</tbody></table>") if rels else '<p class="note">관계 없음</p>'
    miss_html = (f'<h2>놓친 관계 (정답에는 있음) {len(miss_rows)}</h2><table><tbody>' + "".join(miss_rows) + "</tbody></table>") if miss_rows else ""
    index = {o["id"]: {"bbox": o["bbox"]} for o in all_objs}
    for r in rels:
        a, b = by_id.get(r.get("a")), by_id.get(r.get("b"))
        if a and b:
            index[r["id"]] = {"bbox": [min(a["bbox"][0], b["bbox"][0]), min(a["bbox"][1], b["bbox"][1]),
                                       max(a["bbox"][2], b["bbox"][2]), max(a["bbox"][3], b["bbox"][3])]}
    data = {"width": W, "height": H, "index": index}
    css = VIEWER_CSS % {"out": H_OUT, "gt": H_GT, "start": H_START, "rel": H_REL, "bad": H_BAD, "region": H_REGION, "txt": H_TXT, "win": H_WIN}
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><style>{css}</style></head>
<body>
<header>
  <h1>{esc(title)}</h1><span class="stats">{stats}</span>
  {''.join(toggles)}
  <span><button id="b-out">−</button> <button id="b-in">+</button> <button id="b-fit">전체 보기</button></span>
</header>
<main>
  <div id="viewport"><div id="stage" style="width:{W}px;height:{H}px">
    <img src="data:image/png;base64,{base64.b64encode(page_png).decode()}" width="{W}" height="{H}" alt="{esc(out['image']['file'])}" draggable="false">
    {''.join(svg)}
  </div></div>
  <aside>
    <p class="note">휠로 확대·축소, 드래그로 이동. 목록을 누르면 그 객체·연결로 이동하고, 박스나 선에 마우스를 올리면 좌표·확률·정답 비교가 보입니다. 같은 색 선은 같은 net(전기적으로 이어진 선)입니다.</p>
    <h2>objects {len(objs)}</h2>
    <table><thead><tr><th>id</th><th>class</th><th class="num">conf</th><th class="num">IoU</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
    <h2>relations (connected) {len(rels)}</h2>
    {rel_table}
    {miss_html}
    {('<h2>texts ' + str(len(texts)) + '</h2><table><thead><tr><th>id</th><th>심볼 안</th><th class="num">크기</th><th class="num">IoU</th></tr></thead><tbody>' + ''.join(txt_rows) + '</tbody></table>') if texts else ''}
  </aside>
</main>
<div id="tip"></div>
<script>const DATA = {json.dumps(data)};{VIEWER_JS}</script>
</body></html>"""


# ----------------------------------------------------------------------------- main

def page_file_for(out: dict) -> Path:
    img = out["image"]
    if img.get("path"):
        p = Path(img["path"])
        p = p if p.is_absolute() else ROOT / p
        if p.exists():
            return p
    return ROOT / "image" / Path(img["file"]).name


def visualize(output_path: Path, gt_path: Path | None = None, out_dir: Path | None = None, starts_path: Path | None = None) -> list[Path]:
    made = []
    gt, gt_rels, gt_win = _gt_pages(gt_path)
    for out in load_outputs(Path(output_path)):
        src = out.pop("_path")
        page_file = out["image"]["file"]
        page_png = page_file_for(out).read_bytes()
        page = cv2.imdecode(np.frombuffer(page_png, np.uint8), cv2.IMREAD_GRAYSCALE)
        H, W = page.shape[:2]
        gts = gt.get(Path(page_file).name, [])
        window = gt_win.get(Path(page_file).name)
        pairs = match_gt([o for o in out["objects"] if in_window(o["bbox"], window)], gts)
        closure = (out.get("meta") or {}).get("relation_mode") == "mst"
        status, missed = check_relations(out, pairs, gt_rels.get(Path(page_file).name, []), window, closure)
        gt_by_id = {g["id"]: g for g in gts}
        trace = load_trace(src, starts_path)
        objs_t = trace.get("objects", {})
        starts = {k: tuple(v["start_bbox"]) for k, v in objs_t.items() if isinstance(v, dict) and v.get("start_bbox")} if isinstance(objs_t, dict) else {}
        dest = out_dir or src.parent
        dest.mkdir(parents=True, exist_ok=True)
        stem = src.stem.replace("_output", "")
        html_path = dest / f"{stem}.html"
        html_path.write_text(build_html(page_png, W, H, out, pairs, starts, f"{stem} · {page_file}", trace, status, missed, gt_by_id,
                                        window))
        cv2.imwrite(str(dest / f"{stem}_overlay.png"), render_overlay(page, out, pairs, starts, status, missed, gt_by_id, window))
        cv2.imwrite(str(dest / f"{stem}_objects.png"), render_montage(page, out, pairs, starts))
        made += [html_path, dest / f"{stem}_overlay.png", dest / f"{stem}_objects.png"]
    return made


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="출력 JSON을 도면 위에 시각화")
    ap.add_argument("output", type=Path, help="출력 JSON, 정답 파일(gt_p0.json, gt_page-XXX.json), 또는 *_output.json 이 든 폴더")
    ap.add_argument("--gt", type=Path, default=None, help="비교할 정답 파일 (예: experiments/gt_page-016.json)")
    ap.add_argument("--out", type=Path, default=None, help="결과 폴더 (기본: 입력 옆, experiments/ 안의 파일이면 runs/viz)")
    args = ap.parse_args(argv)
    out_dir = args.out
    if out_dir is None and args.output.is_file() and args.output.resolve().parent == HERE:
        out_dir = ROOT / "runs" / "viz"
    made = visualize(args.output, args.gt, out_dir)
    for p in made:
        print(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
