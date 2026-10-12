// GA4 funnel events. Constraint: health data is sensitive (PIPA art. 23), so events carry step names only —
// never values, judgements, names, member ids or invite codes.
export const GA_ID = process.env.NEXT_PUBLIC_GA_ID;

export type FunnelEvent =
  | "login_click"
  | "family_create"
  | "family_join"
  | "upload_file_selected"
  | "upload_submit"
  | "extract_error"
  | "exam_save"
  | "exam_save_error"
  | "invite_share"
  | "invite_copy";

// Calls before gtag.js loads are queued on dataLayer and replayed by the script, so early page views aren't lost.
// eslint-disable-next-line @typescript-eslint/no-unused-vars -- the params only type the call; arguments carries them.
export function gtag(..._args: unknown[]) {
  if (!GA_ID) return;
  const w = window as Window & { dataLayer?: unknown[] };
  w.dataLayer = w.dataLayer || [];
  // Constraint: gtag.js reads the Arguments object itself, not an array copy.
  // eslint-disable-next-line prefer-rest-params
  w.dataLayer.push(arguments);
}

export const track = (event: FunnelEvent) => gtag("event", event);

// Page paths contain member ids and invite codes; collapse them so GA only ever sees the route shape.
export const normalizePath = (path: string) =>
  path.replace(/^\/member\/[^/]+/, "/member/:id").replace(/^\/join\/[^/]+/, "/join/:code");
