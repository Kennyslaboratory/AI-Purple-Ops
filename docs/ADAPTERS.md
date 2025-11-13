# Adapters Guide

Adapters connect AI Purple Ops to any AI model - commercial APIs, local models, or custom endpoints.

## 🚀 For Pentesters: Quick Adapter Generation

**Generate adapters from Burp/cURL in 2-3 minutes** without writing Python code.

👉 **See [QUICK_ADAPTER.md](QUICK_ADAPTER.md) for the pentester-optimized workflow**

```bash
# From Burp: Right-click → Copy as cURL
aipop adapter quick --name target_app --from-curl "curl 'https://api.target.com/chat' ..."

# Test it
aipop adapter test --name target_app

# Use it
aipop run --suite adversarial --adapter target_app
```

---

## Quick Start

### Use Built-in Adapters

AI Purple Ops includes production-ready adapters:

```bash
# List available adapters
aipop adapter list

# Test an adapter
aipop adapter test --name openai
```

**Available:**
- `openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models
- `huggingface` - HuggingFace models (local)
- `ollama` - Ollama (local models)
- `mock` - Testing adapter (no API needed)

### Common Scenarios

#### Scenario 1: OpenAI (Cloud API)

```bash
# Set API key
export OPENAI_API_KEY=sk-your-key-here

# Run a test
aipop run --suite normal --adapter openai

# Or via config
export MODEL_ADAPTER=openai
aipop recipe run --recipe content_policy_baseline
```

#### Scenario 2: Local Model (Ollama)

```bash
# 1. Install and start Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &

# 2. Pull a model
ollama pull llama3.1

# 3. Run tests
export MODEL_ADAPTER=ollama
aipop run --suite adversarial
```

#### Scenario 3: HuggingFace Local

```bash
# Set model cache directory (optional)
export HF_HOME=~/.cache/huggingface

# Run with specific model
aipop run --suite normal --adapter huggingface \
  --model-name "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

---

## Creating Custom Adapters

Need to connect to a proprietary model or custom endpoint? Create a custom adapter.

### Method 1: Interactive Wizard

```bash
aipop adapter init

# Wizard will ask:
# - Adapter name
# - Model type (API, local, custom)
# - Connection details
# - Authentication method
```

### Method 2: Copy Template

```bash
# Create from template
aipop adapter init --template openai --name my_custom_api

# Edit the generated file
vim adapters/my_custom_api.py
```

### Method 3: Write from Scratch

Create `adapters/my_adapter.py`:

```python
from harness.core import Adapter, ModelResponse
from typing import Any

class MyCustomAdapter(Adapter):
    """Adapter for my custom model."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        **kwargs: Any
    ):
        self.model = model
        self.api_key = api_key

    def invoke(self, prompt: str, **kwargs: Any) -> ModelResponse:
        """Send prompt to model and return response."""
        # Your model integration here
        response = self.my_model_api_call(prompt)

        return ModelResponse(
            content=response.text,
            model=self.model,
            finish_reason="stop",
            usage={
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
            }
        )
```

---

## Adapter Protocol

All adapters must implement the `Adapter` protocol:

```python
from typing import Protocol, Any

class Adapter(Protocol):
    def invoke(self, prompt: str, **kwargs: Any) -> ModelResponse:
        """
        Send prompt to model and return response.

        Args:
            prompt: The prompt text to send
            **kwargs: Model-specific parameters (temperature, max_tokens, etc.)

        Returns:
            ModelResponse with content and metadata
        """
        ...
```

### ModelResponse

```python
@dataclass
class ModelResponse:
    content: str                 # Generated text
    model: str                   # Model identifier
    finish_reason: str           # stop, length, error, etc.
    usage: dict[str, int] | None # Token counts, if available
```

---

## Configuration

### Via Config File

```yaml
# configs/harness.yaml
adapters:
  openai:
    type: openai
    model: gpt-4o-mini
    api_key_env: OPENAI_API_KEY
    timeout: 30

  local_llama:
    type: ollama
    model: llama3.1:70b
    base_url: http://localhost:11434
```

### Via Environment

```bash
# Adapter selection
export MODEL_ADAPTER=openai

# Adapter-specific config
export OPENAI_API_KEY=sk-your-key
export ANTHROPIC_API_KEY=sk-ant-your-key
export OLLAMA_BASE_URL=http://localhost:11434
```

### Via CLI

```bash
# Override adapter at runtime
aipop run --suite redteam \
  --adapter openai \
  --model gpt-4o \
  --temperature 0.7
```

---

## Built-in Adapters Reference

### OpenAI Adapter

**Configuration:**
```yaml
type: openai
model: gpt-4o-mini  # or gpt-4o, gpt-3.5-turbo
api_key_env: OPENAI_API_KEY
base_url: https://api.openai.com/v1  # optional
timeout: 30
```

**Environment:**
```bash
export OPENAI_API_KEY=sk-your-key-here
export MODEL_ADAPTER=openai
```

**Features:**
- Automatic retries with exponential backoff
- Token counting and cost calculation
- Streaming support (planned)

### Anthropic Adapter

