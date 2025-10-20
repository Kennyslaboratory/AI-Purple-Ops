# AI Purple Ops

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](docs/ROADMAP.md)

**A vendor-neutral testing harness for AI Safety, Security, and Compliance evaluation.**

AI Purple Ops provides a unified backend infrastructure for evaluating AI systems across three critical dimensions: safety (content & policy), security (tools & data), and compliance (regulatory frameworks). Built to power testing workflows from development through production release gates.

---

## 🎯 Overview

AI Purple Ops addresses the gap between AI capability development and deployment readiness. As AI systems gain agency—making decisions, invoking tools, and accessing sensitive data—traditional security testing approaches fall short. This framework provides:

- **Compliance-First Architecture**: Machine-readable mappings to NIST AI RMF, EU AI Act, and FedRAMP controls
- **Evidence Automation**: Structured JSON schemas for audit trails, conformance reports, and evidence packs
- **Vendor Neutrality**: Adapter-based design for models, platforms, and tooling integration
- **UI-Ready API**: RESTful endpoints for orchestrating tests, retrieving results, and managing benchmarks
- **Reproducibility**: Deterministic test execution with seed control and fixture management

### Why AI Purple Ops?

Modern AI systems require **purple team thinking**—combining offensive security (red team) and defensive validation (blue team) with safety evaluation and compliance documentation. AI Purple Ops unifies these workflows:

| **Safety Lane** | **Security Lane** | **Compliance Lane** |
|-----------------|-------------------|---------------------|
| Content policy violations | Prompt injection attacks | NIST AI RMF measures |
| Harmful output detection | Tool misuse & privilege escalation | EU AI Act Article 15 |
| Bias & fairness metrics | Data exfiltration & RAG leakage | FedRAMP control mappings |
| PII leakage prevention | SSRF, RCE, XSS in agents | Evidence pack generation |

---

## 🚀 Quick Start

> **Note:** Currently in `b01-initial-commit` phase. Runtime implementation begins in `b02-dev-tooling`.

```bash
# Clone the repository
git clone https://github.com/your-org/ai-purple-ops.git
cd ai-purple-ops

# Future: Setup environment (b02+)
# make setup

# Future: Run baseline evaluation (b04+)
# make baseline

# Future: Run adversarial battery (b07+)
# make battery

# Future: Check release gates (b06+)
# make gate
```

---

## 📋 Features

### Current (b01-initial-commit)

- ✅ **Governance Foundation**: Security policies, usage guidelines, contributor agreements
- ✅ **Compliance Mappings**: YAML-based control mappings for NIST AI RMF, EU AI Act, FedRAMP
- ✅ **Evidence Schemas**: JSON schemas for run summaries, evidence manifests, conformance reports
- ✅ **Development Guardrails**: 9 Cursor rules enforcing dev loop, security invariants, tool hygiene
- ✅ **API Surface**: OpenAPI 3.0 spec with endpoints for benchmarks, runs, and evidence retrieval
- ✅ **Tool Registry**: Living catalog with deprecation tracking for security tooling

### Planned (b02-b10)

- 🔄 **Evaluation Framework** (b04): Mock runner, JSON/JUnit reporters, test suite execution
- 🔄 **Policy Oracles** (b05): Content validation, tool allowlists, SLO thresholds
- 🔄 **Release Gates** (b06): Automated pass/fail criteria, evidence pack generation
- 🔄 **Adversarial Suites** (b07): Prompt injection, RAG attacks, UI XSS, property-based fuzzing
- 🔄 **Tool Simulation** (b08): Safe tool execution with ACLs, redaction, schema validation
- 🔄 **CI/CD Integration** (b09): GitHub Actions workflows for PR, nightly, and release gates
- 🔄 **Backend Service** (b10): Dockerized API, observability, production-ready deployment

---

## 🏗️ Architecture

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
┌──────────┐         ┌──────────┐         ┌──────────────┐
│  Safety  │         │ Security │         │  Compliance  │
│   Lane   │         │   Lane   │         │     Lane     │
├──────────┤         ├──────────┤         ├──────────────┤
│ Content  │         │ Prompt   │         │ NIST AI RMF  │
│ Policy   │         │ Injection│         │ EU AI Act    │
│ Harmful  │         │ Tool     │         │ FedRAMP      │
│ Outputs  │         │ Exploits │         │ ISO 42001    │
└────┬─────┘         └────┬─────┘         └──────┬───────┘
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

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [ROADMAP.md](docs/ROADMAP.md) | 10-phase development plan (b01-b10) |
| [BRANCHES.md](docs/BRANCHES.md) | Branch strategy and acceptance criteria |
| [COMPLIANCE_OVERVIEW.md](docs/COMPLIANCE_OVERVIEW.md) | Compliance lane architecture |
| [USAGE_POLICY.md](docs/USAGE_POLICY.md) | Authorized use guidelines for offensive tooling |
| [TOOLS_MANIFEST.md](docs/TOOLS_MANIFEST.md) | Integrated security tools (PyRIT, garak, Semgrep) |
| [GOVERNANCE.md](docs/GOVERNANCE.md) | Decision-making and ADR process |
| [pipeline.md](docs/architecture/pipeline.md) | End-to-end evaluation lifecycle |

### Runbooks

- [Incident Response: Prompt Injection](docs/runbooks/ir_prompt_injection.md)
- [Rollback Procedures](docs/runbooks/rollback.md)
- [Release Checklist](docs/runbooks/release_checklist.md)

