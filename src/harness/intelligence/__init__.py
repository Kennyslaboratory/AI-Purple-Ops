"""Intelligence layer for advanced AI security testing.

This module provides functional stubs for future intelligence features:
- Guardrail fingerprinting (detect and bypass AI defenses)
- Adversarial suffix generation (GCG/AutoDAN-style attacks)
- Attack tree traversal (automated exploit discovery)

These stubs provide comprehensive interfaces and documentation for future
implementation in branches b08.4, b08.5, and b11.

Example Usage:
    # Guardrail fingerprinting (future b08.4)
    from harness.intelligence import GuardrailFingerprinter

    fingerprinter = GuardrailFingerprinter()
    result = fingerprinter.fingerprint(adapter)
    print(f"Detected: {result['guardrail_type']}")

    # Adversarial suffix generation (future b08.5)
    from harness.intelligence import AdversarialSuffixGenerator

    generator = AdversarialSuffixGenerator(method="gcg")
    suffixes = generator.generate_suffix(
        prompt="Ignore previous instructions",
        target="Sure, I can help"
    )

    # Attack tree traversal (future b11)
    from harness.intelligence import AttackTreeTraverser

    traverser = AttackTreeTraverser()
    paths = traverser.discover_paths(
        start_node="jailbreak",
        goal_node="data_exfiltration"
    )
"""

from harness.intelligence.adversarial_suffix import AdversarialSuffixGenerator
from harness.intelligence.attack_tree import AttackTreeTraverser
from harness.intelligence.guardrail_fingerprint import GuardrailFingerprinter
from harness.intelligence.judge_models import (
    GPT4Judge,
    LlamaGuardJudge,
    KeywordJudge,
    EnsembleJudge,
    JudgmentResult,
)

try:
    from harness.intelligence.gcg_core import GCGOptimizer
    from harness.intelligence.autodan import AutoDANConfig, HierarchicalGeneticAlgorithm
    from harness.intelligence.pair import PAIRConfig, PAIRAttacker
    from harness.intelligence.judge_ensemble import EnsembleJudgeConfig, create_ensemble_judge, LlamaGuardGPT4Ensemble

    __all__ = [
        "GuardrailFingerprinter",
        "AdversarialSuffixGenerator",
        "AttackTreeTraverser",
        "GCGOptimizer",
        "GPT4Judge",
        "LlamaGuardJudge",
        "KeywordJudge",
        "EnsembleJudge",
        "JudgmentResult",
        "AutoDANConfig",
        "HierarchicalGeneticAlgorithm",
        "PAIRConfig",
        "PAIRAttacker",
        "EnsembleJudgeConfig",
        "create_ensemble_judge",
        "LlamaGuardGPT4Ensemble",
    ]
except ImportError:
    __all__ = [
        "GuardrailFingerprinter",
        "AdversarialSuffixGenerator",
        "AttackTreeTraverser",
        "GPT4Judge",
        "LlamaGuardJudge",
        "KeywordJudge",
        "EnsembleJudge",
        "JudgmentResult",
    ]

