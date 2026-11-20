# Releasing to PyPI

Releases are made by a person. Nothing in this repository publishes by itself: the release
workflow runs only when you start it or publish a GitHub release, and PyPI uploads wait for
your approval in the `pypi` environment.

## One-time setup

- [ ] Decide the repository name and check that the owner and copyright holder are right everywhere (`LICENSE`, `pyproject.toml`, `CITATION.cff`, `README.md`).
- [x] README links are already absolute GitHub URLs (PyPI does not resolve relative links).
- [ ] Push the repository to GitHub. It must be public so the README images show on PyPI.
- [ ] Create accounts on pypi.org and test.pypi.org (they are separate) and enable two-factor authentication on both.
- [ ] Set up Trusted Publishing without a token. On PyPI: *Account → Publishing → Add a new pending publisher* with project name `complexmd`, your owner, the repository name, workflow `release.yml` and environment `pypi`. Repeat on TestPyPI with environment `testpypi`. A pending publisher creates the project on the first upload.
- [ ] On GitHub, under *Settings → Environments*, create `pypi` and `testpypi`. Add yourself as *required reviewer* on `pypi` so each publication needs your confirmation.

## For each version

1. [ ] Set the version in `pyproject.toml` and `CITATION.cff`, date the entry in `CHANGELOG.md`, commit, and run `uv run --locked ruff check` and `uv run --locked pytest` locally (there is no CI in this repository).
2. [ ] Check locally: `uv build`, `uvx twine check dist/*`, install the wheel into a fresh environment and run `complexmd --version`.
3. [ ] **TestPyPI:** *Actions → Release → Run workflow*. Then try `uv tool install --index-url https://test.pypi.org/simple/ complexmd` and look at the project page on test.pypi.org.
4. [ ] **PyPI:** tag `v0.1.0` and publish a GitHub release for it. The workflow builds the package, waits for your approval in the `pypi` environment, then uploads.
5. [ ] Verify: `pip install complexmd` in a fresh environment. Optionally add a PyPI badge to the README.

## Alternative: upload by hand

The workflow is optional. Instead of Trusted Publishing you can create an API token on PyPI and run `uv build` followed by `uvx twine upload dist/*`. Do the same on TestPyPI first with `--repository testpypi`.

## Good to know

- A version number can be uploaded to PyPI only once. Fix mistakes with a new version.
- The name `complexmd` was reported free on 2026-11-19; check again right before the first upload.
- With Trusted Publishing the PyPA action creates provenance attestations automatically.
