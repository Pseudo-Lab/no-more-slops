// 데이터 저장소. .env 에 Supabase 키가 있으면 Supabase, 없으면 이 브라우저(localStorage)에 저장한다.
import { createClient } from '@supabase/supabase-js';
import { createSessionGuard } from './session.js';

const URL = import.meta.env.VITE_SUPABASE_URL;
const KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;
const sb = URL && KEY ? createClient(URL, KEY) : null;
const sessionOwner = sb ? createSessionGuard(sb) : null;

export const isShared = !!sb;

function readLS(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
}
function writeLS(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch { return false; }
}

export function deviceId() {
  let id = readLS('kk_device', null);
  if (!id) { id = crypto.randomUUID(); writeLS('kk_device', id); }
  return id;
}

const myHearts = new Set(readLS('kk_hearts', []));
export const hasHearted = (postId) => myHearts.has(postId);

function blobToDataURL(blob) {
  return new Promise((res, rej) => {
    const r = new FileReader();
    r.onload = () => res(r.result);
    r.onerror = rej;
    r.readAsDataURL(blob);
  });
}

async function uploadPhoto(blob, folder) {
  if (!sb) return blobToDataURL(blob);
  await sessionOwner();
  const path = `${folder}/${crypto.randomUUID()}.jpg`;
  const { error } = await sb.storage.from('photos').upload(path, blob, { contentType: 'image/jpeg' });
  if (error) throw error;
  return sb.storage.from('photos').getPublicUrl(path).data.publicUrl;
}

// ---------- 읽기 ----------

// 장소 목록. 각 장소에 posts(최신순, dog 포함)를 붙여서 돌려준다.
export async function loadPlaces() {
  let places, posts, dogs;
  if (sb) {
    const [p, q, d] = await Promise.all([
      sb.from('places').select('*'),
      sb.from('posts').select('*').order('created_at', { ascending: false }),
      sb.from('dogs').select('*'),
    ]);
    for (const r of [p, q, d]) if (r.error) throw r.error;
    [places, posts, dogs] = [p.data, q.data, d.data];
  } else {
    ({ places, posts, dogs } = readLS('kk_db', { places: [], posts: [], dogs: [] }));
    posts = [...posts].sort((a, b) => b.created_at.localeCompare(a.created_at));
  }
  const dogById = Object.fromEntries(dogs.map((d) => [d.id, d]));
  const byPlace = Object.fromEntries(places.map((p) => [p.id, { ...p, posts: [] }]));
  for (const post of posts) {
    const place = byPlace[post.place_id];
    if (!place) continue;
    // 길고양이는 등록된 강아지가 없으니 카드에 쓸 정보를 만들어 붙인다
    const who = post.cat_type
      ? { name: post.cat_name || '길에서 만난 친구', breed: post.cat_type, isCat: true }
      : dogById[post.dog_id];
    if (who) place.posts.push({ ...post, dog: who });
  }
  return Object.values(byPlace).filter((p) => p.posts.length);
}

export async function loadMyDogs() {
  if (sb) {
    const owner = await sessionOwner();
    const { data, error } = await sb.from('dogs').select('*').eq('owner_id', owner).order('created_at');
    if (error) throw error;
    return data;
  }
  return readLS('kk_db', { dogs: [] }).dogs.filter((d) => d.device_id === deviceId());
}

// ---------- 쓰기 ----------

function localInsert(table, row) {
  const db = readLS('kk_db', { places: [], posts: [], dogs: [] });
  const full = { id: crypto.randomUUID(), created_at: new Date().toISOString(), ...row };
  db[table].push(full);
  if (!writeLS('kk_db', db)) throw new Error('브라우저 저장 공간이 가득 찼어요. Supabase를 연결하면 사진을 계속 올릴 수 있어요.');
  return full;
}

async function insert(table, row) {
  if (!sb) return localInsert(table, row);
  await sessionOwner();
  const { data, error } = await sb.from(table).insert(row).select().single();
  if (error) throw error;
  return data;
}

export async function addDog({ name, breed, age, intro, avatar }) {
  const owner_id = sb ? await sessionOwner() : null;
  const avatar_url = avatar ? await uploadPhoto(avatar, 'dogs') : null;
  return insert('dogs', { device_id: deviceId(), ...(sb ? { owner_id } : {}), name, breed, age, intro, avatar_url });
}

// 내 강아지 정보 수정. avatar 를 안 바꾸면 기존 사진 유지.
export async function updateDog(id, { name, breed, age, intro, avatar }) {
  if (sb) await sessionOwner();
  const avatar_url = avatar ? await uploadPhoto(avatar, 'dogs') : null;
  if (sb) {
    const { data, error } = await sb.rpc('update_dog', {
      p_id: id, p_name: name, p_breed: breed, p_age: age, p_intro: intro, p_avatar_url: avatar_url,
    });
    if (error) throw error;
    return data;
  }
  const db = readLS('kk_db', { dogs: [] });
  const dog = db.dogs.find((d) => d.id === id && d.device_id === deviceId());
  Object.assign(dog, { name, breed, age, intro }, avatar_url ? { avatar_url } : {});
  if (!writeLS('kk_db', db)) throw new Error('브라우저 저장 공간이 가득 찼어요.');
  return dog;
}

// place: 기존 장소면 { id }, 새 장소면 { name, lat, lng }
// 강아지면 dogId, 길고양이면 cat: { type, name }
export async function addPost({ place, dogId = null, cat = null, photo, caption, takenAt }) {
  if (sb) {
    const owner = await sessionOwner();
    if (dogId) {
      const { data, error } = await sb.from('dogs').select('id').eq('id', dogId).eq('owner_id', owner).maybeSingle();
      if (error) throw error;
      if (!data) throw new Error('내 강아지로만 사진을 올릴 수 있어요.');
    }
  }
  const placeId = place.id ?? (await insert('places', { name: place.name, lat: place.lat, lng: place.lng })).id;
  const photo_url = await uploadPhoto(photo, 'posts');
  return insert('posts', {
    place_id: placeId, dog_id: dogId, cat_type: cat?.type ?? null, cat_name: cat?.name || null, photo_url, caption,
    taken_at: takenAt ? takenAt.toISOString() : null, heart_count: 0,
  });
}

export async function toggleHeart(postId) {
  let count;
  if (sb) {
    await sessionOwner();
    const { data, error } = await sb.rpc('toggle_heart', { p_post: postId, p_device: deviceId() });
    if (error) throw error;
    count = data;
  } else {
    const db = readLS('kk_db', { posts: [] });
    const post = db.posts.find((p) => p.id === postId);
    post.heart_count += myHearts.has(postId) ? -1 : 1;
    writeLS('kk_db', db);
    count = post.heart_count;
  }
  myHearts.has(postId) ? myHearts.delete(postId) : myHearts.add(postId);
  writeLS('kk_hearts', [...myHearts]);
  return count;
}
