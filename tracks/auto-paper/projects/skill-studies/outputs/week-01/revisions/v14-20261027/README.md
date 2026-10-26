# ProbeFlow — public layout correction

[Paper](paper.pdf) · [Supplement](supplement.pdf) · [한국어 해설](explainer.pdf) · [Offline HTML](study.html)

This is a publication copy of the completed, corrected conference narrative dated 26 October 2026. It retains the acknowledgement below, widens the W50 execution and seven-condition comparison table label columns and extends two historical SVG canvases so their complete y-axis titles are visible. It retains the complete earlier scientific content, historical material, figures, tables, three numbered algorithms and negative results. It does not report the separate unfinished follow-up study.

> This work was created as part of the No-More-Slops group activities at Pseudo Lab.

The main scientific claims remain limited: exact-objective gain is `0/no_gain`; CPU and traced-Python-peak wins over strong DP occur in `2/7` constructed conditions; the separate coherent acquisition estimator regresses or ties and has `0` independent final participants. The certificate applies to the stated finite model. This is custom Typst, not an official conference template or evidence of venue acceptance. See [claim status](CLAIM_STATUS.json) and the [six-area scope](METHOD_SCOPE.json).

The [canonical source](source.DOCUMENT.json), three `.typ` files, local SVG assets and inherited coverage/erratum records accompany the PDFs. [Preservation](PRESERVATION.json) maps all 216 original historical sections and every section of the corrected input. [Editorial delta](EDITORIAL_DELTA.json) records these four presentation changes and exact source/data preservation, with the predecessor acknowledgement delta retained by hash. [Document identity](DOCUMENT_IDENTITY.json) binds source, PDF, context, figure and algorithm identities. No raw participant dataset, model weights, credentials, private task logs or third-party article HTML is included.

With an already installed Typst executable and the fonts declared in the supplied Typst sources, run:

```sh
python -B build.py --out ../probeflow-rebuilt
```

The output directory must be new. This command verifies the public input hashes and reuses the included existing compile helper; it downloads nothing and calls no model. `BUILD.json` records the actual local build engine, source and PDF identities. Typst embeds compilation-time metadata, so PDF byte hashes can differ even when every page's text and rendering match. Font or engine differences may also change pagination or bytes. Rebuilding scientific experiments, obtaining external papers and installing dependencies are outside this document-copy operation.

Only files named in [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json), plus that manifest itself, are intended for publication. The manifest does not hash itself; its delivery hash belongs to the separate internal freeze receipt. Parent integration performs a fresh, different exact-copy review before Git delivery; the earlier accepted review covered the preceding corrected edition. [License scope and attribution](LICENSE_SCOPE.md) distinguish repository contributions from cited external work. Historical public editions remain preserved in their existing locations.
