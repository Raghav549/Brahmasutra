"""🕉️ सूत्र अनुप्रयोग निर्माता — now a thin front-end for ब्रह्म-LLM.

What this class used to do: write a fixed ``संकल्प अ 10`` program (an *old*
opcode dialect the current compiler cannot even parse), a static HTML page and a
Python stub, print "निर्मित", and call it an application.

What it does now: there is no app builder in ब्रह्म any more.  The model *is* the
application, so this shim asks :class:`brahma_llm.agent.BrahmaAgent` to write
सूत्र logic for the request, executes it on the project's VM, and writes a
manifest that points at the model's own server (``brahma llm serve``) instead of
pretending to have generated a separate program.

    >>> sv = सूत्रअनुप्रयोगनिर्माता()          # doctest: +SKIP
    >>> sv.सूत्र_अनुप्रयोग("मेरा_अनुप्रयोग")   # doctest: +SKIP

The old method names (``सूत्र_अनुप्रयोग``, ``वेबसाइट``, ``स्वचालन``) and their
``*_निर्माण`` aliases are preserved so the legacy demos keep working.
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.append(_ROOT)

from brahma_paths import data_root  # noqa: E402


def _load_model(model_dir=None):
    """Load the best checkpoint if one exists; ``None`` is a valid answer."""
    try:
        from brahma_llm.model import BrahmaLLM
    except ImportError:  # pragma: no cover - brahma_llm always ships
        return None
    directory = model_dir or data_root("llm", "best")
    if not os.path.isdir(directory):
        return None
    try:
        return BrahmaLLM.load(directory)
    except (OSError, ValueError, KeyError):
        return None


class सूत्रअनुप्रयोगनिर्माता:
    """Drive ब्रह्म-LLM: the model answers, writes सूत्र and runs it."""

    def __init__(self, model_dir=None, out_root=None):
        print("🕉️ सूत्र अनुप्रयोग निर्माता (ब्रह्म-LLM) सक्रिय")
        self.model_dir = model_dir
        self.model = _load_model(model_dir)
        self.अनुप्रयोग_पथ = out_root or data_root("apps", create=True)
        os.makedirs(self.अनुप्रयोग_पथ, exist_ok=True)
        if self.model is None:
            print("   (चेकपॉइंट नहीं मिला — सत्यापित टेम्पलेट से निर्माण होगा;")
            print("    पूर्ण LLM निर्माण के लिए पहले `brahma llm train` चलाएँ)")

    # -- helpers ---------------------------------------------------------
    def नाम_निर्माण(self):
        import random

        return "अनुप्रयोग_" + str(random.randint(1000, 9999))

    def _build(self, नाम, लक्ष्य):
        """Ask the model for सूत्र logic, run it, and record where to talk to it."""
        from brahma_llm.agent import BrahmaAgent

        agent = BrahmaAgent(model=self.model)
        result = agent.code(लक्ष्य)
        directory = os.path.join(self.अनुप्रयोग_पथ, नाम)
        os.makedirs(directory, exist_ok=True)
        logic_file = "%s.sutra" % नाम
        with open(os.path.join(directory, logic_file), "w", encoding="utf-8") as handle:
            handle.write(result.get("source", ""))
        manifest = {
            "name": नाम,
            "target": लक्ष्य,
            "dir": directory,
            "logic_file": logic_file,
            "logic_origin": result.get("origin", "none"),
            "logic_runs": result.get("error") is None and bool(result.get("source")),
            "output": result.get("output", []),
            "smoke": {"ok": result.get("error") is None and bool(result.get("source")),
                      "detail": "मॉडल ने सूत्र लिखा और VM पर चलाया"},
            "engine": "BRAHMA-LLM",
            "mode": "llm-serve",
            "server": "brahma llm serve",
            "endpoints": ["/chat", "/run", "/explain", "/image", "/kernel", "/status"],
        }
        with open(os.path.join(directory, "manifest.json"), "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=1)
        print("मॉडल तैयार: %s" % directory)
        print("  तर्क: %s (%s), निष्पादन: %s"
              % (logic_file, manifest["logic_origin"],
                 "ठीक" if manifest["logic_runs"] else "विफल"))
        print("  बातचीत: `brahma llm serve` चलाएँ (मॉडल ही अनुप्रयोग है)")
        return manifest

    # -- public API (names kept from the legacy builder) -----------------
    def सूत्र_अनुप्रयोग(self, नाम):
        """Write + run सूत्र logic for ``नाम`` and record its manifest."""
        return self._build(नाम, "सूत्र अनुप्रयोग %s" % नाम)

    def वेबसाइट(self, नाम):
        """The web surface is the model's own server (``/`` serves the UI)."""
        manifest = self._build(नाम, "वेबसाइट %s" % नाम)
        manifest["index"] = "brahma llm serve → GET /"
        print("वेबसाइट: %s" % manifest["index"])
        return manifest

    def स्वचालन(self, नाम):
        """Build an automation app whose logic runs on the VM."""
        return self._build(नाम, "स्वचालन कार्य %s" % नाम)

    def निर्माण(self, प्रकार):
        नाम = self.नाम_निर्माण()
        if प्रकार == "सूत्र":
            return self.सूत्र_अनुप्रयोग(नाम)
        if प्रकार == "वेबसाइट":
            return self.वेबसाइट(नाम)
        if प्रकार == "स्वचालन":
            return self.स्वचालन(नाम)
        raise ValueError("अज्ञात प्रकार %r (सूत्र / वेबसाइट / स्वचालन)" % (प्रकार,))

    def सूची(self):
        """List the manifests of every app built so far."""
        found = []
        for name in sorted(os.listdir(self.अनुप्रयोग_पथ)):
            manifest = os.path.join(self.अनुप्रयोग_पथ, name, "manifest.json")
            if os.path.exists(manifest):
                with open(manifest, "r", encoding="utf-8") as handle:
                    found.append(json.load(handle))
        return found


# Compatibility aliases — the demos use the descriptive ``*_निर्माण`` spellings.
सूत्रअनुप्रयोगनिर्माता.सूत्र_अनुप्रयोग_निर्माण = सूत्रअनुप्रयोगनिर्माता.सूत्र_अनुप्रयोग
सूत्रअनुप्रयोगनिर्माता.वेबसाइट_निर्माण = सूत्रअनुप्रयोगनिर्माता.वेबसाइट
सूत्रअनुप्रयोगनिर्माता.स्वचालन_निर्माण = सूत्रअनुप्रयोगनिर्माता.स्वचालन
