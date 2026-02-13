# Agent Task Patterns

## Writing Docs Without Overclaiming

- Link to code paths or command outputs for any statement about capability.
- If something depends on API keys/network access, say so and show the failure mode.
- Prefer short docs that point to a single authoritative spec over duplicating content.

## Inventory-First Changes

When improving credibility:
- Index first (make navigation easy).
- Generate tables from code (prevent drift).
- Only then migrate directories behind compatibility shims.

## Minimal Verification Checklist

For any repo change that could affect operators:
- `make test`
- `python scripts/validate_recipes.py`
- Mock run:
  - `AIPO_OUTPUT_DIR=out/quickstart_mock aipop run --suite adversarial --adapter mock --response-mode smart`
  - `aipop gate --generate-evidence`
