from __future__ import annotations

import hashlib
import hmac
import io
import json
import re
import shutil
from contextlib import asynccontextmanager
from typing import Annotated, Literal
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from PIL import Image, ImageOps, UnidentifiedImageError

from .config import Settings
from .jobs import ARTIFACTS, JobManager
from .storage import QueueFull


def parse_legend(value: str | None) -> dict | None:
    if value is None:
        return None
    if len(value) > 256_000:
        raise HTTPException(413, 'Legend is too large')
    try:
        data = json.loads(value)
        if not isinstance(data, dict) or set(data) != {'classes'} or not isinstance(data['classes'], list):
            raise ValueError()
        classes = data['classes']
        if not 2 <= len(classes) <= 255:
            raise ValueError()
        seen = set()
        for entry in classes:
            if not isinstance(entry, dict) or set(entry) != {'key', 'text'}:
                raise ValueError()
            key, text = entry['key'], entry['text']
            if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_/: .-]{0,79}', key) or key in seen:
                raise ValueError()
            if not isinstance(text, str) or not 1 <= len(text) <= 8000:
                raise ValueError()
            seen.add(key)
        if 'other' not in seen:
            raise ValueError()
        return data
    except (ValueError, TypeError, KeyError):
        raise HTTPException(422, 'Legend must contain 2–255 unique classes with key and text, including other. Image/path fields are not accepted.') from None


