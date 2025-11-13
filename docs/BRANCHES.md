# Branch map

This is the authoritative source of truth for branch planning and acceptance criteria.

## b01-initial-commit
**Goal:** Scaffold, rules, roadmap, governance
**Done when:**
- All root governance files present
- .cursor/rules contains 6-step dev loop
- SECURITY_CONTACTS.md exists
- USAGE_POLICY.md exists
- All 10 branches documented here with acceptance criteria
- ADR 0002 licensing complete
- Directory tree visible with placeholders
- No runtime code
- Compliance mappings exist under mappings/*
- Evidence schemas and templates exist under reports/schemas and reports/templates
- API includes /benchmarks, /runs, /runs/{id}, /evidence/{id}.zip
- Deprecation registry exists under registry/*

## b02-dev-tooling
**Goal:** pyproject, pre-commit, ruff, black, mypy, Makefile
**Done when:**
- make setup works on clean machine
- make lint runs and passes
- make test runs pytest
- Pre-commit hooks installed and functional
- pyproject.toml has all base dependencies
- Basic smoke test passes

## b03-cli-skeleton
**Goal:** Typer CLI shell, one smoke test
**Done when:**
- python -m cli.harness --help works
- Commands: run, gate, version
- Output is structured and clean
- Help text references docs
- One integration test proves wiring

## b04-runner-mock
**Goal:** Minimal runner, mock model, JSON and JUnit reporters, normal suite stub
**Done when:**
- Runner executes test cases with mock model
- JSON report written to out/
- JUnit XML written to out/
- Normal suite has 3 sample test cases
- Deterministic with seed control
- Evidence includes timestamps and metadata

## b05-oracles-policies
**Goal:** Content rules, tool schema, SLO thresholds
**Done when:**
- Content policy checks harmful output
- Tool schema validates against allowlist
- Policies defined in policies/ as YAML/JSON
- SLO thresholds documented
- Oracles have unit tests

## b06-gate-and-reports
**Goal:** Stop ship gate and evidence JSON and JUnit **+ Recipe engine**
**Done when:**
- make gate command works
- Gate fails on threshold breach
- Exit code 1 on failure, 0 on success
- Evidence pack links to all artifacts
- Reports include pass/fail summary
- **IMPORTANT**: Change gate default behavior to fail (exit 1) when summary not found if gates enabled
- **Recipe engine can load and execute YAML recipes**
- **3 reference recipes work end-to-end (safety, security, compliance)**
- **CLI commands: recipe run, recipe list, recipe validate**
- **Recipe schema documented in docs/RECIPES.md**

## b07-redteam-rag-ui-fuzz
**Goal:** Adversarial corpora, RAG leakage, UI XSS, Hypothesis fuzz **+ Security recipes**
**Done when:**
- Red-team suite has 20+ adversarial prompts
- RAG suite tests for leakage and poisoning
- UI suite has XSS and injection cases
- Fuzz tests run with Hypothesis
- All suites integrated into battery
- **6 security recipes implemented (OWASP LLM focus)**
- **Recipe testing framework with fixtures**

## b08-retrievers-simtools
**Goal:** ACL and redaction, simulated tools, action schema **+ Compliance recipes**
**Done when:**
- Retriever adapter with ACL checks
- Redaction for PII and secrets
- Simulated tools (file, http, db) with schema
- Tool allowlist enforcement
- Action validation before execution
- **5 compliance recipes implemented (NIST, EU, FedRAMP, ISO)**
- **Evidence pack templates for each framework**

## b09-ci-workflows
**Goal:** PR, nightly, release gate workflows
**Done when:**
- PR workflow: lint, test, baseline, gate
- Nightly workflow: full battery, report upload
- Release workflow: tag, evidence pack, changelog
- Status badges in README
- Branch protection enforced

## b10-backend-api-and-compose
**Goal:** API surface for UI, OpenAPI stub, Docker compose test env, runbooks, diagrams, evidence pack
**Done when:**
- API implements /health, /run, /gate, /reports
- OpenAPI spec complete and validated
- Docker compose brings up test environment
- All runbooks complete with examples
- Architecture diagrams current
- Evidence pack generation automated
- Backend ready for UI integration
