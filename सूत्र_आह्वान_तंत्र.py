"""🕉️ सूत्र आह्वान तंत्र — the syscall (system-call) interface.

Two dispatch styles are supported:

* **registered handlers** — ``पंजीकरण(नाम, कार्य)`` then ``आह्वान(नाम, *args)``
* **built-in kernel calls** — ``आह्वान("स्मृति"|"सञ्चिका"|"प्रक्रिया", डेटा)``
"""

from __future__ import annotations

#: syscalls the kernel implements natively
मान्य_आह्वान = ("स्मृति", "सञ्चिका", "प्रक्रिया", "यन्त्र", "समय")


class सूत्रआह्वानतंत्र:
    """Registry + dispatcher for system calls."""

    def __init__(self):
        self.पंजीकृत = {}
        self.इतिहास = []
        print("🕉️ सूत्र आह्वान तंत्र सक्रिय")

    # -- registration ----------------------------------------------------
    def पंजीकरण(self, नाम, कार्य):
        if not callable(कार्य):
            raise TypeError(f"आह्वान '{नाम}' के लिए कॉलबल चाहिए")
        self.पंजीकृत[नाम] = कार्य
        print(f"आह्वान पंजीकृत: {नाम}")
        return कार्य

    # ``जोड़`` is a common spelling in the demos
    जोड़ = पंजीकरण

    def हटाओ(self, नाम):
        return self.पंजीकृत.pop(नाम, None)

    # -- dispatch --------------------------------------------------------
    def आह्वान(self, नाम, *args):
        if नाम in self.पंजीकृत:
            परिणाम = self.पंजीकृत[नाम](*args)
            self.इतिहास.append((नाम, True))
            return परिणाम

        try:
            परिणाम = self.कर्ण_आह्वान(नाम, *args)
        except ValueError:
            self.इतिहास.append((नाम, False))
            return "अमान्य आह्वान"
        self.इतिहास.append((नाम, True))
        return परिणाम

    # -- kernel calls ----------------------------------------------------
    def कर्ण_आह्वान(self, नाम, *args):
        डेटा = args[0] if args else None
        if नाम == "स्मृति":
            return self.स्मृति_आह्वान(डेटा)
        if नाम == "सञ्चिका":
            return self.सञ्चिका_आह्वान(डेटा)
        if नाम == "प्रक्रिया":
            return self.प्रक्रिया_आह्वान(डेटा)
        if नाम == "यन्त्र":
            return self.यन्त्र_आह्वान(डेटा)
        if नाम == "समय":
            return self.समय_आह्वान()
        raise ValueError(f"अज्ञात आह्वान: {नाम}")

    def स्मृति_आह्वान(self, डेटा=None):
        print("Kernel: स्मृति आह्वान", डेटा)
        return "स्मृति सफल"

    def सञ्चिका_आह्वान(self, डेटा=None):
        print("Kernel: सञ्चिका आह्वान", डेटा)
        return "सञ्चिका सफल"

    def प्रक्रिया_आह्वान(self, डेटा=None):
        print("Kernel: प्रक्रिया आह्वान", डेटा)
        return "प्रक्रिया सफल"

    def यन्त्र_आह्वान(self, डेटा=None):
        print("Kernel: यन्त्र आह्वान", डेटा)
        return "यन्त्र सफल"

    def समय_आह्वान(self):
        import time

        return time.time()

    # -- introspection ---------------------------------------------------
    def सूची(self):
        print("पंजीकृत आह्वान:")
        for नाम in sorted(self.पंजीकृत):
            print("•", नाम)
        if not self.पंजीकृत:
            print("• कोई नहीं")


# Compatibility alias used by ``आह्वान-परीक्षण.py`` and
# ``सूत्र_उपयोगकर्ता_निष्पादन.py``.
आह्वानतंत्र = सूत्रआह्वानतंत्र
