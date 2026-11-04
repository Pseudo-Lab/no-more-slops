"""Policy tests use explicitly simulated answers, not measured model accuracy."""
from __future__ import annotations

import copy
import json
import math
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from cad_api import connection_graph as graph


class Judge:
    def __init__(self, values=(.94, .93), omit=False, choices=None):
        self.values, self.omit, self.choices = values, omit, choices
        self.calls = []

    async def ask_chunked(self, stage, state, questions, metadata):
        self.calls.append((stage, questions, metadata))
        result = {}
        for name in questions:
            if self.omit and name.endswith("_B"):
                continue
            if stage == "K7_shared_port_choice":
                result[name] = (self.choices or {}).get(name[-1], {"line_a": .05 if name.endswith("_B") else .9,
                                                                "line_b": .9 if name.endswith("_B") else .05,
                                                                "none": .05})
            else:
                result[name] = self.values[1 if name.endswith("_B") else 0]
        return result


def valid_values(answers, names):
    return [answers[name] for name in names if type(answers.get(name)) in (int, float)
            and math.isfinite(answers[name]) and 0 <= answers[name] <= 1]


@pytest.fixture
def example(monkeypatch):
    page = np.full((150, 170), 255, np.uint8)
    page[50, 39:122] = 90
    page[60, 39:122] = 90
    objs = [{"id": "s1", "bbox": [20, 40, 39, 60]},
            {"id": "s2", "bbox": [121, 40, 140, 60]}]
    weak = {"kind": "span", "path": [[40, 50], [120, 50]], "a": [40, 50], "b": [120, 50],
            "bbox": [22, 32, 138, 68], "p_yes": [.4, .4], "confidence": .4}
    checks = {"old": weak}
    endpoints = {"ea": {"bbox": objs[0]["bbox"], "point": [40, 50], "p_yes": [.95, .94]},
                 "eb": {"bbox": objs[1]["bbox"], "point": [120, 50], "p_yes": [.95, .94]}}
    ctx = SimpleNamespace(kind="pid", page=page, text_h=9, k={"erase_ext": False},
                          route_checkpoints=checks, endpoint_checks=endpoints, jev=Judge())
    rel = {"a": 0, "b": 1, "a_side": "right", "b_side": "left", "path": [[40, 50], [120, 50]],
           "accepted": False, "decision": "global_pair_local_uncertain", "checkpoint_keys": ["old"],
           "k3": [.7, .7]}
    extractor = SimpleNamespace(LOCAL_RECOVER=.6, LOCAL_REJECT=.15,
                                V=SimpleNamespace(RED=(0, 0, 230)), BLUE=(230, 0, 0),
                                Img=lambda image: image, valid_noul_values=valid_values,
                                erase_box=lambda obj, extra: list(obj["bbox"]),
                                noul=lambda state, yes, no: {"state": state, "yes": yes, "no": no},
                                choice=lambda state, criteria: {"state": state, "criteria": criteria})
    monkeypatch.setattr(graph, "raw_local_view", lambda *args: np.zeros((2, 2, 3), np.uint8))
    return extractor, ctx, objs, rel


def test_exact_geometry_identity_is_reverse_independent_and_parallel_safe():
    assert graph.canonical_path([[10, 30], [20, 30], [40, 30]]) == graph.canonical_path([[40, 30], [10, 30]])
    a = graph.entity_id("segment", {"path": graph.canonical_path([[10, 30], [40, 30]])})
    b = graph.entity_id("segment", {"path": graph.canonical_path([[40, 31], [10, 31]])})
    assert a != b
    assert graph.canonical_path([[10, 30], [20, 31], [40, 30]]) != [[10, 30], [40, 30]]


def test_conflicting_scores_never_take_optimistic_maximum():
    evidence = [{"p_yes": [.95, .94]}, {"p_yes": [.36, .36]}]
    assert graph.classify_entity(evidence)[0] == "review_needed"
    state, reasons = graph.classify_entity(evidence, {"p_yes": [.92, .91]})
    assert state == "confirmed" and "focused_adjudication_reconciles_crop_ambiguity" in reasons
    assert len(evidence) == 2  # Prior conflicting answers stay present.


@pytest.mark.parametrize("earlier", [[.04, .05], [.95, .1]])
def test_strong_rejection_or_order_conflict_cannot_be_hidden_by_fresh_yes(earlier):
    assert graph.classify_entity([{"p_yes": [.95, .94]}, {"p_yes": earlier}],
                                 {"p_yes": [.99, .99]})[0] == "review_needed"


