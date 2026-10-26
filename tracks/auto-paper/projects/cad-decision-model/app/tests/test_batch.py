"""Folder orchestration tests never call a paid Decision Model."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

from cad_api.app import create_app
from test_api import LocalDecisionService, api_settings, drawing_bytes

SPEC = importlib.util.spec_from_file_location("cad_batch_example", Path(__file__).resolve().parents[1] / "examples" / "batch.py")
BATCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BATCH)


def make_folder(path: Path):
    path.mkdir()
    source = drawing_bytes()
    (path / "a.png").write_bytes(source)
    (path / "b-alias.png").write_bytes(source)
    with Image.open(io.BytesIO(source)) as raw:
        image = raw.convert("RGB")
        ImageDraw.Draw(image).rectangle((25, 25, 32, 32), fill="black")
        image.save(path / "c.png")
    return path


def test_real_api_batch_deduplicates_downloads_every_artifact_and_resumes(tmp_path):
    service = LocalDecisionService()
    folder = make_folder(tmp_path / "images")
    settings = api_settings(tmp_path / "api", service)
    out = tmp_path / "gallery"
    try:
        with TestClient(create_app(settings)) as client:
            runner = BATCH.BatchRunner(folder, out, client, poll_seconds=.01)
            assert runner.run() == 0
            summary = runner.data["summary"]
            assert summary["files"] == 3
            assert summary["unique_images"] == 2
            assert summary["duplicate_files"] == 1
            assert summary["status_counts"] == {"succeeded": 2}
            ids = {item["job_id"] for item in runner.items()}
            assert len(ids) == 2
            assert runner.data["files"][0]["sha256"] == runner.data["files"][1]["sha256"]
            for item in runner.items():
                directory = out / "jobs" / item["sha256"]
                job = json.loads((directory / "job.json").read_text())
                for artifact in job["artifacts"]:
                    assert (directory / artifact["name"]).is_file(), artifact
                assert (directory / "input.png").is_file()
                assert (directory / "input_overlay.png").is_file()
                assert (directory / "overlay-thumbnail.jpg").is_file()
                assert item["metrics"]["input_tokens"] > 0
            page = (out / "index.html").read_text()
            assert page.count("<article ") == 3
            assert "중복 원본: a.png" in page
            assert "input.html" in page and "input_output.json" in page and "input_trace.json" in page
            assert 'http-equiv="refresh"' not in page
            assert summary["estimated_cost_usd"] == pytest.approx(summary["input_tokens"] * .042 / 1_000_000)
            calls = service.count()
            resumed = BATCH.BatchRunner(folder, out, client, poll_seconds=.01)
            assert resumed.run() == 0
            assert {item["job_id"] for item in resumed.items()} == ids
            assert service.count() == calls
    finally:
        service.close()


class MockAPI:
    def __init__(self, *, fail_first=False, ambiguous=False, unsafe_artifact=False, review_artifacts=False):
        self.posts = 0
        self.jobs = {}
        self.fail_first, self.ambiguous, self.unsafe_artifact = fail_first, ambiguous, unsafe_artifact
        self.review_artifacts = review_artifacts
        self.requested_urls = []

    def handle(self, request):
        self.requested_urls.append(str(request.url))
        if request.method == "POST":
            self.posts += 1
            if self.ambiguous:
                raise httpx.ReadTimeout("Fixture interrupted POST", request=request)
            job_id = str(uuid4())
            failed = self.fail_first and self.posts == 1
            names = ["input.png", "input_trace.json"] if failed else ["input.png", "input_output.json", "input_trace.json", "input_overlay.png", "input.html"]
            if self.review_artifacts and not failed:
                names += ["input_review.png", "input_review.json"]
            if self.unsafe_artifact:
                names = ["../private.json"]
            job = {"id": job_id, "status": "failed" if failed else "succeeded",
                   "created_at": "2026-10-25T00:00:00+00:00", "updated_at": "2026-10-25T00:00:02+00:00",
                   "summary": None if failed else {"symbols": 2, "connections": 1, "text_regions": 0,
                                                   "containments": 0, "model_requests": 1, "cached_questions": 0},
                   "error": {"code": "fixture_failure", "message": "Fixture model failed"} if failed else None,
                   "artifacts": [{"name": name, "url": "https://untrusted.invalid/private"} for name in names]}
            self.jobs[job_id] = job
            return httpx.Response(202, json={**job, "status": "queued"})
        parts = request.url.path.strip("/").split("/")
        job = self.jobs[parts[2]]
        if len(parts) == 3:
            return httpx.Response(200, json=job)
        name = parts[-1]
        if name == "input_trace.json":
            return httpx.Response(200, json={"jev": {"fixture": {"requests": 1, "tokens": 100, "cached": 0,
                                                                   "errors": int(job["status"] == "failed")}}})
        if name == "input_output.json":
            return httpx.Response(200, json={"objects": [{"id": "fixture-symbol"}], "relations": []})
        if name == "input_review.json":
            return httpx.Response(200, json={"schema": "connection-review-v1", "candidates": [
                {"id": "fixture-pending", "state": "review_needed"}], "summary": {
                "confirmed_candidates": 1, "review_needed_candidates": 1, "rejected_candidates": 0,
                "unresolved_ports": 2}})
        if name == "input.html":
            return httpx.Response(200, text="<!doctype html><html><body>Fixture viewer</body></html>")
        return httpx.Response(200, content=drawing_bytes())


def one_image(tmp_path):
    folder = tmp_path / "images"
    folder.mkdir()
    (folder / "one.png").write_bytes(drawing_bytes())
    return folder


def test_failed_jobs_need_explicit_retry_and_prior_usage_is_retained(tmp_path):
    api = MockAPI(fail_first=True)
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        first = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert first.run() == 1
        first_id = next(first.items())["job_id"]
        assert api.posts == 1
        assert BATCH.BatchRunner(folder, out, client, poll_seconds=0).run() == 1
        assert api.posts == 1
        retry = BATCH.BatchRunner(folder, out, client, retry_failed=True, poll_seconds=0)
        assert retry.run() == 0
        assert api.posts == 2
        item = next(retry.items())
        assert item["job_id"] != first_id
        assert item["history"][0]["job_id"] == first_id
        assert retry.data["summary"]["input_tokens"] == 200
        directory = out / "jobs" / item["sha256"]
        assert (directory / "attempts" / first_id / "input_trace.json").is_file()
        assert json.loads((directory / "job.json").read_text())["id"] == item["job_id"]


def test_unknown_post_outcome_is_never_automatically_resubmitted(tmp_path):
    api = MockAPI(ambiguous=True)
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        first = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert first.run() == 1
        assert next(first.items())["status"] == "submission_unknown"
        assert api.posts == 1
        resumed = BATCH.BatchRunner(folder, out, client, retry_failed=True, poll_seconds=0)
        assert resumed.run() == 1
        assert api.posts == 1


def test_artifact_paths_and_urls_cannot_escape_the_configured_api(tmp_path):
    api = MockAPI(unsafe_artifact=True)
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        runner = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert runner.run() == 1
        assert next(runner.items())["download_error"]
        assert not (out / "private.json").exists()
        assert all("untrusted.invalid" not in url for url in api.requested_urls)


def test_interrupted_submission_intent_resumes_as_unknown_not_a_new_post(tmp_path):
    api = MockAPI()
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        runner = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        next(runner.items())["status"] = "submitting"
        runner.persist()
        assert 'http-equiv="refresh" content="10"' in (out / "index.html").read_text()
        resumed = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert resumed.run() == 1
        assert api.posts == 0
        assert next(resumed.items())["status"] == "submission_unknown"


def test_resume_rejects_different_backend_or_server(tmp_path):
    api = MockAPI()
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        runner = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        runner.persist()
        with pytest.raises(ValueError, match="another folder/server/kind/backend"):
            BATCH.BatchRunner(folder, out, client, backend="different")
        with pytest.raises(ValueError, match="another folder/server/kind/backend"):
            BATCH.BatchRunner(folder, out, client, server="http://127.0.0.1:9999")


def test_review_artifacts_are_downloaded_offline_counts_do_not_inflate_connections(tmp_path):
    api = MockAPI(review_artifacts=True)
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        runner = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert runner.run() == 0
        item = next(runner.items())
        directory = out / "jobs" / item["sha256"]
        assert (directory / "input_review.png").is_file()
        assert (directory / "input_review.json").is_file()
        assert item["metrics"]["connections"] == 1
        page = (out / "index.html").read_text()
        assert f'data-review="jobs/{item["sha256"]}/input_review.png"' in page
        assert 'data-review-count="1" data-unresolved-ports="2"' in page
        assert '연결 1' in page and '검토 필요 1개, 접점 표시 2개' in page
        assert '확정 연결 수에 포함하지 않습니다' in page
        assert 'data-action="review"' in page and '검토 기록' in page
        # The viewer uses embedded paths and counts, with no browser fetch that
        # would require an HTTP origin when the user opens the downloaded HTML.
        assert 'fetch(' not in Path(BATCH.__file__).with_name('gallery_viewer.js').read_text()


def test_review_gallery_compares_active_revision_with_explicit_previous_revision(tmp_path):
    api = MockAPI()
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        runner = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert runner.run() == 0
        item = next(runner.items())
        original = out / "jobs" / item["sha256"]
        previous = out / "revisions" / "v13" / item["sha256"]
        current = out / "revisions" / "v14" / item["sha256"]
        previous.mkdir(parents=True)
        current.mkdir(parents=True)
        (previous / "input_overlay.png").write_bytes(drawing_bytes())
        for name in ('job.json', 'input.png', 'input_overlay.png'):
            (current / name).write_bytes((original / name).read_bytes())
        (current / "input_review.png").write_bytes(drawing_bytes())
        review = {"schema": "connection-review-v1", "summary": {
            "confirmed_candidates": 1, "review_needed_candidates": 4,
            "rejected_candidates": 3, "unresolved_ports": 0}}
        # Output fallback remains supported if a saved review JSON is unavailable.
        (current / "input_output.json").write_text(json.dumps({"connection_review": review}))
        item['connection_revision'] = {
            'directory': current.relative_to(out).as_posix(),
            'baseline_directory': previous.relative_to(out).as_posix()}
        page = runner.gallery()
        assert f'data-result="revisions/v14/{item["sha256"]}/input_overlay.png"' in page
        assert f'data-baseline="revisions/v13/{item["sha256"]}/input_overlay.png"' in page
        assert f'data-review="revisions/v14/{item["sha256"]}/input_review.png"' in page
        assert 'data-review-count="4" data-unresolved-ports="0"' in page
        assert '検討' not in page


def test_old_gallery_has_no_review_counts_or_state_explanation(tmp_path):
    api = MockAPI()
    folder, out = one_image(tmp_path), tmp_path / "out"
    with httpx.Client(base_url="http://127.0.0.1:8087", transport=httpx.MockTransport(api.handle)) as client:
        runner = BATCH.BatchRunner(folder, out, client, poll_seconds=0)
        assert runner.run() == 0
        page = runner.gallery()
        assert 'data-review="" data-review-count="" data-unresolved-ports=""' in page
        assert '<p class="review-counts">' not in page
        assert '확정 연결 수에 포함하지 않습니다' not in page
        assert 'data-action="review" aria-pressed="false" hidden' in page
