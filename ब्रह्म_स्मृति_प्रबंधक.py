class ब्रह्मस्मृतिप्रबंधक:

    def __init__(self):

        self.memory = {}

        self.total = 1024 * 1024 * 1024   # 1GB simulated RAM

        self.used = 0

        print("🕉️ ब्रह्म स्मृति प्रबंधक सक्रिय")



    def आवंटन(self, नाम, आकार):

        if self.used + आकार > self.total:

            print("त्रुटि: पर्याप्त स्मृति नहीं")

            return False

        self.memory[नाम] = {

            "size": आकार,

            "data": None

        }

        self.used += आकार

        print("स्मृति आवंटित:", नाम, आकार)

        return True



    def लेखन(self, नाम, data):

        if नाम not in self.memory:

            print("त्रुटि: स्मृति नहीं मिली")

            return

        self.memory[नाम]["data"] = data

        print("स्मृति लेखन:", नाम)



    def पठन(self, नाम):

        if नाम not in self.memory:

            print("त्रुटि: स्मृति नहीं मिली")

            return None

        print("स्मृति पठन:", नाम)

        return self.memory[नाम]["data"]



    def मुक्त(self, नाम):

        if नाम in self.memory:

            size = self.memory[नाम]["size"]

            self.used -= size

            del self.memory[नाम]

            print("स्मृति मुक्त:", नाम)



    def स्थिति(self):

        print("कुल:", self.total)

        print("उपयोग:", self.used)

        print("उपलब्ध:", self.total - self.used)
