class ब्रह्मस्मृति:

    def __init__(self, size=1024):

        print("🕉️ ब्रह्म स्मृति सक्रिय")

        self.size = size

        self.memory = [0] * size


    def लिखो(self,address,value):

        if address >= self.size:

            print("स्मृति त्रुटि: सीमा पार")

            return

        self.memory[address] = value

        print("स्मृति लिखित:",address,"=",value)


    def पढ़ो(self,address):

        if address >= self.size:

            print("स्मृति त्रुटि: सीमा पार")

            return 0

        value = self.memory[address]

        print("स्मृति पढ़ित:",address,"=",value)

        return value


    def dump(self,start=0,end=10):

        print("स्मृति dump:")

        for i in range(start,end):

            print(i,"=",self.memory[i])
