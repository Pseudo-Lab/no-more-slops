#!/usr/bin/env python3
"""App Store 배포용 프로비저닝 프로파일을 API로 만들어 이 Mac에 설치한다.

앱 관리(App Manager) 역할의 API 키로는 Xcode의 자동 서명이 클라우드 인증서·프로파일을 만들지 못해
`xcodebuild -exportArchive`가 "Cloud signing permission error / No profiles for '<번들 ID>' were found"로 멈춘다.
이때 키체인의 Apple Distribution 인증서(Xcode › Settings › Accounts › Manage Certificates › + 로 사용자가 만든다)와
이 스크립트로 만든 프로파일로 직접 서명한다.

  python3 -I app_store_profile.py --bundle-id com.example.app --name "Example App Store"

설치 뒤 ExportOptions.plist에 아래 값을 쓴다.
  signingStyle = manual, signingCertificate = Apple Distribution,
  provisioningProfiles = { <번들 ID> = <프로파일 이름> }
"""
import argparse
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asc import call, error_detail, paginate, query  # noqa: E402

PROFILE_DIR = os.path.expanduser("~/Library/Developer/Xcode/UserData/Provisioning Profiles")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--name", required=True, help="프로파일 이름 (ExportOptions에 같은 이름을 쓴다)")
    args = parser.parse_args()

    bundles = list(paginate(query("/v1/bundleIds", **{"filter[identifier]": args.bundle_id})))
    if not bundles:
        sys.exit(f"{args.bundle_id}가 등록되지 않았다 (developer.apple.com › Identifiers에서 등록한다)")
    certificates = list(paginate(query("/v1/certificates", **{"filter[certificateType]": "DISTRIBUTION"})))
    if not certificates:
        sys.exit("배포 인증서가 없다. Xcode › Settings › Accounts › Manage Certificates › + › Apple Distribution으로 만든다.")

    existing = [p for p in paginate(f"/v1/bundleIds/{bundles[0]['id']}/profiles")
                if p["attributes"]["name"] == args.name and p["attributes"]["profileState"] == "ACTIVE"]
    if existing:
        status, result = call("GET", f"/v1/profiles/{existing[0]['id']}")
        profile = result["data"]
    else:
        status, result = call("POST", "/v1/profiles", {"data": {"type": "profiles",
            "attributes": {"name": args.name, "profileType": "IOS_APP_STORE"},
            "relationships": {"bundleId": {"data": {"type": "bundleIds", "id": bundles[0]["id"]}},
                              "certificates": {"data": [{"type": "certificates", "id": c["id"]} for c in certificates]}}}})
        if status >= 300:
            sys.exit(f"프로파일 만들기 실패: {status} {error_detail(result)}")
        profile = result["data"]
    attributes = profile["attributes"]
    os.makedirs(PROFILE_DIR, exist_ok=True)
    path = os.path.join(PROFILE_DIR, f"{attributes['uuid']}.mobileprovision")
    with open(path, "wb") as file:
        file.write(base64.b64decode(attributes["profileContent"]))
    print(f"설치함: {attributes['name']} ({attributes['uuid']}), 만료 {attributes['expirationDate'][:10]}")


if __name__ == "__main__":
    main()
