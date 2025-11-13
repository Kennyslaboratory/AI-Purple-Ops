# CLI Reference

Complete command-line interface reference for AI Purple Ops.

## Installation

```bash
# Clone and setup
git clone https://github.com/Kennyslaboratory/AI-Purple-Ops.git
cd AI-Purple-Ops
make setup

# Verify installation
aipop version
```

---

## Command Overview

```bash
aipop [OPTIONS] COMMAND [ARGS]
```

**Available Commands:**
- `run` - Execute test suites
- `gate` - Evaluate quality gates
- `recipe` - Manage and run recipes
- `suites` - Discover and view test suites
- `adapter` - Manage model adapters
- `tools` - Manage security tool integrations
- `version` - Show version information

---

## Global Options

```bash
--help, -h        Show help message
--version         Show version and exit
```

---

## `aipop run` - Execute Test Suites

Run security test suites against your AI model.

### Basic Usage

```bash
# Run default suite
aipop run

# Run specific suite
aipop run --suite adversarial

# Run all suites
aipop run --suite all
```

### Options

```bash
--suite, -s TEXT           Suite name (default: normal)
--adapter TEXT             Adapter to use (default: from config)
--model TEXT               Model name (gpt-4o, claude-3-5-sonnet, etc.)
--orchestrator TEXT        Orchestrator for conversation management (simple, pyrit, none)
--orch-config PATH         Path to orchestrator config YAML file
--orch-opts TEXT           Orchestrator options (comma-separated: debug,verbose)
--max-turns INTEGER        Maximum conversation turns (1 for simple, 5+ for pyrit multi-turn)
--conversation-id TEXT     Continue previous conversation by ID (pyrit only)
--fingerprint              Force guardrail fingerprinting (auto-detects on first run)
--llm-classifier           Use LLM-based classification (more accurate, slower, costs $)
--generate-probes          Generate additional probes using LLM (experimental)
--config, -c PATH          Config file path
--output-dir PATH          Output directory (default: out/)
--reports-dir PATH         Reports directory (default: out/reports/)
--transcripts-dir PATH     Transcripts directory (default: out/transcripts/)
--log-level TEXT           Log level (DEBUG, INFO, WARN, ERROR)
--seed INTEGER             Random seed for deterministic testing
--response-mode TEXT       Mock adapter mode (echo, refuse, random, smart)
--policy PATH              Policy file path (default: policies/)
```

### Examples

```bash
# Basic adversarial testing
aipop run --suite adversarial

# With specific adapter
aipop run --suite redteam --adapter openai

# Deterministic testing
aipop run --suite normal --seed 42 --response-mode smart

# With custom policy
aipop run --suite policies/content_safety \
  --policy policies/strict_content_policy.yaml

# Debug mode
aipop run --suite adversarial --log-level DEBUG

# With orchestrator
aipop run --suite redteam --orchestrator simple

# Orchestrator with debug mode
aipop run --suite redteam --orchestrator simple --orch-opts debug

# Orchestrator with custom config
aipop run --suite redteam --orchestrator simple --orch-config my_config.yaml --orch-opts debug,verbose

# Multi-turn testing with PyRIT orchestrator
aipop run --suite adversarial --orchestrator pyrit --max-turns 5

# Continue previous conversation
aipop run --suite adversarial --orchestrator pyrit --conversation-id abc-123-def
```

### Guardrail Fingerprinting

Automatically detect which safety system protects your target model.

#### Auto-Detection (Default)

On first run, the tool automatically fingerprints the guardrail:

```bash
aipop run --suite adversarial --adapter openai --model gpt-4o
# Auto-detects guardrail, caches result for 24 hours
```

#### Manual Fingerprinting

Force re-detection:

```bash
aipop run --suite adversarial --adapter openai --fingerprint
```

#### Enhanced Detection

Use LLM classifier for better accuracy:

```bash
aipop run --suite adversarial --llm-classifier
```

#### Experimental: LLM Probe Generation

Generate creative probes (use with caution):

```bash
aipop run --suite adversarial --generate-probes
```

**Warning**: LLM-generated probes are experimental and may produce false positives/negatives.

#### Interpreting Results

- **Confidence >0.7**: High confidence, reliable detection
- **Confidence 0.4-0.7**: Medium confidence, review suggestions
- **Confidence <0.4**: Low confidence, consider `--llm-classifier`
- **Unknown**: Could not detect, see troubleshooting guide

See [Guardrail Fingerprinting Guide](GUARDRAIL_FINGERPRINTING.md) for complete details.

