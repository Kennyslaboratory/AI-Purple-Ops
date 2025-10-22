"""Core data models for test cases and results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelResponse:
    """Model invocation response with metadata.

    Contains the text response plus metadata like tokens, latency, cost,
    finish_reason, etc. Prevents having to change Adapter.invoke() signature
    when adding detector/evaluator support.
    """

    text: str
    meta: dict[str, Any] = field(default_factory=dict)
    # meta can include: tokens, finish_reason, cost, latency, provider, refusal, etc.


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
