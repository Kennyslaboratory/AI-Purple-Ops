"""Typer-based CLI for AI Purple Ops."""

from __future__ import annotations

import json
import os
import uuid
from datetime import UTC, datetime
from pathlib import Path

import typer

from harness import __version__
from harness.utils.config import HarnessConfig, load_config
from harness.utils.errors import HarnessError
from harness.utils.logging import log
from harness.utils.preflight import preflight

app = typer.Typer(add_completion=False, help="AI Purple Ops CLI")


def _apply_cli_overrides(
    cfg: HarnessConfig,
    output_dir: str | None,
    reports_dir: str | None,
    transcripts_dir: str | None,
    log_level: str | None,
    seed: int | None,
) -> HarnessConfig:
    """Apply CLI overrides to configuration."""
    # Aliasing for brevity
    run = cfg.run
    if output_dir:
        run.output_dir = output_dir
    if reports_dir:
        run.reports_dir = reports_dir
    if transcripts_dir:
        run.transcripts_dir = transcripts_dir
    if log_level:
        run.log_level = log_level
    if seed is not None:
        run.seed = int(seed)
    return cfg


@app.command("version")
def version_cmd() -> None:
    """Print version."""
    log.info(f"AI Purple Ops version {__version__}")
    log.ok("Done")


@app.command("run")
def run_cmd(
    suite: str = typer.Option("normal", "--suite", "-s", help="Suite name to execute."),
    config: Path | None = typer.Option(
        None, "--config", "-c", help="Path to configs/harness.yaml."
    ),
    output_dir: Path | None = typer.Option(None, "--output-dir", help="Override run.output_dir."),
    reports_dir: Path | None = typer.Option(
        None, "--reports-dir", help="Override run.reports_dir."
    ),
    transcripts_dir: Path | None = typer.Option(
        None, "--transcripts-dir", help="Override run.transcripts_dir."
    ),
    log_level: str | None = typer.Option(None, "--log-level", help="Override run.log_level."),
    seed: int | None = typer.Option(None, "--seed", help="Override run.seed."),
    dry_run: bool = typer.Option(
        True, "--dry-run/--no-dry-run", help="Write a small JSON artifact only."
    ),
) -> None:
    """Smoke execution. Preflight, then write a small JSON so gates have something to read."""
    try:
        cfg = load_config(str(config) if config else None)
        cfg = _apply_cli_overrides(
            cfg,
            str(output_dir) if output_dir else None,
            str(reports_dir) if reports_dir else None,
            str(transcripts_dir) if transcripts_dir else None,
            log_level,
            seed,
        )

        preflight(str(config) if config else None)

        now = datetime.now(UTC)
        run_id = f"draft-{now.strftime('%Y%m%dT%H%M%S')}-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        artifact = Path(cfg.run.reports_dir) / "cli_run_smoke.json"

        with log.section("Run skeleton"):
            payload = {
                "run_id": run_id,
                "suite": suite,
                "version": __version__,
                "utc_started": now.isoformat(timespec="seconds"),
                "mode": "dry_run" if dry_run else "exec",
                "notes": "b03 CLI skeleton payload. Real runner arrives in b04.",
            }
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            log.info(f"Wrote {artifact}")
            log.ok("Run skeleton OK")

        log.ok("CLI run completed")
    except HarnessError as e:
        log.error(f"Harness error: {e!r}")
        raise typer.Exit(code=1) from None
    except Exception as e:  # pragma: no cover
        log.error(f"Unhandled error: {e!r}")
        raise typer.Exit(code=1) from e


@app.command("gate")
def gate_cmd(
    summary: Path | None = typer.Option(
        None, "--summary", "-r", help="Path to a JSON summary to check."
    ),
    config: Path | None = typer.Option(
        None, "--config", "-c", help="Optional config to locate reports dir."
    ),
) -> None:
    """Placeholder gate. Verifies the smoke artifact exists. Real thresholds land in b06."""
    try:
        cfg = load_config(str(config) if config else None)
        preflight(str(config) if config else None)
        candidate = summary or (Path(cfg.run.reports_dir) / "cli_run_smoke.json")

        with log.section("Gate skeleton"):
            if not candidate.exists():
                log.warn(f"Summary not found, skipping gate: {candidate}")
                log.ok("Gate skeleton OK")
                raise typer.Exit(code=0)
            data = json.loads(candidate.read_text(encoding="utf-8"))
            _ = data.get("run_id")  # presence check only
            log.info(f"Found summary {candidate.name}")
            log.ok("Gate skeleton OK")
    except HarnessError as e:
        log.error(f"Harness error: {e!r}")
        raise typer.Exit(code=1) from None
    except Exception as e:  # pragma: no cover
        log.error(f"Unhandled error: {e!r}")
        raise typer.Exit(code=1) from e


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
