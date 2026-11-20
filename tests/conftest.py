import re
from pathlib import Path

import pytest

from complexmd import cli

REPO = Path(__file__).resolve().parents[1]


def make_valid_contract() -> str:
    """The full template with every placeholder filled in: a contract without findings."""
    text = cli._render_template("Demo model", "demo")
    previous = None
    while previous != text:  # placeholders can be nested, so substitute until stable
        previous, text = text, re.sub(r"\[[^\[\]\n]*[A-Za-z\u2026][^\[\]\n]*\](?!\()", "text", text)
    return text


@pytest.fixture
def valid_contract() -> str:
    return make_valid_contract()


@pytest.fixture
def repo_root() -> Path:
    return REPO
