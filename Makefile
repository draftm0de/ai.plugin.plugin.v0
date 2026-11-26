# Managed by the plugin manager: do not edit. Own targets and variables belong into CUSTOM.mk.
export PYTHONDONTWRITEBYTECODE := 1
PYTHON ?= python3
SOURCE ?= .
TEST_GROUP ?=
CLI ?= claude
.SUFFIXES:
.DEFAULT_GOAL := help
.PHONY: help sync check test verify build-skeleton-hashes test-behavior install-hooks
help:
	@echo 'sync / check          Generate / validate the committed host metadata'
	@echo 'test                  Deterministic tests; TEST_GROUP=<name> selects a component'
	@echo 'verify                Read-only structure checks; REVIEW=1 adds the scope review'
	@echo 'build-skeleton-hashes Rebuild the hash files of sync templates; without such templates nothing happens'
	@echo 'test-behavior         Optional model cases, CLI=claude|codex (may consume credits)'
	@echo 'install-hooks         Activate the pre-commit check for this clone'
	@echo 'Local installation: run make install-local in the marketplace of this plugin.'
sync:
	$(PYTHON) scripts/plugin.py sync
check:
	$(PYTHON) scripts/plugin.py check
test:
	$(PYTHON) -B scripts/run_tests.py --kind deterministic $(if $(TEST_GROUP),--group "$(TEST_GROUP)",)
verify:
	$(PYTHON) scripts/verify/structure.py --source "$(SOURCE)"
	$(PYTHON) scripts/verify/standards.py --source "$(SOURCE)"
	$(PYTHON) scripts/verify/conventions.py --source "$(SOURCE)"
	$(PYTHON) scripts/verify/docs.py --source "$(SOURCE)"
	$(PYTHON) scripts/verify/hashes.py --source "$(SOURCE)"
	$(if $(filter 1,$(REVIEW)),$(PYTHON) scripts/verify/scope.py --source "$(SOURCE)",)
build-skeleton-hashes:
	$(PYTHON) -B scripts/build_hashes.py
test-behavior:
	$(PYTHON) -B tests/behavior/run_cases.py --cli $(CLI)
install-hooks:
	git config core.hooksPath githooks

# Own targets of this repository; optional.
-include CUSTOM.mk
