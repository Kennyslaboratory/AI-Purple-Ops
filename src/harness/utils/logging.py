from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from rich.console import Console
from rich.traceback import install as rich_traceback

rich_traceback(show_locals=False)


@dataclass
class ConsoleLogger:
    width: int = 120
    _console: Console | None = None

    def __post_init__(self) -> None:
        if self._console is None:
            self._console = Console(width=self.width, soft_wrap=False)

    def info(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[cyan][*][/cyan] {msg}")

    def ok(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[bold green][+][/bold green] {msg}")

    def warn(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[yellow][!][/yellow] {msg}")

    def error(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[bold red]\\[x][/bold red] {msg}")

    def try_(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[blue][~][/blue] {msg}")

    def skip(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[dim][-][/dim] {msg}")

    def step(self, msg: str) -> None:
        assert self._console is not None
        self._console.print(f"[magenta][>][/magenta] {msg}")

    @contextmanager
    def section(self, title: str) -> Iterator[None]:
        self.step(title)
        try:
            yield
            self.ok(f"{title} - done")
        except Exception as e:
            self.error(f"{title} - failed: {e!r}")
            raise


log = ConsoleLogger()
