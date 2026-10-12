# Feature Specification: 서비스 도메인 연결

**Feature Branch**: `003-custom-domain`
**Created**: 2026-10-11
**Status**: Ready
**Input**: GitHub issue #18 "상표 확인과 도메인 확보" — 무료 도메인 `oraeorae.kro.kr` 우선 연결

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 기억하기 쉬운 주소로 들어온다 (Priority: P1)

가족이 `oraeorae.kro.kr`로 들어오고, 카카오톡으로 공유한 링크 미리보기에도 이 주소의 이미지가 쓰인다.

**Why this priority**: `family-health-wheat.vercel.app`은 부모님 세대가 읽고 따라 치기 어렵고 서비스명과 다르다.

**Independent Test**: `https://oraeorae.kro.kr/login`이 열리고 OG 이미지 주소가 새 도메인이다.

**Acceptance Scenarios**:

1. **Given** 브라우저, **When** `oraeorae.kro.kr`에 접속하면, **Then** HTTPS로 랜딩이 열린다.
2. **Given** 랜딩 HTML, **When** `og:image`를 보면, **Then** `https://oraeorae.kro.kr/...`이다.
3. **Given** 기존 주소, **When** 접속하면, **Then** 계속 열린다 (카카오·Supabase 설정 전환 전까지).

### Edge Cases

- 카카오 로그인 후 돌아오는 주소는 Supabase Site URL/Redirect URLs에 새 도메인이 등록돼야 새 도메인으로 돌아온다 (운영자 설정).

## Requirements *(mandatory)*

- **FR-001**: 메타데이터 기준 주소를 새 도메인으로 바꾼다.
- **FR-002**: 기존 vercel.app 주소는 리다이렉트하지 않고 유지한다.

## Success Criteria *(mandatory)*

- **SC-001**: 새 도메인에서 `/login`, `/privacy`가 200이고 `og:image`가 새 도메인을 가리킨다.

## Assumptions

- DNS(A, `_vercel` TXT)는 운영자가 내도메인.한국에 등록했고 Vercel 인증 완료 (2026-10-11).
- 브랜드용 `oraeorae.kr` 구매와 상표 조회는 #18에 남는다.
