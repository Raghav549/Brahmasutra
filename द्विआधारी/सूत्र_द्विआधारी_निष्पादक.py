import ast
# 🕉️ सूत्र द्विआधारी निष्पादक

class सूत्रद्विआधारीनिष्पादक:

    def __init__(self):

        print("🕉️ सूत्र द्विआधारी निष्पादक सक्रिय")

        self.रजिस्टर = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0

        }


    def निष्पादन(self, संचिका):

        print("द्विआधारी लोड:", संचिका)


        with open(संचिका,"r",encoding="utf-8") as f:

            # ``eval`` could execute arbitrary Python; the file only ever
            # contains a literal list of instructions, so use a safe parser.
            कोड = ast.literal_eval(f.read())


        for आदेश in कोड:


            opcode = आदेश["opcode"]


            if opcode == "LOAD":

                self.रजिस्टर[आदेश["op1"]] = आदेश["op2"]

                print("स्थापित:", आदेश["op1"], "=", आदेश["op2"])


            elif opcode == "ADD":

                self.रजिस्टर[आदेश["op1"]] += self.रजिस्टर[आदेश["op2"]]

                print("योग:", आदेश["op1"], "=", self.रजिस्टर[आदेश["op1"]])


            elif opcode == "SHOW":

                print("दर्शय:", आदेश["op1"], "=", self.रजिस्टर[आदेश["op1"]])


            elif opcode == "EXIT":

                print("निर्गम")

                break


        print("निष्पादन पूर्ण")
