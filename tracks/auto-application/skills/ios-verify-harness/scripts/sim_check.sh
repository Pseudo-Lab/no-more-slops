#!/bin/bash
# Builds the app for a simulator, runs its in-app self-check in each language and reports PASS/FAIL.
#
# usage: sim_check.sh (-p App.xcodeproj | -w App.xcworkspace) -s Scheme -b bundle.id
#                     [-d "iPhone 17 Pro"] [-l "en ko"] [-a "-selfCheck"] [-r self-check.txt] [-t 120] [-n]
#   -d  simulator name (default iPhone 17 Pro)        -l  languages (default "en")
#   -a  launch arguments that start the check          -r  report file in the app's Documents
#   -t  seconds to wait for the report's DONE line     -n  print the commands without running them
#
# The app writes one "PASS <check>" or "FAIL <check> (<detail>)" line per check to Documents/<report>
# and a final "DONE" line (see references/launch-arguments.md). Exit status 1 if any check failed or
# the report never finished.
set -euo pipefail

usage() { sed -n '2,13p' "$0"; exit 2; }
PROJECT=() SCHEME="" BUNDLE="" DEVICE="iPhone 17 Pro" LANGS="en" ARGS="-selfCheck" REPORT="self-check.txt" TIMEOUT=120 DRY=0
while getopts "p:w:s:b:d:l:a:r:t:n" opt; do
  case $opt in
    p) PROJECT=(-project "$OPTARG") ;;
    w) PROJECT=(-workspace "$OPTARG") ;;
    s) SCHEME=$OPTARG ;;
    b) BUNDLE=$OPTARG ;;
    d) DEVICE=$OPTARG ;;
    l) LANGS=$OPTARG ;;
    a) ARGS=$OPTARG ;;
    r) REPORT=$OPTARG ;;
    t) TIMEOUT=$OPTARG ;;
    n) DRY=1 ;;
    *) usage ;;
  esac
done
{ [ ${#PROJECT[@]} -gt 0 ] && [ -n "$SCHEME" ] && [ -n "$BUNDLE" ]; } || usage

DD=${DERIVED_DATA:-${TMPDIR:-/tmp}/sim-check-$SCHEME}
run() { if [ $DRY -eq 1 ]; then printf '$'; printf ' %q' "$@"; echo; else "$@"; fi; }
read -r -a LAUNCH <<< "$ARGS"

run xcodebuild "${PROJECT[@]}" -scheme "$SCHEME" -configuration Debug -destination "platform=iOS Simulator,name=$DEVICE" \
  -derivedDataPath "$DD" build -quiet
if [ $DRY -eq 0 ]; then
  xcrun simctl boot "$DEVICE" 2>/dev/null || true
  APP=$(find "$DD/Build/Products/Debug-iphonesimulator" -maxdepth 1 -name "*.app" | head -1)
  [ -n "$APP" ] || { echo "no .app in $DD/Build/Products/Debug-iphonesimulator" >&2; exit 1; }
  xcrun simctl install booted "$APP"
else
  run xcrun simctl install booted "$DD/Build/Products/Debug-iphonesimulator/<App>.app"
fi

status=0
for lang in $LANGS; do
  run xcrun simctl terminate booted "$BUNDLE" || true
  if [ $DRY -eq 0 ]; then
    C=$(xcrun simctl get_app_container booted "$BUNDLE" data)
    rm -f "$C/Documents/$REPORT"
  fi
  run xcrun simctl launch booted "$BUNDLE" ${LAUNCH[@]+"${LAUNCH[@]}"} -AppleLanguages "($lang)"
  [ $DRY -eq 1 ] && { echo "# wait for DONE in Documents/$REPORT"; continue; }
  for _ in $(seq 1 "$TIMEOUT"); do grep -q "^DONE" "$C/Documents/$REPORT" 2>/dev/null && break; sleep 1; done
  if ! grep -q "^DONE" "$C/Documents/$REPORT" 2>/dev/null; then
    echo "self-check ($lang): no DONE line after ${TIMEOUT}s in $C/Documents/$REPORT"
    status=1; continue
  fi
  pass=$(grep -c "^PASS" "$C/Documents/$REPORT" || true); fail=$(grep -c "^FAIL" "$C/Documents/$REPORT" || true)
  echo "self-check ($lang): $pass passed, $fail failed"
  grep "^FAIL" "$C/Documents/$REPORT" || true
  [ "$fail" = "0" ] || status=1
done
exit $status
