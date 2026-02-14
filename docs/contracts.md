# Contracts (What Must Not Break)

This document defines the stable contracts of AI Purple Ops. Migration work must preserve these behaviors.

If a behavior is not documented here or in an existing spec, treat it as **unstable** and do not rely on it.

## Stability Levels

- Stable: Breaking changes require an explicit migration plan and compatibility period.
- Stable with notice: Additive changes are allowed, but breaking changes require advance notice and compatibility.
- Experimental: May change without notice; do not build automation that depends on it.

## CLI Contract

Stability: Stable

Scope:
- command names and flags
- default behaviors
- exit code meaning
- help output remains meaningful

Primary references:
- `docs/CLI.md`
- `cli/harness.py`

## Recipe Contract

Stability: Stable

Scope:
- recipe schema structure and required fields
- loader behavior and validation behavior
- recipe discovery via `aipop recipe list`

Primary references:
- `docs/RECIPES.md`
- packaged schema artifact: `src/harness/schemas/recipe.schema.json`
- validation entrypoint: `scripts/validate_recipes.py`

## Output And Evidence Contract

Stability: Stable with notice

Scope:
- default output directory semantics
- evidence pack layout
- where reports/transcripts land

Primary references:
- `docs/CONFIGURATION.md`
- `docs/ENVIRONMENT_VARIABLES.md` (output dir overrides)
- `docs/EVIDENCE_PACK_SPEC.md`

## Gate And Judge Semantics

Stability: Stable

Scope:
- gate thresholds, pass/fail rules, and report shape
- judge score parsing and aggregation semantics

Primary references:
- `docs/GATES.md`
- `src/harness/intelligence/judge_models.py`

## Verified Quickstart Commands (No Keys)

Stability: Stable with notice

These commands are verified in the stabilization/migration workflow and should keep working:

```bash
AIPO_OUTPUT_DIR=out/quickstart_mock .venv/bin/aipop run --suite adversarial --adapter mock --response-mode smart
AIPO_OUTPUT_DIR=out/quickstart_mock .venv/bin/aipop gate --generate-evidence
```
