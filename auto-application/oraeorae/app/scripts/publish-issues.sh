#!/usr/bin/env bash
# Publishes issues/*.md drafts to the origin repo as GitHub issues, once each.
set -euo pipefail

cd "$(dirname "$0")/.."

for file in issues/[0-9]*.md; do
  # Business: a published draft carries its issue URL, so reruns never create duplicates.
  if grep -q '^issue:' "$file"; then
    echo "skip  $file (already published)"
    continue
  fi

  title=$(sed -n 's/^title: *"\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' "$file" | head -1)
  labels=$(sed -n 's/^labels: *//p' "$file" | head -1)
  body=$(awk 'f>=2 {print} /^---$/ {f++}' "$file")

  label_args=()
  IFS=',' read -ra names <<< "$labels"
  for name in "${names[@]}"; do
    name=$(echo "$name" | xargs)
    [ -z "$name" ] && continue
    gh label create "$name" --force >/dev/null
    label_args+=(--label "$name")
  done

  url=$(gh issue create --title "$title" --body "$body" "${label_args[@]}")
  # Drafts written after the work shipped are recorded as closed so the history stays complete.
  if grep -q '^status: done' "$file"; then
    gh issue close "$url" --reason completed >/dev/null
  fi
  # Record the URL right after the opening '---' so the draft is marked as published.
  sed -i '' "1a\\
issue: $url
" "$file"
  echo "done  $file -> $url"
done
