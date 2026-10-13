---
name: ios-verify-harness
description: "iOS 앱이 '동작한다'를 말이 아니라 결과로 확인할 때 쓴다. 모든 화면을 DEBUG 실행 인수로 열게 만들고, 앱 안 자가 점검(PASS/FAIL 보고서)을 시뮬레이터에서 언어별로 돌리고, 기능마다 최대 강도 렌더를 원본과 비교해 아무것도 안 바꾸는 기능을 찾고, 실기기에 설치·실행·파일 회수를 한다. '이 기능 다 동작하는지 점검해줘', '내 아이폰에 설치해줘', '왜 설치가 안 돼', 스크린샷 자동화 준비에 사용한다."
---

# iOS 검증 하네스

"구현했다"와 "동작한다"는 다르다. 이 스킬은 앱을 명령줄에서 원하는 화면과 상태로 열고, 결과를 파일로 받아 판정하는 장치를 앱에 붙인다. 화면 이름, 점검 항목, 기기는 작업별 입력값이다.

## 장치 붙이기

[references/launch-arguments.md](references/launch-arguments.md)의 템플릿을 앱에 넣는다. 모두 `#if DEBUG` 안에 두어 Release에는 들어가지 않게 한다.

- **화면 이동 인수:** `-screen <이름>`, `-tab <이름>`, 샘플 데이터 열기, 첫 실행 상태 초기화, 약관 자동 동의. 새 화면을 만들면 인수도 같이 만든다. 스크린샷(app-store-release)과 레이아웃 점검(global-localization)이 이 인수를 쓴다.
- **자가 점검:** `-selfCheck`로 실행하면 앱이 결정적인 검사(데이터 저장·복원, 계산 결과, 문구 규칙, 기능 조합)를 돌리고 `Documents/self-check.txt`에 `PASS`/`FAIL` 한 줄씩, 끝에 `DONE`을 쓴다. 버그를 고칠 때마다 그 버그를 잡는 검사를 하나 더한다.
- **기능별 렌더:** 이미지·오디오·문서처럼 결과물이 있는 앱은 `-auditRenders`로 같은 입력에 기능 하나씩 최대 강도를 적용한 결과를 `Documents/audit/<기능>.png`, 원본을 `baseline.png`로 저장한다.

## 돌리기

1. **시뮬레이터 자가 점검:**
   ```sh
   scripts/sim_check.sh -p App.xcodeproj -s App -b com.example.app -l "en ko de" -a "-selfCheck -acceptTerms"
   ```
   빌드·설치·언어별 실행 뒤 `DONE`을 기다려 FAIL 줄을 보여 준다. 출시 점검 스크립트에 넣는다.
2. **기능 무변화 감사:** 렌더를 꺼내(`xcrun simctl get_app_container booted <bundle> data` 또는 `device_run.sh -f Documents/audit`) 아래를 실행한다.
   ```sh
   python3 scripts/noop_audit.py audit/
   ```
   - NO-OP: 아무것도 안 바뀐 기능. 반드시 원인을 찾는다.
   - WEAK: 바뀌었지만 폰에서 보기 어려운 기능. 비교 이미지(원본 | 결과 | 변화 ×4와 변화 범위 상자)를 열어 보고, 범위 상자가 엉뚱한 곳(팔 도구가 얼굴을 바꿈)이면 그것도 버그로 본다.

   ![무변화 감사 비교 이미지](assets/noop-audit-sample.jpg)

3. **실기기:**
   ```sh
   scripts/device_run.sh -p App.xcodeproj -s App -b com.example.app -d <기기 ID> -a "-perfReport" -f Documents/perf.txt -o out/
   ```
   설치·실행·파일 회수를 한 번에 한다. 연결이 안 되면 [references/device.md](references/device.md)를 본다.

## 판정 원칙

- 시뮬레이터에 없는 능력(카메라, 일부 Vision 기능, Neural Engine 성능, 실제 사진 품질)이 걸린 기능은 실기기나 실제 입력으로 판정한다. 시뮬레이터 통과만으로 "된다"고 하지 않는다.
- 사용자가 "이거 동작해?"라고 물으면 그 기능을 기본 샘플로 실제로 돌려 결과 이미지를 보여 주고, 어떤 신호(관절, 마스크, 랜드마크)를 써서 동작하는지 함께 말한다.
- 회수한 보고서는 실행 시각을 확인한다. 이전 실행의 파일을 새 결과로 착각하기 쉽다.
- 보고할 때는 돌린 명령, 통과·실패 수, 직접 본 이미지를 말한다. 돌리지 못한 검사는 못 돌렸다고 말한다.
