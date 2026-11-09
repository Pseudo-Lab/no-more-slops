#!/usr/bin/env node
// 상태 없는 MCP 엔드포인트 점검(의존성 없음). 키는 환경변수로만 받고 출력하지 않는다.
// 사용: MCP_KEY=<키> node verify-mcp.mjs <엔드포인트> [도구 이름] [JSON 인자]
// 예:   MCP_KEY=cc_xxx node verify-mcp.mjs http://localhost:3000/api/mcp list_cards '{}'
const [endpoint, tool, rawArgs] = process.argv.slice(2);
const key = process.env.MCP_KEY;
if (!endpoint || !key) {
  console.error("사용: MCP_KEY=<키> node verify-mcp.mjs <엔드포인트> [도구] [JSON 인자]");
  process.exit(2);
}
let failed = 0;
const ok = (cond, msg) => {
  console.log(`${cond ? "OK  " : "FAIL"} ${msg}`);
  if (!cond) failed++;
};
const post = (body, auth) =>
  fetch(endpoint, {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json, text/event-stream", ...(auth ? { authorization: `Bearer ${auth}` } : {}) },
    body: JSON.stringify(body),
  });
const rpc = async (method, params, id = 1) => (await post({ jsonrpc: "2.0", id, method, params }, key)).json();

ok((await post({ jsonrpc: "2.0", id: 1, method: "tools/list" })).status === 401, "키 없으면 401");
ok((await post({ jsonrpc: "2.0", id: 1, method: "tools/list" }, "wrong_key_for_check")).status === 401, "틀린 키면 401");
ok((await fetch(endpoint)).status === 405, "GET(SSE)은 405");

const init = await rpc("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "verify-mcp", version: "0" } });
ok(!!init.result?.protocolVersion, `initialize → ${init.result?.serverInfo?.name} / 프로토콜 ${init.result?.protocolVersion}`);
ok((await post({ jsonrpc: "2.0", method: "notifications/initialized" }, key)).status === 202, "알림(id 없음)은 202");

const list = await rpc("tools/list", {});
const names = list.result?.tools?.map((t) => t.name) ?? [];
ok(names.length > 0, `tools/list → ${names.join(", ")}`);
ok(list.result?.tools?.every((t) => t.inputSchema?.type === "object"), "모든 도구에 inputSchema(type: object)");

ok((await rpc("no/such/method", {})).error?.code === -32601, "모르는 메서드는 -32601");

if (tool) {
  const r = await rpc("tools/call", { name: tool, arguments: rawArgs ? JSON.parse(rawArgs) : {} });
  const text = r.result?.content?.[0]?.text ?? JSON.stringify(r.error);
  ok(!r.error && !r.result?.isError, `tools/call ${tool} → ${text.slice(0, 300)}`);
}
console.log(failed ? `\n${failed}개 실패` : "\n모두 통과");
process.exit(failed ? 1 : 0);
