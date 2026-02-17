from vm.stack import Stack

class निर्देश:

    def __init__(self, vm):

        self.vm = vm
        self.stack = Stack()
        self.labels = {}

    def स्थापित(self, reg, value):

        self.vm.register_set(reg, int(value))

    def प्रदर्शित(self, reg):

        print(self.vm.register_get(reg))

    def वृद्धि(self, reg, value):

        current = self.vm.register_get(reg)

        self.vm.register_set(reg, current + int(value))

    def चिह्न(self, label):

        # handled in VM
        pass

    def यदि_कम(self, reg, value, label):

        if self.vm.register_get(reg) < int(value):

            self.vm.jump(label)

    def धकेलो(self, value):

        self.stack.धकेलो(value)

    def जोड़_स्टैक(self):

        v1 = self.stack.निकालो()

        v2 = self.stack.निकालो()

        self.stack.धकेलो(v1 + v2)

    def प्रदर्शित_स्टैक(self):

        print(self.stack.शीर्ष())
