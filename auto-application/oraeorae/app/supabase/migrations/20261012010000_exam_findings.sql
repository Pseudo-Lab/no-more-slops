-- Business: sheets list findings with no number (e.g. "경증 지방간", "역류성식도염"); missing them hid most of a
-- comprehensive checkup (owner feedback 2026-10-12). Stored verbatim as printed — the app adds no judgement (constitution III).
create table exam_findings (
  id bigint generated always as identity primary key,
  exam_id uuid not null references exams on delete cascade,
  -- The sheet's own grouping (e.g. "소화기계", "간"), when it has one.
  category text,
  finding text not null
);

create index on exam_findings (exam_id);
alter table exam_findings enable row level security;

create policy "read family findings" on exam_findings for select
  using (exists (select 1 from exams e where e.id = exam_id and is_family_member(member_family(e.member_id))));
create policy "add family findings" on exam_findings for insert
  with check (exists (select 1 from exams e where e.id = exam_id and is_family_member(member_family(e.member_id))));
