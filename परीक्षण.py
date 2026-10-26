"""परीक्षण — सूत्र प्रक्रिया-निगरानी का नमूना (bounded).

यह फ़ाइल पहले ``while True: print(...); time.sleep(2)`` चलाती थी: न आयात हो
सकती थी, न सीमित समय में समाप्त। अब यह एक छोटा, नियंत्रित निगरानी-डेमो है —
चक्रों की संख्या तर्क से दी जा सकती है (डिफ़ॉल्ट 3) और सीटीआरएल-सी पर
साफ़-सुथरा रुकती है।

चलाएँ::

    python परीक्षण.py          # 3 चक्र
    python परीक्षण.py --rounds 10 --interval 1.0
"""

from __future__ import annotations

import argparse
import time
from typing import List, Optional

DEFAULT_ROUNDS = 3
DEFAULT_INTERVAL = 2.0


def प्रक्रिया_निगरानी(चक्र: int = DEFAULT_ROUNDS, अंतराल: float = DEFAULT_INTERVAL, विराम=None) -> List[str]:
    """``चक्र`` बार स्थिति दर्ज करें और वे पंक्तियाँ लौटाएँ।

    >>> प्रक्रिया_निगरानी(2, 0, विराम=lambda _: None)
    ['सूत्र प्रक्रिया चल रही है', 'सूत्र प्रक्रिया चल रही है']
    """
    if चक्र < 0:
        raise ValueError("चक्र ऋणात्मक नहीं हो सकते")
    if अंतराल < 0:
        raise ValueError("अंतराल ऋणात्मक नहीं हो सकता")

    पंक्तियाँ = []
    for _ in range(चक्र):
        पंक्ति = "सूत्र प्रक्रिया चल रही है"
        पंक्तियाँ.append(पंक्ति)
        print(पंक्ति)
        if अंतराल:
            (विराम or time.sleep)(अंतराल)
    return पंक्तियाँ


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="सूत्र प्रक्रिया निगरानी डेमो")
    parser.add_argument("--rounds", type=int, default=DEFAULT_ROUNDS)
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL)
    args = parser.parse_args(argv)
    try:
        प्रक्रिया_निगरानी(args.rounds, args.interval)
    except KeyboardInterrupt:
        print("\nनिगरानी रोकी गई")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
