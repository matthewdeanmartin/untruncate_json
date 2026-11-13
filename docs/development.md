# Development

Use Python 3.15 and `uv` for the quality tools. Run `make` to list available jobs.

```sh
make sync
make check
make validate
```

`make check` runs Ruff, Pylint (minimum score 9.7), strict mypy, Bandit, and pytest
with a 90% branch-inclusive coverage minimum. Each gate runs every time.
`make test` runs tests independently. Quality tools use the locked `quality`
group; changelog validation uses the `release` group.

## Build native distributions

```sh
uv build --python 3.15
```

This builds an sdist and a native wheel in `dist/`, requiring a C compiler.
The parser is compiled with mypyc. Python 3.9 uses mypy 1.19.1; newer supported
interpreters use mypy 2.4.1. CI tests installed wheels and verifies that the
compiled parser is loaded.

## Documentation

```sh
make docs
make docs-serve
```

`make docs` builds the site with warnings treated as errors. Output goes to
`site/`. The preview server prints its local URL. Edit Markdown pages in `docs/`
and navigation in `mkdocs.yml`.

Documentation dependencies live in the `docs` dependency group. After upgrading
them, refresh the Read the Docs requirements export:

```sh
uv lock --upgrade
uv export --only-group docs --no-emit-project --no-hashes --output-file docs/requirements.txt
```

Read the Docs uses `.readthedocs.yaml`, Python 3.14, and `docs/requirements.txt`.
Import this GitHub repository into Read the Docs to enable hosting. The documentation URL is
https://untruncate-json.readthedocs.io/en/latest/.

`make zizmor` audits all workflows in pedantic mode without suppressions.
It uses offline audits locally unless `GH_TOKEN` is available. The dedicated zizmor workflow runs only for `.github/**` changes on pull
requests and pushes to `main`; it supplies a GitHub token for online audits
and uploads SARIF findings when permissions allow. Zizmor is pinned in the `security`
dependency group.

## Software homepage

The Hugo site lives in `landing/`, separate from the MkDocs documentation.
Install Hugo 0.164.0, then run `make homepage` or `make homepage-serve`.
The output is `landing/public/` and is ignored by Git.

`.github/workflows/pages.yml` builds homepage changes on pull requests and pushes
to `main`. Only `main` can deploy. A manual workflow run can also deploy `main`.
The workflow verifies the downloaded Hugo binary's SHA-256 before running it.
GitHub Pages must use **GitHub Actions** as its publishing source.

- Homepage: https://matthewdeanmartin.github.io/untruncate_json/
- Documentation: https://untruncate-json.readthedocs.io/en/latest/

The homepage links to Read the Docs; it does not deploy a second copy of the docs.
