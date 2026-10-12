# Feature Specification: 카카오 계정 정보 표시

**Feature Branch**: `008-kakao-profile` | **Created**: 2026-10-12 | **Issue**: #31

## Requirements
- **FR-001**: 설정에 "카카오 계정" 카드 — 프로필 사진, 닉네임, 이메일. 세션의 user_metadata를 요청마다 읽고 저장하지 않는다.
- **FR-002**: 가족 시작·참여의 "가족에게 보일 이름" 기본값은 카카오 닉네임 (수정 가능).

## Constitution Check
I: 새 저장 없음. II: 처리방침의 회원 정보 항목(이메일·닉네임·프로필 사진)과 같음. V: 파일 5개.

## 검증
- lint, build 통과 / 운영 URL 설정 화면 확인
