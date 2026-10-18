#!/usr/bin/env python3
"""App Store Connect API 클라이언트. 표준 라이브러리와 openssl만 쓴다.

환경 변수
  ASC_KEY_ID      키 ID (예: 373UJ786UZ)
  ASC_ISSUER_ID   Issuer ID (UUID, 사용자 및 액세스 › 통합 › App Store Connect API 맨 위)
  ASC_KEY_PATH    .p8 파일 경로 (저장소 밖에 둔다)

명령줄
  python3 -I asc.py GET '/v1/apps?filter[bundleId]=com.example.app'
  python3 -I asc.py PATCH /v1/apps/123 '{"data": {...}}'

다른 스크립트에서는 `from asc import call, paginate`로 쓴다.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.appstoreconnect.apple.com"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def der_to_raw(der: bytes) -> bytes:
    """openssl이 내는 ECDSA 서명(DER: SEQUENCE{INTEGER r, INTEGER s})을 JWT가 쓰는 r||s(각 32바이트)로 바꾼다."""
    if der[0] != 0x30:
        raise ValueError("not a DER sequence")
    i = 2 if der[1] < 0x80 else 2 + (der[1] & 0x7F)
    out = b""
    for _ in range(2):
        if der[i] != 0x02:
            raise ValueError("expected DER integer")
        length = der[i + 1]
        value = der[i + 2:i + 2 + length].lstrip(b"\x00")
        if len(value) > 32:
            raise ValueError("integer longer than 32 bytes")
        out += value.rjust(32, b"\x00")
        i += 2 + length
    return out


def token(key_id: str, issuer: str, key_path: str, lifetime: int = 900) -> str:
    """ES256 JWT (최대 20분). 키 내용은 읽어서 출력하지 않는다."""
    header = b64url(json.dumps({"alg": "ES256", "kid": key_id, "typ": "JWT"}).encode())
    now = int(time.time())
    payload = b64url(json.dumps({"iss": issuer, "iat": now, "exp": now + lifetime, "aud": "appstoreconnect-v1"}).encode())
    signing_input = f"{header}.{payload}".encode()
    der = subprocess.run(["openssl", "dgst", "-sha256", "-sign", key_path],
                         input=signing_input, capture_output=True, check=True).stdout
    return f"{header}.{payload}.{b64url(der_to_raw(der))}"


def _credentials():
    try:
        return os.environ["ASC_KEY_ID"], os.environ["ASC_ISSUER_ID"], os.path.expanduser(os.environ["ASC_KEY_PATH"])
    except KeyError as missing:
        sys.exit(f"환경 변수 {missing}가 필요하다 (ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_PATH)")


def _request(method: str, path: str, body=None):
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token(*_credentials()),
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            text = response.read().decode()
            return response.status, (json.loads(text) if text else {})
    except urllib.error.HTTPError as error:
        text = error.read().decode()
        try:
            return error.code, json.loads(text)
        except ValueError:
            return error.code, {"raw": text}


def call(method: str, path: str, body=None, retries: int = 6):
    """요청 한 번. 429(요청 과다)면 5·10·20·40·60초 기다렸다 다시 보낸다."""
    for attempt in range(retries):
        status, result = _request(method, path, body)
        if status != 429:
            return status, result
        time.sleep(min(60, 5 * 2 ** attempt))
    return status, result


def paginate(path: str):
    """목록 API의 모든 페이지 data를 차례로 돌려준다."""
    while path:
        status, result = call("GET", path)
        if status >= 300:
            raise RuntimeError(f"GET {path} → {status} {error_detail(result)}")
        yield from result.get("data", [])
        path = (result.get("links") or {}).get("next")


def error_detail(result) -> str:
    errors = result.get("errors") if isinstance(result, dict) else None
    if not errors:
        return ""
    first = errors[0]
    return first.get("detail") or first.get("title") or first.get("code") or ""


def query(path: str, **params) -> str:
    """'filter[bundleId]' 같은 대괄호 파라미터를 인코딩한 경로."""
    return path + ("?" + urllib.parse.urlencode(params) if params else "")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help") else 1)
    method, path = sys.argv[1].upper(), sys.argv[2]
    body = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    status, result = call(method, path, body)
    print(status)
    print(json.dumps(result, ensure_ascii=False, indent=1))
