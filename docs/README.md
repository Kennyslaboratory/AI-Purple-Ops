# AI Purple Ops Documentation

Welcome to AI Purple Ops documentation. Find what you need fast.

---

## Quick Start

New to AI Purple Ops? Start here:

1. **[Main README](../README.md)** - Project overview and quick start
2. **[CLI Reference](CLI.md)** - Command-line usage
3. **[Adapters Guide](ADAPTERS.md)** - Connect to your AI model
4. **[Recipes Guide](RECIPES.md)** - Pre-configured workflows

---

## User Guides

### Core Functionality
- **[CLI Reference](CLI.md)** - Complete command-line interface reference
- **[Adapters Guide](ADAPTERS.md)** - Connect to any AI model (OpenAI, Anthropic, local models)
- **[Recipes Guide](RECIPES.md)** - Pre-configured security testing workflows
- **[Configuration Guide](CONFIGURATION.md)** - Advanced configuration options
- **[Environment Variables](ENVIRONMENT_VARIABLES.md)** - Configuration via environment

### Security Testing
- **[Red Team Guide](REDTEAM.md)** - Adversarial testing strategies
- **[Policies Guide](POLICIES.md)** - Content policies and enforcement
- **[Gates Guide](GATES.md)** - Quality gate configuration and thresholds
- **[Indirect Injection](INDIRECT_INJECTION.md)** - Indirect prompt injection attacks

### Compliance & Evidence
- **[Compliance Overview](COMPLIANCE_OVERVIEW.md)** - NIST, EU AI Act, FedRAMP
- **[Evidence Pack Specification](EVIDENCE_PACK_SPEC.md)** - Evidence artifact format
- **[Tool Manifest](TOOLS_MANIFEST.md)** - Integrated security tools

### Operations
- **[Model Management](MODEL_MANAGEMENT.md)** - Disk space and model caching
- **[Usage Policy](USAGE_POLICY.md)** - Authorized use guidelines

---

## Developer Documentation

### Architecture
- **[Architecture: Pipeline](architecture/pipeline.md)** - End-to-end evaluation lifecycle
- **[Architecture: UI Hooks](architecture/UI_HOOKS.md)** - Future UI integration points
- **[Architecture: Values](architecture/VALUES.md)** - Design principles

### Development Process
- **[Roadmap](ROADMAP.md)** - Development phases and status
- **[Branches Strategy](BRANCHES.md)** - Branch workflow and acceptance criteria
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute

### Architecture Decisions
- **[ADR Index](adr/README.md)** - Architecture Decision Records
- **[ADR 0001: Context and Scope](adr/0001-context-and-scope.md)**
- **[ADR 0002: Licensing](adr/0002-licensing.md)**

### Threat Models
- **[Threat Model Template](threatmodels/tm_template.md)** - Template for new features
- **[Threat Models Index](threatmodels/README.md)** - Existing threat models

---

## Operational Runbooks

Emergency procedures and operational guides:

- **[Incident Response: Prompt Injection](runbooks/ir_prompt_injection.md)** - Responding to prompt injection incidents
- **[Release Checklist](runbooks/release_checklist.md)** - Pre-release verification steps
- **[Rollback Procedures](runbooks/rollback.md)** - How to roll back a release

---

## Style Guides

- **[Console Output Style](style/console.md)** - Console output formatting standards

---

## Documentation by Use Case

### "I want to test my AI model for security issues"

1. **[Adapters Guide](ADAPTERS.md)** - Connect to your model
2. **[CLI Reference](CLI.md)** - Run security tests (`aipop run --suite redteam`)
3. **[Gates Guide](GATES.md)** - Set up quality gates
4. **[Red Team Guide](REDTEAM.md)** - Advanced adversarial testing

### "I need to generate compliance evidence"

1. **[Recipes Guide](RECIPES.md)** - Use compliance recipes
2. **[Compliance Overview](COMPLIANCE_OVERVIEW.md)** - Understand frameworks
3. **[Evidence Pack Specification](EVIDENCE_PACK_SPEC.md)** - Evidence format
4. **[Gates Guide](GATES.md)** - Generate evidence packs

### "I want to integrate with my CI/CD pipeline"

1. **[CLI Reference](CLI.md)** - Exit codes and automation
2. **[Gates Guide](GATES.md)** - Automated quality gates
3. **[Configuration Guide](CONFIGURATION.md)** - CI/CD configuration
4. **[Runbooks](runbooks/)** - Operational procedures

### "I want to build a custom adapter"

1. **[Adapters Guide](ADAPTERS.md)** - Adapter development guide
2. **[Architecture: Pipeline](architecture/pipeline.md)** - Understanding the architecture
3. **[Contributing Guide](../CONTRIBUTING.md)** - Development workflow

### "I want to understand the project structure"

1. **[Roadmap](ROADMAP.md)** - Development phases
2. **[Architecture: Values](architecture/VALUES.md)** - Design principles
3. **[Branches Strategy](BRANCHES.md)** - Development process
4. **[ADR Index](adr/README.md)** - Key decisions

---

## API Reference

### Core Protocols

```python
# Adapter Protocol
class Adapter(Protocol):
    def invoke(self, prompt: str, **kwargs) -> ModelResponse:
        ...

# Detector Protocol
class Detector(Protocol):
    def check(self, response: ModelResponse, test_case: TestCase) -> DetectorResult:
        ...

# Gate Protocol
class Gate(Protocol):
    def evaluate(self, metrics: dict[str, float]) -> GateResult:
        ...
```

See source code in `src/harness/core/` for complete protocol definitions.

---

## External Resources

### Standards & Frameworks
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act (Regulation 2024/1689)](https://artificialintelligenceact.eu/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)

### Integrated Tools
- [PyRIT](https://github.com/Azure/PyRIT) - Microsoft's Python Risk Identification Toolkit
- [Garak](https://github.com/leondz/garak) - LLM vulnerability scanner
- [Promptfoo](https://github.com/promptfoo/promptfoo) - LLM testing framework
- [PromptInject](https://github.com/agencyenterprise/PromptInject) - Prompt injection detection

---

## Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/Kennyslaboratory/AI-Purple-Ops/issues)
- **Security Issues**: See [SECURITY.md](../SECURITY.md) for responsible disclosure
- **Discussions**: [GitHub Discussions](https://github.com/Kennyslaboratory/AI-Purple-Ops/discussions)

---

## Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| Main README | ✅ Current | 2025-11-08 |
| CLI Reference | ✅ Current | 2025-11-08 |
| Adapters Guide | ✅ Current | 2025-11-08 |
| Roadmap | ✅ Current | 2025-11-08 |
| Recipes Guide | ⚠️ Review needed | 2025-11-06 |
| Configuration Guide | ✅ Current | 2025-11-06 |
| Gates Guide | ✅ Current | 2025-11-06 |
| Compliance Overview | ⚠️ Stub (needs expansion) | 2025-11-05 |

---

## Contributing to Docs

Found a typo or outdated information? We welcome documentation contributions!

1. Fork the repository
2. Edit the relevant markdown file
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

**Documentation Version**: v0.6.2
**Last Updated**: 2025-11-08
