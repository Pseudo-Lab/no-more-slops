# /// script
# requires-python = ">=3.10"
# dependencies = ["typesafe-sdk[pil]==0.7.5", "numpy>=1.24", "opencv-python-headless>=4.8"]
# ///
"""P0 벤치마크: 정답 박스 25개로 변 방향 툴(B1)과 이동량 툴 두 방식(M1, M2)을 측정한다.

- 방향(B1): 정답 박스의 변 하나를 δ만큼 어긋나게 하고(−40% … +40%) 위/그대로/아래(좌/그대로/우)를 묻는다.
- 이동량 M1: 후보선 여러 개를 한 이미지에 번호로 그리고 하나를 고르게 한다 (스모크 테스트 방식).
- 이동량 M2: 후보 위치마다 빨간 선 하나짜리 뷰를 만들어 방향 질문을 하고, '그대로' 확률이 가장 높은 후보를 고른다.
모든 Choice 질문은 옵션 순서를 바꿔 두 번 묻고 확률을 평균 낸다.

실행 (cad-jev 루트에서):
    uv run experiments/p0_bench.py --dry-run                        # API 호출 없이 렌더링·요청 수·예상 비용 확인
    uv run experiments/p0_bench.py                                  # .env 의 TYPESAFE_MODEL 로 전체 실행
    uv run experiments/p0_bench.py --models jev-1.13.0 jev-1.14.0   # 모델 비교
    uv run experiments/p0_bench.py --parts direction                # 방향만 (direction / magnitude)
결과: runs/p0_bench/<시각>_summary.md (요약), <시각>_<모델>.jsonl (케이스별 원문)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import views as V  # noqa: E402

from typesafe_sdk import AsyncTypeSafeClient, Choice, Image, RetryPolicy, TypeSafeAPIError, TypeSafeError  # noqa: E402

IMAGES_ON = {"TypeSafe-Danger-Zone-Images": "true"}
USD_PER_TOKEN = 0.042 / 1_000_000
PX_PER_TOKEN = 380          # P0 스모크 테스트 실측: 이미지 토큰 ≈ 가로×세로 / 380
TOL = 2                     # 이동량 정답 허용 오차 (px)
DIR_LEVELS = [-0.4, -0.15, -0.06, 0.0, 0.06, 0.15, 0.4]   # 변 길이 대비. + = 박스가 큼(빈틈), − = 박스가 심볼을 자름
MAG_LEVELS = [-0.4, -0.15, 0.15, 0.4]
MIN_PX = {0.06: 2, 0.15: 4, 0.4: 8}
FATAL = {401: "API 키가 거부됐습니다 (.env 확인).", 402: "TypeSafe 크레딧이 없습니다 (console.typesafe.ai/settings/billing).",
         403: "이 키에 권한이 없습니다."}

TASK = "A box must tightly enclose ONE schematic symbol in an engineering logic diagram."
BOX_RULE = ("Inside the box: every stroke of the symbol body, including its vertical input bar and any letters "
            "drawn inside it. Outside the box: wires (connecting lines) leaving the symbol, and text labels next to it.")
#         outward  inward   side word     'beyond' phrase     line orientation
WORDS = {
    "top": ("up", "down", "topmost", "above", "horizontal"),
    "bottom": ("down", "up", "bottommost", "below", "horizontal"),
    "left": ("left", "right", "leftmost", "to the left of", "vertical"),
    "right": ("right", "left", "rightmost", "to the right of", "vertical"),
}


class Fatal(Exception):
    pass


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.removeprefix("export ").strip(), value.strip().strip("'\""))


# ----------------------------------------------------------------------------- questions

def ordered(criteria: dict, reverse: bool) -> dict:
    return dict(reversed(list(criteria.items()))) if reverse else criteria


def direction_q(edge, img, reverse, key, framing):
    out, inward, side, beyond, orient = WORDS[edge]
    criteria = {
        out: f"Some stroke of the symbol body (not a wire) is {beyond} the red line, or the red line cuts through the symbol.",
        "keep": f"The red line touches the {side} stroke of the symbol body or leaves only a hair-thin gap; "
                f"no part of the symbol body is {beyond} it.",
        inward: f"There is clear space (white, or only wires) between the red line and the {side} stroke of the symbol body.",
    }
    lead = (f"In `{key}`, the thick red {orient} line is the {edge.upper()} edge of the box shown in `context`."
            if framing == "box" else
            f"In `{key}`, the thick red {orient} line is a possible {edge.upper()} edge of the box around the symbol in `context`.")
    return Choice(instructions={key: img, "question": f"{lead} Compare it with the {side} stroke of the symbol body. "
                                                      f"Ignore wires and text labels."},
                  criteria=ordered(criteria, reverse))


def magnitude_q(edge, n, outward, img, reverse):
    _, _, side, beyond, _ = WORDS[edge]
    criteria = {str(i + 1): f"the {V.COLOR_NAMES[i]} line labelled {i + 1}" for i in range(n)}
    criteria["beyond"] = (f"The symbol body continues {beyond} every numbered line." if outward
                          else "Every numbered line still leaves a gap before the symbol body.")
    return Choice(instructions={"candidates": img,
                                "question": f"In `candidates`, numbered colored lines are possible positions for the {edge.upper()} "
                                            f"edge of the box around the symbol in `context`. Which numbered line touches the {side} "
                                            f"stroke of the symbol body without cutting it? Wires and text labels are not part of the symbol."},
                  criteria=ordered(criteria, reverse))


# ----------------------------------------------------------------------------- cases

def dim_for(b, edge):
    w, h = V.wh(b)
    return h if edge in ("top", "bottom") else w


def offset_px(level, dim):
    if level == 0:
        return 0
    mag = max(int(round(abs(level) * dim)), MIN_PX[abs(level)])
    return mag if level > 0 else -mag


def perturb(b, edge, off):
    x0, y0, x1, y1 = b
    return {"top": (x0, y0 - off, x1, y1), "bottom": (x0, y0, x1, y1 + off),
            "left": (x0 - off, y0, x1, y1), "right": (x0, y0, x1 + off, y1)}[edge]


def edge_pos(b, edge):
    return {"top": b[1], "bottom": b[3], "left": b[0], "right": b[2]}[edge]


class Case:
    def __init__(self, kind, meta, build):
        self.kind, self.meta, self.build = kind, meta, build
        self.result = None
        self.images: list[tuple[str, int, object]] = []   # (name, references, ndarray) for dry-run / samples


def image(case: Case, name: str, img, refs: int) -> Image:
    case.images.append((name, refs, img))
    return Image(V.png_bytes(img))


def state_for(case, page, box):
    return {"task": TASK, "box_rule": BOX_RULE, "context": image(case, "context", V.context_view(page, box), 1)}


def make_cases(symbols, pages, parts):
    cases = []
    for sym in symbols:
        page, gt = pages[sym["page"]], tuple(sym["bbox"])
        base = {"id": sym["id"], "class": sym["class"]}
        if "direction" in parts:
            def build_zero(case, page=page, gt=gt):
                st = state_for(case, page, gt)
                qs = {}
                for e in V.EDGES:
                    ev = image(case, f"{e}_view", V.edge_view(page, gt, e), 2)
                    qs[f"{e}_A"] = direction_q(e, ev, False, f"{e}_view", "box")
                    qs[f"{e}_B"] = direction_q(e, ev, True, f"{e}_view", "box")
                return st, qs
            cases.append(Case("direction0", {**base, "box": gt}, build_zero))
            for e in V.EDGES:
                for lv in DIR_LEVELS:
                    if lv == 0:
                        continue
                    off = offset_px(lv, dim_for(gt, e))
                    box = perturb(gt, e, off)
                    out, inward = WORDS[e][:2]
                    meta = {**base, "edge": e, "level": lv, "offset": off, "box": box, "expected": inward if off > 0 else out}

                    def build_dir(case, page=page, box=box, e=e):
                        st = state_for(case, page, box)
                        ev = image(case, f"{e}_view", V.edge_view(page, box, e), 2)
                        return st, {"A": direction_q(e, ev, False, f"{e}_view", "box"),
                                    "B": direction_q(e, ev, True, f"{e}_view", "box")}
                    cases.append(Case("direction", meta, build_dir))
        if "magnitude" in parts:
            for e in V.EDGES:
                for lv in MAG_LEVELS:
                    off = offset_px(lv, dim_for(gt, e))
                    box = perturb(gt, e, off)
                    outward = off < 0                       # 박스가 심볼을 자르면 변은 바깥으로 움직여야 한다
                    search = max(int(round(1.0 * dim_for(box, e))), 20)   # 실서비스에서는 beyond가 나오면 범위를 넓힌다
                    cands = V.ink_candidates(page, box, e, outward, search)
                    if not cands:
                        continue
                    gpos = edge_pos(gt, e)
                    meta = {**base, "edge": e, "level": lv, "offset": off, "box": box, "outward": outward,
                            "cands": cands, "gt_pos": gpos, "reachable": any(abs(c - gpos) <= TOL for c in cands)}

                    def build_m1(case, page=page, box=box, e=e, cands=cands, outward=outward):
                        st = state_for(case, page, box)
                        mv = image(case, "candidates", V.magnitude_view(page, box, e, cands), 2)
                        return st, {"A": magnitude_q(e, len(cands), outward, mv, False),
                                    "B": magnitude_q(e, len(cands), outward, mv, True)}

                    def build_m2(case, page=page, box=box, e=e, cands=cands):
                        st = state_for(case, page, box)
                        qs = {}
                        for i, c in enumerate(cands):
                            key = f"cand{i + 1}_view"
                            ev = image(case, key, V.edge_view(page, V.with_edge(box, e, c), e), 2)
                            qs[f"c{i + 1}_A"] = direction_q(e, ev, False, key, "candidate")
                            qs[f"c{i + 1}_B"] = direction_q(e, ev, True, key, "candidate")
                        return st, qs
                    cases.append(Case("m1", dict(meta), build_m1))
                    cases.append(Case("m2", dict(meta), build_m2))
    return cases


# ----------------------------------------------------------------------------- running

async def run_cases(client, model, cases, conc):
    sem = asyncio.Semaphore(conc)
    state = {"done": 0, "fatal": None}

    async def one(case):
        async with sem:
            if state["fatal"]:
                return
            st, qs = await asyncio.to_thread(case.build, case)
            t0 = time.perf_counter()
            try:
                resp = await client.system_one(state=st, questions=qs, model=model, extra_headers=IMAGES_ON)
                case.result = {"ms": round((time.perf_counter() - t0) * 1000), "tokens": resp.usage.input_tokens or 0,
                               "model": resp.model, "probs": {k: v.probabilities for k, v in resp.choices.items()}}
            except TypeSafeAPIError as error:
                case.result = {"error": str(error)}
                if error.status in FATAL:
                    state["fatal"] = error
            except TypeSafeError as error:
                case.result = {"error": str(error)}
            finally:
                case.images.clear()
            state["done"] += 1
            if state["done"] % 25 == 0 or state["done"] == len(cases):
                print(f"\r  진행 {state['done']}/{len(cases)}", end="", flush=True)

    await asyncio.gather(*(one(c) for c in cases))
    print()
    if state["fatal"]:
        e = state["fatal"]
        raise Fatal(f"{e.status} — {FATAL[e.status]} (request_id={e.request_id})")


# ----------------------------------------------------------------------------- scoring

def avg(*dists):
    keys = {k for d in dists for k in d}
    return {k: sum(d.get(k, 0.0) for d in dists) / len(dists) for k in keys}


def argmax(d):
    return max(d, key=d.get)


def direction_rows(cases):
    rows = []
    for c in cases:
        r = c.result
        if not r or "error" in r:
            continue
        if c.kind == "direction0":
            pairs = [(e, r["probs"][f"{e}_A"], r["probs"][f"{e}_B"], 0.0, "keep") for e in V.EDGES]
        elif c.kind == "direction":
            pairs = [(c.meta["edge"], r["probs"]["A"], r["probs"]["B"], c.meta["level"], c.meta["expected"])]
        else:
            continue
        for e, pa, pb, lv, exp in pairs:
            p = avg(pa, pb)
            pred = argmax(p)
            rows.append({"id": c.meta["id"], "class": c.meta["class"], "edge": e, "level": lv, "expected": exp,
                         "pred": pred, "correct": pred == exp, "flip": argmax(pa) != argmax(pb), "maxp": p[pred],
                         "p_keep": p.get("keep", 0.0)})
    return rows


def magnitude_rows(cases):
    rows = []
    for c in cases:
        r = c.result
        if c.kind not in ("m1", "m2") or not r or "error" in r:
            continue
        m, cands = c.meta, c.meta["cands"]
        if c.kind == "m1":
            p = avg(r["probs"]["A"], r["probs"]["B"])
            ch = argmax(p)
            pick = None if ch == "beyond" else cands[int(ch) - 1]
            extra = {"choice": ch, "conf": p[ch]}
        else:
            out, inward = WORDS[m["edge"]][:2]
            cont = out if m["outward"] else inward              # 계속 같은 방향으로 가야 한다는 답
            per = [avg(r["probs"][f"c{i + 1}_A"], r["probs"][f"c{i + 1}_B"]) for i in range(len(cands))]
            best = max(range(len(cands)), key=lambda i: per[i].get("keep", 0.0))
            pick = cands[best]
            flip = next((i for i, p in enumerate(per) if argmax(p) != cont), len(cands) - 1)
            extra = {"pick_flip": cands[flip], "p_keep": [round(p.get("keep", 0.0), 3) for p in per]}
        rows.append({"kind": c.kind, "id": m["id"], "edge": m["edge"], "level": m["level"], "reachable": m["reachable"],
                     "gt_pos": m["gt_pos"], "pick": pick, "correct": pick is not None and abs(pick - m["gt_pos"]) <= TOL,
                     "err": None if pick is None else abs(pick - m["gt_pos"]), **extra})
    return rows


def pct(x):
    return f"{100 * x:5.1f}%" if x is not None else "   -  "


def rate(rows, key="correct"):
    return (sum(r[key] for r in rows) / len(rows)) if rows else None


def summarize(model, cases, lines):
    say = lines.append
    res = [c.result for c in cases if c.result]
    errors = [r for r in res if "error" in r]
    tokens = sum(r.get("tokens", 0) for r in res)
    ms = sorted(r["ms"] for r in res if "ms" in r)
    say(f"\n## {model}\n")
    say(f"요청 {len(res)} (에러 {len(errors)}) · 입력 토큰 {tokens:,} (≈ ${tokens * USD_PER_TOKEN:.3f}) · "
        f"지연 중앙값 {ms[len(ms) // 2] if ms else 0} ms, p90 {ms[int(len(ms) * 0.9)] if ms else 0} ms")
    if errors:
        say(f"에러 예시: {errors[0]['error'][:200]}")

    d = direction_rows(cases)
    if d:
        say("\n### 변 방향 (B1) — 순서 2가지 평균")
        say("| δ (변 길이 대비) | " + " | ".join(f"{int(lv * 100):+d}%" for lv in DIR_LEVELS) + " |")
        say("|---" * (len(DIR_LEVELS) + 1) + "|")
        say("| 정답률 | " + " | ".join(pct(rate([r for r in d if r["level"] == lv])) for lv in DIR_LEVELS) + " |")
        def keep_ratio(rs):
            return sum(r["pred"] == "keep" for r in rs) / len(rs) if rs else None
        say("| '그대로' 답 비율 | " + " | ".join(pct(keep_ratio([r for r in d if r["level"] == lv])) for lv in DIR_LEVELS) + " |")
        say("| n | " + " | ".join(str(len([r for r in d if r["level"] == lv])) for lv in DIR_LEVELS) + " |")
        big = [r for r in d if abs(r["level"]) >= 0.15]
        say("\n변별 정답률 (|δ| ≥ 15%): " + " · ".join(f"{e} {pct(rate([r for r in big if r['edge'] == e]))}" for e in V.EDGES))
        by_cls = defaultdict(list)
        for r in big:
            by_cls[r["class"].split("/")[0]].append(r)
        say("클래스별 (|δ| ≥ 15%): " + " · ".join(f"{k} {pct(rate(v))} (n={len(v)})" for k, v in sorted(by_cls.items())))
        say(f"옵션 순서를 바꾸면 답이 바뀐 비율: {pct(rate(d, 'flip'))}")
        bins = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)]
        say("확신도(평균 확률 최댓값) 구간별 정답률: " + " · ".join(
            f"[{a:.1f},{min(b, 1):.1f}) {pct(rate([r for r in d if a <= r['maxp'] < b]))} (n={len([r for r in d if a <= r['maxp'] < b])})"
            for a, b in bins))
        conf = defaultdict(int)
        for r in d:
            conf[(r["expected"] if r["expected"] == "keep" else ("out" if r["level"] < 0 else "in"),
                  "keep" if r["pred"] == "keep" else ("out" if r["pred"] == WORDS[r["edge"]][0] else "in"))] += 1
        say("혼동표 (기대→예측, out=확장 / in=축소): " + " · ".join(
            f"{a}→{b} {conf[(a, b)]}" for a in ("out", "keep", "in") for b in ("out", "keep", "in")))

    m = magnitude_rows(cases)
    if m:
        say("\n### 이동량 — M1 (한 이미지에 번호 후보선) vs M2 (후보별 방향 질문)")
        say("| δ | 후보 안에 정답 있음 | M1 정답률 | M2 정답률 ('그대로' 최대) | M2-flip (방향이 바뀌는 첫 후보) |")
        say("|---|---|---|---|---|")
        for lv in MAG_LEVELS + ["전체"]:
            sel = (lambda r: True) if lv == "전체" else (lambda r, lv=lv: r["level"] == lv)
            m1 = [r for r in m if r["kind"] == "m1" and sel(r)]
            m2 = [r for r in m if r["kind"] == "m2" and sel(r)]
            reach = rate(m1 or m2, "reachable")
            flip = (sum(abs(r["pick_flip"] - r["gt_pos"]) <= TOL for r in m2) / len(m2)) if m2 else None
            label = lv if lv == "전체" else f"{int(lv * 100):+d}%"
            say(f"| {label} | {pct(reach)} | {pct(rate(m1))} | {pct(rate(m2))} | {pct(flip)} |")
        m1b = [r for r in m if r["kind"] == "m1"]
        say(f"M1이 'beyond'를 고른 비율: {pct(sum(r['choice'] == 'beyond' for r in m1b) / len(m1b) if m1b else None)}")


def write_jsonl(path, cases):
    with path.open("w") as f:
        for c in cases:
            f.write(json.dumps({"kind": c.kind, "meta": c.meta, "result": c.result}, ensure_ascii=False) + "\n")


# ----------------------------------------------------------------------------- main

def dry_run(cases, out_dir, n_samples):
    sample_dir = out_dir / "samples"
    sample_dir.mkdir(parents=True, exist_ok=True)
    per_kind = defaultdict(int)
    tokens, images, t0 = 0, 0, time.perf_counter()
    for c in cases:
        _, qs = c.build(c)
        tokens += 300 + 150 * len(qs)
        for name, refs, img in c.images:
            tokens += refs * img.shape[0] * img.shape[1] // PX_PER_TOKEN
            images += 1
            if per_kind[c.kind] < n_samples:
                tag = f"{c.meta['id']}_{c.meta.get('edge', 'all')}_{c.meta.get('level', 0):+.2f}"
                V.cv2.imwrite(str(sample_dir / f"{c.kind}_{tag}_{name}.png"), img)
        per_kind[c.kind] += 1
        c.images.clear()
    print(f"렌더링 OK: 요청 {len(cases)}개, 이미지 {images}장 ({time.perf_counter() - t0:.1f}초)")
    print("요청 종류별: " + ", ".join(f"{k} {v}" for k, v in per_kind.items()))
    print(f"모델 1개당 예상 입력 토큰 ≈ {tokens:,} (≈ ${tokens * USD_PER_TOKEN:.2f})")
    print(f"샘플 이미지: {sample_dir.relative_to(ROOT)}/")


async def main(argv=None, transport=None) -> int:
    load_env(ROOT / ".env")
    ap = argparse.ArgumentParser(description="Jev P0 benchmark")
    ap.add_argument("--models", nargs="+", default=[os.environ.get("TYPESAFE_MODEL", "jev-1.13.0")])
    ap.add_argument("--parts", nargs="+", default=["direction", "magnitude"], choices=["direction", "magnitude"])
    ap.add_argument("--symbols", nargs="*", help="심볼 id 일부만 (기본: 전체 25개)")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true", help="API 호출 없이 렌더링·요청 수·예상 비용만 확인")
    ap.add_argument("--samples", type=int, default=4, help="--dry-run 때 종류별로 저장할 샘플 이미지 수")
    args = ap.parse_args(argv)

    gt = json.loads((HERE / "gt_p0.json").read_text())["symbols"]
    if args.symbols:
        gt = [s for s in gt if s["id"] in set(args.symbols)]
    pages = {p: V.load_page(ROOT / "image" / p) for p in {s["page"] for s in gt}}
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "runs" / "p0_bench"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        dry_run(make_cases(gt, pages, args.parts), out_dir, args.samples)
        return 0
    if not os.environ.get("TYPESAFE_API_KEY"):
        print("TYPESAFE_API_KEY 가 없습니다. cad-jev/.env 를 확인하세요.")
        return 2

    lines = [f"# P0 벤치마크 결과 ({stamp})", f"심볼 {len(gt)}개 · 파트 {', '.join(args.parts)} · 이동량 허용 오차 ±{TOL}px"]
    code = 0
    for model in args.models:
        cases = make_cases(gt, pages, args.parts)
        print(f"\n[{model}] 요청 {len(cases)}개 실행 (동시 {args.concurrency})")
        client = AsyncTypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], model=model, timeout=90.0,
                                     retry=RetryPolicy(max_retries=4, timeout=180.0), transport=transport)
        async with client:
            try:
                await run_cases(client, model, cases, args.concurrency)
            except Fatal as error:
                print(f"\n중단: {error}")
                code = 1
        write_jsonl(out_dir / f"{stamp}_{model}.jsonl", cases)
        summarize(model, cases, lines)
        if code:
            break
    text = "\n".join(lines)
    print("\n" + text)
    summary = out_dir / f"{stamp}_summary.md"
    summary.write_text(text + "\n")
    print(f"\n저장: {summary.relative_to(ROOT)} (+ 모델별 .jsonl)")
    return code


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
