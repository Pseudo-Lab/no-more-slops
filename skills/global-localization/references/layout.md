# 긴 언어에서 깨지지 않는 레이아웃

## 어디서 깨지나

- 독일어·프랑스어·스페인어·포르투갈어는 영어보다 20~40% 길다. 베트남어·인도네시아어도 버튼·탭 이름이 길어진다.
- 태국어·베트남어는 위아래 성조 부호 때문에 줄 높이가 더 필요하다. 줄 간격을 고정하면 부호가 잘린다.
- 한국어·일본어·중국어는 짧지만 줄바꿈 위치가 어색해질 수 있다. 웹 제목에는 `word-break: keep-all`(한국어)과 `text-wrap: balance`를 쓴다.
- 가장 잘 깨지는 곳: 가로로 나란한 탭·칩·세그먼트, 고정 너비 버튼, 두 단어 이상인 짧은 라벨, 숫자와 단위가 붙은 라벨, 내비게이션 제목 옆 버튼.

## 확인 방법

1. 모든 화면을 DEBUG 실행 인수로 열 수 있게 한다(ios-verify-harness 스킬).
2. 지원하는 가장 작은 기기와 스토어 스크린샷 기기 모두에서, 언어별로 같은 화면을 찍는다.
   ```sh
   xcrun simctl launch booted <bundle id> -AppleLanguages "(de)" -AppleLocale de_DE -screen settings
   ```
   app-store-release 스킬의 `capture_screenshots.py`를 쓰면 모든 언어를 한 번에 찍는다.
3. 아직 번역이 없으면 의사 언어로 먼저 본다. 실행 인수 `-NSDoubleLocalizedStrings YES`는 모든 문자열을 두 배로 늘린다. Xcode 스킴 › Run › Options › App Language에서 Double-Length·Right-to-Left·Accented Pseudolanguage도 고를 수 있다.
4. 찍은 화면을 언어별로 나란히 놓고 겹침, 잘림, 한쪽으로 쏠린 정렬, 말줄임표를 찾는다. 가장 큰 Dynamic Type 크기도 한 번 본다.

## SwiftUI에서 고치는 법

- 고정 너비(`frame(width:)`)를 텍스트에 걸지 않는다. 버튼 라벨은 두 줄을 허용하고(`.fixedSize(horizontal: false, vertical: true)`), `minimumScaleFactor`는 숫자처럼 짧은 값에만 쓴다.
- 가로로 나란한 탭은 "다 들어가면 펼치고, 안 들어가면 가로 스크롤"로 만든다. `ViewThatFits`는 자식의 이상적 크기가 들어가는 첫 번째 것을 고른다. 칸을 고르게 나누는 레이아웃은 이상적 너비를 "모든 단어 너비의 합 + 간격"으로 알려 줘야 긴 언어에서 스크롤로 넘어간다.

```swift
var body: some View {
    // Spread across the width while every word fits, otherwise a scrolling row.
    ViewThatFits(in: .horizontal) {
        TabCells(gap: 14) { tabs(fill: true) }
        ScrollView(.horizontal, showsIndicators: false) { HStack(spacing: 22) { tabs(fill: false) } }
            .fixedSize(horizontal: false, vertical: true)
    }
}

/// Equal cells when the widest word fits one, otherwise each word plus an equal share of the spare width.
/// Its ideal width is the sum of the words, so ViewThatFits falls back to scrolling when they don't fit.
struct TabCells: Layout {
    var gap: CGFloat = 0
    private func widths(_ subviews: Subviews) -> [CGFloat] { subviews.map { $0.sizeThatFits(.unspecified).width } }
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let need = widths(subviews).reduce(0, +) + gap * CGFloat(subviews.count)
        let width = proposal.width.map { $0.isFinite ? max($0, need) : need } ?? need
        return CGSize(width: width, height: subviews.map { $0.sizeThatFits(.unspecified).height }.max() ?? 0)
    }
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let words = widths(subviews), count = CGFloat(max(1, subviews.count))
        let equal = bounds.width / count
        let spare = max(0, bounds.width - words.reduce(0, +)) / count
        var x = bounds.minX
        for (subview, word) in zip(subviews, words) {
            let cell = (words.max() ?? 0) + gap <= equal ? equal : word + spare
            subview.place(at: CGPoint(x: x + cell / 2, y: bounds.midY), anchor: .center,
                          proposal: ProposedViewSize(width: cell, height: bounds.height))
            x += cell
        }
    }
}
```

`tabs(fill:)`는 각 탭 라벨을 `.lineLimit(1)`로 두고, `fill`일 때만 `.frame(maxWidth: .infinity)`를 준다. 가장 넓은 단어 × 개수로 이상적 너비를 계산하면 너무 일찍 스크롤로 넘어가고 탭이 왼쪽으로 쏠린다(일본어 편집 탭에서 겪은 문제).

- 문장은 조각을 이어 붙이지 않는다. 언어마다 어순이 다르므로 `String(localized: "\(count) photos saved")`처럼 문장 전체를 한 키로 두고, 수량은 카탈로그의 복수형 변형으로 처리한다.
- 아이콘 옆 라벨이 길어지면 아이콘을 위로 올리는 `ViewThatFits` 대안을 둔다.
