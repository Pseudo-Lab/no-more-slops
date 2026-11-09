---
name: service-mcp
description: Next.js(App Router) + Supabase 서비스에 MCP 서버를 붙여 사용자가 Claude 같은 AI 비서로 자기 데이터를 읽고 넣게 한다. 사용자 개인 키(해시만 저장) + security definer RPC로 권한을 DB가 확인하고(서버에 service_role 없음), 라우트는 상태 없는 Streamable HTTP 하나, 큰 파일(영상 등)은 일회용 Storage 업로드 경로로 받는다. 앱에는 키를 한 번만 보여 주는 화면을 두고, 테스트와 의존성 없는 점검 스크립트로 확인한 뒤 마이그레이션 → 배포 순서로 올린다. "MCP 붙이자", "AI가 입력 도와주게", "Claude에서 우리 서비스 쓰게", "MCP 서버 만들어", "AI로 기록하기", "MCP로 파일/영상 올리기"처럼 서비스에 AI 비서 연결을 요청하면 이 스킬을 쓴다.
---

# service-mcp

AI 비서는 사람 대신 버튼을 누르는 손이다. 손에게는 그 사람의 열쇠 하나만 주고, 문은 DB가 지킨다. 서버는 말을 전달할 뿐 권한을 판단하지 않는다.

템플릿: `references/route.template.ts`(라우트), `references/ai.template.sql`(키·도구 함수·일회용 업로드, 예시 도메인 `entries`). 둘 다 실제로 돌려 본 코드에서 이름만 일반화했다(코치코치: 운동 기록·자세 영상). 새 서비스에서는 테이블·도구·규칙만 바꿔 쓴다.

## 입력
- 원칙 문서(있으면): AI가 해도 되는 일/안 되는 일, 공유 기본값(AI가 넣은 데이터도 기본 비공개인지).
- 도구 목록 3~5개. **읽기 1~2개 + 쓰기 1~2개**로 시작한다. 지우기·공유 바꾸기·남의 데이터 건드리기는 넣지 않는다(되돌릴 수 없는 일은 앱의 확인 창에서만).
- 쓸 사람의 역할: 보통 "자기 데이터의 주인"(예: 회원) 한 역할만.

## 설계 결정 (바꾸지 않는 기본값)
| 결정 | 이유 |
|---|---|
| 인증은 `Authorization: Bearer <개인 키>` | Claude Code·Cursor 등은 헤더를 넣을 수 있다. claude.ai 웹 커넥터는 OAuth가 필요하다 → 요청이 있을 때 따로 |
| 키는 `prefix_` + 24바이트 난수(hex), DB에는 sha256 해시만 | 유출돼도 DB에서 원문을 못 얻는다. 다시 만들면 이전 키는 즉시 끊긴다(사용자 1명 = 키 1개) |
| 서버는 publishable(anon) 키로 `rpc("ai_*", { k, ... })`만 부른다 | service_role을 서버에 두지 않는다. 키 확인·범위·검증은 security definer 함수 안에서 |
| 라우트는 상태 없는 Streamable HTTP: POST 하나 = JSON-RPC 하나 = JSON 응답 하나 | 세션·SSE 없음 → 서버리스에 그대로. GET은 405, 알림(id 없음)은 202 |
| 매 요청 처음에 `ai_whoami(k)`로 키 확인 → 틀리면 401 + `WWW-Authenticate` | AI 앱이 연결 실패를 바로 보여 준다 |
| 큰 파일은 MCP를 거치지 않는다 | Vercel 함수 본문 4.5MB 한도. 일회용 Storage 경로 + curl |
| SDK 없이 직접 구현(~150줄) | 필요한 메서드는 initialize·ping·tools/list·tools/call뿐. 검증은 공식 SDK 클라이언트로 |

## 절차

### 1. DB (마이그레이션 하나)
`references/ai.template.sql`을 복사해 `entries`를 자기 테이블로 바꾼다.
1. `ai_keys(owner_id pk, key_hash unique, created_at)` + RLS(본인 select/delete만). `issue_ai_key()`(역할 확인 → upsert → 원문 반환)는 `authenticated`에만.
2. `ai_member(k) returns uuid`: 해시로 찾고 없으면 `raise exception 'invalid_key'`. **anon·authenticated 모두 직접 못 부르게** revoke(다른 definer 함수 안에서만 쓴다).
3. 도구마다 `ai_<도구>(k text, ...)` security definer 함수. 첫 줄에서 `ai_member(k)`로 주인을 정하고 그 주인 것만 읽고 쓴다. 앱의 RLS와 **같은 규칙**을 함수 안에 다시 적는다(예: 공유 안 한 건 안 보임, 새 데이터는 기본 비공개).
4. 값 검증은 테이블 check 제약에 맡긴다(앱과 AI가 같은 제약을 쓴다).
5. 권한: `revoke execute on function … from public, anon, authenticated;` 후 필요한 것만 `grant`(`issue_ai_key`는 authenticated, `ai_whoami`·`ai_<도구>`는 anon·authenticated, `ai_member`는 아무에게도). **`from public`만으로는 안 막힌다**(아래 함정).
6. **큰 파일**: `ai_uploads(path pk, owner_id, expires_at)`(정책 없음) + `ai_start_upload(k, ext)`가 `ai/<owner>/<128비트 난수>.<ext>` 경로를 열고, Storage에 `for insert to anon with check (bucket_id = '…' and ai_upload_open(name))` 정책 하나. 파일을 쓰는 함수(예: `ai_add_card`)는 경로 주인 확인 → `storage.objects`에 실제로 올라왔는지 확인 → `ai_uploads`에서 지워 한 번만 쓰게. 주인이 `ai/<자기 id>/…`를 select·delete할 정책도 둔다(레코드를 먼저 지워도 파일을 지울 수 있게).

