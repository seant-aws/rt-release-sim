# rt-release-sim

A throwaway repository for a pre-merge test of the OpenJD release train's live mode. It runs a real
"Release: Bump" and "Release: Publish" flow on a tiny package, with every step that would publish
anything outside this repository, or that needs a secret, replaced by a step that prints what it would
have done. **Nothing is published to PyPI, TestPyPI or any package repository, and nothing is signed.**
The package is not meant to be installed.

## Where the workflows come from

| File | Copied from (read-only) |
|---|---|
| `.github/workflows/release_bump.yml`, `release_publish.yml` | `OpenJobDescription/openjd-sessions-for-python` mainline |
| `.github/workflows/reusable_bump.yml`, `reusable_tag_release.yml`, `reusable_prerelease.yml`, `reusable_release.yml`, `reusable_publish_python.yml` | `OpenJobDescription/.github` mainline (the reusable workflows the two callers name `@mainline`) |
| `.github/actions/tag-release`, `.github/actions/check-release` | `OpenJobDescription/.github` mainline |
| `.github/scripts/get_latest_changelog.py`, `.semantic_release/CHANGELOG.md.j2`, `requirements-release.txt`, the `[tool.semantic_release]` table of `pyproject.toml` | `OpenJobDescription/openjd-sessions-for-python` mainline |
| `.github/workflows/release_train.yml` | the fork test's release-train caller, in live mode |

The first commit imports the files verbatim; the second applies the substitutions below, each marked
`# SUBSTITUTION:` in the YAML, so `git diff` between the two shows exactly what changed.

## Substitutions

| Where | Real workflow | Here |
|---|---|---|
| `release_bump.yml`, `release_publish.yml` | `uses: OpenJobDescription/.github/...@mainline` with `secrets: inherit` | `uses: ./.github/workflows/<same file>` (local copy), no secrets |
| `reusable_bump.yml` checkout and `gh pr create` | `CI_TOKEN` | `GITHUB_TOKEN`. A PR opened with it has its CI held as `action_required` until a person approves the run |
| `reusable_bump.yml` git identity | `EMAIL` and `USER` secrets | the `github-actions[bot]` identity |
| `reusable_tag_release.yml` checkout and tag push | `CI_TOKEN` | `GITHUB_TOKEN` (the caller grants the job `contents: write`) |
| `tag-release` / `check-release` expected author | `EMAIL` secret | the `github-actions[bot]` email (the author of the release PR's squash commit) |
| `tag-release` / `check-release` author comparison | `[[ $AUTHOR != $EXPECTED_AUTHOR ]]` | both sides quoted: the brackets in `github-actions[bot]`'s email are otherwise a glob pattern and never match |
| `reusable_prerelease.yml` checkout | `CI_TOKEN` | `GITHUB_TOKEN`; the build itself is real |
| `reusable_release.yml` | AWS credentials, PGP key from Secrets Manager, detached signatures | removed; a step prints each file it would have signed |
| `reusable_release.yml` `gh release create` | `CI_TOKEN` | `GITHUB_TOKEN`; a real GitHub Release in this repository only (no signatures attached) |
| `reusable_publish_python.yml` | AWS credentials and a CodeBuild publish to the package repository | a step that prints the CodeBuild project and tag it would have run |
| `release_publish.yml` PublishToPyPI | `pypa/gh-action-pypi-publish` | the build runs; the upload is a step that lists `dist/` |
| `reusable_bump.yml`, `reusable_release.yml`, PublishToPyPI | `runs-on: ubuntu-latest` with Python 3.9 | `ubuntu-24.04`: `ubuntu-latest` is Ubuntu 26.04, which has no Python 3.9 for `actions/setup-python` (the upstream jobs fail the same way) |
| `code_quality.yml` | the 3-OS, 6-Python matrix of the shared build workflow | one Linux job on Python 3.12 running this package's two tests |

The `release` environment exists here without protection rules or secrets, so the jobs that name it run
as written. Kept as real as possible: semantic-release's version and CHANGELOG generation, the
`bump/X.Y.Z` branch and its `chore(release): X.Y.Z` PR, the tag on the release commit, the build, the
GitHub Release, and the push to `mainline` that starts Release: Publish.

## Repository settings

Squash merges only (title: PR title, message: commit messages), default branch `mainline`,
"Allow GitHub Actions to create and approve pull requests" on. Actions are disabled once the test ends.
