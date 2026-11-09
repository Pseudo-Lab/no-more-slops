// service-mcp 템플릿: src/app/api/mcp/route.ts
// AI 비서(Claude 등)가 사용자 대신 자기 데이터를 읽고 넣는 MCP 서버.
// 상태 없는 Streamable HTTP: POST 한 번에 JSON-RPC 메시지 하나, 응답은 JSON 하나. 세션·SSE 없음.
// 신원은 사용자가 앱에서 만든 개인 키(Authorization: Bearer)뿐. 키 확인과 권한은 DB 함수(ai_*)가 하고, 여기엔 비밀 키가 없다.
// 짝이 되는 SQL: ai.template.sql (entries 예시). 도구 이름·설명·RPC 매핑만 자기 서비스에 맞게 바꾼다.
import { createClient } from "@supabase/supabase-js";

const SERVICE = "myservice";
const PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];

// 도구 설명은 AI가 지킬 규칙이다: 무엇을 먼저 확인할지, 범위, 사람이 원할 때만 할 일.
const TOOLS = [
  {
    name: "list_entries",
    description: "사용자의 기록 목록(최신순).",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "add_entry",
    description: "기록 하나를 남긴다. 파일을 붙이려면 먼저 start_file_upload로 받은 curl로 올리고 path를 file_path에 넣는다.",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string", minLength: 1, maxLength: 60 },
        body: { type: "string", maxLength: 1000 },
        file_path: { type: "string", description: "start_file_upload로 받아 업로드를 마친 path" },
      },
      required: ["title"],
    },
  },
  {
    name: "start_file_upload",
    description: "파일을 올릴 일회용 주소를 받는다(짧게 열리고 한 번만). 받은 curl 명령으로 올린 뒤 add_entry에 path를 넣는다.",
    inputSchema: { type: "object", properties: { format: { type: "string", enum: ["pdf", "png", "jpg"] } } },
  },
];

const MIME = { pdf: "application/pdf", png: "image/png", jpg: "image/jpeg" } as const;

type Rpc = { jsonrpc: "2.0"; id?: string | number; method: string; params?: Record<string, unknown> };

const db = () => createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!, { auth: { persistSession: false } });

const reply = (id: Rpc["id"], result: unknown) => Response.json({ jsonrpc: "2.0", id, result });
const fail = (id: Rpc["id"] | null, code: number, message: string, status = 200) => Response.json({ jsonrpc: "2.0", id, error: { code, message } }, { status });
const unauthorized = () =>
  Response.json(
    { jsonrpc: "2.0", id: null, error: { code: -32001, message: "앱에서 만든 AI 키를 Authorization: Bearer 로 보내 주세요." } },
    { status: 401, headers: { "WWW-Authenticate": `Bearer realm="${SERVICE}"` } },
  );

// 큰 파일은 이 서버를 거치지 않는다(Vercel 함수 본문 4.5MB 한도). 공개 키 + 일회용 경로만 건넨다.
async function startUpload(k: string, format: string) {
  const ext = format in MIME ? (format as keyof typeof MIME) : "pdf";
  const { data: path, error } = await db().rpc("ai_start_upload", { k, ext });
  if (error) return { data: null, error };
  const url = `${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/files/${path}`;
  const apikey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!;
  return {
    data: {
      path,
      upload_url: url,
      method: "POST",
      headers: { apikey, "Content-Type": MIME[ext] },
      curl: `curl -sS -X POST "${url}" -H "apikey: ${apikey}" -H "Content-Type: ${MIME[ext]}" --data-binary @<파일 경로>`,
    },
    error: null,
  };
}

async function callTool(k: string, name: string, args: Record<string, unknown>) {
  const sb = db();
  const { data, error } =
    name === "list_entries"
      ? await sb.rpc("ai_list_entries", { k })
      : name === "add_entry"
        ? await sb.rpc("ai_add_entry", { k, title: String(args.title ?? ""), body: args.body ?? null, file_path: args.file_path ?? null })
        : name === "start_file_upload"
          ? await startUpload(k, String(args.format ?? "pdf"))
          : { data: null, error: { message: `unknown_tool ${name}` } };
  // check 제약 위반은 사람 말로 바꿔 돌려준다. AI가 범위를 고쳐 다시 부를 수 있게.
  if (error) return { content: [{ type: "text", text: error.message.includes("check constraint") ? "값이 허용 범위를 벗어났어요(제목 60자, 본문 1000자)." : error.message }], isError: true };
  return { content: [{ type: "text", text: JSON.stringify(data) }] };
}

export async function POST(req: Request) {
  const k = req.headers.get("authorization")?.match(/^Bearer\s+(\S+)$/i)?.[1];
  if (!k) return unauthorized();

  const msg = (await req.json().catch(() => null)) as Rpc | null;
  if (!msg || Array.isArray(msg) || typeof msg.method !== "string") return fail(null, -32600, "Invalid Request", 400);
  // 알림(id 없음)에는 답하지 않는다.
  if (msg.id === undefined) return new Response(null, { status: 202 });

  // 틀린 키는 처음부터 막아 AI 앱이 연결 실패를 바로 보여 주게 한다.
  const { data: name, error } = await db().rpc("ai_whoami", { k });
  if (error || !name) return unauthorized();

  switch (msg.method) {
    case "initialize": {
      const asked = String(msg.params?.protocolVersion ?? "");
      return reply(msg.id, {
        protocolVersion: PROTOCOLS.includes(asked) ? asked : PROTOCOLS[0],
        capabilities: { tools: {} },
        serverInfo: { name: SERVICE, version: "1.0.0" },
        instructions: `${name}님의 ${SERVICE}. 넣기 전에 list_entries로 이미 있는지 확인한다.`,
      });
    }
    case "ping":
      return reply(msg.id, {});
    case "tools/list":
      return reply(msg.id, { tools: TOOLS });
    case "tools/call":
      return reply(msg.id, await callTool(k, String(msg.params?.name), (msg.params?.arguments as Record<string, unknown>) ?? {}));
    default:
      return fail(msg.id, -32601, `Method not found: ${msg.method}`);
  }
}

// 서버가 먼저 보내는 스트림(SSE)은 열지 않는다.
export function GET() {
  return new Response(null, { status: 405, headers: { Allow: "POST" } });
}
