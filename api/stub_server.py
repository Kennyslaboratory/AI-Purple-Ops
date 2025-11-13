"""Minimal FastAPI stub for early integration testing."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI-Purple-Ops API", version="0.0.1")


class RunRequest(BaseModel):
    """Request to start a recipe run."""

    recipe: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/runs")
def start_run(req: RunRequest) -> dict[str, str | bool]:
    """Start a recipe run (stub implementation).

    Args:
        req: Run request with recipe name

    Returns:
        Acceptance response with stub run_id
    """
    return {"accepted": True, "recipe": req.recipe, "run_id": "stub-run"}
