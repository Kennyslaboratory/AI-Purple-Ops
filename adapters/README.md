# `adapters/` (Templates, Not Python Code)

This top-level directory is for **adapter templates and metadata** used to help operators and contributors configure integrations.

It is **not** where the Python adapter implementations live.

## Source Of Truth For Adapter Code

Python adapter implementations live under:
- `src/harness/adapters/`

Docs:
- `docs/ADAPTERS.md`

## What Lives Here

- `adapters/templates/`: starter YAML templates (for example `adapters/templates/mcp.yaml`) you can copy/adapt for your environment.
- `adapters/platform/`: platform-specific scaffolding (not a Python runtime package).
