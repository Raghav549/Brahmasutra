import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म अनुप्रयोग लोडर तंत्र
# VERSION 48 FIXED

import os
import runpy

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_अनुप्रयोग_पंजी import ब्रह्मअनुप्रयोगपंजी


class ब्रह्मअनुप्रयोगलोडर:

    def __init__(self):
        self.पंजी = ब्रह्मअनुप्रयोगपंजी()

    def लोड(self, नाम):

        ऐप = self.पंजी.प्राप्त(नाम)

        if not ऐप:
            return {
                "status": "error",
                "message": "application not registered"
            }

        पथ = ऐप["पथ"]

        # FIX: convert to full termux path
        if पथ.startswith("/home/"):
            पथ = पथ.replace(
                "/home/",
                "/data/data/com.termux/files/home/"
            )

        पथ = os.path.expanduser(पथ)

        if not os.path.exists(पथ):
            return {
                "status": "error",
                "message": f"file not found: {पथ}"
            }

        try:

            runpy.run_path(पथ)

            return {
                "status": "success",
                "message": f"{नाम} executed"
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }
