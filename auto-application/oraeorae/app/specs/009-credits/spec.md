# Feature Specification: 판독 크레딧

**Feature Branch**: `009-credits` | **Created**: 2026-10-12 | **Issue**: #33

## Requirements
- **FR-001**: 계정마다 가입 시 3크레딧. 결과지 판독 1회에 1크레딧을 호출 전에 차감한다. 잔액 0이면 판독하지 않고 안내한다.
- **FR-002**: 차감 후 실패해도 환불하지 않는다 (2026-10-12 결정; 환불은 결제 기능 #26에서 서버 전용 키로).
- **FR-003**: 업로드 화면과 설정에 남은 크레딧을 보여 준다.
- **FR-004**: 장부(credit_ledger)만 저장하고 결과지 내용은 저장하지 않는다. 쓰기는 RPC로만.

## Constitution Check
I: 횟수만 저장. IV: RLS + security definer RPC, 사용자별 잠금. V: 마이그레이션 1개, 파일 5개.


## 검증
- lint, build 통과 / 운영 DB 적용 후 업로드 화면 잔액, 판독 후 1 감소 확인
