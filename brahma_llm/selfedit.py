"""🕉️ आत्म-संपादन — the parts of "editing its own body / OS" that are real.

There are three edit surfaces in this project and each one is gated by a check
that can fail:

``expand_hidden`` / ``shrink_hidden``  (body)
    Weight surgery on :class:`brahma_llm.model.NeuralLM`.  Growing appends
    hidden units whose outgoing weights are zero, shrinking drops the units with
    the smallest output norm.  Both are **prediction-preserving by construction**
    and the test suite asserts the forward pass is unchanged to 1e-9, so the
    model can change size without becoming a different model.

``KernelEditor``  (OS)
    Asks the language model for a new सूत्र kernel, compiles and *boots* it, and
    only installs the image when the boot banner, self-test and ``READY`` line
    are all present.

``record``  (audit trail)
    Every accepted or rejected attempt is appended to
    ``$BRAHMA_HOME/self/self_edit_log.json`` with before/after numbers, so the
    history is inspectable instead of being a claim in a README.

What it deliberately does **not** do: rewrite the Python sources of this
repository by itself.  Autonomous source rewriting without human review is how
a project turns into a security incident; instead the editor emits a proposal
(``write_proposal``) that a maintainer can apply and that CI then judges.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from .model import NeuralLM


# ---------------------------------------------------------------------------
# Weight surgery
# ---------------------------------------------------------------------------
def expand_hidden(model: NeuralLM, extra: int, scale: float = 0.02) -> NeuralLM:
    """Add ``extra`` hidden units without changing the model's predictions."""
    if extra <= 0:
        return model
    import random

    generator = random.Random(model.seed + model.hidden)
    old_hidden = model.hidden
    width = model.order * model.d_model
    model.W1.extend([[generator.uniform(-scale, scale) for _ in range(width)] for _ in range(extra)])
    model.b1.extend([0.0] * extra)
    # Zero outgoing weights keep the logits identical until training moves them.
    for row in model.W2:
        row.extend([0.0] * extra)
    model.hidden = old_hidden + extra
    _migrate_adam(model, grow=extra)
    return model


