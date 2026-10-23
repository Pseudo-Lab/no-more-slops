# AUTO blocks and the generator

## Markers

Each marker sits on its own line:

~~~latex
\begin{table}[t]
\centering
% BEGIN AUTO RESULTS
\begin{tabular}{lrr}
...
\end{tabular}
% END AUTO RESULTS
\caption{Call accuracy (\%) on 3,051 examples, one run.}
\label{tab:results}
\end{table}
~~~

In Markdown or HTML use `<!-- BEGIN AUTO RESULTS -->` and `<!-- END AUTO RESULTS -->`.
Names use letters, digits, `_`, `.` and `-`; each appears once per file; blocks do
not nest. `auto_blocks.py` rejects anything else before it writes.

Wrap the smallest generated unit. Keep the float, its placement, the caption
and the label outside the block so the author controls them. A caption that
quotes a result is written text: generate the whole caption, or let
`stale_numbers.py` check it.

## Generator contract

1. **Load** runs from explicit directories, never "the latest". Verify each is
   complete and matches the declared protocol; fail with the run, the field and
   both values.
2. **Compute** every number from records with the paper's denominators. The same
   loaded objects feed every block and the numbers report.
3. **Cross-check** values that appear twice (a method in two tables, a figure
   point and a table cell) and counts that must add up (paired IDs, exclusions).
4. **Format** in one function per block: fixed decimals, `$-$` for minus, an
   explicit `+` on positive differences, intervals as `[lo, hi]`, the best value per
   column bold when the venue uses bold (computed, ties all bold).
5. **Write** all blocks or none: build every block first, then replace them and
   write the file once. Write the numbers report (JSON) with input paths and
   fingerprints next to it.
6. **Never** write outside the blocks.

A minimal Python generator, with `blocks` and `replace` copied from
`scripts/auto_blocks.py` or imported from it:

~~~python
def update_paper(path, contents):  # contents: {block name: LaTeX string}
    text = Path(path).read_text(encoding="utf-8")
    missing = set(contents) - set(blocks(text))
    if missing:
        raise ValueError(f"{path}: missing AUTO blocks {sorted(missing)}")
    for name, content in contents.items():
        text = replace(text, name, content)
    Path(path).write_text(text, encoding="utf-8")
~~~

Without Python, the Makefile can write each block's content to `build/NAME.tex`
and call `auto_blocks.py replace paper/main.tex NAME --from build/NAME.tex`.

## Numbers in prose

Hand-written prose quotes values ("from 63.8% to 74.6%"). After each regeneration,
`stale_numbers.py --before OLD --after NEW README.md` lists quotes of values that
left the blocks. It cannot see derived values; recheck differences, ratios and
words like "highest" or "every run" by hand.

A new paper can generate its prose numbers as macros instead:

~~~latex
% BEGIN AUTO NUMBERS
\newcommand{\AccDirect}{63.8}
\newcommand{\AccJBFC}{74.6}
% END AUTO NUMBERS
...accuracy rises from \AccDirect\% to \AccJBFC\%.
~~~

Do not convert an author's existing prose to macros without asking.

## Checking without writing

- Run the generator on a copy of the paper and `diff` it with the original.
- Or let the generator write block files and run
  `auto_blocks.py check paper/main.tex NAME --from build/NAME.tex` per block; it
  prints a diff and exits 1 when they differ.

A difference means someone edited a block by hand or the records changed.
