# 🕉️ सूत्र वास्तविक CPU

class सूत्रCPU:

    def __init__(self):

        print("🕉️ सूत्र वास्तविक CPU सक्रिय")

        self.रजिस्टर = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0

        }


    def LOAD(self, रजिस्टर, मान):

        self.रजिस्टर[रजिस्टर] = मान

        print("CPU LOAD:", रजिस्टर, "=", मान)


    def ADD(self, र1, र2):

        self.रजिस्टर[र1] += self.रजिस्टर[र2]

        print("CPU ADD:", र1, "=", self.रजिस्टर[र1])


    def SHOW(self, र):

        print("CPU SHOW:", र, "=", self.रजिस्टर[र])


    def STATE(self):

        print("CPU रजिस्टर स्थिति:")

        for र in self.रजिस्टर:

            print(र, "=", self.रजिस्टर[र])


    def EXECUTE(self, program):

        print("CPU निष्पादन प्रारम्भ")

        for instruction in program:

            opcode = instruction["opcode"]

            if opcode == "LOAD":

                self.LOAD(

                    instruction["op1"],
                    instruction["op2"]

                )


            elif opcode == "ADD":

                self.ADD(

                    instruction["op1"],
                    instruction["op2"]

                )


            elif opcode == "SHOW":

                self.SHOW(

                    instruction["op1"]

                )


            elif opcode == "STATE":

                self.STATE()


            elif opcode == "EXIT":

                print("CPU समाप्त")

                break


            else:

                print("अज्ञात opcode:", opcode)
