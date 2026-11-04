# 실기기 설치와 문제 해결

## 기본 명령

```sh
xcrun devicectl list devices                       # 기기 ID와 상태(available, connected, unavailable)
scripts/device_run.sh -p App.xcodeproj -s App -b com.example.app -d <기기 ID>
```

`device_run.sh`는 빌드(`-allowProvisioningUpdates`로 서명·기기 등록 자동) → `devicectl device install app` → `devicectl device process launch --terminate-existing <bundle> -- <앱 인수>` → `devicectl device copy from --domain-type appDataContainer` 순서로 실행한다. 앱 인수는 `--` 뒤에 둬야 `devicectl`이 자기 옵션으로 읽지 않는다.

## 처음 연결할 때 (사용자가 직접)

1. 케이블로 한 번 연결하고 iPhone에서 "이 컴퓨터를 신뢰"를 누른다.
2. iPhone 설정 › 개인정보 보호 및 보안 › 개발자 모드를 켜고 재시동한다.
3. Xcode › Window › Devices and Simulators에서 기기를 고르고 "Connect via network"를 켜면 다음부터 같은 Wi-Fi에서 케이블 없이 설치된다.
4. Xcode › Settings › Accounts에 개발자 계정이 있어야 서명된다.

## 안 될 때

| 증상 | 해결 |
|---|---|
| 같은 Wi-Fi인데 `unavailable`, ping은 응답함 | 사용자 수준 CoreDevice 프로세스를 재시작한다. `pkill -u "$USER" -f CoreDeviceService; pkill -u "$USER" remotepairingd` 몇 초 뒤 `xcrun devicectl list devices`를 다시 본다. 프로세스는 자동으로 다시 뜨고 터널이 다시 연결된다 |
| 설치는 되는데 실행이 실패(잠김) | iPhone 잠금을 풀고 화면을 켠 채로 다시 실행한다 |
| "신뢰하지 않는 개발자" | iPhone 설정 › 일반 › VPN 및 기기 관리에서 개발자 앱을 신뢰한다 |
| 서명 오류, 프로비저닝 프로파일 없음 | Xcode 계정 로그인 확인, `-allowProvisioningUpdates`로 다시 빌드 |
| 기기가 목록에 없음 | 케이블로 다시 연결해 신뢰·개발자 모드를 확인한다 |
| 회수한 파일이 예전 결과 | 보고서 첫 줄의 실행 시각(`run: …`)을 확인하고, 실행 전에 이전 파일을 지우는 코드를 넣는다 |

## 기기에서만 재는 것

- 성능: `-perfReport` 같은 DEBUG 인수로 분석·렌더·저장 시간을 재서 `Documents/perf.txt`에 쓰고 회수한다. 시뮬레이터 수치는 기기 성능을 대신하지 않는다.
- 화면 캡처: DEBUG 인수로 앱이 자기 창을 PNG로 `Documents`에 저장하게 한 뒤 회수하면 명령줄에서 기기 화면을 받을 수 있다.
- 품질: 카메라·사진 처리·ML 모델 결과는 실제 사진으로 기기에서 본다.
