"""🕉️ ब्रह्म-LLM as the product: chat, code, action, image — one agent.

There is no "app builder" in this package any more.  The model itself is the
thing you talk to, and every capability is a real action executed here:

===============  ==================================================================
intent           what actually happens
===============  ==================================================================
``chat``         the model continues the conversation; the reply is model output
``code``         candidate सूत्र programs are generated, **ranked by the model**, the
                 winner is compiled and executed on the सूत्र VM, and its output is
                 returned with the source
``run``          सूत्र source extracted from the message is executed on the VM
``explain``      the program is parsed and reported structurally (functions,
                 loops, builtins, lines) — deterministic, not invented
``image``        the model writes a सूत्र program, the VM runs it, and its numbers
                 plus the model's distribution drive a procedural PNG renderer
``status``       model, kernel, corpus and last mission, all measured
``help``         the capability table above
===============  ==================================================================

Honesty rules baked in:

* every reply carries a ``trace`` of what was executed (program, output, error);
* when free generation produces nothing runnable, the returned program is either
  a **model-ranked** valid candidate (``origin: "ranked"``) or the caller is told
  ``origin: "none"`` — never a silent substitution;
* the ranking is the model's own loss on ``prompt + candidate``, so it is the
  model making the choice, not a keyword match.

See ``docs/LLM.md`` §6.8 for the measured behaviour.
"""

from __future__ import annotations

import os
import re
from typing import Dict, List, Optional

from .programs import ProgramGenerator

CODE_PROMPT = "# लक्ष्य: %s\n"
MAX_PROGRAMS = 12

_SUTRA_HINTS = ("दर्शय", "स्थापय", "यावत्", "कार्य", "प्रत्यागमन", "यदि", "अन्त")
_IMAGE_WORDS = ("चित्र", "image", "draw", "picture", "png", "तस्वीर", "रंग")
_RUN_WORDS = ("चलाओ", "run", "execute", "निष्पादन")
_CODE_WORDS = ("कोड", "code", "लिखो", "write", "कार्यक्रम", "program", "function", "फलन")
_EXPLAIN_WORDS = ("समझाओ", "explain", "विश्लेषण", "analyse", "analyze")
_STATUS_WORDS = ("स्थिति", "status", "मॉडल", "kernel", "कर्नेल", "mission")
_HELP_WORDS = ("सहायता", "help", "क्या कर सकते", "capabilities")


def detect_intent(message: str) -> str:
    """Classify a message into one of the agent's real capabilities."""
    text = (message or "").strip()
    lowered = text.lower()
    if not text:
        return "help"
    if any(word in lowered for word in _HELP_WORDS):
        return "help"
    if any(word in text for word in _SUTRA_HINTS) and len(text.splitlines()) >= 1:
        if any(word in lowered for word in _RUN_WORDS):
            return "run"
        if any(word in lowered for word in _EXPLAIN_WORDS):
            return "explain"
        if text.lstrip().startswith(("दर्शय", "स्थापय", "कार्य", "यदि", "यावत्")):
            return "run"
    if any(word in lowered for word in _IMAGE_WORDS):
        return "image"
    if any(word in lowered for word in _EXPLAIN_WORDS):
        return "explain"
    if any(word in lowered for word in _CODE_WORDS):
        return "code"
    if any(word in lowered for word in _STATUS_WORDS):
        return "status"
    return "chat"


def _candidates(goal: str, seed: int, count: int = MAX_PROGRAMS) -> List:
    """Valid programs for ``goal``: goal-filtered first, then every template.

    The filter is deterministic (goal words → categories); the *choice inside*
    the set is the model's, via :meth:`brahma_llm.model.BrahmaLLM.score`.
    """
    generator = ProgramGenerator(seed=seed)
    relevant = generator.categories_for(goal)
    template_names = relevant if relevant else list(generator.templates)
    found = []
    for index in range(count):
        name = template_names[index % len(template_names)]
        generator = ProgramGenerator(seed=seed * 31 + index)
        source = generator.templates[name]()
        from .programs import validate_program

        candidate = validate_program(source)
        candidate.category = name
        if candidate.ok:
            found.append(candidate)
    return found


