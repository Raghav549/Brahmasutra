# 🕉️ सूत्र Bytecode संकलक

from सूत्र_ast_निर्माता import ASTनिर्माता


class Bytecodeसंकलक:


    OPCODES = {

        "चर_निर्माण": 1,
        "योग": 2,
        "दर्शय": 3,
        "निर्गम": 4

    }


    def __init__(self):

        self.bytecode = []

        self.register_map = {}

        self.next_reg = 1


    def register(self, var):

        if var not in self.register_map:

            self.register_map[var] = self.next_reg
            self.next_reg += 1

        return self.register_map[var]


    def compile_node(self, node):

        प्रकार = node.प्रकार


        if प्रकार == "चर_निर्माण":

            var = node.मान[0]
            val = int(node.मान[1])

            reg = self.register(var)

            self.bytecode.extend([1, reg, val])


        elif प्रकार == "योग":

            r1 = self.register(node.मान[0])
            r2 = self.register(node.मान[1])

            self.bytecode.extend([2, r1, r2])


        elif प्रकार == "दर्शय":

            reg = self.register(node.मान[0])

            self.bytecode.extend([3, reg])


        elif प्रकार == "निर्गम":

            self.bytecode.append(4)


    def compile(self, input_file, output_file):

        builder = ASTनिर्माता()

        tree = builder.निर्माण(input_file)


        for node in tree.संतान:

            self.compile_node(node)


        with open(output_file, "wb") as f:

            f.write(bytes(self.bytecode))


        print("🕉️ Bytecode संकलन सफल:", output_file)
