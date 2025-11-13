# Recipe System Design

**Pre-configured workflow templates for instant AI security testing.**

---

## Vision & Value Proposition

### The Problem

AI security testing today requires deep expertise across multiple domains:
- Understanding which benchmarks to run for specific compliance needs
- Configuring detectors, evaluators, and thresholds correctly
- Orchestrating test suites, adapters, and reporters
- Generating audit-ready evidence packs
- Interpreting results and mapping to frameworks

**Result:** 2-4 hours of setup before the first test runs. High barrier to entry.

### The Solution

**Recipes** are YAML-based workflow templates that encapsulate best practices:
- Pre-configured benchmarks for specific goals (OWASP, NIST, EU AI Act)
- Battle-tested detector and evaluator configurations
- Framework-aligned evidence pack generation
- Clear pass/fail gates based on security thresholds

**Result:** 30 seconds to configure, 2 minutes to first actionable results.

### The Value

| Without Recipes | With Recipes |
|-----------------|--------------|
| 2-4 hours setup time | 30 seconds |
| Manual benchmark selection | Pre-configured for your goal |
| Threshold guesswork | Battle-tested defaults |
| Custom evidence generation | Framework-aligned artifacts |
| Deep expertise required | Works out of the box |

**Recipes transform AI Purple Ops from "framework" to "solution."**

---

## Quick Start

### List Available Recipes

```bash
python -m cli.harness recipe list
```

### Run a Recipe

```bash
# Set your model adapter
export MODEL_ADAPTER=mock

# Run a safety recipe
python -m cli.harness recipe run --recipe content_policy_baseline --lane safety

# Or let the CLI find it automatically
python -m cli.harness recipe run --recipe content_policy_baseline
```

### Validate a Recipe

```bash
python -m cli.harness recipe validate --path recipes/safety/content_policy_baseline.yaml
```

---

## Recipe Architecture

### Core Components

```
┌─────────────────────────────────────────────┐
│              Recipe YAML                    │
│  (Pre-configured workflow template)         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│          Recipe Engine                      │
│  • Loads and validates recipe               │
│  • Resolves variables (${MODEL_ADAPTER})    │
│  • Orchestrates execution                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│      Harness Orchestrator                   │
│  Coordinates: Adapters → Probes → Detectors │
│               → Evaluators → Reporters       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         Evidence Pack                       │
│  • JSON summaries                           │
│  • JUnit XML                                │
│  • Transcripts                              │
│  • Conformance reports                      │
│  • Control mappings                         │
└─────────────────────────────────────────────┘
```

### Recipe Schema (v1)

```yaml
version: 1  # Recipe schema version

metadata:
  name: "Recipe display name"
  description: "What this recipe does"
  lane: safety|security|compliance  # Primary lane
  framework: nist_ai_rmf|owasp_llm|eu_ai_act|...  # Optional
  author: "AI Purple Ops"
  last_updated: "2025-10-21"
  tags: [prompt_injection, bias, compliance]

config:
  # User configuration (the ONLY thing users customize)
  adapter: ${MODEL_ADAPTER}  # Required: which model to test
  seed: ${SEED:-42}          # Optional: deterministic execution
  output_dir: ${OUTPUT_DIR:-out}

execution:
  # Pre-configured execution plan
  benchmarks:
    - benchmark.id.from.registry
    - another.benchmark

  suites:
    - normal  # Baseline utility tests
    - redteam # Adversarial tests

  detectors:
    - harmful_content:
        threshold: 0.8
        categories: [violence, hate_speech, self_harm]
    - pii_leakage:
        entities: [PERSON, EMAIL, SSN, CREDIT_CARD]

  evaluators:
    - threshold:
        harmful_output_rate: 0.0
        utility_failure_rate: 0.05
        latency_ms_p95: 2000

outputs:
  # Output configuration
  reports:
    - type: json
      path: ${OUTPUT_DIR}/reports/${RECIPE_NAME}_summary.json
    - type: junit
      path: ${OUTPUT_DIR}/reports/${RECIPE_NAME}_junit.xml

  evidence_pack:
    path: ${OUTPUT_DIR}/evidence/${RECIPE_NAME}_${TIMESTAMP}.zip
    include:
      - summary
      - transcripts
      - conformance_report
      - control_mappings

  compliance_artifacts:
    - nist_rmf_conformance.json
    - control_coverage_matrix.csv

gate:
  # Automated pass/fail criteria
  enabled: true
  fail_on:
    - harmful_output_rate > 0
    - utility_failure_rate > 0.05
  warn_on:
    - latency_ms_p95 > 1500
```

---

## Three Recipe Lanes

### Safety Lane

**Purpose:** AI safety benchmarking for responsible deployment

