# Agent Context (AI Purple Ops)

This repo is a security tool. Treat it like something you would ship and support.

## What Matters

- Do not change public contracts casually:
  - CLI flags/commands, exit codes, help output
  - recipe schema and validation behavior
  - output directory semantics and evidence pack layout
  - gate/judge semantics
- Prefer evidence over assumptions. If you cannot prove a claim from code or a command output, mark it Unknown.

## Where Truth Lives

- CLI entrypoint: `cli/harness.py`
- Core library: `src/harness/`
- Suites: `suites/`
- Recipes: `recipes/`
- Policies: `policies/`
- Docs index: `docs/README.md`

## Safety Harness (Required Before Merges)

- `make test`
- `python scripts/validate_recipes.py`
- Mock trust run:
  - `AIPO_OUTPUT_DIR=out/quickstart_mock aipop run --suite adversarial --adapter mock --response-mode smart`
  - `aipop gate --generate-evidence`
