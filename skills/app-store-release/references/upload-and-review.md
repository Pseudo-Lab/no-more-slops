# 빌드 업로드와 심사 제출

## 업로드 전에

- 빌드 번호(`CURRENT_PROJECT_VERSION`)가 이전에 올린 빌드보다 커야 한다. 버전(`MARKETING_VERSION`)은 App Store Connect의 버전 페이지와 같아야 한다.
- Info.plist에 `ITSAppUsesNonExemptEncryption` = NO가 있으면 빌드마다 수출 규정 질문이 나오지 않는다(표준 HTTPS 외 암호화를 쓰지 않을 때).
- Release에 DEBUG 전용 코드(실행 인수, 자가 점검)가 들어가지 않는지 확인한다(`#if DEBUG`).
- App Store용 서명에는 Apple 계정이나 App Store Connect API 키가 필요하다. 이 Mac의 Xcode에 계정이 없으면 개발용 인증서만 있어서 내보내기가 `No Accounts` / `No profiles for '<번들 ID>' were found`로 멈춘다.

## Xcode 계정 로그인 (사용자가 직접)

비밀번호와 2단계 인증이 필요하므로 에이전트가 대신할 수 없다. 사용자에게 이렇게 안내한다.

1. Xcode를 연다.
2. 화면 맨 위 메뉴 막대의 **Xcode › Settings…**(⌘,)를 누르고 **Accounts** 탭으로 간다.
3. **그 설정 창의** 왼쪽 아래 **+** 를 누르고 **Apple Account**를 고른다. Xcode 메인 창 왼쪽 파일 목록 아래의 +는 파일 추가 메뉴이니 헷갈리지 않게 짚어 준다.
4. 개발자 계정으로 로그인하고 2단계 인증을 마친다. 오른쪽 Team 목록에 팀이 보이면 끝이다.

로그인 여부는 `defaults read com.apple.dt.Xcode DVTDeveloperAccountManagerAppleIDLists`에 `identifier`가 있는지로 확인한다.

계정 대신 API 키를 쓰려면: App Store Connect › 사용자 및 액세스 › 통합 › App Store Connect API › 팀 키에서 키를 만들고(관리자 권한), `.p8` 파일(한 번만 받을 수 있음), Key ID, Issuer ID를 받는다. 키 파일은 저장소에 넣지 않는다.

## 업로드

사용자가 업로드를 요청했을 때 실행한다.

```sh
scripts/upload_build.sh -p App.xcodeproj -s App -t TEAM_ID -o build/app-store
# API 키: -k ~/keys/AuthKey_XXXX.p8 -i KEY_ID -u ISSUER_ID
# 명령만 보기: -n
```

Release 아카이브 → ExportOptions(`method` app-store-connect, `destination` upload, 자동 서명) → `xcodebuild -exportArchive -allowProvisioningUpdates` 순서다. 첫 업로드 때 배포 인증서와 App Store 프로비저닝 프로파일이 자동으로 만들어진다. 끝에 `Upload succeeded`가 나오면 성공이다. 아카이브만 미리 만들어 두면 로그인 직후 바로 올릴 수 있다.

## 처리와 빌드 선택

- 처리에는 보통 10~30분, 길면 1시간쯤 걸린다. 끝나면 개발자 계정 이메일로 알림이 온다. TestFlight 탭의 iOS 빌드 목록에서 "처리 중" 상태를 볼 수 있다.
- "ITMS-"로 시작하는 문제 메일이 오면 내용을 그대로 받아 고치고, 빌드 번호를 올려 다시 올린다.
- 버전 페이지의 빌드 칸 › 빌드 추가 › 해당 빌드 › 완료. 빌드 하나에 앱이 지원하는 모든 언어가 들어 있으므로 언어별로 올리거나 고르지 않는다.

## 심사 제출

1. 버전 페이지 위쪽에 경고(빈 필수 칸)가 없는지 본다. 언어를 하나씩 바꿔 가며 스크린샷과 URL이 들어갔는지 확인한다.
2. 저장 › 심사에 추가 › 심사를 위해 제출. 수출 규정이나 콘텐츠 권한 질문이 나오면 [app-store-connect.md](app-store-connect.md)의 답을 쓴다.
3. 상태는 심사 대기 중 → 심사 중 → (수동 출시면) 개발자 출시 대기 중 순서로 바뀐다. 보통 하루 이틀 걸린다.
4. 거절되면 App Store Connect의 메시지(앱 심사 › 메시지)를 그대로 받아 사유별로 고친다. 메타데이터만의 문제면 빌드 없이 고쳐 다시 제출할 수 있다. 앱을 고쳤으면 빌드 번호를 올려 새로 올린다.
