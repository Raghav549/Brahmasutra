"""🕉️ सूत्र यन्त्र चालक तंत्र — device driver registry.

``यन्त्रचालक`` accepts a callable per device (legacy API):
``पंजीकरण(नाम, कार्य)`` / ``उपयोग(नाम, डेटा)``.

``यन्त्रचालकतंत्र`` accepts just a name, tracks active/inactive state and can
list devices (used by ``यन्त्र-परीक्षण.py``).
"""

from __future__ import annotations


class यन्त्रचालक:
    """Registry of device -> handler functions."""

    def __init__(self):
        self.उपकरण = {}
        print("🕉️ यन्त्र चालक तंत्र सक्रिय")

    def पंजीकरण(self, नाम, कार्य=None):
        if कार्य is not None and not callable(कार्य):
            raise TypeError(f"उपकरण '{नाम}' के लिए कॉलबल चाहिए")
        self.उपकरण[नाम] = कार्य
        print("उपकरण पंजीकृत:", नाम)
        return कार्य

    def उपयोग(self, नाम, डेटा=None):
        if नाम not in self.उपकरण:
            print("त्रुटि: उपकरण नहीं मिला:", नाम)
            return None
        कार्य = self.उपकरण[नाम]
        if कार्य is None:
            print(f"उपकरण '{नाम}' में कोई चालक नहीं")
            return None
        try:
            return कार्य(डेटा)
        except TypeError:
            return कार्य()

    def सूची(self):
        print("उपकरण:")
        for नाम in sorted(self.उपकरण):
            print("•", नाम)
        if not self.उपकरण:
            print("• कोई नहीं")


class यन्त्रचालकतंत्र:
    """Device table with enable/disable state (legacy ``यन्त्र-परीक्षण`` API)."""

    def __init__(self):
        self.उपकरण = {}
        print("🕉️ यन्त्र चालक तंत्र सक्रिय")

    def पंजीकरण(self, नाम, कार्य=None):
        if नाम in self.उपकरण:
            print(f"उपकरण पहले से पंजीकृत: {नाम}")
            return self.उपकरण[नाम]
        self.उपकरण[नाम] = {"कार्य": कार्य, "सक्रिय": False}
        print("उपकरण पंजीकृत:", नाम)
        return self.उपकरण[नाम]

    def सक्रिय(self, नाम):
        if नाम not in self.उपकरण:
            print("त्रुटि: उपकरण नहीं मिला:", नाम)
            return False
        self.उपकरण[नाम]["सक्रिय"] = True
        print("उपकरण सक्रिय:", नाम)
        return True

    def निष्क्रिय(self, नाम):
        if नाम not in self.उपकरण:
            print("त्रुटि: उपकरण नहीं मिला:", नाम)
            return False
        self.उपकरण[नाम]["सक्रिय"] = False
        print("उपकरण निष्क्रिय:", नाम)
        return True

    def उपयोग(self, नाम, डेटा=None):
        if नाम not in self.उपकरण:
            print("त्रुटि: उपकरण नहीं मिला:", नाम)
            return None
        entry = self.उपकरण[नाम]
        if not entry["सक्रिय"]:
            print(f"त्रुटि: उपकरण निष्क्रिय है: {नाम}")
            return None
        if entry["कार्य"] is None:
            return None
        return entry["कार्य"](डेटा)

    def सूची(self):
        print("उपकरण सूची:")
        for नाम, entry in sorted(self.उपकरण.items()):
            स्थिति = "सक्रिय" if entry["सक्रिय"] else "निष्क्रिय"
            print(f"• {नाम} : {स्थिति}")
        if not self.उपकरण:
            print("• कोई नहीं")
