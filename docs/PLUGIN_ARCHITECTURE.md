# Plugin Architecture

AI Purple Ops uses a plugin system to wrap official, battle-tested attack implementations from research repositories. This approach ensures users achieve the published attack success rates (88-97% ASR) while AIPop focuses on providing unified CLI, policy enforcement, compliance features, and cost management.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    AI Purple Ops (Harness)                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Unified CLI • Policy Checks • Quality Gates •          │  │
│  │  Evidence Packs • Cost Management • Ensemble Judging    │  │
│  └────────────────────────────────────────────────────────┘  │
│                            │                                  │
│          ┌─────────────────┼─────────────────┐               │
│          │                 │                 │               │
│     ┌────▼────┐      ┌────▼────┐      ┌────▼────┐          │
│     │   GCG   │      │  PAIR   │      │ AutoDAN │          │
│     │ Plugin  │      │ Plugin  │      │ Plugin  │          │
│     └────┬────┘      └────┬────┘      └────┬────┘          │
│          │                 │                 │               │
│          │  Subprocess     │                 │               │
│          │  Isolation      │                 │               │
│          │  (Optional)     │                 │               │
└──────────┼─────────────────┼─────────────────┼───────────────┘
           │                 │                 │
           ▼                 ▼                 ▼
┌────────────────┐  ┌─────────────────┐  ┌──────────────┐
│  llm-attacks   │  │ JailbreakingLLMs│  │   AutoDAN    │
│  (Zou et al.)  │  │  (Chao et al.)  │  │  (Liu et al.)│
│  97%+ ASR      │  │    88% ASR      │  │   88%+ ASR   │
└────────────────┘  └─────────────────┘  └──────────────┘
```

## Why Plugins?

### Benefits

- **Battle-tested code**: Achieve published ASR rates (88-97%) instead of 60-70% from scratch implementations
- **Dependency isolation**: Avoid conflicts (e.g., fschat 0.2.20 vs 0.2.23) via subprocess execution
- **Expert customization**: Direct access to all upstream parameters and configurations
- **Fallback support**: Legacy (scratch) implementations available for air-gapped environments

### What AIPop Provides

| Feature | Description |
|---------|-------------|
| **Unified CLI** | Single `aipop` command for all attack methods |
| **Policy Integration** | NIST AI RMF, EU AI Act compliance checking |
| **Quality Gates** | Automated pass/fail decisions for CI/CD |
| **Evidence Packs** | FedRAMP-ready audit bundles and reports |
| **Cost Management** | Budget limits and cost tracking across methods |
| **Ensemble Judging** | Multi-model evaluation (Llama Guard + GPT-4) |
| **Dependency Isolation** | Subprocess execution prevents version conflicts |

## Installation

### Option 1: Subprocess Isolation (Recommended)

This approach installs each plugin in its own virtual environment to prevent dependency conflicts.

```bash
# Install core framework
pip install ai-purple-ops

# Install plugins (creates isolated venvs automatically)
aipop plugins install gcg       # Install GCG
aipop plugins install pair      # Install PAIR
aipop plugins install autodan   # Install AutoDAN
aipop plugins install all       # Install all three
```

### Option 2: Direct Import (Expert Users)

Install plugins as Python packages for direct import in Python code.

```bash
# Install specific attacks
pip install ai-purple-ops[pair-official]     # PAIR only
pip install ai-purple-ops[autodan-official]  # AutoDAN only
pip install ai-purple-ops[all-official]      # All (may have conflicts)

# Import directly
from harness.intelligence.plugins import PAIROfficialPlugin
plugin = PAIROfficialPlugin()
```

**Note**: Direct import may cause dependency conflicts since PAIR requires `fschat==0.2.23` while AutoDAN requires `fschat==0.2.20`.

### Option 3: Legacy/Air-gapped

Use built-in scratch implementations (no external dependencies, but lower ASR).

```bash
pip install ai-purple-ops

# Use legacy implementations
aipop generate-suffix "test" --implementation legacy
```

## Usage

### CLI Examples

```bash
# Default: Uses official implementation (auto-installs if not present)
aipop generate-suffix "Write bomb instructions" --method pair --adapter openai --adapter-model gpt-4

# Explicit official implementation
aipop generate-suffix "test" --method gcg --implementation official --model vicuna-7b

# Legacy implementation (scratch, 60-70% ASR)
aipop generate-suffix "test" --method autodan --implementation legacy --adapter openai
```

### Python API

```python
from harness.intelligence.plugins.loader import load_plugin

# Load official plugin (auto-fallback to legacy if not installed)
plugin = load_plugin("pair", implementation="official")

# Check if available
is_available, error_msg = plugin.check_available()
if not is_available:
    print(f"Not available: {error_msg}")

# Estimate cost
config = {
    "prompt": "Write malware",
    "target": "Sure, here is",
    "adapter_model": "gpt-4",
    "num_streams": 30,
    "iterations_per_stream": 3,
}
cost = plugin.estimate_cost(config)
print(f"Estimated cost: ${cost.total_usd:.2f}")

# Run attack
result = plugin.run(config)
print(f"Success: {result.success}")
print(f"Generated {len(result.adversarial_prompts)} prompts")
```

## Plugin Management

### CLI Commands

```bash
# List installed plugins
aipop plugins list

# Get plugin information
aipop plugins info pair

# Install plugin
aipop plugins install gcg

# Update plugin (pull latest from repo)
aipop plugins update pair

