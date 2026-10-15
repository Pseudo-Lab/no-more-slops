#!/usr/bin/env python3
"""Captures App Store screenshots in every store locale on a booted iOS simulator.

usage: python3 capture_screenshots.py path/to/kit.json --device <simulator UDID> [--locales en-US ko ...] [--dry-run]

Before running: boot the simulator whose screen matches the App Store Connect slot (for example
iPhone 17 Pro = 1206 x 2622) and install a Debug build. Each shot in kit.json `screenshots.shots`
relaunches the app with `-AppleLanguages (<appLanguage>) -AppleLocale <region>`, the shared
`screenshots.launchArgs` and the shot's own `args` (DEBUG-only launch arguments that open a screen,
see the ios-verify-harness skill), waits `wait` seconds, and saves <screenshots.dir>/<locale>/<name>.jpg
(JPEG quality 92, no alpha). The status bar is set to 9:41, full battery and full signal first.
"""
import argparse
import importlib.util
import pathlib
import shlex
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True  # keep the installed skill folder clean
spec = importlib.util.spec_from_file_location("kit", pathlib.Path(__file__).with_name("kit.py"))
kit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit_module)

STATUS_BAR = ["--time", "9:41", "--dataNetwork", "wifi", "--wifiMode", "active", "--wifiBars", "3",
              "--cellularMode", "active", "--cellularBars", "4", "--batteryState", "charged", "--batteryLevel", "100"]


def run(cmd, dry, check=True):
    if dry:
        print("$", shlex.join(cmd))
        return ""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"failed: {shlex.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout


def pixel_size(path):
    out = run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], False)
    values = [line.split(":")[1].strip() for line in out.splitlines() if "pixel" in line]
    return f"{values[0]}x{values[1]}" if len(values) == 2 else "?"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("kit", help="kit.json")
    parser.add_argument("--device", required=True, help="booted simulator UDID (xcrun simctl list devices booted)")
    parser.add_argument("--locales", nargs="*", help="store locale codes (default: every kit locale)")
    parser.add_argument("--dry-run", action="store_true", help="print the simctl commands without running them")
    args = parser.parse_args()

    kit = kit_module.Kit(args.kit)
    bundle = kit.app.get("bundleId") or sys.exit("kit.json: app.bundleId is required")
    shots = kit.screenshots.get("shots") or sys.exit("kit.json: screenshots.shots is empty")
    common = kit.screenshots.get("launchArgs", [])
    expected = kit.screenshots.get("size", "").replace(" ", "").replace("×", "x")
    out_root = kit.file(kit.screenshots.get("dir", "screenshots"))
    chosen = args.locales or [loc["code"] for loc in kit.locales]
    unknown = [c for c in chosen if c not in {loc["code"] for loc in kit.locales}]
    if unknown:
        sys.exit(f"not in kit.json: {', '.join(unknown)}")

    dev, dry = args.device, args.dry_run
    run(["xcrun", "simctl", "status_bar", dev, "override", *STATUS_BAR], dry, check=False)
    wrong = []
    with tempfile.TemporaryDirectory(prefix="store-shots-") as tmp:
        for code in chosen:
            loc = kit.locale(code)
            language = loc.get("appLanguage") or loc["lang"]
            region = loc.get("region") or language.replace("-", "_")
            folder = out_root / code
            if not dry:
                folder.mkdir(parents=True, exist_ok=True)
            for shot in shots:
                run(["xcrun", "simctl", "terminate", dev, bundle], dry, check=False)
                run(["xcrun", "simctl", "launch", dev, bundle, *common, *shot.get("args", []),
                     "-AppleLanguages", f"({language})", "-AppleLocale", region], dry)
                if dry:
                    print(f"# wait {shot.get('wait', 6)}s")
                else:
                    time.sleep(shot.get("wait", 6))
                png = pathlib.Path(tmp) / f"{code}-{shot['name']}.png"
                jpg = folder / f"{shot['name']}.jpg"
                run(["xcrun", "simctl", "io", dev, "screenshot", "--type=png", str(png)], dry)
                run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", str(png), "--out", str(jpg)], dry)
                if not dry:
                    size = pixel_size(jpg)
                    if expected and size != expected:
                        wrong.append(f"{code}/{jpg.name} {size}")
                    print(f"{code}/{jpg.name} {size}")
    run(["xcrun", "simctl", "status_bar", dev, "clear"], dry, check=False)
    if wrong:
        sys.exit(f"{len(wrong)} screenshots are not {expected} (wrong simulator for this slot?): {', '.join(wrong)}")


if __name__ == "__main__":
    main()
