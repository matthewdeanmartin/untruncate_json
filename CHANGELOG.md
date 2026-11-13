# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-11-13
### Changed
- Restore mypyc native builds for CPython 3.9–3.15.
- Build and test Linux x64/ARM64, macOS Intel/Apple Silicon, and Windows x64 wheels together before release publication.
- Upgrade GitHub Actions and refresh the dependency lock.
- Align draft and published release automation with kacl-m, preserving build.yml for PyPI trusted publishing.

### Fixed
- Execute the CLI when invoked as `python -m untruncate_json`.
- Preserve valid Unicode escapes without appending extra quotes.
- Use the native build backend and correct the console command to `untruncate_json`.
- Explicitly declare the package README as Markdown for PyPI rendering.

### Added
- Run explicit Ruff, Pylint, strict mypy, Bandit, coverage, and changelog quality gates before release builds.
- Add a MkDocs Material documentation site with Read the Docs configuration and strict documentation builds.
- Add a Hugo software homepage deployed by GitHub Pages, with links to the Read the Docs documentation.

### Security
- Audit GitHub Actions with pinned zizmor in local and CI quality gates; document permissions and harden reusable workflow references.

## [1.1.0] - 2024-12-24
### Changed
- Add Python 3.12 and 3.13 classifiers to package metadata
- Update GitHub Actions build workflow with revised job matrix
- Drop `truncjson` from benchmark and comparison scripts

### Fixed
- Apply minor code formatting improvements across library modules

## [1.0.0] - 2023-12-03
### Added
- Translate core algorithm from the original TypeScript implementation by dphilipson
- Add unit tests

[1.1.0]: https://github.com/matthewdeanmartin/untruncate_json/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/matthewdeanmartin/untruncate_json/releases/tag/v1.0.0
