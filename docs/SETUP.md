# Setup Guide

Complete guide for configuring AI Purple Ops for your environment.

## Table of Contents

- [Quick Start](#quick-start)
- [API Key Configuration](#api-key-configuration)
- [Configuration Methods](#configuration-methods)
- [Adapter-Specific Setup](#adapter-specific-setup)
- [Environment Variables](#environment-variables)
- [Configuration Priority](#configuration-priority)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

**5-minute setup:**

```bash
# 1. Clone and install
git clone https://github.com/Kennyslaboratory/AI-Purple-Ops.git
cd AI-Purple-Ops
pip install -e .

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env and add your API key
nano .env  # or vim, or any editor

# 4. Test it
aipop run --suite adversarial --adapter openai --model gpt-3.5-turbo
```

---

## API Key Configuration

### Method 1: `.env` File (Recommended)

**Best for:** Project-specific configuration, teams, avoiding accidental exposure

**Steps:**

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your keys:**
   ```bash
   # .env
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```

3. **Verify `.env` is in `.gitignore`:**
   ```bash
   grep -q "^\.env$" .gitignore && echo "✓ .env is gitignored" || echo "✗ WARNING: .env not gitignored!"
   ```

**Advantages:**
- ✅ Automatic loading (no manual export needed)
- ✅ Project-specific (each project can have different keys)
- ✅ Gitignored by default (won't accidentally commit)
- ✅ Team-friendly (everyone uses same `.env` format)
- ✅ Easy to manage multiple environments (dev, staging, prod)

**Disadvantages:**
- ❌ Need to copy `.env.example` first
- ❌ File-based (could be read by other processes)

---

### Method 2: Shell Export (Temporary)

**Best for:** One-off testing, temporary access, debugging

**Steps:**

```bash
# Set for current shell session only
export OPENAI_API_KEY="sk-proj-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Verify it's set
echo $OPENAI_API_KEY

# Run tests (key is available for this session)
aipop run --suite adversarial --adapter openai
```

**Advantages:**
- ✅ Quick and simple
- ✅ Session-only (expires when you close terminal)
- ✅ No file management

**Disadvantages:**
- ❌ Temporary (lost when terminal closes)
- ❌ Need to re-export for each new terminal
- ❌ Easy to forget to set

---

### Method 3: Shell Profile (Persistent)

**Best for:** Personal development, single-user systems, CLI-heavy workflows

**Steps:**

1. **Add to your shell profile:**

   ```bash
   # For bash users:
   echo 'export OPENAI_API_KEY="sk-proj-your-key-here"' >> ~/.bashrc
   echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
   source ~/.bashrc

   # For zsh users:
   echo 'export OPENAI_API_KEY="sk-proj-your-key-here"' >> ~/.zshrc
   echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. **Verify:**
   ```bash
   echo $OPENAI_API_KEY
   ```

**Advantages:**
- ✅ Always available (every new terminal has the key)
- ✅ No file management per project
- ✅ Works for all projects

**Disadvantages:**
- ❌ Global (same key for all projects)
- ❌ Could be logged in shell history
- ❌ Harder to rotate keys (need to edit profile)

---

### Method 4: CLI Flag (Not Recommended for Keys)

**Note:** We do NOT support passing API keys via CLI flags for security reasons.

**Why not?**
- ❌ Keys visible in shell history
- ❌ Keys visible in process list (`ps aux`)
- ❌ Keys visible in CI/CD logs
- ❌ Security risk

**Use environment variables or `.env` files instead.**

---

## Configuration Methods

### Priority Order

Configuration is loaded in this priority (highest to lowest):

```
1. CLI Flags (highest priority)
   ↓
2. Environment Variables
   ↓
3. .env File
   ↓
4. Config Files (configs/harness.yaml)
   ↓
5. Defaults (lowest priority)
```

**Example:**

```bash
# .env file has:
OPENAI_API_KEY=sk-proj-from-dotenv

# Environment variable overrides .env:
export OPENAI_API_KEY=sk-proj-from-export

# CLI flag overrides both:
aipop run --adapter openai --model gpt-4o  # Uses sk-proj-from-export
```

---

## Adapter-Specific Setup

### OpenAI

**Required:**
- API key from https://platform.openai.com/api-keys

**Configuration:**

```bash
# .env
OPENAI_API_KEY=sk-proj-your-key-here
```

**Test:**

```bash
aipop run --suite adversarial --adapter openai --model gpt-3.5-turbo
```

**Models:**
- `gpt-3.5-turbo` - Cheapest, fastest ($0.0005/1K tokens)
- `gpt-4o-mini` - Balanced ($0.00015/1K input, $0.0006/1K output)
- `gpt-4o` - Best quality ($0.005/1K input, $0.015/1K output)

---

### Anthropic

**Required:**
- API key from https://console.anthropic.com/settings/keys

**Configuration:**

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Test:**

```bash
aipop run --suite adversarial --adapter anthropic --model claude-3-5-sonnet-20241022
```

**Models:**
- `claude-3-5-haiku-20241022` - Fast and economical
- `claude-3-5-sonnet-20241022` - Best for security testing
- `claude-3-opus-20240229` - Highest quality (expensive)

---

### Ollama (No API Key Required)

**Required:**
- Ollama installed locally

**Installation:**

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from: https://ollama.com
```

**Setup:**

1. **Start Ollama service:**
   ```bash
   ollama serve
   ```

2. **Download a model:**
   ```bash
   # For testing/debugging (637MB)
   ollama pull tinyllama

   # For actual security testing (4.7GB)
   ollama pull llama3.1:8b
   ```

3. **Test:**
   ```bash
   aipop run --suite adversarial --adapter ollama --model tinyllama
   ```

**No API keys needed!** Everything runs locally.

---

### Mock Adapter (No Configuration)

**Best for:** Development, testing tool logic without API costs

**Usage:**

```bash
# No setup needed, works out of the box
aipop run --suite adversarial --adapter mock --response-mode smart
```

**Response modes:**
- `passthrough` - Echo the prompt back
- `smart` - Simulate realistic responses (default)
- `refuse` - Always refuse (test safety logic)
- `error` - Simulate errors (test error handling)

---

## Environment Variables

### API Keys

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key | `your-azure-key` |
| `AWS_ACCESS_KEY_ID` | AWS Bedrock access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS Bedrock secret key | `...` |

### Harness Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `AIPO_OUTPUT_DIR` | Output directory | `out` |
| `AIPO_LOG_LEVEL` | Logging level | `INFO` |
| `AIPO_SEED` | Random seed | `42` |
| `AIPO_DEBUG` | Enable debug mode | `false` |
| `AIPO_VERBOSE` | Enable verbose mode | `false` |

### Rate Limiting

| Variable | Description | Default |
|----------|-------------|---------|
| `AIPO_RATE_LIMIT_TOKENS_PER_MINUTE` | Max tokens/min | `50000` |
| `AIPO_RATE_LIMIT_REQUESTS_PER_MINUTE` | Max requests/min | `100` |

### Cost Control

| Variable | Description | Default |
|----------|-------------|---------|
| `AIPO_COST_WARN_THRESHOLD` | Warn if cost exceeds (USD) | `1.0` |
| `AIPO_COST_FAIL_THRESHOLD` | Fail if cost exceeds (USD) | `10.0` |

---

## Configuration Priority

### Example: Multiple Configuration Sources

```yaml
# configs/harness.yaml
run:
  log_level: WARNING
```

```bash
# .env
AIPO_LOG_LEVEL=INFO
```

```bash
# Shell
export AIPO_LOG_LEVEL=DEBUG
```

```bash
# CLI
aipop run --log-level ERROR
```

**Result:** `ERROR` (CLI wins)

**Priority:**
1. CLI flag: `--log-level ERROR` ← **Winner**
2. Environment: `export AIPO_LOG_LEVEL=DEBUG`
3. .env: `AIPO_LOG_LEVEL=INFO`
4. Config file: `log_level: WARNING`
5. Default: `INFO`

---

## Troubleshooting

### "OpenAI API key not found"

**Error:**
```
ValueError: OpenAI API key not found. Set OPENAI_API_KEY environment variable.
Example: export OPENAI_API_KEY=sk-...
Or use --adapter mock for testing without API keys.
```

**Solutions:**

1. **Check if key is set:**
   ```bash
   echo $OPENAI_API_KEY
   ```

2. **If empty, set it:**
   ```bash
   export OPENAI_API_KEY="sk-proj-your-key-here"
   ```

3. **Or create `.env` file:**
   ```bash
   cp .env.example .env
   nano .env  # Add your key
   ```

4. **Or use mock adapter for testing:**
   ```bash
   aipop run --adapter mock
   ```

---

### ".env file not loaded"

**Symptoms:**
- Keys are in `.env`
- CLI still says "API key not found"

**Solutions:**

1. **Verify `.env` is in project root:**
   ```bash
   ls -la .env
   ```

2. **Verify `.env` syntax:**
   ```bash
   cat .env | grep OPENAI_API_KEY
   # Should be: OPENAI_API_KEY=sk-proj-...
   # NOT: export OPENAI_API_KEY=sk-proj-...
   ```

3. **Check for typos:**
   ```bash
   # Correct:
   OPENAI_API_KEY=sk-proj-...

   # Wrong:
   OPENAI_API_KEY = sk-proj-...  # Spaces not allowed
   OPENAI_API_KEY="sk-proj-..."  # Quotes optional but OK
   ```

4. **Run from project root:**
   ```bash
   cd /path/to/AI-Purple-Ops
   aipop run ...
   ```

---

### "Rate limit exceeded"

**Error:**
```
RateLimitError: Rate limit exceeded (429)
```

**Solutions:**

1. **Check your API tier:**
   - Free tier: 3 RPM (requests per minute)
   - Pay-as-you-go: 60-3500 RPM depending on model

2. **Adjust rate limits in `.env`:**
   ```bash
   AIPO_RATE_LIMIT_REQUESTS_PER_MINUTE=3  # For free tier
   ```

3. **Or use `--adapter mock` for development:**
   ```bash
   aipop run --adapter mock
   ```

---

### "API key visible in error messages"

**Symptoms:**
- Error logs show full API key
- Security concern

**Solutions:**

1. **API keys are automatically redacted in logs**
   - First 8 chars: `sk-proj-ab` → `sk-proj-ab...`
   - Rest: Hidden

2. **If you see full keys, report a bug:**
   - This is a security issue
   - File at: https://github.com/Kennyslaboratory/AI-Purple-Ops/issues

---

### "Cost too high"

**Error:**
```
⚠️  Cost estimate: $12.50 (above fail threshold $10.0)
Test execution blocked.
```

**Solutions:**

1. **Increase threshold in `.env`:**
   ```bash
   AIPO_COST_FAIL_THRESHOLD=20.0
   ```

2. **Use cheaper model:**
   ```bash
   # Instead of gpt-4o
   aipop run --adapter openai --model gpt-3.5-turbo
   ```

3. **Test with mock adapter first:**
   ```bash
   aipop run --adapter mock
   ```

4. **Run fewer tests:**
   ```bash
   # Instead of full suite
   aipop run --suite suites/adversarial/basic_jailbreak.yaml
   ```

---

## Security Best Practices

### ✅ DO

- ✅ Use `.env` files for local development
- ✅ Use CI/CD secrets for production (GitHub Secrets, etc.)
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Rotate API keys regularly (every 90 days)
- ✅ Use separate keys for dev/staging/prod
- ✅ Monitor API usage dashboards

### ❌ DON'T

- ❌ Commit `.env` files to git
- ❌ Pass keys via CLI flags
- ❌ Share keys in Slack/email
- ❌ Use production keys for development
- ❌ Store keys in code
- ❌ Use weak/test keys in production

---

## Next Steps

- [CLI Reference](CLI.md) - Learn all commands and flags
- [Adapters Guide](ADAPTERS.md) - Detailed adapter configuration
- [Configuration Guide](CONFIGURATION.md) - Advanced configuration options

---

**Need help?** [Open an issue](https://github.com/Kennyslaboratory/AI-Purple-Ops/issues)

