import './style.css';
import * as store from './store.js';
import { readPhotoMeta, shrinkImage, distance } from './image.js';
import { BREEDS, CATS, breedOf, dogFace } from './breeds.js';
import { loadKakao, KakaoMap } from './map.js';
import { hasBadWords, blurFaces, warmUpFaceDetector } from './moderation.js';

const BAD_WORDS_MSG = '욕설이나 비하 표현은 올릴 수 없어요. 고운 말로 적어주세요.';
const FACE_MSG = '사람 얼굴은 자동으로 가렸어요. 미리보기를 확인해 주세요.';

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const HEART = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8.2 3 4.5 6.7 4.5c2.1 0 3.6 1.2 5.3 3 1.7-1.8 3.2-3 5.3-3 3.7 0 5.8 3.7 4.3 7.2C19.5 16.4 12 21 12 21z"/></svg>';
const PAW = '<svg viewBox="0 0 64 64" aria-hidden="true"><ellipse cx="32" cy="42" rx="14" ry="12"/><ellipse cx="14" cy="26" rx="6" ry="8"/><ellipse cx="50" cy="26" rx="6" ry="8"/><ellipse cx="24" cy="12" rx="6" ry="8"/><ellipse cx="40" cy="12" rx="6" ry="8"/></svg>';

// ---------- 지도 ----------
let map = null; // start() 에서 카카오맵이 준비되면 채워진다
const PHOTO_LEVEL = 5; // 카카오 줌 레벨이 이 값 이하(가까움)면 사진 핀, 크면 견종별 묶음

const showDraftMarker = (loc) => map?.showDraft(loc);
const clearDraftMarker = () => map?.clearDraft();

// 패널에 가리지 않게: 데스크톱은 왼쪽, 모바일은 위쪽으로 살짝 옮겨서 보여준다
function focusOn(lat, lng, level = map.level) {
  map.setView({ lat, lng }, level);
  if (innerWidth >= 768) map.panBy(210, 0); else map.panBy(0, innerHeight * 0.3);
}

function markerEl(html, onClick) {
  const el = document.createElement('div');
  el.className = 'pin';
  el.innerHTML = html;
  el.addEventListener('click', onClick);
  return el;
}
let places = [];
let myDogs = [];

function photoHtml(place) {
  const count = place.posts.length;
  return `<div class="pin-photo" style="background-image:url('${esc(place.posts[0].photo_url)}')"></div>
    ${count > 1 ? `<span class="pin-count">${count}</span>` : ''}`;
}

// 화면에서 130px 안에 있는 장소끼리 묶고, 묶음 안의 사진을 견종별로 센다
function clusters() {
  const groups = [];
  for (const place of places) {
    const p = map.point(place);
    const pt = { x: p.x, y: p.y };
    const near = groups.find((g) => Math.hypot(g.pt.x - pt.x, g.pt.y - pt.y) < 130);
    if (near) {
      const n = near.places.push(place);
      near.pt = { x: (near.pt.x * (n - 1) + pt.x) / n, y: (near.pt.y * (n - 1) + pt.y) / n };
    } else groups.push({ pt, places: [place] });
  }
  return groups.map(({ places: group }) => {
    const counts = new Map();
    for (const place of group) for (const post of place.posts) {
      const name = breedOf(post.dog.breed).name;
      counts.set(name, (counts.get(name) ?? 0) + 1);
    }
    return {
      group,
      lat: group.reduce((s, p) => s + p.lat, 0) / group.length,
      lng: group.reduce((s, p) => s + p.lng, 0) / group.length,
      breeds: [...counts].sort((a, b) => b[1] - a[1]),
    };
  });
}

function clusterHtml({ breeds }) {
  const shown = breeds.slice(0, 3);
  const rest = breeds.slice(3).reduce((sum, [, n]) => sum + n, 0);
  return `<div class="cluster">
    ${shown.map(([name, n]) => `<span class="cluster-dog" style="background:${breedOf(name).bg}" title="${esc(name)} ${n}장">
      ${dogFace(name)}${n > 1 ? `<b>${n}</b>` : ''}</span>`).join('')}
    ${rest ? `<span class="cluster-more">+${rest}</span>` : ''}
  </div>`;
}

