"""Shared physical line/port evidence after the frozen connection pipeline.

This module is deliberately independent of an object's pairwise confidence.
It shares judgments only for identical raw-image geometry (or exact collinear
containment of a positively checked stroke), never by object identity alone.
Every unanswered or contradictory local entity remains in the exported graph.
Model choices select code-created anchors; they never create coordinates.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from collections import defaultdict

import cv2
import numpy as np

REVISION = "geometry-local-route-v14-shared-graph"
MAX_ENTITY_REVIEWS = 160
PORT_REASONS = {"instrument_terminal_port", "inline_equipment_port_flange_gap"}


def paired_support(values, threshold=.60):
    return (len(values) == 2 and all(type(p) in (float, int) and math.isfinite(p)
                                   and .5 <= p <= 1 for p in values)
            and sum(values) / 2 >= threshold)


def _valid_pair(values):
    return (isinstance(values, (tuple, list)) and len(values) == 2
            and all(type(p) in (int, float) and math.isfinite(p) and 0 <= p <= 1 for p in values))


def _point(point):
    return [int(v) if float(v).is_integer() else round(float(v), 6) for v in point]


def canonical_path(path):
    """Reverse-independent exact geometry; no proximity snapping occurs here."""
    clean = []
    for point in path or []:
        point = _point(point)
        if not clean or point != clean[-1]:
            clean.append(point)
    # Remove a vertex only if it lies *exactly* between its neighbours.
    index = 1
    while index < len(clean) - 1:
        a, p, b = clean[index - 1:index + 2]
        if _on_segment(p, a, b):
            clean.pop(index)
        else:
            index += 1
    return min(clean, list(reversed(clean)))


def _on_segment(point, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    return (abs((point[0] - a[0]) * dy - (point[1] - a[1]) * dx) <= 1e-7
            and min(a[0], b[0]) <= point[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= point[1] <= max(a[1], b[1]))


def entity_id(kind, geometry):
    payload = json.dumps({"kind": kind, "geometry": geometry}, sort_keys=True, separators=(",", ":"))
    return "g" + hashlib.sha256(payload.encode()).hexdigest()[:20]


def _evidence(key, check, source):
    values = check.get("p_yes", [])
    return {"key": str(key), "source": source,
            "p_yes": list(values) if isinstance(values, (list, tuple)) else [],
            "confidence": sum(values) / 2 if _valid_pair(values) else None,
            "bbox": copy.deepcopy(check.get("bbox")),
            "rechecks": check.get("rechecks"),
            "marker_geometry": check.get("marker_geometry", check.get("marker_style")),
            "context_review": check.get("context_review"),
            "body_contact": copy.deepcopy(check.get("body_contact")),
            "original_point": copy.deepcopy(check.get("original_point")),
            "raw_contact_path": copy.deepcopy(check.get("raw_contact_path")),
            "contact_reason": check.get("reason")}


def classify_entity(evidence, adjudication=None, threshold=.60, reject=.15):
    """Reconcile evidence explicitly; an optimistic maximum is never a vote.

    A finite focused paired judgment may resolve moderate crop ambiguity.
    Earlier strong negative evidence or a colour-order disagreement cannot be
    silently superseded by that new positive judgment.
    """
    valid = [e for e in evidence if _valid_pair(e.get("p_yes"))]
    positive = [e for e in valid if paired_support(e["p_yes"], threshold)]
    negative = [e for e in valid if paired_support([1 - p for p in e["p_yes"]], threshold)]
    strong_negative = [e for e in valid if sum(e["p_yes"]) / 2 < reject]
    order_conflict = [e for e in valid if min(e["p_yes"]) < .5 < max(e["p_yes"])]
    reasons = []
    if positive and negative:
        reasons.append("conflicting_crop_judgments")
    if order_conflict:
        reasons.append("colour_order_disagreement")
    if strong_negative and positive:
        reasons.append("strong_conflicting_negative")
    if adjudication and _valid_pair(adjudication.get("p_yes")):
        fresh = adjudication["p_yes"]
        if paired_support(fresh, threshold) and not strong_negative and not order_conflict:
            return "confirmed", reasons + (["focused_adjudication_reconciles_crop_ambiguity"]
                                           if negative else ["focused_paired_support"])
        if paired_support([1 - p for p in fresh], threshold) and not positive and not order_conflict:
            return "rejected", ["focused_paired_rejection"]
        return "review_needed", reasons + ["focused_adjudication_unresolved"]
    if reasons:
        return "review_needed", reasons
    if positive:
        return "confirmed", ["consistent_shared_paired_support"]
    if strong_negative:
        return "rejected", ["strong_paired_rejection"]
    if not valid:
        return "review_needed", ["missing_paired_answer"]
    return "review_needed", ["local_probability_unresolved"]


def _refresh(entity, extractor):
    entity["state"], entity["reasons"] = classify_entity(
        entity["evidence"], entity.get("adjudication"),
        getattr(extractor, "LOCAL_RECOVER", .60), getattr(extractor, "LOCAL_REJECT", .15))
    positive = [e["confidence"] for e in entity["evidence"] if paired_support(e.get("p_yes", []))]
    fresh = entity.get("adjudication", {}).get("p_yes", [])
    if paired_support(fresh):
        positive.append(sum(fresh) / 2)
    entity["confidence"] = min(positive) if entity["state"] == "confirmed" and positive else None
    if entity["kind"] == "attachment" and entity.get("detail", {}).get("contact_geometry_status") == "unobserved":
        entity["state"], entity["confidence"] = "review_needed", None
        entity["reasons"] = list(dict.fromkeys(entity["reasons"] + ["actual_body_contact_unresolved"]))


def _new_entity(kind, geometry, detail):
    return {"id": entity_id(kind, geometry), "kind": kind, "geometry": geometry,
            "path": copy.deepcopy(detail.get("path", [])), "detail": copy.deepcopy(detail),
            "evidence": [], "state": "review_needed", "reasons": ["missing_paired_answer"],
            "candidate_indices": []}


def _route_entity(check):
    path = canonical_path(check.get("path", []))
    kind = "segment" if check.get("kind", "span") == "span" and len(path) == 2 else "junction"
    if check.get("kind") in {"signal_gap", "outlet_tee_gap"}:
        kind = "gap"
    geometry = {"path": path}
    if kind == "gap":
        # Similar outer markers do not make different inferred gaps identical.
        geometry["core_path"] = canonical_path(check.get("original_gap_path", path))
        geometry["reason"] = check.get("reason")
    return kind, geometry


def _box(extractor, obj, ctx):
    return list(extractor.erase_box(obj, ctx.k.get("erase_ext", False)))


def observed_body_contact(page, box, outside_anchor, side, text_h=9, preferred=None):
    """Locate a finite raw stem at the selected side, never a nearby other arm.

    A geometric projection is only a candidate: its boundary pixel and short
    outside stem must exist in the original image. No symbol box or route is
    changed. Explicit flange/dash geometry remains a separate proposal below.
    """
    if side not in {"left", "right", "top", "bottom"}:
        return None
    x0, y0, x1, y1 = map(int, box)
    ax, ay = map(round, outside_anchor)
    h, w = page.shape[:2]
    if not 0 <= ax < w or not 0 <= ay < h:
        return None
    direction = {"left": (-1, 0), "right": (1, 0), "top": (0, -1), "bottom": (0, 1)}[side]
    dx, dy = direction
    fixed = x0 if side == "left" else x1 if side == "right" else y0 if side == "top" else y1
    projected = [fixed, ay] if dx else [ax, fixed]
    distance = (ax - projected[0]) * dx + (ay - projected[1]) * dy
    if not 0 <= distance <= max(4, round(2 * text_h)):
        return None
    candidates = []
    if preferred is not None:
        px, py = map(round, preferred)
        if (dx and px == fixed and abs(py - ay) <= 1) or (dy and py == fixed and abs(px - ax) <= 1):
            candidates.append([px, py])
    # A fresh generic contact never shifts onto a neighbouring parallel arm.
    # A different transverse pixel is permitted only as an already supplied
    # finite preferred contact, not as a proximity search.
    candidates.append(projected)
    candidates = list(dict.fromkeys(tuple(p) for p in candidates))
    observed = []
    for contact in candidates:
        cx, cy = contact
        if not (x0 <= cx <= x1 and y0 <= cy <= y1 and 0 <= cx < w and 0 <= cy < h):
            continue
        if page[cy, cx] >= 200:
            continue
        # Marker separation requires a real outside arm when the saved anchor
        # is itself at/one pixel beyond the body outline.
        marker_distance = max(4, round(distance))
        marker = [cx + dx * marker_distance, cy + dy * marker_distance]
        if not (0 <= marker[0] < w and 0 <= marker[1] < h):
            continue
        samples = [int(page[cy + dy * step, cx + dx * step]) for step in range(marker_distance + 1)]
        support = sum(p < 200 for p in samples) / len(samples)
        if support < .65 or page[marker[1], marker[0]] >= 200:
            continue
        # A one-pixel adjustment may follow the same observed stroke thickness;
        # equally plausible opposite transverse shifts cannot pick another arm.
        observed.append((abs((cy - ay) if dx else (cx - ax)), support,
                         list(contact), marker, samples))
    if not observed:
        return None
    closest = min(row[0] for row in observed)
    finalists = [row for row in observed if row[0] == closest]
    if closest and len({tuple(row[2]) for row in finalists}) > 1:
        return None
    _, support, contact, marker, samples = max(finalists, key=lambda row: row[1])
    return {"body_contact": contact, "outside_marker": marker,
            "raw_contact_path": [contact, list(outside_anchor)],
            "contact_type": "dashed_stem" if any(p >= 200 for p in samples) else "straight_stem",
            "contact_geometry_status": "observed", "raw_stem_support": round(support, 4),
            "contact_geometry_source": "same_side_observed_raw_boundary_and_stem"}


def _attachment(extractor, ctx, objs, rel, position):
    index = rel["a" if position == 0 else "b"]
    line_anchor = _point(rel["path"][0 if position == 0 else -1])
    contacts = rel.get("endpoint_contacts", {})
    contact = contacts.get(index, contacts.get(str(index), {}))
    box = list(objs[index]["bbox"])
    side = rel.get("a_side" if position == 0 else "b_side")
    preferred = rel.get("a_point" if position == 0 else "b_point")
    # A previous finite contact recheck contains actual geometry, even when its
    # model probability was low. Reuse its geometry without turning it into yes.
    prior_contact_keys = []
    for key, check in getattr(ctx, "endpoint_checks", {}).items():
        if (check.get("body_contact") and list(check.get("bbox", [])) in [box, _box(extractor, objs[index], ctx)]
                and list(check.get("original_point", [])) == line_anchor
                and check.get("side", side) == side):
            contact = {**copy.deepcopy(check), **contact}
            prior_contact_keys.append(str(key))
    signal = getattr(extractor, "SIG", None)
    if not contact.get("body_contact") and signal and hasattr(signal, "endpoint_contact"):
        proposed = signal.endpoint_contact(ctx.page, box, line_anchor, ctx.text_h)
        if proposed and proposed.get("side") == side:
            # This existing geometry helper requires a finite central-side
            # body pixel and raw short-stem support, allowing raster dash gaps.
            # It proposes coordinates only; the Decision Model still judges it.
            contact = {**copy.deepcopy(proposed), **contact,
                       "geometry_source": "fresh_finite_same_side_raw_contact_proposal"}
    point = _point(contact.get("body_contact", preferred or line_anchor))
    observed = observed_body_contact(ctx.page, box, line_anchor, side, ctx.text_h, point)
    explicit = contact.get("body_contact") is not None and contact.get("raw_contact_path")
    if explicit:
        # The upstream finite geometry includes flange/dash gaps that a plain
        # solid-stem density check must not misinterpret. Both contact and arm
        # still have to be observed, finite, on the selected side of this body.
        px, py = map(round, point)
        h, w = ctx.page.shape[:2]
        reason = contact.get("reason", "")
        expected = {"left": box[0], "right": box[2], "top": box[1], "bottom": box[3]}.get(side)
        boundary = px if side in {"left", "right"} else py
        direction = {"left": (-1, 0), "right": (1, 0), "top": (0, -1), "bottom": (0, 1)}.get(side, (0, 0))
        outward = sum((line_anchor[j] - point[j]) * direction[j] for j in (0, 1))
        transverse = abs((line_anchor[1] - py) if direction[0] else (line_anchor[0] - px))
        if (expected is not None and abs(boundary - expected) <= 1 and math.dist(point, line_anchor) > 1
                and math.dist(point, line_anchor) <= max(4, 2 * ctx.text_h)
                and outward > 0 and transverse <= 1 and box[0] <= px <= box[2] and box[1] <= py <= box[3]
                and 0 <= px < w and 0 <= py < h and ctx.page[py, px] < 200):
            length = max(abs(line_anchor[0] - px), abs(line_anchor[1] - py), 1)
            sample_points = [[round(px + (line_anchor[0] - px) * step / length),
                              round(py + (line_anchor[1] - py) * step / length)]
                             for step in range(round(length) + 1)]
            raster_gaps = any(ctx.page[y, x] >= 200 for x, y in sample_points
                              if 0 <= x < w and 0 <= y < h)
            observed = {"body_contact": point, "outside_marker": line_anchor,
                        "raw_contact_path": copy.deepcopy(contact["raw_contact_path"]),
                        "contact_type": "flange" if "flange" in reason else
                                        "dashed_stem" if "instrument_terminal" in reason or raster_gaps else "straight_stem",
                        "contact_geometry_status": "observed",
                        "contact_geometry_source": contact.get("geometry_source", "existing_finite_raw_contact_proposal"),
                        "contact_reason": reason}
    if observed:
        point = _point(observed["body_contact"])
    geometry = {"object": objs[index]["id"], "point": point, "line_anchor": line_anchor,
                "side": side}
    detail = {"bbox": box, "point": point, "line_anchor": line_anchor,
              "object": objs[index]["id"], "side": geometry["side"],
              "raw_contact_path": copy.deepcopy(contact.get("raw_contact_path")),
              "path": [point, line_anchor], "prior_contact_keys": prior_contact_keys,
              "contact_geometry_status": "unobserved", "contact_type": "unresolved"}
    if observed:
        detail.update(observed)
    return geometry, detail


def _record_entities(extractor, ctx, objs, rels):
    registry, check_entities, routes = {}, {}, []
    checks = getattr(ctx, "route_checkpoints", {})
    for key, check in checks.items():
        if len(check.get("path", [])) < 2:
            continue
        kind, geometry = _route_entity(check)
        identity = entity_id(kind, geometry)
        entity = registry.setdefault(identity, _new_entity(kind, geometry, check))
        entity["evidence"].append(_evidence(key, check, "existing_route_checkpoint"))
        check_entities[key] = identity
    endpoints = getattr(ctx, "endpoint_checks", {})
    for index, rel in enumerate(rels):
        path = rel.get("path", [])
        required, attachment_ids = [], []
        active = [k for k in rel.get("checkpoint_keys", []) if k in checks]
        # These duplicate outside-point checks do not observe the actual body.
        # They remain in the graph, while actual attachment checks become
        # mandatory for graph recovery instead of treating their omission as yes.
        if any(checks[k].get("reason") not in PORT_REASONS for k in active):
            active = [k for k in active if checks[k].get("reason") not in PORT_REASONS]
        for key in active:
            if key in check_entities:
                required.append(check_entities[key])
        if not active and len(path) >= 2:
            # New finite alternatives without K5 records are explicit unknowns.
            cg = getattr(extractor, "CG", None)
            if cg and hasattr(cg, "checkpoints"):
                protected = [point for gap in rel.get("signal_gaps", [])
                             if gap.get("reason") == "raw_supported_dashed_elbow"
                             for point in gap.get("path", [])[1:-1]]
                details = cg.checkpoints(path, max_span=max(100, round(ctx.text_h * 20)), protected_turns=protected)
                if rel.get("crossing_details") and hasattr(cg, "partition_crossing_spans"):
                    details = cg.partition_crossing_spans(details, rel["crossing_details"])
            else:
                details = [{"kind": "span", "path": [a, b], "a": a, "b": b}
                           for a, b in zip(path, path[1:]) if a != b]
                details += [{"kind": "junction", "path": [a, b, c], "a": a, "b": c}
                            for a, b, c in zip(path, path[1:], path[2:]) if not _on_segment(b, a, c)]
            if not details:
                precise = canonical_path(path)
                details = [{"kind": "span" if len(precise) == 2 else "junction", "path": precise,
                            "a": precise[0], "b": precise[-1]}]
            for gap in rel.get("signal_gaps", []) + rel.get("tee_gaps", []):
                if gap.get("reason") in PORT_REASONS:
                    continue  # Actual attachments below are still mandatory.
                signal = getattr(extractor, "SIG", None)
                detail = signal.review_detail(ctx.page, gap, ctx.text_h, symbols=objs) if signal else None
                if not detail:
                    gap_path = gap.get("path", gap.get("gap_points", []))
                    if len(gap_path) >= 2:
                        detail = {**copy.deepcopy(gap), "kind": "signal_gap", "path": gap_path,
                                  "a": gap_path[0], "b": gap_path[-1],
                                  "original_gap_path": gap_path}
                if detail:
                    details.append(detail)
            for detail in details:
                kind, geometry = _route_entity(detail)
                identity = entity_id(kind, geometry)
                registry.setdefault(identity, _new_entity(kind, geometry, detail))
                required.append(identity)
        if len(path) >= 2:
            for position in (0, 1):
                geometry, detail = _attachment(extractor, ctx, objs, rel, position)
                identity = entity_id("attachment", geometry)
                entity = registry.setdefault(identity, _new_entity("attachment", geometry, detail))
                from .connection_coverage import _port_id
                coverage_anchor = rel.get("a_anchor" if position == 0 else "b_anchor", geometry["line_anchor"])
                coverage_id = _port_id(geometry["object"], geometry["side"], coverage_anchor)
                entity.setdefault("coverage_port_id", coverage_id)
                if coverage_id not in entity.setdefault("coverage_port_ids", []):
                    entity["coverage_port_ids"].append(coverage_id)
                existing = {e["key"] for e in entity["evidence"]}
                for key, check in endpoints.items():
                    boxes = [detail["bbox"], _box(extractor, objs[rel["a" if position == 0 else "b"]], ctx)]
                    same_point = list(check.get("point", [])) in [detail["point"], detail["line_anchor"]]
                    finite_contact = (list(check.get("body_contact", [])) == detail["point"]
                                      and list(check.get("original_point", [])) == detail["line_anchor"])
                    if list(check.get("bbox", [])) in boxes and (same_point or finite_contact):
                        if str(key) not in existing:
                            entity["evidence"].append(_evidence(key, check, "existing_endpoint_checkpoint"))
                attachment_ids.append(identity)
        required = list(dict.fromkeys(required + attachment_ids))
        for identity in required:
            registry[identity]["candidate_indices"].append(index)
        routes.append({"index": index, "a": objs[rel["a"]]["id"], "b": objs[rel["b"]]["id"],
                       "parent_index": rel.get("_graph_parent_index", index),
                       "alternative_index": rel.get("_graph_alternative_index"),
                       "path": copy.deepcopy(path), "entity_ids": required,
                       "attachment_ids": attachment_ids, "accepted": bool(rel.get("accepted")),
                       "baseline_accepted": bool(rel.get("accepted")),
                       "candidate_source": rel.get("candidate_source"), "net": rel.get("net"),
                       "route_alternatives": copy.deepcopy(rel.get("route_alternatives", [])),
                       "state": "confirmed" if rel.get("accepted") else "review_needed"})
    # A positive check on an exact collinear super-segment also supports a
    # contained primitive. Nearby parallel strokes and corner shortcuts do not.
    supported = [e for e in registry.values() if e["kind"] in {"segment", "junction"}
                 and classify_entity(e["evidence"])[0] == "confirmed"]
    for entity in registry.values():
        if entity["kind"] != "segment":
            continue
        a, b = entity["geometry"]["path"]
        for other in supported:
            if other["id"] == entity["id"]:
                continue
            if any(_on_segment(a, c, d) and _on_segment(b, c, d)
                   for c, d in zip(other["geometry"]["path"], other["geometry"]["path"][1:])):
                for evidence in other["evidence"]:
                    if paired_support(evidence.get("p_yes", [])):
                        entity["evidence"].append({**copy.deepcopy(evidence),
                                                   "source": "exact_contained_physical_stroke",
                                                   "supporting_entity": other["id"]})
        _refresh(entity, extractor)
    for entity in registry.values():
        _refresh(entity, extractor)
    return registry, routes


def _eligible(extractor, ctx, objs, rel, route):
    if rel.get("accepted") or rel.get("blockers") or len(rel.get("path", [])) < 2:
        return False
    if not _valid_pair(rel.get("k3", [])) and not rel.get("_graph_pair_answer_present"):
        return False
    geometry = getattr(extractor, "CG", None)
    if geometry is not None and geometry.intervening_symbols(rel["path"], objs, {rel["a"], rel["b"]}):
        route["reasons"] = ["intervening_symbol"]
        return False
    return bool(route["entity_ids"])


def _expand_alternatives(objs, rels):
    """Keep each retained path independent while retaining its real pair judge."""
    work = list(rels)
    mapping = defaultdict(list)
    lookup = {obj["id"]: index for index, obj in enumerate(objs)}
    for parent_index, primary in enumerate(rels):
        for alternative_index, alternative in enumerate(primary.get("route_alternatives", [])):
            route = copy.deepcopy(alternative)
            # Missing pair endpoints may inherit *identities* only, not answers.
            for end in ("a", "b"):
                value = route.get(end, primary[end])
                route[end] = lookup.get(value, value) if isinstance(value, str) else value
            valid_objects = (all(isinstance(route[end], int) and 0 <= route[end] < len(objs) for end in ("a", "b"))
                             and {route["a"], route["b"]} == {primary["a"], primary["b"]})
            if not valid_objects:
                # Root creates alternatives from code anchors, so malformed
                # endpoints are exceptional. Keep that invalid path visible.
                route["a"], route["b"] = primary["a"], primary["b"]
                route["blockers"] = ["invalid_alternative_endpoints"]
            route["accepted"] = False
            route["decision"] = "retained_physical_route_alternative"
            route["_graph_parent_index"] = parent_index
            route["_graph_alternative_index"] = alternative_index
            route["_graph_pair_answer_present"] = _valid_pair(primary.get("k3", [])) and not primary.get("accepted")
            route["global_pair_evidence_reference"] = {
                "parent_index": parent_index, "p_yes": copy.deepcopy(primary.get("k3", [])),
                "source": "actual_primary_pair_judgment_not_a_new_alternative_answer"}
            route.setdefault("candidate_source", "v14_retained_route_alternative")
            # An alternative has never received an independent K3 question.
            # Local entities plus both actual ports are mandatory for recovery.
            route.pop("k3", None)
            mapping[parent_index].append(len(work))
            work.append(route)
    return work, mapping


def raw_local_view(extractor, page, detail, colors, labels=None):
    """One original image, with all original nonwhite pixels restored exactly."""
    points = detail.get("anchors", [detail.get("a"), detail.get("b")])
    points = [p for p in points if p is not None]
    if detail.get("point") is not None:
        points = [detail["point"], detail.get("outside_marker", detail.get("line_anchor", detail["point"]))]
    coordinates = list(points) + [p for p in detail.get("path", [])]
    box = detail.get("bbox") if detail.get("object") else None
    if box:
        coordinates += [[box[0], box[1]], [box[2], box[3]]]
    xs, ys = zip(*coordinates)
    h, w = page.shape[:2]
    pad = int(detail.get("view_pad", 24))
    rect = (max(0, math.floor(min(xs)) - pad), max(0, math.floor(min(ys)) - pad),
            min(w, math.ceil(max(xs)) + pad + 1), min(h, math.ceil(max(ys)) + pad + 1))
    scale = extractor.fit_scale(rect[2] - rect[0], rect[3] - rect[1], 768, up=6.0)
    view = extractor.ScaledView(page, rect, scale)
    raw = extractor.V.crop(page, *rect)
    raw = cv2.resize(raw, (view.img.shape[1], view.img.shape[0]), interpolation=cv2.INTER_NEAREST)
    original = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
    view.img = original.copy()
    radius = max(6, round(3 * view.s))
    for index, point in enumerate(points):
        x, y = view.p(*point)
        color = colors[index % len(colors)]
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx, cy = x + sx * radius, y + sy * radius
                cv2.line(view.img, (cx, cy), (cx + sx * 6, cy), color, 2, cv2.LINE_8)
                cv2.line(view.img, (cx, cy), (cx, cy + sy * 6), color, 2, cv2.LINE_8)
        if labels:
            cv2.putText(view.img, labels[index], (x + radius + 9, y - radius - 3),
                        cv2.FONT_HERSHEY_SIMPLEX, .65, color, 1, cv2.LINE_AA)
    if box:
        p, q = view.p(box[0] - 2, box[1] - 2), view.p(box[2] + 2, box[3] + 2)
        cv2.rectangle(view.img, p, q, (90, 130, 70), 1, cv2.LINE_8)
    view.img[raw < 255] = original[raw < 255]
    return view.finish()


def competing_attachment_groups(entities, text_h=9):
    """Finite alternatives at one exact body port, with distinct parallel arms.

    Different sides/contacts are distinct ports, not a categorical competition.
    A common stem that branches away from the body also does not qualify.
    """
    groups = defaultdict(list)
    for entity in entities:
        if entity["kind"] != "attachment":
            continue
        if entity.get("detail", {}).get("contact_geometry_status") == "unobserved":
            continue
        geometry = entity["geometry"]
        groups[(geometry["object"], tuple(geometry["point"]), geometry.get("side"))].append(entity)
    result = []
    for alternatives in groups.values():
        if len(alternatives) != 2:
            continue
        a, b = alternatives
        ga, gb = a["geometry"], b["geometry"]
        gap = math.dist(ga["line_anchor"], gb["line_anchor"])
        if not 3 <= gap <= max(6, 2 * text_h):
            continue
        contact = ga["point"]
        vectors = [[g["line_anchor"][j] - contact[j] for j in (0, 1)] for g in (ga, gb)]
        # Only two nearby arms directed to the same side may be competitors.
        if not all(math.hypot(*v) > 3 for v in vectors):
            continue
        dot = sum(vectors[0][j] * vectors[1][j] for j in (0, 1))
        if dot / (math.hypot(*vectors[0]) * math.hypot(*vectors[1])) < .90:
            continue
        if a["state"] == b["state"] == "confirmed":
            continue  # Both previously observed attachments may be a real branch.
        result.append(alternatives)
    return result


def _choice_pair(answers, names, mappings, ids):
    """Map labels in each actual normalized answer back to fixed code anchors."""
    values, raw = {identity: [] for identity in ids}, []
    for name, mapping in zip(names, mappings):
        distribution = answers.get(name)
        options = {"line_a", "line_b", "none"}
        valid = (isinstance(distribution, dict) and set(distribution) == options
                 and all(type(p) in (int, float) and math.isfinite(p) and 0 <= p <= 1
                         for p in distribution.values()) and abs(sum(distribution.values()) - 1) <= .02)
        raw.append(copy.deepcopy(distribution))
        if not valid:
            continue
        for label, identity in mapping.items():
            values[identity].append(distribution[label])
    return values, raw


async def adjudicate_competing_attachments(extractor, ctx, groups, remaining):
    """One paired fixed-category request per eligible physical port."""
    questions, metadata, pending = {}, {}, []
    for alternatives in groups:
        if remaining < len(alternatives):
            break
        if any(entity.get("adjudication") for entity in alternatives):
            continue
        remaining -= len(alternatives)
        identity = entity_id("port_choice", {"alternatives": sorted(e["id"] for e in alternatives)})
        names, mappings = [], []
        for tag, indices in (("A", (0, 1)), ("B", (1, 0))):
            detail = {"object": alternatives[0]["geometry"]["object"],
                      "bbox": alternatives[0]["detail"]["bbox"],
                      "anchors": [alternatives[i]["geometry"]["line_anchor"] for i in indices],
                      "path": [alternatives[0]["geometry"]["point"]]}
            mapping = {"line_a": alternatives[indices[0]]["id"], "line_b": alternatives[indices[1]]["id"]}
            name = f"pc{identity}_{tag}"
            options = {"line_a": "Only the original line at label A enters the boxed symbol at the selected port.",
                       "line_b": "Only the original line at label B enters the boxed symbol at the selected port.",
                       "none": "Neither marked line is uniquely supported as the line entering that selected port."}
            if tag == "B":
                options = dict(reversed(list(options.items())))
            questions[name] = extractor.choice({"port_detail": extractor.Img(raw_local_view(
                extractor, ctx.page, detail, (extractor.V.RED, extractor.BLUE), ("A", "B"))),
                "question": "Choose which one of the two code-marked nearby parallel line arms actually enters "
                            "the boxed target at its selected port. Follow only unchanged original black/grey ink. "
                            "Regular dashes and flange bars may continue a line. Reject proximity, a line passing "
                            "beside the body, an unrelated crossing, or a route through a different symbol. "
                            "If two real branches both enter, or no unique arm can be established, choose none. "
                            "A/B labels and colours do not create lines."}, options)
            metadata[name] = {**detail, "label_to_entity": mapping, "physical_port": identity}
            names.append(name)
            mappings.append(mapping)
        pending.append((alternatives, names, mappings))
    got = await ctx.jev.ask_chunked("K7_shared_port_choice", {"task": "Select one finite original line attachment."},
                                    questions, metadata) if questions else {}
    for alternatives, names, mappings in pending:
        values, raw = _choice_pair(got, names, mappings, [e["id"] for e in alternatives])
        for entity in alternatives:
            entity["adjudication"] = {"source": "fixed_category_port_choice", "stage": "K7_shared_port_choice",
                                       "question_names": names, "p_yes": values[entity["id"]],
                                       "raw_distributions": raw, "label_to_entity": mappings,
                                       "none_means": "no_unique_attachment_keep_review_needed"}
            # 'None' includes ambiguity; it is not a proof of non-connection.
            if not paired_support(values[entity["id"]]):
                entity["state"], entity["reasons"] = "review_needed", ["categorical_attachment_unresolved"]
            else:
                _refresh(entity, extractor)
    return remaining


async def _adjudicate_binary(extractor, ctx, entities, stage):
    questions, metadata = {}, {}
    for entity in entities:
        detail = copy.deepcopy(entity["detail"])
        path = entity.get("path", [])
        if entity["kind"] != "attachment":
            detail.update(a=path[0], b=path[-1], path=path)
        for tag, colors in (("A", (extractor.V.RED, extractor.BLUE)), ("B", (extractor.BLUE, extractor.V.RED))):
            name = f"sg{entity['id']}_{tag}"
            attachment = entity["kind"] == "attachment"
            question = ("The boxed target and coloured bracket centres identify a finite code-proposed "
                        "body contact and outside line anchor. Does the original black/grey line at the "
                        "outside anchor enter that exact selected symbol port? Follow the short original "
                        "stem to the body; a flange or regular dash gap may continue it. Mere proximity "
                        "or a different adjacent arm does not count." if attachment else
                        "The bracket centres identify the two ends of one finite code-proposed original "
                        "line segment or junction. Follow ONLY the unchanged black/grey ink between those "
                        "centres, allowing a regular dashed sequence or visible flange continuation. "
                        "For a turn, require a visible elbow/T/dot, not two nearby unconnected arms. "
                        "Do not follow a different parallel line, connect a broken crossing, or travel "
                        "through another symbol body. Judge this precise local segment, not whether "
                        "other distant symbols are generally connected.")
            if attachment and detail.get("contact_type") == "flange":
                question += (" This is a finite code-observed flange attachment. Two short perpendicular "
                             "flange bars and an aligned original pipe shaft may leave small white gaps; "
                             "those flange marks do not by themselves break the pipe. Confirm continuation "
                             "only if the original bars/shaft align with this exact body contact and outside "
                             "anchor. Reject unrelated bars, another nearby arm, or a shaft passing beside the body.")
            elif attachment and detail.get("contact_type") == "dashed_stem":
                question += (" The code observed an aligned short dashed stem at this port. Follow its original "
                             "repeating grey/black dashes across regular gaps to the selected body contact; "
                             "do not require a solid stroke, and do not join isolated nearby marks.")
            questions[name] = extractor.noul({"physical_detail": extractor.Img(raw_local_view(
                extractor, ctx.page, detail, colors)), "question": question},
                "The marked original local line/attachment is connected.",
                "That marked original local line/attachment is not connected.")
            metadata[name] = {**detail, "entity": entity["id"], "kind": entity["kind"]}
    got = await ctx.jev.ask_chunked(stage, {"task": "Adjudicate one shared physical line entity."},
                                    questions, metadata) if questions else {}
    for entity in entities:
        names = [f"sg{entity['id']}_{tag}" for tag in ("A", "B")]
        values = extractor.valid_noul_values(got, names)
        entity["adjudication"] = {"source": "one_focused_raw_ink_paired_review", "stage": stage,
                                   "question_names": names, "p_yes": list(values),
                                   "model": getattr(ctx.jev, "model", None)}
        _refresh(entity, extractor)


def _route_state(registry, route):
    entities = [registry[i] for i in route["entity_ids"]]
    if (not entities or len(route["attachment_ids"]) != 2
            or not any(e["kind"] != "attachment" for e in entities)):
        return "review_needed", ["missing_route_or_actual_ports"]
    if any(e["state"] == "rejected" for e in entities):
        return "rejected", ["local_entity_rejected"]
    if all(e["state"] == "confirmed" for e in entities):
        return "confirmed", ["all_shared_segments_and_actual_attachments_confirmed"]
    return "review_needed", sorted({reason for e in entities if e["state"] != "confirmed" for reason in e["reasons"]})


async def verify_shared_graph(extractor, ctx, objs, rels, nets=None):
    """Preserve accepted pairs; recover only fully supported physical routes.

    The per-page review budget bounds extra questions, but never removes a
    candidate. Unasked entities are exported with an explicit budget reason.
    No connectivity operation unions the different ports of a symbol body.
    """
    if getattr(ctx, "kind", None) != "pid":
        ctx.connection_graph = {"schema": "shared-connection-graph-v1", "revision": REVISION,
                                "entities": [], "candidate_routes": [], "summary": {"not_applicable": True}}
        return ctx.connection_graph
    if getattr(ctx, "_shared_graph_verified", False):
        return export_graph(ctx, objs, rels)
    work_rels, alternatives = _expand_alternatives(objs, rels)
    registry, routes = _record_entities(extractor, ctx, objs, work_rels)
    eligible = {route["index"] for route in routes
                if _eligible(extractor, ctx, objs, work_rels[route["index"]], route)}
    budget = max(0, int(getattr(ctx, "connection_graph_review_budget", MAX_ENTITY_REVIEWS)))
    remaining = budget
    needed = {identity for route in routes if route["index"] in eligible for identity in route["entity_ids"]}
    def priority(entity):
        relevant = [routes[i] for i in entity["candidate_indices"] if i in eligible]
        unresolved = min((sum(registry[k]["state"] != "confirmed" for k in r["entity_ids"]) for r in relevant), default=999)
        return (unresolved, -len(relevant), -int(any(paired_support(e.get("p_yes", [])) for e in entity["evidence"])), entity["id"])
    def selectable(entity):
        return (entity["id"] in needed and entity["state"] == "review_needed"
                and not entity.get("adjudication")
                and not (entity["kind"] == "attachment" and
                         entity.get("detail", {}).get("contact_geometry_status") == "unobserved")
                and not any(_valid_pair(e.get("p_yes")) and sum(e["p_yes"]) / 2 < getattr(extractor, "LOCAL_REJECT", .15)
                            for e in entity["evidence"]))
    route_entities = sorted((e for e in registry.values() if e["kind"] != "attachment" and selectable(e)), key=priority)
    # A finite new route cannot finish without its actual ports. Reserve part
    # of the same bounded budget for those attachments rather than consuming
    # the entire page budget on disjoint unfinished route segments.
    attachment_needed = sum(e["kind"] == "attachment" and selectable(e) for e in registry.values())
    port_reserve = min(attachment_needed, budget // 3)
    selected = route_entities[:max(0, remaining - port_reserve)]
    remaining -= len(selected)
    await _adjudicate_binary(extractor, ctx, selected, "K7_shared_physical_line")
    # Spend endpoint questions only on routes whose physical segments are all
    # confirmed. Every unresolved route and port stays in the exported graph.
    viable = {route["index"] for route in routes if route["index"] in eligible
              and all(registry[i]["state"] == "confirmed" for i in route["entity_ids"]
                      if registry[i]["kind"] != "attachment")}
    attachment_entities = [e for e in registry.values() if e["kind"] == "attachment"
                           and any(i in viable for i in e["candidate_indices"])]
    groups = competing_attachment_groups(attachment_entities, getattr(ctx, "text_h", 9))
    if hasattr(extractor, "choice"):
        remaining = await adjudicate_competing_attachments(extractor, ctx, groups, remaining)
    selected = sorted((e for e in attachment_entities if selectable(e)), key=priority)[:remaining]
    remaining -= len(selected)
    await _adjudicate_binary(extractor, ctx, selected, "K8_shared_physical_attachment")
    # One bounded completion phase uses the *unused* budget on whole finite
    # route/port bundles. Previously asked entities are never retried. A bundle
    # containing a contradictory fresh answer cannot be completed by optimism.
    completion_start = remaining
    bundles = []
    for route in routes:
        if route["index"] not in eligible:
            continue
        pending_ids = [i for i in route["entity_ids"] if registry[i]["state"] != "confirmed"]
        if (pending_ids and len(pending_ids) <= remaining
                and all(selectable(registry[i]) for i in pending_ids)):
            bundles.append((len(pending_ids), -sum(any(paired_support(e.get("p_yes", []))
                                                     for e in registry[i]["evidence"]) for i in pending_ids),
                            route["index"], pending_ids))
    completion_ids, completion_routes = set(), []
    for _, _, index, pending_ids in sorted(bundles):
        combined = completion_ids | set(pending_ids)
        if len(combined) <= remaining:
            completion_ids = combined
            completion_routes.append(index)
    completion_lines = [registry[i] for i in sorted(completion_ids) if registry[i]["kind"] != "attachment"]
    remaining -= len(completion_lines)
    await _adjudicate_binary(extractor, ctx, completion_lines, "K7_shared_physical_line_completion")
    completion_viable = [routes[i] for i in completion_routes
                         if all(registry[k]["state"] == "confirmed" for k in routes[i]["entity_ids"]
                                if registry[k]["kind"] != "attachment")]
    completion_ports = {i for route in completion_viable for i in route["attachment_ids"]
                        if selectable(registry[i])}
    selected = [registry[i] for i in sorted(completion_ports)][:remaining]
    remaining -= len(selected)
    await _adjudicate_binary(extractor, ctx, selected, "K8_shared_physical_attachment_completion")
    for entity in registry.values():
        if entity["id"] in needed and entity["state"] == "review_needed" and not entity.get("adjudication"):
            if remaining == 0 and selectable(entity):
                entity["reasons"].append("per_page_review_budget_reached")
            elif selectable(entity):
                entity["reasons"].append("bounded_review_pending")
    recovered = 0
    for route in routes:
        rel = work_rels[route["index"]]
        state, reasons = _route_state(registry, route)
        if not route["baseline_accepted"] and route["index"] not in eligible:
            if rel.get("blockers") or route.get("reasons") == ["intervening_symbol"]:
                state, reasons = "rejected", ["intervening_symbol"]
            elif state == "confirmed":
                state, reasons = "review_needed", ["unanswered_pair_or_unavailable_route"]
        route.update(state=state, reasons=reasons, accepted=bool(rel.get("accepted")))
        rel["shared_graph_entity_ids"] = list(route["entity_ids"])
        rel["shared_graph_state"] = state
        rel["shared_graph_reasons"] = reasons
        if route["baseline_accepted"]:
            route["state"] = "confirmed"
            route["preserved_prior_acceptance"] = True
            route["shared_evidence_state"] = state
            continue
        if state == "confirmed" and route["index"] in eligible:
            rel["pre_graph_decision"] = rel.get("decision")
            rel["accepted"], rel["decision"] = True, "shared_physical_route_with_actual_ports"
            confidence = min(registry[i]["confidence"] for i in route["entity_ids"])
            rel["confidence"] = confidence
            rel["local_confidence"] = min(registry[i]["confidence"] for i in route["entity_ids"]
                                           if registry[i]["kind"] != "attachment")
            rel["endpoint_confidence"] = min(registry[i]["confidence"] for i in route["attachment_ids"])
            route["accepted"] = True
            recovered += 1
    # Select the first fully confirmed finite alternative in retained code
    # order; do not invent a winner by taking an optimistic model maximum.
    # All alternatives, including failed/unasked paths, remain in the trace.
    alternative_recoveries = 0
    geometry_fields = {"a", "b", "a_side", "b_side", "a_point", "b_point", "a_anchor", "b_anchor",
                       "path", "net", "length", "bridges", "dashed", "mst", "tee_gaps", "signal_gaps",
                       "endpoint_contacts", "net_attachment_source", "same_original_label_net",
                       "crossing_details", "graph_id", "candidate_source", "net_rank", "checkpoint_keys"}
    for parent_index, indices in alternatives.items():
        primary = rels[parent_index]
        selected = None
        for index in indices:
            alternative, record = work_rels[index], routes[index]
            target = primary["route_alternatives"][record["alternative_index"]]
            target.update({"shared_graph_state": record["state"], "shared_graph_reasons": record["reasons"],
                           "shared_graph_entity_ids": list(record["entity_ids"]),
                           "shared_graph_accepted": bool(alternative.get("accepted")),
                           "global_pair_evidence_reference": copy.deepcopy(alternative["global_pair_evidence_reference"])})
            if selected is None and alternative.get("accepted"):
                selected = index
        if primary.get("accepted") or selected is None:
            continue
        alternative, record = work_rels[selected], routes[selected]
        primary["pre_graph_route"] = {key: copy.deepcopy(primary[key]) for key in geometry_fields if key in primary}
        primary["pre_graph_decision"] = primary.get("decision")
        for key in geometry_fields:
            if key in alternative:
                primary[key] = copy.deepcopy(alternative[key])
            elif key in {"tee_gaps", "signal_gaps", "endpoint_contacts", "crossing_details", "checkpoint_keys"}:
                primary[key] = [] if key != "endpoint_contacts" else {}
        primary.update(accepted=True, decision="shared_physical_alternative_with_actual_ports",
                       confidence=alternative["confidence"], local_confidence=alternative["local_confidence"],
                       endpoint_confidence=alternative["endpoint_confidence"],
                       shared_graph_state="confirmed", shared_graph_reasons=list(record["reasons"]),
                       shared_graph_entity_ids=list(record["entity_ids"]),
                       selected_graph_alternative_index=record["alternative_index"])
        original_record = routes[parent_index]
        original_record["original_path"] = copy.deepcopy(original_record["path"])
        original_record.update(a=record["a"], b=record["b"], path=copy.deepcopy(alternative["path"]), net=alternative.get("net"),
                               entity_ids=list(record["entity_ids"]), attachment_ids=list(record["attachment_ids"]),
                               state="confirmed", reasons=list(record["reasons"]), accepted=True,
                               selected_alternative_index=record["alternative_index"])
        alternative_recoveries += 1
    runtime = getattr(ctx, "connection_geometry_runtime", {})
    physical_graphs = [{"id": record.get("graph_id"), "source": record.get("source"),
                        "net": record.get("net", {}).get("id")}
                       for record in runtime.get("graph_records", [])]
    ctx.connection_graph = {"schema": "shared-connection-graph-v1", "revision": REVISION,
                            "entities": list(registry.values()), "candidate_routes": routes[:len(rels)],
                            "alternative_routes": routes[len(rels):],
                            "physical_graphs": physical_graphs,
                            "policy": {"segment_identity": "exact_reverse_independent_raw_geometry",
                                       "sharing": "exact_geometry_or_positive_collinear_containment",
                                       "symbol_ports": "distinct_ports_never_union_through_symbol_body",
                                       "paired_threshold": getattr(extractor, "LOCAL_RECOVER", .60),
                                       "strong_negative_threshold": getattr(extractor, "LOCAL_REJECT", .15),
                                       "max_entity_reviews": budget, "colour_orders_per_review": 2},
                            "summary": {"entity_reviews": budget - remaining,
                                        "completion_entity_reviews": completion_start - remaining,
                                        "newly_confirmed_pairs": sum(bool(r.get("accepted")) and not routes[i]["baseline_accepted"]
                                                                     for i, r in enumerate(rels)),
                                        "newly_confirmed_alternative_paths": recovered - sum(bool(r.get("accepted")) and
                                             r.get("decision") == "shared_physical_route_with_actual_ports" for r in rels),
                                        "pairs_recovered_by_alternative": alternative_recoveries,
                                        "entities": len(registry),
                                        "confirmed_entities": sum(e["state"] == "confirmed" for e in registry.values()),
                                        "review_needed_entities": sum(e["state"] == "review_needed" for e in registry.values()),
                                        "rejected_entities": sum(e["state"] == "rejected" for e in registry.values()),
                                        "review_needed_candidates": sum(r["state"] == "review_needed" for r in routes[:len(rels)]),
                                        "review_needed_alternatives": sum(r["state"] == "review_needed" for r in routes[len(rels):])}}
    ctx._shared_graph_verified = True
    return export_graph(ctx, objs, rels)


def export_graph(ctx, objs=None, rels=None):
    """Return serializable real evidence without image/label runtime arrays."""
    graph = copy.deepcopy(getattr(ctx, "connection_graph", {
        "schema": "shared-connection-graph-v1", "revision": REVISION,
        "entities": [], "candidate_routes": [], "summary": {"not_run": True}}))
    # numpy scalars can arrive in code-created path/net metadata; they are values
    # only. Image arrays deliberately never enter the public graph.
    def plain(value):
        if isinstance(value, dict):
            return {str(k): plain(v) for k, v in value.items() if not isinstance(v, np.ndarray)}
        if isinstance(value, (tuple, list)):
            return [plain(v) for v in value]
        if isinstance(value, np.generic):
            return value.item()
        return value
    return plain(graph)
