#!/usr/bin/env python3
"""
Evidence pack round-trip test.
Creates a sample evidence pack, verifies structure, and proves the spec works.
"""

from __future__ import annotations

import datetime as dt
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    run_id = dt.datetime.now(dt.UTC).strftime("test_%Y%m%d_%H%M%S")
    pack = OUT / f"{run_id}.zip"
    tmp = OUT / run_id
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "transcripts").mkdir(exist_ok=True)
    (tmp / "artifacts").mkdir(exist_ok=True)
    (tmp / "summary").mkdir(exist_ok=True)

    manifest = {
        "run_id": run_id,
        "started_at": dt.datetime.now(dt.UTC).isoformat(),
        "finished_at": dt.datetime.now(dt.UTC).isoformat(),
        "recipe": "evidence.test",
        "gate": {"passed": True, "reason": "smoke", "metrics": {"coverage": 1.0}},
        "files": [
            "transcripts/session.jsonl",
            "summary/report.json",
        ],
    }
    (tmp / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (tmp / "transcripts" / "session.jsonl").write_text(
        '{"role":"user","text":"hello"}\n', encoding="utf-8"
    )
    (tmp / "summary" / "report.json").write_text(json.dumps({"ok": True}), encoding="utf-8")

    with zipfile.ZipFile(pack, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in tmp.rglob("*"):
            if p.is_file():
                z.write(p, arcname=p.relative_to(tmp))
    print(f"✓ Wrote evidence pack {pack}")
    print(f"✓ Archive size: {pack.stat().st_size} bytes")

    # Verify the pack
    with zipfile.ZipFile(pack, "r") as z:
        manifest_data = json.loads(z.read("manifest.json"))
        for f in manifest_data["files"]:
            if f not in z.namelist():
                raise ValueError(f"Missing file: {f}")
    print("✓ Evidence pack structure valid")


if __name__ == "__main__":
    main()
