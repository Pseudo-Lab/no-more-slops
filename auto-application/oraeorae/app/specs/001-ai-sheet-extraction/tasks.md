# Tasks: 결과지 AI 판독

**Input**: Design documents from `/specs/001-ai-sheet-extraction/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup

- [x] T001 Set `experimental.serverActions.bodySizeLimit` to `4mb` in next.config.ts

## Phase 2: Foundational

- [x] T002 [P] Create standard checkup item catalog in src/lib/checkup-items.ts (keep existing keys sbp, dbp, glucose, ldl, alt)
- [x] T003 [P] Add `extract_error` funnel event in src/lib/analytics.ts

## Phase 3: User Story 1 - 결과지 사진을 올리면 수치가 채워진다 (P1) 🎯 MVP

**Goal**: 실제 결과지 값이 확인 화면에 채워진다
**Independent Test**: 결과지 사진 업로드 → 확인 화면 값이 결과지와 같다

- [x] T004 [US1] Server action `extractSheet` in src/app/(family)/upload/extract.ts: login + transfer consent check, OpenAI Responses API with strict JSON schema, `store: false`, sample fallback when no key
- [x] T005 [US1] Move review-form.tsx to src/app/(family)/upload/ and allow empty judgement until the user picks one
- [x] T006 [US1] Upload form: shrink photos to 2048px on device, call `extractSheet`, switch to review step with its own header
- [x] T007 [US1] Move page header into the form, delete src/app/(family)/upload/review/

## Phase 4: User Story 2 - 읽지 못하면 이유와 다음 행동을 알려 준다 (P2)

- [x] T008 [US2] Error messages for not-a-sheet / too large / service failure; keep the chosen file; track `extract_error`

## Phase 4b: Cost & Accuracy

- [x] T012 Resize photos to the 2,500-patch / 2048px budget in upload-form.tsx
- [x] T013 Static `instructions` with item labels and units, `reasoning.effort: "none"`, pinned model snapshot in extract.ts
- [x] T014 `uncertain` field in schema; "확인 필요" badge in review-form.tsx
- [x] T015 One retry on 429/5xx; handle incomplete responses and JSON parse failures

## Phase 4c: Multi-page PDF

- [x] T016 [US1] Parse PDFs on device with pdfjs-dist: all-page text (RRN masked) + best result page image in sheet-image.ts
- [x] T017 [US1] `find` hints in the catalog for result-page detection
- [x] T018 [US1] Server accepts report text; rules for checkbox forms, slash values, `***`
- [x] T019 [US1] Values on other pages when the result page shows `***`; judgement may stay null and is saved as null (migration drops NOT NULL)
- [x] T020 [US2] Daily limit of 5 AI reads per user (Korean day) via `take_extract_quota` RPC; counted before the paid call
- [x] T021 Switch model to `gpt-5.6-luna` after a 3-run comparison with gpt-5.4-mini on a 36-page report
- [x] T022 [US1] Exam date from the sheet pre-fills the review date; non-numeric findings (장기별·종합소견) extracted verbatim, editable, saved to `exam_findings`, shown on member and home pages
- [x] T023 [US1] Keep every printed result: free `key`/`label`/`section`, text results, reference and H/L as printed (exam_items columns), image-only PDF pages sent as images, review grouped by section

## Phase 5: Polish

- [ ] T009 Lint + build; local check without key (sample path)
- [ ] T010 Update issue #2 with the owner steps (register `OPENAI_API_KEY` in Vercel) and deploy
- [ ] T011 Verify with a real sheet on the production URL after the key is registered
