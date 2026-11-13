# untruncate_json

Python library to repair truncated json. Translated directly from the typescript original version

## Installation

```bash
pip install untruncate_json
```

## Usage

In some cases, a partial json document is invalid and there is no way to recover. A common scenario using OpenAI's chatbot is that the AI created json is truncated at the end of the document. This library will attempt to repair the json by adding the missing closing brackets.

If the context of the json is relatively simple and holds natural language, truncating the text might not degrade the final result much.

```python
import untruncate_json
assert untruncate_json.complete('{"foo": "bar') == '{"foo": "bar"}'
```

## Documentation

Visit the [homepage](https://matthewdeanmartin.github.io/untruncate_json/) or [documentation](https://untruncate-json.readthedocs.io/en/latest/) for usage, the API, development, and releases. Run `make docs-serve` to preview the MkDocs site locally, or `make homepage-serve` for the Hugo homepage.

## Credits
Original Typescript version by dphilipson, MIT license. Code translated by a lazy ChatGPT that didn't
want to translate the long switch blocks. Copilot translated the switch blocks.

## Prior Art

- [untruncate-json](https://github.com/dphilipson/untruncate-json) - Original Typescript version
- [truncjson](https://pypi.org/project/truncjson/) Cython implementation
- [jsonfixer](https://pypi.org/project/jsonfixer/) Fork of half-json?
- [half-json](https://pypi.org/project/halfjson/)

## Benchmarks

- truncjson: 1.28
- untruncate_json: 11.39
- untruncate_json: 1.14 (if you run `mypyc untruncate_json`
- jsonfixer: 23.06

## Project Links

- [GitHub](https://github.com/matthewdeanmartin/untruncate_json)
- [PyPI](https://pypi.org/project/untruncate-json/)
- [Bug Tracker](https://github.com/matthewdeanmartin/untruncate_json/issues)
- [Change Log](https://github.com/matthewdeanmartin/untruncate_json/blob/main/CHANGELOG.md)

## Building native wheels

The parser is compiled with mypyc. Release wheels target standard CPython
3.9–3.15 on Windows x64, macOS Intel/Apple Silicon, and Linux x64/ARM64
(manylinux and musllinux). Free-threaded Python and PyPy are not targeted.
Python 3.9 uses mypy 1.19.1; newer interpreters use mypy 2.4.1.

Run `uv build --python 3.15` to build an sdist and native wheel locally
(a C compiler is required). CI tests installed wheels and checks that the
compiled parser is loaded. The release workflow calls the same wheel workflow
and publishes the complete artifact set only after every build and test passes.
The release bump supplies the version; do not publish the existing 1.1.0 again.

## Quality checks

Run `make` to list available jobs and `make check` to run Ruff, Pylint,
strict mypy, Bandit, and tests with a 90% branch-inclusive coverage gate.
These checks use the locked `quality` dependency group and always run;
there are no history-file shortcuts. `make test` runs tests independently.

## Release process

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
