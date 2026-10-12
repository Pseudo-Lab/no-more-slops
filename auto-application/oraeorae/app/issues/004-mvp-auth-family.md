---
issue: https://github.com/Woo-Yeol/family-health/issues/4
title: "카카오 로그인 · 가족 그룹 · 민감정보 동의"
labels: feature
status: done
---

- Supabase Auth 카카오 로그인, 세션 갱신 proxy, 비로그인 시 랜딩으로 이동
- 민감정보·가족 공유·국외 이전 3개 개별 동의 기록 (`consents`)
- 가족 만들기 / 초대 링크(7일 만료, 새 링크 발급) / 참여
- 부모님 등 로그인 없는 구성원을 대신 추가
- RLS: 가족 단위로만 읽기·쓰기 (가짜 사용자 2명으로 교차 접근 차단 검증)

커밋: bd7b121
