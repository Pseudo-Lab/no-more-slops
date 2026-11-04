"""Additional v13 questions on dense P&ID nets, preserving frozen v12 routes.

The frozen collector asks a spanning tree on ordinary dense pipe nets. One
rejected tree edge can consequently hide an otherwise visible branch. This
supplement adds at most two route-nearest neighbours per object as questions.
Acceptance thresholds and original raw routes stay fixed. A port-only hypothesis
on exactly one unchanged raw net retains that raw net's identity after its usual
gap and endpoint checks; hypotheses joining different raw nets stay separate.
"""
from __future__ import annotations

import copy
from functools import wraps
import json


REVISION = "geometry-local-route-v13-connections"
NEIGHBOURS = 2
PORT_ATTACHMENTS = {"instrument_terminal_port", "inline_equipment_port_flange_gap"}
PORT_CONTACTS = PORT_ATTACHMENTS | {"compact_signal_branch_endpoint"}


def _signature(net, source):
    # The collector assigns a new id when an augmented graph contributes its
    # first question. Match the graph, not that order-dependent integer.
    graph = {k: v for k, v in net.items()
             if k not in {"id", "mst", "inferred_outlet_tee", "v13_candidate_net"}}
    return source, json.dumps(graph, sort_keys=True, separators=(",", ":"))


def _source(net):
    if net.get("signal_gap_proposals"):
        return "inferred_signal"
    if net.get("inferred_outlet_tee"):
        return "inferred_outlet_tee"
    return "original_wire"


def _port_attachment_original(net, raw_nets, raw_labels):
    """A new port on unchanged raw components keeps that wire's identity.

    A gap joining components is topology, even when its source drawing looks
    nearby. It must retain its separate hypothesis id. Likewise, an existing
    object at another port must never act as a bridge through its own body.
    """
    proposals = net.get("signal_gap_proposals")
    labels = set(net.get("labels", []))
    if (not proposals or not labels or net.get("inferred_outlet_tee")
            or any(p.get("reason") not in PORT_ATTACHMENTS for p in proposals)):
        return None
    matching = [old for old in raw_nets if _source(old) == "original_wire"
                and set(old.get("labels", [])) == labels]
    if len(matching) != 1:
        return None
    old = matching[0]
    if (net.get("bridges", []) != old.get("bridges", [])
            or net.get("bridge_paths", []) != old.get("bridge_paths", [])):
        return None
    old_ports, ports = old.get("ports", []), net.get("ports", [])
    if any(p not in ports for p in old_ports):
        return None
    added = [p for p in ports if p not in old_ports]
    if not added:
        return None
    old_objects = {p["obj"] for p in old_ports}
    for port in added:
        contact = port.get("inferred_port_gap", {})
        if port["obj"] in old_objects or contact.get("reason") not in PORT_CONTACTS:
            return None
        anchor = port.get("anchor")
        if not anchor or len(anchor) != 2:
            return None
        x, y = anchor
        if (int(x) != x or int(y) != y or not 0 <= int(y) < raw_labels.shape[0]
                or not 0 <= int(x) < raw_labels.shape[1]
                or int(raw_labels[int(y), int(x)]) not in labels):
            return None
    return old["id"]


def _canonicalize_port_attachments(candidates, nets, raw_nets, raw_labels):
    remap = {net["id"]: original for net in nets
             if (original := _port_attachment_original(net, raw_nets, raw_labels)) is not None}
    result, changed = [], 0
    for candidate in candidates:
        old_id = candidate["net"]
        # These existing gap and port checks are still required by K5/K6. A
        # net id is bookkeeping and cannot replace observed line evidence.
        if (old_id in remap and old_id != remap[old_id]
                and candidate.get("signal_gaps") and candidate.get("endpoint_contacts")):
            candidate = copy.deepcopy(candidate)
            candidate["net_attachment_source"] = old_id
            candidate["net"] = remap[old_id]
            candidate["same_original_label_net"] = True
            changed += 1
        result.append(candidate)
    return result, changed


