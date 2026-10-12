-- Business: AI sheet reading costs money per call; 5 reads per user per Korean day caps abuse (owner decision 2026-10-12).
-- Holds only counts, never sheet content.
create table extract_usage (
  user_id uuid not null references auth.users on delete cascade,
  day date not null,
  count int not null default 0,
  primary key (user_id, day)
);
-- No policies: rows are written only through take_extract_quota below.
alter table extract_usage enable row level security;

-- Atomically takes one read from today's quota; false once the limit is reached.
create function take_extract_quota(p_limit int) returns boolean
language plpgsql security definer set search_path = public as $$
declare used int;
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  insert into extract_usage (user_id, day, count) values (auth.uid(), (now() at time zone 'Asia/Seoul')::date, 1)
  on conflict (user_id, day) do update set count = extract_usage.count + 1
  returning count into used;
  return used <= p_limit;
end $$;

revoke execute on function take_extract_quota from public, anon;
grant execute on function take_extract_quota to authenticated;
