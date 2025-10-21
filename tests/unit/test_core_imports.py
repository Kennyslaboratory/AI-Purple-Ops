"""Smoke test for core interface imports."""

from __future__ import annotations


def test_core_imports() -> None:
    """Verify all core interfaces are importable."""
    from harness.core import Adapter, Reporter, Runner, RunResult, TestCase

    assert all([Adapter, Reporter, RunResult, Runner, TestCase])
