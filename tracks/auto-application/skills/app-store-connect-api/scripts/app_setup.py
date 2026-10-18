#!/usr/bin/env python3
"""App Store Connect 앱 설정을 API로 한다. 모든 명령은 다시 실행해도 같은 결과가 되도록 만들었다.

  python3 -I app_setup.py check --bundle-id com.example.app
  python3 -I app_setup.py age-rating --bundle-id com.example.app --advertising
  python3 -I app_setup.py content-rights --bundle-id com.example.app --uses-third-party
  python3 -I app_setup.py pricing --bundle-id com.example.app --free --exclude CHN
  python3 -I app_setup.py attach-build --bundle-id com.example.app --build 9
  python3 -I app_setup.py testflight --bundle-id com.example.app --group "Internal"

앱 레코드 만들기, 앱 개인정보(App Privacy) 설문, 계약·세금·은행, 심사 제출은 이 스크립트가 하지 않는다.
"""
import argparse
import itertools
import os
import sys

# python3 -I는 스크립트 폴더를 import 경로에 넣지 않는다.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asc import call, error_detail, paginate, query  # noqa: E402

AGE_RATING_LEVELS = [
    "alcoholTobaccoOrDrugUseOrReferences", "contests", "gamblingSimulated", "gunsOrOtherWeapons",
    "medicalOrTreatmentInformation", "profanityOrCrudeHumor", "sexualContentGraphicAndNudity",
    "sexualContentOrNudity", "horrorOrFearThemes", "matureOrSuggestiveThemes", "violenceCartoonOrFantasy",
    "violenceRealisticProlongedGraphicOrSadistic", "violenceRealistic",
]
AGE_RATING_FLAGS = [
    "advertising", "ageAssurance", "gambling", "healthOrWellnessTopics", "lootBox", "messagingAndChat",
    "parentalControls", "unrestrictedWebAccess", "userGeneratedContent", "socialMedia", "socialMediaAgeRestricted",
]


def app_for(bundle_id):
    apps = list(paginate(query("/v1/apps", **{"filter[bundleId]": bundle_id})))
    if not apps:
        sys.exit(f"App Store Connect에 {bundle_id} 앱이 없다. 앱 레코드는 웹에서 직접 만든다 (API로 만들 수 없다).")
    return apps[0]


def editable_app_info(app_id):
    infos = list(paginate(f"/v1/apps/{app_id}/appInfos"))
    for info in infos:
        if info["attributes"].get("state") in ("PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED", "WAITING_FOR_REVIEW"):
            return info
    return infos[0]


def editable_version(app_id):
    for version in paginate(query(f"/v1/apps/{app_id}/appStoreVersions", **{"filter[platform]": "IOS"})):
        if version["attributes"].get("appStoreState") in ("PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED", "METADATA_REJECTED"):
            return version
    sys.exit("편집할 수 있는 버전이 없다 (제출 준비 중인 버전을 먼저 만든다)")


def must(status, result, what):
    if status >= 300:
        sys.exit(f"{what} 실패: {status} {error_detail(result)}")
    return result


def cmd_check(args):
    app = app_for(args.bundle_id)
    app_id = app["id"]
    print(f"앱: {app['attributes']['name']} (id {app_id}, sku {app['attributes'].get('sku')})")
    bundles = list(paginate(query("/v1/bundleIds", **{"filter[identifier]": args.bundle_id})))
    print("번들 ID 등록:", "예" if bundles else "아니요 (developer.apple.com에서 등록하거나 API로 만든다)")
    info = editable_app_info(app_id)
    status, rating = call("GET", f"/v1/appInfos/{info['id']}?fields[appInfos]=appStoreAgeRating,state")
    print("앱 정보:", rating.get("data", {}).get("attributes"))
    version = editable_version(app_id)
    status, detail = call("GET", f"/v1/appStoreVersions/{version['id']}?include=build")
    builds = [i["attributes"].get("version") for i in detail.get("included", [])]
    print(f"버전 {version['attributes']['versionString']} {version['attributes']['appStoreState']} · 연결된 빌드 {builds or '없음'}")
    for build in itertools.islice(paginate(query("/v1/builds", **{"filter[app]": app_id, "sort": "-uploadedDate", "limit": 3})), 3):
        a = build["attributes"]
        print(f"  빌드 {a['version']} {a['processingState']} {a['uploadedDate']}")
    status, rights = call("GET", f"/v1/apps/{app_id}?fields[apps]=contentRightsDeclaration")
    print("콘텐츠 권한:", rights.get("data", {}).get("attributes", {}).get("contentRightsDeclaration") or "미응답")
    for group in paginate(f"/v1/apps/{app_id}/subscriptionGroups"):
        for sub in paginate(f"/v1/subscriptionGroups/{group['id']}/subscriptions"):
            print(f"  구독 {sub['attributes']['productId']}: {sub['attributes']['state']}")
    for iap in paginate(f"/v1/apps/{app_id}/inAppPurchasesV2"):
        print(f"  앱 내 구입 {iap['attributes']['productId']}: {iap['attributes']['state']}")
    print("참고: 구독의 API 상태가 MISSING_METADATA여도 웹의 구독 화면에서 '심사에 추가' 버튼이 켜져 있으면 빠진 칸이 없는 것이다.")


