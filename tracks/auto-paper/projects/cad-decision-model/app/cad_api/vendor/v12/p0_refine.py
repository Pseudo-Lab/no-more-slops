# /// script
# requires-python = ">=3.10"
# dependencies = ["typesafe-sdk[pil]==0.7.5", "numpy>=1.24", "opencv-python-headless>=4.8"]
# ///
"""P0 조정 루프 실험: 어긋난 박스에서 출발해 Jev 판단만으로 bbox를 맞추고, 결과를 도면 위에 그린다.

방식 (P0 벤치마크 결과 반영):
- 라운드마다 변 4개 각각에 대해 코드가 후보 위치를 만든다: 현재 위치 + 바깥쪽 3개 + 안쪽 2개
  (가장 가까운 잉크 경계 + 먼 거리 후보를 섞어 작은 오차와 큰 오차를 함께 덮는다).
- 후보 위치마다 빨간 선 하나짜리 이미지를 만들어 방향 질문을 옵션 순서 2가지로 묻고(M2 비교),
  '그대로' 확률이 가장 높은 위치로 변을 옮긴다.
- 모든 후보의 '그대로' 확률이 0.3 미만이면(맞는 후보가 없음) 현재 위치의 방향 답(잘림/빈틈)에 따라 멀리 이동한다.
- 네 변 모두 현재 위치가 최고점이면, 네 변을 한 번 더 확인한 뒤 멈춘다. 최대 8라운드.
  같은 자리를 오가면 지금까지 본 위치 중 최고점에 고정한다.
- 시작 박스는 정답 박스의 각 변을 10–35% 무작위로 어긋나게 만든다(IoU 0.3–0.85, 시드 고정).

실행 (cad-jev 루트에서):
    uv run experiments/p0_refine.py --model jev-1.14.0
    uv run experiments/p0_refine.py --model jev-1.14.0 --symbols p16_or1 p08_not      # 일부만
결과: runs/p0_refine/<시각>/
    page-XXX_output.json  최종 출력 (docs/PLAN.md §6 형식: objects + relations)
    page-XXX_trace.json   라운드별 기록 (시작 박스, 후보, 확률, 선택)
    page-XXX.html         도면 위 시각화 뷰어 (브라우저로 열기)
    page-XXX_overlay.png, page-XXX_objects.png, summary.md
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import views as V  # noqa: E402
import visualize as VZ  # noqa: E402
from p0_bench import (BOX_RULE, FATAL, IMAGES_ON, TASK, USD_PER_TOKEN, WORDS, Fatal, avg, dim_for,  # noqa: E402
                      direction_q, edge_pos, load_env)

from typesafe_sdk import AsyncTypeSafeClient, Image, RetryPolicy, TypeSafeAPIError, TypeSafeError  # noqa: E402

MAX_ROUNDS = 8
OUT_K, IN_K = 3, 2
LOW_KEEP = 0.3        # 모든 후보의 '그대로' 확률이 이보다 낮으면 현재 위치의 방향 답으로 크게 이동
START_MIN, START_MAX = 0.10, 0.35
IOU_MIN, IOU_MAX = 0.30, 0.85
MIN_SIZE = 4
IDX = {"left": 0, "top": 1, "right": 2, "bottom": 3}


def start_box(gt, rng):
    w, h = V.wh(gt)
    b = list(gt)
    for _ in range(200):
        b = list(gt)
        for e in V.EDGES:
            dim = w if e in ("left", "right") else h
            off = max(3, int(round(rng.uniform(START_MIN, START_MAX) * dim))) * rng.choice((-1, 1))   # + = 바깥
            b[IDX[e]] += -off if e in ("left", "top") else off
        if b[2] - b[0] >= 6 and b[3] - b[1] >= 6 and IOU_MIN <= VZ.iou(b, gt) <= IOU_MAX:
            break
    return tuple(b)


def spread(cur, cands, k, search, sign):
    """가까운 잉크 경계 하나 + 먼 거리(탐색 범위의 40%, 100%) 근처 후보로, 작은 오차와 큰 오차를 함께 덮는다."""
    if k <= 0:
        return []
    chosen = [cands[0]] if cands else []
    for f in (0.4, 1.0)[: k - 1 if cands else k]:
        t = f * search
        near = min(cands, key=lambda c: abs(abs(c - cur) - t)) if cands else None
        pick = near if near is not None and abs(abs(near - cur) - t) <= 0.25 * t else cur + sign * int(round(t))
        if abs(pick - cur) >= 2 and all(abs(pick - c) >= 3 for c in chosen):
            chosen.append(pick)
    return chosen


def candidate_positions(page, box, edge):
    """현재 위치 + 바깥쪽 후보(최대 OUT_K) + 안쪽 후보(최대 IN_K). 반환: (전체 정렬 목록, 바깥 목록, 안쪽 목록)"""
    cur = edge_pos(box, edge)
    dim = dim_for(box, edge)
    out_search, in_search = max(int(round(0.8 * dim)), 20), max(int(round(0.45 * dim)), 6)
    out_sign = -1 if edge in ("top", "left") else 1
    outs = spread(cur, V.ink_candidates(page, box, edge, True, out_search, max_k=50), OUT_K, out_search, out_sign)
    ins = spread(cur, V.ink_candidates(page, box, edge, False, in_search, max_k=50), IN_K, in_search, -out_sign)
    x0, y0, x1, y1 = box
    H, W = page.shape[:2]
    limit = {"top": lambda p: 0 <= p <= y1 - MIN_SIZE, "bottom": lambda p: y0 + MIN_SIZE <= p < H,
             "left": lambda p: 0 <= p <= x1 - MIN_SIZE, "right": lambda p: x0 + MIN_SIZE <= p < W}[edge]
    outs, ins = [p for p in outs if limit(p)], [p for p in ins if limit(p)]
    return sorted({cur, *outs, *ins}), outs, ins


class Runner:
    """Jev 호출 담당: 후보 위치마다 뷰를 만들어 방향 질문을 하고, 위치별 평균 확률을 돌려준다."""

    def __init__(self, client, model, concurrency):
        self.client, self.model = client, model
        self.sem = asyncio.Semaphore(concurrency)
        self.requests = self.tokens = self.errors = 0
        self.ms: list[int] = []
        self.fatal = None

    async def judge(self, page, box, edge, positions):
        def build():
            ctx = Image(V.png_bytes(V.context_view(page, box)))
            qs = {}
            for i, p in enumerate(positions):
                key = f"cand{i + 1}_view"
                img = Image(V.png_bytes(V.edge_view(page, V.with_edge(box, edge, p), edge)))
                qs[f"c{i + 1}_A"] = direction_q(edge, img, False, key, "candidate")
                qs[f"c{i + 1}_B"] = direction_q(edge, img, True, key, "candidate")
            return {"task": TASK, "box_rule": BOX_RULE, "context": ctx}, qs

        async with self.sem:
            if self.fatal:
                raise Fatal(self.fatal)
            st, qs = await asyncio.to_thread(build)
            t0 = time.perf_counter()
            try:
                resp = await self.client.system_one(state=st, questions=qs, model=self.model, extra_headers=IMAGES_ON)
            except TypeSafeAPIError as error:
                if error.status in FATAL:
                    self.fatal = f"{error.status} — {FATAL[error.status]} (request_id={error.request_id})"
                    raise Fatal(self.fatal) from error
                self.errors += 1
                return None
            except TypeSafeError:
                self.errors += 1
                return None
            self.requests += 1
            self.tokens += resp.usage.input_tokens or 0
            self.ms.append(round((time.perf_counter() - t0) * 1000))
            return [avg(resp.choices[f"c{i + 1}_A"].probabilities, resp.choices[f"c{i + 1}_B"].probabilities)
                    for i in range(len(positions))]


async def refine(page, start, judge):
    """한 심볼의 조정 루프. judge(page, box, edge, positions) -> 위치별 확률 목록 (실패 시 None)."""
    box = tuple(start)
    rounds = []
    settled = {e: False for e in V.EDGES}
    seen = {e: {} for e in V.EDGES}                  # 위치 -> 지금까지 본 '그대로' 최고 확률
    visited = {e: [edge_pos(box, e)] for e in V.EDGES}
    verified = False
    for rnd in range(1, MAX_ROUNDS + 1):
        todo = [e for e in V.EDGES if not settled[e]]
        if not todo:
            if verified:
                break
            verified = True                          # 수렴 후 네 변을 한 번 더 확인
            settled = {e: False for e in V.EDGES}
            todo = list(V.EDGES)
        cand = {e: candidate_positions(page, box, e) for e in todo}
        plans = {e: cand[e][0] for e in todo}
        results = await asyncio.gather(*(judge(page, box, e, plans[e]) for e in todo))
        new = list(box)
        log = {"round": rnd, "box": list(box), "edges": {}}
        for e, probs in zip(todo, results):
            cur = edge_pos(box, e)
            if probs is None:
                settled[e] = True
                log["edges"][e] = {"positions": plans[e], "error": True}
                continue
            pk = [round(p.get("keep", 0.0), 4) for p in probs]
            for p_, k_ in zip(plans[e], pk):
                seen[e][p_] = max(seen[e].get(p_, 0.0), k_)
            best = plans[e][max(range(len(pk)), key=pk.__getitem__)]
            rule = "keep"
            outs, ins = cand[e][1], cand[e][2]
            if max(pk) < LOW_KEEP:                  # 맞는 후보가 없음: 현재 위치의 방향 답으로 크게 이동
                pc = probs[plans[e].index(cur)]
                out_w, in_w = WORDS[e][0], WORDS[e][1]
                if outs and pc.get(out_w, 0) >= max(pc.get("keep", 0), pc.get(in_w, 0)):
                    best, rule = max(outs, key=lambda p: abs(p - cur)), "jump_out"
                elif ins and pc.get(in_w, 0) > pc.get("keep", 0):
                    best, rule = min(ins, key=lambda p: abs(p - cur)), "jump_in"
            if rule == "keep" and best == cur:
                settled[e] = True
            elif rule == "keep" and best in visited[e]:   # 오가는 중: 본 위치 중 최고점에 고정
                best, rule = max(seen[e], key=seen[e].get), "oscillation"
                settled[e] = True
            if best != cur:
                verified = False
            visited[e].append(best)
            new[IDX[e]] = best
            log["edges"][e] = {"positions": plans[e], "p_keep": pk, "chosen": best, "rule": rule}
        if new[2] - new[0] < MIN_SIZE or new[3] - new[1] < MIN_SIZE:   # 양쪽 변이 동시에 안으로 들어와 뒤집히면 이번 이동 취소
            new = list(box)
            log["reverted"] = True
        box = tuple(new)
        rounds.append(log)
    conf = min(seen[e].get(edge_pos(box, e), 0.0) for e in V.EDGES)    # 가장 불확실한 변 기준
    return box, round(conf, 4), rounds


def summarize(records, runner, elapsed, model):
    ious0 = [r["iou_start"] for r in records]
    ious1 = [r["iou_final"] for r in records]
    errs = [abs(r["final"][i] - r["gt"][i]) for r in records for i in range(4)]
    rounds = [r["rounds"] for r in records]
    lines = [f"# P0 조정 루프 결과 ({model})", "",
             f"심볼 {len(records)}개 · 요청 {runner.requests} (실패 {runner.errors}) · 입력 토큰 {runner.tokens:,} "
             f"(≈ ${runner.tokens * USD_PER_TOKEN:.3f}) · 소요 {elapsed:.0f}초"
             + (f" · 지연 중앙값 {int(statistics.median(runner.ms))} ms" if runner.ms else ""), "",
             "| | 시작 박스 | 최종 박스 |", "|---|---|---|",
             f"| 평균 IoU | {statistics.mean(ious0):.3f} | {statistics.mean(ious1):.3f} |",
             f"| IoU ≥ 0.9 | {sum(v >= 0.9 for v in ious0)}/{len(records)} | {sum(v >= 0.9 for v in ious1)}/{len(records)} |",
             f"| IoU ≥ 0.95 | {sum(v >= 0.95 for v in ious0)}/{len(records)} | {sum(v >= 0.95 for v in ious1)}/{len(records)} |", "",
             f"변 오차: 중앙값 {statistics.median(errs):.0f}px · ±2px 이내 {sum(e <= 2 for e in errs)}/{len(errs)} · "
             f"라운드 중앙값 {statistics.median(rounds):.0f} (최대 {max(rounds)})", "",
             "| 심볼 | 시작 IoU | 최종 IoU | 변 오차 (좌/상/우/하, px) | 라운드 | 신뢰도 |", "|---|---|---|---|---|---|"]
    for r in sorted(records, key=lambda r: r["iou_final"]):
        e = " / ".join(f"{int(r['final'][i] - r['gt'][i]):+d}" for i in range(4))
        lines.append(f"| {r['id']} | {r['iou_start']:.2f} | {r['iou_final']:.2f} | {e} | {r['rounds']} | {r['conf']:.2f} |")
    return "\n".join(lines)


async def main(argv=None, transport=None, judge_override=None) -> int:
    load_env(ROOT / ".env")
    ap = argparse.ArgumentParser(description="Jev P0 bbox refinement loop")
    ap.add_argument("--model", default=os.environ.get("TYPESAFE_MODEL", "jev-1.13.0"))
    ap.add_argument("--symbols", nargs="*", help="심볼 id 일부만 (기본: 정답 박스 25개 전부)")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0, help="시작 박스를 만드는 난수 시드")
    args = ap.parse_args(argv)
    if judge_override is None and not os.environ.get("TYPESAFE_API_KEY"):
        print("TYPESAFE_API_KEY 가 없습니다. cad-jev/.env 를 확인하세요.")
        return 2

    gt_path = HERE / "gt_p0.json"
    symbols = json.loads(gt_path.read_text())["symbols"]
    if args.symbols:
        symbols = [s for s in symbols if s["id"] in set(args.symbols)]
    pages = {p: V.load_page(ROOT / "image" / p) for p in {s["page"] for s in symbols}}
    out_dir = ROOT / "runs" / "p0_refine" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)

    client = AsyncTypeSafeClient(api_key=os.environ.get("TYPESAFE_API_KEY", "offline"), model=args.model, timeout=90.0,
                                 retry=RetryPolicy(max_retries=4, timeout=180.0), transport=transport)
    runner = Runner(client, args.model, args.concurrency)
    judge = judge_override or runner.judge
    records, traces, done = [], {}, 0
    t0 = time.perf_counter()
    print(f"[{args.model}] 심볼 {len(symbols)}개 조정 시작 (동시 요청 {args.concurrency})")

    async def one(sym):
        nonlocal done
        gt = tuple(sym["bbox"])
        start = start_box(gt, random.Random(f"{args.seed}-{sym['id']}"))
        final, conf, rounds = await refine(pages[sym["page"]], start, lambda *a: judge(*a))
        records.append({"id": sym["id"], "page": sym["page"], "class": sym["class"], "gt": list(gt), "start": list(start),
                        "final": list(final), "conf": conf, "rounds": len(rounds),
                        "iou_start": VZ.iou(start, gt), "iou_final": VZ.iou(final, gt)})
        traces.setdefault(sym["page"], {})[sym["id"]] = {"start_bbox": list(start), "gt_bbox": list(gt), "final_bbox": list(final),
                                                          "confidence": conf, "rounds": rounds}
        done += 1
        print(f"\r  완료 {done}/{len(symbols)}", end="", flush=True)

    fatal = None
    async with client:
        try:
            await asyncio.gather(*(one(s) for s in symbols))
        except Fatal as error:
            fatal = error
    print()
    if fatal:
        print(f"중단: {fatal}")
        return 1

    for page in sorted({r["page"] for r in records}):
        H, W = pages[page].shape[:2]
        objs = [{"id": r["id"], "class": None, "bbox": r["final"], "confidence": r["conf"]}
                for r in sorted(records, key=lambda r: r["id"]) if r["page"] == page]
        output = {"image": {"file": page, "width": W, "height": H}, "objects": objs, "relations": [],
                  "note": f"P0 조정 루프 실험 출력 ({args.model}). class는 분류 툴 구현 전이라 비어 있음, relations는 연결 판단 구현 전."}
        stem = Path(page).stem
        (out_dir / f"{stem}_output.json").write_text(json.dumps(output, ensure_ascii=False, indent=1))
        (out_dir / f"{stem}_trace.json").write_text(json.dumps({"model": args.model, "objects": traces[page]}, ensure_ascii=False, indent=1))

    text = summarize(records, runner, time.perf_counter() - t0, args.model)
    (out_dir / "summary.md").write_text(text + "\n")
    print("\n" + text)
    made = VZ.visualize(out_dir, HERE / "gt_p0.json")
    print("\n시각화 (브라우저로 열기):")
    for p in made:
        if p.suffix == ".html":
            print(f"  open {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
