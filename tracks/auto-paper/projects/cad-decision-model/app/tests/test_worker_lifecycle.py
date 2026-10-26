"""Isolated child processes prove crash cleanup without touching the live API."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from contextlib import suppress
from pathlib import Path

import pytest


CHILD_PROGRAM = """
import os, sys, time
from pathlib import Path
from cad_api.worker import start_parent_watchdog
start_parent_watchdog(int(sys.argv[1]))
heartbeat = Path(sys.argv[2])
counter = 0
while True:
    heartbeat.write_text(str(counter))
    counter += 1
    time.sleep(.05)
"""


PARENT_PROGRAM = """
import json, os, subprocess, sys, time
from pathlib import Path
pid_file, heartbeat, child_program = sys.argv[1:]
child = subprocess.Popen([sys.executable, '-c', child_program, str(os.getpid()), heartbeat])
Path(pid_file).write_text(json.dumps({'parent': os.getpid(), 'child': child.pid}))
while True:
    time.sleep(1)
"""


def wait_for(path: Path, timeout=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists() and path.stat().st_size:
            return
        time.sleep(.025)
    pytest.fail(f"Test child did not create {path.name}")


@pytest.mark.skipif(os.name != "posix", reason="The production worker uses POSIX process isolation")
def test_watchdog_stops_orphan_worker_after_only_its_parent_is_killed(tmp_path):
    pid_file = tmp_path / "test-processes.json"
    heartbeat = tmp_path / "child-heartbeat.txt"
    parent = subprocess.Popen([sys.executable, "-c", PARENT_PROGRAM,
                               str(pid_file), str(heartbeat), CHILD_PROGRAM],
                              start_new_session=True, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    try:
        wait_for(pid_file)
        wait_for(heartbeat)
        created = json.loads(pid_file.read_text())
        assert created["parent"] == parent.pid
        assert created["child"] != parent.pid
        assert parent.poll() is None
        first_heartbeat = heartbeat.stat().st_mtime_ns
        time.sleep(.15)
        assert heartbeat.stat().st_mtime_ns != first_heartbeat

        # Kill the parent alone. The child must notice this itself; the test
        # does not signal the child until the unconditional cleanup below.
        killed_at = time.monotonic()
        parent.kill()
        parent.wait(timeout=3)
        last_heartbeat = heartbeat.stat().st_mtime_ns
        unchanged_since = time.monotonic()
        deadline = killed_at + 3
        while time.monotonic() < deadline:
            time.sleep(.05)
            current = heartbeat.stat().st_mtime_ns
            if current != last_heartbeat:
                last_heartbeat = current
                unchanged_since = time.monotonic()
            elif time.monotonic() - unchanged_since >= .75:
                break
        else:
            pytest.fail("Orphan worker continued its heartbeat after API parent death")
        assert time.monotonic() - killed_at < 3
    finally:
        if parent.poll() is None:
            parent.kill()
            parent.wait(timeout=3)
        # This process group contains only this test's parent and child. It
        # also cleans up the child if the watchdog assertion itself fails.
        with suppress(ProcessLookupError):
            os.killpg(parent.pid, signal.SIGKILL)


def test_worker_rejects_parent_pid_mismatch_before_starting_extraction(tmp_path):
    specification = tmp_path / "invalid-parent.json"
    specification.write_text(json.dumps({"api_pid": 0, "job_dir": str(tmp_path)}))
    worker = subprocess.run([sys.executable, "-m", "cad_api.worker", str(specification)],
                            capture_output=True, timeout=5)
    assert worker.returncode == 4
    assert not (tmp_path / "_worker_error.json").exists()
    assert not (tmp_path / "_worker_result.json").exists()
