import { createClient } from "@/lib/supabase/server";

// Remaining AI reads for the signed-in account (ledger sum; see migration 20261012030000_credits).
export async function creditBalance() {
  const { data } = await (await createClient()).rpc("credit_balance");
  return typeof data === "number" ? data : 0;
}
