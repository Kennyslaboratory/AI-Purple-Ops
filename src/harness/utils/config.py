from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from .errors import ConfigError
from .paths import ensure_dirs

_ENV_PREFIX = "AIPO_"


def _deep_update(base: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    for k, v in new.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_update(base[k], v)
        else:
            base[k] = v
    return base


@dataclass
class RunConfig:
    output_dir: str = "out"
    reports_dir: str = "out/reports"
    transcripts_dir: str = "out/transcripts"
    log_level: str = "INFO"
    seed: int = 42


@dataclass
class AdaptersConfig:
    garak: dict[str, Any] = field(default_factory=lambda: {"model": "openai:gpt-4o-mini"})
    art: dict[str, Any] = field(default_factory=lambda: {"enabled": True})


@dataclass
class HarnessConfig:
    run: RunConfig = field(default_factory=RunConfig)
    adapters: AdaptersConfig = field(default_factory=AdaptersConfig)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        raise ConfigError(f"Invalid YAML in {path}: {e!r}") from e


def _apply_env(cfg: dict[str, Any]) -> dict[str, Any]:
    # Simple env overrides for top-level run.*
    mapping = {
        "run.output_dir": os.getenv(f"{_ENV_PREFIX}OUTPUT_DIR"),
        "run.reports_dir": os.getenv(f"{_ENV_PREFIX}REPORTS_DIR"),
        "run.transcripts_dir": os.getenv(f"{_ENV_PREFIX}TRANSCRIPTS_DIR"),
        "run.log_level": os.getenv(f"{_ENV_PREFIX}LOG_LEVEL"),
        "run.seed": os.getenv(f"{_ENV_PREFIX}SEED"),
    }
    for dotted_key, val in mapping.items():
        if val is None:
            continue
        sect, key = dotted_key.split(".", 1)
        if sect not in cfg:
            cfg[sect] = {}
        # Cast seed to int if provided
        cfg[sect][key] = int(val) if dotted_key.endswith("seed") else val
    return cfg


def load_config(yaml_path: str | None = None) -> HarnessConfig:
    """Load configuration from defaults, configs/harness.yaml, and environment."""
    load_dotenv(override=False)
    base: dict[str, Any] = {
        "run": {
            "output_dir": "out",
            "reports_dir": "out/reports",
            "transcripts_dir": "out/transcripts",
            "log_level": "INFO",
            "seed": 42,
        },
        "adapters": {
            "garak": {"model": "openai:gpt-4o-mini"},
            "art": {"enabled": True},
        },
    }
    file_cfg = _load_yaml(Path(yaml_path) if yaml_path else Path("configs/harness.yaml"))
    merged = _deep_update(base, file_cfg)
    merged = _apply_env(merged)

    # Validate basics
    if "run" not in merged:
        raise ConfigError("Missing 'run' section in configuration")
    rc = RunConfig(**merged["run"])
    ac = AdaptersConfig(**merged.get("adapters", {}))
    # Ensure dirs exist (self-healing)
    ensure_dirs([rc.output_dir, rc.reports_dir, rc.transcripts_dir])
    return HarnessConfig(run=rc, adapters=ac)
