"""Checks the release-kit scripts on the bundled example kit.

usage: python3 tests/test_release_kit.py   (macOS or Linux, Python 3.9+, no extra packages)
"""
import functools
import http.server
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
EXAMPLE = SKILL / "references" / "example"


def run(*args, ok=True):
    result = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    if ok and result.returncode != 0:
        raise AssertionError(f"{args} exited {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class ReleaseKitTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="release-kit-test-")
        self.addCleanup(temp.cleanup)
        self.kit_dir = pathlib.Path(temp.name) / "kit"
        shutil.copytree(EXAMPLE, self.kit_dir)
        self.kit = self.kit_dir / "kit.json"

    def edit_metadata(self, code, field, value):
        path = self.kit_dir / "metadata" / f"{code}.md"
        text = path.read_text(encoding="utf-8")
        text = re.sub(rf"(## {field}\n).*?(?=\n## |\Z)", lambda m: m.group(1) + value + "\n", text, flags=re.S)
        path.write_text(text, encoding="utf-8")

    def edit_kit(self, change):
        data = json.loads(self.kit.read_text(encoding="utf-8"))
        change(data)
        self.kit.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    # check_store_metadata.py

    def test_example_metadata_passes(self):
        out = run(SCRIPTS / "check_store_metadata.py", self.kit).stdout
        self.assertIn("PASS en-US", out)
        self.assertIn("PASS ko", out)

    def test_limits_and_keyword_format_fail(self):
        self.edit_metadata("en-US", "Name", "Tonlit: " + "x" * 40)
        self.edit_metadata("ko", "Keywords", "셀카, 톤업,셀카")
        result = run(SCRIPTS / "check_store_metadata.py", self.kit, ok=False)
        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stdout, r"FAIL en-US: .*name 48/30")
        self.assertIn("space after a comma", result.stdout)
        self.assertIn("keywords repeat 셀카", result.stdout)

    def test_wasted_keyword_warns_and_strict_fails(self):
        self.edit_metadata("en-US", "Keywords", "editor,selfie")
        self.assertIn("WARN en-US", run(SCRIPTS / "check_store_metadata.py", self.kit).stdout)
        self.assertEqual(run(SCRIPTS / "check_store_metadata.py", self.kit, "--strict", ok=False).returncode, 1)

    def test_missing_locale_file_fails(self):
        (self.kit_dir / "metadata" / "ko.md").unlink()
        result = run(SCRIPTS / "check_store_metadata.py", self.kit, ok=False)
        self.assertIn("FAIL ko: no metadata/ko.md", result.stdout)

    # build_support_site.py

    def test_site_pages_per_locale(self):
        run(SCRIPTS / "build_support_site.py", "build", self.kit)
        site = self.kit_dir / "site"
        pages = sorted(p.relative_to(site).as_posix() for p in site.rglob("*.html"))
        self.assertEqual(pages, ["index.html", "ko/index.html", "ko/privacy.html", "ko/support.html", "privacy.html", "support.html"])
        ko = (site / "ko" / "support.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="ko">', ko)
        self.assertIn('href="mailto:support@example.com"', ko)
        self.assertIn('href="../support.html" lang="en"', ko)
        self.assertIn('hreflang="x-default" href="https://example.github.io/tonlit/support.html"', ko)
        self.assertIn("reportaproblem.apple.com", ko)
        self.assertIn("<title>Tonlit: Skin Tone Editor</title>", (site / "index.html").read_text(encoding="utf-8"))

    def test_site_verify_against_local_server(self):
        run(SCRIPTS / "build_support_site.py", "build", self.kit)
        handler = functools.partial(QuietHandler, directory=str(self.kit_dir / "site"))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.edit_kit(lambda d: d["site"].update(baseUrl=f"http://127.0.0.1:{server.server_port}/"))
        self.assertIn("6/6 pages live", run(SCRIPTS / "build_support_site.py", "verify", self.kit).stdout)
        (self.kit_dir / "site" / "ko" / "privacy.html").unlink()
        result = run(SCRIPTS / "build_support_site.py", "verify", self.kit, ok=False)
        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stdout, r"FAIL http://127\.0\.0\.1:\d+/ko/privacy\.html -- HTTP 404")

    def test_site_requires_email_placeholder(self):
        strings = self.kit_dir / "site-strings.json"
        data = json.loads(strings.read_text(encoding="utf-8"))
        data["ko"]["contact"] = "메일을 보내 주세요."
        strings.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        result = run(SCRIPTS / "build_support_site.py", "build", self.kit, ok=False)
        self.assertIn("contact must contain {email}", result.stderr)

    # paste_sheet.py

    def test_paste_sheet_embeds_every_locale(self):
        out = self.kit_dir / "sheet.html"
        run(SCRIPTS / "paste_sheet.py", self.kit, "-o", out)
        html = out.read_text(encoding="utf-8")
        payload = json.loads(re.search(r"const DATA = (\{.*?\});\n", html, re.S).group(1).replace("<\\/", "</"))
        self.assertEqual([d["code"] for d in payload["locales"]], ["en-US", "ko"])
        self.assertEqual(payload["locales"][1]["urls"]["privacy"], "https://example.github.io/tonlit/ko/privacy.html")
        self.assertEqual(payload["locales"][1]["fields"]["name"], "톤릿: 피부톤 보정")
        self.assertEqual(payload["screenshots"]["files"][0], "1-home.jpg")
        self.assertTrue(payload["notes"].startswith("Tonlit is a paid photo editor"))
        self.assertNotIn("/*DATA*/", html)
        self.assertIn("<title>Tonlit 제출 시트</title>", html)

    # capture_screenshots.py and upload_build.sh (dry runs; no simulator or Xcode needed)

    def test_capture_dry_run_launch_arguments(self):
        out = run(SCRIPTS / "capture_screenshots.py", self.kit, "--device", "SIM", "--locales", "ko", "--dry-run").stdout
        self.assertIn("xcrun simctl launch SIM com.example.tonlit -acceptTerms -screen draping -AppleLanguages '(ko)' -AppleLocale ko_KR", out)
        self.assertIn("screenshots/6.3-inch/ko/6-save.jpg", out)
        self.assertEqual(out.count("simctl io SIM screenshot"), 6)

    def test_capture_rejects_unknown_locale(self):
        result = run(SCRIPTS / "capture_screenshots.py", self.kit, "--device", "SIM", "--locales", "fr-FR", "--dry-run", ok=False)
        self.assertIn("not in kit.json: fr-FR", result.stderr)

    def test_upload_dry_run(self):
        script = SCRIPTS / "upload_build.sh"
        out = subprocess.run(["bash", str(script), "-p", "App.xcodeproj", "-s", "App", "-t", "TEAM", "-n"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("-configuration Release -destination generic/platform=iOS", out)
        self.assertIn("destination upload", out)
        self.assertIn("-exportArchive", out)
        missing = subprocess.run(["bash", str(script), "-s", "App"], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