@pytest.mark.asyncio
async def test_one_shared_focused_review_recovers_with_existing_actual_endpoints(example):
    extractor, ctx, objs, rel = example
    before = copy.deepcopy(objs), copy.deepcopy(rel["path"]), ctx.page.copy()
    reverse = {**copy.deepcopy(rel), "a": 1, "b": 0, "a_side": "left", "b_side": "right",
               "path": list(reversed(rel["path"]))}
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel, reverse])
    assert rel["accepted"] and reverse["accepted"]
    assert rel["decision"] == "shared_physical_route_with_actual_ports"
    assert len(ctx.jev.calls) == 1 and len(ctx.jev.calls[0][1]) == 2
    assert result["summary"]["newly_confirmed_pairs"] == 2
    assert len([e for e in result["entities"] if e["kind"] == "segment"]) == 1
    assert objs == before[0] and rel["path"] == before[1] and np.array_equal(ctx.page, before[2])
    await graph.verify_shared_graph(extractor, ctx, objs, [rel, reverse])
    assert len(ctx.jev.calls) == 1
    json.dumps(graph.export_graph(ctx, objs, [rel]))


@pytest.mark.asyncio
async def test_narrow_wide_conflict_is_one_entity_and_provenance_survives(example):
    extractor, ctx, objs, rel = example
    ctx.route_checkpoints["old"]["p_yes"] = [.95, .94]
    ctx.route_checkpoints["wide"] = {**copy.deepcopy(ctx.route_checkpoints["old"]),
                                     "bbox": [0, 0, 169, 149], "p_yes": [.36, .36],
                                     "rechecks": "old", "context_review": "wider_raw_crop"}
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    entity = next(e for e in result["entities"] if e["kind"] == "segment")
    assert rel["accepted"] and len(entity["evidence"]) == 2
    assert "focused_adjudication_reconciles_crop_ambiguity" in entity["reasons"]
    assert {e["key"] for e in entity["evidence"]} == {"old", "wide"}


@pytest.mark.asyncio
async def test_missing_swapped_answer_stays_visible_and_not_accepted(example):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(omit=True)
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert not rel["accepted"]
    assert result["candidate_routes"][0]["state"] == "review_needed"
    assert result["summary"]["review_needed_candidates"] == 1


@pytest.mark.asyncio
async def test_accepted_pairs_preserved_even_when_graph_evidence_conflicts(example):
    extractor, ctx, objs, rel = example
    rel["accepted"] = True
    ctx.route_checkpoints["old"]["p_yes"] = [.01, .01]
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert rel["accepted"] and ctx.jev.calls == []
    assert result["candidate_routes"][0]["preserved_prior_acceptance"]
    assert result["candidate_routes"][0]["shared_evidence_state"] == "rejected"


@pytest.mark.asyncio
async def test_positive_containment_shares_but_parallel_does_not(example):
    extractor, ctx, objs, rel = example
    ctx.connection_graph_review_budget = 0
    ctx.route_checkpoints["old"]["p_yes"] = []
    ctx.route_checkpoints["long"] = {"kind": "span", "path": [[30, 50], [130, 50]], "p_yes": [.9, .9]}
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert rel["accepted"] and ctx.jev.calls == []
    assert any(e.get("supporting_entity") for entity in result["entities"] for e in entity["evidence"])
    del ctx._shared_graph_verified
    rel["accepted"] = False
    ctx.route_checkpoints["long"]["path"] = [[30, 51], [130, 51]]
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and result["candidate_routes"][0]["state"] == "review_needed"


@pytest.mark.asyncio
async def test_containment_does_not_discard_conflicting_parent_evidence(example):
    extractor, ctx, objs, rel = example
    ctx.connection_graph_review_budget = 0
    ctx.route_checkpoints["old"]["p_yes"] = []
    ctx.route_checkpoints["long_yes"] = {"kind": "span", "path": [[30, 50], [130, 50]], "p_yes": [.9, .9]}
    ctx.route_checkpoints["long_no"] = {"kind": "span", "path": [[130, 50], [30, 50]], "p_yes": [.2, .2]}
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert not rel["accepted"]
    short = next(e for e in result["entities"] if e["geometry"].get("path") == [[40, 50], [120, 50]])
    assert short["state"] == "review_needed"
    assert not any(e.get("supporting_entity") for e in short["evidence"])


