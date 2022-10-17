.PHONY: help clean test install all init dev
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

SCSS=$(shell find scss/ -name "*.scss")

DBTOSQLPATH=".direnv/python-3.10.8/bin/db-to-sqlite"

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@
	python -m pip install pre-commit
	pre-commit autoupdate

requirements.%.in:
	echo "-c requirements.txt" > $@

requirements.in:
	@touch $@

requirements.%.txt: requirements.%.in requirements.txt
	@echo "Builing $@"
	@python -m piptools compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@python -m piptools compile -q $^

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
	@touch -d '+1 minute' $@
	@false

init: .direnv .git .git/hooks/pre-commit requirements.dev.txt ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata
	rm -rf .mypy_cache
	rm -rf .hypothesis

package-lock.json: package.json
	npm install

node_modules: package.json package-lock.json
	npm install
	touch $@

node: node_modules

python: requirements.txt $(REQS)
	@echo "Installing $^"
	@python -m piptools sync $^

install: python node ## Install development requirements (default)

dev: init install ## Start work
	code .

upgrade: requirements.in
	@echo "Upgrading pip packages"
	@python -m piptools compile -q --upgrade requirements.in

$(DBTOSQLPATH):
	pip install 'db-to-sqlite[postgresql]'

db.sqlite3: $(DBTOSQLPATH)
	db-to-sqlite $(shell heroku config | grep DATABASE_URL | tr -s " " | cut -d " " -f 2) $@ --all -p

stl/static/css/%.css: scss/%.scss $(SCSS)
	npx sass $< $@

stl/static/css/%.min.css: stl/static/css/%.css
	npx postcss $^ > $@

css: stl/static/css/main.min.css
