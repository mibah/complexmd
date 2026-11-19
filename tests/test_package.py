import subprocess
import sys
import venv
import zipfile
from pathlib import Path


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, check=True, **kw)


def test_wheel_installs_and_works(tmp_path, repo_root):
    dist = tmp_path / "dist"
    _run([sys.executable, "-m", "build", "--wheel", "--outdir", str(dist), str(repo_root)])
    wheel = next(dist.glob("complexmd-*.whl"))

    names = zipfile.ZipFile(wheel).namelist()
    assert "complexmd/templates/full.md" in names
    assert "complexmd/templates/minimal.md" in names

    env = tmp_path / "venv"
    venv.EnvBuilder(with_pip=True).create(env)
    bindir = env / ("Scripts" if sys.platform == "win32" else "bin")
    py = bindir / ("python.exe" if sys.platform == "win32" else "python")
    _run([str(py), "-m", "pip", "install", "--no-index", "--quiet", str(wheel)])

    exe = bindir / ("complexmd.exe" if sys.platform == "win32" else "complexmd")
    version = _run([str(exe), "--version"]).stdout
    assert version.startswith("complexmd 0.1.0")

    work = tmp_path / "work"
    work.mkdir()
    out = _run([str(exe), "init", "--system", "Demo", "--command", "demo"], cwd=work).stdout
    assert out.startswith("Created ")
    assert Path(work / "COMPLEX.md").is_file()
