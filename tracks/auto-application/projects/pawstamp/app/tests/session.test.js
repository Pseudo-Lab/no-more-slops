import assert from 'node:assert/strict';
import test from 'node:test';
import { createSessionGuard } from '../src/session.js';

test('simultaneous first writes share one anonymous sign-in', async () => {
  let calls = 0;
  const owner = createSessionGuard({ auth: {
    getSession: async () => ({ data: { session: null } }),
    signInAnonymously: async () => {
      calls++;
      return { data: { session: {}, user: { id: 'owner-a' } } };
    },
  } });
  assert.deepEqual(await Promise.all([owner(), owner(), owner()]), ['owner-a', 'owner-a', 'owner-a']);
  assert.equal(calls, 1);
});

test('existing sessions are verified rather than replaced or trusted locally', async () => {
  let id = 'owner-a';
  const owner = createSessionGuard({ auth: {
    getSession: async () => ({ data: { session: { user: { id: 'untrusted-id' } } } }),
    getUser: async () => ({ data: { user: { id } } }),
    signInAnonymously: async () => { throw new Error('unexpected sign-in'); },
  } });
  assert.equal(await owner(), 'owner-a');
  id = 'owner-b';
  assert.equal(await owner(), 'owner-b');
});

test('authentication failure blocks writes and a later operation can retry', async () => {
  let fail = true;
  const owner = createSessionGuard({ auth: {
    getSession: async () => ({ data: { session: null } }),
    signInAnonymously: async () => fail
      ? { error: new Error('anonymous sign-ins disabled') }
      : { data: { session: {}, user: { id: 'owner-a' } } },
  } });
  let writes = 0;
  await assert.rejects(async () => { await owner(); writes++; }, /disabled/);
  assert.equal(writes, 0);
  fail = false;
  assert.equal(await owner(), 'owner-a');
});

test('missing user or session never grants an owner', async () => {
  for (const data of [{ session: {} }, { user: { id: 'owner-a' } }]) {
    const owner = createSessionGuard({ auth: {
      getSession: async () => ({ data: { session: null } }),
      signInAnonymously: async () => ({ data }),
    } });
    await assert.rejects(owner(), /저장 세션/);
  }
});
