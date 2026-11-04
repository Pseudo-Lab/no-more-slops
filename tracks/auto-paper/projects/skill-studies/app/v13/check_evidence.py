"""Read-only linkage of bundled result summaries/figure receipt to the document build."""
import argparse
import json
from pathlib import Path

import typeset as t


def verify(inputs, out):
    inputs = Path(inputs).resolve()
    documents = t.verify(inputs, out)
    binding = json.loads((inputs / "EVIDENCE_BINDINGS.json").read_text(encoding="utf8"))
    t.require(binding["schema"] == "nms_v13_bundled_evidence_v1", "invalid evidence binding")
    t.require(t.check_record(binding["publication"]) == Path(out).resolve() / "PUBLICATION.json", "evidence refers to a different publication")
    t.require(t.check_record(binding["checker"]) == Path(__file__).resolve(), "evidence checker identity changed")
    receipt = json.loads(t.check_record(binding["figure_receipt"]).read_text(encoding="utf8"))
    t.require(receipt["schema"] == "conference_figures_v13" and receipt["new_experiments"] == receipt["model_api_calls"] == 0, "figure receipt scope differs")
    for key in t.PROJECTS:
        source = t.check_record(binding["summaries"][key])
        t.require(source == inputs / "evidence" / (key + "-results.json"), "unexpected summary path")
        t.require(any(row["sha256"] == t.sha(source) for row in receipt["sources"]), "summary hash not linked by original figure receipt")
        figures = receipt["projects"][key]
        t.require(len(figures) == 3, "expected three figure records")
        for figure in figures:
            path = inputs / "figures" / key / (figure["id"] + ".svg")
            t.require(t.sha(path) == figure["svg_sha256"], "SVG does not match original figure receipt")
    return {"ok": True, "document_projects": len(documents["projects"]), "bundled_result_summaries": 3,
            "original_figure_source_records": len(receipt["sources"]), "verified_svg_hashes": 9,
            "new_model_calls": 0, "scope": "Copied frozen summaries and original figure-record hash links; not raw-row replay, figure regeneration or experiment reproduction. Two earlier source records in the original figure receipt remain unbundled."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=t.DEFAULT_INPUTS)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.inputs, args.out), ensure_ascii=False, indent=2))