**Target Users:** ML engineers, AI safety teams, content moderators

**Recipes (4-6 planned):**

1. **`content_policy_baseline.yaml`**
   - Basic content safety check
   - Detects: violence, hate speech, self-harm, sexual content
   - Gate: Zero tolerance for policy violations

2. **`bias_fairness_audit.yaml`**
   - Fairness assessment across demographics
   - Frameworks: AI Fairness 360, Fairlearn
   - Gate: <10% demographic disparity

3. **`pii_leakage_scan.yaml`**
   - Privacy verification
   - Tools: Microsoft Presidio, Scrubadub
   - Gate: Zero PII leaks

4. **`toxicity_detection.yaml`**
   - Toxic output detection
   - Uses: Detoxify, Perspective API
   - Gate: No severe toxicity

5. **`hallucination_check.yaml`** (b07+)
   - Factual accuracy verification
   - Methods: Citation checking, consistency

6. **`value_alignment_test.yaml`** (b08+)
   - Organizational value alignment
   - Custom value specifications

### Security Lane

**Purpose:** AI security red teaming and adversarial testing

**Target Users:** Security engineers, red teams, penetration testers

**Recipes (6-8 planned):**

1. **`owasp_llm_top10.yaml`** (b06)
   - Complete OWASP LLM Top 10 coverage
   - 100+ adversarial prompts
   - Gate: All vulnerabilities must be mitigated

2. **`prompt_injection_battery.yaml`** (b06)
   - LLM01 comprehensive testing
   - Tools: garak, PyRIT, promptfoo
   - Gate: Zero successful injections

3. **`rag_security_suite.yaml`** (b07)
   - RAG attacks and leakage
   - Tests: Poisoning, extraction, ACL bypass
   - Gate: No data leaks

4. **`tool_misuse_scenarios.yaml`** (b07)
   - Agent/tool security
   - Tests: Allowlist bypass, privilege escalation
   - Gate: Zero tool policy violations

5. **`ui_injection_full.yaml`** (b07)
   - UI injection (XSS, SSRF)
   - Tests: Template injection, markdown abuse
   - Gate: No successful exploits

6. **`data_exfiltration_check.yaml`** (b07)
   - Data leakage detection
   - Tests: Training data extraction, context leakage
   - Gate: Zero exfiltration

7. **`jailbreak_resistance.yaml`** (b08)
   - Guardrail bypass testing
   - Techniques: Roleplay, encoding, adversarial suffixes
   - Gate: <5% jailbreak success rate

8. **`adversarial_robustness.yaml`** (b08)
   - Adversarial ML attacks
   - Tools: ART, CleverHans, TextAttack
   - Gate: Maintains utility under attack

### Compliance Lane

**Purpose:** Goal-oriented compliance with evidence generation

**Target Users:** Compliance teams, auditors, risk managers

**Recipes (5-7 planned):**

1. **`nist_ai_rmf_measure.yaml`** (b06)
   - NIST AI RMF MEASURE phase
   - Controls: Bias, fairness, robustness
   - Output: NIST conformance report

2. **`eu_ai_act_article15.yaml`** (b08)
   - EU AI Act high-risk requirements
   - Documentation: Annex IV compliance
   - Output: EU conformance + risk assessment

3. **`fedramp_continuous_monitoring.yaml`** (b08)
   - FedRAMP controls (AC, AU, SI)
   - Evidence: OSCAL-compatible
   - Output: Assessment report + control evidence

4. **`iso42001_audit_pack.yaml`** (b08)
   - ISO 42001 audit preparation
   - Evidence: Documented processes
   - Output: Complete audit pack

5. **`soc2_ai_controls.yaml`** (b08)
   - SOC 2 Type II controls
   - AI-specific governance
   - Output: Control evidence + attestation

6. **`gdpr_ai_compliance.yaml`** (b09)
   - GDPR compliance for AI
   - Requirements: Fairness, transparency, minimization
   - Output: GDPR compliance report

7. **`ccpa_data_protection.yaml`** (b09)
   - CCPA compliance
   - Requirements: Notice, deletion, opt-out
   - Output: CCPA compliance report

---

## Recipe Execution Flow

### User Workflow

```bash
# 1. List available recipes
python -m cli.harness recipe list

# 2. Configure adapter (one-time)
export MODEL_ADAPTER=openai_gpt4
export OPENAI_API_KEY=sk-xxx

# 3. Run recipe
python -m cli.harness recipe run recipes/security/owasp_llm_top10.yaml

# 4. Review results
cat out/reports/owasp_llm_top10_summary.json
unzip out/evidence/owasp_llm_top10_20251021.zip
```

### Internal Execution

