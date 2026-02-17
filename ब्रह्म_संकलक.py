import os

class ब्रह्मसंकलक:

    def __init__(self):

        print("🕉️ ब्रह्म संकलक सक्रिय")

        self.instructions = {

            "स्थापित": "SET",
            "योग": "ADD",
            "दर्शय": "PRINT"

        }


    def instruction_convert(self,line):

        parts = line.strip().split()

        if len(parts) == 0:
            return ""


        cmd = parts[0]


        if cmd in self.instructions:

            opcode = self.instructions[cmd]

            return opcode + " " + " ".join(parts[1:])


        return line


    def संकलन(self,input_path,output_path):

        if not os.path.exists(input_path):

            print("त्रुटि: स्रोत संचिका नहीं मिली")

            return


        with open(input_path,"r",encoding="utf-8") as f:

            lines = f.readlines()


        machine_code = []


        for line in lines:

            mc = self.instruction_convert(line)

            if mc:
                machine_code.append(mc)


        with open(output_path,"wb") as f:

            for line in machine_code:

                f.write((line+"\n").encode("utf-8"))


        print("संकलन सफल:",output_path)