def cmd_age_rating(args):
    app = app_for(args.bundle_id)
    info = editable_app_info(app["id"])
    status, declaration = call("GET", f"/v1/appInfos/{info['id']}/ageRatingDeclaration")
    declaration_id = must(status, declaration, "연령 등급 조회")["data"]["id"]
    attributes = {key: "NONE" for key in AGE_RATING_LEVELS}
    attributes.update({key: False for key in AGE_RATING_FLAGS})
    attributes["advertising"] = args.advertising
    attributes["unrestrictedWebAccess"] = args.web_access
    attributes["userGeneratedContent"] = args.user_generated_content
    status, result = call("PATCH", f"/v1/ageRatingDeclarations/{declaration_id}",
                          {"data": {"type": "ageRatingDeclarations", "id": declaration_id, "attributes": attributes}})
    must(status, result, "연령 등급 입력")
    status, info = call("GET", f"/v1/appInfos/{info['id']}?fields[appInfos]=appStoreAgeRating")
    print("연령 등급:", info["data"]["attributes"].get("appStoreAgeRating"))


def cmd_content_rights(args):
    app = app_for(args.bundle_id)
    value = "USES_THIRD_PARTY_CONTENT" if args.uses_third_party else "DOES_NOT_USE_THIRD_PARTY_CONTENT"
    status, result = call("PATCH", f"/v1/apps/{app['id']}", {"data": {"type": "apps", "id": app["id"], "attributes": {"contentRightsDeclaration": value}}})
    must(status, result, "콘텐츠 권한")
    print("콘텐츠 권한:", value)


def cmd_pricing(args):
    app = app_for(args.bundle_id)
    app_id = app["id"]
    territories = [t["id"] for t in paginate("/v1/territories?limit=200")]
    if args.free:
        status, prices = call("GET", f"/v1/appPriceSchedules/{app_id}/manualPrices?limit=1")
        if status == 200 and prices.get("data"):
            print("가격: 이미 설정됨")
        else:
            point = next((p["id"] for p in paginate(query(f"/v1/apps/{app_id}/appPricePoints", **{"filter[territory]": "USA", "limit": 200}))
                          if float(p["attributes"]["customerPrice"]) == 0), None)
            status, result = call("POST", "/v1/appPriceSchedules", {
                "data": {"type": "appPriceSchedules", "relationships": {
                    "app": {"data": {"type": "apps", "id": app_id}},
                    "baseTerritory": {"data": {"type": "territories", "id": "USA"}},
                    "manualPrices": {"data": [{"type": "appPrices", "id": "${free}"}]}}},
                "included": [{"type": "appPrices", "id": "${free}", "attributes": {"startDate": None},
                              "relationships": {"appPricePoint": {"data": {"type": "appPricePoints", "id": point}}}}]})
            must(status, result, "무료 가격")
            print("가격: 무료")
    excluded = set(args.exclude or [])
    refs, included = [], []
    for territory in territories:
        local = "${t-%s}" % territory
        refs.append({"type": "territoryAvailabilities", "id": local})
        included.append({"type": "territoryAvailabilities", "id": local, "attributes": {"available": territory not in excluded},
                         "relationships": {"territory": {"data": {"type": "territories", "id": territory}}}})
    status, result = call("POST", "/v2/appAvailabilities", {
        "data": {"type": "appAvailabilities", "attributes": {"availableInNewTerritories": True},
                 "relationships": {"app": {"data": {"type": "apps", "id": app_id}}, "territoryAvailabilities": {"data": refs}}},
        "included": included})
    must(status, result, "판매 국가")
    print(f"판매 국가: {len(territories) - len(excluded & set(territories))}/{len(territories)} (제외 {sorted(excluded) or '없음'})")


