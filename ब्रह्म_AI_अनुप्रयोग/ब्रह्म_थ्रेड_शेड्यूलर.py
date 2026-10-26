import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म थ्रेड शेड्यूलर
# VERSION 52

import threading

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_प्रोसेस_कर्नेल import ब्रह्मप्रोसेसकर्नेल


class ब्रह्मथ्रेडशेड्यूलर:

    def __init__(self):

        self.kernel = ब्रह्मप्रोसेसकर्नेल()

        self.threads = {}

        print("🕉️ ब्रह्म थ्रेड शेड्यूलर सक्रिय")


    def प्रारंभ(self, नाम):

        def target():

            result = self.kernel.चलाओ(नाम)

            print("THREAD RESULT:", result)


        thread = threading.Thread(target=target)

        thread.start()

        tid = len(self.threads) + 1

        self.threads[tid] = thread

        return {

            "status": "success",

            "thread_id": tid,

            "message": f"{नाम} scheduled"

        }


    def सूची(self):

        result = {}

        for tid, thread in self.threads.items():

            result[tid] = {

                "alive": thread.is_alive()

            }

        return result
