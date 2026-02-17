# 🕉️ ब्रह्म AI Backend निर्माता VERSION 17

import os

print("🕉️ ब्रह्म AI Backend निर्माता VERSION 17 सक्रिय")


class ब्रह्मBackendनिर्माता:

    def __init__(self):

        self.base_path = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_backend")

        os.makedirs(self.base_path, exist_ok=True)

    def निर्मित(self, name):

        app_path = os.path.join(self.base_path, name)

        os.makedirs(app_path, exist_ok=True)

        server_file = os.path.join(app_path, "server.py")

        code = '''# BRAHMA BACKEND SERVER

print("BRAHMA BACKEND RUNNING")

def लॉगिन():
    print("LOGIN SYSTEM ACTIVE")

def डेटाबेस():
    print("DATABASE CONNECTED")

def API():
    print("API READY")

def प्रारम्भ():

    लॉगिन()
    डेटाबेस()
    API()

if __name__ == "__main__":
    प्रारम्भ()
'''

        with open(server_file, "w", encoding="utf-8") as f:
            f.write(code)

        print("Backend निर्मित:", app_path)

        return app_path


# test run

builder = ब्रह्मBackendनिर्माता()

name = input("Backend नाम लिखें: ")

builder.निर्मित(name)
