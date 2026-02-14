#!/usr/bin/env python3
# ruff: noqa: S603
"""
Generate deterministic docs tables and update README placeholder blocks.

Outputs:
  - docs/generated/supported-integrations.md
  - docs/generated/technique-coverage.md

Also updates README.md content between:
  <!-- BEGIN GENERATED: supported-integrations -->
  ...
  <!-- END GENERATED: supported-integrations -->
  <!-- BEGIN GENERATED: technique-coverage -->
  ...
  <!-- END GENERATED: technique-coverage -->
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-not-found]
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
DOCS_GENERATED_DIR = ROOT / "docs" / "generated"
README_PATH = ROOT / "README.md"


@dataclass(frozen=True)
class AdapterRow:
    name: str
    adapter_type: str
    requirements: str


@dataclass(frozen=True)
class SuiteRow:
    category: str
    suite_file: str
    name: str
    description: str
    tests: int
    techniques_examples: str


def _run(cmd: list[str], *, env: dict[str, str] | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            f"  cmd: {cmd}\n"
            f"  cwd: {ROOT}\n"
            f"  exit: {proc.returncode}\n"
            f"  stdout:\n{proc.stdout}\n"
            f"  stderr:\n{proc.stderr}\n"
        )
    return proc.stdout


def _find_aipop_bin() -> Path:
    # Prefer the repo venv for determinism (same CLI our tests use).
    candidates = [
        ROOT / ".venv" / "bin" / "aipop",
        ROOT / ".venv" / "Scripts" / "aipop.exe",
    ]
    for p in candidates:
        if p.exists():
            return p
    # Fall back to PATH.
    return Path("aipop")


def _parse_rich_table_rows(text: str, *, ncols: int) -> list[list[str]]:
    # Rich tables are rendered with box drawing chars. We only rely on the "│" row delimiter.
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("│"):
            continue
        parts = [p.strip() for p in line.split("│")[1:-1]]
        if len(parts) != ncols:
            continue
        rows.append(parts)
    return rows


def _merge_wrapped_rows(rows: list[list[str]]) -> list[list[str]]:
    merged: list[list[str]] = []
    for r in rows:
        if not merged:
            merged.append(r)
            continue
        # If the first column is empty, Rich is wrapping a previous row; append non-empty cells.
        if r[0] == "":
            prev = merged[-1][:]
            out: list[str] = []
            for i, cell in enumerate(r):
                if cell:
                    out.append((prev[i] + " " + cell).strip())
                else:
                    out.append(prev[i])
            merged[-1] = out
            continue
        merged.append(r)
    return merged


def load_adapters_from_cli() -> list[AdapterRow]:
    aipop = _find_aipop_bin()

    # Pin terminal width so Rich wrapping is stable across environments.
    env = dict(os.environ)
    env.setdefault("COLUMNS", "200")
    env.setdefault("LINES", "40")
    env.setdefault("NO_COLOR", "1")

    out = _run([str(aipop), "adapter", "list"], env=env)
    raw_rows = _parse_rich_table_rows(out, ncols=3)
    rows = _merge_wrapped_rows(raw_rows)

    adapters: list[AdapterRow] = []
    for name, adapter_type, requirements in rows:
        if not name:
            continue
        adapters.append(
            AdapterRow(
                name=name,
                adapter_type=adapter_type or "Unknown",
                requirements=requirements or "Unknown",
            )
        )

    # Stable ordering.
    adapters.sort(key=lambda r: r.name)
    return adapters


def _yaml_load(path: Path) -> dict[str, Any]:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required to parse suite YAML for docs generation")

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise RuntimeError(f"Suite YAML did not parse into a dict: {path}")
    return data


def load_suites_from_yaml() -> list[SuiteRow]:
    suite_paths = sorted((ROOT / "suites").rglob("*.yaml"))
    suites: list[SuiteRow] = []

    for p in suite_paths:
        category = p.parent.name
        data = _yaml_load(p)
        suite_name = str(data.get("name") or p.stem)
        description = str(data.get("description") or "").strip()
        cases = data.get("cases") or []
        if not isinstance(cases, list):
            cases = []

        techniques: set[str] = set()
        for c in cases:
            if not isinstance(c, dict):
                continue
            md = c.get("metadata") or {}
            if not isinstance(md, dict):
                continue
            t = md.get("technique")
            if isinstance(t, str) and t.strip():
                techniques.add(t.strip())

        # Keep this column short and deterministic for README embedding.
        technique_examples = ", ".join(sorted(techniques)[:3]) if techniques else "-"

        suites.append(
            SuiteRow(
                category=category,
                suite_file=str(p.relative_to(ROOT)).replace("\\", "/"),
                name=suite_name,
                description=description or "-",
                tests=len(cases),
                techniques_examples=technique_examples,
            )
        )

    # Stable ordering for deterministic output.
    suites.sort(key=lambda r: (r.category, r.suite_file))
    return suites


def _md_escape(text: str) -> str:
    # Minimal escaping for tables.
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render_supported_integrations(adapters: list[AdapterRow]) -> str:
    lines: list[str] = []
    lines.append("<!-- GENERATED FILE: do not edit by hand. See docs/generated/README.md. -->")
    lines.append("")
    lines.append("| Integration (`--adapter`) | Type | Requirements | Status |")
    lines.append("|---|---|---|---|")
    for a in adapters:
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_escape(a.name),
                    _md_escape(a.adapter_type),
                    _md_escape(a.requirements),
                    "Supported",
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append(
        "> Note: “Supported” is limited to built-in adapters listed by `aipop adapter list`."
    )
    return "\n".join(lines) + "\n"


def render_technique_coverage(suites: list[SuiteRow]) -> str:
    lines: list[str] = []
    lines.append("<!-- GENERATED FILE: do not edit by hand. See docs/generated/README.md. -->")
    lines.append("")
    lines.append("| Category | Suite YAML | Name | Tests | Techniques (examples) |")
    lines.append("|---|---|---|---:|---|")
    for s in suites:
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_escape(s.category),
                    f"`{_md_escape(s.suite_file)}`",
                    _md_escape(s.name),
                    str(s.tests),
                    _md_escape(s.techniques_examples),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("> Note: This table is derived from suite YAML under `suites/` (case metadata).")
    return "\n".join(lines) + "\n"


def _replace_generated_block(readme_text: str, *, key: str, replacement: str) -> str:
    begin = f"<!-- BEGIN GENERATED: {key} -->"
    end = f"<!-- END GENERATED: {key} -->"

    b = readme_text.find(begin)
    if b == -1:
        raise RuntimeError(f"README markers not found for key '{key}': missing begin marker")
    b_line_end = readme_text.find("\n", b)
    if b_line_end == -1:
        raise RuntimeError(f"README markers not found for key '{key}': malformed begin marker line")
    e = readme_text.find(end, b_line_end + 1)
    if e == -1:
        raise RuntimeError(f"README markers not found for key '{key}': missing end marker")

    middle = (
        "<!-- GENERATED: do not edit by hand. Run: make docs-tables -->\n\n"
        + replacement.strip()
        + "\n"
    )
    content_start = b_line_end + 1
    content_end = e
    return readme_text[:content_start] + middle + readme_text[content_end:]


def write_if_changed(path: Path, content: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if existing == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    adapters = load_adapters_from_cli()
    suites = load_suites_from_yaml()

    supported_md = render_supported_integrations(adapters)
    technique_md = render_technique_coverage(suites)

    DOCS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    write_if_changed(DOCS_GENERATED_DIR / "supported-integrations.md", supported_md)
    write_if_changed(DOCS_GENERATED_DIR / "technique-coverage.md", technique_md)

    readme = README_PATH.read_text(encoding="utf-8")
    readme2 = _replace_generated_block(
        readme,
        key="supported-integrations",
        replacement=supported_md,
    )
    readme3 = _replace_generated_block(
        readme2,
        key="technique-coverage",
        replacement=technique_md,
    )
    write_if_changed(README_PATH, readme3)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
