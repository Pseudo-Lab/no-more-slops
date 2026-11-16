#!/usr/bin/env node
// 출시 기본기 점검. 의존성 없음(Node 20+).
//   node check-launch.mjs <사이트 URL> [--env <.env 파일>]
// Supabase 주소·공개 키는 --env 파일(NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY 또는 _ANON_KEY)이나
// 같은 이름의 환경변수에서 읽는다. 없으면 DB 항목은 건너뛴다.
// 운영에 돌리면 events에 'landing' 한 줄이 들어간다(지표 1건). 한 항목이라도 FAIL이면 exit 2.
import { readFileSync } from "node:fs";

const [site, ...rest] = process.argv.slice(2);
if (!site) {
  console.error("usage: node check-launch.mjs <site-url> [--env <file>]");
  process.exit(1);
}
const env = { ...process.env };
const envIdx = rest.indexOf("--env");
if (envIdx >= 0) {
  for (const line of readFileSync(rest[envIdx + 1], "utf8").split("\n")) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*"?([^"\n]*)"?\s*$/);
    if (m) env[m[1]] = m[2];
  }
}
const supaUrl = env.NEXT_PUBLIC_SUPABASE_URL;
const supaKey = env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

let failed = 0;
function report(name, ok, detail) {
  failed += ok ? 0 : 1;
  console.log(`${ok ? "ok  " : "FAIL"} ${name}${detail ? ` — ${detail}` : ""}`);
}
const page = async (path) => {
  const r = await fetch(new URL(path, site), { redirect: "manual" });
  return { status: r.status, headers: r.headers, body: await r.text() };
};

// 1. 법적 표기
const privacy = await page("/privacy");
report("/privacy 200", privacy.status === 200, String(privacy.status));
report("처리방침에 '받지 않는 정보' 절", /받지 않|저장하지 않|수집하지 않/.test(privacy.body));
report("처리방침에 문의 mailto", /mailto:/.test(privacy.body));
report("처리방침에 국외 이전 표", /국외 이전/.test(privacy.body));
const terms = await page("/terms");
report("/terms 200", terms.status === 200, String(terms.status));

// 2. 에러 화면·보안 헤더
const missing = await page("/__launch-check-" + Date.now());
report("없는 주소는 404", missing.status === 404, String(missing.status));
report("404가 프레임워크 기본 화면이 아님", !/This page could not be found/.test(missing.body));
const home = await page("/");
report("홈 200", home.status === 200, String(home.status));
report("HSTS 헤더", site.startsWith("https:") ? !!home.headers.get("strict-transport-security") : true, site.startsWith("https:") ? "" : "http라 건너뜀");
// 홈은 로그인 상태를 본 뒤 클라이언트에서 그려져 첫 HTML에 바닥 링크가 없을 수 있다. 서로 잇는 링크로 본다.
report("약관·처리방침·탈퇴가 서로 링크됨", /href="\/terms"/.test(privacy.body) && /href="\/privacy"/.test(terms.body) && /href="\/account"/.test(privacy.body));

// 3. 퍼널 지표와 탈퇴 함수 (익명 키로)
if (!supaUrl || !supaKey) {
  console.log("skip Supabase 항목: NEXT_PUBLIC_SUPABASE_URL / _PUBLISHABLE_KEY 없음");
} else {
  const rest = (path, init = {}) =>
    fetch(`${supaUrl}/rest/v1/${path}`, { ...init, headers: { apikey: supaKey, Authorization: `Bearer ${supaKey}`, "Content-Type": "application/json", ...(init.headers ?? {}) } });
  const ins = await rest("events", { method: "POST", body: JSON.stringify({ step: "landing" }), headers: { Prefer: "return=minimal" } });
  report("지표: 익명으로 단계 넣기", ins.status === 201, String(ins.status));
  const bad = await rest("events", { method: "POST", body: JSON.stringify({ step: "bogus" }) });
  report("지표: 정해진 단계 이름만", bad.status >= 400, String(bad.status));
  const sel = await rest("events?select=step&limit=1");
  const rows = sel.status === 200 ? await sel.json() : null;
  report("지표: 익명으로 읽기 차단", sel.status !== 200 || (Array.isArray(rows) && rows.length === 0), `${sel.status} ${rows ? JSON.stringify(rows) : ""}`);
  const funnel = await rest("rpc/admin_funnel", { method: "POST", body: "{}" });
  report("지표: 운영자 아니면 숫자도 못 봄", funnel.status >= 400, String(funnel.status));
  const del = await rest("rpc/delete_my_account", { method: "POST", body: "{}" });
  report("탈퇴: 로그인 없이 호출 차단", del.status >= 400, String(del.status));
  const paths = await rest("rpc/my_video_paths", { method: "POST", body: "{}" });
  report("탈퇴: 파일 목록 익명 호출 차단", paths.status >= 400, String(paths.status));
}

console.log(failed ? `\n${failed}개 FAIL` : "\n모두 통과");
process.exit(failed ? 2 : 0);
