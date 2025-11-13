#!/usr/bin/env bash
set -euo pipefail
name="${1:-}"
if [[ -z "$name" ]]; then
  echo "Usage: scripts/new-adapter.sh <adapter_name>" >&2
  exit 2
fi
pkg="src/harness/adapters"
testpkg="tests/adapters"
file="$pkg/${name}.py"
testfile="$testpkg/test_${name}.py"
mkdir -p "$pkg" "$testpkg"
if [[ -e "$file" ]]; then
  echo "Refusing to overwrite existing $file" >&2
  exit 1
fi
cat > "$file" <<PY
from __future__ import annotations
from typing import Protocol, Any

class ModelAdapter(Protocol):
    def infer(self, prompt: str, **kwargs: Any) -> str: ...

class ${name^}Adapter:
    def __init__(self, **kwargs: Any) -> None:
        self._cfg = dict(kwargs)

    def infer(self, prompt: str, **kwargs: Any) -> str:
        # TODO: implement real call. This is a stub.
        return f"[${name} reply] " + prompt
PY
cat > "$testfile" <<PY
from ${pkg//\//.}.${name} import ${name^}Adapter

def test_${name}_adapter_basic():
    a = ${name^}Adapter()
    out = a.infer("ping")
    assert "ping" in out
PY
echo "Created $file and $testfile"
