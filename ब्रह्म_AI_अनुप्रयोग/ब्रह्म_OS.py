import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म OS
# Master operating system controller

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_सिस्टम_कोर import ब्रह्मसिस्टमकोर

class ब्रह्मOS:

    def __init__(self):

        print("🕉️ BRAHMA OS सक्रिय")

        self.system = ब्रह्मसिस्टमकोर()

        self.running = False

    def boot(self):

        if self.running:

            return {
                "status": "error",
                "message": "OS already running"
            }

        result = self.system.प्रारंभ()

        if result["status"] == "success":

            self.running = True

        return result

    def shutdown(self):

        if not self.running:

            return {"status": "error"}

        result = self.system.बंद()

        self.running = False

        return result

    def restart(self):

        self.shutdown()

        return self.boot()

    def run_app(self, app):

        if not self.running:

            return {"status": "error"}

        return self.system.ऐप_चलाओ(app)

    def stop_app(self, pid):

        if not self.running:

            return {"status": "error"}

        return self.system.ऐप_रोको(pid)

    def status(self):

        return {
            "os_running": self.running,
            "system": self.system.स्थिति()
        }
