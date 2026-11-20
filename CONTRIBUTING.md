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

Set up once, in the project folder (the `.venv` folder is ignored by Git):

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e . pytest ruff build twine
```

Then, with the environment active:

```bash
python -m pytest        # tests
python -m ruff check    # style check
python -m build         # builds the package into dist/
```

With [uv](https://docs.astral.sh/uv/) the same works as `uv sync --locked`, `uv run --locked pytest`,
`uv run --locked ruff check` and `uv build`.

## Pull requests

- Keep them small and say which checks you ran.
- If you touch the convention, update the template, `checker.py`, the tests and `CHANGELOG.md` together.
- Mark invented examples as fictional. Do not add review results or adoption claims that did not happen.
- Describe the paper in your own words and cite it; mark anything COMPLEXmd adds.

## Releasing (maintainers)

Publishing to PyPI means building the package locally and uploading it with
[twine](https://twine.readthedocs.io/), the standard upload tool. No CI is involved.

1. **Raise the version** in `pyproject.toml` and `CITATION.cff`, and add a dated section to `CHANGELOG.md`. A version number can be uploaded only once, even if you delete the release; fix mistakes with a new number.
2. **Check:** with the environment active, run `python -m pytest` and `python -m ruff check`.
3. **Build:** `rm -rf dist && python -m build`, then `python -m twine check dist/*`.
4. **Commit and push** so GitHub shows the same state: `git add -A && git commit -m "Release X.Y.Z" && git push`.
5. **Upload:** `python -m twine upload dist/*`. Username `__token__`, password a PyPI API token (scope: this project only, created under *Account settings → API tokens*; the account needs two-factor authentication).
6. **Verify** in a fresh environment: `pip install --upgrade complexmd`, then `complexmd --version`.

The PyPI page shows the README of the newest version, so a README change needs a new release.
For a dry run, repeat the upload on https://test.pypi.org with its own account and token and
`python -m twine upload --repository testpypi dist/*`.

By contributing you agree that your work is released under the [MIT License](LICENSE).
