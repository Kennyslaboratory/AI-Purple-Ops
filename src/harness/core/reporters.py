"""Reporter protocol for metrics and logging."""

from __future__ import annotations

from typing import Protocol

from .models import RunResult


class Reporter(Protocol):
    """Metrics and logging (telemetry backend analogy)."""

    def write_summary(self, results: list[RunResult], path: str) -> None:
        """Write test results to a summary file."""
        ...

    # TODO(b04): JSON reporter implementation
    # TODO(b04): JUnit XML reporter implementation
    # TODO(b09): Add CI/CD status check integration
