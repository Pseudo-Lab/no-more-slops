"""Tests for check_build.py and count_terms.py with invented fixtures only."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
FIX = HERE / "fixtures"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cb = load("check_build")
ct = load("count_terms")


def run(script, *args):
    proc = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True)
    assert "Traceback" not in proc.stderr
    return proc.returncode, (json.loads(proc.stdout) if proc.stdout else None)


# check_build: functions

def test_unwrap_log_joins_79_char_lines():
    first = "x" * 79
    assert cb.unwrap_log(f"{first}\ntail\nnext") == [first + "tail", "next"]


def test_parse_log_counts_each_warning_kind():
    log = cb.parse_log((FIX / "bad_build/main.log").read_text())
    assert log["overfull"]["count"] == 2
    assert log["overfull"]["items"][0] == {"lines": [7, 7], "pt": 3.47562, "badness": None}
    assert log["overfull"]["items"][1]["lines"] == [120, 120]
    assert log["underfull"]["items"] == [{"lines": [81, 1], "pt": None, "badness": 10000}]
    refs = log["undefined_references"]["items"]
    assert [r["key"] for r in refs] == ["sec:missing",
                                        "fig:a-very-long-label-name-used-to-test-wrapping-x"]
    assert refs[1]["input_line"] == 55
    assert [c["key"] for c in log["undefined_citations"]["items"]] == ["nobody2023", "ghost2024"]
    assert log["h_float_changed"] == {"count": 2, "changed_to": ["ht", "!ht"]}


def test_label_pages_reads_hyperref_and_plain_newlabel():
    labels = cb.label_pages((FIX / "clean_build/main.aux").read_text())
    assert labels == {"sec:end-of-body": "3", "plain": "2"}


@pytest.mark.parametrize("label,limit,ok", [("sec:end-of-body", 4, True),
                                             ("sec:end-of-body", 2, False),
                                             ("missing", 4, False)])
def test_page_check(label, limit, ok):
    result = cb.page_check({"sec:end-of-body": "3"}, label, limit)
    assert result["within_limit"] is ok
    assert result["found"] is (label != "missing")


def test_scan_sources_finds_todo_and_marks_comments():
    src = cb.scan_sources(FIX / "bad_src")
    found = [(i["match"], i["in_comment"]) for i in src["todo"]["items"]
             if i["file"] == "sections/introduction.tex"]
    assert found == [("\\todo", False), ("XXX", False), ("TODO", True)]
    # \newcommand{\todo} is a definition, not a leftover note; only "TODO:" text inside it hits.
    assert [i["match"] for i in src["todo"]["items"] if i["file"] == "main.tex"] == ["TODO"]
    assert src["personal_paths"]["count"] == 0


def test_scan_sources_finds_personal_paths(tmp_path):
    home = "/" + "Users" + "/someone/data"  # built at runtime so the repo holds no such path
    win = "C:" + "\\" + "Users" + "\\someone"
    (tmp_path / "a.tex").write_text(f"see {home}\nsee {win}\nsee ~/notes\nFig.~\\ref{{x}}\n")
    items = cb.scan_sources(tmp_path)["personal_paths"]["items"]
    assert [i["line"] for i in items] == [1, 2, 3]


# check_build: CLI exit codes

def test_cli_clean_build_exits_0():
    code, report = run("check_build.py", FIX / "clean_build", "--page-limit", 4,
                       "--src", FIX / "clean_src")
    assert code == 0 and report["ok"] and report["problems"] == []
    assert report["pages"]["end_page"] == 3


def test_cli_bad_build_exits_1():
    code, report = run("check_build.py", FIX / "bad_build", "--page-limit", 4,
                       "--src", FIX / "bad_src")
    assert code == 1
    assert report["pages"]["end_page"] == 5
    assert set(report["problems"]) == {"page_limit", "overfull", "underfull",
                                       "undefined_references", "undefined_citations",
                                       "h_float_changed", "todo"}


def test_cli_custom_end_label():
    code, report = run("check_build.py", FIX / "bad_build", "--page-limit", 5,
                       "--end-label", "sec:intro")
    assert report["pages"]["end_page"] == 1 and report["pages"]["within_limit"]
    assert "page_limit" not in report["problems"] and code == 1


def test_cli_missing_input_exits_2(tmp_path):
    code, _ = run("check_build.py", tmp_path, "--page-limit", 4)
    assert code == 2


# count_terms: functions

def test_load_expands_inputs_and_drops_comments():
    text = ct.load(FIX / "clean_src/main.tex")
    assert "small benchmark" in text and "Fixture manuscript" not in text


def test_macros_skip_argument_macros():
    table = ct.macros(ct.load(FIX / "bad_src/main.tex"))
    assert "todo" not in table
    assert ct.macros(r"\newcommand{\X}{7}\def\Y{8}") == {"X": "7", "Y": "8"}


def test_count_numbers_expands_macros_and_ignores_keys():
    text = ct.load(FIX / "clean_src/main.tex")
    abstract = ct.expand_macros(ct.section(text, env="abstract"), ct.macros(text))
    assert ct.count_numbers(abstract) == ["42%", "3.5"]


def test_count_sentences_ignores_abbreviations_and_decimals():
    assert ct.count_sentences("We test e.g. agents. It got 3.5 points. Done!") == 3


def test_new_terms_first_use_case_insensitive():
    intro = ct.section(ct.load(FIX / "clean_src/main.tex"), title="Introduction")
    assert ct.new_terms(intro) == ["pressure", "push", "report gap"]


def test_report_flags_out_of_range():
    result = ct.report(FIX / "bad_src/main.tex")
    assert result["abstract"]["numbers"] == 6 and not result["abstract"]["ok"]
    assert result["introduction"]["new_terms"] == 6 and not result["introduction"]["ok"]


# count_terms: CLI exit codes

def test_cli_count_terms_clean_exits_0():
    code, result = run("count_terms.py", FIX / "clean_src")
    assert code == 0 and result["abstract"]["sentences"] == 3


def test_cli_count_terms_bad_exits_1():
    code, result = run("count_terms.py", FIX / "bad_src/main.tex")
    assert code == 1 and not result["ok"]


def test_cli_count_terms_missing_exits_2(tmp_path):
    code, _ = run("count_terms.py", tmp_path / "nope.tex")
    assert code == 2
