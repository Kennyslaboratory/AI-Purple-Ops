# Development Roadmap

## Project Vision

Build a production-ready backend that powers AI security testing with:
- **Safety Lane**: Content policy enforcement and harm detection
- **Security Lane**: Adversarial testing (prompt injection, RAG attacks, tool exploits)
- **Compliance Lane**: Evidence automation for NIST AI RMF, EU AI Act, FedRAMP
- **Recipe System**: Pre-configured workflows for instant evaluation

---

## Current Status: v0.6.2 (b07+ Complete)

**Production-Ready Components:**
- ✅ Core harness (adapters, runners, reporters)
- ✅ 4 production adapters (OpenAI, Anthropic, HuggingFace, Ollama)
- ✅ 9 test suites with 133+ test cases
- ✅ 2 detectors (HarmfulContent, ToolPolicy)
- ✅ Quality gates with threshold enforcement
- ✅ Recipe engine with 4 working recipes
- ✅ 4 tool integrations (PyRIT, Garak, Promptfoo, PromptInject)
- ✅ Evidence automation (JSON, JUnit, HTML, Evidence Pack)
- ✅ 211 tests passing, 80%+ coverage

---

## Phase Summary

| Phase | Status | Version | Description |
|-------|--------|---------|-------------|
| b01 | ✅ Complete | v0.1.0 | Governance, compliance mappings, schemas |
| b02 | ✅ Complete | v0.2.0 | Dev tooling, config system, tool registry |
| b03 | ✅ Complete | v0.3.0 | CLI skeleton with Typer |
| b04 | ✅ Complete | v0.4.0 | Mock runner, JSON/JUnit reporters |
| b05 | ✅ Complete | v0.5.0 | Detectors and policy enforcement |
| b06 | ✅ Complete | v0.6.0 | Gates, evidence packs, recipe engine |
| b07 | ✅ In Production | v0.6.x | Real adapters, test suites, tool integrations |
| b08 | 📋 Planned | v0.8.0 | Tool simulation sandbox, ACL enforcement |
| b09 | 📋 Planned | v0.9.0 | Enhanced CI/CD, recipe validation |
| b10 | 📋 Planned | v1.0.0 | Production API service, recipe marketplace |

---

## Completed Phases

### b01: Foundation (v0.1.0) ✅
- Machine-readable compliance mappings (NIST, EU, FedRAMP)
- JSON schemas for run summaries, evidence manifests
- Security policies and usage guidelines
- OpenAPI 3.0 specification

### b02: Development Infrastructure (v0.2.0) ✅
- Python build system (pyproject.toml, Makefile)
- Code quality tools (ruff, black, mypy, bandit)
- Configuration system (YAML + env var precedence)
- Professional logging with Rich
- Automated testing (pytest, hypothesis)
- Tool registry: 22 AI-security tools

### b03: CLI Skeleton (v0.3.0) ✅
- Typer-based CLI (`run`, `gate`, `version` commands)
- Config override support (CLI args + env vars)
- Core protocol definitions (Adapter, Runner, Reporter, Gate)
- Integration tests

### b04: Test Execution (v0.4.0) ✅
- MockAdapter with deterministic responses
- MockRunner for streaming test execution
- YAML suite loader (Nuclei-style definitions)
- JSONReporter and JUnitReporter
- Rich progress output
- 92 tests passing

### b05: Policy Enforcement (v0.5.0) ✅
- HarmfulContentDetector (violence, hate, self-harm, sexual content, PII)
- ToolPolicyDetector (allowlist enforcement)
- Policy loader with YAML configuration
- Severity levels (low, medium, high, critical)
- SLO threshold monitoring
- 140+ tests passing

### b06: Quality Gates (v0.6.0) ✅
- Threshold-based quality gates
- Evidence pack generation (ZIP files with manifest)
- Recipe engine foundation
- Recipe executor for workflow orchestration
- Recipe CLI commands (`recipe run`, `recipe list`, `recipe validate`)
- 4 reference recipes
- 170+ tests passing

### b07: Production Features (v0.6.x) ✅
**Real Adapters:**
- OpenAI adapter (GPT-4, GPT-3.5-turbo)
- Anthropic adapter (Claude 3)
- HuggingFace adapter (local models)
- Ollama adapter (local Ollama models)