async def normalize_image(upload: UploadFile, settings: Settings) -> tuple[bytes, dict]:
    blob = bytearray()
    while chunk := await upload.read(1024 * 1024):
        blob.extend(chunk)
        if len(blob) > settings.max_upload_bytes:
            raise HTTPException(413, 'Image exceeds the configured upload limit')
    if not blob:
        raise HTTPException(422, 'Image is empty')
    original_digest = hashlib.sha256(blob).hexdigest()
    try:
        with Image.open(io.BytesIO(blob)) as check:
            if check.format not in {'PNG', 'JPEG'}:
                raise HTTPException(415, 'Only PNG and JPEG images are supported')
            if check.width < 32 or check.height < 32 or check.width * check.height > settings.max_image_pixels:
                raise HTTPException(422, 'Image dimensions are outside the configured limits')
            check.verify()
        with Image.open(io.BytesIO(blob)) as raw:
            image = ImageOps.exif_transpose(raw)
            if image.mode in {'RGBA', 'LA'} or 'transparency' in image.info:
                rgba = image.convert('RGBA')
                image = Image.alpha_composite(Image.new('RGBA', rgba.size, (255, 255, 255, 255)), rgba).convert('RGB')
            elif image.mode not in {'L', 'RGB'}:
                image = image.convert('RGB')
            encoded = io.BytesIO()
            image.save(encoded, format='PNG')
            data = encoded.getvalue()
            return data, {'width': image.width, 'height': image.height, 'input_sha256': original_digest,
                          'normalized_input_sha256': hashlib.sha256(data).hexdigest()}
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        raise HTTPException(422, 'Cannot decode this image') from None
    finally:
        await upload.close()


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    manager = JobManager(settings)

    @asynccontextmanager
    async def lifespan(app):
        await manager.start()
        try:
            yield
        finally:
            await manager.stop()

    app = FastAPI(title='CAD Decision Extraction API', version='0.1.0', lifespan=lifespan,
                  description='Submit one drawing and retrieve its extracted graph, decision trace and visualizations. Versioned connection checks include review candidates and drawing notation evidence. Decision Model services are configured separately.')
    app.state.manager = manager
    app.state.settings = settings

    def authorize(authorization: Annotated[str | None, Header()] = None):
        if settings.api_key:
            value = authorization[7:] if authorization and authorization.startswith('Bearer ') else ''
            if not hmac.compare_digest(value.encode('utf-8'), settings.api_key.encode('utf-8')):
                raise HTTPException(401, 'Invalid API credentials', headers={'WWW-Authenticate': 'Bearer'})

    auth = [Depends(authorize)]

    def get_job(job_id: UUID) -> dict:
        job = manager.store.get(str(job_id))
        if job is None:
            raise HTTPException(404, 'Extraction job not found')
        return job

    def public_job(job: dict) -> dict:
        base = f"/v1/extractions/{job['id']}"
        request = job['request']
        artifacts = []
        if job['status'] in {'succeeded', 'failed'}:
            artifacts = [{'name': name, 'url': f'{base}/artifacts/{name}'} for name in sorted(ARTIFACTS)
                         if (manager.directory(job['id']) / name).is_file()]
        return {'id': job['id'], 'status': job['status'], 'created_at': job['created_at'], 'updated_at': job['updated_at'],
                'kind': request['kind'], 'backend': request['backend']['id'], 'model': request['backend']['model'],
                'original_filename': request['original_filename'], 'width': request['width'], 'height': request['height'],
                'summary': job['summary'], 'error': job['error'], 'artifacts': artifacts,
                'status_url': base, 'result_url': base + '/result', 'trace_url': base + '/trace'}

    @app.get('/health')
    def health():
        return {'status': 'ok', 'algorithm_revision': settings.algorithm_revision}

    @app.get('/v1/backends', dependencies=auth)
    def backends():
        return {'default_backend': settings.default_backend, 'backends': [b.public() for b in settings.backends.values()]}

    @app.post('/v1/extractions', status_code=202, dependencies=auth)
    async def submit(image: Annotated[UploadFile, File(description='One PNG/JPEG drawing')],
                     kind: Annotated[Literal['pid', 'logic', 'auto'], Form()] = 'pid',
                     backend: Annotated[str | None, Form(description='Registered backend id; endpoint/key are server-side')] = None,
                     legend: Annotated[str | None, Form(description='Optional JSON: classes with key/text and an other class')] = None):
        selected = settings.backends.get(backend or settings.default_backend)
        if selected is None:
            await image.close()
            raise HTTPException(422, 'Unknown backend id')
        if not selected.ready():
            await image.close()
            raise HTTPException(503, 'The selected model backend is missing its configured API key')
        custom_legend = parse_legend(legend)
        data, metadata = await normalize_image(image, settings)
        job_id = str(uuid4())
        directory = manager.directory(job_id)
        directory.mkdir(mode=0o700)
        original_filename = (image.filename or 'drawing').replace('\\', '/').split('/')[-1]
        original_filename = ''.join(c for c in original_filename if c.isprintable())[:180]
        request = {**metadata, 'kind': kind, 'backend': selected.__dict__, 'original_filename': original_filename,
                   'legend': custom_legend, 'cache_namespace': selected.cache_namespace(),
                   'algorithm_revision': settings.algorithm_revision}
        try:
            (directory / 'input.png').write_bytes(data)
            manager.store.create(job_id, request, settings.max_pending_jobs)
        except QueueFull:
            shutil.rmtree(directory)
            raise HTTPException(429, 'Extraction queue is full; retry later', headers={'Retry-After': '30'}) from None
        except Exception:
            shutil.rmtree(directory)
            raise
        manager.wake.set()
        return public_job(manager.store.get(job_id))

    @app.get('/v1/extractions/{job_id}', dependencies=auth)
    def status(job_id: UUID):
        return public_job(get_job(job_id))

    @app.get('/v1/extractions/{job_id}/result', dependencies=auth)
    def result(job_id: UUID):
        job = get_job(job_id)
        if job['status'] != 'succeeded':
            raise HTTPException(409, {'message': 'No successful result is available', 'status': job['status'], 'error': job['error']})
        return json.loads((manager.directory(job['id']) / 'input_output.json').read_text())

    @app.get('/v1/extractions/{job_id}/trace', dependencies=auth)
    def trace(job_id: UUID):
        job = get_job(job_id)
        path = manager.directory(job['id']) / 'input_trace.json'
        if job['status'] not in {'succeeded', 'failed'} or not path.is_file():
            raise HTTPException(409, 'Trace is not available yet')
        return json.loads(path.read_text())

    @app.get('/v1/extractions/{job_id}/artifacts/{name}', dependencies=auth)
    def artifact(job_id: UUID, name: str):
        job = get_job(job_id)
        if name not in ARTIFACTS:
            raise HTTPException(404, 'Artifact not found')
        path = manager.directory(job['id']) / name
        if job['status'] not in {'succeeded', 'failed'} or not path.is_file():
            raise HTTPException(404, 'Artifact not found')
        return FileResponse(path, filename=name)

    return app