def _add_alternative(rel):
    rel["net"] = 1
    rel["route_alternatives"] = [{"a": 0, "b": 1, "a_side": "right", "b_side": "left",
                                 "a_anchor": [40, 60], "b_anchor": [120, 60],
                                 "path": [[40, 60], [120, 60]], "net": 2,
                                 "candidate_source": "v14_retained_route_alternative"}]


@pytest.mark.asyncio
async def test_true_fully_supported_alternative_replaces_failed_path_with_provenance(example):
    extractor, ctx, objs, rel = example
    old_path = copy.deepcopy(rel["path"])
    ctx.route_checkpoints["old"]["p_yes"] = [.01, .01]
    _add_alternative(rel)
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert rel["accepted"] and rel["decision"] == "shared_physical_alternative_with_actual_ports"
    assert rel["path"] == [[40, 60], [120, 60]] and rel["net"] == 2
    assert rel["pre_graph_route"]["path"] == old_path and rel["pre_graph_route"]["net"] == 1
    assert len(result["candidate_routes"]) == 1 and len(result["alternative_routes"]) == 1
    assert result["alternative_routes"][0]["parent_index"] == 0
    assert result["alternative_routes"][0]["alternative_index"] == 0
    assert result["alternative_routes"][0]["state"] == "confirmed"
    assert rel["route_alternatives"][0]["shared_graph_accepted"]
    assert result["summary"]["pairs_recovered_by_alternative"] == 1
    assert result["summary"]["newly_confirmed_pairs"] == 1
    assert rel["k3"] == [.7, .7]  # Original actual pair answer; no fake alt K3.


@pytest.mark.asyncio
@pytest.mark.parametrize("condition", ["missing", "budget", "unanswered_pair", "rejected_attachment"])
async def test_unconfirmed_alternative_is_retained_without_acceptance(example, condition):
    extractor, ctx, objs, rel = example
    ctx.route_checkpoints["old"]["p_yes"] = [.01, .01]
    _add_alternative(rel)
    if condition == "missing":
        ctx.jev = Judge(omit=True)
    elif condition == "budget":
        ctx.connection_graph_review_budget = 0
    elif condition == "unanswered_pair":
        rel["k3"] = [.7]
    else:
        class RejectEndpoint(Judge):
            async def ask_chunked(self, stage, state, questions, metadata):
                result = await super().ask_chunked(stage, state, questions, metadata)
                return {k: .01 for k in result} if stage == "K8_shared_physical_attachment" else result
        ctx.jev = RejectEndpoint()
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and rel["path"] == [[40, 50], [120, 50]]
    assert result["alternative_routes"][0]["state"] in {"review_needed", "rejected"}
    assert result["alternative_routes"][0]["path"] == [[40, 60], [120, 60]]
    assert not rel["route_alternatives"][0]["shared_graph_accepted"]


@pytest.mark.asyncio
async def test_accepted_primary_keeps_alternatives_visible_without_new_paid_checks(example):
    extractor, ctx, objs, rel = example
    rel["accepted"] = True
    _add_alternative(rel)
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert rel["accepted"] and rel["path"] == [[40, 50], [120, 50]] and ctx.jev.calls == []
    assert result["alternative_routes"][0]["state"] == "review_needed"


@pytest.mark.asyncio
async def test_no_connectivity_propagation_through_an_intervening_symbol_body(example):
    extractor, ctx, objs, rel = example
    ctx.route_checkpoints["old"]["p_yes"] = [.95, .95]
    objs.append({"id": "s3", "bbox": [70, 40, 90, 60]})
    extractor.CG = SimpleNamespace(intervening_symbols=lambda path, objects, exclude: [2])
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and result["candidate_routes"][0]["state"] == "rejected"
    assert ctx.jev.calls == []


@pytest.mark.asyncio
async def test_distinct_symbol_sides_remain_separate_actual_ports(example):
    extractor, ctx, objs, rel = example
    other = {**copy.deepcopy(rel), "a_side": "left", "path": [[20, 50], [120, 50]]}
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel, other])
    s1 = [e for e in result["entities"] if e["kind"] == "attachment" and e["geometry"]["object"] == "s1"]
    assert len(s1) == 2 and len({e["id"] for e in s1}) == 2
    assert result["policy"]["symbol_ports"] == "distinct_ports_never_union_through_symbol_body"


def _alternative(identity, anchor):
    return {"id": identity, "kind": "attachment", "geometry": {"object": "s1", "point": [40, 50],
                                                                "line_anchor": anchor, "side": "left"},
            "detail": {"bbox": [40, 40, 60, 60]}, "evidence": [], "state": "review_needed", "reasons": []}