def synthesize(goal: str, model=None, seed: int = 7) -> Dict[str, object]:
    """Write a program for ``goal``: generate → model ranks → execute.

    Returns a dict with ``source``, ``category``, ``origin`` (``ranked``,
    ``generated`` or ``none``), ``output``, ``error`` and the ranking table, so a
    caller can see exactly why this program was chosen.
    """
    from brahma.api import execute

    prompt = CODE_PROMPT % goal
    candidates = _candidates(goal, seed)
    ranking = []
    if model is not None and candidates:
        scored = []
        for candidate in candidates:
            try:
                loss = model.score(prompt + candidate.source)
            except Exception:  # noqa: BLE001 - unscored candidates go last
                loss = float("inf")
            scored.append((loss, candidate))
            ranking.append({"category": candidate.category, "loss": round(loss, 4)})
        scored.sort(key=lambda item: item[0])
        chosen = scored[0][1]
        origin = "ranked"
    elif candidates:
        chosen = candidates[0]
        origin = "generated"
    else:
        return {"source": "", "category": "", "origin": "none", "output": [],
                "error": "कोई वैध कार्यक्रम नहीं बना", "ranking": ranking}

    free = ""
    if model is not None:
        try:
            free = model.complete_program(prompt, max_tokens=80, seed=seed)
        except Exception:  # noqa: BLE001 - free generation is a bonus, not a gate
            free = ""
    report = execute(chosen.source, source_name="<agent>", step_limit=200_000)
    result = {
        "source": chosen.source,
        "category": chosen.category,
        "origin": origin,
        "output": list(report.output),
        "error": None if report.error is None else str(report.error),
        "steps": report.steps,
        "ranking": ranking[:6],
        "free_generation": free,
        "free_generation_runs": False,
    }
    if free.strip():
        try:
            probe = execute(free, source_name="<agent-free>", step_limit=20_000)
            result["free_generation_runs"] = probe.error is None and bool(probe.output)
        except Exception:  # noqa: BLE001 - reported as False
            result["free_generation_runs"] = False
    return result


def _extract_program(message: str) -> str:
    """Pull सूत्र source out of a message (fenced block, or the lines themselves)."""
    fenced = re.search(r"```(?:sutra|सूत्र)?\s*(.+?)```", message, re.S)
    if fenced:
        return fenced.group(1).strip()
    lines = [line for line in message.splitlines()]
    kept = []
    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(hint) for hint in _SUTRA_HINTS) or line.startswith((" ", "\t")):
            kept.append(line)
        elif kept and stripped == "":
            continue
    return "\n".join(kept).strip()


def explain(source: str) -> Dict[str, object]:
    """Structural, truthful description of a सूत्र program."""
    from brahma.bytecode import OPCODES
    from brahma.compiler import compile_source
    from brahma.parser import parse

    report: Dict[str, object] = {"ok": False, "lines": len(source.splitlines()), "error": None}
    try:
        program = parse(source, "<explain>")
        code = compile_source(source, source_name="<explain>")
    except Exception as error:  # noqa: BLE001 - reported verbatim
        report["error"] = "%s: %s" % (type(error).__name__, error)
        return report
    functions = []
    depth = 0
    maximum = 0
    for statement in program.statements:
        name = type(statement).__name__
        if name == "FuncDef":
            functions.append({"name": statement.name, "params": list(statement.params),
                              "statements": len(statement.body)})
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.endswith(("अन्त", "else", "अन्यथा")):
            depth = max(0, depth - 1)
        maximum = max(maximum, depth)
        if stripped.endswith(("अन्त", "else", "अन्यथा")) is False and stripped in ("",):
            continue
        if any(stripped.startswith(word) for word in ("यदि", "यावत्", "कार्य")) or stripped.endswith("अन्यथा"):
            depth += 1
    opnames = {instruction.op for instruction in code.instructions}
    report.update({
        "ok": True,
        "statements": len(program.statements),
        "functions": functions,
        "nesting": maximum,
        "bytecode_instructions": len(code.instructions),
        "opcodes": sorted(opnames & set(OPCODES)),
        "loops": source.count("यावत्"),
        "conditionals": source.count("यदि"),
    })
    return report


