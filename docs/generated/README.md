# Generated Docs Tables

This folder contains generated markdown tables used by the repo front door (`README.md`) and docs.

## How To Generate

Run:

```bash
make docs-tables
```

This will:
- Generate `docs/generated/supported-integrations.md`
- Generate `docs/generated/technique-coverage.md`
- Update `README.md` content between the `BEGIN GENERATED` / `END GENERATED` markers

Generation is deterministic:
- Stable ordering
- No timestamps

## Data Sources

Supported integrations:
- Source of truth: `aipop adapter list` (run from the repo `.venv` if present)

Technique coverage:
- Source of truth: suite YAML under `suites/` (case metadata like `metadata.technique`)

## Definitions

Supported:
- An integration that is listed by `aipop adapter list` (built-in adapter registry).

Planned:
- Not generated in Phase 3 because there is no pinned, machine-readable roadmap artifact in-repo.
  If/when a roadmap file exists, this generator can be extended to include a “Planned” section sourced from it.