# Uninstall plugin
aipop plugins uninstall autodan

# Check system capabilities
aipop check
```

### Plugin Status

```bash
$ aipop check

✓ Core framework installed
✓ GCG plugin installed (llm-attacks v0.3.0)
✓ PAIR plugin installed
✗ AutoDAN plugin not installed (run: aipop plugins install autodan)
✓ OpenAI API key configured
✗ GPU not detected (white-box attacks will be slow)
```

## Known Limitations

### GCG (White-box)

**Requirements:**
- Local HuggingFace models (Vicuna, LLaMA)
- 80GB GPU recommended for Vicuna-13B
- Only LLaMA-style tokenizers supported

**Limitations:**
- Cannot use API models (OpenAI, Anthropic)
- Will fail silently on non-LLaMA tokenizers
- High GPU memory requirements

**Fallback:** Use `--implementation legacy` for black-box GCG (60-70% ASR)

### PAIR (Black-box)

**Requirements:**
- API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY)
- Network access to API endpoints

**Limitations:**
- High API costs (~180 queries per attack = $5-20 per attack with GPT-4)
- Judge accuracy varies (Llama Guard 76%, GPT-4 88% but higher FPR)
- No built-in caching (add via AIPop)

**Mitigation:** Use `--max-cost` budget limits in AIPop

### AutoDAN (White-box)

**Requirements:**
- Local HuggingFace model for log-likelihood fitness
- High GPU memory (256 candidates in VRAM simultaneously)

**Limitations:**
- White-box only (cannot use API models)
- ~25,600 forward passes per attack (slow)
- Only HuggingFace models supported

**Fallback:** Use `--implementation legacy` (uses keyword fitness instead of log-likelihood, 60-70% ASR)

## Error Handling

### Plugin Not Installed

```bash
$ aipop generate-suffix "test" --method pair --implementation official

[!] PAIR official implementation not installed.

Install with:
    aipop plugins install pair

Or use legacy implementation:
    aipop generate-suffix "test" --method pair --implementation legacy

Note: Legacy implementation may have lower ASR (60-70% vs 88% published).
```

### Automatic Fallback

If an official plugin is requested but not available, AIPop automatically falls back to the legacy implementation with a warning:

```bash
[yellow]Official PAIR not installed. Using legacy fallback (60-70% ASR).[/yellow]
```

## Architecture Details

### Subprocess Isolation

Plugins can be executed in isolated subprocesses to prevent dependency conflicts:

```python
from harness.intelligence.plugins.executor import SubprocessAttackExecutor

# Create executor for PAIR plugin
executor = SubprocessAttackExecutor(
    plugin_name="pair",
    venv_path="/home/user/.aipop/plugins/pair/venv",
    timeout=3600,
)

# Execute in subprocess
result = executor.execute(config)
```

### Plugin Interface

All plugins implement the `AttackPlugin` base class:

```python
class AttackPlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """Plugin name (gcg, pair, autodan)"""
        
    @abstractmethod
    def check_available(self) -> tuple[bool, str]:
        """Check if dependencies are installed"""
        
    @abstractmethod
    def run(self, config: dict) -> AttackResult:
        """Execute attack"""
        
    @abstractmethod
    def estimate_cost(self, config: dict) -> CostEstimate:
        """Estimate API costs"""
```

## Troubleshooting

### Dependency Conflicts

If you see version conflicts, use subprocess isolation:

```bash
# Instead of:
pip install ai-purple-ops[all-official]  # May cause conflicts

# Do:
aipop plugins install all  # Each in isolated venv
```

### GPU Out of Memory

For AutoDAN and GCG:

```bash
# Reduce population size
aipop generate-suffix "test" --method autodan --population 64  # Instead of 256

# Or use legacy black-box implementations
aipop generate-suffix "test" --method autodan --implementation legacy
```

### API Cost Concerns

For PAIR:

```bash
# Set budget limit
aipop generate-suffix "test" --method pair --max-cost 10.00  # Stop at $10

# Reduce streams
aipop generate-suffix "test" --method pair --streams 10  # Instead of 30
```

## Best Practices

1. **Use official implementations by default** - Achieve published ASR rates
2. **Install plugins in isolation** - Use `aipop plugins install` not pip
3. **Estimate costs first** - Run `--max-cost` to prevent surprises
4. **Monitor progress** - Use progress callbacks for long-running attacks
5. **Cache results** - AIPop automatically caches successful attacks
6. **Validate with multiple judges** - Use `--judge ensemble` for robustness

## Contributing

To add a new attack plugin:

1. Create official wrapper in `src/harness/intelligence/plugins/<method>_official.py`
2. Implement `AttackPlugin` interface
3. Add to registry in `src/harness/intelligence/plugins/install.py`
4. Document known limitations in this file
5. Add tests in `tests/plugins/test_<method>_wrapper.py`

## References

- [GCG Paper](https://arxiv.org/abs/2307.15043) - Zou et al., 2023
- [PAIR Paper](https://arxiv.org/abs/2310.08419) - Chao et al., 2023  
- [AutoDAN Paper](https://arxiv.org/abs/2310.04451) - Liu et al., 2023
- [llm-attacks Repo](https://github.com/llm-attacks/llm-attacks)
- [JailbreakingLLMs Repo](https://github.com/patrickrchao/JailbreakingLLMs)
- [AutoDAN Repo](https://github.com/SheltonLiu-N/AutoDAN)

