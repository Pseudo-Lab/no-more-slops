-- Families share health records only inside their own group; every table is RLS-guarded by group membership.

create table families (
  id uuid primary key default gen_random_uuid(),
  name text not null default '우리 가족',
  invite_code text not null unique default upper(substr(md5(gen_random_uuid()::text), 1, 8)),
  -- Business: invite links expire after 7 days so a leaked link can't be used indefinitely.
  invite_expires_at timestamptz not null default now() + interval '7 days',
  created_by uuid not null references auth.users on delete cascade,
  created_at timestamptz not null default now()
);

-- A member may have no login: a child can register a parent and upload on their behalf (with the parent's consent).
create table members (
  id uuid primary key default gen_random_uuid(),
  family_id uuid not null references families on delete cascade,
  user_id uuid references auth.users on delete cascade,
  display_name text not null,
  relation text not null default '',
  birth_year int,
  next_exam text,
  created_at timestamptz not null default now(),
  unique (family_id, user_id)
);

-- Constraint: health data is sensitive personal information (PIPA art. 23); we keep proof of each separate consent.
create table consents (
  user_id uuid not null references auth.users on delete cascade,
  kind text not null check (kind in ('sensitive', 'share', 'transfer')),
  agreed_at timestamptz not null default now(),
  primary key (user_id, kind)
);

create table exams (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references members on delete cascade,
  exam_date date not null,
  created_by uuid not null references auth.users,
  created_at timestamptz not null default now()
);

create table exam_items (
  id bigint generated always as identity primary key,
  exam_id uuid not null references exams on delete cascade,
  key text not null,
  label text not null,
  unit text not null,
  value numeric not null,
  -- The judgement printed on the sheet; the app never derives its own.
  judgement text not null check (judgement in ('정상', '경계', '질환의심'))
);

create index on members (family_id);
create index on exams (member_id, exam_date);
create index on exam_items (exam_id);

-- security definer so policies can check membership without recursing into members' own RLS.
create function is_family_member(fid uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from members where family_id = fid and user_id = auth.uid());
$$;

create function member_family(mid uuid) returns uuid
language sql stable security definer set search_path = public as $$
  select family_id from members where id = mid;
$$;

alter table families enable row level security;
alter table members enable row level security;
alter table consents enable row level security;
alter table exams enable row level security;
alter table exam_items enable row level security;

create policy "read own families" on families for select using (is_family_member(id));

create policy "read family members" on members for select using (is_family_member(family_id));
create policy "add proxy member" on members for insert with check (is_family_member(family_id) and user_id is null);
create policy "edit family member" on members for update using (is_family_member(family_id));

create policy "own consents" on consents for all using (user_id = auth.uid()) with check (user_id = auth.uid());

create policy "read family exams" on exams for select using (is_family_member(member_family(member_id)));
create policy "add family exams" on exams for insert with check (is_family_member(member_family(member_id)) and created_by = auth.uid());
create policy "delete family exams" on exams for delete using (is_family_member(member_family(member_id)));

create policy "read family items" on exam_items for select
  using (exists (select 1 from exams e where e.id = exam_id and is_family_member(member_family(e.member_id))));
create policy "add family items" on exam_items for insert
  with check (exists (select 1 from exams e where e.id = exam_id and is_family_member(member_family(e.member_id))));

-- Creating a family and joining by code need to write rows the caller can't see yet, so they run as definer.
create function create_family(p_display_name text) returns uuid
language plpgsql security definer set search_path = public as $$
declare fid uuid;
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  insert into families (created_by) values (auth.uid()) returning id into fid;
  insert into members (family_id, user_id, display_name, relation) values (fid, auth.uid(), p_display_name, '본인');
  return fid;
end $$;

create function join_family(p_code text, p_display_name text) returns uuid
language plpgsql security definer set search_path = public as $$
declare fid uuid;
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  select id into fid from families where invite_code = upper(p_code) and invite_expires_at > now();
  if fid is null then raise exception 'invalid or expired invite'; end if;
  insert into members (family_id, user_id, display_name) values (fid, auth.uid(), p_display_name)
  on conflict (family_id, user_id) do nothing;
  return fid;
end $$;

create function renew_invite(p_family uuid) returns text
language plpgsql security definer set search_path = public as $$
declare code text;
begin
  if not is_family_member(p_family) then raise exception 'not a member'; end if;
  update families set invite_code = upper(substr(md5(gen_random_uuid()::text), 1, 8)),
    invite_expires_at = now() + interval '7 days' where id = p_family returning invite_code into code;
  return code;
end $$;

revoke execute on function create_family, join_family, renew_invite from public, anon;
grant execute on function create_family, join_family, renew_invite to authenticated;