function renderMarkers() {
  if (!map) return;
  if (map.level <= PHOTO_LEVEL) {
    map.setMarkers(places.map((place) => ({
      lat: place.lat, lng: place.lng, el: markerEl(photoHtml(place), () => openPlace(place.id)),
    })));
    return;
  }
  map.setMarkers(clusters().map((c) => ({
    lat: c.lat, lng: c.lng,
    el: markerEl(clusterHtml(c), () => {
      if (c.group.length === 1) return openPlace(c.group[0].id, PHOTO_LEVEL);
      map.fitBounds(c.group, 3);
    }),
  })));
}

async function refresh() {
  try {
    [places, myDogs] = await Promise.all([store.loadPlaces(), store.loadMyDogs()]);
  } catch (e) {
    toast('지도를 불러오지 못했어요. 잠시 후 새로고침해 주세요.');
    console.error(e);
  }
  renderMarkers();
  $('#myDogsBtn').innerHTML = myDogs.length
    ? `${avatar(myDogs[0], 'sm')}<span>${esc(myDogs[0].name)}${myDogs.length > 1 ? ` 외 ${myDogs.length - 1}` : ''}</span>`
    : '내 강아지 등록';
}

// ---------- 시트(패널) ----------
const sheet = $('#sheet');
const sheetBody = $('#sheetBody');
function openSheet(html) {
  clearDraftMarker();
  sheetBody.innerHTML = html;
  sheet.hidden = false;
  document.body.classList.add('sheet-open');
  sheet.scrollTop = 0;
}
function closeSheet() {
  clearDraftMarker();
  sheet.hidden = true;
  document.body.classList.remove('sheet-open');
  sheetBody.innerHTML = '';
}
$('#sheetClose').addEventListener('click', closeSheet);

function toast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => (t.hidden = true), 2600);
}

function avatar(dog, size = '') {
  return dog.avatar_url
    ? `<span class="avatar ${size}" style="background-image:url('${esc(dog.avatar_url)}')"></span>`
    : `<span class="avatar ${size} char" style="background:${breedOf(dog.breed).bg}">${dogFace(dog.breed)}</span>`;
}

const fmtDate = (iso) => {
  const d = new Date(iso);
  return `${d.getFullYear()}. ${d.getMonth() + 1}. ${d.getDate()}`;
};

// ---------- 장소 상세 ----------
function openPlace(placeId, level) {
  const place = places.find((p) => p.id === placeId);
  if (!place) return;
  focusOn(place.lat, place.lng, level);
  const dogs = new Set(place.posts.map((p) => p.dog_id ?? `cat:${p.id}`)).size;
  openSheet(`
    <p class="eyebrow">친구 ${dogs}명의 꼬순내가 남아 있어요</p>
    <h2 class="sheet-title">${esc(place.name)}</h2>
    <button class="btn primary wide" type="button" data-been="${place.id}">
      ${PAW} 우리도 꼬순내 남기기
    </button>
    <ul class="feed">
      ${place.posts.map((post) => `
        <li class="card">
          <img class="card-photo" src="${esc(post.photo_url)}" alt="${esc(post.dog.name)} 사진" loading="lazy" />
          <div class="card-body">
            <div class="dog-line">
              ${avatar(post.dog, 'sm')}
              <div class="dog-text">
                <strong>${esc(post.dog.name)}</strong>
                <span class="muted">${post.dog.isCat ? `길에서 만난 친구 · ${esc(post.dog.breed)}` : [post.dog.breed, post.dog.age].filter(Boolean).map(esc).join(' · ')}</span>
              </div>
              <button class="heart ${store.hasHearted(post.id) ? 'on' : ''}" type="button" data-heart="${post.id}" aria-pressed="${store.hasHearted(post.id)}" aria-label="하트">
                ${HEART}<span>${post.heart_count}</span>
              </button>
            </div>
            ${post.caption ? `<p class="caption">${esc(post.caption)}</p>` : ''}
            ${post.dog.intro ? `<p class="intro">“${esc(post.dog.intro)}”</p>` : ''}
            <p class="date">${fmtDate(post.taken_at ?? post.created_at)}</p>
          </div>
        </li>`).join('')}
    </ul>
  `);
}

