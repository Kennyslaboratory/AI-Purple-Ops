# AI Purple Ops

AI Purple Ops is a CLI-first harness for running LLM security test suites, recipes, and quality gates, and packaging evidence for review.

## Why It Exists

Security teams end up stitching together academic repos, vendor dashboards, and one-off scripts. The result is hard to reproduce, hard to audit, and painful to operate.

AI Purple Ops focuses on an operator workflow: run suites, score outcomes, and generate evidence artifacts with predictable paths.

## 60-Second Quickstart (Mock, No Keys)

This is a no-keys smoke path using the built-in `mock` adapter. The goal is to prove the tool runs end-to-end and produces outputs and an evidence pack.

Prerequisite: create the repo virtualenv and install dependencies (see `docs/SETUP.md`).

```bash
AIPO_OUTPUT_DIR=out/quickstart_mock .venv/bin/aipop run --suite adversarial --adapter mock --response-mode smart
AIPO_OUTPUT_DIR=out/quickstart_mock .venv/bin/aipop gate --generate-evidence
```

## Where Outputs Go

With the quickstart commands above:
- Output directory: `out/quickstart_mock/`
- Evidence packs: `out/quickstart_mock/evidence/*.zip`
- Reports: `out/reports/` (for example `summary.json`, `junit.xml`)
- Transcripts: `out/transcripts/`

To control paths, see output-related env vars in `docs/ENVIRONMENT_VARIABLES.md` and configuration precedence in `docs/CONFIGURATION.md`.

## How It Works

High-level:
- `aipop run` executes a YAML suite from `suites/` using an adapter, producing reports/transcripts under `out/`.
- `aipop gate` evaluates results against policy thresholds and can generate an evidence ZIP (see `docs/EVIDENCE_PACK_SPEC.md`).
- `aipop recipe` provides a recipe workflow wrapper around suites/policies (see `docs/RECIPES.md`).

Start at `docs/README.md` for the doc map.

## Supported Integrations (Generated)

<!-- BEGIN GENERATED: supported-integrations -->
<!-- END GENERATED: supported-integrations -->

## Technique Coverage (Generated)

<!-- BEGIN GENERATED: technique-coverage -->
<!-- END GENERATED: technique-coverage -->

## Docs And Contracts

- Docs index: `docs/README.md`
- Contracts (what must not break): `docs/contracts.md`

## Contributing

See `CONTRIBUTING.md`.