**Configuration:**
```yaml
type: anthropic
model: claude-3-5-sonnet-20241022
api_key_env: ANTHROPIC_API_KEY
timeout: 60
```

**Environment:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key
export MODEL_ADAPTER=anthropic
```

**Features:**
- Claude 3.5 Sonnet, Claude 3 Opus support
- Automatic cost calculation
- Long context window support

### Ollama Adapter

**Configuration:**
```yaml
type: ollama
model: llama3.1:70b
base_url: http://localhost:11434
```

**Environment:**
```bash
export OLLAMA_BASE_URL=http://localhost:11434
export MODEL_ADAPTER=ollama
```

**Features:**
- Local model support
- No API key required
- Works with any Ollama-compatible model

### HuggingFace Adapter

**Configuration:**
```yaml
type: huggingface
model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
cache_dir: ~/.cache/huggingface
load_in_4bit: true  # Memory optimization
```

**Environment:**
```bash
export HF_HOME=~/.cache/huggingface
export MODEL_ADAPTER=huggingface
```

**Features:**
- Local inference with transformers
- Automatic model downloading
- 4-bit quantization support

---

## Testing and Validation

### Test Connection

```bash
# Test if adapter can connect
aipop adapter test --name openai

# Expected output:
# ✓ Adapter 'openai' connected successfully
# ✓ Model: gpt-4o-mini
# ✓ Response time: 1.2s
```

### Validate Implementation

```bash
# Run adapter validation suite
aipop run --suite adapters/adapter_validation --adapter my_adapter

# Checks:
# - Protocol compliance
# - Error handling
# - Response format
# - Retry behavior
```

### Dry Run

```bash
# Test adapter without using credits/quota
aipop run --suite normal --adapter openai --dry-run

# Uses mock responses instead of real API calls
```

---

## Advanced Topics

### Retry Logic

Built-in adapters include automatic retry with exponential backoff:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class MyAdapter:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def invoke(self, prompt: str, **kwargs: Any) -> ModelResponse:
        # Will retry up to 3 times with exponential backoff
        ...
```

### Cost Tracking

Add cost calculation to your adapter:

```python
def invoke(self, prompt: str, **kwargs: Any) -> ModelResponse:
    response = self.api_call(prompt)

    # Calculate cost
    input_cost = response.prompt_tokens * self.PRICE_PER_1K_INPUT / 1000
    output_cost = response.completion_tokens * self.PRICE_PER_1K_OUTPUT / 1000

    return ModelResponse(
        content=response.text,
        model=self.model,
        finish_reason="stop",
        usage={
            "prompt_tokens": response.prompt_tokens,
            "completion_tokens": response.completion_tokens,
            "total_cost": input_cost + output_cost,
        }
    )
```

### Error Handling

Handle API errors gracefully:

```python
def invoke(self, prompt: str, **kwargs: Any) -> ModelResponse:
    try:
        response = self.api_call(prompt)
        return ModelResponse(content=response.text, ...)

    except RateLimitError as e:
        # Will trigger retry logic
        raise

    except AuthenticationError as e:
        # Fatal error, don't retry
        raise RuntimeError(f"Authentication failed: {e}")

    except APIError as e:
        # Log and raise
        logger.error(f"API error: {e}")
        raise
```

---

## Troubleshooting

### "Adapter not found"

**Cause:** Adapter name doesn't match registered adapters.

**Fix:**
```bash
# List available adapters
aipop adapter list

# Check adapter is registered
ls adapters/*.py
```

### "Connection failed"

**Cause:** Service not running or wrong configuration.

**Fix:**
```bash
# For Ollama
ollama serve  # Start service
curl http://localhost:11434/api/tags  # Test endpoint

# For APIs
env | grep API_KEY  # Check key is set
aipop adapter test --name openai  # Test connection
```

### "Out of memory"

**Cause:** Model too large for available RAM/VRAM.

**Fix:**
```yaml
# Enable quantization for HuggingFace
type: huggingface
load_in_4bit: true  # Reduces memory by ~75%
device_map: auto    # Automatic GPU/CPU split
```

### "Model not found"

**Cause:** Model not downloaded or wrong identifier.

**Fix:**
```bash
# For Ollama
ollama list  # See downloaded models
ollama pull llama3.1  # Download model

# For HuggingFace
# Models download automatically on first use
# Check HF_HOME for cache location
```

---

## Best Practices

1. **Use environment variables for secrets** - Never hardcode API keys
2. **Test adapters before production** - Run validation suite
3. **Implement retry logic** - Handle transient failures gracefully
4. **Track costs** - Add cost calculation for commercial APIs
5. **Cache responses** - Reduce API costs during development
6. **Handle errors explicitly** - Don't let exceptions crash tests
7. **Document requirements** - List dependencies in adapter docstring

---

## Next Steps

- [CLI Reference](CLI.md) - Command-line usage
- [Recipes Guide](RECIPES.md) - Using adapters in recipes
- [Model Management](MODEL_MANAGEMENT.md) - Disk space and caching
- [Configuration Guide](CONFIGURATION.md) - Advanced config options
