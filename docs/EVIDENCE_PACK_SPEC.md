# Evidence Pack Specification

**Version:** 1.0
**Status:** Final
**Last Updated:** 2025-10-22

---

## Overview

Evidence packs are tamper-evident archives containing all artifacts from a test run. They enable audit trails, compliance verification, and reproducibility of security testing results.

---

## Archive Structure

```
out/evidence/<run_id>.zip
├── manifest.json           # Machine-readable index
├── transcripts/            # Conversation logs
│   └── session.jsonl       # JSONL format, one event per line
├── artifacts/              # External tool outputs, files
│   └── (tool outputs)
└── summary/                # Human-friendly summaries
    └── report.json         # Structured summary for dashboards
```

---

## Manifest Schema

**File:** `manifest.json`

Required fields:

```json
{
  "run_id": "string",
  "started_at": "ISO8601 timestamp with timezone",
  "finished_at": "ISO8601 timestamp with timezone",
  "recipe": "string (recipe name or path)",
  "gate": {
    "passed": "boolean",
    "reason": "string (explanation)",
    "metrics": {"metric_name": 0.0}
  },
  "files": [
    "transcripts/session.jsonl",
    "summary/report.json"
  ]
}
```

### Field Descriptions

- **run_id**: Unique identifier for the test run (UUID or deterministic hash)
- **started_at**: ISO8601 timestamp when run began (UTC, with `Z` suffix)
- **finished_at**: ISO8601 timestamp when run completed (UTC, with `Z` suffix)
- **recipe**: Name or path of the recipe executed
- **gate**: Gate evaluation result (mirrors `GateResult` from core)
  - **passed**: Boolean indicating if all gates passed
  - **reason**: Human-readable explanation of gate outcome
  - **metrics**: Dictionary of metric names to float values
- **files**: List of relative paths to all files in the archive (for integrity checking)

---

## File Formats

### Transcripts (`transcripts/`)

**Format:** JSONL (JSON Lines)

Each line is a valid JSON object representing an event:

```jsonl
{"type":"test","name":"t1","prompt":"ping","response":"[mock:123] ping","passed":true}
{"type":"test","name":"t2","prompt":"test","response":"[mock:456] test","passed":true}
```

### Summary (`summary/report.json`)

**Format:** JSON

Human-friendly summary for dashboards:

```json
{
  "run_id": "test_20251022_143022",
  "passed": true,
  "total_tests": 10,
  "passed_tests": 10,
  "failed_tests": 0,
  "duration_seconds": 2.5,
  "gate_outcome": "PASS",
  "key_metrics": {
    "success_rate": 1.0,
    "coverage": 0.95
  }
}
```

---

## Deterministic Layout Requirements

For reproducibility and compliance:

1. **File paths must be relative** (no absolute paths)
2. **Timestamps must include timezone** (ISO8601 with `Z` or offset)
3. **Manifest must list all files** (enables integrity verification)
4. **Archives use ZIP format** (standard compression, widely supported)
5. **Filenames use run_id** (no collisions, easy identification)

---

## Usage Example

### Creating an Evidence Pack

```python
from pathlib import Path
import json, zipfile, datetime as dt

run_id = "test_20251022_143022"
evidence_dir = Path("out/evidence")
pack_path = evidence_dir / f"{run_id}.zip"
tmp = evidence_dir / run_id

# Create structure
tmp.mkdir(parents=True, exist_ok=True)
(tmp / "transcripts").mkdir()
(tmp / "artifacts").mkdir()
(tmp / "summary").mkdir()

# Write manifest
manifest = {
    "run_id": run_id,
    "started_at": dt.datetime.now(dt.UTC).isoformat(),
    "finished_at": dt.datetime.now(dt.UTC).isoformat(),
    "recipe": "security/prompt_injection",
    "gate": {"passed": True, "reason": "All tests passed", "metrics": {"success_rate": 1.0}},
    "files": ["transcripts/session.jsonl", "summary/report.json"]
}
(tmp / "manifest.json").write_text(json.dumps(manifest, indent=2))

# Write artifacts
(tmp / "transcripts/session.jsonl").write_text('{"event":"test"}\n')
(tmp / "summary/report.json").write_text(json.dumps({"ok": True}))

# Create ZIP archive
with zipfile.ZipFile(pack_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for p in tmp.rglob("*"):
        if p.is_file():
            z.write(p, arcname=p.relative_to(tmp))
```

### Validating an Evidence Pack

```python
import zipfile, json
from pathlib import Path

pack_path = Path("out/evidence/test_20251022_143022.zip")

with zipfile.ZipFile(pack_path, "r") as z:
    # Extract manifest
    manifest = json.loads(z.read("manifest.json"))

    # Verify all listed files exist
    for file_path in manifest["files"]:
        assert file_path in z.namelist(), f"Missing file: {file_path}"

    # Check gate result
    assert "gate" in manifest
    assert "passed" in manifest["gate"]
```

---

## Integration with b06 Recipe Engine

When the recipe engine (b06) executes, it will:

1. Create evidence pack directory structure
2. Stream events to `transcripts/session.jsonl` during execution
3. Collect tool outputs to `artifacts/`
4. Generate summary in `summary/report.json`
5. Write `manifest.json` with gate results
6. Archive everything to `out/evidence/{run_id}.zip`

---

## Compliance Mappings

Evidence packs support compliance requirements:

- **NIST AI RMF**: Evidence for MEASURE phase (MS-2.6, MS-2.7)
- **EU AI Act**: Audit trail for high-risk systems (Article 12)
- **FedRAMP**: Continuous monitoring artifacts (CA-7)
- **ISO 42001**: Testing records for AI management system

---

## See Also

- `scripts/evidence_roundtrip.py` - Reference implementation
- `reports/schemas/evidence_manifest.schema.json` - JSON schema for manifest
- `docs/RECIPES.md` - Recipe system that generates evidence packs
