"""🕉️ Android bundle builder — honest about what it produces.

The audit found four "APK builders" in this repository.  Measured against the
files they left in git:

* two wrote a **three-line text file** with an ``.apk`` extension;
* two wrote a **ZIP archive** whose ``classes.dex`` was the ASCII string
  ``SUTRA_DEX_PLACEHOLDER`` and whose ``AndroidManifest.xml`` was plain XML.

None of those is an APK: Android requires a *binary* (compiled) manifest, a real
DEX file, and a v1/v2 signature.  Producing one needs ``aapt2``, ``d8`` and a
keystore, none of which are pure Python.

So this module does the two honest things:

* :func:`build_bundle` creates a **ZIP bundle** of the application (useful for
  distribution, and readable by any unzip tool) and labels it accordingly;
* :func:`is_installable_apk` checks whether a file really is an installable APK,
  so the project never again claims an archive is an app.

>>> bundle = build_bundle  # doctest: +SKIP
"""

from __future__ import annotations

import os
import zipfile
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

__all__ = ["Bundle", "build_bundle", "is_installable_apk", "DEX_MAGIC", "describe"]

DEX_MAGIC = b"dex\n"
APK_REQUIRED = ("AndroidManifest.xml", "classes.dex")


@dataclass
class Bundle:
    """Result of :func:`build_bundle`."""

    path: str
    files: List[str] = field(default_factory=list)
    is_apk: bool = False

    @property
    def size(self) -> int:
        """Size of the bundle on disk in bytes."""
        return os.path.getsize(self.path)

    def summary(self) -> str:
        """Human-readable one-line description."""
        return "%s (%d files, %d bytes, %s)" % (
            self.path,
            len(self.files),
            self.size,
            "APK" if self.is_apk else "ZIP संग्रह — स्थापन योग्य APK नहीं",
        )


def describe(path: str) -> str:
    """Describe what ``path`` really is."""
    if is_installable_apk(path):
        return "installable APK"
    if zipfile.is_zipfile(path):
        return "ZIP archive (not an installable APK)"
    return "not a ZIP archive"


def is_installable_apk(path: str) -> bool:
    """True only for a file that Android could actually install.

    Checks the ZIP structure, a *binary* manifest (not XML), a real DEX header
    and the presence of a signature block.
    """
    if not os.path.isfile(path) or not zipfile.is_zipfile(path):
        return False

    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        if not set(APK_REQUIRED) <= names:
            return False
        if not any(name.startswith("META-INF/") for name in names):
            return False
        manifest = archive.read("AndroidManifest.xml")
        # a plain-XML manifest starts with '<'; a compiled one does not
        if manifest.lstrip()[:1] in (b"<", b""):
            return False
        dex = archive.read("classes.dex")
        return dex.startswith(DEX_MAGIC)


def _iter_files(paths: Iterable[str]):
    for path in paths:
        if os.path.isdir(path):
            for base, _dirs, files in os.walk(path):
                for name in sorted(files):
                    full = os.path.join(base, name)
                    yield full, os.path.relpath(full, path)
        elif os.path.isfile(path):
            yield path, os.path.basename(path)
        else:
            raise FileNotFoundError(path)


def build_bundle(
    app_name: str,
    sources: Iterable[str],
    output_dir: str,
    flavour: int = 1,
) -> Bundle:
    """Zip ``sources`` into ``output_dir/<app_name>-flavour<N>.zip``.

    The result is **not** an installable APK; :func:`is_installable_apk` on it
    returns ``False`` and the returned :class:`Bundle` says so.
    """
    if not app_name or os.sep in app_name or ".." in app_name:
        raise ValueError("अमान्य अनुप्रयोग नाम: %r" % (app_name,))
    os.makedirs(output_dir, exist_ok=True)

    target = os.path.join(output_dir, "%s-flavour%d.zip" % (app_name, flavour))
    written = []
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for full, arcname in _iter_files(sources):
            archive.write(full, arcname)
            written.append(arcname)
        archive.writestr(
            "README.txt",
            "🕉️ %s\n\n"
            "यह एक ZIP संग्रह है, स्थापन योग्य APK नहीं।\n"
            "APK बनाने के लिए aapt2, d8 और keystore आवश्यक हैं।\n" % app_name,
        )
        written.append("README.txt")

    return Bundle(path=target, files=written, is_apk=False)


def build_zip(app_name: str, sources: Iterable[str], output_dir: str) -> Bundle:
    """Backwards-compatible alias of :func:`build_bundle`."""
    return build_bundle(app_name, sources, output_dir)
