#!/usr/bin/env python3
"""구독·앱 내 구입 상품을 명세(JSON) 하나로 App Store Connect에 만든다. 다시 실행해도 있는 것은 건너뛴다.

  python3 -I iap_setup.py spec.json --validate          # 네트워크 없이 명세만 검사
  python3 -I iap_setup.py spec.json                     # 만들기·갱신
  python3 -I iap_setup.py spec.json --replace-screenshots

명세 형식은 references/example/iap-spec.json. 순서가 중요한 단계가 있다.
- 구독은 판매 국가(subscriptionAvailabilities)를 먼저 정해야 가격이 들어간다.
  (먼저 넣으면 409 "territory is not supported for your subscription and planType")
- 구독 가격은 국가마다 따로 넣어야 한다. 기준 국가 가격의 equalizations로 나머지를 채운다.
- 무료 체험 같은 첫 구매 혜택도 국가마다 만든다.
- 심사 스크린샷에 투명도(알파)가 있으면 IMAGE_INCORRECT_DIMENSIONS로 거절되므로 RGB로 바꿔 올린다.
"""
import argparse
import hashlib
import io
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# python3 -I는 스크립트 폴더를 import 경로에 넣지 않는다.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NAME_LIMIT = 30
DESCRIPTION_LIMIT = 45
PERIODS = {"ONE_WEEK", "ONE_MONTH", "TWO_MONTHS", "THREE_MONTHS", "SIX_MONTHS", "ONE_YEAR"}


def validate_spec(spec):
    """명세의 형식과 글자 수 한도를 검사해 문제 목록을 돌려준다."""
    problems = []
    keys = [s["key"] for s in spec.get("subscriptions", [])] + [n["key"] for n in spec.get("non_consumables", [])]
    if len(keys) != len(set(keys)):
        problems.append("상품 key가 중복된다")
    for sub in spec.get("subscriptions", []):
        if sub.get("period") not in PERIODS:
            problems.append(f"{sub['key']}: period는 {sorted(PERIODS)} 중 하나")
    for item in spec.get("subscriptions", []) + spec.get("non_consumables", []):
        for field in ("key", "product_id", "reference_name", "price"):
            if field not in item:
                problems.append(f"{item.get('key', '?')}: {field} 없음")
    for locale, values in spec.get("localizations", {}).items():
        group = values.get("group")
        if group is not None and not (0 < len(group) <= NAME_LIMIT):
            problems.append(f"{locale} group: 1~{NAME_LIMIT}자")
        for key in keys:
            entry = values.get(key)
            if not entry:
                problems.append(f"{locale}: {key} 없음")
                continue
            if not (0 < len(entry.get("name", "")) <= NAME_LIMIT):
                problems.append(f"{locale} {key} name: 1~{NAME_LIMIT}자 ({len(entry.get('name', ''))})")
            if not (0 < len(entry.get("description", "")) <= DESCRIPTION_LIMIT):
                problems.append(f"{locale} {key} description: 1~{DESCRIPTION_LIMIT}자 ({len(entry.get('description', ''))})")
    return problems


def rgb_png(path):
    """투명도 채널을 없앤 PNG 바이트. Pillow가 없으면 원본을 그대로 쓴다."""
    try:
        from PIL import Image
    except ImportError:
        return open(path, "rb").read()
    image = Image.open(path)
    if image.mode == "RGB":
        return open(path, "rb").read()
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    return buffer.getvalue()


