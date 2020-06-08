.DEFAULT_GOAL := help

# Porcelain
# ###############
.PHONY: run init todo

run: setup ## run the app
	uvicorn src.main:app --reload

# TODO: add docker

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

init: ## one time setup
	direnv allow .


# Plumbing
# ###############
.PHONY: setup remove-main-db

main.db:
	WEAHTER_API_URL="noop" WEAHTER_API_KEY="noop" ADMIN_USERNAME="admin" ADMIN_PASSWORD="gExmNMLyzdUwQXfhTGmsyKqHloiZVF" python migrate.py

remove-main-db:
	rm -f main.db

setup:
	@# noop


# Utilities
# ###############
.PHONY: help
help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
