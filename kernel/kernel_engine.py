#!/usr/bin/env python3
# सूत्र Kernel Engine

import sys
import os
import time

class सूत्रKernel:

    def __init__(self):
        self.running = False
        self.memory = {}
        self.processes = []

    def प्रारम्भ(self):
        print("सूत्र Kernel प्रारम्भ")
        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            cmd = input("सूत्र> ")

            if cmd == "exit":
                self.running = False
                print("सूत्र Kernel समाप्त")

            elif cmd.startswith("run "):
                file = cmd.split(" ",1)[1]
                self.execute(file)

            elif cmd == "memory":
                print(self.memory)

            else:
                print("अज्ञात आदेश")

    def execute(self, file):
        if not os.path.exists(file):
            print("file नहीं मिला")
            return

        print("execution प्रारम्भ:", file)

        with open(file,"r",encoding="utf-8") as f:
            code = f.read()

        exec(code, {}, self.memory)

        print("execution समाप्त")


def मुख्य():
    kernel = सूत्रKernel()
    kernel.प्रारम्भ()


if __name__ == "__main__":
    मुख्य()
