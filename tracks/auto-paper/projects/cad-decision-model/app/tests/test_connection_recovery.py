"""Connection recovery policy using explicitly simulated paired answers.

These tests verify acceptance rules and preservation of original visual
evidence. They do not measure a Decision Model's real accuracy.
"""
from __future__ import annotations

import copy
import math
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from cad_api import connection_recovery as recovery


class Judge:
    def __init__(self, route=(.94, .93), endpoints=(.95, .94), omit=None):
        self.route, self.endpoints, self.omit = route, endpoints, omit
        self.calls = []

    async def ask_chunked(self, stage, state, questions, metadata):
        self.calls.append((stage, state, questions, metadata))
        values = self.route if stage == "K5_dash_context" else self.endpoints
        return {name: values[0 if name.endswith("_A") else 1] for name in questions
                if not (self.omit == stage and name.endswith("_B"))}


def valid_values(answers, names):
    return [answers[name] for name in names if type(answers.get(name)) in (int, float)
            and math.isfinite(answers[name]) and 0 <= answers[name] <= 1]


@pytest.fixture
def example(monkeypatch):
    page = np.full((200, 200), 255, np.uint8)
    page[50, 40:121] = 100
    objs = [{"id": "s1", "bbox": [20, 40, 39, 60]},
            {"id": "s2", "bbox": [121, 40, 140, 60]}]
    item = {"kind": "span", "a": [40, 50], "b": [120, 50],
            "path": [[40, 50], [120, 50]], "bbox": [22, 32, 138, 68],
            "p_yes": [.4, .4], "confidence": .4}
    ctx = SimpleNamespace(kind="pid", page=page, text_h=9, k={"erase_ext": False},
                          route_checkpoints={"old": item}, endpoint_checks={}, jev=Judge())
    rel = {"a": 0, "b": 1, "path": [[40, 50], [120, 50]],
           "accepted": False, "decision": "global_pair_local_uncertain",
           "dashed": True, "k3": [.3, .4], "checkpoint_keys": ["old"]}
    extractor = SimpleNamespace(LOCAL_REJECT=.15, LOCAL_RECOVER=.6,
                                V=SimpleNamespace(RED=(0, 0, 230)), BLUE=(230, 0, 0),
                                Img=lambda image: image,
                                noul=lambda state, yes, no: {"state": state, "yes": yes, "no": no},
                                valid_noul_values=valid_values,
                                erase_box=lambda obj, with_ext: tuple(obj["bbox"]),
                                endpoint_detail_view=lambda *args: np.zeros((2, 2, 3), np.uint8),
                                ENDPOINT_Q="Check actual original attachment.")
    monkeypatch.setattr(recovery, "context_view", lambda *args: np.zeros((2, 2, 3), np.uint8))
    return extractor, ctx, objs, rel


@pytest.mark.asyncio
async def test_full_context_and_both_paired_endpoints_accept_once(example):
    extractor, ctx, objs, rel = example
    before = copy.deepcopy(objs), copy.deepcopy(rel["path"]), ctx.page.copy()
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert rel["accepted"] and rel["decision"] == "dash_context_with_paired_endpoints"
    assert [call[0] for call in ctx.jev.calls] == ["K5_dash_context", "K6_context_endpoint"]
    assert rel["confidence"] >= .6 and len(rel["context_endpoint_keys"]) == 2
    assert objs == before[0] and rel["path"] == before[1] and np.array_equal(ctx.page, before[2])
    count = len(ctx.jev.calls)
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert len(ctx.jev.calls) == count


@pytest.mark.asyncio
@pytest.mark.parametrize("confidence", [None, .05])
async def test_missing_or_strongly_rejected_old_span_never_retries(example, confidence):
    extractor, ctx, objs, rel = example
    ctx.route_checkpoints["old"]["confidence"] = confidence
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and ctx.jev.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("route", [(.95, .2), (.05, .95), (.49, .99)])
async def test_one_colour_order_cannot_recover_context(example, route):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(route=route)
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert not rel["accepted"]
    assert [call[0] for call in ctx.jev.calls] == ["K5_dash_context"]


@pytest.mark.asyncio
async def test_missing_context_answer_does_not_request_or_accept_endpoints(example):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(omit="K5_dash_context")
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and len(ctx.jev.calls) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoints,omit", [((.95, .05), None), ((.49, .99), None),
                                          ((.95, .94), "K6_context_endpoint")])
async def test_failed_or_missing_endpoint_does_not_accept_context(example, endpoints, omit):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(endpoints=endpoints, omit=omit)
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and len(ctx.jev.calls) == 2


