# 오래오래 Constitution

## Core Principles

### I. Health Data Minimization (NON-NEGOTIABLE)
- Health values, judgements and member names MUST be stored only after the user reviews them.
- Original result sheets (images/PDFs) MUST NOT be stored; they live in memory for one request only.
- Analytics, logs and error reports MUST NOT contain health values, judgements, names, member ids
  or invite codes.

Rationale: health data is sensitive information under PIPA art. 23; leaking it ends the service.

### II. Consent Before Processing
- Sensitive-data processing, family sharing and cross-border transfer each need their own
  consent (PIPA art. 15/17/23/28-8), recorded with a timestamp before the feature runs.
- Any new processor or overseas recipient MUST be added to `/privacy` and `src/lib/consents.ts`
  in the same change that starts sending it data.

Rationale: a separate, informed consent is the legal basis for every feature that touches
health data.

### III. Record, Not Diagnose
- The app MUST show judgements exactly as printed on the sheet and MUST NOT produce its own
  medical judgement, advice or risk score.
- AI output is a draft: the user confirms or edits every value before it is saved.

Rationale: the service is not a medical device; medical judgement creates liability.

### IV. Security at the Boundary
- Row Level Security on every table; privileged operations go through `security definer` RPCs
  scoped to `auth.uid()`.
- Secret keys (Supabase secret, AI provider keys) stay server-only and never reach the client,
  repo, chat or notes.
- Server actions validate their input and return `{ error }` instead of throwing to the user.

Rationale: the client is untrusted; family members must never read another family's data.

### V. Smallest Shippable Change
- Each GitHub issue ships as one small, deployable change: spec → plan → tasks → implement →
  verify on the production URL.
- YAGNI and KISS: no option, abstraction or dependency without a current requirement.
- Comments explain why (`Business` / `History` / `Constraint` / `Future`); new magic numbers
  get the owner's reasoning first.

Rationale: a 12-week experiment rewards fast, verifiable steps over speculative design.

## Technology & Operations

- Next.js 16 App Router with Cache Components, Tailwind v4, Supabase (Seoul), Vercel (icn1).
- Login is Kakao OAuth only; Korean UI, mobile first, dark mode follows the system.
- Schema changes go through `supabase/migrations` and `supabase db push`; never
  `supabase config push`.
- Production URL: https://oraeorae.kro.kr (also https://family-health-wheat.vercel.app)

## Development Workflow

- One branch/spec per issue under `specs/`; the issue number is referenced in commits.
- Before closing an issue: lint passes, `next build` passes, and the changed flow is checked on
  the production URL (or the reason it cannot be is written on the issue).
- Steps that need the owner (dashboard settings, keys, legal names) are listed on the issue
  instead of guessed.

## Governance

This constitution overrides other practices in this repo. Amendments update this file with a
version bump (MAJOR: principle removed/redefined, MINOR: principle added, PATCH: wording) and
are committed with the change that needs them. Every spec's plan includes a Constitution Check
against principles I–V.

**Version**: 1.0.1 | **Ratified**: 2026-10-10 | **Last Amended**: 2026-10-11