---

## 🛠️ Integrated Tools

AI Purple Ops wraps best-in-class security tooling with adapters and safe defaults:

**Evaluation & Testing**
- [PyRIT](https://github.com/Azure/PyRIT) - Microsoft's red team framework for LLMs
- [garak](https://github.com/leondz/garak) - LLM vulnerability scanner
- [promptfoo](https://github.com/promptfoo/promptfoo) - LLM testing and evaluation

**Security Analysis**
- [Semgrep](https://semgrep.dev) - SAST for orchestrator code
- [Bandit](https://github.com/PyCQA/bandit) - Python security linting
- [mitmproxy](https://mitmproxy.org) - HTTP traffic interception

**Fuzzing & Property Testing**
- [Hypothesis](https://hypothesis.readthedocs.io) - Property-based testing

**Standards & Frameworks**
- MITRE ATLAS - Adversarial threat landscape for AI
- OWASP LLM Top 10 - Common LLM vulnerabilities
- NIST AI RMF - AI Risk Management Framework

See [registry/tools.yaml](registry/tools.yaml) for complete catalog with status tracking.

---

## 🔬 Research & Standards Alignment

AI Purple Ops implements controls and mappings for:

### NIST AI Risk Management Framework (AI RMF)
- **GOVERN**: Policy and oversight (docs/GOVERNANCE.md)
- **MAP**: Risk identification (mappings/nist_ai_rmf.yaml)
- **MEASURE**: Evaluation metrics (harmful output rate, tool violations)
- **MANAGE**: Risk response (runbooks, rollback procedures)

### EU AI Act (High-Risk AI Systems)
- Article 9: Risk management systems
- Article 10: Data governance
- Article 11: Technical documentation (Annex IV checklist)
- Article 15: Accuracy, robustness, and cybersecurity

### FedRAMP
- Control mappings for AC, AU, SI families
- OSCAL-compatible evidence generation
- Continuous monitoring artifacts

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Loop

Every phase follows a 6-step process:

1. **New Branch**: Create `bNN-short-slug` from main
2. **Threat Model**: Complete threat model template + ADR
3. **Tests First**: Write pytest tests before implementation
4. **Manual Exercise**: Create runnable script, document findings
5. **Housekeeping**: Lint, format, update CHANGELOG and docs
6. **Human Review**: Request review, address feedback

See [.cursor/rules/dev-loop.md](.cursor/rules/dev-loop.md) for details.

### Code Quality

- Python 3.11+ with type hints
- Formatting: `black`, `ruff`
- Security: `bandit`, `pip-audit`
- Testing: `pytest` with deterministic fixtures
- Coverage: Aim for 80%+ on core harness code

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

The MIT License permits broad use but provides no warranty. Organizations are responsible for ensuring compliance with applicable laws and regulations (GDPR, CCPA, SOC 2, etc.). See [ADR 0002](docs/adr/0002-licensing.md) for licensing rationale.

---

## 🔒 Security

**Reporting Vulnerabilities**: See [SECURITY.md](SECURITY.md) for our disclosure policy.

**SLA**: 24-hour triage, 72-hour initial communication, severity-based remediation timelines.

**Contact**: See [SECURITY_CONTACTS.md](SECURITY_CONTACTS.md) for escalation paths.

---

## 📊 Project Status

**Current Phase**: b01-initial-commit (Governance & Compliance Infrastructure)  
**Next Phase**: b02-dev-tooling (pyproject.toml, Makefile, CLI skeleton)  
**Target**: b10-backend-api-and-compose (Production-ready backend service)

| Phase | Status | Description |
|-------|--------|-------------|
| b01 | ✅ Complete | Initial scaffold, governance, compliance mappings |
| b02 | 🔄 Next | Dev tooling (pyproject, pre-commit, Makefile) |
| b03 | 📋 Planned | CLI skeleton with Typer |
| b04 | 📋 Planned | Mock runner, reporters, test execution |
| b05 | 📋 Planned | Policy oracles and validation |
| b06 | 📋 Planned | Release gates and evidence generation |
| b07 | 📋 Planned | Adversarial test suites |
| b08 | 📋 Planned | Tool simulation and RAG security |
| b09 | 📋 Planned | CI/CD workflows |
| b10 | 📋 Planned | Production backend service |

---

## 🎓 Citation

If you use AI Purple Ops in your research or production systems, please cite:

```bibtex
@software{aipurpleops2025,
  title = {AI Purple Ops: A Vendor-Neutral Testing Harness for AI Safety, Security, and Compliance},
  author = {Your Organization},
  year = {2025},
  url = {https://github.com/your-org/ai-purple-ops},
  version = {0.1.0}
}
```

---

## 🙏 Acknowledgments

Built on the shoulders of giants in AI safety and security research:
- Microsoft Security Research (PyRIT)
- OWASP AI Security & Privacy Working Group
- NIST AI Risk Management Framework team
- EU High-Level Expert Group on AI
- MITRE ATLAS contributors

---

## 📞 Contact & Community

- **Issues**: [GitHub Issues](https://github.com/your-org/ai-purple-ops/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-purple-ops/discussions)
- **Security**: See [SECURITY_CONTACTS.md](SECURITY_CONTACTS.md)

---

<p align="center">
  <i>Building the bridge between AI innovation and deployment confidence.</i>
</p>
