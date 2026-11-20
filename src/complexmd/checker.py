"""Structural checks for COMPLEX.md files (rules CX001 to CX060)."""

from __future__ import annotations

import datetime
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_SECTIONS = [
    "Purpose and scales",
    "Canonical workflows",
    "Discover",
    "Configure",
    "Run",
    "Results",
    "Same commands for people and agents",
    "Compose",
    "Conventions and limits",
    "When the interface is not enough",
    "Human checkpoints",
    "Conformance",
    "Living contract",
]
RECOMMENDED_SECTIONS = ["Interventions", "Reporting", "Worked examples"]

PRINCIPLES = [
    "Discoverability/Introspection",
    "Declarative control",
    "Statelessness",
    "Structured, queryable output",
    "Human-Agent parity",
    "Composability",
]
STATUSES = ["implemented", "partial", "planned", "not-applicable"]

DEFAULT_MAX_WORDS = 6000
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}

_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
_FENCE = re.compile(r"^\s{0,3}(```|~~~)")
_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ENTRY = re.compile(r"^(\d{4}-\d{2}-\d{2}) · (\d+\.\d+\.\d+) · \S.*$")
# A placeholder is square brackets around text with a letter or an ellipsis, e.g. [name] or [...].
# Links ([text](url)), empty brackets (errors[]) and number ranges ([0, 1]) do not count.
_PLACEHOLDER = re.compile(r"\[[^\[\]\n]*[A-Za-z\u2026][^\[\]\n]*\](?!\()")


@dataclass
class Issue:
    code: str
    line: int | None
    message: str

    def to_dict(self) -> dict:
        return {"code": self.code, "line": self.line, "message": self.message}


@dataclass
class Report:
    path: str
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    contract_version: str | None = None
    conformance: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "ok": self.ok,
            "errors": [i.to_dict() for i in self.errors],
            "warnings": [i.to_dict() for i in self.warnings],
            "contract_version": self.contract_version,
            "conformance": dict(self.conformance),
        }


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).lower()


def _norm_principle(name: str) -> str:
    name = name.replace("–", "-").replace("—", "-")
    name = re.sub(r"\s*/\s*", "/", name)
    return _norm(name.strip("*` "))


_PRINCIPLE_BY_NORM = {_norm_principle(p): p for p in PRINCIPLES}


def _scan(lines: list[str]) -> list[bool]:
    """Return, per line, whether it lies inside (or on the edge of) a fenced code block."""
    inside = False
    fence = ""
    result = []
    for line in lines:
        m = _FENCE.match(line)
        if m and not inside:
            inside, fence = True, m.group(1)
            result.append(True)
        elif m and inside and m.group(1) == fence:
            inside = False
            result.append(True)
        else:
            result.append(inside)
    return result


def _split_row(line: str) -> list[str]:
    body = line.strip()
    body = body.removeprefix("|")
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-+:?", c) for c in cells)


def _header_value(lines, in_code, label):
    prefix = f"**{label}:**"
    for i, line in enumerate(lines):
        if not in_code[i] and line.startswith(prefix):
            return i + 1, line[len(prefix) :].strip()
    return None, None


def _is_placeholder(token: str) -> bool:
    return token[1:-1].strip().lower() != "x"  # [x] is a checked task box, not a placeholder


def check_text(text: str, path: str = "<text>", max_words: int = DEFAULT_MAX_WORDS) -> Report:
    report = Report(path=path)
    lines = text.splitlines()
    in_code = _scan(lines)

    def error(code, line, msg):
        report.errors.append(Issue(code, line, msg))

    def warn(code, line, msg):
        report.warnings.append(Issue(code, line, msg))

    # Headings outside code blocks.
    headings = []  # (level, normalized title, raw title, line number)
    for i, line in enumerate(lines):
        if in_code[i]:
            continue
        m = _HEADING.match(line)
        if m:
            headings.append((len(m.group(1)), _norm(m.group(2)), m.group(2).strip(), i + 1))

    h2 = [(t, n) for lvl, t, _, n in headings if lvl == 2]
    present = {t for t, _ in h2}
    for name in REQUIRED_SECTIONS:
        if _norm(name) not in present:
            error("CX010", None, f'required section "{name}" is missing')
    for name in RECOMMENDED_SECTIONS:
        if _norm(name) not in present:
            warn("CX011", None, f'recommended section "{name}" is missing')
    known = {_norm(n): n for n in REQUIRED_SECTIONS + RECOMMENDED_SECTIONS}
    seen: dict[str, int] = {}
    for t, n in h2:
        if t in known:
            if t in seen:
                warn("CX012", n, f'section "{known[t]}" appears more than once')
            seen.setdefault(t, n)

    # Header lines.
    line_no, value = _header_value(lines, in_code, "System")
    if not value:
        error("CX020", line_no, "**System:** line is missing or empty")
    line_no, value = _header_value(lines, in_code, "Contract version")
    if value is None or not _SEMVER.match(value):
        error("CX021", line_no, "**Contract version:** is missing or not MAJOR.MINOR.PATCH")
    else:
        report.contract_version = value
    line_no, value = _header_value(lines, in_code, "Last reviewed")
    valid_date = False
    if value is not None and _DATE.match(value):
        try:
            datetime.date.fromisoformat(value)
            valid_date = True
        except ValueError:
            pass
    if value is None or not (valid_date or value == "not yet"):
        error("CX022", line_no, "**Last reviewed:** must be a valid YYYY-MM-DD date or `not yet`")

    _check_conformance(lines, in_code, headings, report)
    _check_revision_log(headings, report)

    # Placeholders.
    count, first = 0, None
    for i, line in enumerate(lines):
        if in_code[i]:
            continue
        n = sum(1 for tok in _PLACEHOLDER.findall(line) if _is_placeholder(tok))
        n += line.count("YYYY-MM-DD")
        if n:
            count += n
            first = first or i + 1
    if count:
        s = "" if count == 1 else "s"
        warn("CX050", first, f"{count} unresolved placeholder{s}")

    words = len(text.split())
    if words > max_words:
        warn("CX060", None, f"{words} words; the limit is {max_words}")

    return report