@pytest.mark.asyncio
async def test_fixed_category_uses_two_code_anchors_and_swapped_label_mapping(example):
    extractor, ctx, objs, rel = example
    alternatives = [_alternative("port-a", [20, 46]), _alternative("port-b", [20, 54])]
    before = copy.deepcopy([e["geometry"] for e in alternatives])
    assert len(graph.competing_attachment_groups(alternatives)) == 1
    remaining = await graph.adjudicate_competing_attachments(extractor, ctx, [alternatives], 2)
    assert remaining == 0
    assert alternatives[0]["state"] == "confirmed" and alternatives[1]["state"] == "review_needed"
    assert alternatives[0]["adjudication"]["p_yes"] == [.9, .9]
    assert alternatives[0]["adjudication"]["label_to_entity"] == [
        {"line_a": "port-a", "line_b": "port-b"}, {"line_a": "port-b", "line_b": "port-a"}]
    questions = ctx.jev.calls[0][1]
    assert all(set(q["criteria"]) == {"line_a", "line_b", "none"} for q in questions.values())
    assert [e["geometry"] for e in alternatives] == before


@pytest.mark.asyncio
async def test_none_category_is_not_a_fake_negative_connection(example):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(choices={tag: {"line_a": .05, "line_b": .05, "none": .9} for tag in ("A", "B")})
    alternatives = [_alternative("port-a", [20, 46]), _alternative("port-b", [20, 54])]
    await graph.adjudicate_competing_attachments(extractor, ctx, [alternatives], 2)
    assert all(e["state"] == "review_needed" for e in alternatives)


def test_competing_attachment_does_not_merge_different_sides_or_far_parallel_lines():
    a, b = _alternative("a", [20, 46]), _alternative("b", [20, 54])
    b["geometry"]["side"] = "right"
    assert graph.competing_attachment_groups([a, b]) == []
    b["geometry"]["side"] = "left"
    b["geometry"]["line_anchor"] = [20, 90]
    assert graph.competing_attachment_groups([a, b]) == []


def test_raw_markers_leave_original_gray_strokes_unchanged():
    page = np.full((100, 100), 255, np.uint8)
    page[5:95:5, 5:95] = 90
    page[5:95, 5:95:5] = 0

    class View:
        def __init__(self, page, rect, scale):
            self.rect, self.s = rect, 1
            self.img = np.zeros((rect[3] - rect[1], rect[2] - rect[0], 3), np.uint8)

        def p(self, x, y):
            return round(x - self.rect[0]), round(y - self.rect[1])

        def finish(self):
            return self.img

    extractor = SimpleNamespace(ScaledView=View, fit_scale=lambda *a, **kw: 1,
                                V=SimpleNamespace(crop=lambda p, x0, y0, x1, y1: p[y0:y1, x0:x1]))
    detail = {"path": [[25, 25], [75, 75]], "a": [25, 25], "b": [75, 75], "view_pad": 24}
    before = page.copy()
    got = graph.raw_local_view(extractor, page, detail, ((0, 0, 230), (230, 0, 0)), ("A", "B"))
    raw = page[1:100, 1:100]
    expected = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
    assert np.array_equal(got[raw < 255], expected[raw < 255])
    assert np.array_equal(page, before)


@pytest.mark.parametrize("side,anchor,contact", [("right", [68, 50], [60, 50]),
                                                 ("left", [32, 50], [40, 50]),
                                                 ("top", [50, 32], [50, 40]),
                                                 ("bottom", [50, 68], [50, 60])])
def test_observed_boundary_stem_has_distinct_contact_and_outside_marker(side, anchor, contact):
    page = np.full((100, 100), 255, np.uint8)
    cv2.line(page, tuple(anchor), tuple(contact), 90, 1)
    before = page.copy()
    result = graph.observed_body_contact(page, [40, 40, 60, 60], anchor, side)
    assert result["body_contact"] == contact and result["outside_marker"] == anchor
    assert result["contact_geometry_status"] == "observed"
    assert result["contact_type"] == "straight_stem"
    assert np.array_equal(page, before)


