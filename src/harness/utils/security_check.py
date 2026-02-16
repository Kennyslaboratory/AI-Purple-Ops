"""Security checks for adapter configs.

Detects secrets in YAML files and warns users to use environment variables.
"""

from __future__ import annotations

import re
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from harness.utils.adapter_paths import adapter_spec_globs, get_adapter_dir

console = Console()


def check_config_for_secrets(config_path: Path) -> list[str]:
    """Scan config for potential secrets (bearer tokens, API keys).
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        List of warning messages for detected secrets
    """
    if not config_path.exists():
        return []
    
    content = config_path.read_text(encoding="utf-8")
    warnings = []
    
    # Detect hardcoded OpenAI keys
    if re.search(r'["\']?sk-[A-Za-z0-9]{20,}["\']?', content):
        warnings.append("OpenAI API key detected in config")
    
    # Detect hardcoded Bearer tokens
    if re.search(r'Bearer\s+[A-Za-z0-9_\-]{20,}', content):
        warnings.append("Bearer token detected in config")
    
    # Detect JWT tokens
    if re.search(r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', content):
        warnings.append("JWT token detected in config")
    
    # Detect generic API keys (long alphanumeric strings)
    if re.search(r'["\']?[A-Za-z0-9_\-]{40,}["\']?', content):
        # Exclude likely environment variable references
        if not re.search(r'\$\{[A-Z_]+\}', content):
            # Only warn if it looks like a real key (not a placeholder)
            if not any(placeholder in content.lower() for placeholder in ["fixme", "your-", "example", "xxx"]):
                warnings.append("Long API key-like string detected in config")
    
    # Detect AWS keys
    if re.search(r'AKIA[0-9A-Z]{16}', content):
        warnings.append("AWS Access Key detected in config")
    
    # Detect private keys
    if "PRIVATE KEY" in content:
        warnings.append("Private key detected in config")
    
    return warnings


def show_security_warning(config_path: Path, warnings: list[str]) -> None:
    """Display security warning panel.
    
    Args:
        config_path: Path to config file
        warnings: List of warning messages
    """
    if not warnings:
        return
    
    warnings_list = "\n".join(f"  • {w}" for w in warnings)
    adapter_name = config_path.stem.upper().replace("-", "_")
    env_var_name = f"{adapter_name}_API_KEY"
    
    console.print()
    console.print(
        Panel.fit(
            f"[yellow]⚠️  SECURITY WARNING[/yellow]\n\n"
            f"Found potential secrets in config:\n"
            f"{warnings_list}\n\n"
            f"[bold]Best Practice:[/bold]\n"
            f"  1. Move secrets to environment variables\n"
            f"  2. Edit: [dim]{config_path}[/dim]\n"
            f"  3. Replace token with: [dim]${{{env_var_name}}}[/dim]\n"
            f"  4. Set environment variable:\n"
            f"     [dim]export {env_var_name}=your-secret-here[/dim]\n"
            f"  5. Never commit adapter configs to git\n\n"
            f"[green]✓ Added to .gitignore automatically[/green]",
            border_style="yellow",
            title="[bold]Security Alert[/bold]",
        )
    )
    console.print()


def ensure_gitignore_protection(repo_root: Path) -> None:
    """Ensure adapter configs are in .gitignore.
    
    Args:
        repo_root: Root directory of the repository
    """
    gitignore_path = repo_root / ".gitignore"
    
    adapter_dir = get_adapter_dir()
    adapter_dir_str = adapter_dir.as_posix()
    yaml_globs = adapter_spec_globs()
    patterns_to_add = [
        "# User-generated adapter configs (may contain secrets)",
        f"{adapter_dir_str}/{yaml_globs[0]}",
        f"{adapter_dir_str}/{yaml_globs[1]}",
        f"!{adapter_dir_str}/templates/",
    ]
    
    if not gitignore_path.exists():
        # Create .gitignore if it doesn't exist
        gitignore_path.write_text("\n".join(patterns_to_add) + "\n", encoding="utf-8")
        return
    
    content = gitignore_path.read_text(encoding="utf-8")
    
    # Check if patterns already exist
    if patterns_to_add[1] in content:
        return  # Already protected
    
    # Append patterns
    with gitignore_path.open("a", encoding="utf-8") as f:
        f.write("\n\n")
        f.write("\n".join(patterns_to_add))
        f.write("\n")


def check_env_var_set(env_var_name: str) -> bool:
    """Check if environment variable is set.
    
    Args:
        env_var_name: Name of environment variable
        
    Returns:
        True if set, False otherwise
    """
    import os
    
    return env_var_name in os.environ


def show_env_var_reminder(env_var_name: str) -> None:
    """Remind user to set environment variable.
    
    Args:
        env_var_name: Name of environment variable needed
    """
    console.print()
    console.print(
        Panel.fit(
            f"[yellow]Environment Variable Not Set[/yellow]\n\n"
            f"[bold]Required:[/bold] {env_var_name}\n\n"
            f"[yellow]Set it now:[/yellow]\n"
            f"  [dim]export {env_var_name}=your-api-key-here[/dim]\n\n"
            f"Or add to ~/.bashrc or ~/.zshrc for persistence",
            border_style="yellow",
            title="[bold]Config Reminder[/bold]",
        )
    )
    console.print()
