"""🕉️ ब्रह्म-LLM — a from-scratch language model stack for the सूत्र language.

Nothing in this package downloads weights or imports a third-party ML library:
the tokenizer, the two models, the gradients, the autonomous trainer, the
self-editor and the app generator are all implemented here in plain Python.

Quick start::

    from brahma_llm import BrahmaLLM, SutraTokenizer

See ``docs/LLM.md`` for the measured numbers and the honest scope.
"""

from .model import PRESETS, BrahmaLLM, LanguageModel, NeuralLM, NgramLM, build_model
from .tokenizer import SutraTokenizer, aksharas

__all__ = [
    "BrahmaLLM",
    "LanguageModel",
    "NeuralLM",
    "NgramLM",
    "PRESETS",
    "SutraTokenizer",
    "aksharas",
    "build_model",
]

__version__ = "2.0.0"
