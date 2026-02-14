# Migration Status

This file tracks the ongoing "credibility upgrade" migration work and the contracts that must not break while it runs.

## Contracts That Must Not Break

Source of truth: `docs/contracts.md`

In particular:
- CLI command names, flags, defaults, exit code meaning
- Recipe schema structure and validation behavior
- Output directory semantics and evidence pack layout
- Gate thresholds and judge semantics

## Phase Status (High Level)

- Phase 1: Docs become mission control (index + agent context) - Done
- Phase 2: README becomes an operator front door (proof-first) - Done
- Phase 3: Generated tables + drift guard (`make docs-check`) - Done
- Phase 4: ASR trust gap (optional, pinned benchmark artifacts) - Planned
- Phase 5: Resolve `adapters/` directory confusion safely
  - Phase 5.1: Document intent (`adapters/README.md`, repo shape clarity) - In progress
  - Phase 5.2: Optional move/rename with compatibility stub - Planned
- Phase 6: Subprocess + exception boundaries (high trust payoff) - Planned
- Phase 7: Structural refactor (migration style, strangler pattern) - Planned

