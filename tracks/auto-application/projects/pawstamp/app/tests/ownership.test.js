import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { PGlite } from '@electric-sql/pglite';

// Isolated PostgreSQL engine; auth.uid() and storage tables stand in for Supabase.
// No production credentials, API, or database are used.
const ownerA = '10000000-0000-0000-0000-000000000001';
const ownerB = '10000000-0000-0000-0000-000000000002';
const legacyDog = '20000000-0000-0000-0000-000000000001';
const newDog = '20000000-0000-0000-0000-000000000002';
const place = '30000000-0000-0000-0000-000000000001';

test('migration and policies enforce session ownership, including direct API bypasses', async (t) => {
  const db = new PGlite();
  t.after(() => db.close());
  await db.exec(`
    create role anon;
    create role authenticated;
    create schema auth;
    create table auth.users (id uuid primary key);
    insert into auth.users values ('${ownerA}'), ('${ownerB}');
    create function auth.uid() returns uuid language sql stable as $$
      select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
    $$;
    grant usage on schema auth to anon, authenticated;
    create schema storage;
    create table storage.buckets (id text primary key, name text, public boolean);
    create table storage.objects (id uuid primary key default gen_random_uuid(), bucket_id text);
    alter table storage.objects enable row level security;
    grant usage on schema storage to anon, authenticated;
    grant select, insert on storage.objects to anon, authenticated;
    create table dogs (
      id uuid primary key default gen_random_uuid(), device_id text not null,
      name text not null, breed text, age text, intro text, avatar_url text,
      created_at timestamptz not null default now()
    );
    insert into dogs (id, device_id, name) values ('${legacyDog}', 'public-legacy-device', 'Legacy');
    create function update_dog(uuid, text, text, text, text, text, text)
      returns dogs language sql as $$ select * from dogs where id = $1 $$;
  `);
  const schema = await readFile(new URL('../supabase/schema.sql', import.meta.url), 'utf8');
  await db.exec(schema);
  await db.exec(schema); // Existing installations can reapply the same schema.
  await db.exec('grant select, insert, update, delete on dogs, places, posts, hearts to anon, authenticated');

  await t.test('legacy ownership stays unset and the insecure old RPC is removed', async () => {
    const { rows } = await db.query('select owner_id from dogs where id = $1', [legacyDog]);
    assert.equal(rows[0].owner_id, null);
    const old = await db.query("select to_regprocedure('update_dog(uuid,text,text,text,text,text,text)') as rpc");
    assert.equal(old.rows[0].rpc, null);
  });

  async function actAs(role, uid = '') {
    await db.exec('reset role');
    await db.query("select set_config('request.jwt.claim.sub', $1, false)", [uid]);
    await db.exec(`set role ${role}`);
  }
  const editDog = (id, name) => db.query(
    "select (update_dog($1, $2, 'breed', '2', 'intro', null)).name as name", [id, name]);
  const post = (dog, cat = null, hearts = 0) => db.query(
    'insert into posts (place_id, dog_id, photo_url, cat_type, heart_count) values ($1,$2,$3,$4,$5)',
    [place, dog, 'https://example.com/photo.jpg', cat, hearts]);

  await t.test('anonymous API role cannot create dogs, invoke edits, or upload', async () => {
    await actAs('anon');
    await assert.rejects(db.query('insert into dogs (device_id,name,owner_id) values ($1,$2,$3)', ['fake', 'Fake', ownerA]), /row-level security/);
    await assert.rejects(editDog(legacyDog, 'Stolen'), /permission denied/);
    await assert.rejects(db.exec("insert into storage.objects (bucket_id) values ('photos')"), /row-level security/);
  });

  await t.test('new dogs bind to the session, and ownerless legacy dogs cannot be claimed', async () => {
    await actAs('authenticated', ownerA);
    await db.query('insert into dogs (id,device_id,name,owner_id) values ($1,$2,$3,$4)', [newDog, 'a-device', 'Mine', ownerA]);
    await assert.rejects(db.query('insert into dogs (device_id,name,owner_id) values ($1,$2,$3)', ['fake', 'Fake', ownerB]), /row-level security/);
    await assert.rejects(db.exec("insert into dogs (device_id,name) values ('fake','No owner')"), /row-level security/);
    await assert.rejects(editDog(legacyDog, 'Claimed'), /내 강아지/);
    assert.equal((await editDog(newDog, 'Updated')).rows[0].name, 'Updated');
    await db.query('insert into places (id,name,lat,lng) values ($1,$2,$3,$4)', [place, 'Park', 37.5, 127]);
    await db.exec("insert into storage.objects (bucket_id) values ('photos')");
  });

  await t.test('other users cannot edit a dog or post as it, even by adding cat_type', async () => {
    await actAs('authenticated', ownerB);
    await assert.rejects(editDog(newDog, 'Stolen'), /내 강아지/);
    await assert.rejects(post(newDog), /row-level security/);
    await assert.rejects(post(newDog, 'tabby'), /row-level security/);
    await assert.rejects(post(legacyDog), /row-level security/);
    await post(null, 'tabby');
  });

  await t.test('own-dog posts work while forged heart counts and missing sessions fail', async () => {
    await actAs('authenticated', ownerA);
    await post(newDog);
    await assert.rejects(post(newDog, null, 100), /row-level security/);
    await actAs('authenticated');
    await assert.rejects(editDog(newDog, 'No session'), /저장 세션/);
    await assert.rejects(post(null, 'tabby'), /row-level security/);
    await assert.rejects(db.exec("insert into storage.objects (bucket_id) values ('photos')"), /row-level security/);
  });
});
