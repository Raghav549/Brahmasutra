# 🕉️ सूत्र CPU Emulator

import सूत्र_binary_loader as loader


class सूत्रCPU:

    def __init__(self):

        print("🕉️ सूत्र CPU Emulator सक्रिय")

        self.register = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0,
            "ई":0,
            "फ":0

        }

        self.memory = [0]*65536

        self.pc = 0

        self.instructions = []


    def load_binary(self, file):

        bin_loader = loader.सूत्रBinaryLoader()

        self.instructions = bin_loader.load(file)

        print("Binary loaded:", file)


    def fetch(self):

        if self.pc < len(self.instructions):

            instr = self.instructions[self.pc]

            self.pc +=1

            return instr

        return None


    def execute(self, instr):

        op = instr[0]


        if op == "SET":

            self.register[instr[1]] = instr[2]

            print("SET:", instr[1], instr[2])


        elif op == "ADD":

            self.register[instr[1]] += self.register[instr[2]]

            print("ADD:", self.register[instr[1]])


        elif op == "PRINT":

            print("PRINT:", self.register[instr[1]])


        elif op == "EXIT":

            print("CPU HALT")

            return False


        return True


    def run(self):

        print("CPU execution started")


        while True:

            instr = self.fetch()

            if instr is None:

                break


            cont = self.execute(instr)

            if not cont:

                break


        print("CPU execution finished")
