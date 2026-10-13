// 견종 프리셋과 캐릭터 얼굴(SVG). 프리셋에 없는 견종은 기본 강아지로 그린다.
// 얼굴은 부품(귀·털뭉치·주둥이·무늬)을 조합해서 만든다. viewBox 0 0 64 64.
// 통통한 머리, 아래쪽에 모인 큰 눈, 작은 코가 귀여움의 핵심.

const INK = '#2a211e';
const LINE = 'rgba(70,45,30,0.2)';
const PINK = '#f7b4c2';

export const BREEDS = [
  { name: '말티즈', slug: 'maltese', bg: '#ffe3ea', fur: '#fffdf9', ear: ['long', '#f5eee4'], top: '#fffdf9', muzzle: '#fffdf9' },
  { name: '푸들', slug: 'poodle', bg: '#fff0d9', fur: '#dc9d62', ear: ['curly', '#cf8c4f'], top: '#dc9d62', muzzle: '#eab986' },
  { name: '포메라니안', slug: 'pomeranian', bg: '#fff3c4', fur: '#f4a74f', ear: ['small', '#f4a74f'], ruff: '#f8bd6c', muzzle: '#fbd29f' },
  { name: '시츄', slug: 'shihtzu', bg: '#ece6ff', fur: '#fffdf9', ear: ['long', '#b98455'], patches: '#c08d5e', bow: true, muzzle: '#fffdf9' },
  { name: '비숑 프리제', slug: 'bichon', bg: '#dff3ff', fur: '#fffdf9', ruff: '#fffdf9', top: '#fffdf9', muzzle: '#fffdf9' },
  { name: '치와와', slug: 'chihuahua', bg: '#ffe8d6', fur: '#ebbd80', ear: ['big', '#ebbd80'], muzzle: '#f6dab0' },
  { name: '웰시코기', slug: 'corgi', bg: '#fff0d6', fur: '#ec9645', ear: ['big', '#ec9645'], blaze: '#fffdf9', cheeks: '#fffdf9', muzzle: '#fffdf9', tongue: true },
  { name: '진돗개', slug: 'jindo', bg: '#e4f2e4', fur: '#f5e9d2', ear: ['pointy', '#f5e9d2'], muzzle: '#fffaf1' },
  { name: '시바견', slug: 'shiba', bg: '#ffe6d1', fur: '#dc8740', ear: ['small', '#dc8740'], cheeks: '#fff7ea', muzzle: '#fff7ea', brows: '#fff7ea' },
  { name: '골든 리트리버', slug: 'golden', bg: '#fff3cf', fur: '#e7ad5d', ear: ['floppy', '#d99a45'], muzzle: '#f1c587', tongue: true },
  { name: '래브라도 리트리버', slug: 'labrador', bg: '#f2ecdf', fur: '#f2d7a0', ear: ['floppy', '#e5c37f'], muzzle: '#f8e6c0' },
  { name: '닥스훈트', slug: 'dachshund', bg: '#fbe3d3', fur: '#a85b2e', ear: ['long', '#8c4823'], muzzle: '#bd7140', eyeRing: true },
  { name: '요크셔테리어', slug: 'yorkie', bg: '#e3ecf7', fur: '#ddaa66', cap: '#7f8c9c', ear: ['pointy', '#ddaa66'], muzzle: '#e8bf86', bow: true },
  { name: '프렌치 불독', slug: 'frenchie', bg: '#f0e6ff', fur: '#ecd8b6', ear: ['bat', '#ecd8b6'], mask: '#5a463b', wrinkle: true },
  { name: '보스턴테리어', slug: 'boston', bg: '#e6eef8', fur: '#2f2a2b', ear: ['bat', '#2f2a2b'], blaze: '#fffdf9', muzzle: '#fffdf9', eyeRing: true },
  { name: '퍼그', slug: 'pug', bg: '#fff1d6', fur: '#e9d3a5', ear: ['fold', '#3f3431'], mask: '#3f3431', wrinkle: true },
  { name: '비글', slug: 'beagle', bg: '#e5f4e1', fur: '#a1602f', ear: ['long', '#7e4723'], blaze: '#fffdf9', muzzle: '#fffdf9', eyeRing: true },
  { name: '보더콜리', slug: 'bordercollie', bg: '#e0ecf5', fur: '#2f2a2b', ear: ['fold', '#2f2a2b'], blaze: '#fffdf9', muzzle: '#fffdf9', eyeRing: true, tongue: true },
  { name: '미니어처 슈나우저', slug: 'schnauzer', bg: '#e8eef2', fur: '#959aa1', ear: ['fold', '#81868d'], brows: '#f5f5f5', beard: '#f5f5f5', muzzle: '#f5f5f5' },
  { name: '말티푸', slug: 'maltipoo', bg: '#ffeede', fur: '#f4d8b2', ear: ['curly', '#ebc495'], top: '#f4d8b2', muzzle: '#f9e6cb' },
  { name: '사모예드', slug: 'samoyed', bg: '#dceeff', fur: '#fffdf9', ear: ['pointy', '#fffdf9'], ruff: '#fffdf9', muzzle: '#fffdf9', tongue: true },
];

