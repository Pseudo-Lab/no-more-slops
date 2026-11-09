-- service-mcp 템플릿: 개인 키로 부르는 AI 함수 + 일회용 파일 업로드.
-- 예시 도메인은 entries(사용자의 기록 한 줄 + 선택 파일). 자기 서비스의 테이블·규칙으로 바꾼다.
-- 전제: pgcrypto(extensions 스키마), Storage 버킷 하나(예: 'files', 비공개, 용량·형식 제한).

create table entries (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid() references auth.users on delete cascade,
  title text not null check (char_length(title) between 1 and 60),
  body text check (char_length(body) <= 1000),
  file_path text,
  created_at timestamptz not null default now()
);
alter table entries enable row level security;
create policy "my entries" on entries for all using (owner_id = auth.uid()) with check (owner_id = auth.uid());

-- 1) 개인 키: 원문은 만들 때 한 번만 돌려주고 해시만 둔다. 사용자 1명에 키 1개, 다시 만들면 이전 키는 끊긴다.
create table ai_keys (
  owner_id uuid primary key references auth.users on delete cascade,
  key_hash text not null unique,
  created_at timestamptz not null default now()
);
alter table ai_keys enable row level security;
create policy "my ai key" on ai_keys for select using (owner_id = auth.uid());
create policy "drop my ai key" on ai_keys for delete using (owner_id = auth.uid());

create function issue_ai_key() returns text
language plpgsql security definer set search_path = public, extensions as $$
-- Constraint: 추측할 수 없어야 한다. 24바이트(192비트) 난수. 접두사는 서비스 이름으로.
declare k text := 'svc_' || encode(gen_random_bytes(24), 'hex');
begin
  if auth.uid() is null then raise exception 'no session'; end if;
  insert into ai_keys (owner_id, key_hash) values (auth.uid(), encode(digest(k, 'sha256'), 'hex'))
    on conflict (owner_id) do update set key_hash = excluded.key_hash, created_at = now();
  return k;
end $$;

-- 2) 키 → 주인. 아래 ai_* 함수 안에서만 쓴다(직접 부르지 못하게 revoke).
create function ai_member(k text) returns uuid
language plpgsql stable security definer set search_path = public, extensions as $$
declare m uuid;
begin
  select owner_id into m from ai_keys where key_hash = encode(digest(coalesce(k, ''), 'sha256'), 'hex');
  if m is null then raise exception 'invalid_key'; end if;
  return m;
end $$;

-- MCP 서버가 매 요청 처음에 부른다. 틀린 키면 예외 → 401.
create function ai_whoami(k text) returns text
language sql stable security definer set search_path = public as $$
  select coalesce(raw_user_meta_data->>'name', 'user') from auth.users where id = ai_member(k);
$$;

-- 3) 도구 = 함수 하나. 첫 줄에서 주인을 정하고 그 주인 것만. 앱의 RLS와 같은 규칙을 여기 다시 적는다.
create function ai_list_entries(k text) returns setof entries
language plpgsql stable security definer set search_path = public as $$
declare m uuid := ai_member(k);
begin
  return query select * from entries e where e.owner_id = m order by e.created_at desc;
end $$;

-- History: returns table(title text, …)처럼 열 이름이 인자와 같으면 "parameter name used more than once". 행 타입으로 돌려준다.
create function ai_add_entry(k text, title text, body text default null, file_path text default null) returns entries
language plpgsql security definer set search_path = public as $$
declare m uuid := ai_member(k); r entries;
begin
  if file_path is not null then
    if not exists (select 1 from ai_uploads u where u.path = ai_add_entry.file_path and u.owner_id = m) then raise exception 'unknown_upload'; end if;
    if not exists (select 1 from storage.objects o where o.bucket_id = 'files' and o.name = ai_add_entry.file_path) then raise exception 'file_not_uploaded'; end if;
    delete from ai_uploads u where u.path = ai_add_entry.file_path; -- 한 번 쓰면 닫는다
  end if;
  insert into entries (owner_id, title, body, file_path)
  values (m, trim(ai_add_entry.title), nullif(trim(ai_add_entry.body), ''), ai_add_entry.file_path)
  returning * into r;
  return r;
end $$;

-- 4) 큰 파일: MCP 서버(함수 본문 4.5MB 한도)를 거치지 않고 일회용 경로로 Storage에 바로.
create table ai_uploads (
  path text primary key,
  owner_id uuid not null references auth.users on delete cascade,
  expires_at timestamptz not null
);
alter table ai_uploads enable row level security; -- 정책 없음: definer 함수로만

create function ai_upload_open(p text) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from ai_uploads where path = p and expires_at > now());
$$;

create function ai_start_upload(k text, ext text default 'bin') returns text
language plpgsql security definer set search_path = public, extensions as $$
declare m uuid := ai_member(k); p text;
begin
  -- 경로에 128비트 난수: 경로 자체가 권한이다. 확장자는 영문·숫자만.
  p := 'ai/' || m || '/' || encode(gen_random_bytes(16), 'hex') || '.' || coalesce(nullif(regexp_replace(lower(coalesce(ext, '')), '[^a-z0-9]', '', 'g'), ''), 'bin');
  -- Business: 열려 있는 시간은 서비스 소유자가 정한다(예: 1시간).
  insert into ai_uploads (path, owner_id, expires_at) values (p, m, now() + interval '1 hour');
  return p;
end $$;

create policy "ai uploads file" on storage.objects for insert to anon
  with check (bucket_id = 'files' and ai_upload_open(name));
-- 주인은 AI로 올린 자기 파일을 보고 지운다. 레코드를 먼저 지워도 찾을 수 있게 select도 연다.
create policy "see my ai file" on storage.objects for select to authenticated
  using (bucket_id = 'files' and (storage.foldername(name))[1] = 'ai' and (storage.foldername(name))[2] = auth.uid()::text);
create policy "remove my ai file" on storage.objects for delete to authenticated
  using (bucket_id = 'files' and (storage.foldername(name))[1] = 'ai' and (storage.foldername(name))[2] = auth.uid()::text);

-- 5) 권한: Supabase는 public 스키마의 새 함수에 anon·authenticated 실행 권한을 따로 준다(기본 권한).
--    `from public`만으로는 안 막힌다. 세 역할 모두에서 거두고 필요한 것만 다시 준다.
revoke execute on function issue_ai_key, ai_member, ai_whoami, ai_list_entries, ai_add_entry, ai_upload_open, ai_start_upload from public, anon, authenticated;
grant execute on function issue_ai_key to authenticated;
grant execute on function ai_whoami, ai_list_entries, ai_add_entry, ai_start_upload, ai_upload_open to anon, authenticated;
