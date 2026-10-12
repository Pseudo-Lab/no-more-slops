-- A measured value can appear elsewhere in the same checkup even when its summary has no checked judgement.
alter table public.exam_items alter column judgement drop not null;