export const DEFAULT_BREED = { name: '기타', slug: 'mixed', bg: '#efe9df', fur: '#cba071', ear: ['floppy', '#ad7f53'], muzzle: '#e7cba5' };

// 생성한 일러스트가 src/assets/characters/<slug>.png 에 있으면 SVG 대신 그 그림을 쓴다
const IMAGES = Object.fromEntries(
  Object.entries(import.meta.glob('./assets/characters/*.{png,webp}', { eager: true, query: '?url', import: 'default' }))
    .map(([path, url]) => [path.split('/').pop().replace(/\.(png|webp)$/, ''), url]),
);
const imageFor = (b) => IMAGES[b.slug] ? `<img class="char-img" src="${IMAGES[b.slug]}" alt="" />` : null;

export const breedOf = (name) => BREEDS.find((b) => b.name === name) ?? CATS.find((c) => c.name === name) ?? DEFAULT_BREED;

const shape = (d, fill) => `<path d="${d}" fill="${fill}" stroke="${LINE}" stroke-width="1" stroke-linejoin="round"/>`;
const circle = (cx, cy, r, fill, line = true) =>
  `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}"${line ? ` stroke="${LINE}" stroke-width="1"` : ''}/>`;
const oval = (cx, cy, rx, ry, fill, extra = '') => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}" ${extra}/>`;
const mirror = (svg) => `${svg}<g transform="translate(64 0) scale(-1 1)">${svg}</g>`;

// 몽글몽글한 털뭉치: 둘레에 작은 원 + 가운데 큰 원
function cloud(cx, cy, r, color, n) {
  let s = '';
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 - Math.PI / 2;
    s += circle((cx + Math.cos(a) * r).toFixed(1), (cy + Math.sin(a) * r).toFixed(1), (r * 0.45).toFixed(1), color);
  }
  return s + circle(cx, cy, r, color, false);
}