class Setup:
    def __init__(self, spec, base_dir, replace_screenshots):
        from asc import call, error_detail, paginate, query
        self.call, self.error_detail, self.paginate, self.query = call, error_detail, paginate, query
        self.spec, self.base_dir, self.replace_screenshots = spec, base_dir, replace_screenshots
        self.app_id = spec["app_id"]
        self.base = spec.get("base_territory", "USA")
        excluded = set(spec.get("exclude_territories", []))
        self.territories = [t["id"] for t in paginate("/v1/territories?limit=200") if t["id"] not in excluded]

    def ok(self, status, result, what):
        if status >= 300:
            raise SystemExit(f"{what}: {status} {self.error_detail(result)}")
        return result

    # MARK: 구독 그룹

    def group(self):
        name = self.spec["group"]["reference_name"]
        group = next((g for g in self.paginate(f"/v1/apps/{self.app_id}/subscriptionGroups") if g["attributes"]["referenceName"] == name), None)
        if not group:
            status, result = self.call("POST", "/v1/subscriptionGroups", {"data": {"type": "subscriptionGroups",
                "attributes": {"referenceName": name}, "relationships": {"app": {"data": {"type": "apps", "id": self.app_id}}}}})
            group = self.ok(status, result, "구독 그룹")["data"]
        have = {x["attributes"]["locale"] for x in self.paginate(f"/v1/subscriptionGroups/{group['id']}/subscriptionGroupLocalizations")}
        added = 0
        for locale, values in self.spec.get("localizations", {}).items():
            if locale in have or not values.get("group"):
                continue
            status, result = self.call("POST", "/v1/subscriptionGroupLocalizations", {"data": {"type": "subscriptionGroupLocalizations",
                "attributes": {"name": values["group"], "locale": locale},
                "relationships": {"subscriptionGroup": {"data": {"type": "subscriptionGroups", "id": group["id"]}}}}})
            self.ok(status, result, f"그룹 현지화 {locale}")
            added += 1
        print(f"구독 그룹 {name}: 현지화 {len(have) + added}개")
        return group["id"]

    # MARK: 구독

    def subscription(self, group_id, sub):
        existing = {s["attributes"]["productId"]: s for s in self.paginate(f"/v1/subscriptionGroups/{group_id}/subscriptions")}
        item = existing.get(sub["product_id"])
        if not item:
            status, result = self.call("POST", "/v1/subscriptions", {"data": {"type": "subscriptions",
                "attributes": {"name": sub["reference_name"], "productId": sub["product_id"], "subscriptionPeriod": sub["period"],
                               "groupLevel": sub.get("level", 1), "familySharable": sub.get("family_sharable", False),
                               "reviewNote": sub.get("review_note", "")},
                "relationships": {"group": {"data": {"type": "subscriptionGroups", "id": group_id}}}}})
            item = self.ok(status, result, f"구독 {sub['product_id']}")["data"]
        sid = item["id"]
        self.localize("subscriptionLocalizations", f"/v1/subscriptions/{sid}/subscriptionLocalizations",
                      {"subscription": {"data": {"type": "subscriptions", "id": sid}}}, sub["key"])
        # 판매 국가가 먼저다.
        status, availability = self.call("GET", f"/v1/subscriptions/{sid}/subscriptionAvailability")
        if status != 200 or not availability.get("data"):
            status, result = self.call("POST", "/v1/subscriptionAvailabilities", {"data": {"type": "subscriptionAvailabilities",
                "attributes": {"availableInNewTerritories": True},
                "relationships": {"subscription": {"data": {"type": "subscriptions", "id": sid}},
                                  "availableTerritories": {"data": [{"type": "territories", "id": t} for t in self.territories]}}}})
            self.ok(status, result, f"{sub['key']} 판매 국가")
        self.subscription_prices(sid, sub)
        if sub.get("intro_offer"):
            self.intro_offers(sid, sub)
        self.screenshot("subscriptionAppStoreReviewScreenshots", f"/v1/subscriptions/{sid}/appStoreReviewScreenshot",
                        "subscription", "subscriptions", sid, sub.get("screenshot"))
        status, now = self.call("GET", f"/v1/subscriptions/{sid}")
        print(f"구독 {sub['product_id']}: {now['data']['attributes']['state']}")

    def price_point(self, path, price):
        for point in self.paginate(self.query(path, **{"filter[territory]": self.base, "limit": 200})):
            if float(point["attributes"]["customerPrice"]) == float(price):
                return point["id"]
        raise SystemExit(f"{self.base}에 {price} 가격 포인트가 없다")

    def subscription_prices(self, sid, sub):
        status, prices = self.call("GET", f"/v1/subscriptions/{sid}/prices?limit=1")
        if (prices.get("meta") or {}).get("paging", {}).get("total", 0) > 0:
            return
        base_point = self.price_point(f"/v1/subscriptions/{sid}/pricePoints", sub["price"])
        allowed = set(self.territories)
        points = [(self.base, base_point)] + [
            (p["relationships"]["territory"]["data"]["id"], p["id"])
            for p in self.paginate(f"/v1/subscriptionPricePoints/{base_point}/equalizations?include=territory&limit=200")
            if p["relationships"]["territory"]["data"]["id"] in allowed]

        def post(entry):
            territory, point = entry
            status, result = self.call("POST", "/v1/subscriptionPrices", {"data": {"type": "subscriptionPrices",
                "attributes": {"startDate": None, "preserveCurrentPrice": False},
                "relationships": {"subscription": {"data": {"type": "subscriptions", "id": sid}},
                                  "subscriptionPricePoint": {"data": {"type": "subscriptionPricePoints", "id": point}},
                                  "territory": {"data": {"type": "territories", "id": territory}}}}})
            return territory, status, self.error_detail(result)
        # 동시에 많이 보내면 429가 나서 3개씩만 보낸다.
        with ThreadPoolExecutor(3) as pool:
            results = list(pool.map(post, points))
        failed = [r for r in results if r[1] >= 300]
        print(f"  {sub['key']} 가격: {len(results) - len(failed)}/{len(results)}개 국가" + (f", 실패 {failed[:3]}" if failed else ""))

    def intro_offers(self, sid, sub):
        status, offers = self.call("GET", f"/v1/subscriptions/{sid}/introductoryOffers?limit=1")
        if offers.get("data"):
            return
        offer = sub["intro_offer"]

        def post(territory):
            status, result = self.call("POST", "/v1/subscriptionIntroductoryOffers", {"data": {"type": "subscriptionIntroductoryOffers",
                "attributes": {"duration": offer["duration"], "offerMode": offer["mode"], "numberOfPeriods": offer.get("periods", 1),
                               "startDate": None, "endDate": None},
                "relationships": {"subscription": {"data": {"type": "subscriptions", "id": sid}},
                                  "territory": {"data": {"type": "territories", "id": territory}}}}})
            return status
        with ThreadPoolExecutor(3) as pool:
            statuses = list(pool.map(post, self.territories))
        print(f"  {sub['key']} 첫 구매 혜택: {sum(s < 300 for s in statuses)}/{len(statuses)}개 국가")

    # MARK: 앱 내 구입 (비소모품)

    def non_consumable(self, item):
        existing = {x["attributes"]["productId"]: x for x in self.paginate(f"/v1/apps/{self.app_id}/inAppPurchasesV2")}
        record = existing.get(item["product_id"])
        if not record:
            status, result = self.call("POST", "/v2/inAppPurchases", {"data": {"type": "inAppPurchases",
                "attributes": {"name": item["reference_name"], "productId": item["product_id"], "inAppPurchaseType": "NON_CONSUMABLE",
                               "familySharable": item.get("family_sharable", False), "reviewNote": item.get("review_note", "")},
                "relationships": {"app": {"data": {"type": "apps", "id": self.app_id}}}}})
            record = self.ok(status, result, f"앱 내 구입 {item['product_id']}")["data"]
        iid = record["id"]
        self.localize("inAppPurchaseLocalizations", f"/v2/inAppPurchases/{iid}/inAppPurchaseLocalizations",
                      {"inAppPurchaseV2": {"data": {"type": "inAppPurchases", "id": iid}}}, item["key"])
        status, schedule = self.call("GET", f"/v1/inAppPurchasePriceSchedules/{iid}/manualPrices?limit=1")
        if status != 200 or not schedule.get("data"):
            point = self.price_point(f"/v2/inAppPurchases/{iid}/pricePoints", item["price"])
            # 비소모품은 기준 국가 가격 하나만 넣으면 나머지 국가는 자동으로 환산된다.
            status, result = self.call("POST", "/v1/inAppPurchasePriceSchedules", {"data": {"type": "inAppPurchasePriceSchedules",
                "relationships": {"inAppPurchase": {"data": {"type": "inAppPurchases", "id": iid}},
                                  "baseTerritory": {"data": {"type": "territories", "id": self.base}},
                                  "manualPrices": {"data": [{"type": "inAppPurchasePrices", "id": "${p}"}]}}},
                "included": [{"type": "inAppPurchasePrices", "id": "${p}", "attributes": {"startDate": None},
                              "relationships": {"inAppPurchasePricePoint": {"data": {"type": "inAppPurchasePricePoints", "id": point}}}}]})
            self.ok(status, result, f"{item['key']} 가격")
            status, result = self.call("POST", "/v1/inAppPurchaseAvailabilities", {"data": {"type": "inAppPurchaseAvailabilities",
                "attributes": {"availableInNewTerritories": True},
                "relationships": {"inAppPurchase": {"data": {"type": "inAppPurchases", "id": iid}},
                                  "availableTerritories": {"data": [{"type": "territories", "id": t} for t in self.territories]}}}})
            self.ok(status, result, f"{item['key']} 판매 국가")
        self.screenshot("inAppPurchaseAppStoreReviewScreenshots", f"/v2/inAppPurchases/{iid}/appStoreReviewScreenshot",
                        "inAppPurchaseV2", "inAppPurchases", iid, item.get("screenshot"))
        status, now = self.call("GET", f"/v2/inAppPurchases/{iid}")
        print(f"앱 내 구입 {item['product_id']}: {now['data']['attributes']['state']}")

    # MARK: 공통

    def localize(self, kind, list_path, relationship, key):
        existing = {x["attributes"]["locale"]: x for x in self.paginate(list_path)}
        count = 0
        for locale, values in self.spec.get("localizations", {}).items():
            entry = values.get(key)
            if not entry:
                continue
            current = existing.get(locale)
            if current:
                if current["attributes"].get("name") == entry["name"] and current["attributes"].get("description") == entry["description"]:
                    count += 1
                    continue
                status, result = self.call("PATCH", f"/v1/{kind}/{current['id']}", {"data": {"type": kind, "id": current["id"],
                    "attributes": {"name": entry["name"], "description": entry["description"]}}})
            else:
                status, result = self.call("POST", f"/v1/{kind}", {"data": {"type": kind,
                    "attributes": {"name": entry["name"], "description": entry["description"], "locale": locale},
                    "relationships": relationship}})
            self.ok(status, result, f"{key} 현지화 {locale}")
            count += 1
        print(f"  {key} 현지화: {count}개 언어")

    def screenshot(self, kind, current_path, relationship, rel_type, rel_id, filename):
        if not filename:
            return
        status, current = self.call("GET", current_path)
        if current.get("data"):
            if not self.replace_screenshots:
                return
            self.call("DELETE", f"/v1/{kind}/{current['data']['id']}")
        data = rgb_png(os.path.join(self.base_dir, filename))
        status, result = self.call("POST", f"/v1/{kind}", {"data": {"type": kind,
            "attributes": {"fileName": os.path.basename(filename), "fileSize": len(data)},
            "relationships": {relationship: {"data": {"type": rel_type, "id": rel_id}}}}})
        reservation = self.ok(status, result, f"심사 스크린샷 {filename}")["data"]
        for op in reservation["attributes"]["uploadOperations"]:
            chunk = data[op["offset"]:op["offset"] + op["length"]]
            request = urllib.request.Request(op["url"], data=chunk, method=op["method"],
                                             headers={h["name"]: h["value"] for h in op["requestHeaders"]})
            urllib.request.urlopen(request, timeout=120).read()
        status, result = self.call("PATCH", f"/v1/{kind}/{reservation['id']}", {"data": {"type": kind, "id": reservation["id"],
            "attributes": {"uploaded": True, "sourceFileChecksum": hashlib.md5(data).hexdigest()}}})
        self.ok(status, result, f"심사 스크린샷 확정 {filename}")
        print(f"  심사 스크린샷 {filename} 올림")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec")
    parser.add_argument("--validate", action="store_true", help="명세만 검사하고 끝낸다")
    parser.add_argument("--replace-screenshots", action="store_true", help="이미 있는 심사 스크린샷도 바꾼다")
    args = parser.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    problems = validate_spec(spec)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"명세 OK: 구독 {len(spec.get('subscriptions', []))}개, 앱 내 구입 {len(spec.get('non_consumables', []))}개, "
          f"언어 {len(spec.get('localizations', {}))}개")
    if args.validate:
        return
    setup = Setup(spec, os.path.dirname(os.path.abspath(args.spec)), args.replace_screenshots)
    if spec.get("subscriptions"):
        group_id = setup.group()
        for sub in spec["subscriptions"]:
            setup.subscription(group_id, sub)
    for item in spec.get("non_consumables", []):
        setup.non_consumable(item)


if __name__ == "__main__":
    main()
