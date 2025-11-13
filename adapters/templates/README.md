# Adapter Templates

This directory contains template code for creating custom adapters.

## Available Templates

- `base.py` - Base adapter template with minimal implementation
- `api_openai.py` - OpenAI-compatible REST API template
- `api_custom.py` - Custom REST API endpoint template
- `local_ollama.py` - Ollama local model template
- `local_huggingface.py` - HuggingFace local model template
- `local_llamacpp.py` - llama.cpp GGUF model template

## Usage

Templates are automatically used by the adapter wizard:

```bash
python -m cli.harness adapter init
```

Or reference them manually when creating custom adapters.

## Template Structure

All templates follow the Adapter protocol:

```python
class MyAdapter:
    def __init__(self, **kwargs):
        # Initialize connection, load model, etc.
        pass

    def invoke(self, prompt: str, **kwargs) -> ModelResponse:
        # Invoke model and return response
        return ModelResponse(text="...", meta={...})
```

## See Also

- [Adapter Quick Start Guide](../docs/ADAPTERS_QUICKSTART.md)
- [Adapter Documentation](../docs/ADAPTERS.md)
