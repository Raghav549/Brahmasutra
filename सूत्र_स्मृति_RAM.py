# 🕉️ सूत्र वास्तविक स्मृति (RAM)

class सूत्रRAM:

    def __init__(self):

        print("🕉️ सूत्र स्मृति सक्रिय")

        self.memory = {}


    def लिखो(self, address, value):

        self.memory[address] = value

        print("RAM लिखो:", address, "=", value)


    def पढ़ो(self, address):

        value = self.memory.get(address,0)

        print("RAM पढ़ो:", address, "=", value)

        return value


    def स्थिति(self):

        print("RAM स्थिति:")

        for addr in self.memory:

            print(addr,"=",self.memory[addr])
