print("🕉️ ब्रह्म द्विआधारी लेखक सक्रिय")


class ब्रह्मद्विआधारीलेखक:


    def __init__(self):

        pass


    def लिखो(self, filename, program):

        with open(filename, "wb") as f:


            for inst in program:


                opcode = inst[0]

                op1 = inst[1]

                op2 = inst[2] if len(inst) > 2 else 0


                f.write(bytes([opcode]))
                f.write(bytes([op1]))
                f.write(bytes([op2]))


        print("Binary written:", filename)
