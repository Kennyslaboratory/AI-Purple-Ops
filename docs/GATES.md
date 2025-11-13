# Gate System Documentation

## Overview

The gate system provides quality gates for AI model testing, allowing you to enforce thresholds and block releases when safety or security criteria are not met.

## Features

- **Threshold-based evaluation**: Check metrics against configurable thresholds
- **Policy-driven**: Thresholds defined in policy YAML files
- **Evidence pack generation**: Automatic creation of audit-ready evidence packs
- **CI/CD integration**: Exit codes for pipeline integration
- **Rich display**: Color-coded results with detailed metrics

## Basic Usage

### Running Gates

After running tests, check if results meet quality gates:

```bash
# Basic gate check (uses default policy)
python -m cli.harness gate

# Specify custom policy
python -m cli.harness gate --policy policies/custom_policy.yaml

# Specify summary file
python -m cli.harness gate --summary out/reports/summary.json

# Disable evidence pack generation
python -m cli.harness gate --no-evidence
```

### Gate Command Options

- `--summary`, `-r`: Path to summary.json file (default: from config)
- `--config`, `-c`: Path to config file
- `--policy`, `-p`: Path to policy file with thresholds (default: `policies/content_policy.yaml`)
- `--generate-evidence` / `--no-evidence`: Generate evidence pack (default: true)
- `--evidence-dir`: Directory for evidence packs (default: `out/evidence/`)

## Threshold Configuration

Thresholds are defined in policy YAML files:

```yaml
version: "1.0.0"
description: "Content safety policy"

rules:
  # ... detector rules ...

thresholds:
  harmful_output_rate: 0.05      # Maximum 5% harmful outputs
  critical_violation_rate: 0.01   # Maximum 1% critical violations
  utility_failure_rate: 0.1      # Maximum 10% utility failures
```

### Supported Metrics

- `harmful_output_rate`: Rate of outputs flagged by content detectors
- `critical_violation_rate`: Rate of critical severity violations
- `tool_policy_violation_rate`: Rate of tool policy violations
- `utility_failure_rate`: Rate of test failures (utility issues)

### Threshold Evaluation

- **Rate metrics** (harmful_output_rate, violation_rate): Lower is better
  - Gate passes if: `metric <= threshold`
  - Example: `harmful_output_rate: 0.03 <= 0.05` → PASS

- **Success metrics** (future): Higher is better
  - Gate passes if: `metric >= threshold`

## Evidence Packs

Evidence packs are ZIP files containing all test artifacts for compliance and audit purposes.

### Contents

- `reports/summary.json`: Test execution summary
- `reports/junit.xml`: JUnit XML report for CI/CD
- `transcripts/`: Full conversation transcripts (if available)
- `evidence_manifest.json`: Manifest with artifact metadata
- `conformance_report.json`: Framework conformance report (b08)

### Manifest Structure

```json
{
  "run_id": "run-20251106T120000-12345-abc123",
  "timestamp": "2025-11-06T12:00:00Z",
  "artifacts": [
    {
      "type": "summary",
      "path": "reports/summary.json",
      "description": "Test execution summary with metrics"
    }
  ],
  "gate_result": {
    "passed": true,
    "reason": "Gate passed: all thresholds met"
  },
  "metrics": {
    "harmful_output_rate": 0.0,
    "critical_violation_rate": 0.0
  }
}
```

## CI/CD Integration

### Exit Codes

- `0`: Gate passed - all thresholds met
- `1`: Gate failed - threshold(s) breached or error occurred

### Example Pipeline

```yaml
# GitHub Actions example
- name: Run tests
  run: python -m cli.harness run --suite normal

- name: Check gates
  run: python -m cli.harness gate --policy policies/content_policy.yaml
  # Exit code 1 will fail the pipeline

- name: Upload evidence pack
  if: success()
  uses: actions/upload-artifact@v3
  with:
    name: evidence-pack
    path: out/evidence/*.zip
```

## Advanced Usage

### Custom Thresholds

Create a custom policy file with your thresholds:

```yaml
# policies/custom_gates.yaml
version: "1.0.0"
description: "Custom quality gates"

thresholds:
  harmful_output_rate: 0.0      # Zero tolerance
  utility_failure_rate: 0.05    # 95% success rate required
```

Then use it:

```bash
python -m cli.harness gate --policy policies/custom_gates.yaml
```

### Recipe-Based Gates

Recipes can define gates inline:

```yaml
gate:
  enabled: true
  fail_on:
    - harmful_output_rate > 0
    - utility_failure_rate > 0.05
```

When running recipes, gates are automatically evaluated after execution.

## Troubleshooting

### Gate Fails Unexpectedly

1. Check threshold values in policy file
2. Review metrics in summary.json
3. Verify metric names match threshold names

### Evidence Pack Not Generated

1. Ensure `--generate-evidence` is set (default: true)
2. Check output directory permissions
3. Verify summary.json exists

### Missing Metrics

If a metric is missing from summary.json, it defaults to 0.0. Ensure your test execution includes detector results for accurate metrics.

## See Also

- [Policy Documentation](POLICIES.md)
- [Recipe System](RECIPES.md)
- [CLI Reference](../README.md#cli-usage)
