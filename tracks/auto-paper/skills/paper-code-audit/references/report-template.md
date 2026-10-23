# Audit report template

~~~markdown
## Summary
- Manuscript: <path, commit>; code: <commit>; records: <run directories>
- Verified: <n> items; findings: <n> (high <n>, medium <n>, low <n>); not verifiable: <n>

## Findings
| # | Severity | Location | Paper says | Evidence | Proposed fix |
| --- | --- | --- | --- | --- | --- |
| 1 | High | §4.4, line 301 | "raises accuracy in every run" | run 3: −0.2 (records, `make report`) | "in two of three runs" |

## Verified without findings
- <item>: <how it was checked>

## Not verified
- <item>: <why, what would verify it>

## Commands run
- `<command>` → <result>
~~~

Severity: **High** wrong number, wrong claim or method mismatch; **Medium**
undocumented deviation or missing caveat; **Low** ambiguity, inconsistency in
naming or style.
