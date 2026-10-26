"""HTTP jobs exercise the real frozen extractor with a local decision service.

The image is an explicitly synthetic geometry fixture, not a benchmark result.
Only model answers are simulated; the production geometry, subprocess worker,
SQLite job store, output serialization and artifact rendering all execute.
"""
from __future__ import annotations

import base64
import io
import json
import shutil
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

from cad_api.app import create_app
from cad_api.config import Backend, Settings
from cad_api.storage import JobStore


LEGEND = json.dumps({"classes": [
    {"key": "general", "text": "An ordinary process component."},
    {"key": "other", "text": "Something other than a process component."},
]})


def drawing_bytes() -> bytes:
    page = Image.new("RGB", (640, 360), "white")
    ink = ImageDraw.Draw(page)
    ink.rectangle((90, 120, 170, 200), outline="black", width=2)
    ink.rectangle((380, 120, 460, 200), outline="black", width=2)
    ink.line((170, 160, 380, 160), fill="black", width=2)
    # Printed text prevents estimating scale from the wire alone.
    ink.text((112, 148), "P1", fill="black")
    ink.text((402, 148), "P2", fill="black")
    stream = io.BytesIO()
    page.save(stream, format="PNG")
    return stream.getvalue()


class LocalDecisionService:
    def __init__(self):
        self.requests: list[dict] = []
        self.lock = threading.Lock()
        self.gate: threading.Event | None = None
        self.malformed = False
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def do_POST(self):
                length = int(self.headers["Content-Length"])
                request = json.loads(self.rfile.read(length))
                with owner.lock:
                    owner.requests.append({"path": self.path, "body": request})
                if owner.gate is not None:
                    owner.gate.wait(timeout=10)
                answers = {}
                for name, question in request["questions"].items():
                    if question["type"] == "noul":
                        answers[name] = 0.98
                        continue
                    keys = list(question["criteria"])
                    preferred = next((key for key in
                                      ("pid", "diagram", "symbol", "general", "not_text", "1")
                                      if key in keys), keys[0])
                    answers[name] = {key: 0.98 if key == preferred else
                                     0.02 / (len(keys) - 1) for key in keys}
                    if len(keys) == 1:
                        answers[name] = {keys[0]: 1.0}
                if owner.malformed:
                    answers = {}
                response = json.dumps({"model": "local-fixture-model", "answers": answers,
                                       "usage": {"input_tokens": 100}}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                try:
                    self.wfile.write(response)
                except (BrokenPipeError, ConnectionResetError):
                    # A timed-out extraction intentionally kills its worker.
                    pass

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def endpoint(self, suffix="decision-a"):
        return f"http://127.0.0.1:{self.httpd.server_port}/{suffix}"

    def count(self, suffix=None):
        with self.lock:
            return sum(1 for request in self.requests
                       if suffix is None or request["path"] == "/" + suffix)

    def close(self):
        if self.gate is not None:
            self.gate.set()
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)


@pytest.fixture
def decision_service():
    service = LocalDecisionService()
    try:
        yield service
    finally:
        service.close()


def api_settings(tmp_path: Path, service: LocalDecisionService, **overrides):
    backends = {
        "a": Backend(id="a", provider="decision_http", endpoint=service.endpoint(),
                     model="same-fixture-model", concurrency=2, timeout_seconds=5),
        "b": Backend(id="b", provider="decision_http", endpoint=service.endpoint("decision-b"),
                     model="same-fixture-model", concurrency=2, timeout_seconds=5),
    }
    values = {"data_dir": tmp_path / "data", "backends": backends,
              "default_backend": "a", "job_timeout_seconds": 30, **overrides}
    return Settings(**values)


@pytest.mark.parametrize('revision,hash_count', [
    ('geometry-local-route-v13-connections', 4), ('geometry-local-route-v14-graph', 7),
    ('geometry-local-route-v15-semantics', 10)])
