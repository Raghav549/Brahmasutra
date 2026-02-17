class बटन:

    def __init__(self, पाठ):
        self.पाठ = पाठ

    def दर्शय(self):
        print(f"[बटन] {self.पाठ}")


class पृष्ठ:

    def __init__(self, नाम):
        self.नाम = नाम
        self.घटक = []

    def जोड़ो(self, घटक):
        self.घटक.append(घटक)

    def दर्शय(self):
        print(f"पृष्ठ: {self.नाम}")
        for g in self.घटक:
            g.दर्शय()
