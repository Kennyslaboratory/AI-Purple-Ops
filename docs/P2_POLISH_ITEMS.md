# P2 Polish Items (From Code Review)

Non-blocking polish items to address in future branches.

## CLI Package Note

**Issue:** `cli/__main__.py` docstring says "Allow python -m cli.harness execution", but technically `__main__` enables `python -m cli`, while tests/docs use `python -m cli.harness`.

**Action:** Update comment for accuracy (both work, just clarify).

**Branch:** b04 or whenever touching CLI code

## Schema Alignment for Smoke Artifact

**Issue:** `cli_run_smoke.json` isn't meant to match `run_summary.schema.json` (by design), but adding a minimal validator would keep validation discipline strong.

**Action:** Add schema validation for CLI smoke artifacts.

**Branch:** b04 (when adding real JSON reporter)

## Per-File Ignores Consistency

**Issue:** ruff config uses `[lint.per-file-ignores]` while keeping `select/ignore` top-level. It works fine, just keep the pattern consistent.

**Action:** Review ruff.toml organization during next config change.

**Branch:** As needed

## Config Documentation (Dataclasses vs Pydantic)

**Issue:** Code uses dataclasses for config, but some docs/reports might reference Pydantic BaseModel patterns.

**Action:** Ensure all documentation consistently shows dataclass-based config examples.

**Branch:** b04 or when updating config documentation

**Status:** Already clarified in core README examples
