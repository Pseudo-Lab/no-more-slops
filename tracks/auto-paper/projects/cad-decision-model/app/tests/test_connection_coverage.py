"""Observed graph alternatives and accounting cannot create accepted edges."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from cad_api.connection_coverage import (
    _graph_id, build_coverage, finalize_coverage, flange_plate_gaps, install,
)


@pytest.fixture
def frozen(monkeypatch):
    source = Path(__file__).resolve().parents[1] / "cad_api/vendor/v12"
    monkeypatch.syspath_prepend(str(source))
    name = "coverage_test_frozen_extractor"
    spec = importlib.util.spec_from_file_location(name, source / "run_page.py")
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    module.CV.set_scale(9)
    return module


def two_routes():
    labels = np.zeros((100, 140), np.int32)
    cv2.line(labels, (10, 20), (110, 20), 1, 1)
    cv2.line(labels, (10, 70), (110, 70), 2, 1)
    nets = []
    for i, (label, y, side) in enumerate(((1, 20, "top"), (2, 70, "bottom"))):
        ports = [{"obj": j, "anchor": [x, y], "point": [x, y], "side": side}
                 for j, x in enumerate((10, 110))]
        nets.append({"id": i, "bbox": [10, y, 110, y], "labels": [label],
                     "ports": ports, "bridges": [], "dashed": False})
    return nets, labels


def harness(frozen, *, throw=False):
    nets, labels = two_routes()
    cv = SimpleNamespace(wire_nets=lambda *a, **kw: (copy.deepcopy(nets), labels),
                         wire_path=frozen.CV.wire_path)
    sig = SimpleNamespace(augment_nets=lambda *a, **kw: [], route_used_gap=frozen.SIG.route_used_gap)
    extractor = SimpleNamespace(CV=cv, CG=frozen.CG, SIG=sig,
                                mst_port_pairs=frozen.mst_port_pairs,
                                erase_box=lambda o, ext: o["bbox"])
    primary = {"a": 0, "b": 1, "a_side": "top", "b_side": "top",
               "a_point": [10, 20], "b_point": [110, 20], "net": 0,
               "path": [[10, 20], [110, 20]], "length": 100, "accepted": False}

    def original(ctx, objects, diag):
        ns, lab = extractor.CV.wire_nets()
        extractor.SIG.augment_nets(ns, lab)
        if throw:
            raise ValueError("collector failed")
        return [copy.deepcopy(primary)], ns

    extractor.relation_candidates = original
    ctx = SimpleNamespace(kind="pid", k={"erase_ext": 0}, text_h=9, tables=[],
                          bw_wire=(labels != 0).astype(np.uint8), port_tee_proposals=[])
    objects = [{"id": "s0", "bbox": [0, 30, 5, 60]},
               {"id": "s1", "bbox": [120, 30, 125, 60]}]
    return extractor, ctx, objects, primary


def test_different_ports_and_nets_are_retained_without_replacing_primary(frozen):
    extractor, ctx, objects, primary = harness(frozen)
    install(extractor)
    candidates, nets = extractor.relation_candidates(ctx, objects, [])
    assert len(candidates) == 1
    got = candidates[0]
    assert all(got[k] == v for k, v in primary.items())
    assert len(got["route_alternatives"]) == 1
    alternative = got["route_alternatives"][0]
    assert alternative["net"] == 1
    assert alternative["path"] == [[10, 70], [110, 70]]
    assert alternative["a_side"] == "bottom"
    assert alternative["requires_shared_graph_verification"]
    assert "accepted" not in alternative
    assert len(nets) == 2
    assert len(ctx.connection_geometry["ports"]) == 4
    assert ctx.connection_geometry["summary"]["retained_route_alternatives"] == 1


def test_accepting_one_route_does_not_confirm_other_ports_of_same_symbols(frozen):
    extractor, ctx, objects, _ = harness(frozen)
    install(extractor)
    candidates, _ = extractor.relation_candidates(ctx, objects, [])
    candidates[0]["accepted"] = True
    geometry = finalize_coverage(ctx.connection_geometry, candidates, objects)
    assert {p["status"] for p in geometry["ports"] if p["side"] == "top"} == {"confirmed"}
    assert {p["status"] for p in geometry["ports"] if p["side"] == "bottom"} == {"review_needed"}
    assert geometry["summary"]["retained_route_alternatives"] == 1


def test_identical_local_route_on_two_global_graphs_is_not_rejudged(frozen):
    extractor, ctx, objects, primary = harness(frozen)
    before = extractor.relation_candidates

    def twice(ctx, objects, diag):
        result, nets = before(ctx, objects, diag)
        extractor.CV.wire_nets()  # an augmented graph with the same local ink
        return result, nets

    extractor.relation_candidates = twice
    install(extractor)
    result, _ = extractor.relation_candidates(ctx, objects, [])
    assert len(result[0]["route_alternatives"]) == 1
    assert len(result[0]["equivalent_graph_ids"]) == 2
    assert len(result[0]["route_alternatives"][0]["equivalent_graph_ids"]) == 1
    assert result[0]["path"] == primary["path"]


def test_dense_net_asks_bounded_neighbours_instead_of_every_pair(frozen):
    extractor, ctx, _, _ = harness(frozen)
    labels = np.zeros((100, 220), np.int32)
    cv2.line(labels, (10, 20), (190, 20), 1, 1)
    ports = [{"obj": i, "anchor": [10+20*i, 20], "point": [10+20*i, 20], "side": "top"}
             for i in range(10)]
    net = {"id": 0, "bbox": [10, 20, 190, 20], "labels": [1], "ports": ports,
           "bridges": [], "dashed": False}
    extractor.CV.wire_nets = lambda *a, **kw: ([copy.deepcopy(net)], labels)

    def original(ctx, objects, diag):
        ns, _ = extractor.CV.wire_nets()
        return [], ns

    extractor.relation_candidates = original
    objects = [{"id": f"s{i}", "bbox": [10+20*i, 40, 15+20*i, 50]} for i in range(10)]
    ctx.bw_wire = (labels != 0).astype(np.uint8)
    install(extractor)
    result, _ = extractor.relation_candidates(ctx, objects, [])
    assert 0 < len(result) <= 2*len(ports)
    assert len(result) < 10*9/2
    assert all(abs(r["a"]-r["b"]) <= 2 for r in result)
    assert all("accepted" not in r for r in result)


def test_isolated_visible_port_and_open_line_end_are_never_silently_dropped():
    nets, labels = two_routes()
    nets = [nets[0]]
    nets[0]["ports"] = nets[0]["ports"][:1]
    record = {"net": nets[0], "labels": labels, "source": "original_wire",
              "graph_id": _graph_id(nets[0], "original_wire")}
    geometry = build_coverage(nets, labels, [record], [{"id": "s0"}], [])
    assert len(geometry["ports"]) == 1
    assert geometry["ports"][0]["candidate_ids"] == []
    assert len(geometry["line_ends"]) == 2
    assert {p["status"] for p in geometry["ports"]+geometry["line_ends"]} == {"review_needed"}
    finalize_coverage(geometry, [], [{"id": "s0"}])
    assert geometry["summary"]["line_ends"]["review_needed"] == 2


def plate_wire(*, competing=False, central_crossing=False):
    mask = np.zeros((100, 100), np.uint8)
    cv2.line(mask, (50, 20), (50, 40), 1, 1)
    cv2.line(mask, (44, 40), (56, 40), 1, 1)
    cv2.line(mask, (47, 46), (53, 46), 1, 1)
    cv2.line(mask, (44, 52), (56, 52), 1, 1)
    cv2.line(mask, (50, 52), (50, 80), 1, 1)
    if competing:
        cv2.line(mask, (48, 44), (52, 44), 1, 1)
    if central_crossing:
        cv2.line(mask, (10, 46), (90, 46), 1, 1)
    _, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    nets = []
    for anchor, obj in (((50, 20), 0), ((50, 80), 1)):
        label = int(labels[anchor[1], anchor[0]])
        x, y, w, h, _ = map(int, stats[label])
        nets.append({"id": len(nets), "labels": [label], "bbox": [x, y, x+w-1, y+h-1],
                     "ports": [{"obj": obj, "side": "bottom" if obj == 0 else "top",
                                "point": list(anchor), "anchor": list(anchor)}], "bridges": []})
    return mask, labels, nets


def test_three_bar_flange_plate_is_only_a_raw_geometry_hypothesis():
    mask, labels, nets = plate_wire()
    before = mask.copy(), labels.copy(), copy.deepcopy(nets)
    gaps = flange_plate_gaps(mask, labels, nets, text_h=12)
    assert len(gaps) == 1
    assert gaps[0]["reason"] == "raw_supported_three_bar_plate"
    assert gaps[0]["gap_points"] == [[50, 40], [50, 52]]
    assert gaps[0]["requires_original_ink_check"]
    assert gaps[0]["status"] == "review_needed"
    assert "accepted" not in gaps[0]
    assert np.array_equal(mask, before[0]) and np.array_equal(labels, before[1]) and nets == before[2]


@pytest.mark.parametrize("competing,central_crossing", [(True, False), (False, True)])
def test_competing_or_crossing_lines_do_not_become_plate_gaps(competing, central_crossing):
    mask, labels, nets = plate_wire(competing=competing, central_crossing=central_crossing)
    assert flange_plate_gaps(mask, labels, nets, text_h=12) == []


def test_symbol_body_blocks_a_flange_plate_hypothesis():
    mask, labels, nets = plate_wire()
    assert flange_plate_gaps(mask, labels, nets, boxes=[[46, 42, 54, 50]], text_h=12) == []


def test_wrapped_geometry_hooks_restore_after_failure(frozen):
    extractor, ctx, objects, _ = harness(frozen, throw=True)
    wire, augment = extractor.CV.wire_nets, extractor.SIG.augment_nets
    install(extractor)
    with pytest.raises(ValueError, match="collector failed"):
        extractor.relation_candidates(ctx, objects, [])
    assert extractor.CV.wire_nets is wire and extractor.SIG.augment_nets is augment


def test_explicit_rejection_applies_only_to_the_same_actual_port():
    nets, labels = two_routes()
    records = [{"net": n, "labels": labels, "source": "original_wire", "graph_id": _graph_id(n, "original_wire")}
               for n in nets]
    geometry = build_coverage(nets, labels, records, [{"id": "s0"}, {"id": "s1"}], [])
    identity = geometry["ports"][0]["id"]
    finalize_coverage(geometry, [], [{"id": "s0"}, {"id": "s1"}],
                      {"entities": [{"kind": "attachment", "coverage_port_id": identity, "status": "rejected"}]})
    assert sum(p["status"] == "rejected" for p in geometry["ports"]) == 1
    assert sum(p["status"] == "review_needed" for p in geometry["ports"]) == 3


def test_verified_shared_attachment_is_accounted_even_with_unresolved_rest_of_route():
    nets, labels = two_routes()
    records = [{"net": n, "labels": labels, "source": "original_wire", "graph_id": _graph_id(n, "original_wire")}
               for n in nets]
    geometry = build_coverage(nets, labels, records, [{"id": "s0"}, {"id": "s1"}], [])
    graph = {"entities": [{"kind": "attachment", "state": "confirmed",
                           "geometry": {"object": "s0", "side": "top", "line_anchor": [10, 20]}}]}
    finalize_coverage(geometry, [], [{"id": "s0"}, {"id": "s1"}], graph)
    assert sum(p["state"] == "confirmed" for p in geometry["ports"]) == 1
    assert sum(p["state"] == "review_needed" for p in geometry["ports"]) == 3


def test_line_end_accounting_does_not_snap_in_a_separate_parallel_wire():
    nets, labels = two_routes()
    records = [{"net": n, "labels": labels, "source": "original_wire", "graph_id": _graph_id(n, "original_wire")}
               for n in nets]
    geometry = build_coverage(nets, labels, records, [{"id": "s0"}, {"id": "s1"}], [])
    graph = {"entities": [{"id": "checked-stroke", "kind": "segment", "state": "confirmed",
                           "geometry": {"path": [[10, 20], [110, 20]]}}]}
    finalize_coverage(geometry, [], [{"id": "s0"}, {"id": "s1"}], graph)
    assert {e["state"] for e in geometry["line_ends"] if e["point"][1] == 20} == {"confirmed"}
    assert {e["state"] for e in geometry["line_ends"] if e["point"][1] == 70} == {"review_needed"}
    assert {p["state"] for p in geometry["ports"]} == {"review_needed"}
