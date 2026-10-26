"""Retain local wire hypotheses and account for observed P&ID contacts.

This supplement does not draw wires or accept connections.  Original v13
questions remain primary; routes on another actual graph are kept as explicit
alternatives.  New questions are bounded by ports and their nearest traced
neighbours.  No graph is joined through a symbol's body.
"""
from __future__ import annotations

import copy
from functools import wraps
import hashlib
import json
import math

import cv2
import numpy as np

REVISION = "geometry-local-route-v14-shared-graph"
NEIGHBOURS = 2
SMALL_NET_PORTS = 8


def _json(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(type(value).__name__)


def _signature(net):
    ignored = {"id", "mst", "v13_candidate_net", "v14_candidate_net", "inferred_outlet_tee"}
    return json.dumps({k: v for k, v in net.items() if k not in ignored},
                      sort_keys=True, separators=(",", ":"), default=_json)


def _graph_id(net, source):
    return "g" + hashlib.sha256((source+_signature(net)).encode()).hexdigest()[:20]


def _point(point):
    return [round(float(x), 3) for x in point]


def _port_id(symbol, side, anchor):
    data = [symbol, side, _point(anchor)]
    return "port-" + hashlib.sha256(json.dumps(data).encode()).hexdigest()[:20]


def _route_key(candidate):
    # A global graph can differ because of an unused distant tee. That is not
    # another physical hypothesis on this exact local route. Keep its graph
    # provenance separately instead of requesting the same image judgment.
    return json.dumps([candidate.get("a_side"), candidate.get("a_point"),
                       candidate.get("b_side"), candidate.get("b_point"),
                       candidate.get("path", []), candidate.get("tee_gaps", []),
                       candidate.get("signal_gaps", []), candidate.get("endpoint_contacts", {})],
                       sort_keys=True, default=_json)


def _thin(binary):
    """Zhang-Suen thinning, without a contrib OpenCV dependency."""
    image = np.pad((binary != 0).astype(np.uint8), 1)
    for _ in range(128):
        changed = False
        for phase in (0, 1):
            p2, p3, p4 = image[:-2, 1:-1], image[:-2, 2:], image[1:-1, 2:]
            p5, p6, p7 = image[2:, 2:], image[2:, 1:-1], image[2:, :-2]
            p8, p9 = image[1:-1, :-2], image[:-2, :-2]
            neighbours = (p2, p3, p4, p5, p6, p7, p8, p9)
            count = sum(neighbours)
            transitions = sum((a == 0) & (b != 0) for a, b in
                              zip(neighbours, neighbours[1:]+neighbours[:1]))
            if phase == 0:
                condition = (p2*p4*p6 == 0) & (p4*p6*p8 == 0)
            else:
                condition = (p2*p4*p8 == 0) & (p2*p6*p8 == 0)
            remove = ((image[1:-1, 1:-1] != 0) & (count >= 2) & (count <= 6)
                      & (transitions == 1) & condition)
            if remove.any():
                image[1:-1, 1:-1][remove] = 0
                changed = True
        if not changed:
            break
    return image[1:-1, 1:-1]


def observed_line_ends(labels, raw_nets):
    """Enumerate one-pixel ends of retained raw line components.

    Ends at object contacts or existing dash/flange bridges are included and
    explicitly accounted for, rather than deleted.  Small omitted glyph
    components are not promoted to line networks.
    """
    allowed = {int(label) for net in raw_nets for label in net.get("labels", [])}
    if not allowed:
        return []
    skeleton = _thin(np.isin(labels, list(allowed)))
    padded = np.pad(skeleton, 1)
    neighbour_count = sum(padded[1+dy:1+dy+skeleton.shape[0],
                                 1+dx:1+dx+skeleton.shape[1]]
                          for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
    yy, xx = np.nonzero((skeleton != 0) & (neighbour_count == 1))
    owner = {int(label): net["id"] for net in raw_nets for label in net.get("labels", [])}
    result = []
    for y, x in zip(yy.tolist(), xx.tolist()):
        label = int(labels[y, x])
        neighbours = [(x+dx, y+dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                      if (dx or dy) and 0 <= y+dy < labels.shape[0]
                      and 0 <= x+dx < labels.shape[1] and skeleton[y+dy, x+dx]]
        if label == 0 or len(neighbours) != 1:
            continue
        nx, ny = neighbours[0]
        result.append({"id": f"end-{label}-{x}-{y}", "point": [x, y],
                       "label": label, "net": owner[label], "direction": [x-nx, y-ny],
                       "status": "review_needed", "reason": "unaccounted_line_end",
                       "candidate_ids": [], "port_ids": []})
    return result


def build_coverage(raw_nets, raw_labels, graph_records, objects, candidates):
    ports = {}
    for record in graph_records:
        for port in record["net"].get("ports", []):
            i = int(port["obj"])
            symbol = objects[i].get("id", str(i)) if i < len(objects) else str(i)
            anchor = port.get("anchor", port.get("point"))
            if anchor is None:
                continue
            identity = _port_id(symbol, port.get("side"), anchor)
            item = ports.setdefault(identity, {
                "id": identity, "object": symbol, "object_index": i,
                "side": port.get("side"), "point": _point(port.get("point", anchor)),
                "anchor": _point(anchor), "status": "review_needed",
                "reason": "no_verified_attachment", "graph_ids": [],
                "candidate_ids": [], "inferred": bool(port.get("inferred_port_gap")),
            })
            if record["graph_id"] not in item["graph_ids"]:
                item["graph_ids"].append(record["graph_id"])
    for index, candidate in enumerate(candidates):
        candidate_id = f"candidate-{index}"
        for route in [candidate]+candidate.get("route_alternatives", []):
            for end in ("a", "b"):
                i = route[end]
                symbol = objects[i].get("id", str(i)) if i < len(objects) else str(i)
                anchor = route.get(f"{end}_anchor", route.get(f"{end}_point"))
                identity = _port_id(symbol, route.get(f"{end}_side"), anchor) if anchor else None
                if identity in ports and candidate_id not in ports[identity]["candidate_ids"]:
                    ports[identity]["candidate_ids"].append(candidate_id)
    ends = observed_line_ends(raw_labels, raw_nets)
    bridge_anchors = [(point, net["id"]) for net in raw_nets for bridge in net.get("bridges", [])
                      for point in bridge]
    for end in ends:
        p = end["point"]
        for port in ports.values():
            if math.dist(p, port["anchor"]) <= 3:
                end["port_ids"].append(port["id"])
                end["candidate_ids"] = sorted(set(end["candidate_ids"]+port["candidate_ids"]))
                end["reason"] = "object_attachment_unverified"
        if not end["port_ids"] and any(net == end["net"] and math.dist(p, q) <= 3
                                       for q, net in bridge_anchors):
            end["reason"] = "existing_bridge_endpoint_unverified"
    geometry = {"revision": REVISION, "ports": list(ports.values()), "line_ends": ends,
                "gap_hypotheses": [], "summary": {}}
    _summarize(geometry)
    return geometry


def _summarize(geometry):
    for kind in ("ports", "line_ends"):
        for item in geometry[kind]:
            item["state"] = item["status"]
    geometry.setdefault("summary", {}).update({kind: {state: sum(x.get("status") == state for x in geometry[kind])
                                  for state in ("confirmed", "review_needed", "rejected")}
                           for kind in ("ports", "line_ends")})


def flange_plate_gaps(mask, labels, raw_nets, boxes=(), *, text_h=9, exclude=()):
    """Propose an interrupted pipe through a three-bar flange/plate marking.

    The two equal outer transverse bars must carry aligned pipe stubs on their
    outside faces. A narrower isolated central bar, two short empty gaps and
    a longer outgoing arm distinguish this marking from arbitrary proximity.
    Object/table interiors and any competing stroke in either gap block it.
    These records are hypotheses, never connectivity or acceptance evidence.
    """
    if mask.shape != labels.shape or mask.ndim != 2:
        raise ValueError("mask and labels must be matching two-dimensional arrays")
    if not math.isfinite(text_h) or text_h <= 0:
        raise ValueError("text_h must be positive and finite")
    binary = (np.asarray(mask) != 0).astype(np.uint8)
    blocked = np.zeros_like(binary)
    for x0, y0, x1, y1 in list(boxes)+list(exclude):
        blocked[max(0, int(y0)):min(binary.shape[0], int(y1)+1),
                max(0, int(x0)):min(binary.shape[1], int(x1)+1)] = 1
    owner = {int(label): net for net in raw_nets for label in net.get("labels", [])}
    result, seen = [], set()
    minimum = max(5, round(.4*text_h))
    for orientation in ("vertical_pipe", "horizontal_pipe"):
        # Transposed coordinates make every candidate a vertical pipe.
        ink = binary if orientation == "vertical_pipe" else binary.T
        lab = labels if orientation == "vertical_pipe" else labels.T
        block = blocked if orientation == "vertical_pipe" else blocked.T
        opened = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((1, minimum), np.uint8))
        n, _, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
        bars = []
        for i in range(1, n):
            x, y, width, height, area = map(int, stats[i])
            if (minimum <= width <= 2.2*text_h and height <= max(2, .25*text_h)
                    and area >= .9*width*height):
                bars.append((x, y, x+width-1, y+height-1))
        bars.sort(key=lambda b: b[1])
        for index, top in enumerate(bars):
            nearby = [b for b in bars[index+1:] if 1 <= b[1]-top[3] <= 1.4*text_h
                      and abs((b[0]+b[2])-(top[0]+top[2])) <= 4]
            for middle_index, middle in enumerate(nearby):
                for bottom in nearby[middle_index+1:]:
                    if bottom[1] <= middle[3]:
                        continue
                    outer_widths = (top[2]-top[0]+1, bottom[2]-bottom[0]+1)
                    middle_width = middle[2]-middle[0]+1
                    gaps = (middle[1]-top[3]-1, bottom[1]-middle[3]-1)
                    if (max(outer_widths)-min(outer_widths) > 2
                            or not .35*min(outer_widths) <= middle_width <= .8*min(outer_widths)
                            or not all(2 <= gap <= max(4, .65*text_h) for gap in gaps)
                            or abs(gaps[0]-gaps[1]) > 2):
                        continue
                    centre = round((top[0]+top[2]+bottom[0]+bottom[2])/4)
                    if (abs(2*centre-middle[0]-middle[2]) > 2
                            or not top[0] <= centre <= top[2]
                            or not bottom[0] <= centre <= bottom[2]):
                        continue
                    # A single unique axial pipe behind each outer flange.
                    arm_lengths = []
                    for row, direction in ((top[1]-1, -1), (bottom[3]+1, 1)):
                        length = 0
                        for distance in range(max(3, round(2*text_h))):
                            y = row+direction*distance
                            if not 0 <= y < ink.shape[0]:
                                break
                            pixels = np.flatnonzero(ink[y, max(0, centre-1):centre+2])
                            if not len(pixels):
                                break
                            length += 1
                        arm_lengths.append(length)
                    if (min(arm_lengths) < max(3, round(.35*text_h))
                            or max(arm_lengths) < max(7, round(text_h))):
                        continue
                    # No competing ink may occupy either entire axial gap.
                    if (ink[top[3]+1:middle[1], centre-1:centre+2].any()
                            or ink[middle[3]+1:bottom[1], centre-1:centre+2].any()
                            or block[top[1]:bottom[3]+1, centre-1:centre+2].any()):
                        continue
                    top_label, middle_label, bottom_label = (int(lab[y, centre])
                        for y in (top[3], middle[1], bottom[1]))
                    if (not top_label or not middle_label or not bottom_label
                            or len({top_label, middle_label, bottom_label}) != 3
                            or top_label not in owner or bottom_label not in owner
                            or owner[top_label]["id"] == owner[bottom_label]["id"]):
                        continue
                    # The central plate is a compact isolated bar, not part of
                    # a perpendicular wire that happens to cross this axis.
                    ys, xs = np.nonzero(lab == middle_label)
                    if (len(xs) != (middle[2]-middle[0]+1)*(middle[3]-middle[1]+1)
                            or xs.min() != middle[0] or xs.max() != middle[2]
                            or ys.min() != middle[1] or ys.max() != middle[3]):
                        continue
                    a, b = [centre, top[3]], [centre, bottom[1]]
                    marking = [list(top), list(middle), list(bottom)]
                    if orientation == "horizontal_pipe":
                        a, b = a[::-1], b[::-1]
                        marking = [[r[1], r[0], r[3], r[2]] for r in marking]
                    key = tuple(sorted((tuple(a), tuple(b))))
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append({"id": "gap-"+hashlib.sha256(json.dumps(key).encode()).hexdigest()[:20],
                        "reason": "raw_supported_three_bar_plate", "gap_points": [a, b], "path": [a, b],
                        "source_labels": [top_label, middle_label, bottom_label],
                        "source_nets": [owner[top_label]["id"], owner[bottom_label]["id"]],
                        "marking_boxes": marking, "arm_lengths": arm_lengths, "gap_lengths": list(gaps),
                        "requires_original_ink_check": True, "status": "review_needed"})
    return result


def _gap_graphs(raw_nets, labels, gaps):
    lookup = {net["id"]: net for net in raw_nets}
    result = []
    for gap in gaps:
        source = [lookup[i] for i in gap["source_nets"]]
        all_labels = sorted(set(gap["source_labels"]) | {l for n in source for l in n["labels"]})
        bounds = [n["bbox"] for n in source]+gap["marking_boxes"]
        net = {"id": -1, "labels": all_labels,
               "bbox": [min(b[0] for b in bounds), min(b[1] for b in bounds),
                        max(b[2] for b in bounds), max(b[3] for b in bounds)],
               "ports": copy.deepcopy([p for n in source for p in n["ports"]]),
               "bridges": copy.deepcopy([b for n in source for b in n.get("bridges", [])])+[gap["gap_points"]],
               "bridge_paths": copy.deepcopy([b for n in source for b in n.get("bridge_paths", [])])
                               +[{"endpoints": gap["gap_points"], "path": gap["path"]}],
               "dashed": any(n.get("dashed") for n in source), "signal_gap_proposals": [copy.deepcopy(gap)]}
        result.append({"net": net, "labels": labels, "source": "v14_gap_hypothesis",
                       "graph_id": _graph_id(net, "v14_gap_hypothesis")})
    return result


def finalize_coverage(geometry, candidates, objects, shared_graph=None):
    """Resolve contacts only from explicit endpoint/shared-graph evidence.

    A rejected full path does not prove that its endpoints have no connection;
    those ports stay review_needed.  An isolated contact is never discarded.
    """
    confirmed, rejected = set(), set()
    for candidate in candidates:
        for route in [candidate]+candidate.get("route_alternatives", []):
            endpoint_checks = route.get("endpoint_checks", {})
            for side in ("a", "b"):
                obj = route.get(side)
                if not isinstance(obj, int) or not 0 <= obj < len(objects):
                    continue
                anchor = route.get(f"{side}_anchor", route.get(f"{side}_point"))
                if not anchor:
                    continue
                key = _port_id(objects[obj].get("id", str(obj)), route.get(f"{side}_side"), anchor)
                if route.get("accepted") or route.get("shared_graph_accepted"):
                    confirmed.add(key)
                check = endpoint_checks.get(str(obj), endpoint_checks.get(obj, {}))
                if isinstance(check, dict) and check.get("status") == "rejected":
                    rejected.add(key)
    for entity in (shared_graph or {}).get("entities", []):
        if entity.get("kind") not in {"port_attachment", "attachment"}:
            continue
        identity = entity.get("coverage_port_id")
        detail = entity.get("geometry", {})
        if (not identity and isinstance(detail, dict) and detail.get("object") is not None
                and detail.get("side") is not None and detail.get("line_anchor") is not None):
            identity = _port_id(detail["object"], detail["side"], detail["line_anchor"])
        identities = {identity} if identity else set()
        identities.update(entity.get("coverage_port_ids", []))
        if entity.get("state", entity.get("status")) == "confirmed":
            confirmed.update(identities)
        elif entity.get("state", entity.get("status")) == "rejected":
            rejected.update(identities)
    for port in geometry.get("ports", []):
        if port["id"] in confirmed:
            port.update(status="confirmed", reason="verified_object_attachment")
        elif port["id"] in rejected:
            port.update(status="rejected", reason="explicitly_rejected_attachment")
    states = {p["id"]: p["status"] for p in geometry.get("ports", [])}
    for end in geometry.get("line_ends", []):
        statuses = [states[p] for p in end.get("port_ids", []) if p in states]
        if "confirmed" in statuses:
            end.update(status="confirmed", reason="verified_object_attachment")
        elif statuses and all(state == "rejected" for state in statuses):
            end.update(status="rejected", reason="explicitly_rejected_attachment")
    # A dash endpoint along an independently confirmed drawn segment is
    # accounted for even when a different part of the full route is pending.
    # Require exact collinear containment; no nearby crossing is snapped in.
    ends = geometry.get("line_ends", [])
    positions = np.asarray([end["point"] for end in ends], float)
    if len(ends):
        for entity in (shared_graph or {}).get("entities", []):
            if (entity.get("state", entity.get("status")) != "confirmed"
                    or entity.get("kind") not in {"segment", "junction"}):
                continue
            path = entity.get("geometry", {}).get("path", [])
            for a, b in zip(path, path[1:]):
                a, b = np.asarray(a, float), np.asarray(b, float)
                vector = b-a
                length_squared = float(vector @ vector)
                if length_squared == 0:
                    continue
                offsets = positions-a
                cross = offsets[:, 0]*vector[1]-offsets[:, 1]*vector[0]
                dot = offsets @ vector
                covered = np.flatnonzero((np.abs(cross) <= 1e-6)
                                         & (dot >= 0) & (dot <= length_squared))
                for index in covered.tolist():
                    if ends[index]["status"] == "review_needed":
                        ends[index].update(status="confirmed", reason="verified_drawn_segment",
                                           supporting_entity=entity.get("id"))
    _summarize(geometry)
    return geometry


def _candidate(extractor, ctx, objects, record, a, b):
    if a["obj"] == b["obj"]:
        return None
    if a["obj"] > b["obj"]:
        a, b = b, a
    net, labels = record["net"], record["labels"]
    path = extractor.CV.wire_path(labels, net, a["anchor"], b["anchor"])
    if not path:
        return None
    candidate = {
        "a": a["obj"], "a_side": a["side"], "a_point": copy.deepcopy(a["point"]),
        "a_anchor": copy.deepcopy(a["anchor"]),
        "b": b["obj"], "b_side": b["side"], "b_point": copy.deepcopy(b["point"]),
        "b_anchor": copy.deepcopy(b["anchor"]), "net": net["id"], "path": path,
        "length": sum(abs(p[0]-q[0])+abs(p[1]-q[1]) for p, q in zip(path, path[1:])),
        "bridges": len(net.get("bridges", [])), "dashed": net.get("dashed", False),
        "mst": len(net.get("ports", [])) > SMALL_NET_PORTS,
        "graph_id": record["graph_id"], "candidate_source": "v14_port_coverage_neighbour",
        "candidate_net_source": record["source"], "candidate_revision": REVISION,
        "requires_shared_graph_verification": True,
        "tee_gaps": [copy.deepcopy(t) for t in getattr(ctx, "port_tee_proposals", [])
                     if record["source"] == "inferred_outlet_tee"
                     and extractor.CG.uses_bridge(path, t["path"], ctx.bw_wire)],
    }
    if net.get("signal_gap_proposals"):
        candidate["signal_gaps"] = [extractor.SIG.route_used_gap(p, path, ctx.bw_wire)
                                    for p in net["signal_gap_proposals"]
                                    if extractor.CG.uses_bridge(path, p["path"], ctx.bw_wire)
                                    or p.get("symbol") in {objects[a["obj"]].get("id"),
                                                         objects[b["obj"]].get("id")}]
        candidate["endpoint_contacts"] = {p["obj"]: copy.deepcopy(p["inferred_port_gap"])
                                           for p in (a, b) if p.get("inferred_port_gap")}
    return candidate


def install(extractor):
    """Observe original geometry and retain bounded alternatives in one worker."""
    if getattr(extractor.relation_candidates, "_v14_coverage", False):
        return
    original = extractor.relation_candidates

    @wraps(original)
    def supplemented(ctx, objects, diagram_boxes):
        if ctx.kind != "pid":
            return original(ctx, objects, diagram_boxes)
        wire_nets, augment = extractor.CV.wire_nets, extractor.SIG.augment_nets
        records, raw_nets, raw_labels = [], [], None

        def capture(nets, labels, source):
            records.extend({"net": copy.deepcopy(net), "labels": labels,
                            "source": source, "graph_id": _graph_id(net, source)} for net in nets)

        def observed_wire(*args, **kwargs):
            nonlocal raw_nets, raw_labels
            nets, labels = wire_nets(*args, **kwargs)
            source = "original_wire" if raw_labels is None else "inferred_outlet_tee"
            if raw_labels is None:
                raw_nets, raw_labels = copy.deepcopy(nets), labels
            capture(nets, labels, source)
            return nets, labels

        def observed_augment(nets, labels, *args, **kwargs):
            result = augment(nets, labels, *args, **kwargs)
            capture(result, labels, "inferred_signal")
            return result

        extractor.CV.wire_nets, extractor.SIG.augment_nets = observed_wire, observed_augment
        try:
            primary, nets = original(ctx, objects, diagram_boxes)
        finally:
            extractor.CV.wire_nets, extractor.SIG.augment_nets = wire_nets, augment
        if raw_labels is None:
            return primary, nets
        boxes = [extractor.erase_box(o, ctx.k["erase_ext"]) for o in objects]
        gaps = flange_plate_gaps((raw_labels != 0).astype(np.uint8), raw_labels,
                                 raw_nets, boxes, text_h=ctx.text_h,
                                 exclude=getattr(ctx, "tables", []))
        records.extend(_gap_graphs(raw_nets, raw_labels, gaps))
        candidates, nets = list(primary), list(nets)
        signatures = {_signature(n): n["id"] for n in nets}
        used = set()
        unique_records = []
        next_id = max((n["id"] for n in nets), default=-1)+1
        for record in records:
            if record["graph_id"] in used:
                continue
            used.add(record["graph_id"])
            net = record["net"]
            signature = _signature(net)
            if signature in signatures:
                net["id"] = signatures[signature]
            else:
                net["id"] = next_id
                next_id += 1
                net["v14_candidate_net"] = True
                nets.append(copy.deepcopy(net))
                signatures[signature] = net["id"]
            unique_records.append(record)
        by_pair = {tuple(sorted((c["a"], c["b"]))): c for c in candidates}
        retained, added = 0, 0
        for record in unique_records:
            net, labels = record["net"], record["labels"]
            ports = net.get("ports", [])
            if len(ports) <= SMALL_NET_PORTS:
                pairs = [(a, b) for i, a in enumerate(ports) for b in ports[i+1:]]
            else:
                pairs = extractor.mst_port_pairs(ports, labels, net, neighbours=NEIGHBOURS)
            for a, b in pairs:
                route = _candidate(extractor, ctx, objects, record, a, b)
                if route is None:
                    continue
                pair = route["a"], route["b"]
                if pair not in by_pair:
                    candidates.append(route)
                    by_pair[pair] = route
                    added += 1
                    continue
                main = by_pair[pair]
                # Same primary geometry is not a meaningful alternative. The
                # anchor fields are used only for coverage bookkeeping.
                identical = _route_key(main) == _route_key(route)
                if identical:
                    main.setdefault("a_anchor", route["a_anchor"])
                    main.setdefault("b_anchor", route["b_anchor"])
                    main.setdefault("graph_id", route["graph_id"])
                    provenance = main.setdefault("equivalent_graph_ids", [])
                    if route["graph_id"] not in provenance:
                        provenance.append(route["graph_id"])
                    continue
                alternatives = main.setdefault("route_alternatives", [])
                key = _route_key(route)
                equivalent = next((r for r in alternatives if _route_key(r) == key), None)
                if equivalent is None:
                    alternatives.append(route)
                    retained += 1
                else:
                    provenance = equivalent.setdefault("equivalent_graph_ids", [])
                    if route["graph_id"] not in provenance:
                        provenance.append(route["graph_id"])
        ctx.connection_geometry_runtime = {"raw_nets": raw_nets, "raw_labels": raw_labels,
                                           "graph_records": unique_records}
        ctx.connection_geometry = build_coverage(raw_nets, raw_labels, unique_records,
                                                  objects, candidates)
        ctx.connection_geometry["gap_hypotheses"] = gaps
        for gap in gaps:
            gap["state"] = gap["status"]
        ctx.connection_geometry["summary"].update({"original_candidates": len(primary),
            "added_candidates": added, "retained_route_alternatives": retained,
            "physical_graphs": len(unique_records), "neighbours": NEIGHBOURS})
        return candidates, nets

    supplemented._v14_coverage = True
    extractor.relation_candidates = supplemented
