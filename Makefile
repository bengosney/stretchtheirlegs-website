.PHONY: help clean test install all init dev css watch node js clean-pyc
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

MAKEFLAGS += -j4

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

SCSS=$(shell find scss/ -name "*.scss")

BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")
DBTOSQLPATH=$(BINPATH)/db-to-sqlite

PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
PIP_PATH:=$(BINPATH)/pip
WHEEL_PATH:=$(BINPATH)/wheel
PRE_COMMIT_PATH:=$(BINPATH)/pre-commit
UV_PATH:=$(BINPATH)/uv

PYTHON_FILES:=$(wildcard ./**/*.py ./**/tests/*.py)

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

requirements.%.txt: $(UV_PATH) requirements.%.in requirements.txt
	@echo "Builing $@"
	$(UV_PATH) pip compile -q -o $@ $(filter-out $<,$^)

requirements.txt: $(UV_PATH) requirements.in
	@echo "Builing $@"
	$(UV_PATH) pip compile -q -o $@ $(filter-out $<,$^)

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: $(PRE_COMMIT_PATH) .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	python -m pip install wheel
	@touch $@

$(UV_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install uv

$(PRE_COMMIT_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install pre-commit
	@touch $@

init: .direnv $(UV_PATH) .git .git/hooks/pre-commit requirements.dev.txt ## Initalise a enviroment

clean-pyc: ## Remove all python build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

clean: clean-pyc ## Remove all build files
	rm -f .testmondata
	rm -rf .hypothesis
	rm -rf .*cache
	rm -f .coverage
	find . -type d -empty -delete

package-lock.json: package.json
	npm install

node_modules: package.json package-lock.json
	npm install
	@touch $@

node: node_modules

python: $(PIP_SYNC_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter-out $<,$^)"
	@python -m piptools sync $(filter-out $<,$^)

install: python node ## Install development requirements (default)

_upgrade: requirements.in
	@echo "Upgrading pip packages"
	@python -m pip install --upgrade pip
	@python -m piptools compile -q --upgrade requirements.in

upgrade: _upgrade python
	@echo "Updateing module paths"
	wagtail updatemodulepaths --ignore-dir .direnv
	python -m pre_commit autoupdate

$(DBTOSQLPATH):
	pip install git+https://github.com/bengosney/db-to-sqlite.git

db.sqlite3: $(DBTOSQLPATH)
	db-to-sqlite $(shell heroku config | grep DATABASE_URL | tr -s " " | cut -d " " -f 2) $@ --all --skip "cerberus_*" -p

stl/static/css/%.css: scss/%.scss $(SCSS)
	npx sass $< $@

stl/static/css/%.min.css: stl/static/css/%.css postcss.config.js
	npx postcss $< -o $@
	@touch $@

css: stl/static/css/main.min.css ## Build the css

JS_SRC = $(wildcard js/*.ts)
JS_LIB = $(JS_SRC:js/%.ts=stl/static/js/%.js)

stl/static/js/: $(JS_LIB)
stl/static/js/%.js: js/%.ts $(JS_SRC)
	@mkdir -p $(@D)
	npx parcel build $< --dist-dir $(@D)
	@touch $@

js: stl/static/js/stl.js ## Build the js

watch-css: ## Watch and build the css
	@echo "Watching scss"
	$(MAKE) css
	@while inotifywait -qr -e close_write scss/; do \
		$(MAKE) css; \
	done

watch-js: ## Watch and build the js
	@echo "Watching js"
	$(MAKE) js
	@while inotifywait -qr -e close_write js/; do \
		$(MAKE) js; \
	done

bs: ## Run browser-sync
	browser-sync start --proxy localhost:8000 --files "./**/*.css" --files "./**/*.js" --files "./**/*.html"

cov.xml: $(PYTHON_FILES)
	python3 -m pytest --cov=. --cov-report xml:$@

coverage: $(PYTHON_FILES)
	python3 -m pytest --cov=. --cov-report html:$@

_server:
	python3 ./manage.py migrate
	python3 ./manage.py runserver

dev: _server watch-js watch-css bs ## Start the dev server, watch the css and js and start browsersync

infrastructure:
	git clone https://github.com/bengosney/tofu-wagtail.git $@
	cd $@ && $(MAKE) init
