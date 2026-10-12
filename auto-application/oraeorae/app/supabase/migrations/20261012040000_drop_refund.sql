-- Business: a read that fails on our side simply costs the credit (owner decision 2026-10-12); refunds come back
-- with the payment feature (#26), behind a server-only key instead of a user-callable function.
drop function refund_credit(bigint);
