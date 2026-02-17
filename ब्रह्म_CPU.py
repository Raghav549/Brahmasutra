import struct

class ब्रह्मCPU:

    def __init__(self):

        print("🕉️ ब्रह्म CPU सक्रिय")

        self.registers = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0

        }

        self.reverse_opcodes = {

            1:"SET",
            2:"ADD",
            3:"PRINT"

        }


    def execute_binary(self,path):

        print("CPU निष्पादन प्रारम्भ:",path)

        with open(path,"rb") as f:

            data = f.read()


        i = 0

        while i < len(data):

            opcode = data[i]

            i += 1


            cmd = self.reverse_opcodes.get(opcode)


            if cmd == "SET":

                reg = chr(data[i])
                i += 2

                value = struct.unpack("I",data[i:i+4])[0]
                i += 4

                self.registers[reg] = value

                print("SET",reg,value)


            elif cmd == "ADD":

                reg = chr(data[i])
                i += 2

                value = struct.unpack("I",data[i:i+4])[0]
                i += 4

                self.registers[reg] += value

                print("ADD",reg,value)


            elif cmd == "PRINT":

                reg = chr(data[i])
                i += 2

                print("PRINT",reg,"=",self.registers.get(reg,0))


            else:

                break


        print("CPU निष्पादन समाप्त")
