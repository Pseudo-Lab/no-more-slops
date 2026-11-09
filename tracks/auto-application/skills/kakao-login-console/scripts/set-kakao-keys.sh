#!/usr/bin/env bash
# 카카오 REST API 키와 Client Secret을 화면에 보이지 않게 입력받아 supabase/.env(커밋 안 함)에 넣는다.
# 채팅이나 셸 기록에 키가 남지 않게 하려고 read -s를 쓴다.
set -euo pipefail

# 사용: 프로젝트 루트에서 bash set-kakao-keys.sh [env 파일, 기본 supabase/.env]
env_file="${1:-supabase/.env}"
mkdir -p "$(dirname "$env_file")"
touch "$env_file"
chmod 600 "$env_file"

read -r -s -p "카카오 REST API 키: " client_id; echo
read -r -s -p "카카오 Client Secret: " secret; echo
[[ -n "$client_id" && -n "$secret" ]] || { echo "빈 값이 있어요. 다시 실행해 주세요."; exit 1; }

# 기존 줄은 지우고 새 값을 붙인다. 값은 환경변수로 넘겨 명령줄에 드러나지 않게 한다.
KAKAO_ID="$client_id" KAKAO_SECRET="$secret" python3 - "$env_file" <<'EOF'
import os, sys
path = sys.argv[1]
keep = [l for l in open(path).read().splitlines()
        if not l.startswith(("SUPABASE_AUTH_EXTERNAL_KAKAO_CLIENT_ID=", "SUPABASE_AUTH_EXTERNAL_KAKAO_SECRET="))]
keep += [f"SUPABASE_AUTH_EXTERNAL_KAKAO_CLIENT_ID={os.environ['KAKAO_ID']}",
         f"SUPABASE_AUTH_EXTERNAL_KAKAO_SECRET={os.environ['KAKAO_SECRET']}"]
open(path, "w").write("\n".join(keep) + "\n")
EOF

echo "저장했어요: REST API 키 ${#client_id}자, Client Secret ${#secret}자 → supabase/.env"
