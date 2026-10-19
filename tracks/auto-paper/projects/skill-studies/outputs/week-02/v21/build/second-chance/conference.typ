#let research-paper(title: [], body) = {
  set document(title: title, keywords: ("research methodology", "measurement validity", "reproducibility", "layout revision v21", "research content v21"))
  set page(paper: "a4", margin: (x: 24mm, y: 22mm), numbering: "1", number-align: center)
  set text(font: "New Computer Modern", size: 10.5pt, lang: "en", fill: black)
  set par(justify: true, leading: 0.5em, spacing: 0.6em)
  set heading(numbering: "1.1")
  show heading.where(level: 1): set text(size: 13pt, weight: "bold")
  show heading.where(level: 2): set text(size: 11pt, weight: "bold")
  show heading: set block(above: 0.8em, below: 0.35em)
  set math.equation(numbering: "(1)", number-align: right)
  show math.equation: set text(font: "New Computer Modern Math")
  set figure(gap: 5pt)
  show figure.where(kind: table): set block(breakable: true)
  show figure.caption: set text(size: 9pt)
  body
}

#let title-block(title, status) = block(width: 100%, below: 7pt)[
  #set par(justify: false)
  #align(center)[#text(size: 18pt, weight: "bold", title)
  #v(5pt)
  #text(size: 9pt)[Research Forge · 19 October 2026 · Layout v21 · Research content v21]
  #v(3pt)
  #text(size: 8.5pt, status)]
]

// Source clipping must be corrected in the SVG; contain fitting cannot restore discarded artists.
#let figure-image(path, height, alt) = block(width: 100%, inset: (x: 0pt, y: 3pt))[
  #image(path, width: 100%, height: height, fit: "contain", alt: alt)
]

#let abstract-block(body) = block(inset: (x: 6mm), below: 8pt)[
  #set text(size: 10pt)
  #set par(leading: 0.4em)
  #align(center)[*Abstract*]
  #v(2pt)#body
]

#let result-table(headers, rows, caption) = figure({
  set text(size: 9pt)
  set par(justify: false, leading: 0.3em)
  table(columns: headers.len(), stroke: none, inset: (x: 4pt, y: 3pt),
    table.hline(stroke: 0.7pt), table.header(..headers.map(strong)),
    table.hline(stroke: 0.4pt), ..rows.flatten(), table.hline(stroke: 0.7pt))
}, kind: table, caption: caption)

#let method-algorithm(lines, caption) = figure(block(stroke: 0.4pt, inset: 7pt)[
  #set text(size: 9.2pt)
  #set par(justify: false, leading: 0.3em, spacing: 0.3em)
  #for line in lines { [#line #parbreak()] }
], kind: "algorithm", supplement: [Algorithm], caption: caption)

#let bibliography-entry(number, body, url) = block(below: 3pt)[
  #set text(size: 9pt)
  #set par(justify: false, leading: 0.35em)
  #grid(columns: (18pt, 1fr), gutter: 3pt, [\[#number\]], [#link(url)[#body]])
]
