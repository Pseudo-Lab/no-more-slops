"""Real wire graphs exercise candidate recovery without any model requests."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from cad_api.connection_candidates import install


@pytest.fixture
def frozen(monkeypatch):
    source = Path(__file__).resolve().parents[1] / "cad_api/vendor/v12"
    monkeypatch.syspath_prepend(str(source))
    name = "candidate_test_frozen_extractor"
    spec = importlib.util.spec_from_file_location(name, source / "run_page.py")
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    module.CV.set_scale(9)
    return module


def u_wire():
    labels = np.zeros((100, 140), np.int32)
    cv2.line(labels, (10, 10), (110, 10), 1, 1)
    cv2.line(labels, (110, 10), (110, 80), 1, 1)
    cv2.line(labels, (10, 80), (110, 80), 1, 1)
    anchors = [(10, 10), (10, 80), (70, 10), (110, 50), (50, 80)]
    ports = [{"obj": i, "anchor": list(p), "point": list(p), "side": "left"}
             for i, p in enumerate(anchors)]
    net = {"id": 7, "bbox": [10, 10, 110, 80], "labels": [1],
           "ports": ports, "bridges": [], "dashed": False}
    return net, labels


def harness(frozen, *, existing=None, augmented=False, throw=False, neighbours=0):
    net, labels = u_wire()
    cv = SimpleNamespace(wire_nets=lambda *a, **kw: ([copy.deepcopy(net)], labels),
                         wire_path=frozen.CV.wire_path)
    extractor = SimpleNamespace(CV=cv, CG=frozen.CG, SIG=frozen.SIG,
                                mst_port_pairs=frozen.mst_port_pairs)
    previous = existing or []

    def original(ctx, objs, diag):
        base_nets, lab = extractor.CV.wire_nets()
        base = base_nets[0]
        edges = extractor.mst_port_pairs(base["ports"], lab, base, neighbours=neighbours)
        base["mst"] = True
        if throw:
            raise ValueError("synthetic collector failure")
        candidates = [{"a": a["obj"], "b": b["obj"], "net": base["id"],
                       "path": frozen.CV.wire_path(lab, base, a["anchor"], b["anchor"])}
                      for a, b in edges]
        candidates.extend(copy.deepcopy(previous))
        if augmented:
            extra_nets, extra_lab = extractor.CV.wire_nets()
            extra = extra_nets[0]
            extra["labels"] = [1, 2]  # a genuinely separate augmented graph
            extractor.mst_port_pairs(extra["ports"], extra_lab, extra, neighbours=0)
            # No baseline candidate survives this augmented graph. The new
            # collector must assign an unused id, rather than reuse base 7.
            ctx.port_tee_proposals = [{"path": [[20, 10], [30, 10]]}]
        return candidates, base_nets

    extractor.relation_candidates = original
    ctx = SimpleNamespace(kind="pid", bw_wire=(labels != 0).astype(np.uint8),
                          port_tee_proposals=[])
    return extractor, ctx, net, labels


def pairs(candidates):
    return {tuple(sorted((r["a"], r["b"]))) for r in candidates}


def test_route_neighbours_do_not_take_a_euclidean_shortcut(frozen):
    extractor, ctx, net, labels = harness(frozen)
    install(extractor)
    result, nets = extractor.relation_candidates(ctx, [], [])
    # Along the U-shaped wire the order is 0,2,3,4,1. Nearby objects 0/1 on
    # the page must not be joined across the white interior of the U.
    assert pairs(result) == {(0, 2), (2, 3), (3, 4), (1, 4), (0, 3), (1, 3)}
    assert (0, 1) not in pairs(result)
    assert all(r["path"] for r in result)
    assert all(r["net"] == 7 for r in result)
    assert len(nets) == 1
    assert ctx.connection_candidate_supplement["added_candidates"] == 2
    assert all("accepted" not in r for r in result)


def test_existing_pair_primary_path_and_net_are_never_replaced(frozen):
    saved = {"a": 0, "b": 3, "net": 99, "path": [[8, 8], [9, 8]],
             "length": 1, "confidence": .9}
    extractor, ctx, _, _ = harness(frozen, existing=[saved])
    install(extractor)
    result, _ = extractor.relation_candidates(ctx, [], [])
    got = [r for r in result if tuple(sorted((r["a"], r["b"]))) == (0, 3)]
    assert got == [saved]
    assert ctx.connection_candidate_supplement["added_candidates"] == 1


def test_augmented_unused_graph_gets_a_distinct_net_and_gap_checks(frozen):
    extractor, ctx, _, _ = harness(frozen, augmented=True)
    # The raw graph cannot supply the alternate paths, but the explicitly
    # augmented graph can. This simulates a tee-only alternate branch.
    raw_path = extractor.CV.wire_path
    extractor.CV.wire_path = lambda lab, net, a, b: [] if net["labels"] == [1] else raw_path(lab, net, a, b)
    extractor.CG = SimpleNamespace(uses_bridge=lambda path, bridge, mask: bool(path))
    install(extractor)
    result, nets = extractor.relation_candidates(ctx, [], [])
    extras = [r for r in result if r.get("candidate_source")]
    assert len(extras) == 2
    assert {r["net"] for r in extras} == {8}
    assert all(r["candidate_net_source"] == "inferred_outlet_tee" for r in extras)
    assert all(r["tee_gaps"] for r in extras)
    assert nets[0]["id"] == 7
    assert nets[1]["id"] == 8 and nets[1]["inferred_outlet_tee"]


def test_hooks_restore_after_collector_error(frozen):
    extractor, ctx, _, _ = harness(frozen, throw=True)
    original_mst, original_wire_nets = extractor.mst_port_pairs, extractor.CV.wire_nets
    install(extractor)
    with pytest.raises(ValueError, match="synthetic collector failure"):
        extractor.relation_candidates(ctx, [], [])
    assert extractor.mst_port_pairs is original_mst
    assert extractor.CV.wire_nets is original_wire_nets


def test_existing_two_neighbour_policy_is_not_expanded_again(frozen):
    extractor, ctx, _, _ = harness(frozen, neighbours=2)
    original, original_nets = extractor.relation_candidates(ctx, [], [])
    install(extractor)
    result, nets = extractor.relation_candidates(ctx, [], [])
    assert result == original and nets == original_nets
    assert ctx.connection_candidate_supplement["added_candidates"] == 0


def test_untraceable_alternates_do_not_become_questions(frozen):
    extractor, ctx, _, _ = harness(frozen)
    extractor.CV.wire_path = lambda *args: []
    install(extractor)
    result, nets = extractor.relation_candidates(ctx, [], [])
    assert pairs(result) == {(0, 2), (2, 3), (3, 4), (1, 4)}
    assert len(nets) == 1
    assert ctx.connection_candidate_supplement["added_candidates"] == 0


def test_logic_calls_original_once_without_supplement(frozen):
    extractor, ctx, _, _ = harness(frozen)
    ctx.kind = "logic"
    before, before_nets = extractor.relation_candidates(ctx, [], [])
    install(extractor)
    result, nets = extractor.relation_candidates(ctx, [], [])
    assert result == before and nets == before_nets
    assert not hasattr(ctx, "connection_candidate_supplement")


def test_real_pid_collector_keeps_objects_baseline_routes_and_net_labels(frozen):
    page = np.full((240, 600), 255, np.uint8)
    cv2.line(page, (40, 100), (520, 100), 0, 1)
    objects = []
    for index, x in enumerate((80, 180, 280, 380, 480)):
        cv2.line(page, (x, 100), (x, 150), 0, 1)
        cv2.rectangle(page, (x-15, 150), (x+15, 180), 0, 1)
        objects.append({"id": f"s{index}", "class": "controller",
                        "bbox": [x-15, 150, x+15, 180], "class_confidence": .95})
    bw = (page < 180).astype(np.uint8)
    before_objects, before_page = copy.deepcopy(objects), page.copy()
    base_ctx = frozen.Ctx(page, bw, None, kind="pid", text_h=9)
    baseline, baseline_nets = frozen.relation_candidates(base_ctx, objects, [[0, 0, 599, 239]])
    install(frozen)
    installed = frozen.relation_candidates
    install(frozen)
    assert frozen.relation_candidates is installed
    ctx = frozen.Ctx(page, bw, None, kind="pid", text_h=9)
    result, nets = frozen.relation_candidates(ctx, objects, [[0, 0, 599, 239]])
    assert len(baseline) == 4 and len(result) == 6
    assert result[:len(baseline)] == baseline
    assert nets == baseline_nets
    assert len(pairs(result)) == len(result)
    assert all(r["a"] != r["b"] for r in result)
    assert len(result)-len(baseline) <= 2*len(objects)
    assert objects == before_objects
    np.testing.assert_array_equal(page, before_page)
    extras = result[len(baseline):]
    assert all(r["candidate_net_source"] == "original_wire" for r in extras)
    assert all("accepted" not in r for r in extras)


def attachment_harness(frozen, *, combine=False, opposite=False, elbow=False, ambiguous=False):
    raw, labels = u_wire()
    raw["id"], raw["ports"], raw["dashed"] = 10, raw["ports"][:2], True
    raw_nets = [raw]
    if combine:
        labels[90, 10:31] = 2
        other = copy.deepcopy(raw)
        other["id"], other["labels"] = 11, [2]
        other["ports"] = []
        raw_nets.append(other)
    if ambiguous:
        other = copy.deepcopy(raw)
        other["id"] = 11
        raw_nets.append(other)
    gap = {"reason": "dashed_elbow_gap" if elbow else "instrument_terminal_port",
           "symbol": "s2", "path": [[70, 10], [70, 15]], "requires_endpoint_check": True}
    attachment = {"obj": 0 if opposite else 2, "side": "top", "point": [70, 10], "anchor": [70, 10],
                  "inferred_port_gap": {"reason": "instrument_terminal_port", "raw_contact_path": [[70, 10], [70, 15]]}}
    hypothesis = copy.deepcopy(raw)
    hypothesis.update({"id": 22, "labels": [1, 2] if combine else [1], "bridge_paths": [],
                       "signal_gap_proposals": [gap]})
    hypothesis["ports"].append(attachment)
    raw_candidate = {"id": "original-pair", "a": 0, "b": 1, "net": 10,
                     "path": [[10, 10], [110, 10], [110, 80], [10, 80]]}
    candidate = {"id": "port-pair", "a": 1, "b": attachment["obj"], "net": 22,
                 "path": [[10, 80], [110, 80], [110, 10], [70, 10]],
                 "signal_gaps": [gap], "endpoint_contacts": {attachment["obj"]: attachment["inferred_port_gap"]}}
    cv = SimpleNamespace(wire_nets=lambda: (raw_nets, labels), wire_path=frozen.CV.wire_path)
    extractor = SimpleNamespace(CV=cv, CG=frozen.CG, SIG=frozen.SIG,
                                mst_port_pairs=frozen.mst_port_pairs)

    def original(ctx, objects, diagram):
        nets, _ = extractor.CV.wire_nets()
        return [raw_candidate, candidate], nets+[hypothesis]

    extractor.relation_candidates = original
    ctx = SimpleNamespace(kind="pid", bw_wire=(labels != 0).astype(np.uint8), port_tee_proposals=[])
    return extractor, ctx, raw_candidate, candidate


def test_confirmed_new_port_on_one_raw_dashed_net_keeps_original_identity(frozen):
    extractor, ctx, raw, port = attachment_harness(frozen)
    before_raw, before_port = copy.deepcopy(raw), copy.deepcopy(port)
    install(extractor)
    candidates, nets = extractor.relation_candidates(ctx, [], [])
    assert candidates[0] == before_raw
    recovered = candidates[1]
    assert recovered["net"] == 10
    assert recovered["net_attachment_source"] == 22 and recovered["same_original_label_net"] is True
    assert recovered["path"] == before_port["path"] and recovered["id"] == before_port["id"]
    assert recovered["signal_gaps"] == before_port["signal_gaps"]
    assert recovered["endpoint_contacts"] == before_port["endpoint_contacts"]
    assert port == before_port  # the frozen collector's original record stays intact
    assert [net["id"] for net in nets] == [10, 22]
    assert ctx.connection_candidate_supplement["canonicalized_port_attachment_candidates"] == 1


@pytest.mark.parametrize("change", ["combine", "opposite", "elbow", "ambiguous"])
def test_two_nets_body_opposite_port_gap_or_ambiguous_identity_do_not_merge(frozen, change):
    extractor, ctx, raw, port = attachment_harness(frozen, **{change: True})
    install(extractor)
    candidates, _ = extractor.relation_candidates(ctx, [], [])
    assert candidates[0] == raw
    assert candidates[1] == port and candidates[1]["net"] == 22
    assert "same_original_label_net" not in candidates[1]
    assert ctx.connection_candidate_supplement["canonicalized_port_attachment_candidates"] == 0


def test_missing_endpoint_evidence_cannot_canonicalize_port_hypothesis(frozen):
    extractor, ctx, _, port = attachment_harness(frozen)
    port.pop("endpoint_contacts")
    install(extractor)
    candidates, _ = extractor.relation_candidates(ctx, [], [])
    assert candidates[1]["net"] == 22
    assert "same_original_label_net" not in candidates[1]
