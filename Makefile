.DEFAULT_GOAL := help
VENV := uv run --frozen --only-group quality
DEV := uv run --frozen

.PHONY: homepage homepage-serve zizmor docs docs-serve validate help sync test ruff pylint mypy bandit check build clean isort black pre-commit version-check dev-status prerelease-check dont-be-lazy pydoc-docs

help:
	@echo "Available jobs:"
	@echo "  sync              Install locked quality dependencies"
	@echo "  check             Run Ruff, Pylint, mypy, Bandit and tests"
	@echo "  test              Run tests with branch coverage"
	@echo "  ruff / pylint     Run lint checks"
	@echo "  mypy              Run strict package type checks"
	@echo "  zizmor            Audit GitHub Actions security"
	@echo "  bandit            Run security checks"
	@echo "  homepage / homepage-serve Build / preview the Hugo homepage"
	@echo "  docs / docs-serve Build / preview documentation"
	@echo "  build             Build native wheel and source distribution"
	@echo "  clean             Remove build and test artifacts"
	@echo "  isort / black     Format imports / Python code"
	@echo "  pre-commit        Run pre-commit hooks"
	@echo "  validate          Validate the changelog"
	@echo "  version-check     Check version consistency"
	@echo "  dev-status        Validate development status"
	@echo "  prerelease-check  Run quality and release metadata checks"
	@echo "  dont-be-lazy      Scan for unfinished work"
	@echo "  pydoc-docs        Generate API documentation"

sync:
	uv sync --frozen --no-install-project --only-group quality

test:
	$(VENV) python -m pytest tests --cov=untruncate_json --cov-branch --cov-report=term-missing --cov-fail-under=90

ruff:
	$(VENV) ruff check .

pylint:
	$(VENV) pylint untruncate_json --fail-under=9.7

mypy:
	$(VENV) mypy untruncate_json

bandit:
	$(VENV) bandit -r untruncate_json

check: ruff pylint mypy bandit test

build:
	uv build

clean:
	$(VENV) python -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in (Path('build'), Path('dist'), Path('htmlcov'), Path('.pytest_cache'), Path('.mypy_cache'), Path('.ruff_cache')) if p.exists()]; [p.unlink() for p in Path('.').glob('.coverage*') if p.is_file()]; [shutil.rmtree(p) for root in ('untruncate_json', 'tests') for p in Path(root).rglob('__pycache__')]"

isort:
	$(DEV) isort untruncate_json tests

black:
	$(DEV) black untruncate_json tests

pre-commit:
	$(DEV) pre-commit run --all-files

version-check:
	$(DEV) jiggle_version check

dev-status:
	$(DEV) troml-dev-status validate .

prerelease-check: check version-check dev-status

dont-be-lazy:
	$(DEV) dont_be_lazy --root . --no-color summary
	$(DEV) dont_be_lazy --root . --no-color scan untruncate_json --no-config-suppressions

pydoc-docs:
	$(DEV) pydoc_fork untruncate_json -o ./pydoc/

validate:
	uv run --frozen --only-group release kaclm validate

docs:
	uv run --frozen --only-group docs mkdocs build --strict

docs-serve:
	uv run --frozen --only-group docs mkdocs serve

zizmor:
	uv run --frozen --only-group security zizmor --persona pedantic --no-ignores --strict-collection .github/workflows

homepage:
	hugo --source landing --minify --gc --panicOnWarning

homepage-serve:
	hugo server --source landing
