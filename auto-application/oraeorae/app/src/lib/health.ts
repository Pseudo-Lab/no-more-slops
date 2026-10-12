// The judgement printed on the checkup sheet; the app never derives its own.
export type Judgement = "정상" | "경계" | "질환의심";

// One printed result. `key` is a catalog key for the 17 national-checkup items (trends match by it) and the printed
// name for everything else. Either `value` (number) or `textValue` ("Negative") is set. `reference` and `flag` (H/L)
// are copied from the sheet, never computed.
export type Item = {
  key: string; label: string; unit: string; section: string | null;
  value: number | null; textValue: string | null; reference: string | null; flag: "H" | "L" | null; judgement: Judgement | null;
};
// A finding printed on the sheet without a number (e.g. "경증 지방간"), kept word for word.
export type Finding = { category: string | null; finding: string };
export type Exam = { id: string; date: string; items: Item[]; findings: Finding[] };
export type Member = {
  id: string; name: string; relation: string; birthYear: number | null; age: number | null; nextExam: string | null; hasLogin: boolean; exams: Exam[];
};

export const latest = (m: Member): Exam | undefined => m.exams[m.exams.length - 1];
// "주의" = what the sheet itself marked (owner decision 2026-10-12): 질환의심 is the stronger mark; 경계 and a lab H/L the lighter.
export const severity = (i: Pick<Item, "judgement" | "flag">): "danger" | "warn" | null => (i.judgement === "질환의심" ? "danger" : i.judgement === "경계" || i.flag !== null ? "warn" : null);
export const flagged = (exam: Exam | undefined) => exam?.items.filter((i) => severity(i) !== null) ?? [];

export function history(m: Member, key: string) {
  return m.exams.flatMap((e) => e.items.filter((i) => i.key === key && i.value !== null).map((i) => ({ year: e.date.slice(0, 4), value: i.value! })));
}

export const formatDate = (iso: string) => iso.replaceAll("-", ".");

// Sheets print headings bilingually ("간기능검사 (Liver Function Test)"); the English tail only costs a line on a phone.
export const printed = (s: string) => s.replace(/\s*\([^()]*[A-Za-z][^()]*\)\s*$/, (m) => (/[가-힣]/.test(m) ? m : "")).trim() || s;

// One glance per person (UI reference 2026-10-12): a dot colour and a sentence, both derived only from what the sheet
// marked. 질환의심 outranks everything; 경계·H/L and a printed finding share the lighter colour; nothing marked is green.
export type Level = "danger" | "warn" | "ok" | "none";
export function glance(exam: Exam | undefined): { level: Level; sentence: string; counts: string } {
  if (!exam) return { level: "none", sentence: "아직 올린 결과지가 없어요", counts: "기록 없음" };
  const danger = exam.items.filter((i) => severity(i) === "danger").length;
  const warn = exam.items.filter((i) => severity(i) === "warn").length;
  const findings = exam.findings.length;
  const parts = [danger && `질환의심 ${danger}`, warn && `경계·H/L ${warn}`, findings && `소견 ${findings}`].filter(Boolean).join(" · ");
  if (danger) return { level: "danger", sentence: `질환의심 ${danger}개가 있어요`, counts: parts };
  if (warn) return { level: "warn", sentence: `주의 ${warn}개, 질환의심은 없어요`, counts: parts };
  if (findings) return { level: "warn", sentence: `수치는 모두 정상, 소견 ${findings}개`, counts: `수치 정상 · 소견 ${findings}` };
  return { level: "ok", sentence: "모두 정상이에요", counts: "모두 정상" };
}

// Where a value sits against the printed reference, as a 0–100 position plus the band the reference covers.
// Handles "70~99", "0 - 40", "<200", "≤5.6", "≥1.00"; anything else (text, 남/여 split ranges) returns null and the
// reference stays as text. shortcut: a one-sided range is drawn against its own bound (0..2×), good enough for a glance.
export function rangeBar(value: number, reference: string | null): { pos: number; band: [number, number] } | null {
  if (!reference) return null;
  const num = "(-?\\d+(?:\\.\\d+)?)";
  const clamp = (n: number) => Math.min(98, Math.max(2, n));
  const two = reference.match(new RegExp(`^\\s*${num}\\s*[~\\-–]\\s*${num}`));
  if (two) {
    const [lo, hi] = [Number(two[1]), Number(two[2])];
    return hi > lo ? { pos: clamp(25 + ((value - lo) / (hi - lo)) * 50), band: [25, 75] } : null;
  }
  const upper = reference.match(new RegExp(`^\\s*[<≤]\\s*=?\\s*${num}`));
  if (upper) { const hi = Number(upper[1]); return hi > 0 ? { pos: clamp((value / hi) * 75), band: [0, 75] } : null; }
  const lower = reference.match(new RegExp(`^\\s*[>≥]\\s*=?\\s*${num}`));
  if (lower) { const lo = Number(lower[1]); return lo > 0 ? { pos: clamp(25 + ((value - lo) / lo) * 50), band: [25, 100] } : null; }
  return null;
}

// Items a person has as a number in two or more exams, the ones the exam on screen marked first. Only the printed
// values travel; whether a line going up is good or bad is for the doctor (constitution III).
export function trends(m: Member, exam: Exam) {
  const newest = [...m.exams].reverse().flatMap((e) => e.items);
  const marked = (key: string) => (severity(exam.items.find((i) => i.key === key) ?? { judgement: null, flag: null }) ? 0 : 1);
  return [...new Set(newest.map((i) => i.key))]
    .map((key) => ({ item: newest.find((i) => i.key === key)!, points: history(m, key) }))
    .filter((t) => t.points.length >= 2)
    .sort((a, b) => marked(a.item.key) - marked(b.item.key));
}
