"""Runner protocol for test execution logic."""

from __future__ import annotations

from typing import Protocol

from .models import RunResult, TestCase


class Runner(Protocol):
    """Execution logic (CI/CD controller analogy)."""

    def execute(self, test_case: TestCase) -> RunResult:
        """Execute a single test case and return result."""
        ...

    # TODO(b05): Add policy oracle integration
    # TODO(b06): Add gate threshold checks
