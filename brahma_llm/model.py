"""🕉️ ब्रह्म-LLM के मॉडल — two language models, implemented from scratch.

Nothing here is a wrapper around somebody else's checkpoint: there is no
``torch``, no ``numpy``, no downloaded weights.  The package ships two
trainable models that share one interface:

``NgramLM``
    Interpolated Jelinek–Mercer n-gram model.  Trains in milliseconds, so it is
    the baseline every neural run is compared against.

``NeuralLM``
    A real neural language model — embedding lookup, tanh hidden layer, softmax
    output, hand-written backpropagation and Adam.  The gradients are verified
    against central differences in ``tests/test_llm.py``, so "it learns" is a
    measured claim rather than a hope.

Both expose ``fit`` / ``loss`` / ``perplexity`` / ``next_token_probs`` and are
serialised to plain JSON, which keeps checkpoints diff-able and the project
dependency-free.

Honest sizing note: the *architecture* scales with ``hidden``/``d_model``/
``order``; the presets in :data:`PRESETS` trade training time for capacity, and
:meth:`BrahmaLLM.info` always reports the counted parameter total.  See
``docs/LLM.md`` for measured numbers.
"""

from __future__ import annotations

import json
import math
import random
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .tokenizer import SutraTokenizer

#: (d_model, hidden, order, epochs) presets.  Bigger is slower, not automatically
#: better — the trainer keeps whichever checkpoint actually wins on held-out text.
PRESETS: Dict[str, Dict[str, int]] = {
    "tiny": {"d_model": 8, "hidden": 32, "order": 2, "epochs": 6, "max_vocab": 96},
    "small": {"d_model": 16, "hidden": 64, "order": 3, "epochs": 8, "max_vocab": 160},
    "medium": {"d_model": 24, "hidden": 128, "order": 4, "epochs": 10, "max_vocab": 256},
    "large": {"d_model": 32, "hidden": 192, "order": 5, "epochs": 12, "max_vocab": 384},
    # Beyond this point the cost is *interpreted Python*, not memory: every
    # multiply-add is a CPython operation, so these presets are honest
    # statements of scale, not claims of speed.  See docs/LLM.md §9.
    "xlarge": {"d_model": 48, "hidden": 384, "order": 6, "epochs": 14, "max_vocab": 512},
    "huge": {"d_model": 64, "hidden": 768, "order": 8, "epochs": 16, "max_vocab": 768},
    "brahma": {"d_model": 96, "hidden": 1536, "order": 10, "epochs": 18, "max_vocab": 1024},
}


def _softmax(logits: Sequence[float]) -> List[float]:
    top = max(logits)
    exps = [math.exp(value - top) for value in logits]
    total = sum(exps)
    return [value / total for value in exps]


class LanguageModel:
    """Interface shared by :class:`NgramLM` and :class:`NeuralLM`."""

    kind = "base"

    def fit(self, sequences: Iterable[Sequence[int]]) -> "LanguageModel":  # pragma: no cover - interface
        raise NotImplementedError

    def next_token_probs(self, context: Sequence[int]) -> List[float]:  # pragma: no cover - interface
        raise NotImplementedError

    def loss(self, sequences: Iterable[Sequence[int]]) -> float:
        """Mean negative log-likelihood per predicted token (lower is better)."""
        total, count = 0.0, 0
        for sequence in sequences:
            for index in range(1, len(sequence)):
                context = sequence[max(0, index - self.order): index]
                probs = self.next_token_probs(context)
                target = sequence[index]
                probability = probs[target] if target < len(probs) else 0.0
                total -= math.log(max(probability, 1e-12))
                count += 1
        return total / count if count else 0.0

    def perplexity(self, sequences: Iterable[Sequence[int]]) -> float:
        return math.exp(self.loss(sequences))

    @property
    def order(self) -> int:  # pragma: no cover - overridden
        return 1

    def generate(
        self,
        tokenizer: SutraTokenizer,
        prompt: str,
        max_tokens: int = 80,
        temperature: float = 0.9,
        seed: Optional[int] = None,
        stop_at_eos: bool = True,
    ) -> str:
        """Sample a continuation for ``prompt``."""
        generator = random.Random(seed)
        ids = tokenizer.encode(prompt)
        if not ids:
            ids = [tokenizer.bos_id]
        for _ in range(max_tokens):
            context = ids[-self.order:]
            probs = self.next_token_probs(context)
            if temperature <= 0:
                nxt = max(range(len(probs)), key=lambda index: probs[index])
            else:
                weights = [value ** (1.0 / temperature) for value in probs]
                nxt = generator.choices(range(len(weights)), weights=weights, k=1)[0]
            if stop_at_eos and nxt == tokenizer.eos_id:
                break
            ids.append(nxt)
        return tokenizer.decode(ids)

    def to_dict(self) -> dict:  # pragma: no cover - interface
        raise NotImplementedError

    def parameter_count(self) -> int:
        return 0


