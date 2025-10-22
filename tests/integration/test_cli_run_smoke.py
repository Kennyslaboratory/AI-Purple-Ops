"""Test CLI run command smoke test."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_run_smoke(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Verify CLI run creates smoke artifact with correct structure."""
    # Get repo root before changing directory
    repo_root = Path(__file__).parent.parent.parent.absolute()

    cfg = tmp_path / "harness.yaml"
    cfg.write_text(
        "run:\n"
        "  output_dir: outx\n"
        "  reports_dir: outx/reports\n"
        "  transcripts_dir: outx/transcripts\n"
        "  log_level: INFO\n"
        "  seed: 7\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    # Add repo root to PYTHONPATH so subprocess can find cli module
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli.harness",
            "run",
            "--suite",
            "normal",
            "--config",
            str(cfg),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0
    out_file = Path("outx/reports/cli_run_smoke.json")
    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data.get("suite") == "normal"
    assert "run_id" in data
