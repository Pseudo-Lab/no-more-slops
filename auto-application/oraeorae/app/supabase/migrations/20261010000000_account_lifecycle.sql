-- Account deletion and member management.

-- History: created_by cascaded on families, so the creator leaving wiped every other member's records,
-- and on exams it blocked deleting anyone who had uploaded for a relative. Keep the rows, drop the pointer.
alter table families alter column created_by drop not null;
alter table families drop constraint families_created_by_fkey,
  add constraint families_created_by_fkey foreign key (created_by) references auth.users on delete set null;

alter table exams alter column created_by drop not null;
alter table exams drop constraint exams_created_by_fkey,
  add constraint exams_created_by_fkey foreign key (created_by) references auth.users on delete set null;

-- Proxy members (no login) can be removed by their family; members with a login leave by deleting their account.
create policy "remove proxy member" on members for delete using (is_family_member(family_id) and user_id is null);

-- Business: on leaving, the user's own profile, records and consents go immediately; records kept for relatives
-- stay with the family. If no one with a login remains, the whole family is deleted so nothing is orphaned.
create function delete_my_account() returns void
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  delete from families f
  where is_family_member(f.id)
    and not exists (select 1 from members m where m.family_id = f.id and m.user_id is not null and m.user_id <> auth.uid());
  delete from auth.users where id = auth.uid();
end $$;

revoke execute on function delete_my_account from public, anon;
grant execute on function delete_my_account to authenticated;
