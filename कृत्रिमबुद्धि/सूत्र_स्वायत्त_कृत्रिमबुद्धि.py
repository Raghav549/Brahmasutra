"""🕉️ सूत्र स्वायत्त कृत्रिमबुद्धि — a demo loop that "decides" what to do next.

Honest scope: the decisions are ``random.choice`` over three strings; nothing
here learns.  What it *does* do is exercise the module/counter pipeline, and it
writes its generated modules into the data directory (``BRAHMA_HOME`` or
``~/सूत्र-तंत्र``) instead of the current working directory, so running a demo
can no longer litter your checkout.
"""

import os
import random
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from brahma_paths import data_root  # noqa: E402

def output_dir() -> str:
    """Where generated ``स्वायत्त_NNNN.py`` modules go (created on first use)."""
    return data_root("स्वायत्त_मॉड्यूल", create=True)


class सूत्रस्वायत्तकृत्रिमबुद्धि:


    def __init__(self):

        print("🕉️ सूत्र स्वायत्त कृत्रिमबुद्धि सक्रिय")

        self.संस्करण = 1

        self.कार्यसूची = []

        self.सक्रिय = True


    def निर्णय(self):

        निर्णयसूची = ["मॉड्यूल","उन्नयन","कार्य"]

        return random.choice(निर्णयसूची)


    def मॉड्यूल(self):

        नाम = "स्वायत्त_" + str(random.randint(1000,9999))

        with open(os.path.join(output_dir(), नाम + ".py"),"w",encoding="utf-8") as f:

            f.write(f'print("स्वायत्त मॉड्यूल: {नाम}")')

        print("मॉड्यूल निर्मित:", os.path.join(output_dir(), नाम + ".py"))


    def उन्नयन(self):

        self.संस्करण += 1

        print("संस्करण:", self.संस्करण)


    def कार्य(self):

        नाम = "कार्य_" + str(random.randint(100,999))

        self.कार्यसूची.append(नाम)

        print("कार्य जोड़ा:", नाम)


    def कार्य_चलाओ(self):

        if self.कार्यसूची:

            कार्य = self.कार्यसूची.pop(0)

            print("कार्य चल रहा:", कार्य)


    def चक्र(self):

        निर्णय = self.निर्णय()

        print("निर्णय:", निर्णय)

        if निर्णय == "मॉड्यूल":

            self.मॉड्यूल()

        elif निर्णय == "उन्नयन":

            self.उन्नयन()

        elif निर्णय == "कार्य":

            self.कार्य()

        self.कार्य_चलाओ()


    def प्रारम्भ(self):

        print("AI प्रारम्भ")

        while self.सक्रिय:

            self.चक्र()

            time.sleep(2)


    def बन्द(self):

        self.सक्रिय = False

        print("AI बन्द")


def main():
    """One demo cycle, then exit (the old ``प्रारम्भ`` looped forever)."""
    ai = सूत्रस्वायत्तकृत्रिमबुद्धि()
    for _ in range(3):
        ai.चक्र()
    ai.बन्द()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
