#!/usr/bin/make

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install webcomponents dependencies
	npm install

.PHONY: build
build: ## Build the production bundle
	npm run build

.PHONY: watch
watch:  ## Start a Webpack dev server and watch for resources changes
	npm run watch

.PHONY: lint
lint:  ## Run ESLint to check code for errors
	npm run lint

.PHONY: fix-codestyle
fix-codestyle:  ## Run prettier and fix code style
	npm run prettier:fix
