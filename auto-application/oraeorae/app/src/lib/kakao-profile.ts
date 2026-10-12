import { createClient } from "@/lib/supabase/server";

// What Kakao handed us at login (Supabase keeps it in user_metadata). Read per request, never copied into our tables:
// the privacy policy lists email, nickname and profile image as account info, nothing more (constitution I).
export async function kakaoProfile() {
  const { data } = await (await createClient()).auth.getUser();
  const user = data.user;
  if (!user) return null;
  const meta = user.user_metadata as Record<string, string | undefined>;
  return {
    nickname: meta.name || meta.preferred_username || meta.full_name || null,
    email: user.email ?? null,
    avatarUrl: meta.avatar_url || null,
  };
}
