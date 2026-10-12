# Feature Specification: 되돌릴 수 없는 동작 확인 팝업

**Feature Branch**: `006-confirm-dialog` | **Created**: 2026-10-12 | **Issue**: #27

## User Story
가족 구성원이 검진 기록 삭제·구성원 삭제·로그아웃·회원 탈퇴를 누르면 바로 실행되지 않고, 무엇이 사라지는지 적힌
확인 팝업에서 한 번 더 확인한 뒤 실행된다.

## Requirements
- **FR-001**: 네 동작 모두 공용 확인 모달(`<dialog>`)을 거친다. 취소·바깥 탭·Esc로 닫힌다.
- **FR-002**: 팝업 제목에 대상(검진일·구성원 이름)을 적고, 되돌릴 수 없음을 설명한다.
- **FR-003**: 탈퇴 페이지의 확인 체크박스는 팝업이 뜨기 전에 검사된다.

## Constitution Check
I–IV 해당 없음. V: 컴포넌트 하나 교체, 호출부 4곳.

## 검증
- lint, build 통과 / 운영 URL에서 네 동작 모두 팝업 확인
