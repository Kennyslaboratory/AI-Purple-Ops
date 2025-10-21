"""Adapter protocol for model I/O abstraction."""

from __future__ import annotations

from typing import Any, Protocol


class Adapter(Protocol):
    """Model I/O abstraction (device driver analogy)."""

    def invoke(self, prompt: str, **kwargs: Any) -> str:  # noqa: ANN401
        """Invoke the model with a prompt and return response."""
        ...

    # TODO(b05): Add streaming support
    # TODO(b07): Add tool call support for agent testing
