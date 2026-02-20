# Architecture (Repo-Level Map)

This document is a repo-level map: what each top-level directory is for, and the expected import boundaries.

For deeper architecture docs, see:
- `docs/architecture/pipeline.md`
- `docs/architecture/VALUES.md`
- `docs/architecture/UI_HOOKS.md`

## Directory Ownership (Import Boundaries)

These boundaries are a contributor contract intended to prevent cyclic dependencies and "everything imports everything".
They are not yet fully enforced by tooling.

| Directory | Owner | Purpose | May import | Must not import |
| --- | --- | --- | --- | --- |
| `src/harness/` | Harness core | Runtime engine: loaders, adapters, judges, gates, evidence, storage | Stdlib + third-party deps, internal `src/harness/*` | `cli/`, `scripts/`, `tests/` |
| `cli/` | CLI surface | CLI entrypoints that call into `src/harness/` | `src/harness/` | `tests/` |
| `scripts/` | Maintainers | Developer/CI utilities (docs generation, ratchets, validators) | `src/harness/`, `cli/` (when needed) | N/A |
| `recipes/`, `suites/`, `registry/` | Operators + maintainers | Data: recipe definitions, suite definitions, registries used by the runtime | N/A | N/A |
| `adapters/` | Operators + maintainers | Runtime adapter YAML specs and non-code integration scaffolding (not Python adapter code) | N/A | N/A |
| `docs/` | Maintainers | Human documentation and contracts | N/A | N/A |
| `tests/` | Maintainers | Test harness and contract tests | `src/harness/`, `cli/`, `scripts/` | N/A |
