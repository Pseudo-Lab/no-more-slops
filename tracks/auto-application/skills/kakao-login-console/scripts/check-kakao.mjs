#!/usr/bin/env node
// 카카오 로그인 설정 점검: Supabase authorize가 카카오로 넘기는 주소에서 client_id·redirect_uri·scope를 본다.
// 사용: node check-kakao.mjs <SUPABASE_URL> <돌아올 사이트 URL>
// 예:   node check-kakao.mjs https://abcd.supabase.co https://myservice.kro.kr
// 키 값은 출력하지 않는다(길이만).
const [base, site] = process.argv.slice(2);
if (!base || !site) {
  console.error("사용: node check-kakao.mjs <SUPABASE_URL> <사이트 URL>");
  process.exit(2);
}
const start = `${base.replace(/\/$/, "")}/auth/v1/authorize?provider=kakao&redirect_to=${encodeURIComponent(site)}`;
const r = await fetch(start, { redirect: "manual" });
const loc = r.headers.get("location");
if (!loc) {
  const body = await r.text();
  console.log(`FAIL Supabase가 카카오로 보내지 않음 (HTTP ${r.status}): ${body.slice(0, 200)}`);
  console.log("→ provider가 꺼져 있거나(config push 안 함) client_id가 비어 있을 수 있다.");
  process.exit(1);
}
const u = new URL(loc);
const ok = (cond, msg, fix) => console.log(`${cond ? "OK  " : "FAIL"} ${msg}${cond ? "" : `\n     → ${fix}`}`);
ok(u.host === "kauth.kakao.com", `카카오 인증 서버로 보냄: ${u.host}`, "provider 설정 확인");
const id = u.searchParams.get("client_id") ?? "";
ok(id.length === 32, `client_id 길이 ${id.length}자 (REST API 키는 32자)`, "REST API 키를 넣었는지(JavaScript 키·네이티브 키 아님) 확인");
const redirect = u.searchParams.get("redirect_uri") ?? "";
ok(redirect === `${base.replace(/\/$/, "")}/auth/v1/callback`, `redirect_uri: ${redirect}`, "카카오 콘솔에 이 주소를 그대로 등록");
console.log(`     scope: ${u.searchParams.get("scope")} → 콘솔 동의항목에 전부 켜져 있어야 한다(없으면 KOE205)`);

// History: KOE 오류는 카카오 로그인을 마친 뒤에야 나온다(가짜 client_id도 로그인 화면까지는 간다). 그래서 여기선 못 잡고 사람이 본다.
console.log("     KOE 오류(KOE006·KOE101·KOE205 등)는 실제 로그인 뒤에만 보인다 → SKILL.md 오류표로 사람이 확인");
