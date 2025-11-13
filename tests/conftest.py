"""Global pytest fixtures for all tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_policy_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for policy files."""
    policy_dir = tmp_path / "policies"
    policy_dir.mkdir(parents=True)
    return policy_dir
