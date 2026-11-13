# Releases


The workflow files have separate roles:

| Workflow | Purpose |
| --- | --- |
| `quality_gates.yml` | Run lint, type, security, coverage, and changelog checks on pushes and PRs, and before release builds. |
| `build_wheels.yml` | Build and test 49 native wheels plus one source distribution; validate metadata, artifact count, and versions. Also callable by the release workflow. |
| `create_draft_release.yml` | Refresh the GitHub draft release from the changelog on pushes to `main`, or manually. |
| `build.yml` | Handle a published GitHub release, bump versions, run checks, build distributions, and publish to PyPI. |

**Keep the publishing workflow named `build.yml`.** PyPI trusted publishing is
registered to that filename for this repository. Its publish job uses the
GitHub environment `pypi` and `id-token: write`; it does not use a PyPI API token.
The workflow's display name is `Release`.

1. Add changes under `[Unreleased]` in `CHANGELOG.md`. Run `make check` and
   `make validate`. To preview the next version without changing files, run
   `uv run --frozen --only-group release kaclm release --bump-versions --dry-run`.
2. After the changes reach `main`, review the generated draft release's version
   and notes. Publish the draft when ready to start the release workflow.
3. `build.yml` runs `kaclm release-bump --github-output`, which creates a release
   branch and PR and updates the changelog, `pyproject.toml`, and
   `untruncate_json/version.py`. Quality checks and builds use that branch.
4. Publishing waits for the quality gates and every wheel build, test, and
   artifact validation to pass. The publish job downloads the full artifact
   set and uploads it using PyPI trusted publishing.
5. Confirm the release is available on PyPI, then merge the generated release PR.

For a failed quality or build job, inspect its logs and fix the failure before
retrying; nothing has been uploaded at that stage. If publishing fails, inspect
PyPI for partial uploads before retrying. Reuse a retained, validated artifact
set where possible, and never attempt to replace files already published on PyPI.

Release history is maintained in the repository [changelog](https://github.com/matthewdeanmartin/untruncate_json/blob/main/CHANGELOG.md).
