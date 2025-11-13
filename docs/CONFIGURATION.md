# Configuration Precedence

AI Purple Ops uses the following precedence (highest to lowest):

1. Command-line flags (e.g., `--output-dir`)
2. Environment variables (e.g., `AIPO_OUTPUT_DIR`)
3. Configuration file (`configs/harness.yaml`)
4. Built-in defaults

## Examples

### CLI flag overrides all

```bash
aipop run --output-dir custom_out
```

The `--output-dir` flag overrides any environment variable or config file value.

### Environment variable overrides config file

```bash
export AIPO_OUTPUT_DIR=env_out
aipop run
```

The environment variable `AIPO_OUTPUT_DIR` overrides the value in `configs/harness.yaml`.

### Config file value used if no override

```bash
aipop run
```

Uses the value from `configs/harness.yaml` if no CLI flag or environment variable is set.

## Environment Variables

The following environment variables can override configuration:

- `AIPO_OUTPUT_DIR` - Override `run.output_dir`
- `AIPO_REPORTS_DIR` - Override `run.reports_dir`
- `AIPO_TRANSCRIPTS_DIR` - Override `run.transcripts_dir`
- `AIPO_LOG_LEVEL` - Override `run.log_level`
- `AIPO_SEED` - Override `run.seed`

## Configuration File

Default configuration file: `configs/harness.yaml`

Example configuration:

```yaml
run:
  output_dir: out
  reports_dir: out/reports
  transcripts_dir: out/transcripts
  log_level: INFO
  seed: 42
```

## Validation

Validate your configuration:

```bash
aipop config validate
```

This checks:
- Configuration file syntax
- Path existence
- Directory permissions

## Viewing Current Configuration

See what configuration is actually being used:

```bash
aipop config show
```

This displays:
- Current values for all settings
- Source of each value (CLI flag, env var, config file, or default)
