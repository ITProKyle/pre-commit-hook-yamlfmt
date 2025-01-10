CI := $(if $(CI),yes,no)
SHELL := /bin/bash

ifeq ($(CI), yes)
	POETRY_OPTS = "-v"
	PRE_COMMIT_OPTS = --show-diff-on-failure --verbose
endif

help: ## show this message
	@awk \
		'BEGIN {FS = ":.*##"; printf "\nUsage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' \
		$(MAKEFILE_LIST)

fix-black: ## automatically fix all black errors
	@poetry run black .

fix-md: ## automatically fix markdown format errors
	@poetry run pre-commit run mdformat --all-files

fix-ruff: ## automatically fix everything ruff can fix (implies fix-imports)
	@poetry run ruff check . --fix-only

lint: lint-black lint-ruff lint-pyright ## run all linters

lint-black: ## run black
	@echo "Running black... If this fails, run 'make fix-black' to resolve."
	@poetry run black . --check --color --diff
	@echo ""

lint-pyright: ## run pyright
	@echo "Running pyright..."
	@npm exec --no -- pyright --venvpath ./
	@echo ""

lint-ruff: ## run ruff
	@echo "Running ruff... If this fails, run 'make fix-ruff' to resolve some error automatically, other require manual action."
	@poetry run ruff check .
	@echo ""

run-pre-commit: ## run pre-commit for all files
	@poetry run pre-commit run $(PRE_COMMIT_OPTS) \
		--all-files \
		--color always

setup: setup-poetry setup-pre-commit setup-npm ## setup dev environment

setup-npm: ## install node dependencies with npm
	@npm ci

setup-poetry: ## setup python virtual environment
	@poetry sync $(POETRY_OPTS) --ansi

setup-pre-commit: ## install pre-commit git hooks
	@poetry run pre-commit install

spellcheck: ## run cspell
	@echo "Running cSpell to checking spelling..."
	@npm exec --no -- cspell lint . \
		--color \
		--config .vscode/cspell.json \
		--dot \
		--gitignore \
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
