# सूत्र भाषा Core v2

import सूत्र_parser as पार्सर
import सूत्र_bytecode as बाइटकोड
import सूत्र_cpu as CPU

class सूत्रCore:

    def __init__(self):

        print("🕉️ सूत्र भाषा Core सक्रिय")

        self.cpu = CPU.सूत्रCPU()


    def संचिका_चलाओ(self, filename):

        try:

            with open(filename, "r", encoding="utf-8") as f:

                code = f.read()

        except:

            print("त्रुटि: संचिका नहीं मिली")
            return


        print("संचिका लोड:", filename)

        ast = पार्सर.parse(code)

        bytecode = बाइटकोड.generate(ast)

        self.cpu.execute(bytecode)

        print("संचिका निष्पादन पूर्ण")


    def संवाद(self):

        print("सूत्र संवाद सक्रिय")
        print("निर्गम लिखें बन्द करने हेतु")

        while True:

            cmd = input("सूत्र >>> ")

            if cmd == "निर्गम":

                break

            ast = पार्सर.parse(cmd)

            bytecode = बाइटकोड.generate(ast)

            self.cpu.execute(bytecode)
