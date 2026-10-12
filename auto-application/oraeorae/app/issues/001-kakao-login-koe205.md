---
issue: https://github.com/Woo-Yeol/family-health/issues/1
title: "카카오 로그인 시 KOE205 (account_email 동의항목 미설정)"
labels: bug, auth
status: done
---

## 현상
카카오로 시작하기를 누르면 카카오 로그인 화면에서 **KOE205** 오류가 나고 로그인이 막힌다.

개발 서버 로그:

```
GET /auth/callback?error=invalid_scope&error_description=Invalid+scope%3A+account_email&next=%2F 307
GET /login?error=1 200
```

## 원인
- Supabase 카카오 provider는 scope를 항상 `account_email profile_image profile_nickname`으로 요청한다.
- 카카오 앱에서 **카카오계정(이메일)** 동의항목이 꺼져 있어 `account_email`이 유효하지 않은 scope로 처리됐다.
- 이메일 동의항목은 **비즈 앱**에서만 켤 수 있는데, 앱이 일반 앱이었다.

## 조치
1. 카카오디벨로퍼스 계정 설정에서 앱 소유자 본인인증
2. [앱] > [일반] > [비즈니스 정보] > **[개인 개발자 비즈 앱 전환]** (사업자등록번호 불필요, 카카오비즈니스 통합 서비스 약관 동의)
3. [카카오 로그인] > [동의항목]에서 **카카오계정(이메일)** 을 필수 동의로 설정 (목적: 로그인 계정 식별). 닉네임·프로필 사진은 선택 동의
4. 앱 아이콘 등록 (`public/app-icon.png`)

## 검증
- [x] 동의 화면에 이메일 항목이 보인다
- [x] 로그인 후 `/start`로 이동한다
- [x] 가족 만들기 후 `families`, `members`, `consents`에 행이 생긴다

## 참고
- 개인 개발자 비즈 앱은 비즈니스 채널(카카오톡 채널)을 연결할 수 없다. 필요해지면 사업자등록 후 일반 비즈 앱으로 전환한다.
- [앱 설정 > 앱 - 카카오디벨로퍼스](https://developers.kakao.com/docs/ko/app-setting/app)