function ears([type, color]) {
  switch (type) {
    case 'pointy': // 진돗개·사모예드·요키: 끝이 둥근 세모 귀
      return mirror(shape('M13 31 C11 21 13 11 17.5 7 C22 9 27 15 29.5 21 Z', color) + shape('M16.5 26 C16 20 17 14 18.5 12 C21 14 24 18 25 21 Z', PINK));
    case 'small': // 시바·포메: 작고 동그란 세모 귀
      return mirror(shape('M15 27 C14 20 16 13 19.5 11 C23 12.5 26.5 16 28.5 20 Z', color) + shape('M18 23.5 C18 19.5 19 16 20.3 15 C22 16.5 24 18.5 25 20.5 Z', PINK));
    case 'big': // 치와와·코기: 큰 귀
      return mirror(shape('M12.5 33 C8 22 8 9 11 3.5 C17 5 25 12 29.5 20 Z', color) + shape('M15 27 C12.5 20 12.5 13 13.8 9.5 C17.5 11 22.5 16 25 21 Z', PINK));
    case 'bat': // 프렌치 불독·보스턴: 둥글고 큰 박쥐 귀
      return mirror(shape('M14 30 C8 21 8 8 13 4.5 C19 3.5 26 12 29 20 Z', color) + shape('M16 25 C12.5 19 12.5 11 15 9 C18.5 9 22.5 15 24.5 20 Z', PINK));
    case 'floppy': // 리트리버: 물방울 모양 늘어진 귀
      return mirror(shape('M18 23 C10 22 6.5 33 7.5 43 C8.5 49 15 50 17.5 45 C19.5 38 20.5 29 18 23 Z', color));
    case 'long': // 말티즈·비글·닥스: 길게 늘어진 귀
      return mirror(shape('M18.5 23 C10 22 5.5 35 6 47 C6.5 55 14 57 16.5 51 C19 43 21 30 18.5 23 Z', color));
    case 'fold': // 퍼그·슈나우저·보더콜리: 접힌 귀
      return mirror(shape('M13.5 26 C13 18.5 19 14 28.5 17 C25.5 20 22.5 25 21 30 C17.5 30.5 14.5 29 13.5 26 Z', color));
    case 'curly': // 푸들·말티푸: 곱슬 귀
      return mirror([[13.5, 31, 6.5], [10.5, 39, 6.5], [11.5, 47, 6], [16, 52, 5]].map(([x, y, r]) => circle(x, y, r, color)).join(''));
    default:
      return '';
  }
}