def test_same_point_without_observed_outside_stem_and_neighbouring_arm_are_unresolved():
    page = np.full((100, 100), 255, np.uint8)
    page[50, 60] = 90
    assert graph.observed_body_contact(page, [40, 40, 60, 60], [60, 50], "right") is None
    page[51, 60:69] = 90  # An unrelated adjacent arm cannot repair y=50.
    assert graph.observed_body_contact(page, [40, 40, 60, 60], [68, 50], "right") is None
    page[50, 60:65] = 90
    result = graph.observed_body_contact(page, [40, 40, 60, 60], [60, 50], "right")
    assert result["body_contact"] == [60, 50] and result["outside_marker"] == [64, 50]


@pytest.mark.asyncio
async def test_unobserved_body_contact_is_flagged_even_if_old_endpoint_answer_said_yes(example):
    extractor, ctx, objs, rel = example
    ctx.page[50, 39] = 255
    ctx.route_checkpoints["old"]["p_yes"] = [.95, .95]
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    attachment = next(e for e in result["entities"] if e["kind"] == "attachment" and e["geometry"]["object"] == "s1")
    assert not rel["accepted"] and attachment["state"] == "review_needed"
    assert "actual_body_contact_unresolved" in attachment["reasons"]
    assert attachment["detail"]["contact_geometry_status"] == "unobserved"


@pytest.mark.asyncio
async def test_finite_flange_geometry_uses_structural_question_and_preserves_old_scores(example):
    extractor, ctx, objs, rel = example
    ctx.route_checkpoints["old"]["p_yes"] = [.95, .95]
    ctx.page[50, 39:48] = 255
    ctx.page[48:53, 39] = 90
    ctx.page[48:53, 43] = 90
    ctx.page[50, 47:51] = 90
    rel["path"][0] = [47, 50]
    rel["endpoint_contacts"] = {0: {"body_contact": [39, 50], "raw_contact_path": [[39, 50], [47, 50]],
                                    "reason": "inline_equipment_port_flange_gap", "side": "right"}}
    ctx.endpoint_checks["ea"] = {"bbox": objs[0]["bbox"], "point": [40, 50], "body_contact": [39, 50],
                                 "original_point": [47, 50], "raw_contact_path": [[39, 50], [47, 50]],
                                 "side": "right", "p_yes": [.24, .19]}
    result = await graph.verify_shared_graph(extractor, ctx, objs, [rel])
    attachment = next(e for e in result["entities"] if e["kind"] == "attachment" and e["geometry"]["object"] == "s1")
    assert attachment["detail"]["contact_type"] == "flange"
    assert attachment["detail"]["point"] == [39, 50] and attachment["detail"]["outside_marker"] == [47, 50]
    assert any(e["p_yes"] == [.24, .19] for e in attachment["evidence"])
    assert any("Two short perpendicular flange bars" in question["state"]["question"]
               for _, questions, _ in ctx.jev.calls for question in questions.values())


@pytest.mark.asyncio
async def test_unused_budget_completes_new_bundles_without_retrying_any_entity(example):
    extractor, ctx, objs, rel = example
    ctx.connection_graph_review_budget = 3
    ctx.route_checkpoints["short"] = {"kind": "span", "path": [[50, 50], [110, 50]], "p_yes": [.4, .4]}
    ctx.route_checkpoints["shorter"] = {"kind": "span", "path": [[60, 50], [100, 50]], "p_yes": [.4, .4]}
    paths = [rel, {**copy.deepcopy(rel), "checkpoint_keys": ["short"]},
             {**copy.deepcopy(rel), "checkpoint_keys": ["shorter"]}]
    # A separate rejected route has two as-yet-unjudged observed ports. Those
    # ports reserve budget initially but are not paid for after its rejection.
    ctx.page[32, 30:131] = 90
    ctx.page[32:41, 30] = 90
    ctx.page[32:41, 130] = 90
    ctx.route_checkpoints["blocked"] = {"kind": "span", "path": [[30, 32], [130, 32]], "p_yes": [.01, .01]}
    paths.append({**copy.deepcopy(rel), "a_side": "top", "b_side": "top",
                  "path": [[30, 32], [130, 32]], "checkpoint_keys": ["blocked"]})
    result = await graph.verify_shared_graph(extractor, ctx, objs, paths)
    assert all(route["accepted"] for route in paths[:3]) and not paths[3]["accepted"]
    assert result["summary"]["entity_reviews"] == 3
    assert result["summary"]["completion_entity_reviews"] == 1
    assert any(stage == "K7_shared_physical_line_completion" for stage, _, _ in ctx.jev.calls)
    names = [name for _, questions, _ in ctx.jev.calls for name in questions]
    assert len(names) == len(set(names)) == 6  # Two orders, each physical entity once.