sheetBody.addEventListener('click', async (e) => {
  const heartBtn = e.target.closest('[data-heart]');
  if (heartBtn) {
    const id = heartBtn.dataset.heart;
    heartBtn.disabled = true;
    try {
      const n = await store.toggleHeart(id);
      const on = store.hasHearted(id);
      heartBtn.classList.toggle('on', on);
      heartBtn.setAttribute('aria-pressed', on);
      heartBtn.querySelector('span').textContent = n;
      for (const p of places) for (const post of p.posts) if (post.id === id) post.heart_count = n;
    } catch (err) {
      toast('하트를 누르지 못했어요. 다시 시도해 주세요.');
      console.error(err);
    }
    heartBtn.disabled = false;
    return;
  }
  const been = e.target.closest('[data-been]');
  if (been) startUpload({ placeId: been.dataset.been });
});

// ---------- 강아지 등록 / 수정 ----------
// dog 를 넘기면 수정, 없으면 새로 등록
function openDogForm({ dog = null, after = null } = {}) {
  const preset = dog && BREEDS.some((b) => b.name === dog.breed) ? dog.breed : null;
  const custom = dog && !preset ? dog.breed ?? '' : '';
  let breed = preset ?? (dog ? '기타' : null);
  openSheet(`
    <p class="eyebrow">${dog ? '내 강아지 수정' : myDogs.length ? '새 친구' : '처음 오셨네요'}</p>
    <h2 class="sheet-title">${dog ? `${esc(dog.name)} 정보 고치기` : '우리 강아지를 소개해 주세요'}</h2>
    <form id="dogForm" class="form">
      <label class="avatar-pick">
        <input id="dogAvatar" type="file" accept="image/*" hidden />
        <span id="dogAvatarPreview">${dog ? avatar(dog, 'lg') : `<span class="avatar lg empty">${PAW}</span>`}</span>
        <span class="muted">${dog?.avatar_url ? '프로필 사진 바꾸기' : '프로필 사진 (선택)'}</span>
      </label>
      <label>이름<input id="dogName" required maxlength="20" placeholder="예: 콩이" value="${esc(dog?.name)}" /></label>
      <fieldset class="breed-pick">
        <legend>견종</legend>
        <div class="breed-grid">
          ${[...BREEDS, { name: '기타' }].map((b) => `
            <label class="breed-opt">
              <input type="radio" name="breed" value="${esc(b.name)}" ${breed === b.name ? 'checked' : ''} />
              <span class="breed-face" style="background:${breedOf(b.name).bg}">${dogFace(b.name)}</span>
              <span class="breed-name">${b.name === '기타' ? '기타·믹스' : esc(b.name)}</span>
            </label>`).join('')}
        </div>
        <input id="dogBreedCustom" maxlength="20" placeholder="견종을 적어주세요 (예: 믹스, 스피츠)" value="${esc(custom)}" ${breed === '기타' ? '' : 'hidden'} />
      </fieldset>
      <label>나이<input id="dogAge" maxlength="10" placeholder="예: 3살" value="${esc(dog?.age)}" /></label>
      <label>한 줄 소개<input id="dogIntro" maxlength="60" placeholder="예: 공만 보면 세상 다 가진 표정" value="${esc(dog?.intro)}" /></label>
      <button class="btn primary wide" type="submit">${dog ? '저장하기' : '등록하기'}</button>
      ${myDogs.length ? '' : '<p class="muted small">등록한 강아지는 이 브라우저에 기억돼요.</p>'}
    </form>
  `);
  let avatarBlob = null;
  $('#dogForm').addEventListener('change', (e) => {
    if (e.target.name !== 'breed') return;
    breed = e.target.value;
    $('#dogBreedCustom').hidden = breed !== '기타';
    if (breed === '기타') $('#dogBreedCustom').focus();
    if (!avatarBlob && !dog?.avatar_url) {
      $('#dogAvatarPreview').innerHTML = avatar({ breed: breed === '기타' ? null : breed }, 'lg');
    }
  });
  $('#dogAvatar').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const { blob, faces } = await blurFaces(await shrinkImage(file, 400));
      if (faces) toast(FACE_MSG);
      avatarBlob = blob;
      $('#dogAvatarPreview').innerHTML = `<span class="avatar lg" style="background-image:url(${URL.createObjectURL(avatarBlob)})"></span>`;
    } catch (err) { toast(err.message); }
  });
  $('#dogForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!breed) return toast('견종을 골라주세요. 목록에 없으면 기타를 눌러주세요.');
    if (hasBadWords($('#dogName').value, $('#dogBreedCustom').value, $('#dogAge').value, $('#dogIntro').value)) return toast(BAD_WORDS_MSG);
    const btn = e.target.querySelector('button[type=submit]');
    const label = btn.textContent;
    btn.disabled = true;
    btn.textContent = '저장하는 중…';
    const fields = {
      name: $('#dogName').value.trim(),
      breed: breed === '기타' ? $('#dogBreedCustom').value.trim() || '믹스' : breed,
      age: $('#dogAge').value.trim(),
      intro: $('#dogIntro').value.trim(),
      avatar: avatarBlob,
    };
    try {
      dog ? await store.updateDog(dog.id, fields) : await store.addDog(fields);
      await refresh();
      toast(dog ? '저장했어요!' : `${fields.name} 등록 완료!`);
      after ? after() : openMyDogs();
    } catch (err) {
      toast(err.message || '저장하지 못했어요. 다시 시도해 주세요.');
      console.error(err);
      btn.disabled = false;
      btn.textContent = label;
    }
  });
}

