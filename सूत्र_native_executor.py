# 🕉️ सूत्र Native Instruction Executor

import सूत्र_CPU_नियंत्रण as cpu


class सूत्रNativeExecutor:


    def __init__(self):

        print("🕉️ सूत्र Native Executor सक्रिय")

        self.cpu = cpu.सूत्रCPUनियंत्रण()


    def चलाओ(self, instruction_list):

        print("Native Execution प्रारम्भ")


        for instr in instruction_list:


            opcode = instr["opcode"]

            op1 = instr["op1"]

            op2 = instr["op2"]


            if opcode == "LOAD":

                self.cpu.रजिस्टर[op1] = op2

                print("LOAD:", op1, op2)


            elif opcode == "ADD":

                self.cpu.रजिस्टर[op1] += self.cpu.रजिस्टर[op2]

                print("ADD:", self.cpu.रजिस्टर[op1])


            elif opcode == "STORE":

                self.cpu.स्मृतिलेखन(op1, op2)


            elif opcode == "SHOW":

                self.cpu.चलाओ("दर्शय")


        print("Native Execution समाप्त")
