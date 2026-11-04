#let scholarly-paper(title: [], body) = {
  set document(title: title, keywords: ("research design", "week 1", "pre-experimental"))
  set page(paper: "a4", margin: (x: 24mm, y: 22mm), numbering: "1", number-align: center)
  set text(font: "New Computer Modern", size: 11pt, lang: "en", fill: black)
  set par(justify: true, leading: 0.55em, spacing: 0.65em)
  set heading(numbering: none)
  show heading.where(level: 1): set text(size: 13.5pt, weight: "bold")
  show heading.where(level: 2): set text(size: 11pt, weight: "bold")
  show heading: set block(above: 0.72em, below: 0.34em)
  set math.equation(numbering: "(1)", number-align: right)
  show math.equation: set text(font: "New Computer Modern Math", size: 11pt)
  set figure(gap: 4pt)
  show figure.caption: set text(size: 8.3pt)
  body
}

#let title-block(title, status) = block(width: 100%, below: 7pt)[
  #set par(justify: false)
  #align(center)[#text(size: 18pt, weight: "bold", title)
  #v(4pt)
  #text(size: 8.6pt)[12 October 2026 · Week 1 research-design draft]
  #v(3pt)
  #text(size: 8pt, status)]
]

#let abstract-block(body) = block(inset: (x: 6mm), above: 0pt, below: 7pt)[
  #set text(size: 10pt)
  #set par(leading: 0.36em, spacing: 0.35em)
  #align(center)[*Abstract*]
  #v(2pt)
  #body
]

#let planned-table(headers, rows, caption) = figure({
  set text(size: 8.6pt)
  set par(justify: false, leading: 0.35em)
  table(columns: headers.len(), stroke: none, inset: (x: 4pt, y: 3pt),
    table.hline(stroke: 0.7pt), table.header(..headers.map(strong)),
    table.hline(stroke: 0.4pt), ..rows.flatten(), table.hline(stroke: 0.7pt))
}, kind: table, caption: caption)

#let algorithm-block(lines, caption) = figure(block(stroke: 0.4pt, inset: 6pt)[
  #set text(size: 9pt)
  #set par(justify: false, leading: 0.34em, spacing: 0.3em)
  #for line in lines { [#line #parbreak()] }
], caption: caption)

#let bibliography-entry(number, body, url) = block(above: 0pt, below: 3pt)[
  #set text(size: 9.2pt)
  #set par(justify: false, leading: 0.35em)
  #grid(columns: (16pt, 1fr), gutter: 2pt, [\[#number\]], [#link(url)[#body]])
]
