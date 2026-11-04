from __future__ import annotations

import asyncio
import fcntl
import json
import os
import signal
import sys
from contextlib import suppress
from pathlib import Path

from .config import Settings
from .storage import JobStore

ARTIFACTS = frozenset({'input.png', 'input_output.json', 'input_trace.json', 'input.html', 'input_overlay.png', 'input_objects.png', 'input_steps.png', 'summary.md', 'input_review.png', 'input_review.json'})


class JobManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.store: JobStore | None = None
        self.wake = asyncio.Event()
        self.tasks: list[asyncio.Task] = []
        self.lock_file = None

    async def start(self):
        root = self.settings.data_dir
        (root / 'jobs').mkdir(parents=True, exist_ok=True)
        (root / 'cache').mkdir(exist_ok=True)
        self.lock_file = (root / 'server.lock').open('a')
        try:
            fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock_file.close()
            self.lock_file = None
            raise RuntimeError('This data directory is already used by another API process. Run one Uvicorn worker.') from None
        self.store = JobStore(root / 'jobs.sqlite3')
        self.store.recover()
        self.tasks = [asyncio.create_task(self.loop()) for _ in range(self.settings.workers)]
        self.wake.set()

    async def stop(self):
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        if self.store:
            self.store.close()
        if self.lock_file:
            fcntl.flock(self.lock_file, fcntl.LOCK_UN)
            self.lock_file.close()

    def directory(self, job_id: str) -> Path:
        return self.settings.data_dir / 'jobs' / job_id

    async def loop(self):
        while True:
            job = self.store.claim()
            if job is None:
                with suppress(TimeoutError):
                    await asyncio.wait_for(self.wake.wait(), timeout=1)
                self.wake.clear()
                continue
            try:
                await self.run(job)
            except asyncio.CancelledError:
                raise
            except Exception:
                self.store.finish(job['id'], error={'code': 'worker_failed', 'message': 'Could not start or complete the extraction worker.'})

    @staticmethod
    async def terminate(process):
        if process.returncode is None:
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGTERM)
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except TimeoutError:
                with suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGKILL)
                await process.wait()

    async def run(self, job: dict):
        directory = self.directory(job['id'])
        spec = {**job['request'], 'job_id': job['id'], 'job_dir': str(directory),
                'api_pid': os.getpid(),
                'resources_dir': str(self.settings.resources_dir),
                'algorithm_revision': job['request'].get('algorithm_revision', self.settings.algorithm_revision),
                'cache_dir': str(self.settings.data_dir / 'cache' / job['request']['cache_namespace'])}
        (directory / '_worker_spec.json').write_text(json.dumps(spec))
        process = None
        with (directory / '_worker.log').open('wb') as log:
            try:
                process = await asyncio.create_subprocess_exec(sys.executable, '-m', 'cad_api.worker', str(directory / '_worker_spec.json'),
                                                               stdout=log, stderr=log, start_new_session=True)
                await asyncio.wait_for(process.wait(), timeout=self.settings.job_timeout_seconds)
            except TimeoutError:
                if process:
                    await self.terminate(process)
                self.store.finish(job['id'], error={'code': 'extraction_timeout', 'message': 'Extraction exceeded the configured job timeout.'})
                return
            except asyncio.CancelledError:
                if process:
                    await self.terminate(process)
                self.store.finish(job['id'], error={'code': 'server_stopped', 'message': 'The server stopped during extraction. Submit a new job.'})
                raise
        error_file = directory / '_worker_error.json'
        if process.returncode != 0 or error_file.exists():
            error = json.loads(error_file.read_text()) if error_file.exists() else {'code': 'extraction_failed', 'message': 'Extraction did not complete.'}
            self.store.finish(job['id'], error=error)
            return
        summary = json.loads((directory / '_worker_result.json').read_text())
        self.store.finish(job['id'], summary=summary)

