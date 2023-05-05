.PHONY: docs

SHELL := /bin/bash

help: ## show this message
	@awk \
		'BEGIN {FS = ":.*##"; printf "\nUsage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' \
		$(MAKEFILE_LIST)

fix-black: ## automatically fix all black errors
	@poetry run black .

fix-isort: ## automatically fix all isort errors
	@poetry run isort .

fix-md: ## automatically fix markdown format errors
	@poetry run pre-commit run mdformat --all-files

lint: lint-black lint-isort lint-pyright lint-flake8 ## run linters

lint-black: ## run black
	@echo "Running black... If this fails, run 'make fix-black' to resolve."
	@poetry run black . --check --color --diff
	@echo ""

lint-flake8: ## run flake8
	@echo "Running flake8..."
	@poetry run flake8
	@echo ""

lint-isort: ## run isort
	@echo "Running isort... If this fails, run 'make fix-isort' to resolve."
	@poetry run isort . --check-only
	@echo ""

lint-pyright: ## run pyright
	@echo "Running pyright..."
	@npx pyright --venv-path ./
	@echo ""

run-pre-commit: ## run pre-commit for all files
	@poetry run pre-commit run -a

setup: setup-poetry setup-pre-commit setup-npm ## setup dev environment

setup-npm: ## install node dependencies with npm
	@npm ci

setup-poetry: ## setup python virtual environment
	@if [[ -d .venv ]]; then \
		poetry run python -m pip --version >/dev/null 2>&1 || rm -rf ./.venv/* ./.venv/.*; \
	fi
	@poetry lock --check
	@poetry install $(POETRY_OPTS) --sync

setup-pre-commit: ## install pre-commit git hooks
	@poetry run pre-commit install

spellcheck: ## run cspell
	@echo "Running cSpell to checking spelling..."
	@npx cspell "**/*" \
		--color \
		--config .vscode/cspell.json \
		--must-find-files \
		--no-progress \
		--relative \
		--show-context

test: ## run tests
	# @poetry run pytest \
	#	--cov runway \
	#	--cov-report term-missing:skip-covered \
	#	--dist loadfile \
	#	--numprocesses auto
	@echo "Success!"
