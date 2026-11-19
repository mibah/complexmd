# Contributing

Thanks for helping. COMPLEXmd is small on purpose, so the most useful contributions are
evidence rather than features.

## What helps most

- Experience reports from real models: what worked, what did not, what you had to change.
- Findings from review rounds ([docs/living-contract.md](docs/living-contract.md)).
- Improvements to the templates and documentation.
- Proposals for the convention itself.

## Proposing changes to the convention

Open an issue first (`Convention change`). Changing a heading, header line or status value
affects every existing contract, so it needs discussion before code.

## Development

```bash
uv sync --locked
uv run --locked pytest
uv run --locked ruff check
uv build
```

## Pull requests

- Keep them small and say which checks you ran.
- If you touch the convention, update the template, `checker.py`, `docs/specification.md`, the tests and `CHANGELOG.md` together.
- Mark invented examples as fictional. Do not add review results or adoption claims that did not happen.
- Describe the paper in your own words and cite it; mark anything COMPLEXmd adds.

By contributing you agree that your work is released under the [MIT License](LICENSE).
