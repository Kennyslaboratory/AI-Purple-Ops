SHELL := /bin/bash
.PHONY: help setup lint fmt type sec audit test smoke clean ci docs-tables docs-check

VENV := .venv
ifeq ($(OS),Windows_NT)
	PY := $(VENV)/Scripts/python.exe
	PIP := $(VENV)/Scripts/pip.exe
	PRE := $(VENV)/Scripts/pre-commit.exe
	PYTEST := $(VENV)/Scripts/pytest.exe
else
	PY := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
	PRE := $(VENV)/bin/pre-commit
	PYTEST := $(VENV)/bin/pytest
endif

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make <target>\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-16s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Create venv, install deps, enable hooks
	python -m venv $(VENV)
	$(PY) -m pip install -U pip
	$(PIP) install -e ".[dev]"
	$(PRE) install || true

lint: ## Ruff + Black check
	@if [ "$(OS)" = "Windows_NT" ]; then \
		$(VENV)/Scripts/ruff.exe check . && $(VENV)/Scripts/black.exe --check .; \
	else \
		$(VENV)/bin/ruff check . && $(VENV)/bin/black --check .; \
	fi

fmt: ## Auto-format with Ruff fmt + Black
	$(VENV)/bin/ruff format . || $(VENV)/Scripts/ruff.exe format .
	$(VENV)/bin/black . || $(VENV)/Scripts/black.exe .

type: ## mypy type-check
	@if [ "$(OS)" = "Windows_NT" ]; then \
		$(VENV)/Scripts/mypy.exe src; \
	else \
		$(VENV)/bin/mypy src; \
	fi

sec: ## Bandit SAST
	@if [ "$(OS)" = "Windows_NT" ]; then \
		$(VENV)/Scripts/bandit.exe -q -r src -ll; \
	else \
		$(VENV)/bin/bandit -q -r src -ll; \
	fi

audit: ## pip-audit dependencies (non-fatal, informational only)
	$(PY) -m pip_audit -s moderate || true

test: ## Run pytest
	$(PYTEST)

smoke: ## Self-healing preflight + style demo
	$(PY) scripts/dev_smoke.py

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .mypy_cache dist build *.egg-info

api.up: ## Start FastAPI stub server on port 8080
	python -m uvicorn api.stub_server:app --reload --port 8080

evidence.test: ## Create and verify sample evidence pack
	python scripts/evidence_roundtrip.py

ci: lint type sec test ## Run core checks (audit not included, see help)

docs-tables: ## Generate docs tables (docs/generated/*) and update README placeholders
	$(PY) scripts/generate_docs_tables.py

docs-check: docs-tables ## Fail if generated docs tables drift from committed outputs
	git diff --exit-code -- docs/generated README.md

toolkit: ## Install and verify redteam tools
	@echo "=== Installing Redteam Toolkit ==="
	aipop tools install --stable || $(PY) -m cli.harness tools install --stable
	@echo ""
	@echo "=== Verifying Tool Installation ==="
	aipop tools check || $(PY) -m cli.harness tools check
	@echo ""
	@echo "=== Running Tool Health Checks ==="
	@$(PY) scripts/test_toolkit.py || echo "Toolkit test script not found - skipping health checks"

toolkit.update: ## Update toolkit to latest versions
	aipop tools update || $(PY) -m cli.harness tools update

toolkit.check: ## Check toolkit installation status
	aipop tools check || $(PY) -m cli.harness tools check
