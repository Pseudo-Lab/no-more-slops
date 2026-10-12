-- Business: a comprehensive report prints ~100 results beyond the 17 national-checkup items (CBC, thyroid, InBody,
-- bone density, text results like "Negative"). Owner decision 2026-10-12: keep every printed result, as printed.
alter table exam_items
  alter column value drop not null,
  -- Printed non-numeric result ("Negative", "정상범위").
  add column text_value text,
  -- The sheet's own section heading ("간기능검사", "체성분분석").
  add column section text,
  -- Reference range exactly as printed; the app never compares against it.
  add column reference text,
  -- H/L mark printed by the lab, not derived.
  add column flag text check (flag in ('H', 'L')),
  add constraint exam_items_has_result check (value is not null or text_value is not null);
