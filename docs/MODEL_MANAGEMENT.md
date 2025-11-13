# Model Management Guide

This guide explains how AI Purple Ops handles model storage to keep your repository clean and prevent accidental commits of large model files.

## Overview

**Key Principle:** Models are stored **outside** the repository by default. The framework uses standard cache directories and environment variables to manage model storage locations.

## Storage Locations by Adapter Type

### HuggingFace Models

**Default Location:** `~/.cache/huggingface/`

**Configuration:**
- Set `HF_HOME` environment variable to change cache location
- Example: `export HF_HOME=/opt/models/huggingface`

**What Gets Stored:**
- Model weights (downloaded automatically on first use)
- Tokenizer files
- Configuration files

**Disk Space:**
- Small models (1-3B): ~2-5 GB
- Medium models (7-13B): ~15-30 GB
- Large models (70B+): ~140+ GB

### Ollama Models

**Default Location:** `~/.ollama/models/` (Linux/Mac) or `%USERPROFILE%\.ollama\models` (Windows)

**Configuration:**
- Set `OLLAMA_MODELS` environment variable to change storage location
- Example: `export OLLAMA_MODELS=/opt/models/ollama`

**What Gets Stored:**
- Model files in Ollama's internal format
- Automatically managed by Ollama service

**Disk Space:**
- TinyLlama (1.1B): ~600 MB
- Phi-3-mini (3.8B): ~2.5 GB
- Gemma 2B: ~1.5 GB
- Larger models: 4-20 GB

### llama.cpp Models (GGUF Format)

**Storage:** User-specified file paths (not managed by framework)

**Best Practices:**
- Store in dedicated directory: `~/models/` or `/opt/models/`
- Use descriptive filenames: `tinyllama-1.1b-q4_k_m.gguf`
- Keep model files organized by model family

**Disk Space:**
- Quantized models (Q4_K_M): ~50-70% of original size
- Q8_0: ~80-90% of original size

### Cloud API Models (OpenAI, Anthropic, AWS Bedrock)

**Storage:** No local storage required

**Configuration:**
- API keys stored in environment variables (never in repo)
- Example: `export OPENAI_API_KEY=sk-...`

## Environment Variables Reference

| Variable | Purpose | Default | Example |
|----------|---------|---------|---------|
| `HF_HOME` | HuggingFace cache directory | `~/.cache/huggingface` | `/opt/models/hf` |
| `OLLAMA_MODELS` | Ollama models directory | `~/.ollama/models` | `/opt/models/ollama` |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://localhost:11434` | `http://192.168.1.100:11434` |
| `TRANSFORMERS_CACHE` | Transformers cache (alternative to HF_HOME) | Same as HF_HOME | `/opt/models/transformers` |

## Configuration in harness.yaml

You can configure model storage in `configs/harness.yaml`:

```yaml
model_storage:
  # Local model cache (for HuggingFace)
  cache_dir: ${HF_HOME:-~/.cache/huggingface}

  # Maximum disk usage warning threshold (GB)
  max_cache_size_gb: 50

  # Ollama configuration
  ollama:
    base_url: ${OLLAMA_BASE_URL:-http://localhost:11434}
    models_dir: ${OLLAMA_MODELS:-~/.ollama/models}
```

## Sharing Model Configurations

**DO Share:**
- Recipe YAML files (they reference models, not store them)
- Adapter configuration files
- Model names/IDs (e.g., `"tinyllama"`, `"TinyLlama/TinyLlama-1.1B-Chat-v1.0"`)

**DON'T Share:**
- Model weight files (`.bin`, `.safetensors`, `.gguf`)
- Model cache directories
- API keys or credentials

**Example Recipe (Safe to Commit):**
```yaml
config:
  adapter: ollama
  adapter_config:
    model: tinyllama  # Just the name, not the file
    base_url: http://localhost:11434
```

## Disk Space Management

### Checking Cache Size

**HuggingFace:**
```bash
du -sh ~/.cache/huggingface/
```

**Ollama:**
```bash
du -sh ~/.ollama/models/
```

### Cleaning Cache

**HuggingFace:**
```bash
# Remove specific model
rm -rf ~/.cache/huggingface/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0

# Clear entire cache (WARNING: removes all models)
rm -rf ~/.cache/huggingface/*
```

**Ollama:**
```bash
# List models
ollama list

# Remove specific model
ollama rm tinyllama

# Clean up unused models
ollama prune
```

**Using Framework Command:**
```bash
python -m cli.harness adapter clean
```

## CI/CD Best Practices

### GitHub Actions / GitLab CI

**DO:**
- Use lightweight models for CI (TinyLlama, Phi-3-mini)
- Set cache size limits
- Use model caching in CI runners
- Test with mock adapter for fast feedback

**DON'T:**
- Download large models in every CI run
- Store models in repository
- Commit model files

**Example CI Configuration:**
```yaml
# .github/workflows/test.yml
env:
  HF_HOME: ${{ runner.temp }}/hf_cache
  OLLAMA_MODELS: ${{ runner.temp }}/ollama_models

steps:
  - name: Cache HuggingFace models
    uses: actions/cache@v3
    with:
      path: ${{ env.HF_HOME }}
      key: hf-models-${{ hashFiles('requirements.txt') }}
```

## Troubleshooting

### "Model not found" Error

**HuggingFace:**
- Check model ID is correct (case-sensitive)
- Verify internet connection for first download
- Check `HF_HOME` directory permissions

**Ollama:**
- Run `ollama list` to see available models
- Pull model: `ollama pull <model_name>`
- Check Ollama service is running: `ollama serve`

**llama.cpp:**
- Verify file path is correct
- Check file exists and is readable
- Ensure file is valid GGUF format

### "Out of disk space" Error

1. Check current usage: `df -h`
2. Clean unused models (see "Cleaning Cache" above)
3. Move cache to larger disk:
   ```bash
   export HF_HOME=/mnt/large-disk/huggingface
   ```

### "Permission denied" Error

- Check directory permissions: `ls -ld ~/.cache/huggingface`
- Fix permissions: `chmod -R u+w ~/.cache/huggingface`
- Or use different location with write access

## Best Practices Summary

1. **Never commit model files** - They're in `.gitignore` for a reason
2. **Use environment variables** - Configure storage locations via env vars
3. **Monitor disk space** - Large models can fill up disks quickly
4. **Share configs, not models** - Commit recipe files, not model weights
5. **Use lightweight models for testing** - Save large models for production
6. **Clean up regularly** - Remove unused models to free space

## See Also

- [Adapter Quick Start Guide](ADAPTERS_QUICKSTART.md) - How to set up adapters
- [Adapter Documentation](ADAPTERS.md) - Custom adapter development
- [Recipe System](RECIPES.md) - Using models in recipes
