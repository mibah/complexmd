import re

import pytest

from complexmd import checker
from complexmd.checker import check_file, check_path, check_text


def codes(issues):
    return [i.code for i in issues]


def all_codes(report):
    return codes(report.errors) + codes(report.warnings)


def replace_once(text: str, old: str, new: str) -> str:
    assert old in text, old
    return text.replace(old, new, 1)


def test_valid_contract_has_no_findings(valid_contract):
    report = check_text(valid_contract)
    assert report.ok
    assert all_codes(report) == []
    assert report.contract_version == "0.1.0"
    assert report.conformance == {p: "planned" for p in checker.PRINCIPLES}


# --- CX001 -------------------------------------------------------------------------------------


def test_cx001_missing_file(tmp_path):
    report = check_file(tmp_path / "COMPLEX.md")
    assert codes(report.errors) == ["CX001"]


def test_cx001_not_utf8(tmp_path):
    f = tmp_path / "COMPLEX.md"
    f.write_bytes(b"# COMPLEX.md\n\xff\xfe\x00")
    assert codes(check_file(f).errors) == ["CX001"]


def test_cx001_absent_for_readable_file(tmp_path, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract, encoding="utf-8")
    assert "CX001" not in all_codes(check_file(f))


# --- CX010 / CX011 / CX012 -----------------------------------------------------------------------


@pytest.mark.parametrize("section", checker.REQUIRED_SECTIONS)
def test_cx010_each_required_section(valid_contract, section):
    text = replace_once(valid_contract, f"## {section}\n", f"## Renamed {section}\n")
    assert "CX010" in codes(check_text(text).errors)


def test_cx010_absent_when_complete(valid_contract):
    assert "CX010" not in all_codes(check_text(valid_contract))


def test_cx010_is_case_and_space_insensitive(valid_contract):
    text = replace_once(valid_contract, "## Discover\n", "##   DISCOVER   \n")
    assert "CX010" not in all_codes(check_text(text))


@pytest.mark.parametrize("section", checker.RECOMMENDED_SECTIONS)
def test_cx011_each_recommended_section(valid_contract, section):
    text = replace_once(valid_contract, f"## {section}\n", f"## Renamed {section}\n")
    report = check_text(text)
    assert "CX011" in codes(report.warnings)
    assert report.ok


def test_cx011_absent_in_full_template(valid_contract):
    assert "CX011" not in all_codes(check_text(valid_contract))


def test_cx012_duplicate_section(valid_contract):
    report = check_text(valid_contract + "\n## Run\n\nAgain.\n")
    assert "CX012" in codes(report.warnings)


def test_cx012_absent_without_duplicates(valid_contract):
    assert "CX012" not in all_codes(check_text(valid_contract))


def test_headings_in_code_blocks_are_ignored(valid_contract):
    text = replace_once(valid_contract, "## Discover\n", "## Elsewhere\n")
    text += "\n```markdown\n## Discover\n```\n"
    assert "CX010" in codes(check_text(text).errors)


def test_header_lines_in_code_blocks_are_ignored(valid_contract):
    text = replace_once(valid_contract, "**System:** Demo model\n", "")
    text += "\n```\n**System:** Hidden\n```\n"
    assert "CX020" in codes(check_text(text).errors)


# --- CX020 / CX021 / CX022 -----------------------------------------------------------------------


def test_cx020_missing_and_empty(valid_contract):
    assert "CX020" in codes(check_text(replace_once(valid_contract, "**System:** Demo model\n", "")).errors)
    empty = replace_once(valid_contract, "**System:** Demo model", "**System:**   ")
    assert "CX020" in codes(check_text(empty).errors)


@pytest.mark.parametrize("bad", ["1.0", "v1.0.0", "one", "1.0.0-rc1", ""])
def test_cx021_invalid_version(valid_contract, bad):
    text = replace_once(valid_contract, "**Contract version:** 0.1.0", f"**Contract version:** {bad}")
    report = check_text(text)
    assert "CX021" in codes(report.errors)
    assert report.contract_version is None


def test_cx021_missing(valid_contract):
    text = replace_once(valid_contract, "**Contract version:** 0.1.0\n", "")
    assert "CX021" in codes(check_text(text).errors)


@pytest.mark.parametrize("good", ["not yet", "2026-11-19", "2024-02-29"])
def test_cx022_valid(valid_contract, good):
    text = replace_once(valid_contract, "**Last reviewed:** not yet", f"**Last reviewed:** {good}")
    assert "CX022" not in all_codes(check_text(text))


