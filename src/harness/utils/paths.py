"""XDG-compliant data directory management using platformdirs.

Provides consistent, OS-appropriate paths for:
- Session databases
- Payload databases
- Response cache
- Configuration files
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Use platformdirs (not appdirs - actively maintained)
try:
    import platformdirs
    HAVE_PLATFORMDIRS = True
except ImportError:
    HAVE_PLATFORMDIRS = False
    logger.warning("platformdirs not installed, falling back to local directories")


def get_data_dir(override: Path | str | None = None) -> Path:
    """Get the data directory for AI Purple Ops.
    
    Uses XDG Base Directory specification on Linux/BSD,
    appropriate locations on macOS/Windows.
    
    Default locations:
    - Linux: ~/.local/share/aipop/
    - macOS: ~/Library/Application Support/aipop/
    - Windows: %LOCALAPPDATA%\\aipop\\
    
    Args:
        override: Optional override path
    
    Returns:
        Path to data directory
    """
    if override:
        path = Path(override)
        logger.info(f"Using override data directory: {path}")
        return path
    
    if HAVE_PLATFORMDIRS:
        path = Path(platformdirs.user_data_dir("aipop", "ai-purple-ops"))
    else:
        # Fallback to local directory
        path = Path.home() / ".aipop" / "data"
    
    # Ensure directory exists
    path.mkdir(parents=True, exist_ok=True)
    
    return path


def get_sessions_dir(data_dir: Path | str | None = None) -> Path:
    """Get the sessions directory.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        Path to sessions directory
    """
    base = get_data_dir(data_dir)
    sessions_dir = base / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir


def get_payloads_dir(data_dir: Path | str | None = None) -> Path:
    """Get the payloads directory.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        Path to payloads directory
    """
    base = get_data_dir(data_dir)
    payloads_dir = base / "payloads"
    payloads_dir.mkdir(parents=True, exist_ok=True)
    return payloads_dir


def get_cache_dir(data_dir: Path | str | None = None) -> Path:
    """Get the cache directory.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        Path to cache directory
    """
    if data_dir:
        cache_dir = Path(data_dir) / "cache"
    elif HAVE_PLATFORMDIRS:
        cache_dir = Path(platformdirs.user_cache_dir("aipop", "ai-purple-ops"))
    else:
        cache_dir = Path.home() / ".aipop" / "cache"
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_config_dir(data_dir: Path | str | None = None) -> Path:
    """Get the config directory.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        Path to config directory
    """
    if data_dir:
        config_dir = Path(data_dir) / "config"
    elif HAVE_PLATFORMDIRS:
        config_dir = Path(platformdirs.user_config_dir("aipop", "ai-purple-ops"))
    else:
        config_dir = Path.home() / ".aipop" / "config"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_session_db_path(session_id: str, data_dir: Path | str | None = None) -> Path:
    """Get path to a specific session database.
    
    Args:
        session_id: Session identifier
        data_dir: Optional data directory override
    
    Returns:
        Path to session database file
    """
    sessions_dir = get_sessions_dir(data_dir)
    return sessions_dir / f"{session_id}.duckdb"


def get_payload_db_path(data_dir: Path | str | None = None) -> Path:
    """Get path to the payload database.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        Path to payload database file
    """
    payloads_dir = get_payloads_dir(data_dir)
    return payloads_dir / "payloads.duckdb"


def get_session_index_path(data_dir: Path | str | None = None) -> Path:
    """Get path to the session index database.
    
    The session index stores metadata about all sessions for quick listing.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        Path to session index database
    """
    sessions_dir = get_sessions_dir(data_dir)
    return sessions_dir / "index.duckdb"


def list_session_ids(data_dir: Path | str | None = None) -> list[str]:
    """List all session IDs by scanning the sessions directory.
    
    Args:
        data_dir: Optional data directory override
    
    Returns:
        List of session IDs (without .duckdb extension)
    """
    sessions_dir = get_sessions_dir(data_dir)
    
    # Find all .duckdb files except index.duckdb
    session_files = [
        f.stem for f in sessions_dir.glob("*.duckdb")
        if f.name != "index.duckdb"
    ]
    
    return sorted(session_files)


def cleanup_old_sessions(days: int = 14, data_dir: Path | str | None = None) -> int:
    """Remove session databases older than specified days.
    
    Args:
        days: Age threshold in days
        data_dir: Optional data directory override
    
    Returns:
        Number of sessions deleted
    """
    import time
    
    sessions_dir = get_sessions_dir(data_dir)
    threshold = time.time() - (days * 86400)  # Convert days to seconds
    deleted = 0
    
    for session_file in sessions_dir.glob("*.duckdb"):
        if session_file.name == "index.duckdb":
            continue
        
        # Check file modification time
        if session_file.stat().st_mtime < threshold:
            logger.info(f"Deleting old session: {session_file.name}")
            session_file.unlink()
            deleted += 1
    
    return deleted


def ensure_dirs(paths: list[Path | str]) -> None:
    """Ensure all directories in the list exist.
    
    Args:
        paths: List of directory paths to create
    """
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)
