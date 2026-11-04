#!/usr/bin/env bash
# Collects the evidence lines that micro-saas-audit scores. Prints facts only; the judgement is in SKILL.md.
# usage: audit.sh <repo dir> <prod url>
set -uo pipefail
repo=$1; url=${2%/}
cd "$repo"
say() { printf '%s: %s\n' "$1" "$2"; }
code() { curl -s -o /dev/null -w '%{http_code}' "$url$1"; }

echo "== 1 constitution-first"
c=.specify/memory/constitution.md
say C1.constitution "$([ -f $c ] && echo "exists, MUST NOT=$(grep -c 'MUST NOT' $c)" || echo missing)"
say C2.specs_without_constitution_check "$(grep -L 'Constitution Check' specs/*/spec.md 2>/dev/null | paste -sd' ' - || true)"
say C3.merged_prs_without_constitution_check "$(gh pr list --state merged --limit 100 --json number,body -q '[.[] | select(.body|test("Constitution")|not) | .number] | join(" ")')"

echo "== 2 skeleton-on-prod"
say S1.login_page "$(code /login)"
say S2.tables_vs_rls "$(cat supabase/migrations/*.sql | grep -ci 'create table') tables / $(cat supabase/migrations/*.sql | grep -ci 'enable row level security') rls"
say S3.service_role_in_src "$(grep -rli 'service_role' src | paste -sd' ' - || echo none)"
say S4.tsc "$(npx tsc --noEmit >/dev/null 2>&1 && echo pass || echo FAIL)"
say S4.lint "$(npm run -s lint >/dev/null 2>&1 && echo pass || echo FAIL)"

echo "== 3 launch-basics"
say L1.terms_privacy "$(code /terms) $(code /privacy), privacy says 저장하지 않: $(curl -s "$url/privacy" | grep -c '저장하지 않')"
say L2.delete_rpc "$(grep -li 'delete_account\|delete_my_account' supabase/migrations/*.sql | paste -sd' ' - || echo none)"
say L3.error_pages "$(ls src/app/error.tsx src/app/not-found.tsx 2>/dev/null | paste -sd' ' -)"
say L4.funnel_events_declared_not_tracked "$(for e in $(grep -o '"[a-z_]*"' src/lib/analytics.ts | tr -d '"'); do grep -rq "\"$e\"" src --exclude=analytics.ts || printf '%s ' "$e"; done)"
say L4.path_masking "$(grep -c 'replace(' src/lib/analytics.ts)"
say L5.https_og "hsts=$(curl -sI "$url/" | grep -ci strict-transport) og=$(code /opengraph-image.png)"

echo "== 4 core-feature-with-review"
say F1.schema_strict_store_false "$(grep -rhoE 'strict: *true|store: *false' src | sort -u | paste -sd' ' -)"
say F2.review_before_save "$(grep -rl 'ReviewForm' src | paste -sd' ' -)"
say F3.original_storage "storage calls: $(grep -rl 'storage.from' src | wc -l | tr -d ' '), pdf in git: $(git ls-files | grep -ci '\.pdf$')"
say F4.sample_mode_without_key "$(grep -c 'OPENAI_API_KEY) return' src/app/\(family\)/upload/extract.ts)"

echo "== 5 model-bakeoff"
say M1.bakeoff_table_rows_in_repo "$(grep -rhiE '^\| *(gpt|claude|gemini|o[0-9])' --include='*.md' . 2>/dev/null | grep -vc node_modules)"
say M3.abuse_caps "$(grep -lE 'take_extract_quota|spend_credit' supabase/migrations/*.sql | paste -sd' ' -)"

echo "== 6 glance-and-guardrails"
say G1.glance_fn "$(grep -n 'export function glance' src/lib/health.ts | cut -d: -f1)"
say G2.dialog_users "$(grep -rl 'ConfirmButton' src | grep -v confirm-button | wc -l | tr -d ' ') pages"
say G3.ledger "delta=$(grep -c 'sum(delta)' supabase/migrations/*credits*.sql | cut -d: -f2 | paste -sd+ - | bc) lock=$(grep -c advisory supabase/migrations/*credits*.sql | cut -d: -f2 | paste -sd+ - | bc)"

echo "== 7 env-split"
say E1.env_files "$(ls .env.example .env.development.local 2>/dev/null | paste -sd' ' -)"
say E2.local_supabase "$(grep -c 'kakao' supabase/config.toml 2>/dev/null)"
say E3.prod_key_in_local_env "$(grep -c '^OPENAI_API_KEY=.\+' .env.development.local 2>/dev/null)"

echo "== ship-loop"
prs=$(mktemp); gh pr list --state merged --limit 100 --json number,baseRefName,headRefName,body > "$prs"
say P1.prs_not_based_on_main "$(jq -r '[.[] | select(.baseRefName != "main") | "#\(.number)->\(.baseRefName)"] | join(" ")' "$prs")"
say P2.prs_without_closes "$(jq -r '[.[] | select(.body|test("Closes #")|not) | .number] | join(" ")' "$prs")"
say P3.branches_not_NNN "$(jq -r '[.[] | select(.headRefName|test("^[0-9]{3}-")|not) | .headRefName] | join(" ")' "$prs")"
say P4.specs "$(ls specs | wc -l | tr -d ' ') for $(jq length "$prs") merged PRs"; rm -f "$prs"
say P5.open_issues "$(gh issue list --state open --json number,title -q '.[] | "#\(.number) \(.title)"' | paste -sd'|' -)"

echo "== guardrails"
say X1.secrets_in_history "$(git log -p --all | grep -cE 'sk-[A-Za-z0-9]{20,}|sb_secret_[A-Za-z0-9]{10,}')"
say X2.why_comments "$(grep -rhoE '// (Business|History|Constraint|Future):' src supabase | wc -l | tr -d ' ')"
say X3.tests "$(ls -d test tests __tests__ e2e 2>/dev/null | paste -sd' ' - || echo none)"