def install(extractor):
    """Wrap ``relation_candidates`` in one isolated extraction worker.

    Only P&ID dense-net MST calls are supplemented. The temporary hooks observe
    the original graph construction and return exactly its original values;
    they are restored before extra paths are traced, including after errors.
    Calling install twice is harmless. There are no Decision Model calls here.
    """
    if getattr(extractor.relation_candidates, "_v13_dense_candidates", False):
        return
    original_relation_candidates = extractor.relation_candidates

    @wraps(original_relation_candidates)
    def supplemented(ctx, objs, diag_boxes):
        if ctx.kind != "pid":
            return original_relation_candidates(ctx, objs, diag_boxes)

        original_mst = extractor.mst_port_pairs
        original_wire_nets = extractor.CV.wire_nets
        owners, captured = {}, []
        raw_nets, raw_labels = [], None
        graph_calls = 0

        def observe_wire_nets(*args, **kwargs):
            nonlocal graph_calls, raw_nets, raw_labels
            nets, lab = original_wire_nets(*args, **kwargs)
            source = "original_wire" if graph_calls == 0 else "inferred_outlet_tee"
            if graph_calls == 0:
                raw_nets, raw_labels = list(nets), lab
            graph_calls += 1
            owners.update({id(net): source for net in nets})
            return nets, lab

        def observe_mst(ports, lab=None, net=None, neighbours=0):
            edges = original_mst(ports, lab, net, neighbours=neighbours)
            source = owners.get(id(net))
            # Signal hypotheses already receive these two neighbours in v12.
            # Unknown graphs are withheld rather than guessed to be raw nets.
            if source is not None and lab is not None and net is not None and neighbours < NEIGHBOURS:
                captured.append((copy.deepcopy(net), lab, source))
            return edges

        extractor.mst_port_pairs = observe_mst
        extractor.CV.wire_nets = observe_wire_nets
        try:
            original_candidates, original_nets = original_relation_candidates(ctx, objs, diag_boxes)
        finally:
            extractor.mst_port_pairs = original_mst
            extractor.CV.wire_nets = original_wire_nets

        candidates, nets = list(original_candidates), list(original_nets)
        existing = {tuple(sorted((r["a"], r["b"]))) for r in candidates}
        net_ids = {_signature(net, _source(net)): net["id"] for net in nets}
        next_net_id = max((net["id"] for net in nets), default=-1) + 1
        seen_graphs = set()
        added = 0
        for net, lab, source in captured:
            signature = _signature(net, source)
            if signature in seen_graphs:
                continue
            seen_graphs.add(signature)
            for a, b in original_mst(net["ports"], lab, net, neighbours=NEIGHBOURS):
                if a["obj"] == b["obj"]:
                    continue
                if a["obj"] > b["obj"]:
                    a, b = b, a
                key = a["obj"], b["obj"]
                if key in existing:
                    continue
                path = extractor.CV.wire_path(lab, net, a["anchor"], b["anchor"])
                if not path:
                    continue
                tees = [tee for tee in getattr(ctx, "port_tee_proposals", [])
                        if extractor.CG.uses_bridge(path, tee["path"], ctx.bw_wire)]
                # The v12 augmented outlet graph may ask a raw path too. Such
                # a path belongs to its original graph and is not relabelled
                # as an inferred tee connection.
                if source == "inferred_outlet_tee" and not tees:
                    continue
                if signature not in net_ids:
                    appended = copy.deepcopy(net)
                    appended["id"] = next_net_id
                    appended["v13_candidate_net"] = True
                    if source == "inferred_outlet_tee":
                        appended["inferred_outlet_tee"] = True
                    nets.append(appended)
                    net_ids[signature] = next_net_id
                    next_net_id += 1
                candidate = {
                    "a": a["obj"], "a_side": a["side"], "a_point": copy.deepcopy(a["point"]),
                    "b": b["obj"], "b_side": b["side"], "b_point": copy.deepcopy(b["point"]),
                    "net": net_ids[signature], "path": path,
                    "length": sum(abs(p[0]-q[0]) + abs(p[1]-q[1]) for p, q in zip(path, path[1:])),
                    "bridges": len(net["bridges"]), "dashed": net.get("dashed", False), "mst": True,
                    "tee_gaps": copy.deepcopy(tees),
                    "candidate_source": "v13_dense_net_neighbour", "candidate_net_source": source,
                    "candidate_revision": REVISION,
                }
                if net.get("signal_gap_proposals"):
                    candidate["signal_gaps"] = [extractor.SIG.route_used_gap(gap, path, ctx.bw_wire)
                                               for gap in net["signal_gap_proposals"]
                                               if extractor.CG.uses_bridge(path, gap["path"], ctx.bw_wire)
                                               or gap.get("symbol") in {objs[a["obj"]]["id"], objs[b["obj"]]["id"]}]
                    candidate["endpoint_contacts"] = {p["obj"]: copy.deepcopy(p["inferred_port_gap"])
                                                      for p in (a, b) if p.get("inferred_port_gap")}
                candidates.append(candidate)
                existing.add(key)
                added += 1
        candidates, canonicalized = _canonicalize_port_attachments(candidates, nets, raw_nets, raw_labels)
        ctx.connection_candidate_supplement = {
            "revision": REVISION, "source": "dense_net_route_neighbours", "neighbours": NEIGHBOURS,
            "original_candidates": len(original_candidates), "added_candidates": added,
            "dense_graphs": len(seen_graphs), "added_net_records": len(nets)-len(original_nets),
            "canonicalized_port_attachment_candidates": canonicalized,
        }
        return candidates, nets

    supplemented._v13_dense_candidates = True
    extractor.relation_candidates = supplemented
