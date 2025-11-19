"""MCP transport layer implementations.

Supports three transport types:
- HTTP: Streamable POST+SSE (2025 spec) and legacy HTTP+SSE fallback
- stdio: Local process communication via stdin/stdout
- WebSocket: Community transport (not official spec)

All transports implement the MCPTransport protocol for uniform interface.
"""

from __future__ import annotations

__all__ = ["MCPTransport", "HTTPTransport", "StdioTransport", "WebSocketTransport"]

# Lazy imports
def __getattr__(name: str):
    """Lazy import to avoid loading heavy dependencies until needed."""
    if name == "MCPTransport":
        from harness.adapters.mcp.transports.base import MCPTransport
        return MCPTransport
    if name == "HTTPTransport":
        from harness.adapters.mcp.transports.http import HTTPTransport
        return HTTPTransport
    if name == "StdioTransport":
        from harness.adapters.mcp.transports.stdio import StdioTransport
        return StdioTransport
    if name == "WebSocketTransport":
        from harness.adapters.mcp.transports.websocket import WebSocketTransport
        return WebSocketTransport
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

