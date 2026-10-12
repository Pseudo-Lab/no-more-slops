# Feature Specification: 개인정보 보호책임자 표기

**Feature Branch**: `002-privacy-officer`
**Created**: 2026-10-10
**Status**: Ready
**Input**: GitHub issue #16 "개인정보 보호책임자 이름 기재"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 이용자가 개인정보 문의처를 안다 (Priority: P1)

이용자는 개인정보처리방침과 모든 화면 하단에서 개인정보 문의를 받는 담당과 연락처를 볼 수 있다.

**Why this priority**: 개인정보보호법 제30조 필수 기재 사항이며, 현재 "운영자 이름 입력 예정"으로 비어 있다.

**Independent Test**: `/privacy`와 하단에 담당 이름과 이메일이 보인다.

**Acceptance Scenarios**:

1. **Given** `/privacy`, **When** 보호책임자 항목을 보면, **Then** "담당 오래오래 개인정보 보호 담당 · 이메일 …"이 보인다.
2. **Given** 아무 공개 화면, **When** 하단을 보면, **Then** "개인정보 문의 오래오래 개인정보 보호 담당 · …"이 보인다.

### Edge Cases

- 유료화(결제) 시작 시 전자상거래법상 대표자 실명 표시 의무가 생겨 실명으로 바꿔야 한다.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 처리방침과 하단에 보호업무 담당 이름과 연락처(이메일)를 표시해야 한다.
- **FR-002**: "입력 예정" 같은 자리표시 문구가 남지 않아야 한다.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 배포 주소의 `/privacy`와 `/login` 하단에 자리표시 문구가 0건이다.

## Assumptions

- 제30조는 "성명 또는 담당 부서의 명칭"과 연락처를 요구하므로 담당 이름으로 충족한다. 1인 운영에서 이 표기가 적절한지는 #19 법률 검토에서 확인한다.
- 운영자가 실명 대신 담당 이름을 선택했다 (2026-10-10).
