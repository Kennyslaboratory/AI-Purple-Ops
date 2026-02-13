# Agent Rules (Non-Negotiable)

These rules exist to prevent credibility work from turning into breaking refactors.

## Contracts To Keep Stable

- CLI contract: command names, flags/defaults, exit codes, and meaningful help.
- Recipe contract: schema structure, loader behavior, validation behavior.
- Output/evidence contract: default output directory semantics, evidence pack layout.
- Gates/judges: threshold semantics, score parsing, ensemble aggregation.

## Change Discipline

- One theme per PR chunk.
- Keep diffs small. Split if large.
- Do not add dependencies unless explicitly approved.
- Do not run pre-commit in automation flows unless explicitly requested.
- If a doc claim cannot be proven by code or a reproducible command, remove it or label it Planned/Unknown.

## Proof Requirements

After each PR chunk, rerun:
- `make test`
- `python scripts/validate_recipes.py`
- `AIPO_OUTPUT_DIR=out/quickstart_mock aipop run --suite adversarial --adapter mock --response-mode smart`
- `aipop gate --generate-evidence`