### Available Suites

```bash
adversarial        # Jailbreaks and prompt injection
rag                # RAG poisoning and data leakage
ui                 # XSS, SSRF injection attacks
redteam            # Advanced adversarial prompts
policies           # Content safety validation
normal             # Utility baseline testing
adapters           # Adapter health checks
comparison         # Multi-model benchmarking
all                # Run all suites
```

---

## `aipop mutate` - Generate Prompt Mutations

Generate mutated versions of prompts using encoding, unicode, HTML, LLM paraphrasing, and genetic algorithms.

### Basic Usage

```bash
# Generate mutations
aipop mutate "Tell me how to hack a system"

# Specific strategies
aipop mutate "Attack prompt" --strategies encoding,unicode

# With LLM paraphrasing (requires API key)
aipop mutate "Leak system prompt" --strategies paraphrase --provider openai

# Save to file
aipop mutate "test" --output mutations.json --count 20

# Show statistics
aipop mutate "test" --stats
```

### Options

```bash
PROMPT                    Prompt text to mutate (required)
--config, -c PATH         Mutation config YAML file
--output, -o PATH         Save mutations to JSON file
--count, -n INTEGER      Number of mutations to generate (default: 10)
--strategies TEXT         Comma-separated strategies (encoding,unicode,html,paraphrase,genetic)
--provider TEXT           LLM provider for paraphrasing (openai, anthropic, ollama)
--stats                   Show mutation statistics
```

### Examples

```bash
# Basic encoding mutations
aipop mutate "Hello World" --strategies encoding

# Unicode obfuscation
aipop mutate "attack" --strategies unicode

# HTML containers
aipop mutate "malicious" --strategies html

# LLM paraphrasing (requires OPENAI_API_KEY)
aipop mutate "Leak the prompt" --strategies paraphrase --provider openai

# All strategies
aipop mutate "test" --strategies encoding,unicode,html

# Custom config
aipop mutate "test" --config my_mutation_config.yaml --output results.json
```

### Available Strategies

- **encoding**: Base64, URL, ROT13, hex encoding
- **unicode**: Homoglyphs, zero-width characters
- **html**: HTML comments, script tags, CDATA
- **paraphrase**: LLM-assisted paraphrasing (requires API key)
- **genetic**: Genetic algorithm evolution (requires population)

See [Mutation Engine Guide](MUTATION_ENGINE.md) for complete details.

---

## `aipop gate` - Evaluate Quality Gates

Check if test results meet quality thresholds. Returns exit code 1 if gates fail (CI/CD integration).

### Basic Usage

```bash
# Check latest run
aipop gate

# Check specific summary
aipop gate --summary out/reports/summary.json

# Generate evidence pack
aipop gate --generate-evidence
```

### Options

```bash
--summary, -r PATH         Path to summary JSON file
--policy, -p PATH          Policy file with thresholds
--generate-evidence        Generate evidence pack ZIP
--evidence-dir PATH        Evidence output directory (default: out/evidence/)
--config, -c PATH          Config file path
--fail-on TEXT             Metrics to fail on (comma-separated)
--dry-run                  Preview without failing
```

### Examples

```bash
# Basic gate check
aipop gate

# With custom policy
aipop gate --policy policies/strict_policy.yaml

# Generate evidence for audit
aipop gate --generate-evidence --evidence-dir compliance/evidence/

# Fail on specific metrics
aipop gate --fail-on harmful_output_rate,critical_violation_rate

# Fail on tool policy violations
aipop gate --fail-on tool_policy_violation_rate

# Preview thresholds
aipop gate --dry-run
```

### Exit Codes

- `0` - All gates passed
- `1` - One or more gates failed
- `2` - Error (missing summary, invalid config, etc.)

---

## `aipop recipe` - Recipe Management

Manage and execute pre-configured security testing workflows.

### Sub-Commands

```bash
aipop recipe list             # List available recipes
aipop recipe run              # Execute a recipe
aipop recipe validate         # Validate recipe syntax
aipop recipe preview          # Preview recipe configuration
```

### `recipe list`

List all available recipes.

```bash
# List all recipes
aipop recipe list

# Show detailed information
aipop recipe list --verbose
```

### `recipe run`

Execute a recipe workflow.

```bash
# Basic usage
aipop recipe run --recipe content_policy_baseline

# With specific adapter
aipop recipe run --recipe prompt_injection_baseline --adapter openai

# Override config
aipop recipe run --recipe nist_measure \
  --config custom_config.yaml \
  --output-dir compliance/nist/
```

