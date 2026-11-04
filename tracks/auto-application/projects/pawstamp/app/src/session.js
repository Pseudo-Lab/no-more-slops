// 공유 저장소의 소유권은 브라우저 ID 대신 Supabase가 발급한 세션으로 확인한다.
export function createSessionGuard(client) {
  let pending = null;
  return async function sessionOwner() {
    if (!pending) {
      pending = (async () => {
        const { data, error } = await client.auth.getSession();
        if (error) throw error;
        const result = data?.session
          ? await client.auth.getUser()
          : await client.auth.signInAnonymously();
        if (result.error) throw result.error;
        const id = result.data?.user?.id;
        if (!id || (!data?.session && !result.data?.session)) {
          throw new Error('저장 세션을 확인하지 못했어요. 잠시 후 다시 시도해 주세요.');
        }
        return id;
      })();
    }
    const request = pending;
    try { return await request; } finally {
      if (pending === request) pending = null;
    }
  };
}
