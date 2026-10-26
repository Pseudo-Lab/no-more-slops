# Dataset and template attribution

## Public benchmark figure

`paper-source/figures/open100_examples.png` and Figure 2 in `paper.pdf` contain public PID2Graph/OPEN100 raster crops with evaluation overlays. Source: Jan Marius Stürmer, Marius Graumann, Tobias Koch and DLR, [PID2Graph release](https://zenodo.org/records/14803338), DOI [10.5281/zenodo.14803338](https://doi.org/10.5281/zenodo.14803338). Original OPEN100 drawings are provided by the [Energy Impact Center OPEN100 project](https://www.open-100.com/).

The dataset release and these adapted figure assets are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). This license continues to apply to the reproduced and adapted dataset material; the repository's default license does not replace it.

Changes: original crops were resized for presentation and annotated with captions, reference boxes and annotation-node center polylines, plus saved prediction boxes and routes. The source crop pixels were not edited. Reference overlays were used only for evaluation, never as extraction inputs. `benchmark-results.json` records source hashes, native crop coordinates, endpoint references and the deterministic selection rule. The correct pair denotes reference agreement under this adapted evaluator, not improvement over another revision.

Cite: Jan Marius Stürmer, Marius Graumann and Tobias Koch. *From Engineering Diagrams to Graphs: Digitizing P&IDs with Transformers*. DSAA 2025. DOI [10.1109/DSAA65442.2025.11248012](https://doi.org/10.1109/DSAA65442.2025.11248012).

The benchmark configuration used separate public synthetic plans 0 and 2 as legend sources. The API source bundles losslessly converted PNG versions of those plans, a derived equipment-crop panel and legend descriptions under `../../app/cad_api/resources/`; their selection, original hashes and modifications are recorded in the resource attribution and manifest files there. These images retain CC BY-SA 4.0. Synthetic symbol credit in the original release: Copyright 2023 Steven Baltakatei Sandoval, [baltakatei.com](https://baltakatei.com/), CC BY-SA 4.0. No private drawing, private crop or private legend is included.

## Framework figure and paper draft

Figure 1 (`paper-source/figures/framework.tex`) is an editable implementation schematic by the manuscript authors. It is not a screenshot or a benchmark prediction. The manuscript is credited to Minhyeong Yu and Seunghyun Lee, Enhans. `paper.pdf` is an unchanged four-page working draft; its WWW 2027 formatting header is not a conference acceptance or publication claim.

## ACM template files

The bundled `paper-source/acmart.cls` and original `paper-source/template-source/acmart.dtx` are copyrighted 2016–2026 by the Association for Computing Machinery and distributed under the LaTeX Project Public License, version 1.3 or later. The full license is preserved in [paper-source/template-source/LICENSE](paper-source/template-source/LICENSE). The original `.dtx` source and `.ins` installer are included with the unchanged generated class, as required by its distribution notice. Current maintainer listed in the source: Boris Veytsman.

`paper-source/ACM-Reference-Format.bst` identifies Nelson H. F. Beebe, Boris Veytsman and Gerald Murray as authors and declares its license as public domain. Its original notice is preserved. These third-party licenses and notices are retained separately from the repository's default license.
