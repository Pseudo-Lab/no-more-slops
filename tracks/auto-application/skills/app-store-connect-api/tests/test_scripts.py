"""네트워크 없이 도는 단위 검사: python3 -I -m unittest discover -s tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import asc  # noqa: E402
import app_name_check  # noqa: E402
import iap_setup  # noqa: E402


class AscTests(unittest.TestCase):
    def test_der_to_raw_pads_and_strips(self):
        r = b"\x00" + b"\x81" * 32          # 부호 비트 때문에 앞에 0이 붙은 33바이트
        s = b"\x01" * 31                    # 31바이트 → 32바이트로 채운다
        der = b"\x30" + bytes([4 + len(r) + len(s)]) + b"\x02" + bytes([len(r)]) + r + b"\x02" + bytes([len(s)]) + s
        raw = asc.der_to_raw(der)
        self.assertEqual(len(raw), 64)
        self.assertEqual(raw[:32], b"\x81" * 32)
        self.assertEqual(raw[32:], b"\x00" + b"\x01" * 31)

    def test_token_signs_with_p256_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = os.path.join(tmp, "key.p8")
            subprocess.run(["openssl", "ecparam", "-name", "prime256v1", "-genkey", "-noout", "-out", key], check=True, capture_output=True)
            jwt = asc.token("KEYID", "issuer-uuid", key)
        header, payload, signature = jwt.split(".")
        pad = lambda s: s + "=" * (-len(s) % 4)  # noqa: E731
        import base64
        self.assertEqual(json.loads(base64.urlsafe_b64decode(pad(header)))["kid"], "KEYID")
        self.assertEqual(json.loads(base64.urlsafe_b64decode(pad(payload)))["aud"], "appstoreconnect-v1")
        self.assertEqual(len(base64.urlsafe_b64decode(pad(signature))), 64)

    def test_query_encodes_brackets(self):
        self.assertEqual(asc.query("/v1/apps", **{"filter[bundleId]": "a.b"}), "/v1/apps?filter%5BbundleId%5D=a.b")


class NameCheckTests(unittest.TestCase):
    def test_brand_after_prefix_is_taken(self):
        taken, similar = app_name_check.classify("Albumate", ["Swipe Photo Sorting - Albumate", "Albumates Club"])
        self.assertEqual(taken, ["Swipe Photo Sorting - Albumate"])
        self.assertEqual(similar, ["Albumates Club"])

    def test_spaced_candidate(self):
        taken, _ = app_name_check.classify("Photo Shelf", ["My Photo Shelf: Albums"])
        self.assertEqual(taken, ["My Photo Shelf: Albums"])


class SpecTests(unittest.TestCase):
    def test_example_spec_is_valid(self):
        spec = json.load(open(os.path.join(HERE, "..", "references", "example", "iap-spec.json"), encoding="utf-8"))
        self.assertEqual(iap_setup.validate_spec(spec), [])
        self.assertEqual(len(spec["localizations"]), 35)

    def test_limits_are_enforced(self):
        spec = {"subscriptions": [{"key": "m", "product_id": "p", "reference_name": "r", "price": 1, "period": "ONE_MONTH"}],
                "localizations": {"en-US": {"group": "G", "m": {"name": "x" * 31, "description": "y" * 46}}}}
        problems = iap_setup.validate_spec(spec)
        self.assertTrue(any("name" in p for p in problems))
        self.assertTrue(any("description" in p for p in problems))

    def test_unknown_period(self):
        spec = {"subscriptions": [{"key": "m", "product_id": "p", "reference_name": "r", "price": 1, "period": "MONTHLY"}], "localizations": {}}
        self.assertTrue(any("period" in p for p in iap_setup.validate_spec(spec)))


if __name__ == "__main__":
    unittest.main()