class BrahmaAgent:
    """The model plus the tools it is allowed to use.  One object, one API."""

    def __init__(self, model=None, checkpoint: Optional[str] = None, seed: int = 7):
        if model is None and checkpoint:
            from .model import BrahmaLLM

            model = BrahmaLLM.load(checkpoint)
        self.model = model
        self.seed = seed
        self.history: List[Dict[str, str]] = []

    # -- individual capabilities -----------------------------------------
    def chat(self, message: str) -> Dict[str, object]:
        text = ""
        if self.model is not None:
            try:
                text = self.model.generate(message, max_tokens=60, temperature=0.8, seed=self.seed)
            except Exception as error:  # noqa: BLE001 - reported in the trace
                text = ""
                self.history.append({"error": str(error)})
        reply = text.strip()
        if not reply:
            reply = ("मेरे पास इस समय प्रशिक्षित चेकपॉइंट नहीं है। "
                     "`brahma llm train` या `brahma llm mission` चलाएँ, फिर पूछें।")
        return {"intent": "chat", "text": reply, "model_output": bool(text.strip())}

    def code(self, goal: str) -> Dict[str, object]:
        result = synthesize(goal, self.model, seed=self.seed)
        summary = []
        if result["source"]:
            summary.append("🕉️ सूत्र कार्यक्रम (%s, %s):" % (result["category"], result["origin"]))
            summary.append(result["source"])
            if result["error"]:
                summary.append("त्रुटि: %s" % result["error"])
            else:
                summary.append("आउटपुट: %s" % ", ".join(result["output"][:8]))
        else:
            summary.append("कोई कार्यक्रम नहीं बना")
        return {"intent": "code", "text": "\n".join(summary), **result}

    def run(self, message: str) -> Dict[str, object]:
        from brahma.api import execute

        source = _extract_program(message)
        if not source:
            synthesised = synthesize(message, self.model, seed=self.seed)
            source = synthesised["source"]
            origin = synthesised["origin"]
        else:
            origin = "message"
        if not source:
            return {"intent": "run", "text": "चलाने के लिए कोई सूत्र कोड नहीं मिला",
                    "origin": origin, "output": [], "error": "no code"}
        report = execute(source, source_name="<agent-run>", step_limit=200_000)
        lines = ["🕉️ सूत्र निष्पादन (%s):" % origin, source]
        if report.error is None:
            lines.append("आउटपुट: %s" % ", ".join(report.output[:20]))
        else:
            lines.append("त्रुटि: %s" % report.error)
        return {"intent": "run", "text": "\n".join(lines), "source": source,
                "origin": origin, "output": list(report.output),
                "error": None if report.error is None else str(report.error),
                "steps": report.steps}

    def explain(self, message: str) -> Dict[str, object]:
        source = _extract_program(message)
        if not source:
            synthesised = synthesize(message, self.model, seed=self.seed)
            source = synthesised["source"]
        report = explain(source)
        if not report["ok"]:
            return {"intent": "explain", "text": "विश्लेषण विफल: %s" % report["error"],
                    "source": source, "report": report}
        text = [
            "🕉️ संरचना: %d कथन, %d बाइटकोड निर्देश, %d फलन, अधिकतम नेस्टिंग %d"
            % (report["statements"], report["bytecode_instructions"],
               len(report["functions"]), report["nesting"]),
            "चक्र: %d, शर्तें: %d" % (report["loops"], report["conditionals"]),
        ]
        for function in report["functions"]:
            text.append("  कार्य %s(%s): %d कथन"
                        % (function["name"], ", ".join(function["params"]), function["statements"]))
        return {"intent": "explain", "text": "\n".join(text), "source": source,
                "report": report}

    def image(self, prompt: str, path: Optional[str] = None) -> Dict[str, object]:
        from .image import generate

        meta = generate(prompt, self.model, path=path)
        text = ("🕉️ चित्र: %s (%d×%d, %d बाइट)\nक्रम: %s\nस्रोत: %s"
                % (meta["path"], meta["size"][0], meta["size"][1],
                   os.path.getsize(meta["path"]), meta["engine"], meta["origin"]))
        return {"intent": "image", "text": text, **meta}

    def status(self) -> Dict[str, object]:
        from .kernel import verify

        kernel = verify()
        info: Dict[str, object] = {
            "intent": "status",
            "kernel": {"ok": kernel["ok"], "steps": kernel["steps"],
                       "image_bytes": kernel["image_bytes"]},
            "model": None,
        }
        if self.model is not None:
            info["model"] = self.model.info()
        try:
            from .mission import last_mission

            info["mission"] = last_mission()
        except Exception:  # noqa: BLE001 - optional
            info["mission"] = None
        lines = ["🕉️ स्थिति"]
        if info["model"]:
            lines.append("  मॉडल: %s / %s, %s पैरामीटर"
                         % (info["model"]["kind"], info["model"]["size"],
                            info["model"]["params"]))
        else:
            lines.append("  मॉडल: कोई चेकपॉइंट नहीं")
        lines.append("  कर्नेल: %s (%d चरण)" % ("ठीक" if kernel["ok"] else "विफल", kernel["steps"]))
        if info["mission"]:
            lines.append("  पिछला मिशन: %s — ppl %s"
                         % (info["mission"]["target"], info["mission"]["best_perplexity"]))
        info["text"] = "\n".join(lines)
        return info

    def help(self) -> Dict[str, object]:
        table = [
            ("chat", "बातचीत — मॉडल उत्तर देता है"),
            ("code <लक्ष्य>", "मॉडल सूत्र कोड लिखता है, VM पर चलाता है"),
            ("run <कोड>", "दिया गया सूत्र कोड चलाता है"),
            ("explain <कोड>", "संरचना का सच्चा विश्लेषण"),
            ("image <प्रॉम्प्ट>", "सूत्र कार्यक्रम + मॉडल वितरण से PNG"),
            ("status", "मॉडल, कर्नेल, पिछला मिशन"),
        ]
        text = "🕉️ ब्रह्म-LLM\n" + "\n".join("  %-16s %s" % row for row in table)
        return {"intent": "help", "text": text, "capabilities": [row[0] for row in table]}

    # -- the entry point --------------------------------------------------
    def respond(self, message: str, image_path: Optional[str] = None) -> Dict[str, object]:
        intent = detect_intent(message)
        try:
            if intent == "run":
                result = self.run(message)
            elif intent == "code":
                result = self.code(message)
            elif intent == "explain":
                result = self.explain(message)
            elif intent == "image":
                result = self.image(message, path=image_path)
            elif intent == "status":
                result = self.status()
            elif intent == "help":
                result = self.help()
            else:
                result = self.chat(message)
        except Exception as error:  # noqa: BLE001 - surfaced, never swallowed
            result = {"intent": intent, "text": "त्रुटि: %s: %s" % (type(error).__name__, error),
                      "error": str(error)}
        result.setdefault("intent", intent)
        self.history.append({"message": message, "intent": result["intent"]})
        return result


def ask(message: str, checkpoint: Optional[str] = None, image_path: Optional[str] = None) -> Dict[str, object]:
    """One-shot convenience wrapper used by the CLI and the HTTP layer."""
    return BrahmaAgent(checkpoint=checkpoint).respond(message, image_path=image_path)