@pytest.mark.asyncio
async def test_another_broken_span_cannot_be_hidden_by_a_good_context(example):
    extractor, ctx, objs, rel = example
    ctx.route_checkpoints["broken"] = {**ctx.route_checkpoints["old"], "confidence": .01}
    rel["checkpoint_keys"].append("broken")
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and ctx.jev.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("condition", ["accepted", "blocker", "non_pid", "unanswered_k3", "not_dashed"])
async def test_ineligible_routes_are_preserved_without_model_calls(example, condition):
    extractor, ctx, objs, rel = example
    if condition == "accepted":
        rel["accepted"] = True
    elif condition == "blocker":
        rel["blockers"] = ["s3"]
    elif condition == "non_pid":
        ctx.kind = "logic"
    elif condition == "unanswered_k3":
        rel["k3"] = [.8]
    else:
        rel["dashed"] = False
    before = copy.deepcopy(rel)
    await recovery.recover_context(extractor, ctx, objs, [rel])
    assert rel == before and ctx.jev.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("local", [None, .59])
async def test_new_backup_pair_requires_all_local_spans(example, local):
    extractor, ctx, objs, rel = example
    rel.update(accepted=True, candidate_source="bounded_backup", local_confidence=local,
               decision="global_pair_local_supported")
    await recovery.verify_added_pairs(extractor, ctx, objs, [rel])
    assert not rel["accepted"] and rel["decision"] == "backup_route_unconfirmed"
    assert ctx.jev.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoints,omit,accepted", [((.95, .94), None, True),
                                                   ((.95, .05), None, False),
                                                   ((.49, .99), None, False),
                                                   ((.95, .94), "K6_backup_endpoint", False)])
async def test_new_backup_pair_requires_both_orders_at_both_endpoints(example, endpoints, omit, accepted):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(endpoints=endpoints, omit=omit)
    rel.update(accepted=True, candidate_source="bounded_backup", local_confidence=.9,
               decision="global_pair_local_supported")
    await recovery.verify_added_pairs(extractor, ctx, objs, [rel])
    assert rel["accepted"] is accepted
    assert [call[0] for call in ctx.jev.calls] == ["K6_backup_endpoint"]


@pytest.mark.asyncio
async def test_old_mean_endpoint_acceptance_does_not_exempt_new_pair_from_both_orders(example):
    extractor, ctx, objs, rel = example
    ctx.jev = Judge(endpoints=(.95, .4))
    rel.update(accepted=True, candidate_source="bounded_backup", local_confidence=.9,
               decision="local_route_with_endpoints", endpoint_keys=["old-a", "old-b"])
    ctx.endpoint_checks = {"old-a": {"p_yes": [.95, .4], "confidence": .675},
                           "old-b": {"p_yes": [.95, .95], "confidence": .95}}
    await recovery.verify_added_pairs(extractor, ctx, objs, [rel])
    assert not rel["accepted"]


def test_context_expands_crop_without_changing_route_anchor_or_old_answer():
    page = np.full((160, 160), 255, np.uint8)
    item = {"bbox": [45, 45, 75, 75], "path": [[50, 50], [70, 70]],
            "a": [50, 50], "b": [70, 70], "p_yes": [.4, .4], "confidence": .4}
    before = copy.deepcopy(item)
    detail = recovery.context_detail(page, item, 9)
    assert detail["path"] == item["path"] and detail["a"] == item["a"] and detail["b"] == item["b"]
    assert detail["bbox"] == [5, 5, 115, 115]
    assert "p_yes" not in detail and "confidence" not in detail and item == before


def test_context_markers_preserve_every_original_gray_and_black_pixel():
    page = np.full((100, 100), 255, np.uint8)
    page[15:90:5, 10:90] = 89
    page[10:90, 15:90:5] = 0
    detail = {"bbox": [0, 0, 99, 99], "a": [35, 35], "b": [65, 65]}

    class View:
        def __init__(self, source, rect, scale):
            self.s, self.rect = scale, rect
            self.img = np.full((100, 100, 3), 255, np.uint8)

        def p(self, x, y):
            return x, y

        def finish(self):
            return self.img

    extractor = SimpleNamespace(fit_scale=lambda *args, **kwargs: 1,
                                ScaledView=View,
                                V=SimpleNamespace(crop=lambda src, x0, y0, x1, y1: src[y0:y1, x0:x1]))
    before = page.copy()
    got = recovery.context_view(extractor, page, detail, (0, 0, 230), (230, 0, 0))
    raw_ink = page < 255
    expected = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
    assert np.array_equal(got[raw_ink], expected[raw_ink])
    assert np.array_equal(page, before)
    assert np.any(got[~raw_ink] != expected[~raw_ink])  # Marks only occupy blank original pixels.


def test_paired_support_keeps_mean_threshold_and_requires_agreement():
    assert recovery.paired_support([.61, .59])
    assert not recovery.paired_support([.59, .59])
    assert not recovery.paired_support([.95, .4])
    assert not recovery.paired_support([.9])
    assert not recovery.paired_support([float("nan"), .9])