function openMyDogs() {
  if (!myDogs.length) return openDogForm();
  openSheet(`
    <p class="eyebrow">내 강아지</p>
    <h2 class="sheet-title">우리 집 강아지들</h2>
    <ul class="dog-list">
      ${myDogs.map((d) => {
        const n = places.reduce((sum, p) => sum + p.posts.filter((post) => post.dog_id === d.id).length, 0);
        return `<li class="dog-line">${avatar(d)}<div class="dog-text"><strong>${esc(d.name)}</strong>
          <span class="muted">${[d.breed, d.age].filter(Boolean).map(esc).join(' · ')}</span>
          ${d.intro ? `<span class="intro">“${esc(d.intro)}”</span>` : ''}
          <span class="muted small">사진 ${n}장</span></div>
          <button class="btn small-btn" type="button" data-edit="${d.id}">수정</button></li>`;
      }).join('')}
    </ul>
    <button class="btn wide" type="button" id="addAnotherDog">+ 친구 한 명 더 등록</button>
  `);
  $('#addAnotherDog').addEventListener('click', () => openDogForm());
  $('.dog-list').addEventListener('click', (e) => {
    const id = e.target.closest('[data-edit]')?.dataset.edit;
    if (id) openDogForm({ dog: myDogs.find((d) => d.id === id) });
  });
}
$('#myDogsBtn').addEventListener('click', openMyDogs);

// ---------- 사진 올리기 ----------
let picking = null; // 지도에서 위치 고르는 중일 때의 콜백

function onMapClick(loc) {
  if (!picking) return;
  const cb = picking;
  stopPicking();
  cb(loc);
}
function startPicking(cb) {
  picking = cb;
  sheet.hidden = true;
  $('#pickBanner').hidden = false;
  document.body.classList.add('picking');
}
function stopPicking() {
  picking = null;
  $('#pickBanner').hidden = true;
  document.body.classList.remove('picking');
}
$('#pickCancel').addEventListener('click', () => { stopPicking(); sheet.hidden = false; });

// 길고양이 보호: 실제 위치에서 80~130m 떨어진 임의의 지점으로 옮긴다
function blurLocation({ lat, lng }) {
  const angle = Math.random() * Math.PI * 2;
  const meters = 80 + Math.random() * 50;
  return {
    lat: lat + (Math.cos(angle) * meters) / 111320,
    lng: lng + (Math.sin(angle) * meters) / (111320 * Math.cos((lat * Math.PI) / 180)),
  };
}

