# 🕉️ ब्रह्म प्रक्रिया निष्पादन कोर

import os
import subprocess

class ब्रह्मप्रक्रियानिष्पादनकोर:

    def __init__(self):
        print("🕉️ ब्रह्म प्रक्रिया निष्पादन कोर सक्रिय")
        self.प्रक्रियाएँ = {}

    def प्रारम्भ(self, नाम, आदेश):
        try:
            प्रक्रिया = subprocess.Popen(
                आदेश,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.प्रक्रियाएँ[नाम] = प्रक्रिया

            print(f"प्रक्रिया प्रारम्भ: {नाम}")
            print(f"PID: {प्रक्रिया.pid}")

        except Exception as e:
            print("त्रुटि:", e)

    def रोकें(self, नाम):

        if नाम in self.प्रक्रियाएँ:

            प्रक्रिया = self.प्रक्रियाएँ[नाम]

            प्रक्रिया.terminate()

            del self.प्रक्रियाएँ[नाम]

            print(f"प्रक्रिया रोकी गई: {नाम}")

        else:
            print("त्रुटि: प्रक्रिया नहीं मिली")

    def स्थिति(self):

        print("सक्रिय प्रक्रियाएँ:")

        for नाम, प्रक्रिया in self.प्रक्रियाएँ.items():

            चल_रही = प्रक्रिया.poll() is None

            स्थिति = "चल रही" if चल_रही else "बंद"

            print(f"{नाम} → PID {प्रक्रिया.pid} → {स्थिति}")
