# 🕉️ सूत्र AST निर्माता


class ASTNode:


    def __init__(self, प्रकार, मान=None):

        self.प्रकार = प्रकार
        self.मान = मान
        self.संतान = []


    def जोड़ो(self, node):

        self.संतान.append(node)


    def दिखाओ(self, स्तर=0):

        indent = "  " * स्तर

        print(f"{indent}{self.प्रकार}: {self.मान}")

        for child in self.संतान:

            child.दिखाओ(स्तर + 1)




class ASTनिर्माता:


    def निर्माण(self, संचिका):

        root = ASTNode("कार्यक्रम")

        with open(संचिका, encoding="utf-8") as f:

            lines = f.readlines()


        for line in lines:

            parts = line.strip().split()

            if not parts:
                continue


            cmd = parts[0]


            if cmd == "संकल्प":

                node = ASTNode("चर_निर्माण", parts[1:])

                root.जोड़ो(node)


            elif cmd == "योग":

                node = ASTNode("योग", parts[1:])

                root.जोड़ो(node)


            elif cmd == "दर्शय":

                node = ASTNode("दर्शय", parts[1:])

                root.जोड़ो(node)


            elif cmd == "निर्गम":

                node = ASTNode("निर्गम")

                root.जोड़ो(node)


        return root
