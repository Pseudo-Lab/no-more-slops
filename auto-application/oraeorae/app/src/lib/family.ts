import "server-only";
import { redirect } from "next/navigation";
import { connection } from "next/server";
import { cache } from "react";
import { createClient } from "./supabase/server";
import type { Exam, Judgement, Member } from "./health";

export type Family = { id: string; inviteCode: string; inviteExpiresAt: string; members: Member[]; meId: string };

type Row = {
  id: string; user_id: string | null; display_name: string; relation: string; birth_year: number | null; next_exam: string | null;
  exams: { id: string; exam_date: string; exam_items: { key: string; label: string; unit: string; section: string | null; value: number | null; text_value: string | null; reference: string | null; flag: "H" | "L" | null; judgement: Judgement | null }[];
    exam_findings: { category: string | null; finding: string }[] }[];
};

// Returns null when the signed-in user hasn't created or joined a family yet. Cached per request: layout and page both read it.
export const getFamily = cache(async (): Promise<Family | null> => {
  // Constraint: ages use the current year; with cacheComponents, reading the clock needs connection() first so it runs per request.
  await connection();
  const supabase = await createClient();
  const { data: claims } = await supabase.auth.getClaims();
  const uid = claims?.claims.sub;
  if (!uid) return null;

  const { data: me } = await supabase.from("members").select("id, family_id").eq("user_id", uid).limit(1).maybeSingle();
  if (!me) return null;

  const [{ data: family }, { data: rows, error }] = await Promise.all([
    supabase.from("families").select("invite_code, invite_expires_at").eq("id", me.family_id).single(),
    supabase.from("members")
      .select("id, user_id, display_name, relation, birth_year, next_exam, exams(id, exam_date, exam_items(key, label, unit, section, value, text_value, reference, flag, judgement), exam_findings(category, finding))")
      .eq("family_id", me.family_id).order("created_at"),
  ]);
  if (error) throw error;

  const year = new Date().getFullYear();
  const members = (rows as Row[]).map((r): Member => ({
    id: r.id,
    name: r.display_name,
    relation: r.relation,
    birthYear: r.birth_year,
    age: r.birth_year ? year - r.birth_year : null,
    nextExam: r.next_exam,
    hasLogin: r.user_id !== null,
    exams: r.exams
      .map((e): Exam => ({ id: e.id, date: e.exam_date, items: e.exam_items.map(({ text_value, ...i }) => ({ ...i, value: i.value === null ? null : Number(i.value), textValue: text_value })), findings: e.exam_findings }))
      .sort((a, b) => a.date.localeCompare(b.date)),
  }));
  return { id: me.family_id, inviteCode: family!.invite_code, inviteExpiresAt: family!.invite_expires_at, members, meId: me.id };
});

export async function requireFamily(): Promise<Family> {
  const family = await getFamily();
  if (!family) redirect("/start");
  return family;
}
