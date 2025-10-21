# AI Purple Ops

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](docs/ROADMAP.md)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](pyproject.toml)

**A vendor-neutral testing harness for AI Safety, Security, and Compliance evaluation.**

AI Purple Ops provides a unified backend infrastructure for evaluating AI systems across three critical dimensions: safety (content & policy), security (tools & data), and compliance (regulatory frameworks). Built to power testing workflows from development through production release gates.

## Overview

AI Purple Ops addresses the gap between AI capability development and deployment readiness. As AI systems gain agency—making decisions, invoking tools, and accessing sensitive data—traditional security testing approaches fall short. This framework provides:

- **Compliance-First Architecture**: Machine-readable mappings to NIST AI RMF, EU AI Act, and FedRAMP controls
- **Evidence Automation**: Structured JSON schemas for audit trails, conformance reports, and evidence packs
- **Vendor Neutrality**: Adapter-based design for models, platforms, and tooling integration
- **API-Driven Design**: RESTful endpoints for orchestrating tests, retrieving results, and managing benchmarks
- **Reproducibility**: Deterministic test execution with seed control and fixture management
- **Comprehensive Tooling**: Integration catalog of 35 security tools across 11 categories

### Three-Lane Testing Approach

Modern AI systems require purple team thinking—combining offensive security (red team) and defensive validation (blue team) with safety evaluation and compliance documentation. AI Purple Ops unifies these workflows across three operational lanes:

| **Safety Lane** | **Security Lane** | **Compliance Lane** |
|-----------------|-------------------|---------------------|
| Content policy violations | Prompt injection attacks | NIST AI RMF measures |
| Harmful output detection | Tool misuse and privilege escalation | EU AI Act Article 15 |
| Bias and fairness metrics | Data exfiltration and RAG leakage | FedRAMP control mappings |
| PII leakage prevention | SSRF, RCE, XSS in agents | Evidence pack generation |

## Quick Start

**Current Status:** Phase b02 (Development Tooling) complete. Core evaluation framework begins in b04.

```bash
# Clone the repository
git clone https://github.com/Kennyslaboratory/AI-Purple-Ops.git
cd AI-Purple-Ops

# Setup development environment
make setup

# Run smoke test
make smoke

# Run development checks (lint, type, security, tests)
make ci

# Available commands
make help
```

### Configuration

Configuration is loaded from `configs/harness.yaml` with environment variable overrides. Set `AIPO_*` variables to override configuration values (e.g., `AIPO_OUTPUT_DIR`, `AIPO_LOG_LEVEL`). See [src/harness/utils/config.py](src/harness/utils/config.py) for implementation details.

## Features

### Implemented (b01-b02)

**Governance and Compliance Infrastructure (b01)**
- Comprehensive security policies and usage guidelines for offensive security tooling
- Machine-readable compliance mappings for NIST AI RMF, EU AI Act, and FedRAMP
- JSON schemas for run summaries, evidence manifests, and conformance reports
- OpenAPI 3.0 specification with endpoints for benchmarks, runs, and evidence retrieval
- Development workflow rules and ADR process documentation

**Development Tooling (b02)**
- Complete Python build system (pyproject.toml, Makefile with 10 targets)
- Strict code quality enforcement (ruff, black, mypy with strict mode, bandit, pip-audit)
- Self-healing configuration system (YAML + environment variable precedence)
- Professional console logging with structured output
- Automated testing infrastructure (pytest, hypothesis integration)
- Pre-commit hooks with secrets detection
- Comprehensive tool registry: 35 security tools across 11 categories

### In Development (b03-b10)

**CLI Skeleton (b03)**
- Typer-based command-line interface
- Commands for run, gate, version operations
- Structured output with help text

**Evaluation Framework (b04)**
- Mock runner for deterministic test execution
- JSON and JUnit XML reporters
- Test suite execution with seed control

**Policy Oracles (b05)**
- Content policy validation
- Tool allowlist enforcement
- SLO threshold monitoring

**Release Gates (b06)**
- Automated pass/fail criteria
- Evidence pack generation
- Conformance report generation

**Adversarial Test Suites (b07)**
- Prompt injection batteries
- RAG poisoning and leakage tests
- UI injection (XSS, SSRF) test cases
- Property-based fuzzing with Hypothesis

**Tool Simulation (b08)**
- Safe tool execution sandbox
- ACL enforcement and redaction
- Schema validation for tool calls

**CI/CD Integration (b09)**
- GitHub Actions workflows for PR and nightly runs
- Branch protection and status checks
- Release automation

**Production Backend (b10)**
- Dockerized API service
- Observability and monitoring
- Production-ready deployment artifacts

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend UI                         │
│                      (Future Integration)                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Purple Ops API                        │
│  /benchmarks  /runs  /evidence  /conformance               │
└────┬──────────────────────┬──────────────────────┬─────────┘
     │                      │                      │
     ▼                      ▼                      ▼
