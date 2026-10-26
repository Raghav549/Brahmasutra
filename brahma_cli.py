"""🕉️ Shared CLI helpers for the demo scripts.

Most scripts in this repository were written for an interactive terminal.  Run
with stdin closed — which is what happens in CI, in tests, and when a script is
piped — they used to die with a raw ``EOFError`` traceback.  ``चलाओ`` (``run``)
turns that into a clear message and a meaningful exit code:

===== =====================================================
code  meaning
===== =====================================================
0     success
1     unhandled error (traceback is printed)
2     interactive input required but stdin was closed
130   interrupted with Ctrl-C
===== =====================================================

>>> run(lambda: 0)
0
>>> run(lambda: (_ for _ in ()).throw(EOFError()))  # message goes to stderr
2
"""

from __future__ import annotations

import inspect
import sys
import traceback
from typing import Callable, Iterable, Optional, Sequence

__all__ = ["run", "चलाओ", "पूछो", "ask", "is_interactive", "print_usage"]

EOF_MESSAGE = "इनपुट उपलब्ध नहीं (stdin बंद है) — यह डेमो इंटरैक्टिव टर्मिनल चाहता है।"


def is_interactive() -> bool:
    """True when stdin is attached to a terminal."""
    try:
        return bool(sys.stdin and sys.stdin.isatty())
    except (AttributeError, ValueError):
        return False


def run(main: Callable, argv: Optional[Sequence[str]] = None) -> int:
    """Call ``main`` and translate failures into an exit code.

    ``main`` may accept zero arguments or one (``argv``); its return value, when
    not ``None``, is used as the exit code.
    """
    try:
        takes_args = bool(inspect.signature(main).parameters) if _inspectable(main) else False
        result = main(argv) if takes_args else main()
    except EOFError:
        print(EOF_MESSAGE, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nरोका गया (Ctrl-C)", file=sys.stderr)
        return 130
    except SystemExit as exc:  # let scripts raise SystemExit themselves
        return int(exc.code or 0) if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    except Exception:  # noqa: BLE001 - report, do not swallow
        traceback.print_exc()
        return 1

    if result is None:
        return 0
    if isinstance(result, bool):
        return 0 if result else 1
    if isinstance(result, int):
        return result
    return 0


def _inspectable(func: Callable) -> bool:
    try:
        inspect.signature(func)
    except (TypeError, ValueError):
        return False
    return True


#: Hindi alias used by the सूत्र scripts.
चलाओ = run


def पूछो(प्रश्न: str = "", डिफ़ॉल्ट: Optional[str] = None, विकल्प: Optional[Iterable[str]] = None) -> str:
    """Ask for input, returning ``डिफ़ॉल्ट`` instead of raising on EOF."""
    प्रश्न_पूर्ण = प्रश्न
    if डिफ़ॉल्ट is not None:
        प्रश्न_पूर्ण = "%s [%s] " % (प्रश्न, डिफ़ॉल्ट)
    try:
        उत्तर = input(प्रश्न_पूर्ण)
    except EOFError:
        if डिफ़ॉल्ट is not None:
            return डिफ़ॉल्ट
        raise
    उत्तर = उत्तर.strip()
    if विकल्प is not None and उत्तर and उत्तर not in विकल्प:
        raise ValueError("अमान्य विकल्प %r (समर्थित: %s)" % (उत्तर, ", ".join(विकल्प)))
    return उत्तर or (डिफ़ॉल्ट or "")


#: English alias.
ask = पूछो


def print_usage(message: str) -> int:
    """Print a usage message to stderr and return exit code 2."""
    print(message, file=sys.stderr)
    return 2
