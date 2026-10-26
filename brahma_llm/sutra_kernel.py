"""🕉️ सूत्र-गणित — the model's arithmetic, written in its own language.

The claim "the model is built in सूत्र" is only worth something if it can be
checked.  This module contains the forward pass of
:class:`brahma_llm.model.NeuralLM` as a सूत्र program (the language defined by
``brahma/``), compiles it with the project's own compiler, runs it on the
project's own VM, and compares the result against the Python implementation.

The program implements everything from primitives, because the language's
standard library is deliberately small:

``घातांक(x)``
    ``e**x`` via a 20-term Maclaurin series after scaling by 32 and squaring
    five times.
``सॉफ्टमैक्स(values)``
    max-subtracted softmax.
``अग्रपरत(...)``
    embedding lookup → tanh hidden layer (tanh built from ``घातांक``) → logits.

``python3 -m brahma_llm.sutra_kernel --check`` runs the equivalence proof.
"""

from __future__ import annotations

import json
from typing import List, Optional, Sequence

from brahma.compiler import compile_source
from brahma.vm import VM

#: The reference implementation.  Kept as a string so it can be printed,
#: diffed, compiled and — importantly — read by a Sanskrit programmer.
SUTRA_MATH = r'''
# 🕉️ सूत्र-गणित — ब्रह्म-LLM का अग्रगमन, सूत्र भाषा में लिखा गया।

# e^x — 32 से विभाजित करके 20 पदों की श्रेणी, फिर 5 बार वर्ग।
कार्य घातांक(x)
    स्थापय y = x / 32.0
    स्थापय s = 1.0
    स्थापय term = 1.0
    स्थापय i = 1
    यावत् i <= 20
        term = term * y / i
        s = s + term
        i = i + 1
    अन्त
    स्थापय k = 0
    यावत् k < 5
        s = s * s
        k = k + 1
    अन्त
    प्रत्यागमन s
अन्त

# tanh(a) = (e^2a - 1) / (e^2a + 1)
कार्य स्पर्शरेखा(a)
    स्थापय e = घातांक(2.0 * a)
    प्रत्यागमन (e - 1.0) / (e + 1.0)
अन्त

कार्य सॉफ्टमैक्स(values)
    स्थापय n = लम्बाई(values)
    स्थापय m = values[0]
    स्थापय i = 1
    यावत् i < n
        यदि values[i] > m
            m = values[i]
        अन्त
        i = i + 1
    अन्त
    स्थापय total = 0.0
    स्थापय e = []
    स्थापय k = 0
    यावत् k < n
        स्थापय v = घातांक(values[k] - m)
        जोड़ें(e, v)
        total = total + v
        k = k + 1
    अन्त
    स्थापय out = []
    स्थापय q = 0
    यावत् q < n
        जोड़ें(out, e[q] / total)
        q = q + 1
    अन्त
    प्रत्यागमन out
अन्त

# एक अग्रगमन: context -> probabilities
# E, W1, W2 सपाट (flattened) आव्यूह हैं; d, H, V, order आकार।
कार्य अग्रपरत(context, E, W1, b1, W2, b2, d, H, V, order)
    स्थापय x = []
    स्थापय c = 0
    यावत् c < order
        स्थापय tok = context[c]
        स्थापय j = 0
        यावत् j < d
            जोड़ें(x, E[tok * d + j])
            j = j + 1
        अन्त
        c = c + 1
    अन्त
    स्थापय m = order * d
    स्थापय h = []
    स्थापय r = 0
    यावत् r < H
        स्थापय acc = b1[r]
        स्थापय col = 0
        यावत् col < m
            acc = acc + W1[r * m + col] * x[col]
            col = col + 1
        अन्त
        जोड़ें(h, स्पर्शरेखा(acc))
        r = r + 1
    अन्त
    स्थापय logits = []
    स्थापय v = 0
    यावत् v < V
        स्थापय acc2 = b2[v]
        स्थापय col2 = 0
        यावत् col2 < H
            acc2 = acc2 + W2[v * H + col2] * h[col2]
            col2 = col2 + 1
        अन्त
        जोड़ें(logits, acc2)
        v = v + 1
    अन्त
    प्रत्यागमन सॉफ्टमैक्स(logits)
अन्त
'''


def _driver(call: str) -> str:
    """Program that evaluates ``call`` and stores it in ``परिणाम``."""
    return "%s\nस्थापय परिणाम = %s\n" % (SUTRA_MATH, call)


