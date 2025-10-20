from __future__ import annotations

from pathlib import Path

from .config import load_config
from .errors import PreflightError
from .logging import log


def preflight() -> None:
    """Basic self-healing checks to make dev UX smooth."""
    with log.section("Preflight"):
        cfg = load_config()
        # Sanity for dirs is already ensured in load_config; re-affirm with logs.
        for p in [cfg.run.output_dir, cfg.run.reports_dir, cfg.run.transcripts_dir]:
            if not Path(p).exists():
                raise PreflightError(f"Directory not found after ensure: {p}")
        log.info(f"Output dir     : {cfg.run.output_dir}")
        log.info(f"Reports dir    : {cfg.run.reports_dir}")
        log.info(f"Transcripts dir: {cfg.run.transcripts_dir}")
        log.ok("Preflight OK")
