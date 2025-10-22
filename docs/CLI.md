# CLI Quick Usage

## Running the CLI

The AI Purple Ops CLI is invoked using Python's module execution syntax.

### Help

Display all available commands and options:

```bash
python -m cli.harness --help
```

### Version

Display the current version:

```bash
python -m cli.harness version
```

### Run

Execute a test suite (default: dry-run mode):

```bash
python -m cli.harness run --suite normal --dry-run
```

Run without dry-run:

```bash
python -m cli.harness run --suite normal --no-dry-run
```

### Gate

Check gate status (verifies smoke artifact exists):

```bash
python -m cli.harness gate
```

Check specific summary file:

```bash
python -m cli.harness gate --summary path/to/summary.json
```

## Configuration Overrides

Override configuration values at runtime:

```bash
python -m cli.harness run \
  --config configs/harness.yaml \
  --output-dir tmp/out \
  --log-level DEBUG \
  --seed 42
```

Available overrides:
- `--config` / `-c`: Path to configuration file
- `--output-dir`: Override `run.output_dir`
- `--reports-dir`: Override `run.reports_dir`
- `--transcripts-dir`: Override `run.transcripts_dir`
- `--log-level`: Override `run.log_level`
- `--seed`: Override `run.seed`

## Command Details

### run

**Purpose**: Execute test suite and generate artifacts.

**Options**:
- `--suite` / `-s`: Suite name (default: normal)
- `--config` / `-c`: Path to config file
- `--dry-run` / `--no-dry-run`: Dry-run mode (default: enabled)
- Configuration overrides (see above)

**Output**: Creates `cli_run_smoke.json` in reports directory.

### gate

**Purpose**: Verify test results meet criteria.

**Options**:
- `--summary` / `-r`: Path to summary JSON
- `--config` / `-c`: Path to config file

**Note**: Full gating logic arrives in b06. Current implementation verifies artifact existence only.

### version

**Purpose**: Display version information.

**Output**: Prints version from `harness.__version__`.

## Examples

Basic workflow:

```bash
# Check version
python -m cli.harness version

# Run smoke test
python -m cli.harness run --suite normal --dry-run

# Verify gate
python -m cli.harness gate
```

Custom configuration:

```bash
# Run with custom config and overrides
python -m cli.harness run \
  --config configs/custom.yaml \
  --output-dir /tmp/results \
  --log-level DEBUG \
  --seed 123 \
  --dry-run
```

## Exit Codes

- `0`: Success
- `1`: Error (harness error or unhandled exception)

## Notes

- Commands use structured console output via `ConsoleLogger`
- All commands run preflight checks before execution
- Dry-run mode is enabled by default for safety
- Real runner implementation arrives in b04
- Full gating thresholds arrive in b06
