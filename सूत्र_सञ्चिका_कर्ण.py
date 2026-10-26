"""🕉️ सूत्र सञ्चिका कर्ण — a small file-system service.

The storage root is configurable so that demos and tests never write into the
user's home directory by accident:

* ``SUTRA_DATA_DIR`` environment variable, else
* ``~/सूत्र-तंत्र/संग्रह`` (the historical location).

Names are validated: absolute paths and ``..`` components are rejected.
"""

from __future__ import annotations

import os


def _मूल_निर्धारण():
    return os.environ.get("SUTRA_DATA_DIR") or डिफ़ॉल्ट_मूल


class सूत्रसञ्चिकाकर्ण:
    """Read/write/list/delete files inside a single directory."""

    def __init__(self, मूलपथ=None):
        self.मूलपथ = os.path.abspath(मूलपथ or _मूल_निर्धारण())
        os.makedirs(self.मूलपथ, exist_ok=True)
        print("🕉️ सञ्चिका कर्ण तंत्र सक्रिय")

    # -- helpers ---------------------------------------------------------
    def पथ(self, नाम):
        """Resolve ``नाम`` inside the root, refusing escapes."""
        if not isinstance(नाम, str) or not नाम or नाम in (".", ".."):
            raise ValueError(f"अमान्य सञ्चिका नाम: {नाम!r}")
        if os.path.isabs(नाम) or ".." in नाम.replace("\\", "/").split("/"):
            raise ValueError(f"पथ वर्जित है: {नाम!r}")
        पूर्ण = os.path.abspath(os.path.join(self.मूलपथ, नाम))
        if os.path.commonpath([पूर्ण, self.मूलपथ]) != self.मूलपथ:
            raise ValueError(f"पथ मूल निर्देशिका से बाहर: {नाम!r}")
        return पूर्ण

    # -- operations ------------------------------------------------------
    def निर्माण(self, नाम, डेटा=""):
        पूर्णपथ = self.पथ(नाम)
        with open(पूर्णपथ, "w", encoding="utf-8") as f:
            f.write(डेटा)
        print("सञ्चिका निर्मित:", नाम)
        return पूर्णपथ

    def लेखन(self, नाम, डेटा):
        पूर्णपथ = self.पथ(नाम)
        with open(पूर्णपथ, "w", encoding="utf-8") as f:
            f.write(डेटा)
        print("सञ्चिका लिखित:", नाम)
        return पूर्णपथ

    def पठन(self, नाम):
        पूर्णपथ = self.पथ(नाम)
        if not os.path.exists(पूर्णपथ):
            print("त्रुटि: सञ्चिका नहीं मिली:", नाम)
            return None
        with open(पूर्णपथ, "r", encoding="utf-8") as f:
            डेटा = f.read()
        print("सञ्चिका पढ़ी:", नाम)
        return डेटा

    def सूची(self):
        try:
            files = sorted(os.listdir(self.मूलपथ))
        except OSError as exc:
            print("त्रुटि:", exc)
            return []
        print("सञ्चिका सूची:")
        for f in files:
            print("•", f)
        if not files:
            print("• कोई सञ्चिका नहीं")
        return files

    def विलोपन(self, नाम):
        पूर्णपथ = self.पथ(नाम)
        if os.path.exists(पूर्णपथ):
            os.remove(पूर्णपथ)
            print("सञ्चिका हटाई:", नाम)
            return True
        print("त्रुटि: सञ्चिका नहीं मिली:", नाम)
        return False

    def स्थिति(self):
        return {
            "मूल": self.मूलपथ,
            "सञ्चिकाएँ": len(os.listdir(self.मूलपथ)) if os.path.isdir(self.मूलपथ) else 0,
        }


# ---------------------------------------------------------------------------
# Compatibility alias — ``सञ्चिका-परीक्षण.py`` expects ``सञ्चिकातंत्र``.
# ---------------------------------------------------------------------------
सञ्चिकातंत्र = सूत्रसञ्चिकाकर्ण


डिफ़ॉल्ट_मूल = os.path.expanduser("~/सूत्र-तंत्र/संग्रह")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    pass

    #: default storage root


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