@pytest.mark.parametrize("bad", ["2026-13-01", "2026-02-30", "2025-02-29", "yesterday", "", "2026-1-1"])
def test_cx022_invalid(valid_contract, bad):
    text = replace_once(valid_contract, "**Last reviewed:** not yet", f"**Last reviewed:** {bad}")
    assert "CX022" in codes(check_text(text).errors)


def test_cx022_missing(valid_contract):
    text = replace_once(valid_contract, "**Last reviewed:** not yet\n", "")
    assert "CX022" in codes(check_text(text).errors)


# --- Conformance: CX030 to CX034 -----------------------------------------------------------------


def _drop_table(text: str) -> str:
    return re.sub(r"^\|.*\n", "", text, flags=re.MULTILINE)


def test_cx030_no_table(valid_contract):
    text = _drop_table(valid_contract)
    assert "CX030" in codes(check_text(text).errors)


def test_cx030_absent_with_table(valid_contract):
    assert "CX030" not in all_codes(check_text(valid_contract))


def test_cx031_missing_principle(valid_contract):
    text = replace_once(valid_contract, "| Statelessness | planned | |\n", "")
    report = check_text(text)
    assert "CX031" in codes(report.errors)
    assert "Statelessness" in report.errors[0].message


def test_cx031_unknown_row(valid_contract):
    text = replace_once(
        valid_contract, "| Composability | planned | |\n", "| Composability | planned | |\n| Magic | planned | |\n"
    )
    assert "CX031" in codes(check_text(text).errors)


def test_cx031_duplicate_row(valid_contract):
    row = "| Statelessness | planned | |\n"
    text = replace_once(valid_contract, row, row + row)
    assert "CX031" in codes(check_text(text).errors)


@pytest.mark.parametrize(
    "variant",
    ["Human–Agent parity", "Human—Agent parity", "HUMAN-AGENT PARITY", "human-agent  parity"],
)
def test_cx031_accepts_dash_and_case_variants(valid_contract, variant):
    text = replace_once(valid_contract, "| Human-Agent parity |", f"| {variant} |")
    assert "CX031" not in all_codes(check_text(text))


def test_cx031_ignores_spaces_around_slash(valid_contract):
    text = replace_once(valid_contract, "| Discoverability/Introspection |", "| Discoverability / Introspection |")
    assert "CX031" not in all_codes(check_text(text))


def test_cx032_invalid_status(valid_contract):
    text = replace_once(valid_contract, "| Statelessness | planned |", "| Statelessness | done |")
    assert "CX032" in codes(check_text(text).errors)


@pytest.mark.parametrize("status", checker.STATUSES)
def test_cx032_valid_statuses(valid_contract, status):
    text = replace_once(valid_contract, "| Statelessness | planned | |", f"| Statelessness | {status} | because |")
    assert "CX032" not in all_codes(check_text(text))


def test_cx033_not_applicable_needs_reason(valid_contract):
    bad = replace_once(valid_contract, "| Statelessness | planned | |", "| Statelessness | not-applicable | |")
    assert "CX033" in codes(check_text(bad).errors)
    good = replace_once(
        valid_contract, "| Statelessness | planned | |", "| Statelessness | not-applicable | batch tool |"
    )
    assert "CX033" not in all_codes(check_text(good))


def test_cx034_implemented_without_how(valid_contract):
    bad = replace_once(valid_contract, "| Statelessness | planned | |", "| Statelessness | implemented | |")
    report = check_text(bad)
    assert "CX034" in codes(report.warnings)
    assert report.ok
    good = replace_once(
        valid_contract, "| Statelessness | planned | |", "| Statelessness | implemented | file-only CLI |"
    )
    assert "CX034" not in all_codes(check_text(good))


# --- Revision log: CX040 to CX042 ----------------------------------------------------------------


def _drop_entries(text: str) -> str:
    return re.sub(r"^#### .*\n(- .*\n)*", "", text, flags=re.MULTILINE)


def test_cx040_no_entry(valid_contract):
    assert "CX040" in codes(check_text(_drop_entries(valid_contract)).errors)


def test_cx040_absent_with_entry(valid_contract):
    assert "CX040" not in all_codes(check_text(valid_contract))


