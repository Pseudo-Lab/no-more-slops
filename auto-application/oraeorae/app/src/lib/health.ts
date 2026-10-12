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
