-- Business: AI reads become a per-account credit (owner decision 2026-10-12): 3 free at signup, 1 per read; buying
-- more is #26. Replaces the daily cap, which the credit total already bounds. Holds counts only, never sheet content.
create table credit_ledger (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users on delete cascade,
  delta int not null,
  reason text not null check (reason in ('signup', 'grant', 'extract', 'refund', 'purchase')),
  -- The 'extract' row a refund reverses; unique, so a read is refunded at most once.
  refunds bigint references credit_ledger unique,
  created_at timestamptz not null default now()
);
create index on credit_ledger (user_id);
alter table credit_ledger enable row level security;
create policy "read own ledger" on credit_ledger for select using (user_id = auth.uid());
-- No insert/update/delete policies: balances change only through the functions below.

create function credit_balance() returns int
language sql stable security invoker set search_path = public as $$
  select coalesce(sum(delta), 0)::int from credit_ledger where user_id = auth.uid();
$$;

-- Takes one credit and returns the ledger row id, or null when the balance is 0.
-- Locked per user so two taps in flight can't both pass the balance check.
create function spend_credit() returns bigint
language plpgsql security definer set search_path = public as $$
declare rid bigint;
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  perform pg_advisory_xact_lock(hashtext(auth.uid()::text));
  if (select coalesce(sum(delta), 0) from credit_ledger where user_id = auth.uid()) < 1 then return null; end if;
  insert into credit_ledger (user_id, delta, reason) values (auth.uid(), -1, 'extract') returning id into rid;
  return rid;
end $$;

-- Gives back the credit of a read that failed on our side.
-- shortcut: the caller can refund any of their own reads from the last 2 minutes, so a hand-crafted call could reverse
-- one successful read; move the refund behind a server-only key before credits are sold (#26).
create function refund_credit(p_spend bigint) returns void
language plpgsql security definer set search_path = public as $$
begin
  insert into credit_ledger (user_id, delta, reason, refunds)
  select s.user_id, 1, 'refund', s.id from credit_ledger s
  where s.id = p_spend and s.user_id = auth.uid() and s.reason = 'extract' and s.created_at > now() - interval '2 minutes'
    and not exists (select 1 from credit_ledger r where r.refunds = s.id);
end $$;

revoke execute on function credit_balance, spend_credit, refund_credit from public, anon;
grant execute on function credit_balance, spend_credit, refund_credit to authenticated;

-- Every new account starts with 3 free reads.
create function grant_signup_credits() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into credit_ledger (user_id, delta, reason) values (new.id, 3, 'signup');
  return new;
end $$;
create trigger on_auth_user_created after insert on auth.users for each row execute function grant_signup_credits();

-- Existing accounts get the same 3. The owner's account (the public service contact) gets 100 for testing.
insert into credit_ledger (user_id, delta, reason) select id, 3, 'signup' from auth.users;
insert into credit_ledger (user_id, delta, reason) select id, 100, 'grant' from auth.users where email = 'king199276@gmail.com';

drop function take_extract_quota(int);
drop table extract_usage;
