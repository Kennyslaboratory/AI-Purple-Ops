"""Integration tests for CLI discovery commands (list, config show)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def test_list_suites_command(project_root):
    """Test that 'list suites' command works and shows available suites."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "list", "suites"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    # Should exit successfully
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Should show suite information
    assert "Available Test Suites" in result.stdout or "normal" in result.stdout.lower()


def test_list_invalid_resource(project_root):
    """Test that 'list' with invalid resource fails gracefully."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "list", "invalid_resource"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    # Should fail
    assert result.returncode == 1

    # Should show helpful error
    assert "Unknown resource type" in result.stdout or "Unknown resource type" in result.stderr


def test_config_show_command(project_root):
    """Test that 'config show' command works and displays configuration."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "config", "show"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    # Should exit successfully
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Should show config information
    output = result.stdout.lower()
    assert any(keyword in output for keyword in ["configuration", "config", "output_dir", "seed"])


def test_config_invalid_action(project_root):
    """Test that 'config' with invalid action fails gracefully."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "config", "invalid_action"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    # Should fail
    assert result.returncode == 1

    # Should show helpful error
    assert "Unknown action" in result.stdout or "Unknown action" in result.stderr


def test_config_show_with_custom_config(project_root, tmp_path):
    """Test config show with custom config file."""
    # Create a custom config
    custom_config = tmp_path / "custom_harness.yaml"
    custom_config.write_text(
        """
run:
  output_dir: custom_out
  reports_dir: custom_out/reports
  log_level: DEBUG
  seed: 999
"""
    )

    result = subprocess.run(
        ["python", "-m", "cli.harness", "config", "show", "--config", str(custom_config)],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    # Should exit successfully
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Should show custom config values
    assert "999" in result.stdout or "DEBUG" in result.stdout


def test_config_show_with_env_vars(project_root):
    """Test that config show displays environment variable overrides."""
    # Set environment variable
    env = os.environ.copy()
    env["AIPO_SEED"] = "12345"

    result = subprocess.run(
        ["python", "-m", "cli.harness", "config", "show"],
        cwd=project_root,
        capture_output=True,
        text=True,
        env=env,
    )

    # Should exit successfully
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Should show the env var value or mention env vars
    assert "12345" in result.stdout or "AIPO_" in result.stdout
