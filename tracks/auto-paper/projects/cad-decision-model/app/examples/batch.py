"""Resume folder extraction jobs and build a gallery from their actual artifacts.

Example: python examples/batch.py ../image --out downloaded-folder --kind auto
Submitting a job can incur model charges. This script never retries a failed or
ambiguous submission automatically; GET/download retries do not submit jobs.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import html
import json
import math
import os
import shutil
import time
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit
from uuid import UUID, uuid4

import httpx
from PIL import Image, ImageOps

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
ARTIFACT_NAMES = {"input.png", "input_output.json", "input_trace.json", "input.html",
                  "input_overlay.png", "input_objects.png", "input_steps.png", "summary.md",
                  "input_review.png", "input_review.json"}
ACTIVE = {"queued", "running"}
TERMINAL = {"succeeded", "failed", "submission_unknown"}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_bytes(path: Path, content: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        with temporary.open("wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_json(path: Path, value):
    atomic_bytes(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode())


def scan_images(folder: Path):
    files = []
    originals = {}
    for path in sorted(folder.iterdir(), key=lambda value: value.name):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        originals.setdefault(digest, path.name)
        files.append({"name": path.name, "sha256": digest, "canonical": originals[digest],
                      "duplicate": path.name != originals[digest]})
    if not files:
        raise ValueError("No PNG/JPEG images were found in the folder")
    return files


def safe_server(value: str):
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Server must be an HTTP(S) URL without credentials, query or fragment")
    _ = parsed.port
    return value.rstrip("/")


def elapsed(created, updated):
    try:
        return max(0.0, (datetime.fromisoformat(updated) - datetime.fromisoformat(created)).total_seconds())
    except (TypeError, ValueError):
        return None


class BatchPaused(Exception):
    """The saved manifest is safe to resume after the read-only problem is fixed."""


class BatchRunner:
    def __init__(self, folder: Path, out: Path, client, *, server="http://127.0.0.1:8087",
                 kind="auto", backend=None, max_running=1, rate_per_million=.042,
                 retry_failed=False, poll_seconds=2):
        self.folder, self.out = folder.resolve(), out.resolve()
        self.client = client
        self.server, self.kind, self.backend = safe_server(server), kind, backend
        if kind not in {"auto", "pid", "logic"} or not 1 <= max_running <= 32 or not math.isfinite(rate_per_million) or rate_per_million < 0 or poll_seconds < 0:
            raise ValueError("Invalid batch execution settings")
        self.max_running, self.poll_seconds = max_running, poll_seconds
        self.rate = rate_per_million
        self.retry_failed = retry_failed
        self.manifest_path = self.out / "manifest.json"
        self.out.mkdir(parents=True, exist_ok=True)
        self.data = self.load()

    def load(self):
        config = {"folder": str(self.folder), "server": self.server, "kind": self.kind, "backend": self.backend}
        if self.manifest_path.exists():
            data = json.loads(self.manifest_path.read_text())
            if data.get("version") != 1 or any(data.get(key) != value for key, value in config.items()):
                raise ValueError("Existing manifest belongs to another folder/server/kind/backend; use its original settings or a separate output folder")
        else:
            data = {"version": 1, **config, "started_at": utc_now(), "items": {}}
        data["rate_per_million_usd"] = self.rate
        data["files"] = scan_images(self.folder)
        for file in data["files"]:
            item = data["items"].setdefault(file["sha256"], {
                "sha256": file["sha256"], "canonical": file["canonical"],
                "status": "pending", "job_id": None, "downloaded": False, "history": []})
            item["canonical"] = file["canonical"]
            if item["status"] == "submitting" and not item.get("job_id"):
                item["status"] = "submission_unknown"
                item["error"] = {"code": "submission_unknown", "message": "A previous POST was interrupted before its job ID was saved. Check the API job store before submitting again."}
            if self.retry_failed and item["status"] == "failed":
                item["history"].append({key: item.get(key) for key in ("job_id", "status", "error", "metrics")})
                item.update(status="pending", job_id=None, downloaded=False)
                for key in ("job", "metrics", "error", "download_error", "artifacts"):
                    item.pop(key, None)
            source = self.out / "sources" / (file["sha256"] + Path(file["canonical"]).suffix.lower())
            file["source"] = source.relative_to(self.out).as_posix()
            if not source.exists():
                atomic_bytes(source, (self.folder / file["canonical"]).read_bytes())
        return data

    def items(self):
        seen = set()
        for file in self.data["files"]:
            if file["sha256"] not in seen:
                seen.add(file["sha256"])
                yield self.data["items"][file["sha256"]]

    @contextmanager
    def exclusive(self):
        lock = (self.out / ".batch.lock").open("a")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            lock.close()
            raise ValueError("Another batch process is already using this output folder") from None
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()

    def persist(self):
        self.data["updated_at"] = utc_now()
        self.data["summary"] = self.summary()
        atomic_json(self.manifest_path, self.data)
        atomic_bytes(self.out / "index.html", self.gallery().encode())

    def summary(self):
        items = list(self.items())
        counts = Counter(item["status"] for item in items)
        attempts = [attempt for item in self.data["items"].values() for attempt in [*item.get("history", []), item]]
        usage = {key: sum((attempt.get("metrics") or {}).get(key) or 0 for attempt in attempts)
                 for key in ("input_tokens", "model_requests", "cached_questions", "model_errors")}
        reported = sum((attempt.get("metrics") or {}).get("input_tokens") is not None for attempt in attempts)
        return {"files": len(self.data["files"]), "unique_images": len(items),
                "duplicate_files": len(self.data["files"]) - len(items), "status_counts": dict(counts),
                **usage, "tokens_reporting_jobs": reported,
                "estimated_cost_usd": usage["input_tokens"] * self.rate / 1_000_000,
                "rate_per_million_usd": self.rate,
                "cost_basis": "Model-reported input tokens in downloaded traces; cached answers add no tokens. Estimate only, not an invoice. Failed requests without usage are excluded.",
                "wall_elapsed_seconds": elapsed(self.data["started_at"], self.data.get("updated_at", utc_now()))}

    def submit(self, item):
        item.update(status="submitting", error=None)
        self.persist()  # Record intent before the possibly paid POST.
        form = {"kind": self.kind}
        if self.backend:
            form["backend"] = self.backend
        try:
            with (self.folder / item["canonical"]).open("rb") as image:
                response = self.client.post("/v1/extractions", data=form,
                                            files={"image": (item["canonical"], image)})
            if response.status_code in {429, 503}:
                item.update(status="pending", error={"code": "server_not_ready", "message": f"API rejected submission with HTTP {response.status_code}; rerun when ready."})
                self.persist()
                raise BatchPaused("API queue/backend is unavailable; progress is saved")
            if 400 <= response.status_code < 500:
                item.update(status="failed", error={"code": "submission_rejected", "http_status": response.status_code,
                                                     "message": "The API rejected this image before creating a job."})
                self.persist()
                return
            response.raise_for_status()
            job = response.json()
            UUID(job["id"])
            if job["status"] not in ACTIVE | {"succeeded", "failed"}:
                raise ValueError("Unexpected API job status")
        except BatchPaused:
            raise
        except (httpx.HTTPError, ValueError, KeyError):
            item.update(status="submission_unknown", error={"code": "submission_unknown",
                "message": "The POST outcome is unknown. Check the API job store before submitting this image again."})
            self.persist()
            return
        item.update(job_id=job["id"], status=job["status"], job=job, error=job.get("error"))
        self.persist()

    def poll(self, item):
        try:
            response = self.client.get(f"/v1/extractions/{item['job_id']}")
            response.raise_for_status()
            job = response.json()
            if job["id"] != item["job_id"] or job["status"] not in ACTIVE | {"succeeded", "failed"}:
                raise ValueError("Unexpected API job status")
        except (httpx.HTTPError, ValueError, KeyError):
            item["poll_error"] = "Could not read this saved job; rerun after restoring API access. No job was resubmitted."
            self.persist()
            raise BatchPaused("Could not read a saved API job") from None
        item.update(status=job["status"], job=job, error=job.get("error"))
        item.pop("poll_error", None)
        self.persist()

    def download(self, item):
        directory = self.out / "jobs" / item["sha256"]
        directory.mkdir(parents=True, exist_ok=True)
        previous = directory / "job.json"
        if previous.exists():
            previous_id = json.loads(previous.read_text())["id"]
            if previous_id != item["job_id"]:
                UUID(previous_id)
                archive = directory / "attempts" / previous_id
                archive.mkdir(parents=True, exist_ok=True)
                for name in ARTIFACT_NAMES | {"job.json", "overlay-thumbnail.jpg"}:
                    old = directory / name
                    if old.is_file():
                        shutil.move(str(old), archive / name)
        atomic_json(directory / "job.json", item["job"])
        downloaded = []
        try:
            for artifact in item["job"].get("artifacts", []):
                name = artifact["name"]
                if name not in ARTIFACT_NAMES or Path(name).name != name:
                    raise ValueError("Unsafe artifact filename")
                path = directory / name
                if not path.exists():
                    # Construct our own same-API route; do not trust a returned URL.
                    response = self.client.get(f"/v1/extractions/{item['job_id']}/artifacts/{name}")
                    response.raise_for_status()
                    atomic_bytes(path, response.content)
                downloaded.append(path.relative_to(self.out).as_posix())
            item.update(downloaded=True, artifacts=downloaded)
            item.pop("download_error", None)
        except (httpx.HTTPError, ValueError, KeyError, OSError):
            item.update(downloaded=False, artifacts=downloaded,
                        download_error="Artifacts could not all be downloaded safely. Rerunning resumes downloads without submitting this job again.")
        trace = None
        trace_file = directory / "input_trace.json"
        if trace_file.exists():
            try:
                trace = json.loads(trace_file.read_text())
            except (ValueError, OSError):
                item["download_error"] = "Downloaded trace is not valid JSON; review the API artifact."
                item["downloaded"] = False
        stats = trace.get("jev", {}) if isinstance(trace, dict) else None
        job_summary = item["job"].get("summary") or {}
        metrics = {key: job_summary.get(key) for key in ("symbols", "text_regions", "connections", "containments")}
        metrics["elapsed_seconds"] = elapsed(item["job"].get("created_at"), item["job"].get("updated_at"))
        for target, stage_key, fallback in (("input_tokens", "tokens", None), ("model_requests", "requests", job_summary.get("model_requests")),
                                            ("cached_questions", "cached", job_summary.get("cached_questions")), ("model_errors", "errors", None)):
            metrics[target] = sum(stage.get(stage_key, 0) for stage in stats.values()) if isinstance(stats, dict) else fallback
        item["metrics"] = metrics
        self.persist()

    def run(self):
        with self.exclusive():
            # Refresh after acquiring the process lock to avoid using a stale manifest.
            self.data = self.load()
            self.persist()
            attempted_downloads = set()
            while True:
                for item in self.items():
                    if item["status"] in ACTIVE:
                        self.poll(item)
                for item in self.items():
                    if item["status"] in {"succeeded", "failed"} and item.get("job") and not item.get("downloaded") and item["sha256"] not in attempted_downloads:
                        attempted_downloads.add(item["sha256"])
                        self.download(item)
                capacity = self.max_running - sum(item["status"] in ACTIVE for item in self.items())
                for item in self.items():
                    if capacity <= 0:
                        break
                    if item["status"] == "pending":
                        self.submit(item)
                        if item["status"] in ACTIVE:
                            capacity -= 1
                if all(item["status"] in TERMINAL for item in self.items()):
                    # A job can already be terminal in its POST response.
                    for item in self.items():
                        if item["status"] in {"succeeded", "failed"} and item.get("job") and not item.get("downloaded") and item["sha256"] not in attempted_downloads:
                            attempted_downloads.add(item["sha256"])
                            self.download(item)
                    self.data["finished_at"] = utc_now()
                    self.persist()
                    return 1 if any(item["status"] != "succeeded" or item.get("download_error") for item in self.items()) else 0
                time.sleep(self.poll_seconds)

    def thumbnail(self, source: Path, destination: Path):
        if destination.exists():
            return destination.relative_to(self.out).as_posix()
        try:
            with Image.open(source) as original:
                image = ImageOps.exif_transpose(original).convert("RGB")
                image.thumbnail((640, 400))
                destination.parent.mkdir(parents=True, exist_ok=True)
                image.save(destination, format="JPEG", quality=88)
            return destination.relative_to(self.out).as_posix()
        except (OSError, ValueError):
            return source.relative_to(self.out).as_posix()

    @staticmethod
    def connection_review(directory: Path):
        """Read saved review evidence without another request (also works offline)."""
        for name in ("input_review.json", "input_output.json"):
            try:
                value = json.loads((directory / name).read_text())
            except (OSError, ValueError):
                continue
            if name == "input_output.json" and isinstance(value, dict):
                value = value.get("connection_review")
            if isinstance(value, dict) and isinstance(value.get("summary"), dict):
                return value
        return None

    def gallery(self):
        viewer_css = Path(__file__).with_name('gallery_viewer.css').read_text()
        viewer_js = Path(__file__).with_name('gallery_viewer.js').read_text()
        summary = self.summary()
        labels = {"pending": "대기", "submitting": "접수 중", "queued": "대기 중", "running": "추출 중",
                  "succeeded": "완료", "failed": "실패", "submission_unknown": "접수 결과 확인 필요"}
        active = any(item["status"] in {"pending", "submitting"} | ACTIVE for item in self.items())
        refresh = '<meta http-equiv="refresh" content="10">' if active else ""
        cards = []
        has_review = False
        for file in self.data["files"]:
            item = self.data["items"][file["sha256"]]
            revision = item.get('connection_revision') or {}
            original_directory = self.out / "jobs" / file["sha256"]
            baseline_directory = self.out / revision['baseline_directory'] if revision.get('baseline_directory') else original_directory
            directory = self.out / revision['directory'] if revision.get('directory') else original_directory
            overlay = directory / "input_overlay.png"
            source = self.out / file["source"]
            record = directory / "job.json"
            try:
                current_artifacts = record.exists() and json.loads(record.read_text()).get("id") == item.get("job_id")
            except (OSError, ValueError):
                current_artifacts = False
            if current_artifacts and overlay.exists():
                image = self.thumbnail(overlay, directory / "overlay-thumbnail.jpg")
                image_label = "추출 결과" if item["status"] == "succeeded" else "부분 결과"
                full_result = overlay.relative_to(self.out).as_posix()
            else:
                image = self.thumbnail(source, self.out / "sources" / (file["sha256"] + "-thumbnail.jpg"))
                image_label = "원본"
                full_result = ''
            normalized = directory / 'input.png'
            full_original = normalized.relative_to(self.out).as_posix() if current_artifacts and normalized.exists() else file['source']
            full_baseline = (baseline_directory / 'input_overlay.png').relative_to(self.out).as_posix() if revision and (baseline_directory / 'input_overlay.png').exists() else ''
            review = self.connection_review(directory) if current_artifacts else None
            review_image = directory / 'input_review.png'
            full_review = review_image.relative_to(self.out).as_posix() if review and review_image.exists() else ''
            has_review = has_review or bool(review)
            review_summary = review.get('summary', {}) if review else {}
            def review_count(key):
                value = review.get('visualization', {}).get('displayed_port_marker_groups', review_summary.get(key)) if review and key == 'unresolved_ports' else review_summary.get(key)
                return str(value) if type(value) is int and value >= 0 else ''
            pending_count, unresolved_ports = review_count('review_needed_candidates'), review_count('unresolved_ports')
            review_counts = []
            if pending_count:
                review_counts.append(f'검토 필요 {int(pending_count):,}개')
            if unresolved_ports:
                review_counts.append(f'접점 표시 {int(unresolved_ports):,}개')
            review_detail = f'<p class="review-counts">{", ".join(review_counts)}</p>' if review_counts else ''
            links = [f'<a href="{quote(file["source"])}">원본</a>']
            for name, label in (("input.html", "결과 보기"), ("input_output.json", "JSON"), ("input_trace.json", "판단 기록"),
                                ("input_review.json", "검토 기록")):
                path = directory / name
                if current_artifacts and path.exists():
                    links.append(f'<a href="{quote(path.relative_to(self.out).as_posix())}">{label}</a>')
            metrics = item.get("metrics") or {}
            counts = ", ".join(f"{label} {metrics[key]:,}" for key, label in
                                (("symbols", "심볼"), ("connections", "확정 연결" if review else "연결"),
                                 ("text_regions", "글자 영역")) if metrics.get(key) is not None)
            duplicate = f'<p class="duplicate">중복 원본: {html.escape(file["canonical"])}</p>' if file["duplicate"] else ""
            error = item.get("download_error") or (item.get("error") or {}).get("message") or item.get("poll_error")
            detail = f'<p class="error">{html.escape(error)}</p>' if error else ""
            if revision:
                detail += '<p class="duplicate">연결 보완 적용, 객체와 글자 결과는 동일</p>'
            seconds = metrics.get("elapsed_seconds")
            duration = f'<span>{seconds:.1f}초 (대기 포함)</span>' if seconds is not None else ""
            cards.append(f'''<article data-name="{html.escape(file['name'].lower(), quote=True)}" data-status="{item['status']}">
<button type="button" class="preview" data-original="{quote(full_original)}" data-result="{quote(full_result)}" data-baseline="{quote(full_baseline)}" data-review="{quote(full_review)}" data-review-count="{pending_count}" data-unresolved-ports="{unresolved_ports}" aria-label="{html.escape(file['name'], quote=True)} 크게 보기" title="크게 보기"><img loading="lazy" src="{quote(image)}" alt="{html.escape(file['name'], quote=True)}"><span>{image_label}</span></button>
<div class="body"><div class="row"><h2>{html.escape(file['name'])}</h2><span class="status {item['status']}">{labels[item['status']]}</span></div>
{duplicate}<p class="counts">{counts or '추출 수치가 아직 없습니다'}</p>{review_detail}<div class="links">{' '.join(links)}{duration}</div>{detail}</div></article>''')
        counts = summary["status_counts"]
        totals = [("완료", counts.get("succeeded", 0)), ("진행 중", counts.get("running", 0) + counts.get("queued", 0) + counts.get("submitting", 0)),
                  ("대기", counts.get("pending", 0)), ("실패", counts.get("failed", 0)), ("접수 확인 필요", counts.get("submission_unknown", 0))]
        total_html = "".join(f'<div><span>{label}</span><strong>{count}</strong></div>' for label, count in totals)
        review_note = '<p class="review-note"><span class="review-swatch" aria-hidden="true"></span>주황색 경로와 원은 확인이 필요한 후보 경로, 접점, 선 끝입니다. 검토 후보는 확정 연결 수에 포함하지 않습니다.</p>' if has_review else ''
        return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{refresh}
<title>도면 폴더 추출 결과</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f7fa;color:#172b44;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif}}main{{max-width:1320px;margin:auto;padding:40px 28px 64px}}h1{{font-size:30px;letter-spacing:-.8px;margin:0 0 6px}}.intro{{margin:0;color:#55677d}}.totals{{display:flex;gap:36px;flex-wrap:wrap;padding:24px 0 18px;border-bottom:1px solid #dce3ec}}.totals span{{display:block;color:#63738a;font-size:13px}}.totals strong{{font-size:27px}}.usage{{margin:18px 0;color:#40566e}}.note{{font-size:12px;color:#62738a}}.toolbar{{display:flex;gap:12px;margin:26px 0 20px}}input,select{{font:inherit;padding:11px 14px;border:1px solid #cdd8e5;border-radius:8px;background:white;color:#172b44}}input{{flex:1;min-width:0}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}}article{{background:white;border:1px solid #dce3ec;border-radius:10px;overflow:hidden}}.preview{{height:230px;background:#edf1f6;position:relative;padding:12px}}.preview img{{width:100%;height:100%;object-fit:contain}}.preview>span{{position:absolute;bottom:10px;right:10px;font-size:11px;background:#fffffff0;border-radius:4px;padding:3px 7px;color:#4f6177}}.body{{padding:16px}}.row{{display:flex;gap:10px;align-items:start;justify-content:space-between}}h2{{font-size:15px;margin:0;overflow-wrap:anywhere}}.status{{white-space:nowrap;font-size:11px;padding:3px 7px;border-radius:5px;background:#edf1f6;color:#55677d}}.succeeded{{background:#e8f3ee;color:#286649}}.running,.queued{{background:#eaf0fa;color:#365c95}}.failed{{background:#faeded;color:#934b4b}}.submission_unknown{{background:#f4eee4;color:#78613f}}.counts{{margin:12px 0;font-size:13px;color:#465c74}}.links{{display:flex;flex-wrap:wrap;gap:12px;font-size:12px}}a{{color:#254f81;text-decoration:none}}a:hover{{text-decoration:underline}}.links span{{color:#62738a}}.duplicate{{margin:6px 0;font-size:12px;color:#64758b}}.error{{font-size:12px;overflow-wrap:anywhere;color:#7b5959;margin-bottom:0}}[hidden]{{display:none!important}}footer{{margin-top:30px;color:#718095;font-size:12px}}@media(max-width:980px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media(max-width:620px){{main{{padding:28px 16px}}.grid{{grid-template-columns:1fr}}.toolbar{{flex-direction:column}}.totals{{gap:20px}}h1{{font-size:25px}}}}
{viewer_css}
</style></head><body><main><h1>도면 폴더 추출 결과</h1><p class="intro">심볼과 글자 영역, 연결 경로를 원본 위에 표시합니다.</p><p class="intro">{summary['files']}개 파일, 서로 다른 원본 {summary['unique_images']}개, 중복 파일 {summary['duplicate_files']}개</p>
<div class="totals">{total_html}</div><div class="usage">모델 보고 입력 토큰 <strong>{summary['input_tokens']:,}</strong>, 예상 비용 <strong>${summary['estimated_cost_usd']:.6f}</strong><br><span class="note">1M 입력 토큰당 ${self.rate:g}로 계산했습니다. 청구 금액이 아니며, 사용량이 보고되지 않은 실패 요청은 포함하지 않습니다. 토큰 기록 {summary['tokens_reporting_jobs']}건, 중복 파일은 한 번만 계산하고 명시적으로 재시도한 작업은 비용에 포함합니다.</span></div>
{review_note}
<div class="toolbar"><input id="search" type="search" placeholder="파일 이름 검색" aria-label="파일 이름 검색"><select id="filter" aria-label="상태 선택"><option value="">전체 상태</option><option value="succeeded">완료</option><option value="running">추출 중</option><option value="queued">대기 중</option><option value="pending">대기</option><option value="failed">실패</option><option value="submission_unknown">접수 확인 필요</option></select></div>
<section class="grid">{''.join(cards)}</section><footer>최근 기록: {html.escape(self.data.get('updated_at', utc_now()))}, {'진행 중에는 10초마다 새로고침합니다' if active else '배치 처리가 종료되었습니다'}, API 작업 시간에는 대기가 포함됩니다</footer></main>
<dialog id="image-viewer" aria-labelledby="viewer-title">
<div class="viewer-header"><h2 id="viewer-title"></h2><button type="button" data-action="close">닫기</button></div>
<div class="viewer-toolbar">
<div class="viewer-group"><button type="button" data-action="previous" aria-label="이전 이미지">←</button><button type="button" data-action="next" aria-label="다음 이미지">→</button></div>
<div class="viewer-group viewer-modes"><button type="button" data-action="original" aria-pressed="false">원본</button><button type="button" data-action="baseline" aria-pressed="false" hidden>개선 전</button><button type="button" data-action="result" aria-pressed="true">추출 결과</button><button type="button" data-action="review" aria-pressed="false" hidden>검토 필요</button></div>
<div class="viewer-group"><button type="button" data-action="zoom-out" aria-label="축소">−</button><output id="viewer-zoom" aria-live="polite">100%</output><button type="button" data-action="zoom-in" aria-label="확대">+</button><button type="button" data-action="fit">화면에 맞춤</button><button type="button" data-action="actual">100%</button></div>
<span id="viewer-position"></span></div>
<p id="viewer-review-status" class="viewer-review-status" aria-live="polite" hidden></p>
<div id="viewer-stage" aria-label="확대한 도면" aria-busy="false"><img id="viewer-image" alt="" draggable="false"><p id="viewer-error" hidden>이미지를 열지 못했습니다</p></div>
<p class="viewer-hint">드래그로 이동, 휠로 확대하거나 축소, Esc로 닫기</p>
</dialog>
<script>const galleryStorage={{getItem(key){{try{{return sessionStorage.getItem(key)}}catch{{return null}}}},setItem(key,value){{try{{sessionStorage.setItem(key,value)}}catch{{}}}}}};const search=document.getElementById('search'),filter=document.getElementById('filter');function apply(){{const query=search.value.toLowerCase(),status=filter.value;document.querySelectorAll('article').forEach(card=>card.hidden=!card.dataset.name.includes(query)||(status&&card.dataset.status!==status));galleryStorage.setItem('cad-gallery-search',search.value);galleryStorage.setItem('cad-gallery-filter',filter.value)}}search.value=galleryStorage.getItem('cad-gallery-search')||'';filter.value=galleryStorage.getItem('cad-gallery-filter')||'';search.addEventListener('input',apply);filter.addEventListener('change',apply);apply();
{viewer_js}
</script></body></html>'''


def main(argv=None):
    parser = argparse.ArgumentParser(description="Extract each unique image through the API and build a resumable local gallery")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--server", default="http://127.0.0.1:8087")
    parser.add_argument("--kind", choices=("auto", "pid", "logic"), default="auto")
    parser.add_argument("--backend")
    parser.add_argument("--max-running", type=int, default=1)
    parser.add_argument("--poll-seconds", type=float, default=2)
    parser.add_argument("--rate-per-million", type=float, default=.042, help="USD per million model-reported input tokens; estimate only")
    parser.add_argument("--retry-failed", action="store_true", help="Explicitly submit failed images again; this can incur additional model charges")
    args = parser.parse_args(argv)
    key = os.environ.get("CAD_API_KEY")
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    try:
        with httpx.Client(base_url=safe_server(args.server), headers=headers, timeout=60) as client:
            runner = BatchRunner(args.folder, args.out, client, server=args.server, kind=args.kind, backend=args.backend,
                                 max_running=args.max_running, rate_per_million=args.rate_per_million,
                                 retry_failed=args.retry_failed, poll_seconds=args.poll_seconds)
            code = runner.run()
            print(json.dumps(runner.data["summary"], ensure_ascii=False, indent=2))
            print(f"Gallery: {runner.out / 'index.html'}")
            return code
    except BatchPaused as error:
        print(f"Paused: {error}. Rerun the same command to resume saved jobs.")
        return 2
    except KeyboardInterrupt:
        print("Stopped waiting. Submitted API jobs remain saved; rerun the same command to resume.")
        return 130
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
