# Working on COMPLEXmd

- The convention comes first. Keep the CLI small and free of runtime dependencies.
- Template headings, header lines and status values are checked by `complexmd check`. When you
  change one, update `src/complexmd/checker.py`, the tests and `CHANGELOG.md` in the same change.
- The example must pass `complexmd check`. Keep it marked as fictional.
- Describe the paper in your own words and cite it. Mark COMPLEXmd additions as such.
- Never claim review results, readiness or adoption that did not happen.
- Commands: `uv sync --locked`, `uv run --locked pytest`, `uv run --locked ruff check`, `uv build`.
- Do not push, tag or publish without explicit approval.