### 2. 라우트 `src/app/api/mcp/route.ts`
`references/route.template.ts`를 복사해 `SERVICE`, `TOOLS`(이름·설명·inputSchema), `callTool`의 RPC 매핑만 바꾼다.
- 도구 설명에 **AI가 지켜야 할 규칙**을 쓴다: 먼저 무엇을 확인할지(예: "list_cards로 이름 확인 후 add_log"), 범위, 공유는 사람이 원할 때만.
- `initialize`의 `instructions`에 사용자 이름과 맥락(연결된 상대 이름 등)을 넣는다.
- 오류는 `isError: true` + 사람 말로 바꾼 문장(check 제약 위반 → 허용 범위 안내).
- 업로드 도구는 `{ path, upload_url, method: "POST", headers: { apikey, Content-Type }, curl, expires_in_minutes }`를 돌려준다. curl의 파일 자리는 `@<파일 경로>` 표시만.

### 3. 앱 화면 (키 발급)
- "AI 비서로 기록하기" 칸: 키 없음 → [키 만들기] / 키 있음 → [새 키 만들기] [연결 끊기], 둘 다 확인 창.
- 만든 직후에만 키를 보여 주고 붙여 넣을 명령을 준다:
  `claude mcp add --transport http <서비스> <origin>/api/mcp --header "Authorization: Bearer <키>"`
  + "다른 AI 앱: 주소, 헤더" 한 줄 + [명령 복사].
- "이 키는 지금 한 번만 보여요", "AI가 넣은 데이터도 기본 비공개" 문구.

### 4. 테스트 (로컬 Supabase, node:test)
최소 항목: 해당 역할만 키 발급 / 로그인 없이 `issue_ai_key`·`ai_member` 직접 호출은 permission denied / 틀린 키 `invalid_key` / 읽기 도구가 주인 것만 / 쓰기 도구가 앱 규칙과 같은 기본값 / 다시 만들면 이전 키 끊김 / 키 삭제 후 끊김 / anon이 테이블을 직접 못 읽음 / (업로드) 열지 않은 경로 거부·한 번 쓰면 닫힘·덮어쓰기 불가·공유 안 한 사람은 파일 못 받음.

### 5. 점검
- `MCP_KEY=<로컬 키> node <skill-dir>/scripts/verify-mcp.mjs http://localhost:<port>/api/mcp <도구> '<JSON>'` — 401(키 없음·틀림), GET 405, initialize, 알림 202, tools/list, inputSchema, -32601, 도구 호출.
- 프로토콜 호환은 공식 SDK 클라이언트로 한 번: 스크래치 폴더에 `npm i @modelcontextprotocol/sdk@1` 후 `StreamableHTTPClientTransport(url, { requestInit: { headers: { Authorization } } })`로 connect → listTools → callTool. (프로젝트 의존성에 넣지 않는다.)
- 업로드는 실제 파일로: 도구가 준 curl을 그대로 실행 → 다른 사용자 권한으로 내려받아 크기 비교.

### 6. 배포
마이그레이션을 **먼저** 운영에 → 그다음 코드 배포. 운영 점검: 키 없이 401, 틀린 키 401. 마이그레이션 권한이 막히면 커밋만 하고 배포를 멈춘 뒤 사람에게 명령을 건넨다.

## 함정 (실제로 밟은 것)
- plpgsql `returns table(...)`의 열 이름이 인자 이름과 같으면 "parameter name used more than once" → `returns <테이블>`(행 타입)로.
- Supabase는 public 스키마의 새 함수에 **anon·authenticated 실행 권한을 따로** 준다(기본 권한). `revoke … from public`만 하면 그대로 열려 있다 → `from public, anon, authenticated`. RLS 판정용 함수까지 전부 적는다. 판정 함수를 anon에서 막으면 anon의 테이블 조회는 `[]` 대신 401이 된다(정상).
- 테스트에 "직접 부르면 permission denied" 단언을 꼭 넣는다(코치코치는 이걸 빼먹어 `ai_member`가 열려 있었다).
- Storage 삭제는 select 권한도 필요하다. 레코드를 지운 뒤 파일을 지우면 "레코드가 있으면 보임" 정책으로는 못 찾는다.
- 이미 열려 있는 Claude Code 세션에는 새로 붙인 MCP 도구가 안 보인다 → 사용자에게 재시작을 안내한다.
- 길이 같은 의미 제한(영상 90초)은 서버가 못 막는다(용량만 버킷이). 도구 설명에 "올리기 전 확인(ffprobe)"을 쓰고, 서버에서도 막아야 하면 별도 작업으로 남긴다.

## 멈추는 지점 (사람 몫)
- 도구 목록과 "AI가 해도 되는 일" 확정, 공유 기본값.
- 운영 마이그레이션 실행 권한, 실제 AI 앱에서 키 넣고 한 번 써 보기.

## 산출물
마이그레이션(키·ai_* 함수·업로드 정책), `/api/mcp` 라우트, 키 발급 화면, 테스트, verify-mcp 통과 출력, README의 연결 명령 한 줄.
