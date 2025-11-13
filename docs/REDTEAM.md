# Redteam Orchestration

AI Purple Ops provides a universal orchestrator for running multiple redteam tools with a single recipe configuration.

## Installation

### Automated Installation (Recommended)

The easiest way to install all redteam tools is using the Makefile target:

```bash
make toolkit
```

This will:
1. Install all tools from `configs/toolkit.yaml` using stable versions
2. Verify installation with health checks
3. Run comprehensive tests

### Manual Installation via CLI

You can also use the CLI command directly:

```bash
# Install all tools (stable versions)
aipop tools install --stable

# Install specific tool
aipop tools install --tool promptfoo --stable

# Check installation status
aipop tools check

# Update to latest versions (not recommended)
aipop tools update
```

### Version Selection

The toolkit system supports two version strategies:

- **Stable (Recommended)**: Tested, pinned versions with SHA256 verification
- **Latest**: Bleeding-edge versions (may break, no checksum verification)

The default is stable. To use latest versions:

```bash
aipop tools install --latest
```

### Configuration File

Tool versions, URLs, and SHA256 checksums are managed in `configs/toolkit.yaml` (similar to Puppetfile pattern). This ensures:

- Reproducible installations
- Security through checksum verification
- Easy version updates

### SHA256 Verification

Stable versions include SHA256 checksums for security. If a download doesn't match the expected checksum, installation will fail with a clear error message.

## Quick Start

### 1. Initialize a Redteam Project

```bash
aipop init redteam my-project
cd my-project
```

This creates:
- `recipes/security/full_redteam.yaml` - Reference recipe
- `.env.example` - API key template
- `.github/workflows/aipop-redteam.yml` - CI/CD workflow
- `README.md` - Quick start guide

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run Redteam Tests

```bash
# With real API (requires keys)
aipop recipe run security/full_redteam --adapter openai --model gpt-4

# Or in mock mode (no API calls)
aipop recipe run security/full_redteam --mock
```

## Supported Tools

### Promptfoo (Priority 1 - Most Adopted)

**Installation:**
```bash
npm install -g promptfoo
```

**Features:**
- Prompt injection detection
- Harmful content detection
- CI/CD integration
- Multiple model support

**Usage in Recipe:**
```yaml
tools:
  - tool: promptfoo
    config:
      plugins: ["prompt-injection", "harmful"]
      model: "gpt-4"
      provider: "openai"
```

### Garak (Priority 2 - IBM Research)

**Installation:**
```bash
pip install garak
```

**Features:**
- 100+ vulnerability probes
- Encoding attacks
- Jailbreak detection
- Academic backing

**Usage in Recipe:**
```yaml
tools:
  - tool: garak
    config:
      probes: ["encoding", "jailbreak"]
      model: "gpt-4"
```

### PyRIT (Priority 3 - Microsoft)

**Installation:**
```bash
pip install pyrit
```

**Features:**
- Red team orchestration
- Attack strategy automation
- Enterprise-grade

**Usage in Recipe:**
```yaml
tools:
  - tool: pyrit
    config:
      strategies: ["red-team-orchestrator"]
      model: "gpt-4"
```

### PromptInject (Priority 4 - Research)

**Installation:**
```bash
# Install from GitHub
git clone https://github.com/agencyenterprise/promptinject
cd promptinject && pip install -e .
```

**Features:**
- Academic attack patterns
- Research-backed methodologies

**Usage in Recipe:**
```yaml
tools:
  - tool: promptinject
    config:
      attacks: ["all"]
      model: "gpt-4"
```

### Indirect Injection Baseline (Built-in)

**No installation required** - Built into AI Purple Ops.

**Features:**
- File upload poisoning (PDF, CSV, Markdown)
- RAG poisoning basics
- Context confusion testing

**Usage in Recipe:**
```yaml
tools:
  - tool: indirect_injection
    config:
      vectors: ["file_upload", "rag_poisoning", "context_confusion"]
```

## Recipe Configuration

### Full Example

```yaml
version: 1
metadata:
  name: "Comprehensive Redteam"
  lane: security

config:
  adapter: "${MODEL_ADAPTER:-mock}"
  model: "${MODEL_NAME:-gpt-4}"

execution:
  suites:
    - normal
    - policies

  tools:
    - tool: promptfoo
      enabled: true
      config:
        plugins: ["prompt-injection", "harmful"]

    - tool: garak
      enabled: true
      config:
        probes: ["encoding", "jailbreak"]

    - tool: indirect_injection
      enabled: true
      config:
        vectors: ["file_upload", "rag_poisoning"]

gates:
  fail_on:
    - "redteam_success_rate > 0.0"
```

## Tool Comparison

| Tool | Installation | Strengths | Best For |
|------|-------------|-----------|----------|
| Promptfoo | `npm install -g promptfoo` | CI/CD, comprehensive | Production workflows |
| Garak | `pip install garak` | 100+ probes, academic | Research & testing |
| PyRIT | `pip install pyrit` | Enterprise, automation | Large-scale testing |
| PromptInject | GitHub clone | Research patterns | Academic validation |
| Indirect Injection | Built-in | File upload, RAG | Novel attack vectors |

## Interpreting Results

### Aggregated Report

After running a recipe with tools, check `out/reports/tool_results.json`:

```json
{
  "tools": [
    {
      "tool_name": "promptfoo",
      "success": true,
      "findings_count": 5,
      "findings": [...]
    }
  ]
}
```

### Evidence Pack

All tool outputs are included in the evidence pack ZIP:
- `reports/summary.json` - Test results
- `reports/tool_results.json` - Tool findings
- `reports/junit.xml` - CI/CD format

## Troubleshooting

### Tool Not Found

If a tool is not installed:
```bash
# Install all optional tools
pip install ai-purple-ops[redteam]

# Or install individually
npm install -g promptfoo
pip install garak pyrit
```

### Missing API Keys

Run in mock mode:
```bash
aipop recipe run security/full_redteam --mock
```

### Tool Execution Fails

Check tool-specific logs in `out/reports/tool_results.json`. Each tool wrapper handles errors gracefully and continues with other tools.

## Next Steps

- See [ADAPTERS.md](ADAPTERS.md) for custom adapter development
- See [INDIRECT_INJECTION.md](INDIRECT_INJECTION.md) for indirect injection methodology
- See [INTEGRATIONS.md](INTEGRATIONS.md) for adding new tool wrappers