def _section_range(headings, total, level, title):
    """Line range (start, end), 1-based, of the body of the first heading `title` at `level`."""
    for idx, (lvl, t, _, n) in enumerate(headings):
        if lvl == level and t == _norm(title):
            end = total + 1
            for lvl2, _, _, n2 in headings[idx + 1 :]:
                if lvl2 <= level:
                    end = n2
                    break
            return n + 1, end
    return None


def _check_conformance(lines, in_code, headings, report):
    rng = _section_range(headings, len(lines), 2, "Conformance")
    if rng is None:
        return  # CX010 already reported
    block = []
    for i in range(rng[0] - 1, rng[1] - 1):
        if not in_code[i] and lines[i].lstrip().startswith("|"):
            block.append(i)
        elif block:
            break
    rows = [(i, _split_row(lines[i])) for i in block]
    if len(rows) < 2 or not _is_separator(rows[1][1]):
        report.errors.append(Issue("CX030", None, "Conformance has no table"))
        return
    seen = set()
    for i, cells in rows[2:]:
        name = cells[0] if cells else ""
        key = _norm_principle(name)
        principle = _PRINCIPLE_BY_NORM.get(key)
        if principle is None:
            msg = f'row "{name}" is not one of the six principles'
            report.warnings.append(Issue("CX031", i + 1, msg))
            continue
        if principle in seen:
            report.errors.append(Issue("CX031", i + 1, f'principle "{principle}" appears twice'))
            continue
        seen.add(principle)
        status = _norm((cells[1] if len(cells) > 1 else "").strip("*` "))
        how = (cells[2] if len(cells) > 2 else "").strip()
        report.conformance[principle] = status
        if status not in STATUSES:
            msg = f'status "{status}" of "{principle}" is not one of {", ".join(STATUSES)}'
            report.errors.append(Issue("CX032", i + 1, msg))
        elif status == "not-applicable" and not how:
            msg = f'"{principle}" is not-applicable but gives no reason in How'
            report.errors.append(Issue("CX033", i + 1, msg))
        elif status == "implemented" and not how:
            msg = f'"{principle}" is implemented but says nothing in How'
            report.warnings.append(Issue("CX034", i + 1, msg))
    for p in PRINCIPLES:
        if p not in seen:
            report.errors.append(Issue("CX031", None, f'principle "{p}" is missing from the table'))


def _check_revision_log(headings, report):
    living = next((k for k, h in enumerate(headings) if h[0] == 2 and h[1] == "living contract"), None)
    entries = []  # (raw title, line)
    in_log = False
    if living is not None:
        for lvl, t, raw, n in headings[living + 1 :]:
            if lvl <= 2:
                break
            if lvl == 3:
                in_log = t == "revision log"
            elif lvl == 4 and in_log:
                entries.append((raw, n))
    if not entries:
        report.errors.append(Issue("CX040", None, "Revision log has no entry"))
        return
    parsed = []
    for raw, n in entries:
        m = _ENTRY.match(raw)
        if m:
            parsed.append((m.group(1), tuple(int(x) for x in m.group(2).split(".")), m.group(2)))
        else:
            msg = f'entry "{raw}" does not match "#### YYYY-MM-DD · X.Y.Z · Title"'
            report.warnings.append(Issue("CX041", n, msg))
    if parsed and report.contract_version:
        newest = max(parsed, key=lambda p: (p[0], p[1]))
        if newest[2] != report.contract_version:
            msg = (
                f"newest log entry is {newest[2]} but Contract version is "
                f"{report.contract_version}"
            )
            report.warnings.append(Issue("CX042", None, msg))


def _read(path: Path, report: Report) -> str | None:
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError:
        report.errors.append(Issue("CX001", None, "file not found"))
    except IsADirectoryError:
        report.errors.append(Issue("CX001", None, "is a directory"))
    except UnicodeDecodeError:
        report.errors.append(Issue("CX001", None, "file is not valid UTF-8"))
    except OSError as exc:
        report.errors.append(Issue("CX001", None, f"cannot read file: {exc.strerror or exc}"))
    return None


def check_file(path, max_words: int = DEFAULT_MAX_WORDS) -> Report:
    p = Path(path)
    placeholder = Report(path=str(path))
    text = _read(p, placeholder)
    if text is None:
        return placeholder
    return check_text(text, path=str(path), max_words=max_words)


def find_contracts(path) -> list[Path]:
    p = Path(path)
    if not p.is_dir():
        return [p]
    found = []
    for root, dirs, files in os.walk(p):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        if "COMPLEX.md" in files:
            found.append(Path(root) / "COMPLEX.md")
    return sorted(found)


def check_path(path, max_words: int = DEFAULT_MAX_WORDS) -> list[Report]:
    """Check a file, or every COMPLEX.md below a directory. A missing path gives one CX001."""
    p = Path(path)
    if not p.is_dir():
        return [check_file(p, max_words)]
    return [check_file(f, max_words) for f in find_contracts(p)]
