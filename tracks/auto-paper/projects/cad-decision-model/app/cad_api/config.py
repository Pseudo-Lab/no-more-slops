from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

PACKAGE_ROOT = Path(__file__).resolve().parent
SERVER_ROOT = PACKAGE_ROOT.parent
IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")
ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class Backend:
    id: str
    provider: str
    endpoint: str
    model: str
    api_key_env: str | None = None
    timeout_seconds: float = 90
    concurrency: int = 8
    max_request_tokens: int = 24_000

    def __post_init__(self):
        if not IDENTIFIER.fullmatch(self.id):
            raise ValueError("Invalid backend id")
        if self.provider not in {"typesafe", "decision_http"}:
            raise ValueError("Unsupported backend provider")
        url = urlsplit(self.endpoint)
        if url.scheme not in {"http", "https"} or not url.hostname or url.username or url.password or url.query or url.fragment:
            raise ValueError("Backend endpoint must be an HTTP(S) URL without embedded credentials, query or fragment")
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./:@+-]{0,199}', self.model) or '..' in self.model.split('/'):
            raise ValueError("Invalid model name")
        if self.api_key_env is not None and not ENV_NAME.fullmatch(self.api_key_env):
            raise ValueError("Invalid backend API-key environment variable")
        if self.provider == "typesafe" and not self.api_key_env:
            raise ValueError("TypeSafe requires api_key_env")
        if not 1 <= self.concurrency <= 32 or not 1 <= self.timeout_seconds <= 3600 or not 100 <= self.max_request_tokens <= 1_000_000:
            raise ValueError("Invalid backend execution limits")

    def ready(self) -> bool:
        return self.api_key_env is None or bool(os.environ.get(self.api_key_env, '').strip())

    def public(self) -> dict:
        return {"id": self.id, "provider": self.provider, "model": self.model, "endpoint": self.endpoint, "configured": self.ready()}

    def cache_namespace(self) -> str:
        # Different endpoints, model revisions and accounts cannot share answers.
        key_digest = hashlib.sha256(os.environ.get(self.api_key_env or '', '').encode()).hexdigest()
        value = {**asdict(self), "credential_digest": key_digest}
        return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    backends: dict[str, Backend]
    default_backend: str
    api_key: str | None = field(default=None, repr=False)
    workers: int = 1
    max_upload_bytes: int = 20 * 1024 * 1024
    max_image_pixels: int = 25_000_000
    max_pending_jobs: int = 32
    job_timeout_seconds: int = 1800
    resources_dir: Path = PACKAGE_ROOT / "resources"
    algorithm_revision: str = 'geometry-local-route-v12'

    def __post_init__(self):
        if self.default_backend not in self.backends:
            raise ValueError("Default backend is not registered")
        if self.algorithm_revision not in {'geometry-local-route-v12', 'geometry-local-route-v13-connections', 'geometry-local-route-v14-graph', 'geometry-local-route-v15-semantics'}:
            raise ValueError('Unsupported extraction revision')
        if not 1 <= self.workers <= 8 or min(self.max_upload_bytes, self.max_image_pixels, self.max_pending_jobs, self.job_timeout_seconds) < 1:
            raise ValueError("Invalid API execution limits")

    @classmethod
    def from_env(cls) -> Settings:
        # Existing local credentials remain in their original .env file.
        load_dotenv(SERVER_ROOT / '.env', override=False)
        load_dotenv(SERVER_ROOT.parent / '.env', override=False)
        config_file = os.environ.get('CAD_MODEL_BACKENDS_FILE')
        if config_file:
            config = json.loads(Path(config_file).expanduser().read_text())
            records = config['backends']
            default = config['default_backend']
        else:
            default = 'default'
            provider = os.environ.get('CAD_MODEL_PROVIDER', 'typesafe')
            records = [{"id": default, "provider": provider,
                        "endpoint": os.environ.get('CAD_MODEL_ENDPOINT', 'https://api.typesafe.ai'),
                        "model": os.environ.get('CAD_MODEL_NAME', 'jev-1.14.0'),
                        "api_key_env": os.environ.get('CAD_MODEL_API_KEY_ENV', 'TYPESAFE_API_KEY') if provider == 'typesafe' else os.environ.get('CAD_MODEL_API_KEY_ENV'),
                        "timeout_seconds": float(os.environ.get('CAD_MODEL_TIMEOUT_SECONDS', '90')),
                        "concurrency": int(os.environ.get('CAD_MODEL_CONCURRENCY', '8')),
                        "max_request_tokens": int(os.environ.get('CAD_MODEL_MAX_REQUEST_TOKENS', '24000'))}]
        backends = {record['id']: Backend(**record) for record in records}
        if len(backends) != len(records):
            raise ValueError("Duplicate backend ids")
        return cls(data_dir=Path(os.environ.get('CAD_DATA_DIR', str(SERVER_ROOT / 'data'))).expanduser().resolve(),
                   backends=backends, default_backend=default,
                   api_key=os.environ.get('CAD_API_KEY') or None,
                   workers=int(os.environ.get('CAD_WORKERS', '1')),
                   max_upload_bytes=int(os.environ.get('CAD_MAX_UPLOAD_BYTES', str(20 * 1024 * 1024))),
                   max_image_pixels=int(os.environ.get('CAD_MAX_IMAGE_PIXELS', '25000000')),
                   max_pending_jobs=int(os.environ.get('CAD_MAX_PENDING_JOBS', '32')),
                   job_timeout_seconds=int(os.environ.get('CAD_JOB_TIMEOUT_SECONDS', '1800')),
                   resources_dir=Path(os.environ.get('CAD_RESOURCES_DIR', str(PACKAGE_ROOT / 'resources'))).expanduser().resolve(),
                   algorithm_revision=os.environ.get('CAD_ALGORITHM_REVISION', 'geometry-local-route-v15-semantics'))