function startUpload({ placeId } = {}) {
  warmUpFaceDetector();
  const fixedPlace = placeId ? places.find((p) => p.id === placeId) : null;
  // mode: 'dog'(기본, 내가 다녀온 기록) | 'cat'(길에서 만난 친구)
  const state = { placeName: '', photo: null, takenAt: null, loc: fixedPlace ? { lat: fixedPlace.lat, lng: fixedPlace.lng } : null, placeId: fixedPlace?.id ?? null, mode: 'dog', dogId: myDogs[0]?.id ?? null, catType: null };

  openSheet(`
    <p class="eyebrow">${fixedPlace ? esc(fixedPlace.name) : '새 꼬순내'}</p>
    <h2 class="sheet-title">${fixedPlace ? '우리도 다녀왔어요' : '어디 다녀왔어요?'}</h2>
    <form id="postForm" class="form">
      <div class="seg" role="radiogroup" aria-label="누구와의 기록인가요">
        <label><input type="radio" name="mode" value="dog" checked /><span>${PAW} 우리 강아지랑 다녀왔어요</span></label>
        <label><input type="radio" name="mode" value="cat" /><span>길에서 친구를 만났어요</span></label>
      </div>
      <div id="dogBox">
        ${myDogs.length ? `<fieldset class="dog-choose">
          <legend>누구랑 갔어요?</legend>
          ${myDogs.map((d) => `<label class="dog-opt"><input type="radio" name="dog" value="${d.id}" ${state.dogId === d.id ? 'checked' : ''} />${avatar(d, 'sm')}${esc(d.name)}</label>`).join('')}
        </fieldset>` : `<div class="empty-dog"><p class="muted">아직 등록한 강아지가 없어요. 먼저 소개해 주세요.</p>
          <button class="btn" type="button" id="registerDog">+ 우리 강아지 등록하기</button></div>`}
      </div>
      <div id="catBox" class="cat-box" hidden>
        <p class="muted small">무늬를 골라주세요</p>
        <div class="breed-grid cat-grid">
          ${CATS.map((c) => `<label class="breed-opt"><input type="radio" name="catType" value="${c.name}" />
            <span class="breed-face" style="background:${c.bg}">${dogFace(c.name)}</span><span class="breed-name">${c.name}</span></label>`).join('')}
        </div>
        <label>동네에서 부르는 이름 (선택)<input id="catName" maxlength="20" placeholder="예: 나비" /></label>
        <p class="cat-note">길고양이 보호를 위해 새로 만드는 장소는 실제 위치에서 100m 정도 떨어진 곳에 표시돼요. 장소 이름도 "망원동 골목"처럼 동네 정도로만 적어주세요.</p>
      </div>
      <label class="photo-pick" id="photoPick">
        <input id="postPhoto" type="file" accept="image/*" hidden />
        <span class="photo-empty">${PAW}<span>사진 고르기</span></span>
      </label>
      <div id="locBox" class="loc-box" ${fixedPlace ? 'hidden' : ''}></div>
      <label>한마디<input id="postCaption" maxlength="80" placeholder="예: 여기 풀 냄새 최고였음" /></label>
      <button class="btn primary wide" type="submit" id="postSubmit">꼬순내 남기기</button>
    </form>
  `);

  const renderLoc = () => {
    const box = $('#locBox');
    if (!box || fixedPlace) return;
    if (state.loc) showDraftMarker(state.loc);
    if (!state.loc) {
      box.innerHTML = `<p class="muted">${state.photo ? '사진에 위치 정보가 없어요. 장소를 검색하거나 지도에서 골라주세요.' : '사진을 고르면 찍은 위치를 자동으로 찾아볼게요.'}</p>
        <div class="search-row"><input id="placeSearch" type="search" placeholder="장소 검색 (예: 서울숲)" /><button class="btn" type="button" data-search>검색</button></div>
        <ul id="searchResults" class="search-results"></ul>
        <button class="btn" type="button" data-pick>지도에서 직접 고르기</button>`;
      return;
    }
    const near = places
      .map((p) => ({ p, d: distance(state.loc, p) }))
      .filter((x) => x.d < 150)
      .sort((a, b) => a.d - b.d)
      .slice(0, 3);
    box.innerHTML = `
      <p class="loc-ok">${PAW} 위치를 정했어요 <button class="link-btn" type="button" data-pick>다시 고르기</button></p>
      ${near.length ? `<p class="muted small">근처에 이미 있는 장소예요. 같은 곳이면 골라주세요.</p>
        <div class="place-opts">${near.map(({ p }) => `<label class="place-opt"><input type="radio" name="place" value="${p.id}" ${state.placeId === p.id ? 'checked' : ''} />${esc(p.name)}</label>`).join('')}
        <label class="place-opt"><input type="radio" name="place" value="" ${state.placeId ? '' : 'checked'} />새 장소</label></div>` : ''}
      <label ${state.placeId ? 'hidden' : ''} id="placeNameLabel">장소 이름<input id="placeName" maxlength="40" placeholder="예: 서울숲 반려견 놀이터" value="${esc(state.placeName)}" /></label>
    `;
  };
  renderLoc();

  const runSearch = async () => {
    const q = $('#placeSearch')?.value.trim();
    if (!q) return;
    const results = await map.search(q);
    $('#searchResults').innerHTML = results.length
      ? results.map((r, i) => `<li><button type="button" data-result="${i}"><strong>${esc(r.name)}</strong><span class="muted small">${esc(r.address)}</span></button></li>`).join('')
      : '<li class="muted small">검색 결과가 없어요. 지도에서 직접 골라주세요.</li>';
    $('#searchResults').results = results;
  };
  $('#locBox').addEventListener('keydown', (e) => {
    if (e.target.id === 'placeSearch' && e.key === 'Enter') { e.preventDefault(); runSearch(); }
  });
  $('#locBox').addEventListener('click', (e) => {
    if (e.target.closest('[data-search]')) return runSearch();
    const pickedResult = e.target.closest('[data-result]');
    if (pickedResult) {
      const r = $('#searchResults').results[pickedResult.dataset.result];
      state.loc = { lat: r.lat, lng: r.lng };
      state.placeId = null;
      state.placeName = r.name;
      focusOn(r.lat, r.lng, 3);
      return renderLoc();
    }
    if (!e.target.closest('[data-pick]')) return;
    startPicking((loc) => {
      state.loc = loc;
      state.placeId = null;
      sheet.hidden = false;
      renderLoc();
    });
  });
  $('#locBox').addEventListener('change', (e) => {
    if (e.target.name !== 'place') return;
    state.placeId = e.target.value || null;
    $('#placeNameLabel').hidden = !!state.placeId;
  });
  $('#postForm').addEventListener('change', (e) => {
    if (e.target.name === 'mode') {
      state.mode = e.target.value;
      $('#catBox').hidden = state.mode !== 'cat';
      $('#dogBox').hidden = state.mode !== 'dog';
    }
    if (e.target.name === 'dog') state.dogId = e.target.value;
    if (e.target.name === 'catType') state.catType = e.target.value;
  });
  $('#registerDog')?.addEventListener('click', () => openDogForm({ after: () => startUpload({ placeId }) }));

  $('#postPhoto').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const pick = $('#photoPick');
    pick.classList.add('loading');
    try {
      const [meta, shrunk] = await Promise.all([readPhotoMeta(file), shrinkImage(file)]);
      const { blob, faces } = await blurFaces(shrunk);
      if (faces) toast(FACE_MSG);
      state.photo = blob;
      state.takenAt = meta.takenAt;
      pick.style.backgroundImage = `url(${URL.createObjectURL(blob)})`;
      pick.classList.add('has-photo');
      if (!fixedPlace && meta.lat != null) {
        state.loc = { lat: meta.lat, lng: meta.lng };
        state.placeId = null;
        focusOn(meta.lat, meta.lng, 3);
        toast('사진 속 위치를 찾았어요!');
      }
      renderLoc();
    } catch (err) {
      toast(err.message);
    }
    pick.classList.remove('loading');
  });

  $('#postForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!state.photo) return toast('사진을 먼저 골라주세요.');
    if (!state.loc) return toast('위치를 골라주세요.');
    const name = $('#placeName')?.value.trim();
    if (!state.placeId && !name) return toast('장소 이름을 적어주세요.');
    if (hasBadWords(name, $('#postCaption').value, $('#catName').value)) return toast(BAD_WORDS_MSG);
    const isCatPost = state.mode === 'cat';
    if (isCatPost && !state.catType) return toast('고양이 무늬를 골라주세요.');
    if (!isCatPost && !state.dogId) return toast('우리 강아지를 먼저 등록해 주세요.');
    const btn = $('#postSubmit');
    btn.disabled = true;
    btn.textContent = '올리는 중…';
    try {
      const post = await store.addPost({
        place: state.placeId ? { id: state.placeId } : { name, ...(isCatPost ? blurLocation(state.loc) : state.loc) },
        dogId: isCatPost ? null : state.dogId,
        cat: isCatPost ? { type: state.catType, name: $('#catName').value.trim() } : null,
        photo: state.photo,
        caption: $('#postCaption').value.trim(),
        takenAt: state.takenAt,
      });
      await refresh();
      toast('꼬순내를 남겼어요!');
      openPlace(post.place_id);
    } catch (err) {
      toast(err.message || '올리지 못했어요. 다시 시도해 주세요.');
      console.error(err);
      btn.disabled = false;
      btn.textContent = '꼬순내 남기기';
    }
  });
}
$('#addBtn').addEventListener('click', () => startUpload());

