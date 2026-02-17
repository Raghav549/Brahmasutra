class CallStack:

    def __init__(self):

        self.stack = []

    def धकेलो(self, address):

        self.stack.append(address)

    def निकालो(self):

        if not self.stack:

            return None

        return self.stack.pop()

    def स्थिति(self):

        return self.stack
