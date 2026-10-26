"""🕉️ सूत्र स्मृति तंत्र — flat memory plus a simple paged allocator.

Two APIs live here:

* ``सूत्रस्मृति`` — a flat 64 KiB array with ``लेखन``/``पठन`` (legacy).
* ``स्मृतितंत्र`` — a first-fit allocator with ``आवंटन``/``मुक्त``/``स्थिति``
  (used by ``स्मृति-परीक्षण.py``).
"""

from __future__ import annotations

#: default flat memory size in cells
डिफ़ॉल्ट_आकार = 65536


class सूत्रस्मृति:
    """Flat memory (legacy API)."""

    def __init__(self, आकार=डिफ़ॉल्ट_आकार):
        print("🕉️ सूत्र स्मृति तंत्र सक्रिय")
        self.आकार = आकार
        self.स्मृति = [0] * आकार

    def _जाँच(self, स्थान):
        if not isinstance(स्थान, int) or isinstance(स्थान, bool):
            raise TypeError("स्मृति स्थान पूर्णांक होना चाहिए")
        if स्थान < 0 or स्थान >= self.आकार:
            raise IndexError(f"स्मृति स्थान सीमा से बाहर: {स्थान}")
        return स्थान

    def लेखन(self, स्थान, मान):
        self._जाँच(स्थान)
        self.स्मृति[स्थान] = मान
        print("स्मृति लेखन:", स्थान, मान)
        return मान

    def पठन(self, स्थान):
        self._जाँच(स्थान)
        मान = self.स्मृति[स्थान]
        print("स्मृति पठन:", स्थान, मान)
        return मान

    def स्थिति(self):
        return {"आकार": self.आकार, "प्रयुक्त": sum(1 for v in self.स्मृति if v)}


class स्मृतितंत्र:
    """First-fit paged allocator.

    Blocks are returned as integer *addresses* that can be released with
    :meth:`मुक्त`.  Allocation is deterministic so the demo output is stable.
    """

    def __init__(self, कुल_आकार=65536):
        self.कुल_आकार = कुल_आकार
        self.अगला_पता = 0
        self.ब्लॉक = {}          # पता -> आकार
        self.मुक्त_ब्लॉक = []    # [(पता, आकार)]
        print("🕉️ स्मृति तंत्र सक्रिय")

    # -- allocator -------------------------------------------------------
    def आवंटन(self, आकार):
        if not isinstance(आकार, int) or isinstance(आकार, bool) or आकार <= 0:
            raise ValueError("आवंटन आकार धनात्मक पूर्णांक होना चाहिए")

        # reuse a free block when it fits (first fit)
        for index, (पता, मुक्त_आकार) in enumerate(self.मुक्त_ब्लॉक):
            if मुक्त_आकार >= आकार:
                self.मुक्त_ब्लॉक.pop(index)
                if मुक्त_आकार > आकार:
                    self.मुक्त_ब्लॉक.insert(index, (पता + आकार, मुक्त_आकार - आकार))
                self.ब्लॉक[पता] = आकार
                print(f"स्मृति आवंटित: {आकार} बाइट @ {पता}")
                return पता

        if self.अगला_पता + आकार > self.कुल_आकार:
            raise MemoryError("पर्याप्त स्मृति नहीं")

        पता = self.अगला_पता
        self.अगला_पता += आकार
        self.ब्लॉक[पता] = आकार
        print(f"स्मृति आवंटित: {आकार} बाइट @ {पता}")
        return पता

    def मुक्त(self, पता):
        आकार = self.ब्लॉक.pop(पता, None)
        if आकार is None:
            print(f"त्रुटि: अमान्य पता {पता}")
            return False
        self.मुक्त_ब्लॉक.append((पता, आकार))
        self.मुक्त_ब्लॉक.sort()
        print(f"स्मृति मुक्त: {पता} ({आकार} बाइट)")
        return True

    # -- introspection ---------------------------------------------------
    def स्थिति(self):
        प्रयुक्त = sum(self.ब्लॉक.values())
        स्थिति = {
            "कुल": self.कुल_आकार,
            "प्रयुक्त": प्रयुक्त,
            "मुक्त": self.कुल_आकार - प्रयुक्त,
            "ब्लॉक": len(self.ब्लॉक),
        }
        print("स्मृति स्थिति:", स्थिति)
        return स्थिति