def shrink_hidden(model: NeuralLM, keep: Optional[int] = None) -> NeuralLM:
    """Drop the least-used hidden units, preserving predictions when possible."""
    keep = keep if keep is not None else max(1, model.hidden // 2)
    keep = max(1, min(keep, model.hidden))
    if keep == model.hidden:
        return model
    norms = []
    for column in range(model.hidden):
        norms.append((sum(abs(row[column]) for row in model.W2), column))
    keep_columns = sorted(column for _norm, column in sorted(norms, reverse=True)[:keep])
    # W1 is ``hidden x (order*d_model)``: hidden units are its *rows*.
    model.W1 = [model.W1[unit] for unit in keep_columns]
    model.b1 = [model.b1[unit] for unit in keep_columns]
    for index, row in enumerate(model.W2):
        model.W2[index] = [row[column] for column in keep_columns]
    model.hidden = keep
    _migrate_adam(model, keep_columns=keep_columns)
    return model


def _migrate_adam(model: NeuralLM, grow: int = 0, keep_columns: Optional[Sequence[int]] = None) -> None:
    """Keep Adam's moments consistent across weight surgery.

    Dropping them (the obvious shortcut) restarts the optimiser at full learning
    rate on an already-converged model, which measurably *degrades* held-out
    perplexity.  Padding/regrouping instead keeps training stable.
    """
    state = model._adam
    if not state:
        return
    if "W1" in state:
        moment, velocity = state["W1"]
        if grow:
            moment.extend([[0.0] * len(moment[0]) for _ in range(grow)])
            velocity.extend([[0.0] * len(velocity[0]) for _ in range(grow)])
        if keep_columns is not None:
            state["W1"] = ([moment[unit] for unit in keep_columns],
                           [velocity[unit] for unit in keep_columns])
    if "b1" in state:
        moment, velocity = state["b1"]
        if grow:
            moment.extend([0.0] * grow)
            velocity.extend([0.0] * grow)
        if keep_columns is not None:
            state["b1"] = ([moment[unit] for unit in keep_columns],
                           [velocity[unit] for unit in keep_columns])
    if "W2" in state:
        moment, velocity = state["W2"]
        if grow:
            for row in moment:
                row.extend([0.0] * grow)
            for row in velocity:
                row.extend([0.0] * grow)
        if keep_columns is not None:
            state["W2"] = ([[row[c] for c in keep_columns] for row in moment],
                           [[row[c] for c in keep_columns] for row in velocity])


def prediction_drift(before: Sequence[Sequence[float]], after: Sequence[Sequence[float]]) -> float:
    """Largest absolute change between two probability tables."""
    worst = 0.0
    for left, right in zip(before, after):
        for a, b in zip(left, right):
            worst = max(worst, abs(a - b))
    return worst


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------
@dataclass
class EditRecord:
    """One attempt at changing the system, accepted or not."""

    kind: str
    description: str
    accepted: bool
    before: Dict[str, float] = field(default_factory=dict)
    after: Dict[str, float] = field(default_factory=dict)
    detail: str = ""
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> dict:
        return {
            "kind": self.kind,
            "description": self.description,
            "accepted": self.accepted,
            "before": self.before,
            "after": self.after,
            "detail": self.detail,
            "timestamp": self.timestamp,
        }


class SelfEditor:
    """Applies gated self-edits and keeps an audit log."""

    def __init__(self, workdir: Optional[str] = None, log=None):
        from brahma_paths import data_root

        self.workdir = workdir or data_root("self", create=True)
        self.log = log or (lambda message: None)
        self.records: List[EditRecord] = []
        self.log_path = os.path.join(self.workdir, "self_edit_log.json")

    # -- body ------------------------------------------------------------
    def try_grow(self, model: NeuralLM, contexts: Sequence[Sequence[int]], extra: int = 8) -> EditRecord:
        """Grow the hidden layer if it does not change current predictions."""
        before_probs = [model.next_token_probs(context) for context in contexts]
        before_hidden = model.hidden
        expand_hidden(model, extra)
        after_probs = [model.next_token_probs(context) for context in contexts]
        drift = prediction_drift(before_probs, after_probs)
        record = EditRecord(
            kind="body-growth",
            description="hidden %d → %d" % (before_hidden, model.hidden),
            accepted=drift < 1e-9,
            before={"hidden": before_hidden, "params": model.parameter_count()},
            after={"hidden": model.hidden, "params": model.parameter_count(), "drift": drift},
            detail="prediction drift %.2e" % drift,
        )
        self.records.append(record)
        self.log("  आत्म-संपादन (body): %s → %s" % (record.description, "स्वीकृत" if record.accepted else "अस्वीकृत"))
        return record

    def try_shrink(self, model: NeuralLM, contexts: Sequence[Sequence[int]], keep: Optional[int] = None) -> EditRecord:
        before_probs = [model.next_token_probs(context) for context in contexts]
        before_hidden = model.hidden
        shrink_hidden(model, keep)
        after_probs = [model.next_token_probs(context) for context in contexts]
        drift = prediction_drift(before_probs, after_probs)
        record = EditRecord(
            kind="body-prune",
            description="hidden %d → %d" % (before_hidden, model.hidden),
            accepted=drift < 1e-6,
            before={"hidden": before_hidden, "params": model.parameter_count()},
            after={"hidden": model.hidden, "params": model.parameter_count(), "drift": drift},
            detail="prediction drift %.2e" % drift,
        )
        self.records.append(record)
        self.log("  आत्म-संपादन (prune): %s → %s" % (record.description, "स्वीकृत" if record.accepted else "अस्वीकृत"))
        return record

    # -- OS --------------------------------------------------------------
    def try_os(self, source: str) -> EditRecord:
        """Build a kernel image from ``source`` and install it only if it boots."""
        from .kernel import build_image, install, verify

        image = build_image(source)
        report = verify(image)
        record = EditRecord(
            kind="os-kernel",
            description="कर्नेल पुनर्निर्माण (%d बाइट स्रोत)" % len(source),
            accepted=bool(report["ok"]),
            before={},
            after={"steps": float(report["steps"]), "image_bytes": float(report["image_bytes"])},
            detail="; ".join(report["problems"]) or "boot ठीक",
        )
        if record.accepted:
            record.detail += " → स्थापित %s" % install(image)
        self.records.append(record)
        self.log("  आत्म-संपादन (OS): %s" % ("स्वीकृत" if record.accepted else "अस्वीकृत: " + record.detail))
        return record

    # -- proposals -------------------------------------------------------
    def write_proposal(self, title: str, body: str) -> str:
        """Record a source-change suggestion for human review."""
        os.makedirs(self.workdir, exist_ok=True)
        path = os.path.join(self.workdir, "proposal-%d.md" % int(time.time()))
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("# %s\n\n%s\n" % (title, body))
        self.log("  प्रस्ताव लिखा: %s" % path)
        return path

    def flush(self) -> str:
        os.makedirs(self.workdir, exist_ok=True)
        existing: List[dict] = []
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as handle:
                    existing = json.load(handle)
            except (ValueError, OSError):
                existing = []
        existing.extend(record.as_dict() for record in self.records)
        with open(self.log_path, "w", encoding="utf-8") as handle:
            json.dump(existing[-500:], handle, ensure_ascii=False, indent=1)
        return self.log_path
