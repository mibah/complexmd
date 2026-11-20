import json
import os
import re
import subprocess
import sys
from datetime import date

import pytest

from complexmd import cli


def run(capsys, *argv):
    code = cli.main(list(argv))
    out = capsys.readouterr()
    return code, out.out, out.err


# --- init ----------------------------------------------------------------------------------------


def test_init_default(tmp_path, capsys):
    code, out, err = run(capsys, "init", "--path", str(tmp_path))
    target = tmp_path / "COMPLEX.md"
    assert code == 0
    assert out == (
        f"Created {target} from the template.\n"
        "Next: describe your interface under Discover, Configure, Run and Results,\n"
        f"then run `complexmd check {target}`.\n"
    )
    assert err == ""
    assert "## Reporting" in target.read_text(encoding="utf-8")


def test_init_replaces_values_and_sets_date(tmp_path, capsys):
    run(capsys, "init", "--path", str(tmp_path), "--system", "Demo", "--command", "demo")
    text = (tmp_path / "COMPLEX.md").read_text(encoding="utf-8")
    assert "**System:** Demo" in text
    assert "[cmd]" not in text and "`demo describe`" in text
    assert "claim that Demo is ready" in text
    assert f"#### {date.today().isoformat()} · 0.1.0 · First version" in text
    assert "YYYY-MM-DD" not in text


def test_init_json(tmp_path, capsys):
    code, out, _ = run(capsys, "init", "--path", str(tmp_path), "--json")
    assert code == 0
    assert json.loads(out) == {"created": str(tmp_path / "COMPLEX.md")}


def test_init_does_not_overwrite_file(tmp_path, capsys):
    target = tmp_path / "COMPLEX.md"
    target.write_text("mine", encoding="utf-8")
    code, out, err = run(capsys, "init", "--path", str(tmp_path))
    assert code == 2
    assert out == ""
    assert err.strip() == f"COMPLEX.md already exists in {tmp_path}; nothing was written."
    assert target.read_text() == "mine"


def test_init_protects_symlink(tmp_path, capsys):
    victim = tmp_path / "victim.txt"
    victim.write_text("keep", encoding="utf-8")
    try:
        os.symlink(victim, tmp_path / "COMPLEX.md")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not available")
    code, _, err = run(capsys, "init", "--path", str(tmp_path))
    assert code == 2 and "already exists" in err
    assert victim.read_text() == "keep"


def test_init_protects_dangling_symlink(tmp_path, capsys):
    try:
        os.symlink(tmp_path / "nowhere", tmp_path / "COMPLEX.md")
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not available")
    code, _, err = run(capsys, "init", "--path", str(tmp_path))
    assert code == 2 and "already exists" in err
    assert not (tmp_path / "nowhere").exists()


def test_init_protects_directory(tmp_path, capsys):
    (tmp_path / "COMPLEX.md").mkdir()
    code, _, err = run(capsys, "init", "--path", str(tmp_path))
    assert code == 2 and "already exists" in err


def test_init_missing_directory_is_not_created(tmp_path, capsys):
    missing = tmp_path / "nope"
    code, out, err = run(capsys, "init", "--path", str(missing))
    assert code == 2 and out == "" and "does not exist" in err
    assert not missing.exists()


def test_init_output_passes_check_without_errors(tmp_path, capsys):
    run(capsys, "init", "--path", str(tmp_path), "--system", "Demo", "--command", "demo")
    code, _, _ = run(capsys, "check", str(tmp_path))
    assert code == 0


# --- check ---------------------------------------------------------------------------------------


def test_check_file_text_output(tmp_path, capsys, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract + "\nTodo [here]\n", encoding="utf-8")
    code, out, _ = run(capsys, "check", str(f))
    lines = out.splitlines()
    assert code == 0
    assert lines[0] == str(f)
    assert re.fullmatch(r"  warning CX050 line \d+  1 unresolved placeholder", lines[1])
    assert lines[2] == "ok · contract 0.1.0 · 0 errors, 1 warning"
    assert lines[-1] == "Checked structure only. This does not test whether the interface works."


def test_check_errors_give_exit_1(tmp_path, capsys, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract.replace("## Discover\n", "## Other\n"), encoding="utf-8")
    code, out, _ = run(capsys, "check", str(f))
    assert code == 1
    assert "error CX010" in out and "failed" in out


def test_check_default_path_is_cwd(tmp_path, capsys, monkeypatch, valid_contract):
    (tmp_path / "COMPLEX.md").write_text(valid_contract, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    code, out, _ = run(capsys, "check")
    assert code == 0 and "COMPLEX.md" in out


def test_check_directory_is_recursive(tmp_path, capsys, valid_contract):
    for d in ("one", "two/deep"):
        (tmp_path / d).mkdir(parents=True)
        (tmp_path / d / "COMPLEX.md").write_text(valid_contract, encoding="utf-8")
    code, out, _ = run(capsys, "check", "--json", str(tmp_path))
    assert code == 0
    assert len(json.loads(out)["results"]) == 2


def test_check_strict(tmp_path, capsys, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract + "\nTodo [here]\n", encoding="utf-8")
    assert run(capsys, "check", str(f))[0] == 0
    code, out, _ = run(capsys, "check", "--strict", str(f))
    assert code == 1 and "failed" in out


def test_check_max_words(tmp_path, capsys, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract, encoding="utf-8")
    _, out, _ = run(capsys, "check", "--max-words", "20", str(f))
    assert "CX060" in out


def test_check_json(tmp_path, capsys, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract, encoding="utf-8")
    code, out, err = run(capsys, "check", "--json", str(f))
    data = json.loads(out)
    assert code == 0 and err == ""
    assert set(data) == {"complexmd", "results"}
    assert set(data["results"][0]) == {
        "path", "ok", "errors", "warnings", "contract_version", "conformance",
    }  # fmt: skip
    assert "Checked structure only" not in out


def test_check_no_file_found(tmp_path, capsys):
    code, out, err = run(capsys, "check", str(tmp_path))
    assert code == 2 and out == "" and "no COMPLEX.md found" in err


def test_check_missing_path(tmp_path, capsys):
    code, out, _ = run(capsys, "check", str(tmp_path / "nope.md"))
    assert code == 2 and "CX001" in out


def test_check_no_color_when_not_a_tty(tmp_path, capsys, valid_contract):
    f = tmp_path / "COMPLEX.md"
    f.write_text(valid_contract.replace("## Discover\n", "## Other\n"), encoding="utf-8")
    _, out, _ = run(capsys, "check", str(f))
    assert "\033[" not in out


# --- misc ----------------------------------------------------------------------------------------


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    assert re.fullmatch(r"complexmd \S+\n", capsys.readouterr().out)


def test_no_subcommand_shows_help(capsys):
    code, out, _ = run(capsys)
    assert code == 0 and "usage: complexmd" in out


def test_python_dash_m():
    proc = subprocess.run(
        [sys.executable, "-m", "complexmd", "--version"],
        capture_output=True, text=True, check=False,
    )  # fmt: skip
    assert proc.returncode == 0
    assert proc.stdout.startswith("complexmd ")
