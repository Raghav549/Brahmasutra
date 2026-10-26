"""🕉️ सूत्र कॉर्पस और कार्यक्रम-जनक — the data engine of the autonomous loop.

An autonomous trainer needs data it can trust.  This module produces it in two
ways and never pretends otherwise:

:func:`load_corpus`
    Every ``.sutra`` file in the checkout, the kernel/maths sources that ship
    with the package, and the Devanagari prose from the docs.  Works installed
    from a wheel too, because the embedded seeds are always included.

:class:`ProgramGenerator`
    A grammar/template generator that writes **valid** सूत्र programs from a
    random seed, optionally biased by a target string (``"prime"``, ``"सूची"``,
    …).  Every candidate is compiled *and executed* on :func:`brahma.api.execute`
    before it may enter the corpus — so "the model trained on programs that
    run" is a checked statement, not a vibe.
"""

from __future__ import annotations

import os
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from brahma.api import execute

#: Keywords (Devanagari and ASCII) understood by :class:`ProgramGenerator`.
GOAL_KEYWORDS: Dict[str, Sequence[str]] = {
    "गणित": ("गणित", "math", "अंकगणित", "arithmetic", "योग", "sum", "गुणा"),
    "अभाज्य": ("अभाज्य", "prime"),
    "फ़िबोनाची": ("फ़िबोनाची", "fibonacci", "fib"),
    "सूची": ("सूची", "list", "सरणी", "array"),
    "पाठ": ("पाठ", "string", "text", "शब्द"),
    "चक्र": ("चक्र", "loop", "iteration", "पुनरावृत्ति"),
    "कर्नेल": ("कर्नेल", "kernel", "os", "boot", "ऑपरेटिंग"),
    "अनुप्रयोग": ("अनुप्रयोग", "app", "application", "वेब", "web"),
}

EMBEDDED_SEEDS = (
    r'''
# सूत्र-OS कर्नेल प्रारम्भ
दर्शय "🕉️ सूत्र-OS"
स्थापय अ = 2 + 3
दर्शय "योग: " + पाठ(अ)
''',
    r'''
कार्य योग(a, b)
    प्रत्यागमन a + b
अन्त
दर्शय योग(3, 4)
''',
)


def repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sutra_files(root: Optional[str] = None, limit: int = 400) -> List[str]:
    """Every ``.sutra``/``.सूत्र`` file under ``root`` (default: repository)."""
    root = root or repo_root()
    found: List[str] = []
    for base, directories, files in os.walk(root):
        directories[:] = [d for d in directories if d not in (".git", "__pycache__", ".venv", "build", "dist")]
        for name in files:
            if name.endswith((".sutra", ".सूत्र")):
                found.append(os.path.join(base, name))
        if len(found) >= limit:
            break
    return sorted(found)[:limit]


def doc_texts(root: Optional[str] = None, limit: int = 12) -> List[str]:
    """Devanagari prose (README, docs, changelog) for natural-language training."""
    root = root or repo_root()
    texts: List[str] = []
    candidates = [os.path.join(root, "README.md"), os.path.join(root, "CHANGELOG.md"),
                  os.path.join(root, "docs", "AUDIT.md"), os.path.join(root, "docs", "TESTING.md")]
    for path in candidates:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for chunk in handle.read().split("\n\n"):
                chunk = chunk.strip()
                if len(chunk) > 40 and sum("\u0900" <= ch <= "\u097f" for ch in chunk) > 10:
                    texts.append(chunk)
    return texts[:limit * 20]


def load_corpus(root: Optional[str] = None, include_docs: bool = True) -> List[str]:
    """All training texts: सूत्र sources + embedded seeds (+ optional prose)."""
    texts = list(EMBEDDED_SEEDS)
    for path in sutra_files(root):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                source = handle.read()
        except OSError:
            continue
        if source.strip():
            texts.append(source)
    texts.extend(_kernel_and_math_sources())
    if include_docs:
        texts.extend(doc_texts(root))
    return texts


def _kernel_and_math_sources() -> List[str]:
    from .kernel import KERNEL_SOURCE
    from .sutra_kernel import SUTRA_MATH

    return [KERNEL_SOURCE, SUTRA_MATH]


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
@dataclass
class GeneratedProgram:
    """A candidate program plus the verdict of running it."""

    source: str
    category: str
    ok: bool
    output: List[str] = field(default_factory=list)
    error: str = ""
    steps: int = 0

    def as_dict(self) -> dict:
        return {"category": self.category, "ok": self.ok, "error": self.error,
                "steps": self.steps, "lines": len(self.source.splitlines())}


def validate_program(source: str, step_limit: int = 200_000) -> GeneratedProgram:
    """Compile and execute ``source``; ``ok`` means it ran without an error."""
    result = execute(source, source_name="<generated>", step_limit=step_limit)
    return GeneratedProgram(
        source=source,
        category="",
        ok=result.error is None,
        output=list(result.output),
        error="" if result.error is None else str(result.error),
        steps=result.steps,
    )


