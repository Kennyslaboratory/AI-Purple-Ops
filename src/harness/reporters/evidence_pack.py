"""Evidence pack generator for compliance and audit artifacts."""

from __future__ import annotations

import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from harness.core.gates import GateResult
from harness.utils.errors import HarnessError


class EvidencePackError(HarnessError):
    """Error generating evidence pack."""


class EvidencePackGenerator:
    """Generate evidence packs with all test artifacts and metadata."""

    def __init__(self, output_dir: Path | str) -> None:
        """Initialize evidence pack generator.

        Args:
            output_dir: Base output directory where evidence packs will be created
        """
        output_path = Path(output_dir)
        # Check if path already ends with "evidence" to avoid duplication
        # Use absolute path for comparison to handle both relative and absolute paths
        abs_path = str(output_path.resolve())
        if abs_path.endswith("evidence") or output_path.name == "evidence":
            self.output_dir = output_path
        else:
            self.output_dir = output_path / "evidence"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        run_id: str,
        summary_path: Path | str,
        junit_path: Path | str | None = None,
        transcripts_dir: Path | str | None = None,
        gate_result: GateResult | None = None,
        metrics: dict[str, float] | None = None,
        tool_results: dict[str, Any] | None = None,
    ) -> Path:
        """Generate evidence pack ZIP file.

        Collects all artifacts, creates manifest, and packages into ZIP.

        Args:
            run_id: Unique run identifier
            summary_path: Path to summary.json
            junit_path: Optional path to junit.xml
            transcripts_dir: Optional directory containing transcript files
            gate_result: Optional gate evaluation result
            metrics: Optional dictionary of metrics

        Returns:
            Path to generated evidence pack ZIP file

        Raises:
            EvidencePackError: If generation fails
        """
        summary_path = Path(summary_path)

        if not summary_path.exists():
            raise EvidencePackError(f"Summary file not found: {summary_path}")

        # Use output directory directly (already set to evidence dir in __init__)
        evidence_dir = self.output_dir
        evidence_dir.mkdir(parents=True, exist_ok=True)

        # Generate evidence pack filename
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
        zip_filename = f"{run_id}_evidence_{timestamp}.zip"
        zip_path = evidence_dir / zip_filename

        try:
            # Collect artifacts
            artifacts: list[dict[str, Any]] = []

            # Add summary.json
            artifacts.append(
                {
                    "type": "summary",
                    "path": "reports/summary.json",
                    "description": "Test execution summary with metrics",
                }
            )

            # Add junit.xml if present
            if junit_path:
                junit_path_obj = Path(junit_path)
                if junit_path_obj.exists():
                    artifacts.append(
                        {
                            "type": "junit",
                            "path": "reports/junit.xml",
                            "description": "JUnit XML report for CI/CD integration",
                        }
                    )

            # Add transcripts if present
            transcript_count = 0
            if transcripts_dir:
                transcripts_path = Path(transcripts_dir)
                if transcripts_path.exists() and transcripts_path.is_dir():
                    transcript_files = list(transcripts_path.glob("*.json"))
                    transcript_count = len(transcript_files)
                    if transcript_count > 0:
                        artifacts.append(
                            {
                                "type": "transcripts",
                                "path": "transcripts/",
                                "count": transcript_count,
                                "description": "Full conversation transcripts",
                            }
                        )

            # Create evidence manifest
            manifest: dict[str, Any] = {
                "run_id": run_id,
                "timestamp": datetime.now(UTC).isoformat(),
                "artifacts": artifacts,
            }

            # Add gate result if provided
            if gate_result:
                manifest["gate_result"] = {
                    "passed": gate_result.passed,
                    "reason": gate_result.reason,
                }

            # Add metrics if provided
            if metrics:
                manifest["metrics"] = metrics

            # Add tool results if provided
            if tool_results:
                manifest["tool_results"] = tool_results
                artifacts.append(
                    {
                        "type": "tool_results",
                        "path": "tool_results.json",
                        "description": "External redteam tool execution results",
                    }
                )

            # Create ZIP file with size limit (100MB)
            MAX_ZIP_SIZE = 100 * 1024 * 1024  # 100MB
            total_size = 0

            def check_size(file_size: int) -> None:
                nonlocal total_size
                total_size += file_size
                if total_size > MAX_ZIP_SIZE:
                    size_mb = MAX_ZIP_SIZE / (1024 * 1024)
                    current_mb = total_size / (1024 * 1024)
                    raise EvidencePackError(
                        f"Evidence pack would exceed size limit ({size_mb:.0f}MB). "
                        f"Current size: {current_mb:.2f}MB"
                    )

            # Create ZIP file
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add summary.json
                summary_size = summary_path.stat().st_size
                check_size(summary_size)
                zipf.write(summary_path, "reports/summary.json")

                # Add junit.xml if present
                if junit_path:
                    junit_path_obj = Path(junit_path)
                    if junit_path_obj.exists():
                        junit_size = junit_path_obj.stat().st_size
                        check_size(junit_size)
                        zipf.write(junit_path_obj, "reports/junit.xml")

                # Add transcripts if present
                if transcripts_dir:
                    transcripts_path = Path(transcripts_dir)
                    if transcripts_path.exists() and transcripts_path.is_dir():
                        for transcript_file in transcripts_path.glob("*.json"):
                            transcript_size = transcript_file.stat().st_size
                            check_size(transcript_size)
                            zipf.write(
                                transcript_file,
                                f"transcripts/{transcript_file.name}",
                            )

                # Add evidence manifest
                manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
                manifest_size = len(manifest_json.encode("utf-8"))
                check_size(manifest_size)
                zipf.writestr("evidence_manifest.json", manifest_json)

                # Add conformance report stub (for b08)
                conformance_stub = {
                    "run_id": run_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "note": "Conformance report will be populated in b08 with framework mappings",
                    "frameworks": [],
                }
                conformance_json = json.dumps(conformance_stub, indent=2, ensure_ascii=False)
                conformance_size = len(conformance_json.encode("utf-8"))
                check_size(conformance_size)
                zipf.writestr("conformance_report.json", conformance_json)

            # Verify ZIP was created successfully
            if not zip_path.exists():
                raise EvidencePackError(f"Evidence pack ZIP file was not created: {zip_path}")

            zip_size = zip_path.stat().st_size
            if zip_size == 0:
                raise EvidencePackError(f"Evidence pack ZIP file is empty: {zip_path}")

            return zip_path

        except Exception as e:
            raise EvidencePackError(f"Failed to generate evidence pack: {e}") from e
