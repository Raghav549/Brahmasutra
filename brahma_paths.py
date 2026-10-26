"""🕉️ Data locations for the ब्रह्म demos.

Ten modules hard-coded a Termux path (``/data/data/com.termux/files/home/…``),
so on any other system they died with ``PermissionError: '/data'``.  Everything
now resolves through this module:

* ``BRAHMA_HOME`` environment variable, else
* ``~/सूत्र-तंत्र`` (the historical location).

>>> import os
>>> os.path.isabs(data_root()) or data_root() == "सूत्र-तंत्र"
True
"""

from __future__ import annotations

import os
from typing import Optional

__all__ = ["home_root", "data_root", "ensure_dir", "TERMUX_HOME"]

#: The path the demos used to hard-code.  Kept for reference/migration only.
TERMUX_HOME = "/data/data/com.termux/files/home/" + "सूत्र-तंत्र"


def home_root() -> str:
    """Base directory for generated data (``BRAHMA_HOME`` or ``~/सूत्र-तंत्र``)."""
    return os.path.abspath(
        os.environ.get("BRAHMA_HOME") or os.path.expanduser("~/सूत्र-तंत्र")
    )


def data_root(*parts: str, create: bool = False) -> str:
    """Return ``home_root()/parts...``; create it when ``create`` is true."""
    path = os.path.abspath(os.path.join(home_root(), *parts))
    if os.path.commonpath([home_root(), path]) != home_root():
        raise ValueError("पथ %r आधार निर्देशिका से बाहर है" % (path,))
    if create:
        os.makedirs(path, exist_ok=True)
    return path


def ensure_dir(path: Optional[str] = None) -> str:
    """Create ``path`` (default: the data root) and return it."""
    target = os.path.abspath(path or data_root())
    os.makedirs(target, exist_ok=True)
    return target