def test_connection_revision_is_selected_and_provenance_is_exported(tmp_path, decision_service, revision, hash_count):
    settings = api_settings(tmp_path, decision_service, algorithm_revision=revision)
    with TestClient(create_app(settings)) as client:
        assert client.get('/health').json()['algorithm_revision'] == revision
        job_id = submit(client)
        completed(client, job_id)
        result = client.get(f'/v1/extractions/{job_id}/result').json()
        assert result['meta']['algorithm_revision'] == revision
        assert result['meta']['baseline_revision'] == 'geometry-local-route-v12'
        assert len(result['meta']['supplement_hashes']) == hash_count
        assert result['meta']['api']['algorithm_revision'] == revision
        if revision in {'geometry-local-route-v14-graph', 'geometry-local-route-v15-semantics'}:
            review = result['connection_review']
            assert review['schema'] == 'cad_connection_review_v1'
            assert review['summary']['confirmed_candidates'] == sum(r['type'] == 'connected' for r in result['relations'])
            assert all(c['state'] in {'confirmed', 'review_needed', 'rejected'} for c in review['candidates'])
            saved = client.get(f'/v1/extractions/{job_id}/artifacts/input_review.json')
            assert saved.status_code == 200 and saved.json() == review
            overlay = client.get(f'/v1/extractions/{job_id}/artifacts/input_review.png')
            assert overlay.status_code == 200 and overlay.content.startswith(b'\x89PNG\r\n\x1a\n')
            if revision == 'geometry-local-route-v15-semantics':
                assert review['previous_connection_revision'] == 'geometry-local-route-v14-graph'
                assert 'K9 drawing notation semantics' in result['meta']['pipeline']


def submit(client: TestClient, backend="a"):
    response = client.post("/v1/extractions", data={"kind": "pid", "backend": backend,
                                                  "legend": LEGEND},
                           files={"image": ("user-drawing.png", drawing_bytes(), "image/png")})
    assert response.status_code == 202, response.text
    return response.json()["id"]


def completed(client: TestClient, job_id: str):
    job = terminal(client, job_id)
    assert job["status"] == "succeeded", job
    return job


def terminal(client: TestClient, job_id: str):
    deadline = time.monotonic() + 35
    while time.monotonic() < deadline:
        response = client.get(f"/v1/extractions/{job_id}")
        assert response.status_code == 200, response.text
        job = response.json()
        if job["status"] in {"succeeded", "failed"}:
            return job
        time.sleep(0.05)
    pytest.fail(f"Extraction {job_id} did not complete")


def image_payloads(value):
    if isinstance(value, dict):
        if value.get("type") == "image":
            yield value
        else:
            for child in value.values():
                yield from image_payloads(child)
    elif isinstance(value, list):
        for child in value:
            yield from image_payloads(child)


def test_real_extraction_outputs_artifacts_and_survives_restart(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service)
    with TestClient(create_app(settings)) as client:
        job_id = submit(client)
        job = completed(client, job_id)
        result_response = client.get(f"/v1/extractions/{job_id}/result")
        assert result_response.status_code == 200
        result = result_response.json()
        assert result["meta"]["algorithm_revision"] == "geometry-local-route-v12"
        assert result["image"]["width"] == 640 and result["image"]["height"] == 360
        symbols = [obj for obj in result["objects"] if obj["class"] == "general"]
        assert len(symbols) >= 2, result
        assert any(relation["type"] == "connected" for relation in result["relations"]), result
        trace_response = client.get(f"/v1/extractions/{job_id}/trace")
        assert trace_response.status_code == 200
        trace = trace_response.json()
        assert trace["candidates"] and trace["relation_candidates"]
        assert sum(stats["requests"] for stats in trace["jev"].values()) > 0
        assert sum(stats["errors"] for stats in trace["jev"].values()) == 0
        artifacts = job["artifacts"]
        names = list(artifacts) if isinstance(artifacts, dict) else [
            artifact["name"] if isinstance(artifact, dict) else artifact for artifact in artifacts]
        assert any(name.endswith("_overlay.png") for name in names), artifacts
        overlay_name = next(name for name in names if name.endswith("_overlay.png"))
        overlay = client.get(f"/v1/extractions/{job_id}/artifacts/{overlay_name}")
        assert overlay.status_code == 200
        assert overlay.content.startswith(b"\x89PNG\r\n\x1a\n")
        assert client.get(f"/v1/extractions/{job_id}/artifacts/job.json").status_code == 404
        calls_before_restart = decision_service.count()
        assert calls_before_restart > 0

    # A new API instance reads completed jobs from persistent storage.
    with TestClient(create_app(settings)) as client:
        assert client.get(f"/v1/extractions/{job_id}").json()["status"] == "succeeded"
        assert client.get(f"/v1/extractions/{job_id}/result").json() == result
        assert decision_service.count() == calls_before_restart

    # Image fields stay separate, encoded within their original nested slots.
    payloads = [image for request in decision_service.requests
                for image in image_payloads(request["body"])]
    assert payloads
    assert all(image["mime_type"] == "image/png" for image in payloads)
    assert all(base64.b64decode(image["data"]).startswith(b"\x89PNG") for image in payloads)