class SutraKernel:
    """Compile :data:`SUTRA_MATH` once, then call its functions from Python."""

    def __init__(self, step_limit: int = 4_000_000):
        self.step_limit = step_limit
        self._programs = {}

    def _program(self, name: str, arity: int):
        key = (name, arity)
        if key not in self._programs:
            arguments = ", ".join("आगमन[%d]" % index for index in range(arity))
            source = _driver("%s(%s)" % (name, arguments))
            self._programs[key] = compile_source(source, source_name="<sutra-math>")
        return self._programs[key]

    def call(self, name: str, *args):
        """Run ``name(*args)`` inside the ब्रह्म VM and return its value."""
        code = self._program(name, len(args))
        vm = VM(out=None, step_limit=self.step_limit, globals_={"आगमन": list(args)})
        vm.run(code)
        return vm.globals["परिणाम"]

    # -- convenient wrappers --------------------------------------------
    def exp(self, value: float) -> float:
        return self.call("घातांक", float(value))

    def softmax(self, values: Sequence[float]) -> List[float]:
        return self.call("सॉफ्टमैक्स", [float(value) for value in values])


def _flatten(matrix: Sequence[Sequence[float]]) -> List[float]:
    return [value for row in matrix for value in row]


def sutra_forward(model, context: Sequence[int]) -> List[float]:
    """Run ``model``'s forward pass on the सूत्र VM."""
    kernel = SutraKernel()
    padded = list(context)[-model.order:]
    while len(padded) < model.order:
        padded.insert(0, 0)
    return kernel.call(
        "अग्रपरत",
        [int(token) for token in padded],
        _flatten(model.E),
        _flatten(model.W1),
        list(model.b1),
        _flatten(model.W2),
        list(model.b2),
        model.d_model,
        model.hidden,
        model.vocab_size,
        model.order,
    )


def sutra_generate(model, tokenizer, prompt: str, max_tokens: int = 40,
                   temperature: float = 0.8, seed: Optional[int] = None) -> str:
    """Sample from ``model`` with every forward pass running on the सूत्र VM."""
    import random

    kernel = SutraKernel()
    flat_e, flat_w1, flat_w2 = _flatten(model.E), _flatten(model.W1), _flatten(model.W2)
    ids = tokenizer.encode(prompt) or [tokenizer.bos_id]
    generator = random.Random(seed)
    for _ in range(max_tokens):
        context = list(ids)[-model.order:]
        while len(context) < model.order:
            context.insert(0, 0)
        probs = kernel.call(
            "अग्रपरत", context, flat_e, flat_w1, list(model.b1), flat_w2, list(model.b2),
            model.d_model, model.hidden, model.vocab_size, model.order,
        )
        if temperature <= 0:
            nxt = max(range(len(probs)), key=lambda index: probs[index])
        else:
            weights = [value ** (1.0 / temperature) for value in probs]
            nxt = generator.choices(range(len(weights)), weights=weights, k=1)[0]
        if nxt == tokenizer.eos_id:
            break
        ids.append(nxt)
    return tokenizer.decode(ids)


def compare(model, context: Sequence[int]) -> dict:
    """Return the largest absolute difference between सूत्र and Python."""
    python = model.next_token_probs(context)
    sutra = sutra_forward(model, context)
    if len(python) != len(sutra):
        raise AssertionError("वेक्टर आकार भिन्न: %d बनाम %d" % (len(python), len(sutra)))
    worst = max(abs(a - b) for a, b in zip(python, sutra))
    return {"max_abs_diff": worst, "python": python, "sutra": sutra}


def self_check(samples: int = 5) -> dict:
    """End-to-end proof used by the CLI and the test suite."""
    import math
    import random

    from .model import NeuralLM

    generator = random.Random(11)
    model = NeuralLM(vocab_size=7, d_model=3, hidden=4, order=2, seed=3)
    results = []
    for _ in range(samples):
        context = [generator.randrange(model.vocab_size) for _ in range(model.order)]
        results.append(compare(model, context)["max_abs_diff"])
    kernel = SutraKernel()
    values = [1.0, 2.0, -3.0]
    top = max(values)
    weights = [math.exp(value - top) for value in values]
    reference = [value / sum(weights) for value in weights]
    return {
        "samples": samples,
        "max_abs_diff": max(results),
        "exp_check": abs(kernel.exp(1.0) - math.e),
        "softmax_check": max(abs(a - b) for a, b in zip(kernel.softmax(values), reference)),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="सूत्र-गणित प्रमाण")
    parser.add_argument("--check", action="store_true", help="समानता जाँचें")
    parser.add_argument("--json", action="store_true", help="JSON में छापें")
    args = parser.parse_args(list(argv) if argv is not None else None)

    report = self_check()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print("सूत्र-गणित जाँच")
        print("  exp(1) त्रुटि      : %.3e" % report["exp_check"])
        print("  softmax त्रुटि     : %.3e" % report["softmax_check"])
        print("  अग्रगमन अधिकतम अंतर: %.3e" % report["max_abs_diff"])
    ok = report["max_abs_diff"] < 1e-9 and report["exp_check"] < 1e-12
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