def cmd_attach_build(args):
    app = app_for(args.bundle_id)
    version = editable_version(app["id"])
    builds = list(paginate(query("/v1/builds", **{"filter[app]": app["id"], "filter[version]": args.build, "limit": 1})))
    if not builds or builds[0]["attributes"]["processingState"] != "VALID":
        sys.exit(f"빌드 {args.build}가 아직 처리되지 않았다 (VALID가 되면 다시 실행한다)")
    status, result = call("PATCH", f"/v1/appStoreVersions/{version['id']}/relationships/build", {"data": {"type": "builds", "id": builds[0]["id"]}})
    must(status, result, "빌드 연결")
    print(f"버전 {version['attributes']['versionString']}에 빌드 {args.build} 연결")


def cmd_testflight(args):
    app = app_for(args.bundle_id)
    group = next((g for g in paginate(f"/v1/apps/{app['id']}/betaGroups") if g["attributes"]["isInternalGroup"]), None)
    if not group:
        status, result = call("POST", "/v1/betaGroups", {"data": {"type": "betaGroups",
            "attributes": {"name": args.group, "isInternalGroup": True, "hasAccessToAllBuilds": True},
            "relationships": {"app": {"data": {"type": "apps", "id": app["id"]}}}}})
        group = must(status, result, "내부 테스트 그룹")["data"]
    print("내부 테스트 그룹:", group["attributes"]["name"])
    existing = {t["attributes"].get("email") for t in paginate(f"/v1/betaGroups/{group['id']}/betaTesters")}
    # 내부 테스터는 App Store Connect 사용자여야 한다.
    for user in paginate("/v1/users?limit=50"):
        a = user["attributes"]
        if args.email and a["username"] not in args.email:
            continue
        if a["username"] in existing:
            continue
        status, result = call("POST", "/v1/betaTesters", {"data": {"type": "betaTesters",
            "attributes": {"email": a["username"], "firstName": a["firstName"], "lastName": a["lastName"]},
            "relationships": {"betaGroups": {"data": [{"type": "betaGroups", "id": group["id"]}]}}}})
        print(f"  테스터 추가 {a['firstName']} {a['lastName']}: {status} {error_detail(result)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "age-rating", "content-rights", "pricing", "attach-build", "testflight"):
        p = sub.add_parser(name)
        p.add_argument("--bundle-id", required=True)
        if name == "age-rating":
            p.add_argument("--advertising", action="store_true", help="앱에 광고가 있다")
            p.add_argument("--web-access", action="store_true", help="앱 안에서 임의 웹사이트를 열 수 있다")
            p.add_argument("--user-generated-content", action="store_true")
        if name == "content-rights":
            p.add_argument("--uses-third-party", action="store_true", help="타사 콘텐츠(외부 모델·음원·사진 등)를 포함·표시·사용하고 권리가 있다")
        if name == "pricing":
            p.add_argument("--free", action="store_true")
            p.add_argument("--exclude", nargs="*", help="판매하지 않을 국가 코드 (예: CHN)")
        if name == "attach-build":
            p.add_argument("--build", required=True)
        if name == "testflight":
            p.add_argument("--group", default="Internal")
            p.add_argument("--email", nargs="*", help="이 사용자만 추가 (기본: 모든 사용자)")
    args = parser.parse_args()
    {"check": cmd_check, "age-rating": cmd_age_rating, "content-rights": cmd_content_rights, "pricing": cmd_pricing,
     "attach-build": cmd_attach_build, "testflight": cmd_testflight}[args.command](args)


if __name__ == "__main__":
    main()
