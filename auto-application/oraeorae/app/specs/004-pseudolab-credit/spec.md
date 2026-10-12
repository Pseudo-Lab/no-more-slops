# Feature Specification: 가짜연구소 Acknowledgement 표시

**Feature Branch**: `004-pseudolab-credit` | **Created**: 2026-10-12

## 배경
가짜연구소 13기 No-More-Slops 규칙: 개인 명의로 운영하는 서비스도 소개·크레딧에 Acknowledgement를 표시해야 한다
(https://github.com/Pseudo-Lab/no-more-slops README "소유권과 Acknowledgement").

## Requirements
- **FR-001**: 모든 화면의 푸터에 "이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다."를 표시한다.

## Constitution Check
I–IV 해당 없음(데이터·동의·보안 변화 없음). V: 문구 한 줄.

## 검증
- lint, build 통과 / 운영 URL 푸터에 문구 표시
