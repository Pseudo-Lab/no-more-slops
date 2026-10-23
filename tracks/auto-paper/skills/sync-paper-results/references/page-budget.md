# Fitting a page budget

Know what the venue counts: the body pages before the references, whether the
references, appendix or checklist count, whether the references must start on a
new page, and the total limit.

## Measure

After every build:

~~~sh
python3 scripts/check_layout.py paper/main.pdf --body-pages 4 --max-pages 6 \
    --log paper/main.log --sections Abstract Introduction Conclusion
~~~

It reports the page where the references start; text read before the references
heading on the first page after the body (the body spilled over); missing
headings; `??`; overfull boxes, undefined references or citations, missing
characters and "rerun" warnings in the log (`--allow overfull` accepts a reviewed
one); and Type 3 fonts. A shorter body is not a problem.

Then look at the pages themselves (`pdftoppm -r 60 -png paper/main.pdf /tmp/page`):
floats drifting to the end, a table wider than its column, a lone line at the
top of a page.

## Cut words, not layout

Cheapest first:

1. Sentences that repeat a table. Keep the number that carries the claim; the
   table holds the rest.
2. Captions. Say what is shown and how to read it; state method details once in
   the text, not in every caption.
3. Hedges and signposts ("It is worth noting that", "In this section, we").
4. Paragraphs whose last line holds one or two words; a short rewording saves the
   whole line.
5. Details already in the repository or an appendix. Ask before moving content
   out of the body.

Allowed layout changes: float placement (`[t]`, moving a float's source near its
first mention) and figure size, as long as figure text stays readable.

Never: shrink fonts, margins, column separation or line spacing; add negative
`\vspace`; set tables in a smaller font than the template uses; scale text
until it is unreadable; drop a required section; or touch frozen or approved
text without asking.

## Iterate

Change, build, check. Near the boundary make one cut at a time: float placement
makes page breaks jumpy, so a small cut can pull a figure back a page, and a
small addition can push one forward. Under budget, do not pad.

## Record

In the validation log: page count, where the references start, the
`check_layout.py` output, and which passages were shortened, so the author can
review the cuts.
