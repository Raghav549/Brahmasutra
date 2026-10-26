"""🕉️ ब्रह्म-LLM — a from-scratch model stack for the सूत्र language.

Nothing in this package downloads weights or imports a third-party ML library:
the tokenizer, the two models, the gradients, the autonomous trainer, the
self-editor, the सूत्र-OS kernel, the agent (chat · code · run · explain · image)
and the HTTP server are all implemented here in plain Python.

Quick start::

    from brahma_llm import BrahmaLLM, SutraTokenizer, BrahmaAgent

    agent = BrahmaAgent(checkpoint="~/सूत्र-तंत्र/llm/best")
    print(agent.respond("कोड लिखो: अभाज्य संख्या जाँच")["text"])

The model *is* the application: ``brahma llm serve`` exposes it over HTTP.
See ``docs/LLM.md`` for the measured numbers and the honest scope.
"""

from .agent import BrahmaAgent, detect_intent, synthesize
from .model import PRESETS, BrahmaLLM, LanguageModel, NeuralLM, NgramLM, build_model
from .tokenizer import SutraTokenizer, aksharas

__all__ = [
    "BrahmaAgent",
    "BrahmaLLM",
    "detect_intent",
    "synthesize",
    "LanguageModel",
    "NeuralLM",
    "NgramLM",
    "PRESETS",
    "SutraTokenizer",
    "aksharas",
    "build_model",
]

__version__ = "3.0.0"