class NgramLM(LanguageModel):
    """Jelinek–Mercer interpolated n-gram model with add-k smoothing."""

    kind = "ngram"

    def __init__(self, order: int = 3, vocab_size: int = 0, interpolate: float = 0.6, add_k: float = 0.2):
        self._order = max(1, int(order))
        self.vocab_size = max(1, int(vocab_size))
        self.interpolate = float(interpolate)
        self.add_k = float(add_k)
        self.counts: List[Dict[Tuple[int, ...], Dict[int, int]]] = [{} for _ in range(self._order + 1)]
        self.context_counts: List[Dict[Tuple[int, ...], int]] = [{} for _ in range(self._order + 1)]
        self.unigram: Dict[int, int] = {}
        self.total = 0
        self._cache: Dict[Tuple[int, ...], List[float]] = {}

    @property
    def order(self) -> int:
        return self._order

    def fit(self, sequences: Iterable[Sequence[int]], vocab_size: Optional[int] = None) -> "NgramLM":
        if vocab_size:
            self.vocab_size = int(vocab_size)
        for sequence in sequences:
            padded = list(sequence)
            for index in range(1, len(padded)):
                target = padded[index]
                self.unigram[target] = self.unigram.get(target, 0) + 1
                self.total += 1
                for size in range(1, self._order + 1):
                    if index - size < 0:
                        continue
                    context = tuple(padded[index - size: index])
                    bucket = self.counts[size].setdefault(context, {})
                    bucket[target] = bucket.get(target, 0) + 1
                    self.context_counts[size][context] = self.context_counts[size].get(context, 0) + 1
        self._cache.clear()
        return self

    def _unigram_probs(self) -> List[float]:
        denominator = self.total + self.add_k * self.vocab_size
        return [
            (self.unigram.get(token, 0) + self.add_k) / denominator
            for token in range(self.vocab_size)
        ]

    def next_token_probs(self, context: Sequence[int]) -> List[float]:
        key = tuple(context)
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        distribution = self._unigram_probs()
        for size in range(1, min(self._order, len(context)) + 1):
            sub = tuple(context[-size:])
            bucket = self.counts[size].get(sub)
            if not bucket:
                continue
            observed = self.context_counts[size].get(sub, 0)
            denominator = observed + self.add_k * self.vocab_size
            higher = [(bucket.get(token, 0) + self.add_k) / denominator for token in range(self.vocab_size)]
            weight = self.interpolate
            distribution = [(1.0 - weight) * distribution[token] + weight * higher[token]
                            for token in range(self.vocab_size)]
        self._cache[key] = distribution
        return distribution

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "order": self._order,
            "vocab_size": self.vocab_size,
            "interpolate": self.interpolate,
            "add_k": self.add_k,
            "unigram": [[token, count] for token, count in sorted(self.unigram.items())],
            "counts": [
                [[list(context), sorted(bucket.items())] for context, bucket in size.items()]
                for size in self.counts
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NgramLM":
        model = cls(order=data["order"], vocab_size=data["vocab_size"],
                    interpolate=data.get("interpolate", 0.6), add_k=data.get("add_k", 0.2))
        model.unigram = {int(token): int(count) for token, count in data.get("unigram", [])}
        model.total = sum(model.unigram.values())
        for size, entries in enumerate(data.get("counts", [])):
            for context, bucket in entries:
                model.counts[size][tuple(int(value) for value in context)] = {
                    int(token): int(count) for token, count in bucket
                }
                model.context_counts[size][tuple(int(value) for value in context)] = sum(
                    model.counts[size][tuple(int(value) for value in context)].values()
                )
        return model

    def parameter_count(self) -> int:
        return sum(len(bucket) for size in self.counts for bucket in size.values()) + len(self.unigram)


class NeuralLM(LanguageModel):
    """Embedding → tanh hidden → softmax, with hand-written gradients + Adam."""

    kind = "neural"

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 16,
        hidden: int = 64,
        order: int = 3,
        seed: int = 7,
        init_scale: float = 0.1,
        learning_rate: float = 0.02,
    ):
        self.vocab_size = int(vocab_size)
        self.d_model = int(d_model)
        self.hidden = int(hidden)
        self._order = max(1, int(order))
        self.seed = int(seed)
        self.learning_rate = float(learning_rate)
        self.steps = 0
        generator = random.Random(seed)
        scale = init_scale
        self.E = [[generator.uniform(-scale, scale) for _ in range(self.d_model)]
                  for _ in range(self.vocab_size)]
        # A small deterministic bias in the output layer breaks the symmetry
        # between classes without making the initial distribution peaked.
        self.W1 = [[generator.uniform(-scale, scale) for _ in range(self.order * self.d_model)]
                   for _ in range(self.hidden)]
        self.b1 = [0.0] * self.hidden
        self.W2 = [[generator.uniform(-scale, scale) * 0.5 for _ in range(self.hidden)]
                   for _ in range(self.vocab_size)]
        self.b2 = [0.0] * self.vocab_size
        self.epoch_losses: List[float] = []
        self._adam: Dict[str, List] = {}

    # -- helpers ---------------------------------------------------------
    @property
    def order(self) -> int:
        return self._order

    def _context_vector(self, context: Sequence[int]) -> List[float]:
        vector: List[float] = []
        padded = list(context)[-self.order:]
        while len(padded) < self.order:
            padded.insert(0, 0)
        for token in padded:
            vector.extend(self.E[token % self.vocab_size])
        return vector

    def _forward(self, context: Sequence[int]) -> Tuple[List[float], List[float], List[float]]:
        x = self._context_vector(context)
        W1, b1 = self.W1, self.b1
        hidden_pre = [b1[row] for row in range(self.hidden)]
        for row in range(self.hidden):
            weights = W1[row]
            total = hidden_pre[row]
            for column, value in enumerate(x):
                total += weights[column] * value
            hidden_pre[row] = total
        h = [math.tanh(value) for value in hidden_pre]
        logits = [self.b2[row] for row in range(self.vocab_size)]
        for row in range(self.vocab_size):
            weights = self.W2[row]
            total = logits[row]
            for column, value in enumerate(h):
                total += weights[column] * value
            logits[row] = total
        return x, h, logits

    def next_token_probs(self, context: Sequence[int]) -> List[float]:
        _x, _h, logits = self._forward(context)
        return _softmax(logits)

    # -- learning --------------------------------------------------------
    def _accumulate(self, context: Sequence[int], target: int, grads: Dict[str, List]) -> float:
        x, h, logits = self._forward(context)
        probs = _softmax(logits)
        loss = -math.log(max(probs[target], 1e-12))

        dlogits = list(probs)
        dlogits[target] -= 1.0

        dW2 = grads["W2"]
        db2 = grads["b2"]
        for row in range(self.vocab_size):
            delta = dlogits[row]
            if -1e-7 < delta < 1e-7:
                continue
            db2[row] += delta
            weights = dW2[row]
            for column in range(self.hidden):
                weights[column] += delta * h[column]

        dh = [0.0] * self.hidden
        for row in range(self.vocab_size):
            delta = dlogits[row]
            if -1e-7 < delta < 1e-7:
                continue
            weights = self.W2[row]
            for column in range(self.hidden):
                dh[column] += weights[column] * delta

        dpre = [dh[row] * (1.0 - h[row] * h[row]) for row in range(self.hidden)]

        dW1 = grads["W1"]
        db1 = grads["b1"]
        for row in range(self.hidden):
            delta = dpre[row]
            if delta == 0.0:
                continue
            db1[row] += delta
            weights = dW1[row]
            for column in range(len(x)):
                weights[column] += delta * x[column]

        dx = [0.0] * len(x)
        for row in range(self.hidden):
            delta = dpre[row]
            if delta == 0.0:
                continue
            weights = self.W1[row]
            for column in range(len(x)):
                dx[column] += weights[column] * delta

        dE = grads["E"]
        padded = list(context)[-self.order:]
        while len(padded) < self.order:
            padded.insert(0, 0)
        for position, token in enumerate(padded):
            row = dE[token % self.vocab_size]
            base = position * self.d_model
            for column in range(self.d_model):
                row[column] += dx[base + column]
        return loss

    def _empty_grads(self) -> Dict[str, List]:
        return {
            "E": [[0.0] * self.d_model for _ in range(self.vocab_size)],
            "W1": [[0.0] * (self.order * self.d_model) for _ in range(self.hidden)],
            "b1": [0.0] * self.hidden,
            "W2": [[0.0] * self.hidden for _ in range(self.vocab_size)],
            "b2": [0.0] * self.vocab_size,
        }

    def loss_and_grads(self, examples: Sequence[Tuple[Sequence[int], int]]) -> Tuple[float, Dict[str, List]]:
        """Mean loss and gradients for ``(context, target)`` pairs.

        Exposed (rather than private) because ``tests/test_llm.py`` checks these
        gradients against central differences.
        """
        grads = self._empty_grads()
        total = 0.0
        for context, target in examples:
            total += self._accumulate(context, target, grads)
        scale = 1.0 / max(1, len(examples))
        for key, value in grads.items():
            if isinstance(value[0], list):
                for row in value:
                    for index in range(len(row)):
                        row[index] *= scale
            else:
                for index in range(len(value)):
                    value[index] *= scale
        return total * scale, grads

    def _adam_update(self, name: str, parameter, gradient, beta1: float = 0.9, beta2: float = 0.999,
                     epsilon: float = 1e-8) -> None:
        state = self._adam.get(name)
        if state is None:
            if isinstance(parameter[0], list):
                m = [[0.0] * len(row) for row in parameter]
                v = [[0.0] * len(row) for row in parameter]
            else:
                m = [0.0] * len(parameter)
                v = [0.0] * len(parameter)
            state = self._adam[name] = [m, v]
        m, v = state
        step = self.steps
        correction1 = 1.0 - beta1 ** step
        correction2 = 1.0 - beta2 ** step
        rate = self.learning_rate * math.sqrt(correction2) / correction1
        if isinstance(parameter[0], list):
            for row_index, row in enumerate(parameter):
                mrow, vrow, grow = m[row_index], v[row_index], gradient[row_index]
                for index in range(len(row)):
                    g = grow[index]
                    mrow[index] = beta1 * mrow[index] + (1.0 - beta1) * g
                    vrow[index] = beta2 * vrow[index] + (1.0 - beta2) * g * g
                    row[index] -= rate * mrow[index] / (math.sqrt(vrow[index]) + epsilon)
        else:
            for index in range(len(parameter)):
                g = gradient[index]
                m[index] = beta1 * m[index] + (1.0 - beta1) * g
                v[index] = beta2 * v[index] + (1.0 - beta2) * g * g
                parameter[index] -= rate * m[index] / (math.sqrt(v[index]) + epsilon)

    def fit(
        self,
        sequences: Iterable[Sequence[int]],
        epochs: int = 20,
        batch_size: int = 16,
        shuffle: bool = True,
        seed: Optional[int] = None,
        on_epoch=None,
        max_examples: Optional[int] = None,
    ) -> "NeuralLM":
        """Train on id sequences; ``on_epoch(epoch, mean_loss)`` is called each pass."""
        examples: List[Tuple[Sequence[int], int]] = []
        for sequence in sequences:
            for index in range(1, len(sequence)):
                examples.append((sequence[max(0, index - self.order): index], sequence[index]))
        if not examples:
            return self
        rng = random.Random(self.seed if seed is None else seed)
        for epoch in range(epochs):
            order = list(range(len(examples)))
            if shuffle:
                rng.shuffle(order)
            if max_examples and len(order) > max_examples:
                order = order[:max_examples]
            epoch_loss = 0.0
            for start in range(0, len(order), batch_size):
                batch = [examples[index] for index in order[start:start + batch_size]]
                self.steps += 1
                loss, grads = self.loss_and_grads(batch)
                epoch_loss += loss * len(batch)
                for name, parameter in (("E", self.E), ("W1", self.W1), ("b1", self.b1),
                                        ("W2", self.W2), ("b2", self.b2)):
                    self._adam_update(name, parameter, grads[name])
            self.epoch_losses.append(epoch_loss / len(examples))
            if on_epoch is not None:
                on_epoch(epoch, self.epoch_losses[-1])
        return self

    # -- persistence -----------------------------------------------------
    def parameter_count(self) -> int:
        vectors = [self.E, self.W1, self.W2]
        return sum(len(row) for group in vectors for row in group) + len(self.b1) + len(self.b2)

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "vocab_size": self.vocab_size,
            "d_model": self.d_model,
            "hidden": self.hidden,
            "order": self._order,
            "seed": self.seed,
            "learning_rate": self.learning_rate,
            "steps": self.steps,
            "E": self.E,
            "W1": self.W1,
            "b1": self.b1,
            "W2": self.W2,
            "b2": self.b2,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NeuralLM":
        model = cls(
            vocab_size=data["vocab_size"],
            d_model=data.get("d_model", 16),
            hidden=data.get("hidden", 64),
            order=data.get("order", 3),
            seed=data.get("seed", 7),
            learning_rate=data.get("learning_rate", 0.02),
        )
        model.E = data["E"]
        model.W1 = data["W1"]
        model.b1 = data["b1"]
        model.W2 = data["W2"]
        model.b2 = data["b2"]
        model.steps = data.get("steps", 0)
        return model


