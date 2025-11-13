#!/usr/bin/env python3
"""Test script to verify redteam toolkit installation and functionality."""

from __future__ import annotations

import subprocess
import sys

from harness.tools.installer import (
    ToolkitConfigError,
    check_tool_available,
    load_toolkit_config,
)
from harness.utils.logging import log


def test_promptfoo() -> tuple[bool, str]:
    """Test Promptfoo installation and basic functionality."""
    try:
        # Check if promptfoo is available
        result = subprocess.run(
            ["promptfoo", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode != 0:
            return False, "promptfoo --version failed"

        # Try to run a minimal eval (just check command exists)
        # We don't actually run eval here as it requires config
        return True, f"Version: {result.stdout.strip()}"
    except FileNotFoundError:
        return False, "promptfoo not found in PATH"
    except subprocess.TimeoutExpired:
        return False, "promptfoo --version timed out"
    except Exception as e:
        return False, f"Error: {e}"


def test_garak() -> tuple[bool, str]:
    """Test Garak installation and basic functionality."""
    try:
        # Check if garak is available
        result = subprocess.run(
            ["python", "-m", "garak", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            return True, f"Version: {result.stdout.strip() or 'installed'}"

        # Try listing probes as fallback
        result = subprocess.run(
            ["python", "-m", "garak", "--list_probes"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode == 0:
            return True, "Installed (probes available)"
        return False, "garak --version and --list_probes failed"
    except FileNotFoundError:
        return False, "garak module not found"
    except subprocess.TimeoutExpired:
        return False, "garak command timed out"
    except Exception as e:
        return False, f"Error: {e}"


def test_pyrit() -> tuple[bool, str]:
    """Test PyRIT installation and basic functionality."""
    try:
        # Try importing pyrit
        import pyrit

        # Try to get version if available
        try:
            version = pyrit.__version__
            return True, f"Version: {version}"
        except AttributeError:
            return True, "Installed (import successful)"
    except ImportError:
        return False, "pyrit module not found"
    except Exception as e:
        return False, f"Error: {e}"


def test_promptinject() -> tuple[bool, str]:
    """Test PromptInject installation and basic functionality."""
    try:
        # Try importing promptinject
        import promptinject

        # Try to get version if available
        try:
            version = promptinject.__version__
            return True, f"Version: {version}"
        except AttributeError:
            return True, "Installed (import successful)"
    except ImportError:
        return False, "promptinject module not found"
    except Exception as e:
        return False, f"Error: {e}"


def main() -> int:
    """Run toolkit health checks."""
    log.info("Running redteam toolkit health checks...")

    # Load toolkit config
    try:
        config = load_toolkit_config()
        tools = config.get("tools", {})
    except ToolkitConfigError as e:
        log.error(f"Failed to load toolkit config: {e}")
        return 1

    # Test functions mapping
    test_functions = {
        "promptfoo": test_promptfoo,
        "garak": test_garak,
        "pyrit": test_pyrit,
        "promptinject": test_promptinject,
    }

    results = {}
    passed = 0
    failed = 0

    for tool_name, tool_spec in sorted(tools.items()):
        # Check if tool is available using config health check
        is_available, version = check_tool_available(tool_name, tool_spec)

        if not is_available:
            results[tool_name] = (False, "Not installed")
            failed += 1
            continue

        # Run specific test function if available
        if tool_name in test_functions:
            test_func = test_functions[tool_name]
            success, message = test_func()
            results[tool_name] = (success, message)
            if success:
                passed += 1
            else:
                failed += 1
        else:
            # Fallback to basic availability check
            results[tool_name] = (True, f"Installed ({version})")
            passed += 1

    # Print results
    log.info("")
    log.info("Toolkit Health Check Results:")
    log.info("")

    for tool_name, (success, message) in sorted(results.items()):
        if success:
            log.ok(f"✓ {tool_name}: {message}")
        else:
            log.error(f"✗ {tool_name}: {message}")

    log.info("")
    log.info(f"Summary: {passed} passed, {failed} failed")

    # Return exit code
    if failed > 0:
        log.error("Some tools failed health checks")
        return 1

    log.ok("All tools passed health checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
