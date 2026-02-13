#!/usr/bin/env python3
"""
Changed-files lint ratchet for messy repos.

Goal: Prevent new Ruff violations from entering the codebase without requiring
the entire repo to be clean today.

Behavior:
- Determine changed files vs a base ref (default: origin/main if available).
- For each changed Python file, compare Ruff diagnostics count at base vs head.
- Fail only if the count increased (a ratchet), allowing legacy debt to remain.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], *, check: bool) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)


def _default_base_ref() -> str:
    # Prefer origin/main if it exists; fall back to main.
    try:
        _run(["git", "show-ref", "--verify", "--quiet", "refs/remotes/origin/main"], check=True)
        return "origin/main"
    except Exception:
        return "main"


def _changed_files(base: str, head: str) -> list[str]:
    # Use triple-dot to diff from merge-base -> head.
    cp = _run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", f"{base}...{head}"],
        check=False,
    )
    if cp.returncode != 0:
        sys.stderr.write(cp.stdout)
        raise SystemExit(f"git diff failed for base={base} head={head}")
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def _ruff_json_count_for_path(ruff_bin: str, path: str) -> int:
    cp = subprocess.run(
        [ruff_bin, "check", "-q", "--output-format", "json", path],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    # Ruff exits non-zero when it finds diagnostics. We still want the JSON list.
    out = (cp.stdout or "").strip()
    if not out:
        return 0
    idx = out.find("[")
    if idx == -1:
        raise ValueError(f"unexpected ruff output for {path}: {out[:200]}")
    data = json.loads(out[idx:])
    return len(data)


def _ruff_json_count_for_git_blob(ruff_bin: str, base: str, path: str) -> int:
    # If the file doesn't exist at base, treat as new file with 0 baseline.
    exists = (
        subprocess.run(
            ["git", "cat-file", "-e", f"{base}:{path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )
    if not exists:
        return 0

    show = subprocess.run(
        ["git", "show", f"{base}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if show.returncode != 0:
        raise RuntimeError(show.stderr.strip() or f"git show failed for {base}:{path}")

    cp = subprocess.run(
        [ruff_bin, "check", "-q", "--output-format", "json", "--stdin-filename", path, "-"],
        input=show.stdout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out = (cp.stdout or "").strip()
    if not out:
        return 0
    idx = out.find("[")
    if idx == -1:
        raise ValueError(f"unexpected ruff output for {path}@{base}: {out[:200]}")
    data = json.loads(out[idx:])
    return len(data)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.getenv("RATCHET_BASE", "") or _default_base_ref())
    ap.add_argument("--head", default=os.getenv("RATCHET_HEAD", "") or "HEAD")
    args = ap.parse_args(argv)

    files = _changed_files(args.base, args.head)
    py_files = [f for f in files if f.endswith(".py") and not f.startswith(".venv/")]

    if not py_files:
        print("ratchet(lint): no changed python files detected")
        return 0

    # Prefer the venv tool if present; fall back to PATH.
    ruff = Path(sys.executable).with_name("ruff")
    ruff_bin = str(ruff if ruff.exists() else "ruff")

    increased: list[tuple[str, int, int]] = []
    for path in py_files:
        base_count = _ruff_json_count_for_git_blob(ruff_bin, args.base, path)
        head_count = _ruff_json_count_for_path(ruff_bin, path)
        if head_count > base_count:
            increased.append((path, base_count, head_count))

    if increased:
        print("ratchet(lint): FAIL (ruff diagnostics increased vs base)")
        for path, base_count, head_count in increased:
            print(f"- {path}: base={base_count} head={head_count}")
        return 1

    print("ratchet(lint): OK (no increases vs base)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