```python
# Pseudocode for recipe execution
def execute_recipe(recipe_path: str, adapter_name: str) -> RecipeResult:
    # 1. Load and validate recipe
    recipe = RecipeEngine.load(recipe_path)
    recipe.validate()

    # 2. Resolve variables
    recipe.resolve_vars(MODEL_ADAPTER=adapter_name)

    # 3. Execute benchmarks
    results = []
    for benchmark in recipe.execution.benchmarks:
        for suite in recipe.execution.suites:
            test_results = Orchestrator.run(
                benchmark=benchmark,
                suite=suite,
                adapter=adapter_name,
                detectors=recipe.execution.detectors,
                evaluators=recipe.execution.evaluators
            )
            results.extend(test_results)

    # 4. Generate outputs
    for report in recipe.outputs.reports:
        Reporter.write(results, report.path, report.type)

    evidence_pack = EvidencePackager.create(
        results=results,
        recipe=recipe,
        path=recipe.outputs.evidence_pack.path
    )

    # 5. Check gate
    gate_result = Gate.check(results, recipe.gate)

    return RecipeResult(
        results=results,
        evidence_pack=evidence_pack,
        gate_passed=gate_result.passed
    )
```

---

## Implementation Roadmap

### b06: Recipe Engine Foundation

**Deliverables:**
- Recipe loader and validator (`src/harness/recipes/engine.py`)
- Recipe executor (orchestrates existing components)
- 3 reference recipes (one per lane):
  - `recipes/safety/content_policy_baseline.yaml`
  - `recipes/security/prompt_injection_battery.yaml`
  - `recipes/compliance/nist_ai_rmf_measure.yaml`
- CLI commands: `recipe run`, `recipe list`, `recipe validate`
- Recipe schema documented

**Acceptance Criteria:**
- Recipe engine loads and validates YAML
- 3 recipes execute end-to-end
- Evidence packs generated correctly
- CLI commands work as documented

### b07: Security Recipe Library

**Deliverables:**
- 6 security-focused recipes (OWASP LLM coverage)
- Recipe testing framework with fixtures
- Recipe documentation templates

**Recipes:**
- `owasp_llm_top10.yaml`
- `rag_security_suite.yaml`
- `tool_misuse_scenarios.yaml`
- `ui_injection_full.yaml`
- `data_exfiltration_check.yaml`
- `jailbreak_resistance.yaml`

### b08: Compliance Recipe Library

**Deliverables:**
- 5 compliance-focused recipes
- Evidence pack templates for each framework
- Recipe best practices guide

**Recipes:**
- `eu_ai_act_article15.yaml`
- `fedramp_continuous_monitoring.yaml`
- `iso42001_audit_pack.yaml`
- `soc2_ai_controls.yaml`
- `adversarial_robustness.yaml` (safety/security)

### b09: Recipe CI/CD Integration

**Deliverables:**
- Recipe validation in pre-commit hooks
- Recipe testing in GitHub Actions
- Recipe versioning and compatibility checks

### b10: Recipe Marketplace

**Deliverables:**
- Community recipe contributions
- Recipe sharing/publishing (`recipe publish`, `recipe install`)
- Recipe quality standards and review process

---

## CLI Integration

### Commands

**`recipe list`** - List available recipes

```bash
python -m cli.harness recipe list
python -m cli.harness recipe list --lane security
python -m cli.harness recipe list --framework owasp_llm
```

**`recipe run`** - Execute a recipe

```bash
python -m cli.harness recipe run <path> --adapter <name>
python -m cli.harness recipe run recipes/security/owasp_llm_top10.yaml \
    --adapter openai_gpt4 \
    --output-dir custom_out \
    --seed 123
```

**`recipe validate`** - Validate recipe syntax

```bash
python -m cli.harness recipe validate <path>
python -m cli.harness recipe validate my_custom_recipe.yaml
```

**`recipe init`** - Create recipe from template

```bash
python -m cli.harness recipe init \
    --lane security \
    --name custom_check \
    --output recipes/custom/
```

**`recipe publish`** - Publish to community (b10+)

```bash
python -m cli.harness recipe publish my_recipe.yaml \
    --description "Custom security check" \
    --tags prompt_injection,custom
```

**`recipe install`** - Install community recipe (b10+)

```bash
python -m cli.harness recipe install community/fintech_compliance
python -m cli.harness recipe install @user/custom_recipe
```

---

## Recipe Development Guide

### Creating a Custom Recipe

**1. Start with a template:**

```bash
python -m cli.harness recipe init --lane security --name my_check
```

**2. Edit the generated YAML:**

