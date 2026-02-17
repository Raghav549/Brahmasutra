# 🕉️ सूत्र Native Compiler

import सूत्र_native_instruction as native


class सूत्रNativeCompiler:


    def __init__(self):

        print("🕉️ सूत्र Native Compiler सक्रिय")

        self.native = native.सूत्रNativeInstruction()


    def compile(self, sutra_code):

        for line in sutra_code:


            parts = line.split()


            if parts[0] == "संकल्प":

                reg = parts[1]

                val = int(parts[2])

                self.native.जोड़ो("LOAD", reg, val)


            elif parts[0] == "योग":

                self.native.जोड़ो("ADD", parts[1], parts[2])


            elif parts[0] == "दर्शय":

                self.native.जोड़ो("SHOW")


        return self.native.सूची()
