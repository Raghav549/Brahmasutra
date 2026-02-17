# सूत्र Memory Model

class स्मृति:

    def __init__(self):
        self.variables = {}
        self.stack = []

    def स्थापित(self, नाम, मूल्य):
        self.variables[नाम] = मूल्य

    def प्राप्त(self, नाम):
        if नाम in self.variables:
            return self.variables[नाम]
        else:
            raise Exception(f"अपरिभाषित चर: {नाम}")

    def धकेलो(self, मूल्य):
        self.stack.append(मूल्य)

    def निकालो(self):
        if len(self.stack) == 0:
            raise Exception("Stack रिक्त है")
        return self.stack.pop()

    def स्थिति(self):
        print("चर:", self.variables)
        print("Stack:", self.stack)
