-- launch-basics 템플릿. <버킷>·<경로 규칙>을 서비스에 맞게 바꾼다. profiles.id가 auth.users를 on delete cascade로 참조하고,
-- 사용자가 만든 모든 테이블이 profiles를 on delete cascade로 참조한다는 전제다.

-- 1. 퍼널 단계. 사람 id·IP·주소·수치는 남기지 않는다. 누가 했는지 모르고 몇 번 일어났는지만 안다.
create table events (
  id bigint generated always as identity primary key,
  step text not null check (step in ('landing', 'login_start', 'signup', 'core_action', 'saved', 'shared')),
  at timestamptz not null default now()
);
alter table events enable row level security;
create policy "anyone records a step" on events for insert to anon, authenticated with check (true);
-- 읽기 정책은 없다. 숫자는 운영자 함수로만 본다.

create function admin_funnel() returns json
language plpgsql stable security definer set search_path = public as $$
begin
  if not is_admin() then raise exception 'not_admin'; end if;   -- 서비스의 운영자 판정 함수
  return (
    select coalesce(json_agg(json_build_object('step', s.step, 'd7', s.d7, 'd30', s.d30) order by s.ord), '[]')
    from (
      select k.step, k.ord,
        (select count(*) from events e where e.step = k.step and e.at > now() - interval '7 days') d7,
        (select count(*) from events e where e.step = k.step and e.at > now() - interval '30 days') d30
      from unnest(array['landing', 'login_start', 'signup', 'core_action', 'saved', 'shared']) with ordinality k(step, ord)
    ) s
  );
end $$;
revoke execute on function admin_funnel from public, anon;
grant execute on function admin_funnel to authenticated;

-- 2. 탈퇴 1단계: 내가 올린 파일 경로. Storage 파일은 SQL로 지울 수 없어 앱이 이 목록으로 storage.remove()를 먼저 부른다.
create function my_video_paths() returns setof text
language sql stable security definer set search_path = public, storage as $$
  select o.name from storage.objects o
  where o.bucket_id = '<버킷>'
    and (storage.foldername(o.name))[1] = auth.uid()::text;   -- <경로 규칙>: 첫 폴더가 올린 사람
$$;

-- 3. 탈퇴 2단계: auth.users를 지우면 profiles → 그 사람이 만든 모든 행이 cascade로 지워진다.
create function delete_my_account() returns void
language plpgsql security definer set search_path = public, auth as $$
begin
  if auth.uid() is null then raise exception 'not_signed_in'; end if;
  delete from auth.users where id = auth.uid();
end $$;

-- Supabase는 public 스키마의 새 함수에 anon·authenticated 실행 권한을 따로 준다. `from public`만으로는 안 막힌다.
revoke execute on function my_video_paths, delete_my_account from public, anon, authenticated;
grant execute on function my_video_paths, delete_my_account to authenticated;