class ProgramGenerator:
    """Template generator for valid सूत्र programs, biased by a goal string."""

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.templates = {
            "गणित": self._math,
            "अभाज्य": self._primes,
            "फ़िबोनाची": self._fibonacci,
            "सूची": self._list_ops,
            "पाठ": self._strings,
            "चक्र": self._loop,
            "कर्नेल": self._kernel,
            "अनुप्रयोग": self._service,
        }

    # -- goal handling ---------------------------------------------------
    def categories_for(self, goal: str = "") -> List[str]:
        goal = (goal or "").lower()
        selected = [name for name, words in GOAL_KEYWORDS.items() if any(word.lower() in goal for word in words)]
        return selected or list(self.templates)

    # -- templates -------------------------------------------------------
    def _math(self) -> str:
        a, b = self.rng.randint(2, 40), self.rng.randint(2, 40)
        op = self.rng.choice(["+", "-", "*"])
        return (
            'स्थापय अ = %d\nस्थापय ब = %d\n'
            'स्थापय परिणाम = अ %s ब\n'
            'दर्शय "परिणाम: " + पाठ(परिणाम)\n' % (a, b, op)
        )

    def _primes(self) -> str:
        limit = self.rng.choice([20, 30, 50, 60])
        return (
            "कार्य अभाज्य(n)\n"
            "    यदि n < 2\n        प्रत्यागमन असत्य\n    अन्त\n"
            "    स्थापय i = 2\n"
            "    यावत् i * i <= n\n"
            "        यदि n %% i == 0\n            प्रत्यागमन असत्य\n        अन्त\n"
            "        i = i + 1\n    अन्त\n"
            "    प्रत्यागमन सत्य\nअन्त\n\n"
            "स्थापय n = 2\n"
            "यावत् n <= %d\n"
            "    यदि अभाज्य(n)\n        दर्शय n\n    अन्त\n"
            "    n = n + 1\nअन्त\n" % limit
        )

    def _fibonacci(self) -> str:
        count = self.rng.choice([8, 10, 12])
        return (
            "स्थापय अ = 0\nस्थापय ब = 1\nस्थापय i = 0\n"
            "यावत् i < %d\n"
            "    दर्शय अ\n"
            "    स्थापय अगला = अ + ब\n"
            "    अ = ब\n    ब = अगला\n    i = i + 1\nअन्त\n" % count
        )

    def _list_ops(self) -> str:
        values = [self.rng.randint(1, 30) for _ in range(4)]
        literal = "[" + ", ".join(str(value) for value in values) + "]"
        return (
            "स्थापय सूची = %s\n"
            "स्थापय योग = 0\nस्थापय i = 0\n"
            "यावत् i < लम्बाई(सूची)\n"
            "    योग = योग + सूची[i]\n    i = i + 1\nअन्त\n"
            'दर्शय "योग: " + पाठ(योग)\n'
            'दर्शय "औसत: " + पाठ(योग / लम्बाई(सूची))\n' % literal
        )

    def _strings(self) -> str:
        word = self.rng.choice(["नमस्ते", "ब्रह्म", "सूत्र", "विश्व", "संस्कृतम्"])
        times = self.rng.choice([2, 3, 4])
        return (
            'स्थापय शब्द = "%s"\n'
            "स्थापय i = 0\nस्थापय पंक्ति = \"\"\n"
            "यावत् i < %d\n"
            '    पंक्ति = पंक्ति + शब्द + " "\n'
            "    i = i + 1\nअन्त\n"
            'दर्शय "लम्बाई: " + पाठ(लम्बाई(पंक्ति))\n' % (word, times)
        )

    def _loop(self) -> str:
        limit = self.rng.choice([5, 6, 7, 10])
        return (
            "स्थापय कुल = 0\nस्थापय i = 1\n"
            "यावत् i <= %d\n    कुल = कुल + i * i\n    i = i + 1\nअन्त\n"
            'दर्शय "वर्गों का योग: " + पाठ(कुल)\n' % limit
        )

    def _kernel(self) -> str:
        value = self.rng.randint(3, 9)
        return (
            "# सूत्र-OS स्व-परीक्षण\n"
            'दर्शय "🕉️ सूत्र-OS"\n'
            "कार्य योग(a, b)\n    प्रत्यागमन a + b\nअन्त\n"
            "स्थापय अ = योग(%d, %d)\n"
            'दर्शय "स्व-परीक्षण: " + पाठ(अ)\n'
            'यदि अ > 0\n    दर्शय "READY"\nअन्त\n' % (value, value)
        )

    def _service(self) -> str:
        port = self.rng.choice([8000, 8080, 9090])
        return (
            "# अनुप्रयोग स्थिति\n"
            'स्थापय नाम = "अनुप्रयोग"\n'
            'स्थापय पोर्ट = %d\n'
            'दर्शय नाम + " पोर्ट " + पाठ(पोर्ट) + " पर तैयार"\n' % port
        )

    # -- public ----------------------------------------------------------
    def generate(self, goal: str = "", count: int = 8, validate: bool = True) -> List[GeneratedProgram]:
        """Generate ``count`` candidates (validated by execution by default)."""
        categories = self.categories_for(goal)
        programs: List[GeneratedProgram] = []
        for _ in range(count):
            category = self.rng.choice(categories)
            source = self.templates[category]()
            candidate = validate_program(source) if validate else GeneratedProgram(source, category, True)
            candidate.category = category
            programs.append(candidate)
        return programs

    def passing(self, goal: str = "", count: int = 8) -> List[GeneratedProgram]:
        """Only the candidates that compiled and ran cleanly."""
        return [program for program in self.generate(goal, count) if program.ok]
