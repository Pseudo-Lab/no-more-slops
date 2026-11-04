// 투명 배경 글자 오버레이를 PNG 프레임으로 뽑는다 (compose_cut.py --overlay 로 영상에 얹는다).
// 유료 API 없이 로컬 Chrome(puppeteer-core)만 쓴다.
//
// 사용법:
//   node scripts/overlay.mjs <overlay.html> <out_dir> [--seconds 2.5] [--fps 30] [--size 1080x1920]
//        [--query "text=...&t0=0.25"] [--root <정적 서버 루트, 기본 현재 폴더>] [--still t:out.png]
//
// 오버레이 HTML 규칙:
//   - window.renderAt(t: 초) 를 정의한다. 같은 t면 항상 같은 그림 (실시간 시계 금지)
//   - 준비가 끝나면 window.sceneReady = true (글꼴 로딩까지 기다린 뒤)
//   - 배경은 투명 (html, body { background: transparent })
// 글꼴 파일(fontUrl)은 --root 기준 경로로 준다. 외부 글꼴 서버는 쓰지 않는다.
// 결과: <out_dir>/o0000.png … (알파 포함)
// puppeteer-core 찾기: 이 스킬 폴더에서 npm install, 또는 PUPPETEER_CORE_DIR=<node_modules가 있는 폴더>
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

async function loadPuppeteer() {
  try {
    return (await import("puppeteer-core")).default;
  } catch (e) {
    const dir = process.env.PUPPETEER_CORE_DIR;
    if (!dir) throw new Error("puppeteer-core가 없다: 스킬 폴더에서 `npm install` 하거나 PUPPETEER_CORE_DIR을 준다");
    const req = createRequire(path.join(path.resolve(dir), "noop.js"));
    const mod = await import(pathToFileURL(req.resolve("puppeteer-core")).href);
    return mod.default ?? mod;
  }
}

function findChrome() {
  const c = [process.env.CHROME_PATH, "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium", "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"];
  return c.find((p) => p && fs.existsSync(p));
}

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args.splice(i, 2)[1] : def;
};
const seconds = Number(opt("seconds", 2.5));
const fps = Number(opt("fps", 30));
const [width, height] = opt("size", "1080x1920").split("x").map(Number);
const query = opt("query", "").replace(/^\?/, "");
const root = path.resolve(opt("root", process.cwd()));
const stills = [];
for (let s; (s = opt("still")); ) stills.push(s);
const [htmlArg, outArg] = args;
if (!htmlArg || !outArg) {
  console.error("사용법: node scripts/overlay.mjs <overlay.html> <out_dir> [--seconds 2.5] [--fps 30] [--size 1080x1920] [--query k=v&...] [--root dir] [--still t:out.png]");
  process.exit(1);
}
const html = path.resolve(htmlArg);
const outDir = path.resolve(outArg);
if (!html.startsWith(root + path.sep)) throw new Error(`오버레이 파일이 --root(${root}) 안에 있어야 한다`);
const chrome = findChrome();
if (!chrome) throw new Error("Chrome을 찾지 못했다 (CHROME_PATH)");
const puppeteer = await loadPuppeteer();

// file://에서는 글꼴·모듈 로딩이 막히므로 루트를 정적 서버로 연다 (루트 밖 접근 금지)
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json", ".png": "image/png",
  ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf" };
const server = http.createServer((req, res) => {
  const p = path.resolve(root, "." + decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(root + path.sep) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
    res.writeHead(404).end();
    return;
  }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] ?? "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const url = `http://127.0.0.1:${server.address().port}/${path.relative(root, html).split(path.sep).join("/")}${query ? "?" + query : ""}`;

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ["--hide-scrollbars", "--font-render-hinting=none"] });
const started = Date.now();
try {
  const page = await browser.newPage();
  page.on("console", (m) => m.type() === "error" && console.error("[overlay]", m.text()));
  page.on("pageerror", (e) => console.error("[overlay]", e.message));
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: "load" });
  await page.waitForFunction("window.sceneReady === true", { timeout: 30000 });
  for (const s of stills) {
    const i = s.indexOf(":");
    await page.evaluate((t) => window.renderAt(t), Number(s.slice(0, i)));
    await page.screenshot({ path: path.resolve(s.slice(i + 1)), omitBackground: true });
    console.log("정지 이미지:", s.slice(i + 1));
  }
  fs.mkdirSync(outDir, { recursive: true });
  const total = Math.round(seconds * fps);
  for (let i = 0; i < total; i++) {
    await page.evaluate((t) => window.renderAt(t), i / fps);
    await page.screenshot({ path: path.join(outDir, `o${String(i).padStart(4, "0")}.png`), omitBackground: true });
  }
  console.log(`완료: 프레임 ${total}장 → ${path.relative(process.cwd(), outDir) || "."} (${((Date.now() - started) / 1000).toFixed(1)}초)`);
} finally {
  await browser.close();
  server.close();
}
