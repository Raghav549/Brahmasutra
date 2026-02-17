print("🕉️ ब्रह्म द्विआधारी पाठक सक्रिय")


class ब्रह्मद्विआधारीपाठक:


    def __init__(self):

        pass


    def पढ़ो(self, filename):

        program = []


        with open(filename, "rb") as f:


            data = f.read()


            for i in range(0, len(data), 3):


                opcode = data[i]
                op1 = data[i+1]
                op2 = data[i+2]


                program.append((opcode, op1, op2))


        print("Binary loaded:", filename)

        return program
