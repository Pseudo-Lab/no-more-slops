#!/bin/bash
# Builds, installs and launches the app on a connected iPhone, and copies files back from its Documents.
#
# usage: device_run.sh (-p App.xcodeproj | -w App.xcworkspace) -s Scheme -b bundle.id -d DEVICE
#                      [-c Debug|Release] [-a "launch args"] [-f Documents/report.txt -o out-dir] [-n]
#   -d  device identifier from `xcrun devicectl list devices` (run without -d to list them)
#   -a  launch arguments (DEBUG-only ones need -c Debug)
#   -f  file or folder in the app container to copy back after launch (waits for it to appear)
#   -n  print the commands without running them
#
# Needs: the iPhone paired with this Mac (cable once, then Wi-Fi works), Developer Mode on, and an Apple
# account in Xcode > Settings > Accounts for signing. See references/device.md when the device is
# "unavailable".
set -euo pipefail

usage() { sed -n '2,14p' "$0"; exit 2; }
PROJECT=() SCHEME="" BUNDLE="" DEVICE="" CONFIG="Debug" ARGS="" FETCH="" OUT="." DRY=0
while getopts "p:w:s:b:d:c:a:f:o:n" opt; do
  case $opt in
    p) PROJECT=(-project "$OPTARG") ;;
    w) PROJECT=(-workspace "$OPTARG") ;;
    s) SCHEME=$OPTARG ;;
    b) BUNDLE=$OPTARG ;;
    d) DEVICE=$OPTARG ;;
    c) CONFIG=$OPTARG ;;
    a) ARGS=$OPTARG ;;
    f) FETCH=$OPTARG ;;
    o) OUT=$OPTARG ;;
    n) DRY=1 ;;
    *) usage ;;
  esac
done
if [ -z "$DEVICE" ] && [ $DRY -eq 0 ]; then xcrun devicectl list devices; echo; usage; fi
{ [ ${#PROJECT[@]} -gt 0 ] && [ -n "$SCHEME" ] && [ -n "$BUNDLE" ] && [ -n "$DEVICE" ]; } || usage

DD=${DERIVED_DATA:-${TMPDIR:-/tmp}/device-run-$SCHEME}
run() { if [ $DRY -eq 1 ]; then printf '$'; printf ' %q' "$@"; echo; else "$@"; fi; }
read -r -a LAUNCH <<< "$ARGS"

run xcodebuild "${PROJECT[@]}" -scheme "$SCHEME" -configuration "$CONFIG" -destination "platform=iOS,id=$DEVICE" \
  -derivedDataPath "$DD" -allowProvisioningUpdates build -quiet
APP="$DD/Build/Products/$CONFIG-iphoneos/<App>.app"
if [ $DRY -eq 0 ]; then
  APP=$(find "$DD/Build/Products/$CONFIG-iphoneos" -maxdepth 1 -name "*.app" | head -1)
  [ -n "$APP" ] || { echo "no .app in $DD/Build/Products/$CONFIG-iphoneos" >&2; exit 1; }
fi
run xcrun devicectl device install app --device "$DEVICE" "$APP"
# Arguments after "--" go to the app; without it devicectl reads "-flag" arguments as its own options.
if [ ${#LAUNCH[@]} -gt 0 ]; then
  run xcrun devicectl device process launch --device "$DEVICE" --terminate-existing "$BUNDLE" -- "${LAUNCH[@]}"
else
  run xcrun devicectl device process launch --device "$DEVICE" --terminate-existing "$BUNDLE"
fi

[ -n "$FETCH" ] || exit 0
COPY=(xcrun devicectl device copy from --device "$DEVICE" --domain-type appDataContainer
      --domain-identifier "$BUNDLE" --source "$FETCH" --destination "$OUT/$(basename "$FETCH")")
if [ $DRY -eq 1 ]; then run "${COPY[@]}"; exit 0; fi
mkdir -p "$OUT"
for _ in $(seq 1 60); do "${COPY[@]}" >/dev/null 2>&1 && break; sleep 2; done
[ -e "$OUT/$(basename "$FETCH")" ] || { echo "could not copy $FETCH from the device" >&2; exit 1; }
echo "copied $FETCH -> $OUT/$(basename "$FETCH")"
echo "note: a file left by an earlier run looks the same; check a timestamp inside it"
