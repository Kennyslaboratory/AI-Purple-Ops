# Environment Variables

AI Purple Ops supports configuration via environment variables with the `AIPO_` prefix. These variables provide a convenient way to configure the tool without modifying config files, especially useful for CI/CD pipelines and different environments.

## Precedence

Configuration values are resolved in the following order (highest to lowest priority):

1. **CLI flags** (e.g., `--output-dir`, `--log-level`)
2. **Environment variables** (e.g., `AIPO_OUTPUT_DIR`, `AIPO_LOG_LEVEL`)
3. **Config file** (`configs/harness.yaml`)
4. **Defaults** (hardcoded in the application)

## Available Variables

### `AIPO_OUTPUT_DIR`

Base output directory for all artifacts.

**Default**: `out`

**Example**:
```bash
export AIPO_OUTPUT_DIR=/tmp/aipop-results
aipopp run --suite normal
# Results will be in /tmp/aipop-results/reports/
```

**Cascade Behavior**: When `AIPO_OUTPUT_DIR` is set, `reports_dir` and `transcripts_dir` automatically default to `{AIPO_OUTPUT_DIR}/reports` and `{AIPO_OUTPUT_DIR}/transcripts` unless explicitly overridden.

### `AIPO_REPORTS_DIR`

Directory for report files (summary.json, junit.xml).

**Default**: `out/reports`

**Example**:
```bash
export AIPO_REPORTS_DIR=/custom/reports
aipop run --suite normal
# Reports will be in /custom/reports/
```

**Note**: If `AIPO_OUTPUT_DIR` is set and `AIPO_REPORTS_DIR` is not, `AIPO_REPORTS_DIR` will default to `{AIPO_OUTPUT_DIR}/reports`.

### `AIPO_TRANSCRIPTS_DIR`

Directory for conversation transcript files.

**Default**: `out/transcripts`

**Example**:
```bash
export AIPO_TRANSCRIPTS_DIR=/custom/transcripts
aipop run --suite normal
# Transcripts will be in /custom/transcripts/
```

**Note**: If `AIPO_OUTPUT_DIR` is set and `AIPO_TRANSCRIPTS_DIR` is not, `AIPO_TRANSCRIPTS_DIR` will default to `{AIPO_OUTPUT_DIR}/transcripts`.

### `AIPO_LOG_LEVEL`

Logging verbosity level.

**Default**: `INFO`

**Valid values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`

**Example**:
```bash
export AIPO_LOG_LEVEL=DEBUG
aipop run --suite normal
# Will show detailed debug logs
```

### `AIPO_SEED`

Random seed for reproducible test execution.

**Default**: `42`

**Example**:
```bash
export AIPO_SEED=12345
aipop run --suite normal
# Tests will use seed 12345 for reproducibility
```

## Adapter-Specific Variables

These variables are used by specific adapters and are not prefixed with `AIPO_`:

### OpenAI Adapter

- **`OPENAI_API_KEY`**: OpenAI API key (required for `openai` adapter)

**Example**:
```bash
export OPENAI_API_KEY=sk-...
aipop recipe run security/prompt_injection_baseline --adapter openai
```

### Anthropic Adapter

- **`ANTHROPIC_API_KEY`**: Anthropic API key (required for `anthropic` adapter)

**Example**:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
aipop recipe run safety/content_policy_baseline --adapter anthropic
```

### AWS Bedrock Adapter

- **`AWS_REGION`**: AWS region (default: `us-east-1`)
- **`AWS_ACCESS_KEY_ID`**: AWS access key ID
- **`AWS_SECRET_ACCESS_KEY`**: AWS secret access key

**Example**:
```bash
export AWS_REGION=us-west-2
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
aipop recipe run security/prompt_injection_baseline --adapter bedrock
```

## Common Scenarios

### CI/CD Pipeline

```bash
# Set output directory for CI artifacts
export AIPO_OUTPUT_DIR=${CI_PROJECT_DIR}/artifacts
export AIPO_LOG_LEVEL=INFO

# Run tests
aipop run --suite normal --quiet

# Check gates
aipop gate --skip-policy-prompt
```

### Development with Custom Paths

```bash
# Use custom directories
export AIPO_OUTPUT_DIR=~/aipop-dev
export AIPO_LOG_LEVEL=DEBUG
export AIPO_SEED=42

# Run tests
aipop run --suite normal
```

### Testing Without API Keys

```bash
# No API keys needed - use mock adapter
aipop run --suite normal --adapter mock
# or
aipop recipe run security/prompt_injection_baseline --mock
```

### Multiple Environments

Create environment-specific files:

**`.env.development`**:
```bash
AIPO_OUTPUT_DIR=out/dev
AIPO_LOG_LEVEL=DEBUG
AIPO_SEED=42
```

**`.env.production`**:
```bash
AIPO_OUTPUT_DIR=/var/aipop/prod
AIPO_LOG_LEVEL=INFO
AIPO_SEED=12345
```

Load with:
```bash
source .env.development
aipop run --suite normal
```

## Security Considerations

- **Never commit API keys** to version control
- Use secrets management in CI/CD (GitHub Secrets, GitLab CI Variables, etc.)
- Environment variables are sanitized and validated for security
- Paths are validated to prevent directory traversal attacks

## Validation

All environment variables are validated:

- **Paths**: Must be within allowed directories (current directory or `/tmp`)
- **Log Level**: Must be one of: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- **Seed**: Must be a valid integer

Invalid values will cause the CLI to exit with an error message.

## Checking Current Configuration

View current configuration including environment variable sources:

```bash
aipop config show
```

This displays all settings with their source (env var, config file, or default).

## Troubleshooting

### Environment Variable Not Taking Effect

1. Check variable name spelling (must be uppercase with `AIPO_` prefix)
2. Verify variable is exported: `echo $AIPO_OUTPUT_DIR`
3. Check precedence: CLI flags override env vars
4. Use `aipop config show` to see actual values being used

### Path Issues

If you get path validation errors:

- Ensure paths are relative to current directory or absolute paths in `/tmp`
- Check that paths don't contain `..` or other traversal attempts
- Use `aipop config show` to verify resolved paths

### Adapter Not Available

Check adapter requirements:

```bash
aipop list adapters
```

This shows which adapters are available and what environment variables they need.
