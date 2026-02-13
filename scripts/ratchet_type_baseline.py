#!/usr/bin/env python3
"""
Type-checking ratchet for messy repos.

Goal: prevent mypy debt from increasing without fixing the entire backlog today.

Behavior:
- Run `mypy src` at the base ref in a temporary git worktree.
- Run `mypy src` at head in the current worktree.
- Fail only if the total mypy error count increased.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


MYPY_COUNT_RE = re.compile(r"^Found\s+(\d+)\s+errors?\b", re.MULTILINE)


def _run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def _default_base_ref() -> str:
    # Prefer origin/main if it exists; fall back to main.
    try:
        _run(["git", "show-ref", "--verify", "--quiet", "refs/remotes/origin/main"], check=True)
        return "origin/main"
    except Exception:
        return "main"


def _mypy_bin() -> str:
    # Prefer the venv tool if present; fall back to PATH.
    candidate = Path(sys.executable).with_name("mypy")
    return str(candidate if candidate.exists() else "mypy")


def _mypy_error_count(output: str, *, returncode: int) -> int:
    m = MYPY_COUNT_RE.search(output)
    if m:
        return int(m.group(1))
    if returncode == 0:
        return 0
    # Unknown mypy output shape; treat as failure and surface output.
    raise ValueError("could not parse mypy error count")


def _mypy_src_errors(repo_dir: Path) -> tuple[int, str]:
    mypy = _mypy_bin()
    print(f"ratchet(type): running mypy in {repo_dir} ...", flush=True)
    cp = _run([mypy, "src"], cwd=repo_dir, check=False)
    count = _mypy_error_count(cp.stdout, returncode=cp.returncode)
    return count, cp.stdout


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.getenv("RATCHET_BASE", "") or _default_base_ref())
    ap.add_argument("--head", default=os.getenv("RATCHET_HEAD", "") or "HEAD")
    args = ap.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]

    with tempfile.TemporaryDirectory(prefix="aipop-mypy-base-") as td:
        base_dir = Path(td)
        print(f"ratchet(type): creating base worktree at {base_dir} ...", flush=True)
        add = _run(["git", "worktree", "add", "--detach", str(base_dir), args.base], cwd=repo_root)
        if add.returncode != 0:
            sys.stderr.write(add.stdout)
            return 2

        try:
            base_count, base_out = _mypy_src_errors(base_dir)
            head_count, head_out = _mypy_src_errors(repo_root)

            print(f"ratchet(type): base_errors={base_count} head_errors={head_count}")

            if head_count > base_count:
                print("ratchet(type): FAIL (mypy error count increased vs base)")
                # Keep output short but actionable in CI logs.
                print("--- base mypy tail ---")
                print("\n".join(base_out.strip().splitlines()[-40:]))
                print("--- head mypy tail ---")
                print("\n".join(head_out.strip().splitlines()[-40:]))
                return 1

            print("ratchet(type): OK (no increases vs base)")
            return 0
        finally:
            # Ensure worktree is removed even if mypy fails.
            _run(["git", "worktree", "remove", "--force", str(base_dir)], cwd=repo_root)
            # If remove fails for any reason, still try cleaning the directory.
            if base_dir.exists():
                shutil.rmtree(base_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
