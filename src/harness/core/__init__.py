"""Core interfaces for AI Purple Ops evaluation framework."""

from __future__ import annotations

from .adapters import Adapter
from .models import RunResult, TestCase
from .reporters import Reporter
from .runners import Runner

__all__ = ["Adapter", "Reporter", "RunResult", "Runner", "TestCase"]

# Future exports (uncomment when implemented):
# from .detectors import Detector
# from .evaluators import Evaluator
# from .probes import Probe
# from .mutators import Mutator
# from .exploits import ExploitBuilder