export function dogFace(breed = DEFAULT_BREED) {
  const b = typeof breed === 'string' ? breedOf(breed) : breed;
  const img = imageFor(b);
  if (img) return img;
  if (b.cat) return catFace(b);
  const p = [];
  if (b.ruff) p.push(cloud(32, 39, 21, b.ruff, 16));
  if (b.ear) p.push(ears(b.ear));
  // 통통한 머리
  p.push(oval(32, 37, 20.5, 19, b.fur, `stroke="${LINE}" stroke-width="1"`));
  if (b.top) p.push(cloud(32, 20, 6.5, b.top, 8));
  if (b.cap) p.push(`<path d="M12.5 33 C13 22 21 17.5 32 17.5 C43 17.5 51 22 51.5 33 C45 28.5 39 27.5 32 29 C25 27.5 19 28.5 12.5 33 Z" fill="${b.cap}"/>`);
  if (b.patches) p.push(oval(24, 37.5, 6.8, 6, b.patches) + oval(40, 37.5, 6.8, 6, b.patches));
  if (b.blaze) p.push(`<path d="M30 18.5 C31.3 18 32.7 18 34 18.5 C35 25 36.5 33 37.5 41 L26.5 41 C27.5 33 29 25 30 18.5 Z" fill="${b.blaze}"/>`);
  if (b.cheeks) p.push(oval(23.5, 45, 8, 6.2, b.cheeks) + oval(40.5, 45, 8, 6.2, b.cheeks));
  // 머리 윗부분 살짝 광택
  p.push(oval(25, 26, 6, 3.5, 'rgba(255,255,255,0.28)', 'transform="rotate(-20 25 26)"'));
  if (b.wrinkle) p.push(`<path d="M28 27.5 Q32 25.5 36 27.5 M29.5 30.5 Q32 29.3 34.5 30.5" fill="none" stroke="rgba(90,60,40,0.35)" stroke-width="1.1" stroke-linecap="round"/>`);
  // 주둥이
  p.push(oval(32, 45, b.mask ? 9 : 7.8, b.mask ? 7 : 5.8, b.mask ?? b.muzzle ?? b.fur));
  if (b.brows) p.push(oval(24.5, 32.5, 3.3, 1.8, b.brows, 'transform="rotate(-10 24.5 32.5)"') + oval(39.5, 32.5, 3.3, 1.8, b.brows, 'transform="rotate(10 39.5 32.5)"'));
  if (b.beard) p.push(cloud(32, 50, 4.5, b.beard, 7));
  // 큰 눈 + 반짝이 두 개
  for (const x of [24.5, 39.5]) {
    if (b.eyeRing) p.push(circle(x, 38, 4.2, '#fffdf9', false));
    p.push(circle(x, 38, 3.3, INK, false) + circle(x + 1.1, 36.8, 1.2, '#fff', false) + circle(x - 1, 39.3, 0.55, '#fff', false));
  }
  // 볼 터치
  p.push(oval(19.5, 44, 3.3, 2, 'rgba(255,120,150,0.4)') + oval(44.5, 44, 3.3, 2, 'rgba(255,120,150,0.4)'));
  // 코
  p.push(`<path d="M29.4 42.2 C30.8 41.2 33.2 41.2 34.6 42.2 C34.6 43.8 33.3 45 32 45 C30.7 45 29.4 43.8 29.4 42.2 Z" fill="${INK}"/>`);
  p.push(oval(31.2, 42.3, 1, 0.5, 'rgba(255,255,255,0.6)'));
  if (b.tongue) p.push(`<path d="M30.2 47.6 C30.2 50.6 33.8 50.6 33.8 47.6 Z" fill="#ff8ea5"/>`);
  const mouth = b.mask ? '#fff4ea' : INK;
  p.push(`<path d="M29 46.6 Q30.6 48.2 32 46.4 Q33.4 48.2 35 46.6" fill="none" stroke="${mouth}" stroke-width="1.2" stroke-linecap="round"/>`);
  if (b.bow) p.push(`<path d="M32 19 C29 15.5 25.5 15.5 25.5 19 C25.5 22.5 29 22.5 32 19 Z M32 19 C35 15.5 38.5 15.5 38.5 19 C38.5 22.5 35 22.5 32 19 Z" fill="#ff7a9a"/>` + circle(32, 19, 1.7, '#ff5683', false));
  return `<svg viewBox="0 0 64 64" aria-hidden="true">${p.join('')}</svg>`;
}

// ---------- 길고양이 ----------
// 고양이는 "내 가족 등록"이 아니라 길에서 만난 친구라서 무늬만 고른다.
export const CATS = [
  { name: '치즈', slug: 'cat-cheese', cat: true, bg: '#fff0d6', fur: '#f3a64f', stripe: '#d98530', muzzle: '#fff6e6' },
  { name: '고등어', slug: 'cat-mackerel', cat: true, bg: '#e6ecf2', fur: '#a6acb3', stripe: '#5d636b', muzzle: '#f4f5f6' },
  { name: '삼색이', slug: 'cat-calico', cat: true, bg: '#fde8e8', fur: '#fffdf9', earL: '#e9973f', earR: '#3a3433', patchL: '#e9973f', patchR: '#3a3433', muzzle: '#fffdf9' },
  { name: '턱시도', slug: 'cat-tuxedo', cat: true, bg: '#e6eaf5', fur: '#2f2a2b', blaze: '#fffdf9', muzzle: '#fffdf9', eyeRing: true, whisker: 'rgba(255,255,255,0.75)' },
  { name: '까망이', slug: 'cat-black', cat: true, bg: '#efe6f7', fur: '#2f2a2b', muzzle: '#3a3435', iris: '#e8c547', whisker: 'rgba(255,255,255,0.75)' },
];
export const isCat = (name) => CATS.some((c) => c.name === name);

