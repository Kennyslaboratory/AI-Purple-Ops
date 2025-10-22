#!/usr/bin/env python3
"""
Validate all recipes/**/*.yaml against reports/schemas/recipe.schema.json.
Exits nonzero with a readable error list on failure.
"""

from __future__ import annotations

import json
import pathlib
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except Exception as e:
    print(f"Missing dev deps: {e}", file=sys.stderr)
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "reports" / "schemas" / "recipe.schema.json"
RECIPES_GLOB = ROOT.glob("recipes/**/*.yaml")


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"Schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 2
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    failures: list[tuple[pathlib.Path, str]] = []
    found = False
    for p in sorted(RECIPES_GLOB):
        found = True
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            if errors:
                for e in errors:
                    loc = "/".join([str(x) for x in e.path]) or "<root>"
                    failures.append((p, f"{loc}: {e.message}"))
        except Exception as e:
            failures.append((p, f"YAML parse error: {e}"))
    if not found:
        print("No recipes found under recipes/**/*.yaml", file=sys.stderr)
        return 1
    if failures:
        print("Recipe validation failed:")
        for fp, msg in failures:
            print(f"- {fp}: {msg}")
        return 1
    print("All recipes valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
