# 🕉️ ब्रह्म प्रोसेस कर्नेल — VERSION 57
# बहु-अनुप्रयोग समानांतर निष्पादन इंजन

import threading
import subprocess
import os

class ब्रह्मप्रोसेसकर्नेल:

    def __init__(self):
        self.प्रोसेस = {}
        self.अगला_pid = 1
        print("🕉️ ब्रह्म समानांतर प्रोसेस कर्नेल सक्रिय")

    def चलाओ(self, अनुप्रयोग_नाम):

        पथ = os.path.expanduser(f"~/सूत्र-तंत्र/test_apps/{अनुप्रयोग_नाम}.py")

        if not os.path.exists(पथ):
            return {"status":"error","message":"app not found"}

        pid = self.अगला_pid
        self.अगला_pid += 1

        thread = threading.Thread(
            target=self.__निष्पादन,
            args=(pid, पथ),
            daemon=True
        )

        self.प्रोसेस[pid] = {
            "path": पथ,
            "running": True,
            "thread": thread
        }

        thread.start()

        return {
            "status":"success",
            "pid": pid,
            "message":"parallel execution started"
        }

    def __निष्पादन(self, pid, पथ):

        try:

            subprocess.run(
                ["python", पथ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        except Exception as e:
            print("त्रुटि:", e)

        finally:

            if pid in self.प्रोसेस:
                self.प्रोसेस[pid]["running"] = False

    def सूची(self):

        परिणाम = {}

        for pid in self.प्रोसेस:

            परिणाम[pid] = {
                "running": self.प्रोसेस[pid]["running"],
                "path": self.प्रोसेस[pid]["path"]
            }

        return परिणाम

    def रोकें(self, pid):

        if pid not in self.प्रोसेस:
            return {"status":"error","message":"pid not found"}

        self.प्रोसेस[pid]["running"] = False

        return {"status":"success","message":"process marked stopped"}

    def स्थिति(self, pid):

        if pid not in self.प्रोसेस:
            return {"status":"error"}

        return {
            "pid": pid,
            "running": self.प्रोसेस[pid]["running"],
            "path": self.प्रोसेस[pid]["path"]
        }
