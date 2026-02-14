#!/usr/bin/env python3
"""
Validate all recipes/**/*.yaml against reports/schemas/recipe.schema.json.
Exits nonzero with a readable error list on failure.
"""

from __future__ import annotations

import pathlib
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except Exception as exc:
    print(f"Missing dev deps: {exc}", file=sys.stderr)
    sys.exit(2)

try:
    from harness.utils.schema_resolver import load_json_schema
except Exception as exc:
    print(f"Failed to import schema resolver: {exc}", file=sys.stderr)
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECIPES_GLOB = ROOT.glob("recipes/**/*.yaml")


def main() -> int:
    try:
        loaded = load_json_schema("recipe.schema.json")
        schema = loaded.schema
    except Exception as e:
        print(f"Schema not found or failed to load: {e}", file=sys.stderr)
        return 2
    validator = Draft202012Validator(schema)
    failures: list[tuple[pathlib.Path, str]] = []
    found = False
    for p in sorted(RECIPES_GLOB):
        found = True
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            if errors:
                for err in errors:
                    loc = "/".join([str(x) for x in err.path]) or "<root>"
                    failures.append((p, f"{loc}: {err.message}"))
        except Exception as exc:
            failures.append((p, f"YAML parse error: {exc}"))
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