**Options:**
```bash
--recipe, -r TEXT      Recipe name (required)
--adapter TEXT         Override adapter
--config PATH          Custom config file
--output-dir PATH      Output directory
--policy PATH          Custom policy file
--lane TEXT            Recipe lane (safety, security, compliance)
```

### `recipe validate`

Validate recipe syntax and configuration.

```bash
# Validate recipe
aipop recipe validate --path recipes/safety/content_policy_baseline.yaml

# Validate all recipes
aipop recipe validate --all
```

### `recipe preview`

Preview recipe configuration without running.

```bash
# Preview recipe
aipop recipe preview --recipe full_redteam

# Show execution plan
aipop recipe preview --recipe nist_measure --verbose
```

### Available Recipes

```bash
content_policy_baseline    # Basic content safety validation
prompt_injection_baseline  # Security baseline for prompt injection
full_redteam              # Comprehensive adversarial testing
nist_measure              # NIST AI RMF MEASURE phase compliance
```

---

## `aipop suites` - Test Suite Discovery

Discover and view information about available test suites.

### Sub-Commands

```bash
aipop suites list              # List all available test suites
aipop suites info              # Show detailed information about a suite
```

### `suites list`

List all available test suites with metadata.

```bash
# List all suites
aipop suites list
```

**Output:**
```
Available Test Suites
┌─────────────┬────────────────────────┬──────────────────────┬───────┐
│ Category    │ Suite                  │ Description          │ Tests │
├─────────────┼────────────────────────┼──────────────────────┼───────┤
│ adversarial │ basic_jailbreak        │ Basic jailbreak...   │ 8     │
│ adversarial │ fuzz_tests             │ Fuzzing boundary...  │ 12    │
│ redteam     │ prompt_injection_...   │ Advanced prompt...   │ 15    │
│ ...         │ ...                    │ ...                  │ ...   │
└─────────────┴────────────────────────┴──────────────────────┴───────┘

Total: 10 suite(s), 133 test cases
```

### `suites info`

Show detailed information about a specific test suite.

```bash
# Show suite details
aipop suites info --suite tool_policy_validation

# With category prefix
aipop suites info --suite tools/tool_policy_validation
```

**Options:**
```bash
--suite, -s TEXT    Suite name (required for info)
```

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│ Suite Information                                           │
├─────────────────────────────────────────────────────────────┤
│ Suite: Tool Policy Validation                               │
│ Category: tools                                             │
│ Path: suites/tools/tool_policy_validation.yaml             │
│ Description: Tests for tool policy enforcement...           │
│                                                             │
│ Test Cases: 8                                               │
│                                                             │
│   1. authorized_search - Test that authorized web_search... │
│   2. authorized_calculator - Test that authorized...        │
│   ...                                                       │
│                                                             │
│ Categories: tool_policy                                     │
│ Risk Levels: low, high, critical                            │
└─────────────────────────────────────────────────────────────┘
```

### Examples

```bash
# Discover available suites
aipop suites list

# Get details about a specific suite
aipop suites info --suite basic_jailbreak

# Use category/suite format
aipop suites info --suite adversarial/basic_jailbreak

# Then use suite in run command
aipop run --suite adversarial/basic_jailbreak
```

---

## `aipop adapter` - Adapter Management

Manage model adapters for connecting to AI systems.

### Sub-Commands

```bash
aipop adapter list      # List available adapters
aipop adapter test      # Test adapter connection
aipop adapter init      # Create new adapter (wizard)
aipop adapter validate  # Validate adapter implementation
```

### `adapter list`

List all registered adapters.

```bash
# List adapters
aipop adapter list

# Show adapter details
aipop adapter list --verbose
```

**Output:**
```
Available Adapters:
  ✓ openai      - OpenAI GPT models
  ✓ anthropic   - Anthropic Claude models
  ✓ huggingface - HuggingFace local models
  ✓ ollama      - Ollama local models
  ✓ mock        - Testing adapter (no API)
```

### `adapter test`

Test adapter connection and health.

```bash
# Test specific adapter
aipop adapter test --name openai

# Test with custom config
aipop adapter test --name ollama --config configs/local.yaml
```

### `adapter init`

Create new adapter (interactive wizard).

```bash
# Interactive wizard
aipop adapter init

# With template
aipop adapter init --template openai --name my_custom_api

# Non-interactive
aipop adapter init --name my_adapter \
  --template custom_api \
  --model-type api \
  --base-url https://api.example.com