def test_endpoint_switch_does_not_reuse_other_models_cached_answers(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service)
    with TestClient(create_app(settings)) as client:
        completed(client, submit(client, "a"))
        first_calls = decision_service.count("decision-a")
        assert first_calls > 0
        completed(client, submit(client, "a"))
        assert decision_service.count("decision-a") == first_calls
        completed(client, submit(client, "b"))
        assert decision_service.count("decision-b") > 0
    same_id_new_endpoint = Backend(id="a", provider="decision_http",
                                   endpoint=decision_service.endpoint("decision-b"),
                                   model="same-fixture-model", concurrency=2, timeout_seconds=5)
    assert settings.backends["a"].cache_namespace() != same_id_new_endpoint.cache_namespace()


def test_corrupt_cached_answer_is_requeried_without_discarding_valid_cache(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service)
    with TestClient(create_app(settings)) as client:
        first_id = submit(client)
        completed(client, first_id)
        first_result = client.get(f"/v1/extractions/{first_id}/result").json()
        cache_entries = sorted((settings.data_dir / "cache").rglob("*.json"))
        assert len(cache_entries) > 1
        broken_entry = cache_entries[0]
        broken_entry.write_text('{"model":"interrupted-write","answer":')
        calls_before_repeat = decision_service.count()

        second_id = submit(client)
        second = completed(client, second_id)
        assert decision_service.count() == calls_before_repeat + 1
        assert second["summary"]["model_requests"] == 1
        assert second["summary"]["cached_questions"] > 0
        second_result = client.get(f"/v1/extractions/{second_id}/result").json()
        assert second_result["objects"] == first_result["objects"]
        assert second_result["relations"] == first_result["relations"]
        repaired_entry = json.loads(broken_entry.read_text())
        assert repaired_entry["model"] == "local-fixture-model"
        assert "answer" in repaired_entry


def test_invalid_upload_and_unknown_backend_are_rejected_without_model_calls(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service, max_upload_bytes=100_000,
                            max_image_pixels=640 * 360)
    with TestClient(create_app(settings)) as client:
        invalid = client.post("/v1/extractions", files={"image": ("bad.png", b"not an image", "image/png")})
        assert invalid.status_code in {400, 415, 422}, invalid.text
        too_large = client.post("/v1/extractions", files={"image": ("huge.png", b"x" * 100_001, "image/png")})
        assert too_large.status_code == 413, too_large.text
        unknown = client.post("/v1/extractions", data={"backend": "http://unregistered.invalid/decision"},
                              files={"image": ("drawing.png", drawing_bytes(), "image/png")})
        assert unknown.status_code in {400, 422}, unknown.text
        page = Image.new("RGB", (641, 360), "white")
        buffer = io.BytesIO()
        page.save(buffer, format="PNG")
        too_many_pixels = client.post("/v1/extractions", files={
            "image": ("too-many-pixels.png", buffer.getvalue(), "image/png")})
        assert too_many_pixels.status_code == 422, too_many_pixels.text
        no_other = client.post("/v1/extractions", data={"legend": json.dumps({"classes": [
            {"key": "only_component", "text": "A component."}]})}, files={
            "image": ("drawing.png", drawing_bytes(), "image/png")})
        assert no_other.status_code == 422, no_other.text
        assert client.get("/v1/extractions/not-a-job/result").status_code == 422
        assert client.get("/v1/extractions/00000000-0000-0000-0000-000000000000/result").status_code == 404
        assert decision_service.count() == 0


def test_invalid_model_answers_fail_job_but_preserve_partial_trace(tmp_path, decision_service):
    decision_service.malformed = True
    settings = api_settings(tmp_path, decision_service)
    with TestClient(create_app(settings)) as client:
        job_id = submit(client)
        job = terminal(client, job_id)
        assert job["status"] == "failed", job
        assert job["error"]["code"] == "decision_model_error", job
        assert client.get(f"/v1/extractions/{job_id}/result").status_code == 409
        trace = client.get(f"/v1/extractions/{job_id}/trace")
        assert trace.status_code == 200, trace.text
        assert sum(stats["errors"] for stats in trace.json()["jev"].values()) > 0


