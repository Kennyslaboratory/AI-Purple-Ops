"""Legacy scratch implementations for research and testing.

These implementations were created for educational purposes and testing.
For production use, install official implementations via the plugin system:

    aipop plugins install all

Official implementations achieve published ASR rates (88-97%), while these
legacy implementations may only achieve 60-70% ASR.
"""

import warnings

# Emit deprecation warning when legacy module is imported
warnings.warn(
    "You are using legacy (scratch) implementations. "
    "For production use with research-grade ASR rates, install official implementations: "
    "aipop plugins install all",
    DeprecationWarning,
    stacklevel=2,
)

from harness.intelligence.legacy.gcg_blackbox import GCGBlackBoxOptimizer
from harness.intelligence.legacy.autodan_scratch import (
    AutoDANScratchConfig,
    HierarchicalGeneticAlgorithmScratch,
)
from harness.intelligence.legacy.pair_scratch import (
    PAIRScratchConfig,
    PAIRAttackerScratch,
)

__all__ = [
    "GCGBlackBoxOptimizer",
    "AutoDANScratchConfig",
    "HierarchicalGeneticAlgorithmScratch",
    "PAIRScratchConfig",
    "PAIRAttackerScratch",
]

