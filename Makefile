SHELL := /bin/bash
.PHONY: help setup lint fmt type sec audit test smoke clean ci

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

ci: lint type sec test ## Run core checks (audit not included, see help)
