# 🕉️ सूत्र Process Manager


import uuid


class सूत्रProcessManager:


    def __init__(self):

        print("🕉️ सूत्र Process Manager सक्रिय")

        self.processes = {}


    def create(self, app):

        pid = str(uuid.uuid4())[:8]

        self.processes[pid] = {

            "app": app,

            "status": "running"

        }

        print(f"Process created: {pid} → {app}")

        return pid


    def list(self):

        print("Active Processes:")

        for pid in self.processes:

            proc = self.processes[pid]

            print(f"{pid} → {proc['app']} ({proc['status']})")


    def stop(self, pid):

        if pid in self.processes:

            self.processes[pid]["status"] = "stopped"

            print(f"Process stopped: {pid}")


    def remove(self, pid):

        if pid in self.processes:

            del self.processes[pid]

            print(f"Process removed: {pid}")