**Test Suites (9 suites, 133+ cases):**
- adversarial/ (jailbreaks, prompt injection)
- rag/ (RAG poisoning, data leakage)
- ui/ (XSS, SSRF injection attacks)
- redteam/ (advanced adversarial prompts)
- policies/ (content safety validation)
- normal/ (utility baseline)
- adapters/ (adapter health checks)
- comparison/ (multi-model benchmarking)

**Tool Integrations:**
- PyRIT (Microsoft's risk identification toolkit)
- Garak (LLM vulnerability scanner)
- Promptfoo (LLM testing framework)
- PromptInject (prompt injection detection)

**Status:**
- 211 tests passing
- 80%+ code coverage
- Production-ready

---

## Upcoming Phases

### b08: Tool Simulation (v0.8.0) 📋
**Goal:** Safe execution environment for testing AI agents with tool access.

**Features:**
- Tool execution sandbox
- ACL enforcement and permission checking
- Input/output redaction for sensitive data
- Schema validation for tool calls
- Tool misuse detection

**Deliverables:**
- Safe tool execution environment
- Tool policy enforcer
- 5 compliance recipes (NIST, EU, FedRAMP, ISO, SOC2)
- Tool simulation test suite

**Success Criteria:**
- Tools execute in isolated sandbox
- Dangerous operations blocked
- All tool calls logged and auditable

### b09: CI/CD Enhancement (v0.9.0) 📋
**Goal:** Production-grade CI/CD integration and recipe validation.

**Features:**
- Enhanced GitHub Actions workflows
- Recipe validation in pre-commit hooks
- Automated recipe testing
- Branch protection with security gates
- Release automation
- Docker containers for reproducible testing

**Deliverables:**
- Complete CI/CD pipeline
- Recipe validation framework
- Docker images
- Nightly security scan automation

**Success Criteria:**
- All PRs blocked if security gates fail
- Recipes validated automatically
- Docker images published on release

### b10: Production Backend (v1.0.0) 📋
**Goal:** Production-ready API service and community ecosystem.

**Features:**
- FastAPI service with OpenAPI spec
- Recipe marketplace (community contributions)
- Web UI (view results, manage recipes)
- Observability and monitoring
- Production deployment artifacts
- Multi-tenant support

**Deliverables:**
- Production API service
- Recipe marketplace
- Web UI
- Docker Compose stack
- Kubernetes manifests
- Production runbooks

**Success Criteria:**
- API service handles 100+ concurrent requests
- Recipe marketplace has 25+ community recipes
- Web UI provides full workflow management
- Production deployment in <30 minutes

---

## Development Principles

1. **Demo-Ready Every Phase** - Each phase delivers working features
2. **Test-First Development** - Write tests before implementation
3. **Small Pull Requests** - Keep changes focused and reviewable
4. **Production Quality** - Every phase meets production standards
5. **User-Focused** - Features solve real security testing problems

---

## How to Contribute

Each development phase follows a 6-step process:

1. **Branch** - Create `bNN-short-slug` from main
2. **Design** - Write threat model and ADR if needed
3. **Test** - Write pytest tests (test-first development)
4. **Implement** - Build feature with manual validation
5. **Polish** - Run linting, update docs and CHANGELOG
6. **Review** - Submit PR, address feedback

See [CONTRIBUTING.md](../CONTRIBUTING.md) for complete workflow.

---

## Version History

- **v0.6.2** (2025-11-08) - Documentation overhaul
- **v0.6.1** (2025-11-07) - Critical bug fixes, security hardening
- **v0.6.0** (2025-11-06) - Quality gates, evidence packs, recipe engine
- **v0.5.0** (2025-11-05) - Policy enforcement, detectors
- **v0.4.0** (2025-11-04) - Mock runner, reporters
- **v0.3.0** (2025-11-03) - CLI skeleton
- **v0.2.0** (2025-11-02) - Development tooling
- **v0.1.0** (2025-11-01) - Initial foundation

---

## Long-Term Vision

**Near-Term (6 months)**
- Complete b08-b10 phases
- Reach 25+ community recipes
- Launch recipe marketplace
- Deploy production API service

**Medium-Term (12 months)**
- Expand to 50+ AI security tools
- Support for more model providers
- Advanced fuzzing and property-based testing
- Compliance automation for additional frameworks

**Long-Term (24+ months)**
- Become the standard for AI security testing
- Power enterprise security testing workflows
- Enable automated compliance for all major frameworks
- Build thriving community ecosystem
