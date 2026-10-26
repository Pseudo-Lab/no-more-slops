"""Submit a drawing, wait for completion, and download its artifacts."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=Path)
    parser.add_argument('--server', default='http://127.0.0.1:8087')
    parser.add_argument('--backend')
    parser.add_argument('--kind', choices=['pid', 'logic', 'auto'], default='pid')
    parser.add_argument('--out', type=Path, default=Path('downloaded'))
    parser.add_argument('--wait-seconds', type=int, default=3600)
    args = parser.parse_args()
    key = os.environ.get('CAD_API_KEY')
    headers = {'Authorization': f'Bearer {key}'} if key else {}
    with httpx.Client(base_url=args.server.rstrip('/'), headers=headers, timeout=60) as client:
        form = {'kind': args.kind}
        if args.backend:
            form['backend'] = args.backend
        with args.image.open('rb') as image:
            submitted = client.post('/v1/extractions', data=form, files={'image': (args.image.name, image)})
        submitted.raise_for_status()
        job = submitted.json()
        deadline = time.monotonic() + args.wait_seconds
        while job['status'] not in {'succeeded', 'failed'}:
            if time.monotonic() >= deadline:
                raise SystemExit(f"Wait timeout; job remains available at {job['status_url']}")
            time.sleep(1)
            response = client.get(job['status_url'])
            response.raise_for_status()
            job = response.json()
        directory = args.out / job['id']
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'job.json').write_text(json.dumps(job, ensure_ascii=False, indent=2))
        for artifact in job['artifacts']:
            name = artifact['name']
            if Path(name).name != name:
                raise SystemExit('Invalid artifact filename from API')
            downloaded = client.get(artifact['url'])
            downloaded.raise_for_status()
            (directory / name).write_bytes(downloaded.content)
        if job['status'] == 'failed':
            raise SystemExit(f"Extraction failed: {job['error']['code']}; available records: {directory}")
        print(json.dumps({'id': job['id'], 'summary': job['summary'], 'downloaded': str(directory)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
