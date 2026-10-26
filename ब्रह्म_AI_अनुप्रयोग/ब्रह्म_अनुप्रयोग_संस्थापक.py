import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म अनुप्रयोग संस्थापक तंत्र
# VERSION 49

import os
import shutil

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_अनुप्रयोग_पंजी import ब्रह्मअनुप्रयोगपंजी


class ब्रह्मअनुप्रयोगसंस्थापक:

    def __init__(self):

        self.पंजी = ब्रह्मअनुप्रयोगपंजी()

        self.स्थापना_स्थान = os.path.expanduser(
            "~/सूत्र-तंत्र/installed_apps"
        )

        os.makedirs(self.स्थापना_स्थान, exist_ok=True)

    def स्थापित(self, स्रोत_पथ):

        if स्रोत_पथ.startswith("/home/"):

            स्रोत_पथ = स्रोत_पथ.replace(
                "/home/",
                "/data/data/com.termux/files/home/"
            )

        स्रोत_पथ = os.path.expanduser(स्रोत_पथ)

        if not os.path.exists(स्रोत_पथ):

            return {
                "status": "error",
                "message": "source file not found"
            }

        नाम = os.path.basename(स्रोत_पथ)

        गंतव्य = os.path.join(
            self.स्थापना_स्थान,
            नाम
        )

        shutil.copy(स्रोत_पथ, गंतव्य)

        ऐप_नाम = नाम.replace(".py", "")

        self.पंजी.पंजीकरण(
            ऐप_नाम,
            गंतव्य
        )

        return {
            "status": "success",
            "message": f"{ऐप_नाम} installed",
            "path": गंतव्य
        }
