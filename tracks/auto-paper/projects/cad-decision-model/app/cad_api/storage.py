from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class QueueFull(Exception):
    pass


class JobStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('''CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY, status TEXT NOT NULL, created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL, request TEXT NOT NULL,
            summary TEXT, error TEXT
        )''')
        self.db.commit()

    @staticmethod
    def decode(row) -> dict | None:
        if row is None:
            return None
        value = dict(row)
        for key in ('request', 'summary', 'error'):
            value[key] = json.loads(value[key]) if value[key] else None
        return value

    def get(self, job_id: str) -> dict | None:
        with self.lock:
            return self.decode(self.db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone())

    def create(self, job_id: str, request: dict, limit: int):
        with self.lock, self.db:
            active = self.db.execute("SELECT COUNT(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
            if active >= limit:
                raise QueueFull()
            stamp = now()
            self.db.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?)',
                            (job_id, 'queued', stamp, stamp, json.dumps(request), None, None))

    def recover(self):
        with self.lock, self.db:
            self.db.execute("UPDATE jobs SET status='failed', updated_at=?, error=? WHERE status='running'",
                            (now(), json.dumps({'code': 'server_restarted', 'message': 'The server stopped during extraction. Submit a new job.'})))

    def claim(self) -> dict | None:
        with self.lock, self.db:
            row = self.db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY created_at LIMIT 1").fetchone()
            if row is None:
                return None
            self.db.execute("UPDATE jobs SET status='running', updated_at=? WHERE id=?", (now(), row['id']))
            return self.get(row['id'])

    def finish(self, job_id: str, *, summary: dict | None = None, error: dict | None = None):
        with self.lock, self.db:
            self.db.execute('UPDATE jobs SET status=?, updated_at=?, summary=?, error=? WHERE id=?',
                            ('failed' if error else 'succeeded', now(), json.dumps(summary) if summary else None,
                             json.dumps(error) if error else None, job_id))

    def close(self):
        with self.lock:
            self.db.close()