┌──────────┐         ┌──────────┐          ┌──────────────┐
│  Safety  │         │ Security │          │  Compliance  │
│   Lane   │         │   Lane   │          │     Lane     │
├──────────┤         ├──────────┤          ├──────────────┤
│ Content  │         │ Prompt   │          │ NIST AI RMF  │
│ Policy   │         │ Injection│          │ EU AI Act    │
│ Harmful  │         │ Tool     │          │ FedRAMP      │
│ Outputs  │         │ Exploits │          │ ISO 42001    │
└────┬─────┘         └────┬─────┘          └──────┬───────┘
     │                    │                       │
     └────────────────────┴───────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │     Test Suite Execution       │
         │  • Normal (utility baseline)   │
         │  • Red Team (adversarial)      │
         │  • RAG (retrieval attacks)     │
         │  • UI (XSS, injection)         │
         │  • Regression (past incidents) │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │    Evidence & Reports          │
         │  • JSON summaries              │
         │  • JUnit XML                   │
         │  • Evidence manifests          │
         │  • Conformance reports         │
         └────────────────────────────────┘
```

See [docs/architecture/pipeline.md](docs/architecture/pipeline.md) for detailed lifecycle diagram.

## Documentation

| Document | Description |
|----------|-------------|
| [ROADMAP.md](docs/ROADMAP.md) | 10-phase development plan (b01-b10) |
| [BRANCHES.md](docs/BRANCHES.md) | Branch strategy and acceptance criteria |
| [COMPLIANCE_OVERVIEW.md](docs/COMPLIANCE_OVERVIEW.md) | Compliance lane architecture |
| [USAGE_POLICY.md](docs/USAGE_POLICY.md) | Authorized use guidelines for offensive tooling |
| [TOOLS_MANIFEST.md](docs/TOOLS_MANIFEST.md) | Security tool integration manifest |
| [GOVERNANCE.md](docs/GOVERNANCE.md) | Decision-making and ADR process |
| [pipeline.md](docs/architecture/pipeline.md) | End-to-end evaluation lifecycle |
| [REVIEWER_NOTES.md](docs/REVIEWER_NOTES.md) | Code review feedback and action items |

### Operational Runbooks

- [Incident Response: Prompt Injection](docs/runbooks/ir_prompt_injection.md)
- [Rollback Procedures](docs/runbooks/rollback.md)
- [Release Checklist](docs/runbooks/release_checklist.md)

## Integrated Security Tools

AI Purple Ops maintains a comprehensive registry of 35 security tools across 11 functional categories. All tools are wrapped with adapters providing safe defaults, rate limiting, and audit logging. See [registry/tools.yaml](registry/tools.yaml) and [registry/INTEGRATION_STATUS.md](registry/INTEGRATION_STATUS.md) for complete catalog and integration roadmap.

### LLM Security and Red Teaming (5 tools)
- **garak** - LLM vulnerability scanner with 100+ probes
- **PyRIT** - Microsoft's Python Risk Identification Toolkit for LLMs
- **promptfoo** - LLM testing framework with security assertions
- **llm-guard** - Comprehensive security toolkit for LLM interactions
- **rebuff** - Prompt injection detection framework

### Adversarial Machine Learning (4 tools)
- **ART (Adversarial Robustness Toolbox)** - IBM's adversarial robustness framework
- **CleverHans** - Adversarial examples library
- **Foolbox** - Python toolbox for adversarial attacks
- **TextAttack** - Framework for adversarial attacks on NLP models

### Code Security (5 tools)
- **Semgrep** - SAST with semantic code patterns
- **Bandit** - Python security linter
- **pip-audit** - Dependency vulnerability scanner
- **TruffleHog** - Secrets scanning in code and git history
- **detect-secrets** - Enterprise secrets detection

### Fuzzing and Property Testing (2 tools)
- **Hypothesis** - Property-based testing for Python
- **Atheris** - Google's coverage-guided Python fuzzer

### Traffic Interception and Monitoring (2 tools)
- **mitmproxy** - Interactive HTTPS proxy for security testing
- **OWASP ZAP** - Web application security testing

### Evaluation and Benchmarking (3 tools)
- **lm-evaluation-harness** - EleutherAI's LLM evaluation framework
- **HELM** - Stanford's Holistic Evaluation of Language Models
- **MLflow** - ML lifecycle management with evaluation tracking

### Safety and Content Moderation (4 tools)
- **Detoxify** - Toxic comment classification
- **NeMo Guardrails** - NVIDIA's programmable guardrails for LLMs
- **LangKit** - LLM monitoring and guardrails toolkit
- **Guardrails AI** - LLM validation framework

### RAG Security (3 tools)
- **LangChain** - Framework with security considerations for RAG
- **LlamaIndex** - RAG framework with security features
- **RAGChecker** - Amazon's RAG faithfulness and relevancy checker

### Compliance and Governance (3 tools)
- **AI Fairness 360** - IBM's AI fairness toolkit
- **Fairlearn** - Microsoft's fairness assessment toolkit
- **MLTE** - Machine Learning Test and Evaluation framework

### Privacy and PII Detection (2 tools)
- **Presidio** - Microsoft's PII detection and anonymization
- **Scrubadub** - PII removal from text

### Penetration Testing (2 tools)
- **NetExec** - Network exploitation framework
- **CrackMapExec** - Post-exploitation tool (deprecated, replaced by NetExec)

## Standards and Compliance Alignment

AI Purple Ops implements machine-readable control mappings and evidence generation for:

### NIST AI Risk Management Framework (AI RMF 1.0)
- **GOVERN**: Policy and oversight structures (docs/GOVERNANCE.md)
- **MAP**: Risk identification and categorization (mappings/nist_ai_rmf.yaml)
- **MEASURE**: Evaluation metrics including harmful output rate and tool policy violation rate
- **MANAGE**: Risk response procedures (runbooks, rollback procedures)

### EU AI Act (Regulation 2024/1689)
- Article 9: Risk management systems for high-risk AI
- Article 10: Data and data governance requirements
- Article 11: Technical documentation (Annex IV compliance checklist)
- Article 15: Accuracy, robustness, and cybersecurity requirements

### FedRAMP (Federal Risk and Authorization Management Program)
- Control mappings for Access Control (AC), Audit and Accountability (AU), and System and Information Integrity (SI) families
- OSCAL-compatible evidence generation
- Continuous monitoring artifacts and assessment reports

### Additional Frameworks
- **MITRE ATLAS**: Adversarial Threat Landscape for Artificial-Intelligence Systems
- **OWASP LLM Top 10**: Common security risks in LLM applications
- **ISO/IEC 42001**: AI management system standard (planned)

## Contributing

Contributions are welcome. Please review [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and the development workflow.

### Development Workflow

Each development phase follows a structured 6-step process:

1. Create feature branch `bNN-short-slug` from main
2. Complete threat model template and ADR if introducing new attack surface
3. Write pytest tests before implementation (test-first development)
4. Implement functionality with manual validation script
5. Run linting, formatting, update CHANGELOG and documentation
6. Submit for human review, address feedback

See [.cursor/rules/dev-loop.md](.cursor/rules/dev-loop.md) for complete workflow details.

### Code Quality Standards

- Python 3.11+ with comprehensive type hints
- Code formatting: black (100 char), ruff (15+ rule families)
- Security scanning: bandit (SAST), pip-audit (dependency vulnerabilities)
- Testing: pytest with deterministic fixtures, hypothesis for property-based testing
- Type checking: mypy with strict mode enabled
- Target: 80%+ test coverage on core harness modules

## License

MIT License. See [LICENSE](LICENSE) for full text.

The MIT License permits broad use but provides no warranty. Organizations deploying this software are responsible for ensuring compliance with applicable laws and regulations (GDPR, CCPA, SOC 2, etc.). See [ADR 0002](docs/adr/0002-licensing.md) for licensing rationale.

## Security

Report security vulnerabilities via GitHub Security Advisories. See [SECURITY.md](SECURITY.md) for disclosure policy and response timeline commitments.

## Project Status

**Current Phase:** b02-dev-tooling (Complete)
**Next Phase:** b03-cli-skeleton
**Target:** b10-backend-api-and-compose (Production-ready backend service)

| Phase | Status | Description |
|-------|--------|-------------|
| b01 | Complete | Governance, compliance mappings, evidence schemas |
| b02 | Complete | Development tooling, configuration system, tool registry |
| b03 | Planned | CLI skeleton with Typer framework |
| b04 | Planned | Mock runner, JSON/JUnit reporters, test execution |
| b05 | Planned | Policy oracles and validation rules |
| b06 | Planned | Release gates and evidence pack generation |
| b07 | Planned | Adversarial test suites (prompt injection, RAG, UI) |
| b08 | Planned | Tool simulation and RAG security features |
| b09 | Planned | CI/CD workflows and automation |
| b10 | Planned | Production backend API service |

## Citation

```bibtex
@software{aipurpleops2025,
  title = {AI Purple Ops: A Vendor-Neutral Testing Harness for AI Safety, Security, and Compliance},
  author = {Kenny's Laboratory},
  year = {2025},
  url = {https://github.com/Kennyslaboratory/AI-Purple-Ops},
  version = {0.2.0}
}
```

## Acknowledgments

Built on research and tooling from:
- Microsoft Security Research (PyRIT framework)
- OWASP AI Security and Privacy Working Group
- NIST AI Risk Management Framework team
- EU High-Level Expert Group on Artificial Intelligence
- MITRE ATLAS project contributors
- IBM Research (Adversarial Robustness Toolbox, AI Fairness 360)
- Stanford CRFM (HELM evaluation framework)

## Contact

- **Repository**: [https://github.com/Kennyslaboratory/AI-Purple-Ops](https://github.com/Kennyslaboratory/AI-Purple-Ops)
- **Issues**: [GitHub Issues](https://github.com/Kennyslaboratory/AI-Purple-Ops/issues)
- **Security**: See [SECURITY.md](SECURITY.md) for vulnerability reporting
