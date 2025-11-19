"""MCP method implementations.

Implements all MCP spec methods:
- Lifecycle: initialize, initialized, shutdown
- Tools: tools/list, tools/call
- Resources: resources/list, resources/read, resources/templates/list
- Prompts: prompts/list, prompts/get
- Completion: completion/complete
- Logging: logging/setLevel, notifications/message
"""

from __future__ import annotations

__all__ = [
    "LifecycleMethods",
    "ToolsMethods",
    "ResourcesMethods",
    "PromptsMethods",
    "CompletionMethods",
    "LoggingMethods",
]

# Lazy imports
def __getattr__(name: str):
    """Lazy import to avoid loading heavy dependencies until needed."""
    if name == "LifecycleMethods":
        from harness.adapters.mcp.methods.lifecycle import LifecycleMethods
        return LifecycleMethods
    if name == "ToolsMethods":
        from harness.adapters.mcp.methods.tools import ToolsMethods
        return ToolsMethods
    if name == "ResourcesMethods":
        from harness.adapters.mcp.methods.resources import ResourcesMethods
        return ResourcesMethods
    if name == "PromptsMethods":
        from harness.adapters.mcp.methods.prompts import PromptsMethods
        return PromptsMethods
    if name == "CompletionMethods":
        from harness.adapters.mcp.methods.completion import CompletionMethods
        return CompletionMethods
    if name == "LoggingMethods":
        from harness.adapters.mcp.methods.logging import LoggingMethods
        return LoggingMethods
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

