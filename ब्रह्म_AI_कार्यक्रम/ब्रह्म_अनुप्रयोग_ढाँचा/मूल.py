class ब्रह्मअनुप्रयोग:

    def __init__(self, नाम):
        self.नाम = नाम
        self.सक्रिय = False
        self.घटक = []

    def प्रारम्भ(self):
        self.सक्रिय = True
        print(f"अनुप्रयोग प्रारम्भ: {self.नाम}")

    def घटक_जोड़ो(self, घटक):
        self.घटक.append(घटक)
        print(f"घटक जोड़ा: {घटक}")

    def स्थिति(self):
        print(f"नाम: {self.नाम}")
        print(f"सक्रिय: {self.सक्रिय}")
        print(f"घटक: {self.घटक}")
