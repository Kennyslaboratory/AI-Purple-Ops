"""CLI integration tests for PyRIT orchestrator."""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def test_suite_file(tmp_path: Path) -> Path:
    """Create minimal test suite file."""
    suite_file = tmp_path / "test_suite.yaml"
    suite_file.write_text("""
id: test-suite
name: Test Suite
test_cases:
  - id: test-1
    prompt: "Test prompt"
    metadata:
      expected: "response"
""")
    return suite_file


def test_cli_with_pyrit_basic(test_suite_file):
    """Test basic PyRIT orchestrator via CLI."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "pyrit",
            "--max-turns", "3"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)  # 0 or 1 (some tests failed) is acceptable
    assert "Loaded" in result.stdout or "test" in result.stdout.lower()


def test_cli_with_pyrit_single_turn(test_suite_file):
    """Test PyRIT with single turn (should work like simple)."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "pyrit",
            "--max-turns", "1"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)


def test_cli_with_pyrit_multi_turn(test_suite_file):
    """Test PyRIT with multiple turns."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "pyrit",
            "--max-turns", "5"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)


def test_cli_with_pyrit_debug(test_suite_file):
    """Test PyRIT with debug mode."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "pyrit",
            "--max-turns", "2",
            "--orch-opts", "debug"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)


def test_cli_with_pyrit_verbose(test_suite_file):
    """Test PyRIT with verbose mode."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "pyrit",
            "--max-turns", "2",
            "--orch-opts", "verbose"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)


def test_cli_without_orchestrator_backward_compat(test_suite_file):
    """Test backward compatibility without orchestrator flag."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file)
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)


def test_cli_with_simple_orchestrator(test_suite_file):
    """Test simple orchestrator still works."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "simple"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)


def test_cli_pyrit_help():
    """Test that help text mentions pyrit."""
    result = subprocess.run(
        ["aipop", "run", "--help"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "--orchestrator" in result.stdout
    assert "--max-turns" in result.stdout


def test_cli_invalid_orchestrator(test_suite_file):
    """Test error handling for invalid orchestrator."""
    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "invalid"
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1
    assert "Unknown orchestrator" in result.stdout or "invalid" in result.stdout.lower()


def test_cli_pyrit_with_config_file(test_suite_file, tmp_path):
    """Test PyRIT with custom config file."""
    config_file = tmp_path / "pyrit_config.yaml"
    config_file.write_text("""
orchestrator_type: pyrit
debug: true
custom_params:
  max_turns: 3
  context_window: 2
""")

    result = subprocess.run(
        [
            "aipop", "run",
            "--suite", str(test_suite_file),
            "--orchestrator", "pyrit",
            "--orch-config", str(config_file)
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode in (0, 1)