def test_cx040_entry_outside_log_does_not_count(valid_contract):
    text = _drop_entries(valid_contract).replace("### Revision log", "### Notes")
    assert "CX040" in codes(check_text(text).errors)


def test_cx041_entry_heading_format(valid_contract):
    bad = re.sub(r"^#### .*$", "#### First version", valid_contract, flags=re.MULTILINE)
    assert "CX041" in codes(check_text(bad).warnings)
    assert "CX041" not in all_codes(check_text(valid_contract))


def test_cx042_version_mismatch(valid_contract):
    text = replace_once(valid_contract, "**Contract version:** 0.1.0", "**Contract version:** 0.2.0")
    assert "CX042" in codes(check_text(text).warnings)
    assert "CX042" not in all_codes(check_text(valid_contract))


def test_cx042_uses_newest_entry(valid_contract):
    older = "#### 2025-01-01 · 0.0.9 · Older\n- **Change:** x\n"
    text = valid_contract.rstrip("\n") + "\n\n" + older
    assert "CX042" not in all_codes(check_text(text))


# --- CX050 / CX060 -------------------------------------------------------------------------------


def test_cx050_placeholders_are_summarised(valid_contract):
    text = valid_contract + "\nSee <first> and <second>.\n"
    report = check_text(text)
    hits = [w for w in report.warnings if w.code == "CX050"]
    assert len(hits) == 1
    assert hits[0].message.startswith("2 unresolved placeholders")
    assert hits[0].line == len(text.splitlines())


def test_cx050_counts_date_placeholder(valid_contract):
    text = valid_contract + "\nDate: YYYY-MM-DD\n"
    assert "CX050" in codes(check_text(text).warnings)


def test_cx050_ignores_html_and_code_blocks(valid_contract):
    text = valid_contract + (
        '\n<br>\n<img src="x.svg" alt="y">\n<p align="center">\n</p>\n<https://example.org>\n'
        "\n```\n<in code> YYYY-MM-DD\n```\n"
    )
    assert "CX050" not in all_codes(check_text(text))


def test_cx050_in_templates():
    from complexmd import cli

    raw = cli._render_template("full", None, None)
    assert "CX050" in codes(check_text(raw).warnings)


def test_cx060_word_limit(valid_contract):
    long = valid_contract + "\n" + "word " * 6001
    assert "CX060" in codes(check_text(long).warnings)
    assert "CX060" not in all_codes(check_text(valid_contract))
    assert "CX060" in codes(check_text(valid_contract, max_words=50).warnings)


# --- Templates, examples, paths --------------------------------------------------------------------


@pytest.mark.parametrize("name", ["full", "minimal"])
def test_templates_have_no_errors(name):
    from complexmd import cli

    report = check_text(cli._render_template(name, None, None))
    assert report.errors == []


def test_minimal_contains_exactly_the_required_sections():
    from complexmd import cli

    text = cli._render_template("minimal", None, None)
    h2 = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", text, flags=re.MULTILINE)]
    assert h2 == checker.REQUIRED_SECTIONS


@pytest.mark.parametrize("example", ["epidemic-model", "opinion-dynamics"])
def test_examples_have_no_errors(repo_root, example):
    report = check_file(repo_root / "examples" / example / "COMPLEX.md")
    assert report.errors == []
    assert 80 <= len((repo_root / "examples" / example / "COMPLEX.md").read_text().splitlines()) <= 140


def test_check_path_walks_directories(tmp_path, valid_contract):
    (tmp_path / "a" / "b").mkdir(parents=True)
    (tmp_path / "a" / "b" / "COMPLEX.md").write_text(valid_contract, encoding="utf-8")
    (tmp_path / "COMPLEX.md").write_text(valid_contract, encoding="utf-8")
    for skipped in (".git", ".venv", "node_modules", "__pycache__"):
        (tmp_path / skipped).mkdir()
        (tmp_path / skipped / "COMPLEX.md").write_text(valid_contract, encoding="utf-8")
    reports = check_path(tmp_path)
    assert len(reports) == 2
    assert all(r.ok for r in reports)


def test_check_path_empty_directory(tmp_path):
    assert check_path(tmp_path) == []


def test_report_to_dict(valid_contract):
    d = check_text(valid_contract, path="x.md").to_dict()
    assert set(d) == {"path", "ok", "errors", "warnings", "contract_version", "conformance"}
    assert d["ok"] is True