def test_restart_recovers_queued_jobs_and_marks_interrupted_jobs_failed(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service)
    with TestClient(create_app(settings)) as client:
        seed_id = submit(client)
        completed(client, seed_id)
    calls_after_seed = decision_service.count()
    # Seed the persisted states that remain after an unclean process stop.
    store = JobStore(settings.data_dir / "jobs.sqlite3")
    request = store.get(seed_id)["request"]
    interrupted_id = str(uuid4())
    store.create(interrupted_id, request, settings.max_pending_jobs)
    assert store.claim()["id"] == interrupted_id
    queued_id = str(uuid4())
    store.create(queued_id, request, settings.max_pending_jobs)
    queued_dir = settings.data_dir / "jobs" / queued_id
    queued_dir.mkdir()
    shutil.copyfile(settings.data_dir / "jobs" / seed_id / "input.png", queued_dir / "input.png")
    store.close()

    with TestClient(create_app(settings)) as client:
        interrupted = client.get(f"/v1/extractions/{interrupted_id}").json()
        assert interrupted["status"] == "failed"
        assert interrupted["error"]["code"] == "server_restarted"
        assert client.get(f"/v1/extractions/{interrupted_id}/result").status_code == 409
        queued = completed(client, queued_id)
        assert queued["summary"]["cached_questions"] > 0
        assert decision_service.count() == calls_after_seed


def test_job_timeout_terminates_worker_and_rejects_incomplete_result(tmp_path, decision_service):
    decision_service.gate = threading.Event()
    settings = api_settings(tmp_path, decision_service, job_timeout_seconds=1)
    with TestClient(create_app(settings)) as client:
        job_id = submit(client)
        job = terminal(client, job_id)
        assert job["status"] == "failed", job
        assert job["error"]["code"] == "extraction_timeout", job
        assert client.get(f"/v1/extractions/{job_id}/result").status_code == 409
        # The process was killed rather than leaving a live inference job.
        assert not (settings.data_dir / "jobs" / job_id / "_worker_result.json").exists()
    decision_service.gate.set()


def test_two_parallel_jobs_use_safe_shared_cache(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service, workers=2)
    with TestClient(create_app(settings)) as client:
        first_id = submit(client)
        second_id = submit(client)
        first = completed(client, first_id)
        second = completed(client, second_id)
        assert first["summary"]["symbols"] == second["summary"]["symbols"]
        assert first["summary"]["connections"] == second["summary"]["connections"]
        assert first["summary"]["connections"] > 0
        # Whichever subprocess gets the namespace lock first fills the cache;
        # the other completes using it without duplicate model requests.
        assert min(first["summary"]["model_requests"], second["summary"]["model_requests"]) == 0
        assert max(first["summary"]["cached_questions"], second["summary"]["cached_questions"]) > 0
        calls_after_both = decision_service.count()
        completed(client, submit(client))
        assert decision_service.count() == calls_after_both


def test_queue_limit_does_not_leave_orphan_uploads(tmp_path, decision_service):
    decision_service.gate = threading.Event()
    settings = api_settings(tmp_path, decision_service, max_pending_jobs=1)
    with TestClient(create_app(settings)) as client:
        first_id = submit(client)
        assert client.get(f"/v1/extractions/{first_id}/result").status_code == 409
        assert client.get(f"/v1/extractions/{first_id}/trace").status_code == 409
        rejected = client.post("/v1/extractions", data={"kind": "pid", "legend": LEGEND},
                               files={"image": ("rejected.png", drawing_bytes(), "image/png")})
        assert rejected.status_code == 429, rejected.text
        assert rejected.headers["Retry-After"] == "30"
        assert {entry.name for entry in (settings.data_dir / "jobs").iterdir()} == {first_id}
        decision_service.gate.set()
        completed(client, first_id)


def test_api_auth_is_separate_from_decision_backend_auth(tmp_path, decision_service):
    settings = api_settings(tmp_path, decision_service, api_key="fixture-extraction-secret")
    with TestClient(create_app(settings)) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/v1/backends").status_code == 401
        assert client.get("/v1/backends", headers={"Authorization": "Bearer wrong"}).status_code == 401
        malformed = client.get("/v1/backends", headers={"Authorization": b"Bearer wrong\xc3\xa9"})
        assert malformed.status_code == 401
        allowed = client.get("/v1/backends", headers={"Authorization": "Bearer fixture-extraction-secret"})
        assert allowed.status_code == 200
        assert "fixture-extraction-secret" not in allowed.text
        assert decision_service.count() == 0
