class Stack:

    def __init__(self):

        self.stack = []

    def धकेलो(self, value):

        self.stack.append(int(value))

    def निकालो(self):

        if not self.stack:

            raise Exception("Stack खाली है")

        return self.stack.pop()

    def शीर्ष(self):

        if not self.stack:

            return None

        return self.stack[-1]

    def स्थिति(self):

        return self.stack
