.DEFAULT_GOAL := help

# Porcelain
# ###############
.PHONY: run init todo recreate-db

run: setup bd.db ## run the app
	uvicorn src.main:app --reload

# TODO: add docker

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

init: ## one time setup
	direnv allow .

recreate-db: remove-db bd.db ## get a fresh database
	@# noop


# Plumbing
# ###############
.PHONY: setup remove-db

bd.db:
	./migrate.py

remove-db:
	rm -f bd.db

setup:
	@# noop


# Utilities
# ###############
.PHONY: help
help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
