# Tool Integration Status

## Current State (b02)

### ✅ Registry Complete
- **22 AI-security-focused tools** cataloged in `tools.yaml`
- **7 categories** covering AI safety, security, and compliance testing
- All tools have repos, descriptions, and status tracking
- Infrastructure/dev tools removed (not for end-user AI testing)

### 🔧 Adapters TODO
The `adapters/` directory is currently **placeholder-only**. Adapter implementation happens in phases **b04-b08**:

| Phase | Branch | What Gets Adapted |
|-------|--------|-------------------|
| b04 | runner-mock | Mock model adapter (baseline) |
| b05 | oracles-policies | Content filters, guardrails |
| b07 | redteam-rag-ui-fuzz | garak, PyRIT, promptfoo (LLM security) |
| b08 | retrievers-simtools | RAG security, tool simulation |

## Integration Roadmap

### Phase 1: Core Evaluation (b04-b05)
**Priority adapters:**
- Mock model (for deterministic testing)
- Basic content filters
- Tool schema validators

### Phase 2: Security Testing (b07)
**LLM Security adapters:**
- `garak` - LLM vulnerability scanner
- `pyrit` - Microsoft red team framework
- `promptfoo` - Security assertions
- `llm-guard` - Interaction security
- `rebuff` - Prompt injection detection

**Adversarial ML adapters:**
- `art` - IBM adversarial robustness
- `textattack` - NLP adversarial attacks

**Property Testing:**
- `hypothesis` - Property-based testing for AI model behavior

### Phase 3: RAG & Tool Security (b08)
**RAG Security adapters:**
- `ragchecker` - Amazon's RAG faithfulness checker

**Privacy:**
- `presidio` - PII detection/anonymization
- `scrubadub` - Text sanitization

**Safety:**
- `nemo-guardrails` - NVIDIA guardrails
- `detoxify` - Toxicity detection
- `langkit` - LLM monitoring

### Phase 4: Evaluation & Benchmarking (b09)
**Evaluation & Benchmarking:**
- `lm-evaluation-harness` - EleutherAI evals
- `helm` - Stanford holistic evaluation

### Phase 5: Production Backend (b10)

**Compliance:**
- `ai-fairness-360` - Bias detection
- `fairlearn` - Fairness assessment
- `mlte` - ML test & evaluation

## Adapter Architecture

Each tool adapter will implement:

```python
class ToolAdapter(Protocol):
    """Common interface for security tool adapters."""

    def configure(self, config: dict[str, Any]) -> None:
        """Load adapter-specific configuration."""

    def run(self, test_case: TestCase) -> Result:
        """Execute test case through the tool."""

    def parse_results(self, raw: Any) -> list[Finding]:
        """Normalize tool output to common schema."""
```

### Safe Defaults
All adapters will include:
- Rate limiting and cost controls
- Input sanitization
- Output redaction for PII/secrets
- Dry-run mode (no destructive actions)
- Detailed logging and audit trails

### Configuration Pattern
```yaml
# configs/harness.yaml
adapters:
  garak:
    enabled: true
    model: "openai:gpt-4o-mini"
    max_parallel: 5
    timeout_sec: 30

  presidio:
    enabled: true
    entities: ["PERSON", "EMAIL", "CREDIT_CARD"]
    confidence_threshold: 0.8
```

## What's Ready Now?

### ✅ Ready for Integration
1. **Registry catalog** - 22 AI-security-focused tools documented
2. **Configuration system** - `AdaptersConfig` in `src/harness/utils/config.py`
3. **Benchmark mappings** - `registry/benchmarks.yaml` references adapters
4. **Directory structure** - `adapters/` hierarchy exists
5. **Core protocols** - Adapter, Runner, Reporter, Gate interfaces defined

### 🚧 Still Needed
1. **Adapter implementations** - Python classes for each tool (b04-b08)
2. **Dependency management** - Add tool packages to `pyproject.toml`
3. **Integration tests** - Verify adapters work end-to-end
4. **Documentation** - Usage guides for each adapter

## Summary

The **registry is complete and ready** - it's a focused catalog of 22 AI-security-focused tools across 7 categories. Infrastructure and dev tools have been removed to keep the focus on end-user AI system testing.

Adapters will be built **incrementally across phases b04-b08**, starting with core functionality (mock models, content filters) and progressively adding security testing tools (garak, PyRIT), RAG security (RAGChecker), and compliance tools (fairness, evaluation frameworks).

The adapter pattern is already established in `config.py`, so integrating new tools follows a consistent template. Each phase is demo-ready, ensuring the system stays working as complexity grows.

**Bottom line:** Registry is the "shopping list" ✓, adapters are the "implementation" (coming in b04-b08).