def build_model(kind: str, vocab_size: int, size: str = "small", seed: int = 7) -> LanguageModel:
    """Factory used by the CLI and the autonomous trainer."""
    preset = PRESETS.get(size, PRESETS["small"])
    if kind == "ngram":
        return NgramLM(order=min(preset["order"], 4), vocab_size=vocab_size)
    if kind == "neural":
        return NeuralLM(
            vocab_size=vocab_size,
            d_model=preset["d_model"],
            hidden=preset["hidden"],
            order=min(preset["order"], 5),
            seed=seed,
        )
    raise ValueError("अज्ञात मॉडल प्रकार %r (ngram या neural चुनें)" % (kind,))


class BrahmaLLM:
    """Tokenizer + model + metadata: the object the CLI, apps and trainer share."""

    def __init__(self, model: LanguageModel, tokenizer: SutraTokenizer, size: str = "small",
                 corpus_note: str = ""):
        self.kind = model.kind
        self.seed = getattr(model, "seed", 7)
        self.model = model
        self.tokenizer = tokenizer
        self.size = size
        self.corpus_note = corpus_note
        self.history: List[Dict[str, float]] = []

    # -- construction ----------------------------------------------------
    @classmethod
    def create(cls, kind: str = "neural", size: str = "small", min_count: int = 1,
               max_vocab: int = 512, seed: int = 7) -> "BrahmaLLM":
        tokenizer = SutraTokenizer(min_count=min_count, max_vocab=max_vocab)
        model = build_model(kind, len(tokenizer), size=size, seed=seed)
        return cls(model, tokenizer, size=size)

    # -- training --------------------------------------------------------
    def fit(self, texts: Sequence[str], epochs: Optional[int] = None, batch_size: int = 16,
            on_epoch=None, max_examples: Optional[int] = 1200) -> "BrahmaLLM":
        preset = PRESETS.get(self.size, PRESETS["small"])
        self.tokenizer.max_vocab = min(self.tokenizer.max_vocab, preset.get("max_vocab", 4096))
        self.tokenizer.fit(texts)
        sequences = [self.tokenizer.encode(text, add_special=True) for text in texts]
        epochs = preset["epochs"] if epochs is None else epochs
        self.model = build_model(self.kind, self.tokenizer.vocab_size, self.size, seed=self.seed)
        if isinstance(self.model, NeuralLM):
            self.model.fit(sequences, epochs=epochs, batch_size=batch_size, on_epoch=on_epoch,
                           max_examples=max_examples)
            self.history.extend(self.model.epoch_losses[-5:])
        else:
            self.model.fit(sequences, vocab_size=self.tokenizer.vocab_size)
        return self

    def continue_training(self, texts: Sequence[str], epochs: int = 4, batch_size: int = 16,
                          max_examples: Optional[int] = 800,
                          learning_rate: Optional[float] = None) -> "BrahmaLLM":
        """Warm-start training with the *current* vocabulary (unseen → ``<unk>``).

        ``learning_rate`` lets the trainer anneal the step size between rounds;
        the default keeps the model's own rate.
        """
        sequences = [self.tokenizer.encode(text, add_special=True) for text in texts]
        if isinstance(self.model, NeuralLM):
            if learning_rate is not None:
                self.model.learning_rate = float(learning_rate)
            self.model.fit(sequences, epochs=epochs, batch_size=batch_size, max_examples=max_examples)
            self.history.extend(self.model.epoch_losses[-3:])
        else:
            self.model.fit(sequences, vocab_size=self.tokenizer.vocab_size)
        return self

    def score(self, text: str) -> float:
        """Cross-entropy of ``text`` under this model (lower = more natural).

        Used as a *ranker*: several candidate सूत्र programs are generated, and
        the one the model finds most likely wins.  That is the honest version of
        "the model writes the code" at this model size — see docs/LLM.md §6.8.
        """
        report = self.evaluate([text])
        return float(report["loss"])

    def evaluate(self, texts: Sequence[str]) -> Dict[str, float]:
        sequences = [self.tokenizer.encode(text, add_special=True) for text in texts]
        loss = self.model.loss(sequences)
        return {"loss": loss, "perplexity": math.exp(loss), "tokens": sum(len(s) for s in sequences)}

    # -- generation ------------------------------------------------------
    def generate(self, prompt: str, max_tokens: int = 80, temperature: float = 0.9,
                 seed: Optional[int] = None) -> str:
        return self.model.generate(self.tokenizer, prompt, max_tokens=max_tokens,
                                   temperature=temperature, seed=seed)

    def complete_program(self, prompt: str, max_tokens: int = 120, seed: Optional[int] = None) -> str:
        """Generate a सूत्र program and keep the longest syntactically valid prefix."""
        from brahma.api import execute  # local import: keeps this module import-light

        text = self.generate(prompt, max_tokens=max_tokens, temperature=0.7, seed=seed)
        lines = text.splitlines()
        best = ""
        for end in range(len(lines), 0, -1):
            candidate = "\n".join(lines[:end]).rstrip()
            if not candidate.strip():
                continue
            probe = execute(candidate, source_name="<llm>", step_limit=20_000)
            if probe.error is None:
                return candidate + "\n" if not candidate.endswith("\n") else candidate
            best = best or candidate
        return best

    # -- introspection / persistence -------------------------------------
    def info(self) -> Dict[str, object]:
        return {
            "kind": self.model.kind,
            "size": self.size,
            "params": self.model.parameter_count(),
            "vocab_size": self.tokenizer.vocab_size,
            "order": self.model.order,
            "d_model": getattr(self.model, "d_model", None),
            "hidden": getattr(self.model, "hidden", None),
            "corpus": self.corpus_note,
            "history": self.history[-5:],
        }

    def save(self, directory: str) -> str:
        import os

        os.makedirs(directory, exist_ok=True)
        self.tokenizer.save(os.path.join(directory, "tokenizer.json"))
        with open(os.path.join(directory, "model.json"), "w", encoding="utf-8") as handle:
            json.dump(self.model.to_dict(), handle, ensure_ascii=False)
        with open(os.path.join(directory, "meta.json"), "w", encoding="utf-8") as handle:
            json.dump({"size": self.size, "corpus_note": self.corpus_note, "history": self.history},
                      handle, ensure_ascii=False, indent=1)
        return directory

    @classmethod
    def load(cls, directory: str) -> "BrahmaLLM":
        import os

        tokenizer = SutraTokenizer.load(os.path.join(directory, "tokenizer.json"))
        with open(os.path.join(directory, "model.json"), "r", encoding="utf-8") as handle:
            data = json.load(handle)
        model = NeuralLM.from_dict(data) if data.get("kind") == "neural" else NgramLM.from_dict(data)
        meta = {}
        meta_path = os.path.join(directory, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as handle:
                meta = json.load(handle)
        instance = cls(model, tokenizer, size=meta.get("size", "small"),
                       corpus_note=meta.get("corpus_note", ""))
        instance.history = meta.get("history", [])
        return instance
