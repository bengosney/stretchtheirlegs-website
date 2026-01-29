.PHONY: help clean test install all init dev css watch node js clean-pyc cog COGABLE
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

REQS=$(shell python -c 'import tomllib;[print(f"requirements.{k}.txt") for k in tomllib.load(open("pyproject.toml", "rb"))["project"]["optional-dependencies"].keys()]')

SCSS=$(shell find scss/ -name "*.scss")

PYTHON_VERSION:=$(shell cat .python-version)
VENV_PATH:=.venv
DBTOSQLPATH=$(VENV_PATH)/bin/db-to-sqlite

UV_PATH:=$(shell command -v uv 2>/dev/null || echo ~/.cargo/bin/uv)
PRE_COMMIT:=$(UV_PATH) tool run pre-commit

COGABLE:=$(shell git ls-files | xargs grep -l "\[\[\[cog")
PYTHON_FILES:=$(wildcard ./**/*.py ./**/tests/*.py)

check_command = @command -v $(1) >/dev/null 2>&1 || { echo >&2 "$(1) is not installed."; $(2); }

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml: | .git
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@
	$(PRE_COMMIT) autoupdate

requirements.%.txt: $(UV_PATH) requirements.txt pyproject.toml
	@echo "Building $@"
	$(UV_PATH) pip compile --quiet --generate-hashes -o $@ --extra $* $(filter-out $<,$^)

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Building $@"
	$(UV_PATH) pip compile --quiet --generate-hashes -o $@ $(filter-out $<,$^)

.git/hooks/pre-commit: .pre-commit-config.yaml .git
	$(PRE_COMMIT) install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo 'if [ ! -d $(VENV_PATH) ]; then' > $@
	@echo '    make $(VENV_PATH)' >> $@
	@echo 'fi' >> $@
	@echo '' >> $@
	@echo 'PATH_add "$(VENV_PATH)/bin"' >> $@
	@echo 'export VIRTUAL_ENV="$$PWD/$(VENV_PATH)"' >> $@
	@echo 'export VIRTUAL_ENV_PROMPT="$$(basename $$PWD)"' >> $@
	@echo 'watch_file $(VENV_PATH)' >> $@
	@touch -d '+1 minute' $@
	@false

$(VENV_PATH): $(UV_PATH) .python-version
	$(UV_PATH) venv --python $(PYTHON_VERSION)

cog: $(UV_PATH) $(COGABLE)
	@uv tool run --from cogapp cog -rc $(filter-out $<,$^)

init: .envrc .git .git/hooks/pre-commit requirements.txt requirements.dev.txt ## Initalise a enviroment

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

python: $(VENV_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter-out $<,$^)"
	@$(UV_PATH) pip sync $(filter-out $<,$^)

install: python node ## Install development requirements (default)

upgrade: python
	@echo "Updateing module paths"
	wagtail updatemodulepaths --ignore-dir $(VENV_PATH)
	$(PRE_COMMIT) autoupdate

db.sqlite3: | $(UV_PATH) ## Import the database from heroku
	$(call check_command,heroku,exit 1)
	$(call check_command,db-to-sqlite,uv pip install db-to-sqlite)
	db-to-sqlite $(shell heroku config | grep DATABASE_URL | tr -s " " | cut -d " " -f 2) $@ --all --skip "cerberus_*" -p

stl/static/css/%.css: scss/%.scss $(SCSS) node_modules
	npx sass $< $@

stl/static/css/%.min.css: stl/static/css/%.css postcss.config.js node_modules
	npx postcss $< -o $@
	@rm -f $<.map
	@touch $@

css: stl/static/css/main.min.css ## Build the css

JS_SRC = $(wildcard js/*.ts)
JS_LIB = $(JS_SRC:js/%.ts=stl/static/js/%.js)

stl/static/js/: $(JS_LIB)
stl/static/js/%.min.js: js/%.ts $(JS_SRC)
	@mkdir -p $(@D)
	npx esbuild $< --bundle --minify --sourcemap --outfile=$@
	@touch $@

stl/static/js/snow.min.js:
	curl https://app.embed.im/snow.js > $@

stl/static/js/fireworks.min.js:
	curl https://cdn.jsdelivr.net/npm/fireworks-js@latest/dist/fireworks.js > $@

stl/static/js/tsparticles.min.js:
	curl https://cdn.jsdelivr.net/npm/tsparticles@2.9.3/tsparticles.bundle.min.js > $@

js: stl/static/js/stl.min.js stl/static/js/snow.min.js stl/static/js/fireworks.min.js stl/static/js/tsparticles.min.js ## Build the js

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
