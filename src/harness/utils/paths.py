from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


def ensure_dirs(paths: Iterable[str | Path]) -> None:
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)