document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (picking) { stopPicking(); sheet.hidden = false; } else closeSheet();
});

// ---------- 사진 보호: 우클릭 저장·길게 눌러 저장·끌어서 저장 막기 ----------
const PROTECTED = 'img, .pin-photo, .avatar, .photo-pick, .card-photo';
document.addEventListener('contextmenu', (e) => { if (e.target.closest(PROTECTED)) e.preventDefault(); });
document.addEventListener('dragstart', (e) => { if (e.target.closest(PROTECTED)) e.preventDefault(); });

// ---------- 처음 들어왔을 때 인사 ----------
const APP_NAME = document.title;
function openWelcome() {
  openSheet(`
    <div class="welcome">
      <span class="welcome-faces">${['말티즈', '시바견', '웰시코기'].map((n) => `<span class="breed-face" style="background:${breedOf(n).bg}">${dogFace(n)}</span>`).join('')}</span>
      <h2 class="sheet-title">안녕하세요!<br />내 강아지와의 추억을 남기는 ${esc(APP_NAME)}입니다.</h2>
      <p>강아지가 아니어도 괜찮아요! 길에서 마주친 예쁜 동물들도 함께 남겨주세요 💓</p>
      <button class="btn primary wide" type="button" id="welcomeStart">${PAW} 첫 꼬순내 남기기</button>
      <button class="btn wide" type="button" id="welcomeLook">먼저 구경할래요</button>
    </div>
  `);
  $('#welcomeStart').addEventListener('click', () => startUpload());
  $('#welcomeLook').addEventListener('click', closeSheet);
}
let welcomed = false;
try { welcomed = localStorage.getItem('kk_welcomed') === '1'; localStorage.setItem('kk_welcomed', '1'); } catch {}
if (!welcomed) openWelcome();

async function start() {
  try {
    const kakao = await loadKakao();
    map = new KakaoMap(kakao, $('#map'), { lat: 37.5446, lng: 127.0379, level: 7 }); // 서울숲 근처
    map.onZoom(renderMarkers);
    map.onClick(onMapClick);
  } catch (err) {
    toast(err.message);
    console.error(err);
    return;
  }
  await refresh();
  if (places.length) map.fitBounds(places, 3);
  renderMarkers();
}
start().then(() => {
  if (!store.isShared) console.info('[Pawstamp] Supabase 미연결: 이 브라우저에만 저장됩니다.');
});
