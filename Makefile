#!/usr/bin/make
VENV_FOLDER=.venv

ifeq (, $(shell which uv ))
  $(error "[ERROR] The 'uv' command is missing from your PATH. Install it from: https://docs.astral.sh/uv/getting-started/installation/")
endif

.PHONY: buildout cleanall help release start test test-coverage

help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(VENV_FOLDER):
	@echo "Creating virtual environment with uv"
	uv venv

$(VENV_FOLDER)/bin/buildout: $(VENV_FOLDER)
	@echo "Installing requirements with uv pip interface"
	uv pip install --python $(VENV_FOLDER)/bin/python -r requirements.txt

buildout: $(VENV_FOLDER)/bin/buildout ## Install dependencies with buildout
	$(VENV_FOLDER)/bin/buildout -t 7

release: ## Run full release with uvx zest.releaser
	uvx --from zest.releaser fullrelease

test: buildout ## Run tests
	./bin/test

test-coverage: buildout ## Run tests with coverage (fails under 90%)
	./bin/test-coverage

start: buildout ## Start the development server
	ALLOWED_DISTRIBUTIONS=classic ./bin/instance fg

cleanall: ## Clean development environment
	rm -rf .venv pyvenv.cfg bin develop-eggs downloads eggs include lib lib64 parts .installed.cfg .mr.developer.cfg bootstrap.py parts/omelette local share
