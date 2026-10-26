import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म सिस्टम कोर
# Full system controller

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_बूटलोडर import ब्रह्मबूटलोडर

class ब्रह्मसिस्टमकोर:

    def __init__(self):

        print("🕉️ ब्रह्म सिस्टम कोर सक्रिय")

        self.bootloader = ब्रह्मबूटलोडर()
        self.kernel = None

        self.started = False

    def प्रारंभ(self):

        if self.started:

            return {
                "status": "error",
                "message": "system already started"
            }

        result = self.bootloader.बूट()

        if result["status"] == "success":

            self.kernel = self.bootloader.kernel

            self.started = True

        return result

    def बंद(self):

        if not self.started:

            return {"status": "error"}

        result = self.bootloader.shutdown()

        self.kernel = None

        self.started = False

        return result

    def ऐप_चलाओ(self, app_name):

        if not self.started:

            return {
                "status": "error",
                "message": "system not started"
            }

        return self.kernel.प्रक्रिया_बनाओ(app_name)

    def ऐप_रोको(self, pid):

        if not self.started:

            return {"status": "error"}

        return self.kernel.प्रक्रिया_रोको(pid)

    def स्थिति(self):

        return {
            "system_started": self.started,
            "kernel_loaded": self.kernel is not None
        }
