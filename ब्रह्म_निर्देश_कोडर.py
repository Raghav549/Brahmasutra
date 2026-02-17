import struct

class ब्रह्मनिर्देशकोडर:

    def __init__(self):

        print("🕉️ ब्रह्म निर्देश कोडर सक्रिय")

        self.opcodes = {

            "SET": 1,
            "ADD": 2,
            "PRINT": 3

        }


    def encode_line(self,line):

        parts = line.strip().split()

        if len(parts) == 0:
            return b""


        cmd = parts[0]

        opcode = self.opcodes.get(cmd,0)


        data = struct.pack("B",opcode)


        for part in parts[1:]:

            try:

                num = int(part)

                data += struct.pack("I",num)

            except:

                data += part.encode("utf-8")+b'\0'


        return data


    def encode_file(self,input_path,output_path):

        with open(input_path,"rb") as f:

            lines = f.readlines()


        binary = b""


        for line in lines:

            binary += self.encode_line(line.decode("utf-8"))


        with open(output_path,"wb") as f:

            f.write(binary)


        print("Machine encoding सफल:",output_path)
