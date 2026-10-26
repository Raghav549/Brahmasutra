"""🕉️ सूत्र प्रक्रिया तंत्र — process objects and manager.

Public API
----------
``प्रक्रिया``          a process with a name, a pid and a state
``प्रक्रिया_प्रबंधक``  creates/starts/stops processes
``प्रक्रियातंत्र``     alias kept for the older demo scripts

The manager accepts either a name or a numeric pid in every lookup, because the
historical demos use both spellings.
"""

from __future__ import annotations

#: process states
निर्मित_स्थिति = "निर्मित"
चालू_स्थिति = "चल रहा"
रुकी_स्थिति = "रुका"
बन्द_स्थिति = "बन्द"

#: states that count as "alive" for :meth:`प्रक्रिया_प्रबंधक.सक्रिय`
_जीवित = (निर्मित_स्थिति, चालू_स्थिति, रुकी_स्थिति)


class प्रक्रिया:
    """A single process."""

    def __init__(self, नाम, pid=None):
        self.नाम = नाम
        self.pid = pid
        self.स्थिति = निर्मित_स्थिति

    # -- lifecycle -------------------------------------------------------
    def चलाओ(self):
        self.स्थिति = चालू_स्थिति
        print(f"प्रक्रिया चल रही: {self.नाम}")
        return self

    # ``प्रारम्भ`` is the name the scheduler uses
    def प्रारम्भ(self):
        return self.चलाओ()

    def रोको(self):
        self.स्थिति = रुकी_स्थिति
        print(f"प्रक्रिया रुकी: {self.नाम}")
        return self

    def बन्द(self):
        self.स्थिति = बन्द_स्थिति
        print(f"प्रक्रिया बन्द: {self.नाम}")
        return self

    # -- helpers ---------------------------------------------------------
    @property
    def सक्रिय(self):
        return self.स्थिति in _जीवित

    def वर्णन(self):
        return {"pid": self.pid, "नाम": self.नाम, "स्थिति": self.स्थिति}

    def __repr__(self):  # pragma: no cover - debugging helper
        return f"<प्रक्रिया {self.pid}:{self.नाम} {self.स्थिति}>"


class प्रक्रिया_प्रबंधक:
    """Create and track processes."""

    def __init__(self, चरम_प्रक्रिया=256):
        self.प्रक्रियाएँ = {}
        self.अगला_pid = 1
        self.चरम_प्रक्रिया = चरम_प्रक्रिया
        print("🕉️ प्रक्रिया प्रबंधक निर्मित")

    # -- creation --------------------------------------------------------
    def निर्माण(self, नाम):
        if len(self.प्रक्रियाएँ) >= self.चरम_प्रक्रिया:
            raise RuntimeError("प्रक्रिया सीमा पूरी हो गई")
        p = प्रक्रिया(नाम, pid=self.अगला_pid)
        self.प्रक्रियाएँ[self.अगला_pid] = p
        self.अगला_pid += 1
        print(f"प्रक्रिया निर्मित: {नाम} (pid {p.pid})")
        return p

    def नाम_से(self, नाम):
        for p in self.प्रक्रियाएँ.values():
            if p.नाम == नाम:
                return p
        return None

    def खोजो(self, पहचान):
        """Find a process by pid or by name."""
        if isinstance(पहचान, प्रक्रिया):
            return पहचान
        if isinstance(पहचान, int) or (isinstance(पहचान, str) and पहचान.isdigit()):
            return self.प्रक्रियाएँ.get(int(पहचान))
        return self.नाम_से(पहचान)

    # -- lifecycle -------------------------------------------------------
    def प्रारम्भ(self, पहचान):
        p = self.खोजो(पहचान)
        if p is None:
            print(f"त्रुटि: प्रक्रिया नहीं मिली: {पहचान}")
            return None
        return p.चलाओ()

    def रोको(self, पहचान):
        p = self.खोजो(पहचान)
        if p is None:
            print(f"त्रुटि: प्रक्रिया नहीं मिली: {पहचान}")
            return None
        return p.रोको()

    def समाप्त(self, पहचान):
        p = self.खोजो(पहचान)
        if p is None:
            print(f"त्रुटि: प्रक्रिया नहीं मिली: {पहचान}")
            return None
        p.बन्द()
        self.प्रक्रियाएँ.pop(p.pid, None)
        return p

    # ``चलाओ`` is the name used by the earliest demo generation
    def चलाओ(self, पहचान):
        return self.प्रारम्भ(पहचान)

    # -- introspection ---------------------------------------------------
    def सक्रिय(self):
        return [p for p in self.प्रक्रियाएँ.values() if p.सक्रिय]

    def सूची(self):
        print("प्रक्रिया सूची:")
        for p in sorted(self.प्रक्रियाएँ.values(), key=lambda x: x.pid):
            print(f"{p.pid} : {p.नाम} : {p.स्थिति}")
        if not self.प्रक्रियाएँ:
            print("• कोई प्रक्रिया नहीं")

    def स्थिति(self):
        return {
            "कुल": len(self.प्रक्रियाएँ),
            "सक्रिय": len(self.सक्रिय()),
            "अगला_pid": self.अगला_pid,
        }


# ---------------------------------------------------------------------------
# Compatibility aliases — older demo scripts import these names.
# ---------------------------------------------------------------------------
प्रक्रियातंत्र = प्रक्रिया_प्रबंधक

#: shared manager, created on first use (importing this module stays free of
#: side effects, but ``प्रक्रिया_तंत्र.प्रारम्भ()`` still returns an object)
प्रबंधक = None


def प्रबंधक_प्राप्त():
    """Return the shared manager, creating it on first call."""
    global प्रबंधक
    if प्रबंधक is None:
        प्रबंधक = प्रक्रिया_प्रबंधक()
    return प्रबंधक


def प्रारम्भ():
    print("🕉️ प्रक्रिया तंत्र सक्रिय")
    return प्रबंधक_प्राप्त()


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    प्रबंधक_प्राप्त().सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
