"""Core data models for test cases and results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TestCase:
    """Single test case definition."""

    id: str
    prompt: str
    metadata: dict[str, Any]
    # TODO(b05): Add expected_policy field
    # TODO(b07): Add attack_type field for redteam


@dataclass
class RunResult:
    """Single test execution result."""

    test_id: str
    response: str
    passed: bool
    metadata: dict[str, Any]
    # TODO(b05): Add policy_violations field
    # TODO(b06): Add evidence_links field
