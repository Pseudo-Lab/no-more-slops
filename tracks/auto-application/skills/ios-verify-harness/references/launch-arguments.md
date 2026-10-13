# DEBUG 실행 인수와 자가 점검 템플릿

SwiftUI 앱 기준이다. 이름과 화면 목록은 앱에 맞게 바꾼다. 세 부분 모두 `#if DEBUG` 안에 있어 Release 빌드에서는 아무 일도 하지 않는다.

## 1. 실행 인수

```swift
import Foundation

/// Debug-only launch arguments, so the app can be driven from the command line
/// (`xcrun simctl launch booted <bundle id> -screen settings`) for screenshots and checks.
/// None of these do anything in Release builds.
enum LaunchArguments {
    /// Forget onboarding/terms state so the first-launch flow runs again.
    static let resetState = has("-resetState")
    /// Skip the terms screen (test devices only).
    static let acceptTerms = has("-acceptTerms")
    /// Open the built-in sample content right away.
    static let openSample = has("-openSample")
    /// Open a screen: `-screen settings|export|history`
    static let screen: String? = value(after: "-screen")
    /// Preselect a tab inside a screen: `-tab tools|adjust`
    static let tab: String? = value(after: "-tab")

    private static func has(_ flag: String) -> Bool {
        #if DEBUG
        return ProcessInfo.processInfo.arguments.contains(flag)
        #else
        return false
        #endif
    }

    private static func value(after flag: String) -> String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: flag), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
}
```

루트 화면에서 한 번 읽어 이동한다. 실제 사용자 흐름과 같은 상태를 거치게 해야(예: 샘플 열기 → 편집 화면) 스크린샷이 실제 화면과 같다.

```swift
.task {
    if LaunchArguments.acceptTerms { appState.termsAccepted = true }
    if LaunchArguments.openSample { router.openEditor(with: .sample, tab: LaunchArguments.tab) }
    if let screen = LaunchArguments.screen { router.open(screen) }   // unknown names do nothing
}
```

`-AppleLanguages "(de)" -AppleLocale de_DE`는 시스템 인수라 따로 만들 필요가 없다.

## 2. 자가 점검 (`-selfCheck`)

```swift
#if DEBUG
import UIKit

/// Deterministic checks of the app's own logic. Runs only with -selfCheck and writes one line per
/// check to Documents/self-check.txt, ending with DONE (scripts/sim_check.sh waits for it).
enum SelfCheck {
    static func runIfRequested() {
        guard ProcessInfo.processInfo.arguments.contains("-selfCheck") else { return }
        Task { @MainActor in
            var lines = ["run: \(Date().ISO8601Format())"]
            func check(_ ok: Bool, _ name: String, _ detail: String = "") {
                lines.append("\(ok ? "PASS" : "FAIL") \(name)\(detail.isEmpty ? "" : " (\(detail))")")
            }
            // Persistence round trip in a throwaway store, never the user's data.
            let defaults = UserDefaults(suiteName: "self-check")!
            defaults.removePersistentDomain(forName: "self-check")
            let store = ItemStore(defaults: defaults)
            check(store.save(name: "One"), "Save an item")
            check(ItemStore(defaults: defaults).items.map(\.name) == ["One"], "Saved items persist")

            // Copy rules in the current language (run once per language with -AppleLanguages).
            let titles = ["Saved items", "Settings"].map { NSLocalizedString($0, comment: "") }
            check(titles.allSatisfy { !$0.hasSuffix(".") && !$0.hasSuffix("。") }, "Titles have no terminal period")

            // Every tool changes the result (catches tools that silently do nothing).
            let input = SampleImage.load()
            for tool in Tool.allCases {
                let difference = meanDifference(input, tool.apply(to: input, strength: 1))
                check(difference > 0.5, "\(tool) changes the image", String(format: "%.2f", difference))
            }

            // Release-relevant identity.
            check(Bundle.main.object(forInfoDictionaryKey: "NSPhotoLibraryAddUsageDescription") != nil, "Photo add permission text exists")

            let passed = lines.filter { $0.hasPrefix("PASS") }.count, failed = lines.filter { $0.hasPrefix("FAIL") }.count
            lines.append("DONE \(passed) passed, \(failed) failed")
            let url = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0].appendingPathComponent("self-check.txt")
            try? lines.joined(separator: "\n").write(to: url, atomically: true, encoding: .utf8)
            print(lines.joined(separator: "\n"))
        }
    }
}
#endif
```

`App`의 `init()`에서 `#if DEBUG SelfCheck.runIfRequested() #endif`로 부른다. 검사는 결정적이어야 한다(고정 입력, 합성 이미지, 임시 저장소). 사용자가 지적한 버그는 고친 뒤 그 버그를 잡는 검사로 남긴다. 예: "추천 보정을 두 번 누르면 원래대로 돌아온다", "프리셋은 얼굴 형태를 바꾸지 않는다".

## 3. 기능별 렌더 (`-auditRenders`)

```swift
#if DEBUG
/// Writes the untouched sample and each tool at full strength to Documents/audit/ for scripts/noop_audit.py.
enum AuditRenders {
    static func runIfRequested() {
        guard ProcessInfo.processInfo.arguments.contains("-auditRenders") else { return }
        Task.detached(priority: .userInitiated) {
            let dir = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0].appendingPathComponent("audit")
            try? FileManager.default.removeItem(at: dir)
            try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
            let input = SampleImage.load()
            try? input.pngData()?.write(to: dir.appendingPathComponent("baseline.png"))
            for tool in Tool.allCases {
                try? tool.apply(to: input, strength: 1).pngData()?.write(to: dir.appendingPathComponent("\(tool).png"))
            }
            try? "done \(Date().ISO8601Format())".write(to: dir.appendingPathComponent("done.txt"), atomically: true, encoding: .utf8)
        }
    }
}
#endif
```

양방향 슬라이더는 `<tool>-neg.png`도 저장한다. 실제 사진 품질은 시뮬레이터보다 실기기나 Mac Catalyst 대상(같은 코드를 Mac에서 실행)에서 실제 사진 여러 장으로 렌더해 본다. 시뮬레이터에는 일부 Vision 기능(예: 사람 마스크, 몸 관절)이 없다.
