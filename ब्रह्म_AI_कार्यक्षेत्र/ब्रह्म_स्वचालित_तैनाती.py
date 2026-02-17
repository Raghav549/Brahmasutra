# 🕉️ ब्रह्म स्वचालित तैनाती इंजन VERSION 120

import os
import subprocess
import threading
import time

class ब्रह्मस्वचालिततैनाती:

    def __init__(self, कार्यक्षेत्र):
        self.कार्यक्षेत्र = कार्यक्षेत्र
        print("🕉️ ब्रह्म स्वचालित तैनाती इंजन सक्रिय")

    def backend_चलाओ(self):

        backend_path = os.path.join(self.कार्यक्षेत्र, "backend")

        if not os.path.exists(backend_path):
            print("Backend नहीं मिला")
            return

        print("Backend प्रारम्भ हो रहा है...")

        subprocess.Popen(
            ["python", "server.py"],
            cwd=backend_path
        )

    def frontend_चलाओ(self):

        frontend_path = os.path.join(self.कार्यक्षेत्र, "frontend")

        if not os.path.exists(frontend_path):
            print("Frontend नहीं मिला")
            return

        print("Frontend प्रारम्भ हो रहा है...")

        subprocess.Popen(
            ["python", "-m", "http.server", "8000"],
            cwd=frontend_path
        )

    def तैनात(self):

        print("पूर्ण तैनाती प्रारम्भ")

        threading.Thread(target=self.backend_चलाओ).start()

        time.sleep(2)

        threading.Thread(target=self.frontend_चलाओ).start()

        time.sleep(2)

        print("")
        print("🕉️ ब्रह्म अनुप्रयोग LIVE")
        print("")
        print("Backend: http://127.0.0.1:5000")
        print("Frontend: http://127.0.0.1:8000")
        print("")
        print("Browser में Frontend link खोलें")
