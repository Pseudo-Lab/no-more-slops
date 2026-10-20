#!/bin/bash
# Archives an iOS app in Release and uploads it to App Store Connect with xcodebuild.
#
# usage: upload_build.sh (-p App.xcodeproj | -w App.xcworkspace) -s Scheme -t TEAM_ID
#                        [-o out-dir] [-k AuthKey_XXXX.p8 -i KEY_ID -u ISSUER_ID] [-e] [-n]
#   -o  where the archive, ExportOptions.plist and logs go (default: ./build/app-store)
#   -k/-i/-u  App Store Connect API key instead of the Apple account signed in to Xcode
#   -e  export a signed .ipa only, don't upload
#   -n  print the commands without running them
#
# App Store signing needs an Apple account in Xcode > Settings > Accounts (or an API key); without
# one the export stops with "No Accounts" / "No profiles for '<bundle id>' were found".
# Each upload needs a higher build number (CURRENT_PROJECT_VERSION) than the last one.
set -euo pipefail

usage() { sed -n '2,13p' "$0"; exit 2; }
PROJECT=() SCHEME="" TEAM="" OUT="build/app-store" KEY="" KEY_ID="" ISSUER="" DEST="upload" DRY=0
while getopts "p:w:s:t:o:k:i:u:en" opt; do
  case $opt in
    p) PROJECT=(-project "$OPTARG") ;;
    w) PROJECT=(-workspace "$OPTARG") ;;
    s) SCHEME=$OPTARG ;;
    t) TEAM=$OPTARG ;;
    o) OUT=$OPTARG ;;
    k) KEY=$OPTARG ;;
    i) KEY_ID=$OPTARG ;;
    u) ISSUER=$OPTARG ;;
    e) DEST="export" ;;
    n) DRY=1 ;;
    *) usage ;;
  esac
done
{ [ ${#PROJECT[@]} -gt 0 ] && [ -n "$SCHEME" ] && [ -n "$TEAM" ]; } || usage

AUTH=(-allowProvisioningUpdates)
if [ -n "$KEY" ]; then
  { [ -n "$KEY_ID" ] && [ -n "$ISSUER" ]; } || { echo "-k needs -i KEY_ID and -u ISSUER_ID" >&2; exit 2; }
  AUTH+=(-authenticationKeyPath "$KEY" -authenticationKeyID "$KEY_ID" -authenticationKeyIssuerID "$ISSUER")
elif [ $DRY -eq 0 ] && ! defaults read com.apple.dt.Xcode DVTDeveloperAccountManagerAppleIDLists 2>/dev/null | grep -q identifier; then
  echo "Xcode has no Apple account. Sign in at Xcode > Settings > Accounts (+ > Apple Account), or pass an API key with -k/-i/-u." >&2
  exit 3
fi

ARCHIVE="$OUT/App.xcarchive" PLIST="$OUT/ExportOptions.plist"
ARCHIVE_CMD=(xcodebuild "${PROJECT[@]}" -scheme "$SCHEME" -configuration Release -destination generic/platform=iOS
             -archivePath "$ARCHIVE" "${AUTH[@]}" archive)
EXPORT_CMD=(xcodebuild -exportArchive -archivePath "$ARCHIVE" -exportOptionsPlist "$PLIST" -exportPath "$OUT/export" "${AUTH[@]}")

if [ $DRY -eq 1 ]; then
  printf '$'; printf ' %q' "${ARCHIVE_CMD[@]}"; echo
  echo "# $PLIST: method app-store-connect, destination $DEST, signingStyle automatic, teamID $TEAM"
  printf '$'; printf ' %q' "${EXPORT_CMD[@]}"; echo
  exit 0
fi

mkdir -p "$OUT"
echo "== archive ($SCHEME, Release)"
"${ARCHIVE_CMD[@]}" > "$OUT/archive.log" 2>&1 \
  || { tail -30 "$OUT/archive.log"; echo "archive failed, full log: $OUT/archive.log" >&2; exit 1; }
INFO="$ARCHIVE/Info.plist"
VERSION=$(/usr/libexec/PlistBuddy -c "Print :ApplicationProperties:CFBundleShortVersionString" "$INFO")
BUILD=$(/usr/libexec/PlistBuddy -c "Print :ApplicationProperties:CFBundleVersion" "$INFO")
APP_PATH=$(/usr/libexec/PlistBuddy -c "Print :ApplicationProperties:ApplicationPath" "$INFO")
echo "archived version $VERSION ($BUILD)"
if ! /usr/libexec/PlistBuddy -c "Print :ITSAppUsesNonExemptEncryption" "$ARCHIVE/Products/$APP_PATH/Info.plist" >/dev/null 2>&1; then
  echo "note: Info.plist has no ITSAppUsesNonExemptEncryption, so App Store Connect asks the export-compliance question for this build"
fi

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>method</key><string>app-store-connect</string>
  <key>destination</key><string>$DEST</string>
  <key>signingStyle</key><string>automatic</string>
  <key>teamID</key><string>$TEAM</string>
  <key>uploadSymbols</key><true/>
  <key>manageAppVersionAndBuildNumber</key><false/>
</dict>
</plist>
EOF

echo "== export ($DEST)"
"${EXPORT_CMD[@]}" > "$OUT/export.log" 2>&1 \
  || { grep -iE "error" "$OUT/export.log" | tail -10 || true; echo "export failed, full log: $OUT/export.log" >&2; exit 1; }
if [ "$DEST" = "upload" ]; then
  grep -q "Upload succeeded" "$OUT/export.log" || { echo "no 'Upload succeeded' in $OUT/export.log" >&2; exit 1; }
  echo "Uploaded $VERSION ($BUILD). App Store Connect processes it in about 10-30 minutes; then pick it in the version page's Build section."
else
  echo "Signed .ipa in $OUT/export"
fi
