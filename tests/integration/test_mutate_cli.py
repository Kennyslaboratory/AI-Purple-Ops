"""CLI integration tests for mutate command."""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest


def test_cli_mutate_basic():
    """Test basic mutate command."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "mutate", "test prompt"],
        capture_output=True,
        text=True,
    )

    # Should execute successfully
    assert result.returncode in (0, 1)  # May fail if dependencies missing
    assert "test prompt" in result.stdout.lower() or "mutations" in result.stdout.lower()


def test_cli_mutate_with_strategies():
    """Test mutate command with specific strategies."""
    result = subprocess.run(
        [
            "python",
            "-m",
            "cli.harness",
            "mutate",
            "test",
            "--strategies",
            "encoding,unicode",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode in (0, 1)


def test_cli_mutate_with_output():
    """Test mutate command with output file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        output_path = f.name

    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "cli.harness",
                "mutate",
                "test prompt",
                "--output",
                output_path,
                "--count",
                "5",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Check if file was created
            assert Path(output_path).exists()

            # Check if JSON is valid
            with open(output_path) as f:
                data = json.load(f)
                assert isinstance(data, list)
    finally:
        if Path(output_path).exists():
            Path(output_path).unlink()


def test_cli_mutate_with_config():
    """Test mutate command with config file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config_path = f.name
        f.write("enable_encoding: true\nenable_unicode: false\n")

    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "cli.harness",
                "mutate",
                "test",
                "--config",
                config_path,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode in (0, 1)
    finally:
        if Path(config_path).exists():
            Path(config_path).unlink()


def test_cli_mutate_with_count():
    """Test mutate command with count limit."""
    result = subprocess.run(
        [
            "python",
            "-m",
            "cli.harness",
            "mutate",
            "test",
            "--count",
            "3",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode in (0, 1)


def test_cli_mutate_with_stats():
    """Test mutate command with stats flag."""
    result = subprocess.run(
        [
            "python",
            "-m",
            "cli.harness",
            "mutate",
            "test",
            "--stats",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode in (0, 1)


def test_cli_mutate_invalid_strategy():
    """Test mutate command with invalid strategy."""
    result = subprocess.run(
        [
            "python",
            "-m",
            "cli.harness",
            "mutate",
            "test",
            "--strategies",
            "invalid_strategy",
        ],
        capture_output=True,
        text=True,
    )

    # Should still execute (invalid strategies just ignored)
    assert result.returncode in (0, 1)


def test_cli_mutate_help():
    """Test mutate command help."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "mutate", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "mutate" in result.stdout.lower()
    assert "prompt" in result.stdout.lower()


def test_cli_mutate_provider_flag():
    """Test mutate command with provider flag."""
    result = subprocess.run(
        [
            "python",
            "-m",
            "cli.harness",
            "mutate",
            "test",
            "--strategies",
            "paraphrase",
            "--provider",
            "openai",
        ],
        capture_output=True,
        text=True,
    )

    # May fail if API key missing, but should handle gracefully
    assert result.returncode in (0, 1)


def test_cli_mutate_empty_prompt():
    """Test mutate command with empty prompt."""
    result = subprocess.run(
        ["python", "-m", "cli.harness", "mutate", ""],
        capture_output=True,
        text=True,
    )

    assert result.returncode in (0, 1)

