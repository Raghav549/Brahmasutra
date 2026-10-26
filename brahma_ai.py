"""🕉️ ब्रह्म AI — a small, real text model (no external services).

The audit found dozens of files named ``*_AI*`` whose "AI" was a chain of
``if`` statements that copied a fixed template.  This module provides the two
things those files claimed to have:

* :class:`MarkovModel` — a trainable character/word n-gram language model that
  generates text and reports a perplexity number;
* :class:`PromptRouter` — a transparent keyword router that maps a natural
  language request to an application template.

Everything runs locally, deterministically (seedable) and without network
access or third-party libraries::

>>> model = MarkovModel(order=1).train("नमस्ते विश्व नमस्ते ब्रह्म")
>>> "नमस्ते" in model.generate("नमस्ते", length=3)
True

``PromptRouter`` is *not* a neural network and says so: :meth:`PromptRouter.explain`
returns the rule that fired.
"""

from __future__ import annotations

import json
import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

__all__ = ["MarkovModel", "PromptRouter", "TEMPLATES"]

#: Application templates the router can pick, with the features each implies.
TEMPLATES: Dict[str, Dict[str, object]] = {
    "chat": {"features": ["register", "login", "chat"], "admin": False},
    "admin_chat": {"features": ["register", "login", "chat", "admin"], "admin": True},
    "status": {"features": ["status"], "admin": False},
}

#: keyword → template.  First match wins, in this order.
RULES: Sequence[Tuple[str, Sequence[str]]] = (
    ("admin_chat", ("admin", "एडमिन", "प्रशासक", "saas", "users")),
    ("chat", ("chat", "चैट", "message", "संदेश", "login", "लॉगिन")),
    ("status", ("status", "स्थिति", "api", "एपीआई", "health")),
)


class MarkovModel:
    """An n-gram language model with backoff to shorter contexts."""

    def __init__(self, order: int = 1, seed: Optional[int] = None) -> None:
        if order < 1:
            raise ValueError("order कम से कम 1 होना चाहिए")
        self.order = order
        self.seed = seed
        self.counts: Dict[str, Dict[str, int]] = {}
        self.starts: List[str] = []
        self.tokens = 0

    # -- training --------------------------------------------------------
    def train(self, text: str) -> "MarkovModel":
        """Add ``text`` to the model (tokens are whitespace separated)."""
        words = str(text).split()
        if not words:
            return self
        self.starts.append(words[0])
        self.tokens += len(words)
        for index, word in enumerate(words):
            context = _context(words, index, self.order)
            if context is None:
                continue
            self.counts.setdefault(context, {})
            self.counts[context][word] = self.counts[context].get(word, 0) + 1
        return self

    def fit(self, texts: Sequence[str]) -> "MarkovModel":
        """Train on several documents."""
        for text in texts:
            self.train(text)
        return self

    # -- generation ------------------------------------------------------
    def is_trained(self) -> bool:
        """True when the model has at least one transition."""
        return bool(self.counts)

    def _next(self, context: str, rng: random.Random) -> Optional[str]:
        """Sample the next token for ``context``, with backoff."""
        probe = context
        while probe:
            choices = self.counts.get(probe)
            if choices:
                population = sorted(choices)
                weights = [choices[token] for token in population]
                return rng.choices(population, weights=weights, k=1)[0]
            probe = probe.split(" ", 1)[1] if " " in probe else ""
        return None

    def generate(self, seed: str = "", length: int = 12) -> str:
        """Generate at most ``length`` tokens starting from ``seed``."""
        if not self.is_trained():
            raise ValueError("मॉडल प्रशिक्षित नहीं है (पहले train() चलाएँ)")
        rng = random.Random(self.seed)
        seed_tokens = str(seed).split()
        if not seed_tokens:
            first = rng.choice(sorted(self.starts))
            seed_tokens = [first]

        tokens = list(seed_tokens)
        while len(tokens) < length:
            context = _context(tokens, len(tokens), self.order)
            if context is None:
                break
            nxt = self._next(context, rng)
            if nxt is None:
                break
            tokens.append(nxt)
        return " ".join(tokens)

    # -- evaluation ------------------------------------------------------
    def perplexity(self, text: str) -> float:
        """Perplexity of ``text`` under the model (lower is better).

        Unknown transitions are smoothed with Add-1 so the value stays finite.
        """
        words = str(text).split()
        if len(words) < 2:
            return float("inf")
        vocabulary = {token for choices in self.counts.values() for token in choices}
        size = max(len(vocabulary), 1)
        log_sum = 0.0
        scored = 0

        for index in range(1, len(words)):
            context = _context(words, index, self.order)
            choices = self.counts.get(context or "", {})
            total = sum(choices.values())
            count = choices.get(words[index], 0)
            probability = (count + 1) / (total + size)
            log_sum += math.log(probability)
            scored += 1

        return math.exp(-log_sum / max(scored, 1))

    # -- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        """Serialisable state."""
        return {
            "order": self.order,
            "seed": self.seed,
            "counts": self.counts,
            "starts": self.starts,
            "tokens": self.tokens,
        }

    def save(self, path: str) -> str:
        """Write the model as JSON; return ``path``."""
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False)
        return path

    @classmethod
    def load(cls, path: str) -> "MarkovModel":
        """Read a model written by :meth:`save`."""
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        model = cls(order=int(data.get("order", 1)), seed=data.get("seed"))
        model.counts = {k: dict(v) for k, v in data.get("counts", {}).items()}
        model.starts = list(data.get("starts", []))
        model.tokens = int(data.get("tokens", 0))
        return model


def _context(tokens: Sequence[str], index: int, order: int) -> Optional[str]:
    """Context string ending *before* ``tokens[index]``."""
    start = index - order
    if start < 0:
        return None
    return " ".join(tokens[start:index])


class PromptRouter:
    """Map a prompt to one of :data:`TEMPLATES` using explicit rules.

    This is a keyword router, not a classifier: :meth:`explain` always returns
    the rule that matched so the decision is auditable.
    """

    def __init__(self, rules: Sequence[Tuple[str, Sequence[str]]] = RULES) -> None:
        self.rules = rules

    def route(self, prompt: str) -> str:
        """Return the template name for ``prompt``."""
        return self.explain(prompt)[0]

    def explain(self, prompt: str) -> Tuple[str, str]:
        """Return ``(template, matched_keyword_or_default)``."""
        lowered = str(prompt or "").lower()
        for template, keywords in self.rules:
            for keyword in keywords:
                if keyword.lower() in lowered:
                    return template, keyword
        return "status", "default"

    def options(self, prompt: str) -> Dict[str, object]:
        """Template description for ``prompt`` (name, features, admin flag, rule)."""
        template, matched = self.explain(prompt)
        spec = dict(TEMPLATES[template])
        spec.update({"template": template, "matched": matched})
        return spec
