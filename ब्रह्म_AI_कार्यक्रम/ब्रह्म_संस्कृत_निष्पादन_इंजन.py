from ब्रह्म_संस्कृत_आदेश_पार्सर import ब्रह्मसंस्कृतआदेशपार्सर


class ब्रह्मसंस्कृतनिष्पादनइंजन:

    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत निष्पादन इंजन सक्रिय")

        self.parser = ब्रह्मसंस्कृतआदेशपार्सर()

        self.memory = {}


    def निष्पादित(self, पाठ):

        आदेशसूची = self.parser.पार्स(पाठ)

        result = None

        for आदेश in आदेशसूची:

            if आदेश["type"] == "store":

                self.memory[आदेश["var"]] = आदेश["value"]

                print(f"संग्रहित: {आदेश['var']} = {आदेश['value']}")

            elif आदेश["type"] == "add":

                a = self.memory.get(आदेश["a"], 0)

                b = self.memory.get(आदेश["b"], 0)

                result = a + b

                print(f"योग परिणाम: {result}")

            elif आदेश["type"] == "print":

                value = self.memory.get(आदेश["var"], None)

                print(f"मान: {value}")

        return result
