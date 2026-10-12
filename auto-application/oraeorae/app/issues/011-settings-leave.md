---
issue: https://github.com/Woo-Yeol/family-health/issues/11
title: "설정 · 로그아웃 · 회원 탈퇴"
labels: feature
status: done
---

- 설정: 내 정보 수정, 동의 내역(날짜), 약관·방침·문의, 로그아웃
- 탈퇴: 삭제/유지 범위 미리 보여 주고 확인 후 `delete_my_account` RPC
- 수정(DB): 가족을 만든 사람이 탈퇴하면 다른 가족 기록까지 지워지던 FK cascade
- 탈퇴 시나리오 3개를 롤백 트랜잭션으로 검증

커밋: b0c88f7
