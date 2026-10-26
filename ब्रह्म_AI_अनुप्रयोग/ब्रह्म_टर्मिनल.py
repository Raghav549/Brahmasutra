import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म टर्मिनल
# Command line interface for BRAHMA OS

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_OS import ब्रह्मOS

class ब्रह्मटर्मिनल:

    def __init__(self):

        print("🕉️ BRAHMA TERMINAL सक्रिय")

        self.os = ब्रह्मOS()

    def चलाओ(self):

        while True:

            cmd = input("ब्रह्म > ")

            if cmd == "boot":

                print(self.os.boot())

            elif cmd == "shutdown":

                print(self.os.shutdown())

                break

            elif cmd == "restart":

                print(self.os.restart())

            elif cmd.startswith("run "):

                app = cmd.split(" ")[1]

                print(self.os.run_app(app))

            elif cmd.startswith("stop "):

                pid = int(cmd.split(" ")[1])

                print(self.os.stop_app(pid))

            elif cmd == "status":

                print(self.os.status())

            elif cmd == "exit":

                break

            else:

                print("unknown command")
