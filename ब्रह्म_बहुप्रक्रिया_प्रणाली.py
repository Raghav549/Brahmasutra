# 🕉️ ब्रह्म बहुप्रक्रिया प्रणाली

import subprocess
import time

class ब्रह्मबहुप्रक्रियाप्रणाली:

    def __init__(self):

        print("🕉️ ब्रह्म बहुप्रक्रिया प्रणाली सक्रिय")

        self.प्रक्रियाएँ = {}
        self.क्रम = 0

    def निर्माण(self, नाम, आदेश):

        try:

            प्रक्रिया = subprocess.Popen(
                आदेश,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.क्रम += 1

            self.प्रक्रियाएँ[self.क्रम] = {
                "नाम": नाम,
                "प्रक्रिया": प्रक्रिया,
                "PID": प्रक्रिया.pid,
                "स्थिति": "चल रही"
            }

            print(f"नई प्रक्रिया निर्मित: {नाम}")
            print(f"क्रम: {self.क्रम}")
            print(f"PID: {प्रक्रिया.pid}")

        except Exception as e:

            print("त्रुटि:", e)

    def सूची(self):

        print("\nसभी प्रक्रियाएँ:\n")

        for क्रम, डेटा in self.प्रक्रियाएँ.items():

            प्रक्रिया = डेटा["प्रक्रिया"]

            if प्रक्रिया.poll() is None:

                स्थिति = "चल रही"

            else:

                स्थिति = "समाप्त"

            print(f"{क्रम} → {डेटा['नाम']} → PID {डेटा['PID']} → {स्थिति}")

    def रोकें(self, क्रम):

        if क्रम in self.प्रक्रियाएँ:

            प्रक्रिया = self.प्रक्रियाएँ[क्रम]["प्रक्रिया"]

            प्रक्रिया.terminate()

            self.प्रक्रियाएँ[क्रम]["स्थिति"] = "रोकी गई"

            print(f"प्रक्रिया रोकी गई: {क्रम}")

        else:

            print("त्रुटि: प्रक्रिया नहीं मिली")

    def साफ(self):

        समाप्त = []

        for क्रम, डेटा in self.प्रक्रियाएँ.items():

            if डेटा["प्रक्रिया"].poll() is not None:

                समाप्त.append(क्रम)

        for क्रम in समाप्त:

            del self.प्रक्रियाएँ[क्रम]

        print("समाप्त प्रक्रियाएँ हटाई गई")
