.PHONY: clean docs package run clean_raw clean_de clean_features start_jupyter

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DATA_DIR := $(realpath data)
BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
PROFILE = default
PROJECT_NAME = phantasyfootballer
PYTHON_INTERPRETER = python

## Execute the kedro run command
run:
	kedro run

download_data: clean_raw
	kedro run --pipeline
## Transform all notebooks to scripts (use the path for 1 notebook)
notebook_convert:
	kedro jupyter convert --all

## Clean up the raw data files
clean-raw:
	rm -fv data/01_raw/*

## Clean intermediate files
clean-intermediate:
	rm -fv data/02_intermediate/*

## Clean primary data
clean-primary:
	rm -fv data/03_primary/*

## Remove files associated with data engineering
clean-de: clean-primary clean-intermediate

## delete data features
clean-features:
	rm -fv data/04_feature/*

## delete all generated data
clean-data: clean-features clean-primary clean-intermediate clean-raw

## Clean up the old files
clean:
	rm -fv src/dist/.

## Package the Python code in to an .egg and .wheel
package: clean
	kedro package

## Do all the pre-checks
pre-check:
	black .
	flake8
	mypy

## Update version for a patch (these get pulled into the repo)
patch: pre-check
	bump2version --tag --commit patch

## Update version on each commit
build: pre-check
	bump2version build

## Update version that will be released (takes off the dev tag)
release: pre-check
	bump2version release

## Build api odx using Sphinx
docs:
	kedro build-docs

## Install Python Dependencies
requirements:
	kedro build-reqs

## Start jupyter
start_jupyter:
	jupyter notebook --ip=0.0.0.0 \
		--port=7999 --allow-root --no-browser \
		--notebook-dir /workspaces/phantasyfootballer/notebooks --autoreload

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
