"""Mutator implementations."""

from harness.mutators.encoding import EncodingMutator
from harness.mutators.html import HTMLMutator
from harness.mutators.genetic import GeneticMutator
from harness.mutators.paraphrasing import ParaphrasingMutator
from harness.mutators.unicode_mutator import UnicodeMutator

try:
    from harness.mutators.gcg_mutator import GCGMutator

    __all__ = [
        "EncodingMutator",
        "UnicodeMutator",
        "HTMLMutator",
        "ParaphrasingMutator",
        "GeneticMutator",
        "GCGMutator",
    ]
except ImportError:
    __all__ = [
        "EncodingMutator",
        "UnicodeMutator",
        "HTMLMutator",
        "ParaphrasingMutator",
        "GeneticMutator",
    ]