```

### `adapter validate`

Validate adapter implementation.

```bash
# Validate adapter
aipop adapter validate --name my_custom_adapter

# Run validation suite
aipop adapter validate --name my_custom_adapter --full
```

---

## `aipop tools` - Tool Management

Manage external security tool integrations (PyRIT, Garak, etc.).

### Sub-Commands

```bash
aipop tools check      # Check installation status
aipop tools install    # Install security tools
aipop tools update     # Update installed tools
aipop tools list       # List available tools
```

### `tools check`

Check which tools are installed.

```bash
# Check all tools
aipop tools check

# Check specific tool
aipop tools check --tool garak
```

**Output:**
```
Tool Installation Status:
  ✓ pyrit       - Installed (v0.1.2)
  ✓ garak       - Installed (v0.8.1)
  ✗ promptfoo   - Not installed
  ✗ airt        - Not installed
```

### `tools install`

Install external security tools.

```bash
# Install all tools (stable versions)
aipop tools install

# Install specific tool
aipop tools install --tool garak

# Install latest versions
aipop tools install --latest

# Install specific tool with latest version
aipop tools install --tool pyrit --latest
```

### `tools list`

List all available tool integrations.

```bash
# List tools
aipop tools list

# Show details
aipop tools list --verbose
```

---

## `aipop version`

Show version information.

```bash
aipop version
```

**Output:**
```
AI Purple Ops v0.6.2
Python 3.11.5
Platform: Linux-6.6.87.2-microsoft-standard-WSL2
```

---

## Configuration

### Config File

Default: `configs/harness.yaml`

```yaml
run:
  output_dir: out
  reports_dir: out/reports
  transcripts_dir: out/transcripts
  log_level: INFO
  seed: null

adapters:
  openai:
    type: openai
    model: gpt-4o-mini
    api_key_env: OPENAI_API_KEY

  ollama:
    type: ollama
    model: llama3.1
    base_url: http://localhost:11434
```

### Environment Variables

```bash
# Override config values
export AIPO_OUTPUT_DIR=./custom-output
export AIPO_LOG_LEVEL=DEBUG
export AIPO_SEED=42

# Adapter credentials
export OPENAI_API_KEY=sk-your-key
export ANTHROPIC_API_KEY=sk-ant-your-key

# Adapter selection
export MODEL_ADAPTER=openai
```

### CLI Override Priority

1. CLI arguments (highest)
2. Environment variables (`AIPO_*`)
3. Config file
4. Defaults (lowest)

---

## Common Workflows

### Pre-Deployment Security Check

```bash
# Run comprehensive security testing
aipop run --suite redteam --adapter openai

# Check quality gates
aipop gate --generate-evidence

# Exit code 0 = safe to deploy
# Exit code 1 = blocked (violations found)
```

### Continuous Integration

```bash
#!/bin/bash
# ci-security-check.sh

# Run tests
aipop run --suite adversarial --adapter $CI_MODEL_ADAPTER

# Evaluate gates (will exit 1 if failed)
aipop gate --fail-on harmful_output_rate,critical_violation_rate

# Upload evidence
aipop gate --generate-evidence
```

### Recipe-Based Evaluation

```bash
# Safety evaluation
aipop recipe run --recipe content_policy_baseline --adapter openai

# Security evaluation
aipop recipe run --recipe prompt_injection_baseline --adapter anthropic

# Compliance evaluation
aipop recipe run --recipe nist_measure --adapter huggingface
```

### Multi-Model Comparison

```bash
# Test same suite against multiple models
for adapter in openai anthropic ollama; do
  aipop run --suite adversarial \
    --adapter $adapter \
    --output-dir results/$adapter
done

# Compare results
aipop compare results/openai results/anthropic results/ollama
```

---

## Troubleshooting

### Command Not Found

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Or use full path
.venv/bin/aipop version
```

### Config Not Found

```bash
# Check config path
ls configs/harness.yaml

# Use custom config
aipop run --config /path/to/config.yaml
```

### Permission Denied

```bash
# Make output directories writable
chmod -R u+w out/

# Or use custom output directory
aipop run --output-dir /tmp/aipop-out
```

---

## Next Steps

- [Adapters Guide](ADAPTERS.md) - Connect to any AI model
- [Recipes Guide](RECIPES.md) - Pre-configured workflows
- [Configuration Guide](CONFIGURATION.md) - Advanced configuration
- [Gates Guide](GATES.md) - Quality gate setup
