"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { CONSENTS } from "@/lib/consents";
import type { Finding, Item } from "@/lib/health";
import { createClient } from "@/lib/supabase/server";

const REQUIRED_CONSENTS = CONSENTS.map((c) => c.id);

async function recordConsents(formData: FormData) {
  const given = new Set(formData.getAll("consent"));
  if (!REQUIRED_CONSENTS.every((c) => given.has(c))) throw new Error("필수 동의가 필요해요");
  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  const uid = data?.claims.sub;
  if (!uid) redirect("/login");
  const { error } = await supabase.from("consents").upsert(REQUIRED_CONSENTS.map((kind) => ({ user_id: uid, kind })));
  if (error) throw error;
  return supabase;
}

const text = (formData: FormData, key: string) => String(formData.get(key) ?? "").trim().slice(0, 20);
const nameOf = (formData: FormData) => text(formData, "name") || "나";

export async function startFamily(formData: FormData) {
  const supabase = await recordConsents(formData);
  const { error } = await supabase.rpc("create_family", { p_display_name: nameOf(formData) });
  if (error) throw error;
  redirect("/");
}

export async function joinFamily(code: string, formData: FormData) {
  const supabase = await recordConsents(formData);
  const { error } = await supabase.rpc("join_family", { p_code: code, p_display_name: nameOf(formData) });
  if (error) throw error;
  redirect("/");
}

export async function addMember(familyId: string, formData: FormData) {
  const supabase = await createClient();
  const birthYear = Number(formData.get("birthYear")) || null;
  const { error } = await supabase.from("members").insert({
    family_id: familyId,
    display_name: text(formData, "name"),
    relation: text(formData, "relation"),
    birth_year: birthYear,
  });
  if (error) throw error;
  revalidatePath("/", "layout");
}

export async function renewInvite(familyId: string) {
  const supabase = await createClient();
  const { error } = await supabase.rpc("renew_invite", { p_family: familyId });
  if (error) throw error;
  revalidatePath("/invite");
}

// Business: input caps for free text from the client (owner decision 2026-10-12): a 36-page report has ~110 items,
// so 300 leaves room; names stay readable at 60 chars, units/ranges/sections at 40. Text results and findings share
// 100 chars: an ultrasound line like "지방간(경도), 비장비대(종대)" blocked a save at 40 (2026-10-12).
const MAX_ITEMS = 300, MAX_LABEL = 60, MAX_SHORT = 40, MAX_TEXT = 100, MAX_FINDINGS = 30, MAX_FINDING = MAX_TEXT;
const short = (s: unknown, max = MAX_SHORT) => s === null || (typeof s === "string" && s.length <= max);

// Returns an error message instead of throwing so the review screen can show it next to the save button.
export async function saveExam(memberId: string, examDate: string, items: Item[], findings: Finding[] = []): Promise<{ error: string } | void> {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(examDate)) return { error: "검진일을 입력해 주세요" };
  if (items.length > MAX_ITEMS) return { error: `항목은 ${MAX_ITEMS}개까지 저장할 수 있어요` };
  const badItem = items.find((i) =>
    typeof i.key !== "string" || !i.key || i.key.length > MAX_LABEL || typeof i.label !== "string" || !i.label.trim() || i.label.length > MAX_LABEL
    // History: section/reference aren't editable on the review screen, so a 40-char cap blocked saving a sheet whose
    // heading reads "지질검사 (Lipid Test), 혈관질환 위험인자 (Vascular risk factor)" (54 chars, 2026-10-12). Same cap as text results.
    || typeof i.unit !== "string" || !short(i.unit) || !short(i.section, MAX_TEXT) || !short(i.reference, MAX_TEXT)
    || !(i.value === null ? typeof i.textValue === "string" && i.textValue.trim() && i.textValue.length <= MAX_TEXT : Number.isFinite(i.value) && i.textValue === null)
    || ![null, "H", "L"].includes(i.flag) || (i.judgement !== null && !["정상", "경계", "질환의심"].includes(i.judgement)));
  if (badItem) return { error: `값을 확인해 주세요: ${typeof badItem.label === "string" ? badItem.label.slice(0, MAX_LABEL) : "항목"}` };
  // Constraint: findings are free text from the client; cap them so one save can't flood a family's records.
  if (findings.length > MAX_FINDINGS || findings.some((f) => typeof f.finding !== "string" || !f.finding.trim() || f.finding.length > MAX_FINDING)) return { error: "소견을 확인해 주세요" };
  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  const uid = data?.claims.sub;
  if (!uid) redirect("/login");

  const { data: exam, error } = await supabase
    .from("exams").insert({ member_id: memberId, exam_date: examDate, created_by: uid }).select("id").single();
  if (error) return { error: "저장하지 못했어요. 잠시 후 다시 눌러 주세요" };
  const { error: itemsError } = items.length
    ? await supabase.from("exam_items").insert(
      // Only real columns: extraction-only fields like `uncertain` would make the insert fail.
      items.map((i) => ({
        key: i.key, label: i.label.trim(), unit: i.unit.trim(), section: i.section?.trim() || null, value: i.value,
        text_value: i.textValue?.trim() ?? null, reference: i.reference?.trim() || null, flag: i.flag, judgement: i.judgement, exam_id: exam.id,
      })),
    )
    : { error: null };
  const { error: findingsError } = findings.length
    ? await supabase.from("exam_findings").insert(
      findings.map((f) => ({ category: typeof f.category === "string" ? f.category.slice(0, MAX_SHORT) : null, finding: f.finding.trim(), exam_id: exam.id })),
    )
    : { error: null };
  if (itemsError || findingsError) {
    // Future: no transaction across these inserts; drop the empty exam so a failed save leaves nothing behind.
    await supabase.from("exams").delete().eq("id", exam.id);
    return { error: "저장하지 못했어요. 잠시 후 다시 눌러 주세요" };
  }
  revalidatePath("/", "layout");
  redirect(`/member/${memberId}`);
}

export async function updateMember(memberId: string, formData: FormData) {
  const supabase = await createClient();
  const { error } = await supabase.from("members").update({
    display_name: text(formData, "name") || "이름 없음",
    relation: text(formData, "relation"),
    birth_year: Number(formData.get("birthYear")) || null,
    next_exam: text(formData, "nextExam") || null,
  }).eq("id", memberId);
  if (error) throw error;
  revalidatePath("/", "layout");
  redirect(`/member/${memberId}`);
}

// RLS only lets proxy members (no login) be removed; family members with a login leave by deleting their account.
export async function deleteMember(memberId: string) {
  const supabase = await createClient();
  const { error } = await supabase.from("members").delete().eq("id", memberId).is("user_id", null);
  if (error) throw error;
  revalidatePath("/", "layout");
  redirect("/");
}

export async function deleteExam(memberId: string, examId: string) {
  const supabase = await createClient();
  const { error } = await supabase.from("exams").delete().eq("id", examId);
  if (error) throw error;
  revalidatePath("/", "layout");
  redirect(`/member/${memberId}`);
}

export async function signOut() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/login");
}

export async function deleteAccount() {
  const supabase = await createClient();
  const { error } = await supabase.rpc("delete_my_account");
  if (error) throw error;
  await supabase.auth.signOut();
  redirect("/login?deleted=1");
}
