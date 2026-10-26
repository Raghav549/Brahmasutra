# 🕉️ ब्रह्म प्रक्रिया प्रबंधक कोर
# VERSION 11

import os
import threading

from ब्रह्म_Runtime_कोर import ब्रह्मRuntimeकोर


class ब्रह्मप्रक्रिया:

    def __init__(self, pid, अनुप्रयोग):

        self.pid = pid
        self.app = अनुप्रयोग
        self.runtime = ब्रह्मRuntimeकोर()

        self.thread = threading.Thread(
            target=self.runtime.प्रारम्भ,
            args=(अनुप्रयोग,)
        )

        self.active = False


    def प्रारम्भ(self):

        print(f"प्रक्रिया प्रारम्भ: PID={self.pid}")

        self.active = True

        self.thread.start()


    def स्थिति(self):

        if self.active:

            return "सक्रिय"

        else:

            return "निष्क्रिय"


    def रोक(self):

        print(f"प्रक्रिया रोक: PID={self.pid}")

        self.runtime.रोक()

        self.active = False



class ब्रह्मप्रक्रियाप्रबंधककोर:

    def __init__(self):

        self.processes = {}

        self.next_pid = 1

        print("प्रक्रिया प्रबंधक तैयार")


    def निर्माण(self, अनुप्रयोग):

        pid = self.next_pid

        self.next_pid += 1

        process = ब्रह्मप्रक्रिया(pid, अनुप्रयोग)

        self.processes[pid] = process

        print(f"प्रक्रिया निर्मित: PID={pid}")

        return pid


    def प्रारम्भ(self, pid):

        if pid in self.processes:

            self.processes[pid].प्रारम्भ()

        else:

            print("त्रुटि: PID नहीं मिला")


    def सूची(self):

        print("सभी प्रक्रियाएँ:")

        for pid, proc in self.processes.items():

            print(f"PID={pid} | App={proc.app} | State={proc.स्थिति()}")


    def रोक(self, pid):

        if pid in self.processes:

            self.processes[pid].रोक()

        else:

            print("त्रुटि: PID नहीं मिला")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global manager, pid


    print("🕉️ ब्रह्म प्रक्रिया प्रबंधक कोर सक्रिय")
    manager = ब्रह्मप्रक्रियाप्रबंधककोर()

    pid = manager.निर्माण("परीक्षण.ब्रह्म")

    manager.सूची()

    manager.प्रारम्भ(pid)

    manager.सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