export function catFace(cat) {
  const c = typeof cat === 'string' ? CATS.find((x) => x.name === cat) ?? CATS[0] : cat;
  const p = [];
  const ear = (d, inner, color) => shape(d, color) + shape(inner, PINK);
  p.push(ear('M12 31 C10.5 21 12 11 14.5 5.5 C20 8.5 25.5 13.5 28.5 18.5 Z', 'M15 25.5 C14.5 19.5 15.5 13.5 16.8 10.5 C20 12.5 23.5 16 25 19 Z', c.earL ?? c.fur));
  p.push(`<g transform="translate(64 0) scale(-1 1)">${ear('M12 31 C10.5 21 12 11 14.5 5.5 C20 8.5 25.5 13.5 28.5 18.5 Z', 'M15 25.5 C14.5 19.5 15.5 13.5 16.8 10.5 C20 12.5 23.5 16 25 19 Z', c.earR ?? c.fur)}</g>`);
  p.push(oval(32, 37.5, 21.5, 18.5, c.fur, `stroke="${LINE}" stroke-width="1"`));
  if (c.patchL) p.push(`<path d="M11.5 34 C12 24 19 19.5 27 19.5 C26 25 22 31 13 37 Z" fill="${c.patchL}"/>`);
  if (c.patchR) p.push(`<path d="M52.5 34 C52 24 45 19.5 37 19.5 C38.5 24 42 30 51.5 37.5 Z" fill="${c.patchR}"/>`);
  if (c.blaze) p.push(`<path d="M30.5 24 C31.5 23.5 32.5 23.5 33.5 24 C34.5 30 36 36 37 42 L27 42 C28 36 29.5 30 30.5 24 Z" fill="${c.blaze}"/>`);
  if (c.stripe) {
    p.push(`<path d="M28.5 21 L29 26.5 M32 19.8 L32 26.8 M35.5 21 L35 26.5" stroke="${c.stripe}" stroke-width="2.3" stroke-linecap="round"/>`);
    p.push(mirror(`<path d="M11.5 36.5 L17 37.5 M12 41 L17 41" stroke="${c.stripe}" stroke-width="2" stroke-linecap="round"/>`));
  }
  p.push(oval(25, 26.5, 6, 3.3, 'rgba(255,255,255,0.22)', 'transform="rotate(-20 25 26.5)"'));
  // 볼록한 고양이 주둥이
  p.push(oval(29.2, 45.6, 4.3, 3.4, c.muzzle) + oval(34.8, 45.6, 4.3, 3.4, c.muzzle));
  for (const x of [24.5, 39.5]) {
    if (c.eyeRing) p.push(circle(x, 38, 4.2, '#fffdf9', false));
    if (c.iris) p.push(circle(x, 38, 3.8, c.iris, false) + circle(x, 38, 2.3, INK, false));
    else p.push(circle(x, 38, 3.3, INK, false));
    p.push(circle(x + 1.1, 36.8, 1.2, '#fff', false) + circle(x - 1, 39.3, 0.55, '#fff', false));
  }
  p.push(oval(19, 44, 3.3, 2, 'rgba(255,120,150,0.4)') + oval(45, 44, 3.3, 2, 'rgba(255,120,150,0.4)'));
  p.push(`<path d="M30.2 42.6 C31 42 33 42 33.8 42.6 C33.4 43.8 32.6 44.5 32 44.5 C31.4 44.5 30.6 43.8 30.2 42.6 Z" fill="#f08aa0"/>`);
  p.push(`<path d="M29.4 46.4 Q30.8 47.8 32 46.2 Q33.2 47.8 34.6 46.4" fill="none" stroke="${c.whisker ? '#fff4ea' : INK}" stroke-width="1.15" stroke-linecap="round"/>`);
  p.push(mirror(`<path d="M24 45 L11 43 M24 47 L11.5 48.5" stroke="${c.whisker ?? 'rgba(42,33,30,0.45)'}" stroke-width="0.9" stroke-linecap="round"/>`));
  return `<svg viewBox="0 0 64 64" aria-hidden="true">${p.join('')}</svg>`;
}
