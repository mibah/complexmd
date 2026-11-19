"""Command line interface: `complexmd init | templates | check`."""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from importlib import metadata, resources
from pathlib import Path

from complexmd import checker

TEMPLATES = {
    "full": "all sections with guidance",
    "minimal": "required sections only",
}
FILENAME = "COMPLEX.md"
FOOTER = "Checked structure only. This does not test whether the interface works."


def _version() -> str:
    try:
        return metadata.version("complexmd")
    except metadata.PackageNotFoundError:
        return "unknown"


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


def _color(text: str, code: str, enabled: bool) -> str:
    return f"\033[{code}m{text}\033[0m" if enabled else text


def _use_color() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _render_template(name: str, system: str | None, command: str | None) -> str:
    text = (resources.files("complexmd") / "templates" / f"{name}.md").read_text(encoding="utf-8")
    if system:
        text = text.replace("<name of the simulator or library>", system).replace("<system>", system)
    if command:
        text = text.replace("<cmd>", command)
    return text.replace("#### YYYY-MM-DD", f"#### {datetime.date.today().isoformat()}", 1)


def cmd_init(args: argparse.Namespace) -> int:
    directory = Path(args.path)
    if not directory.is_dir():
        _err(f"directory does not exist: {directory}")
        return 2
    target = directory / FILENAME
    exists_msg = f"{FILENAME} already exists in {directory}; nothing was written."
    try:
        target.lstat()
    except FileNotFoundError:
        pass
    else:
        _err(exists_msg)
        return 2
    text = _render_template(args.template, args.system, args.command)
    try:
        with open(target, "x", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    except FileExistsError:
        _err(exists_msg)
        return 2
    except OSError as exc:
        _err(f"cannot write {target}: {exc.strerror or exc}")
        return 2
    if args.json:
        print(json.dumps({"created": str(target), "template": args.template}))
    else:
        print(f"Created {target} from the {args.template} template.")
        print("Next: describe your interface under Discover, Configure, Run and Results,")
        print(f"then run `complexmd check {target}`.")
    return 0


def cmd_templates(args: argparse.Namespace) -> int:
    if args.json:
        print(json.dumps([{"name": n, "description": d} for n, d in TEMPLATES.items()]))
    else:
        print("\n".join(f"{key:<8}{text}" for key, text in TEMPLATES.items()))
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    reports: list[checker.Report] = []
    for p in args.paths:
        found = checker.check_path(p, max_words=args.max_words)
        if not found:
            _err(f"no {FILENAME} found under {p}")
            return 2
        reports.extend(found)

    unreadable = any(i.code == "CX001" for r in reports for i in r.errors)
    failed = any(r.errors or (args.strict and r.warnings) for r in reports)

    if args.json:
        print(json.dumps({"complexmd": _version(), "results": [r.to_dict() for r in reports]}))
    else:
        color = _use_color()
        for r in reports:
            print(r.path)
            for level, issues, code in (("error", r.errors, "31"), ("warning", r.warnings, "33")):
                for i in issues:
                    where = f" line {i.line}" if i.line else ""
                    print(f"  {_color(level, code, color)} {i.code}{where}  {i.message}")
            bad = bool(r.errors or (args.strict and r.warnings))
            status = _color("failed", "31", color) if bad else _color("ok", "32", color)
            contract = f" · contract {r.contract_version}" if r.contract_version else ""
            counts = f"{_plural(len(r.errors), 'error')}, {_plural(len(r.warnings), 'warning')}"
            print(f"{status}{contract} · {counts}")
            print()
        print(FOOTER)
    if unreadable:
        return 2
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="complexmd",
        description="Create and check COMPLEX.md agent contracts for complex systems models.",
    )
    parser.add_argument("--version", action="version", version=f"complexmd {_version()}")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help=f"create a {FILENAME} from a template")
    p_init.add_argument("--template", choices=list(TEMPLATES), default="full")
    p_init.add_argument("--path", default=".", help="existing directory (default: .)")
    p_init.add_argument("--system", help="name of your simulator or library")
    p_init.add_argument("--command", help="the command line tool that drives your model")
    p_init.add_argument("--json", action="store_true", help="machine-readable output")
    p_init.set_defaults(func=cmd_init)

    p_tpl = sub.add_parser("templates", help="list the available templates")
    p_tpl.add_argument("--json", action="store_true", help="machine-readable output")
    p_tpl.set_defaults(func=cmd_templates)

    p_chk = sub.add_parser("check", help=f"check the structure of {FILENAME} files")
    p_chk.add_argument("paths", nargs="*", default=None, metavar="PATH")
    p_chk.add_argument("--json", action="store_true", help="machine-readable output")
    p_chk.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p_chk.add_argument("--max-words", type=int, default=checker.DEFAULT_MAX_WORDS, metavar="N")
    p_chk.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    if args.command == "check" and not args.paths:
        args.paths = ["."]
    return args.func(args)