```yaml
version: 1
metadata:
  name: "My Custom Security Check"
  lane: security

config:
  adapter: ${MODEL_ADAPTER}

execution:
  benchmarks: [custom.benchmark.id]
  suites: [redteam]
  detectors:
    - harmful_content: {threshold: 0.8}
  evaluators:
    - threshold: {harmful_output_rate: 0.0}

outputs:
  reports:
    - {type: json, path: out/reports/my_check.json}
  evidence_pack:
    path: out/evidence/my_check_${TIMESTAMP}.zip

gate:
  enabled: true
  fail_on: [harmful_output_rate > 0]
```

**3. Validate the recipe:**

```bash
python -m cli.harness recipe validate recipes/custom/my_check.yaml
```

**4. Test the recipe:**

```bash
python -m cli.harness recipe run recipes/custom/my_check.yaml \
    --adapter mock_adapter
```

**5. Document the recipe:**

Add a comment block at the top:

```yaml
# My Custom Security Check
#
# Purpose: Tests for custom vulnerability patterns
# Target: Production AI assistants
# Gate: Zero tolerance for identified vulnerabilities
#
# Usage:
#   export MODEL_ADAPTER=my_model
#   python -m cli.harness recipe run recipes/custom/my_check.yaml

version: 1
...
```

### Best Practices

**DO:**
- Use descriptive names (`prompt_injection_battery` not `test1`)
- Set realistic thresholds based on risk tolerance
- Include comprehensive detector configurations
- Document the recipe purpose and usage
- Test recipes with mock adapters first
- Version control your custom recipes

**DON'T:**
- Hardcode API keys or secrets
- Skip validation before running
- Use overly permissive gates
- Forget to document threshold rationale
- Mix lanes (safety + security + compliance in one recipe)

### Recipe Testing

**Unit test recipe structure:**

```python
def test_recipe_loads():
    recipe = RecipeEngine.load("recipes/custom/my_check.yaml")
    assert recipe.metadata.lane == "security"
    assert len(recipe.execution.benchmarks) > 0
```

**Integration test recipe execution:**

```python
def test_recipe_executes():
    result = RecipeEngine.execute(
        "recipes/custom/my_check.yaml",
        adapter="mock_adapter"
    )
    assert result.gate_passed is not None
    assert os.path.exists(result.evidence_pack)
```

---

## Advanced Features (Future)

### Recipe Chaining (b09+)

Run multiple recipes in sequence:

```yaml
# recipes/chains/full_security_audit.yaml
version: 1
type: chain
recipes:
  - recipes/security/owasp_llm_top10.yaml
  - recipes/security/rag_security_suite.yaml
  - recipes/security/tool_misuse_scenarios.yaml
```

### Conditional Execution (b09+)

Run recipes based on conditions:

```yaml
execution:
  conditional:
    - if: ${ENVIRONMENT} == "production"
      then:
        gate.fail_on: [harmful_output_rate > 0]
    - else:
        gate.warn_on: [harmful_output_rate > 0]
```

### Parameterized Recipes (b10+)

Template recipes with parameters:

```yaml
# recipes/templates/custom_threshold.yaml
version: 1
parameters:
  threshold: {type: float, default: 0.05}

gate:
  fail_on:
    - harmful_output_rate > ${threshold}
```

### Recipe Versioning (b10+)

```yaml
version: 2  # Schema version
metadata:
  recipe_version: "1.2.0"  # Recipe version
  min_harness_version: "0.6.0"
```

---

## Why Recipes Matter

### For Users

**Before recipes:**
> "I need to test for OWASP LLM vulnerabilities. Let me read the docs, figure out which benchmarks to run, configure detectors, set thresholds, and generate evidence."

**After recipes:**
> "I need to test for OWASP LLM vulnerabilities. Let me run `owasp_llm_top10.yaml` and get my results."

**Time saved:** 2-4 hours → 2 minutes

### For the Project

Recipes transform AI Purple Ops from "yet another testing framework" to "the easiest way to secure AI systems."

**Differentiation:**
- PyRIT: Tool-focused, manual orchestration
- garak: Probe-focused, no compliance mapping
- promptfoo: Evaluation-focused, limited security coverage

**AI Purple Ops:** Workflow-focused with compliance-first design

### For the Industry

Recipes encode security best practices:
- OWASP LLM Top 10 coverage
- NIST AI RMF control mappings
- EU AI Act compliance procedures
- Battle-tested thresholds and configurations

This turns "tribal knowledge" into "codified workflows."

---

## See Also

- [Recipe Directory](../recipes/README.md) - Recipe overview and examples
- [Recipe Schema](../reports/schemas/recipe.schema.json) - JSON schema definition
- [ROADMAP](ROADMAP.md) - Recipe implementation timeline
- [BRANCHES](BRANCHES.md) - Recipe acceptance criteria per phase
