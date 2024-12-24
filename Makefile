# isort . && black . && bandit -r . && pylint && pre-commit run --all-files
# Get changed files

FILES := $(wildcard **/*.py)

# if you wrap everything in poetry run, it runs slower.
ifeq ($(origin VIRTUAL_ENV),undefined)
    VENV := poetry run
else
    VENV :=
endif

poetry.lock: pyproject.toml
	@echo "Installing dependencies"
	@poetry install --with dev

clean-pyc:
	@echo "Removing compiled files"
	@find untruncate_json -name '*.pyc' -exec rm -f {} + || true
	@find untruncate_json -name '*.pyo' -exec rm -f {} + || true
	@find untruncate_json -name '__pycache__' -exec rm -fr {} + || true

clean-test:
	@echo "Removing coverage data"
	@rm -f .coverage || true
	@rm -f .coverage.* || true

clean: clean-pyc clean-test

# tests can't be expected to pass if dependencies aren't installed.
# tests are often slow and linting is fast, so run tests on linted code.
test: clean .build_history/pylint .build_history/bandit poetry.lock
	@echo "Running unit tests"
	# $(VENV) python -m unittest discover
	$(VENV) py.test tests --cov=untruncate_json --cov-report=html --cov-fail-under 50

.build_history:
	@mkdir -p .build_history

.build_history/isort: .build_history $(FILES)
	@echo "Formatting imports"
	$(VENV) isort .
	@touch .build_history/isort

.PHONY: isort
isort: .build_history/isort

.build_history/black: .build_history .build_history/isort $(FILES)
	@echo "Formatting code"
	$(VENV) black untruncate_json --exclude .venv
	$(VENV) black tests --exclude .venv
	# $(VENV) black scripts --exclude .venv
	@touch .build_history/black

.PHONY: black
black: .build_history/black

.build_history/pre-commit: .build_history .build_history/isort .build_history/black
	@echo "Pre-commit checks"
	$(VENV) pre-commit run --all-files
	@touch .build_history/pre-commit

.PHONY: pre-commit
pre-commit: .build_history/pre-commit

.build_history/bandit: .build_history $(FILES)
	@echo "Security checks"
	$(VENV)  bandit untruncate_json
	@touch .build_history/bandit

.PHONY: bandit
bandit: .build_history/bandit

.PHONY: pylint
.build_history/pylint: .build_history .build_history/isort .build_history/black $(FILES)
	@echo "Linting with pylint"
	$(VENV) pylint untruncate_json --fail-under 9.7
	@touch .build_history/pylint

# for when using -j (jobs, run in parallel)
.NOTPARALLEL: .build_history/isort .build_history/black

check: test pylint bandit pre-commit

.PHONY: publish
publish_test:
	rm -rf dist && poetry version minor && poetry build && twine upload -r testpypi dist/*

.PHONY: publish
publish: test
	rm -rf dist && poetry build

.PHONY:
docker:
	docker build -t untruncate_json -f Dockerfile .

.PHONY:
pex:
	# linux only
	@poetry export -f requirements.txt --output requirements.txt
	@pex -r "requirements.txt" -e "untruncate_json.cli:main" -o "untruncate_json.pex"

shiv: untruncate_json.pyz
	@shiv untruncate_json -o untruncate_json.pyz --python python --console-script untruncate_json
