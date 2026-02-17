# 🕉️ सूत्र RAM प्रबंधक

class सूत्रRAM:

    def __init__(self, आकार=1024):

        print("🕉️ सूत्र RAM प्रबंधक सक्रिय")

        self.आकार = आकार

        self.स्मृति = [0] * आकार

        self.अगला_स्थान = 0


    def आवंटन(self, आकार):

        if self.अगला_स्थान + आकार > self.आकार:

            print("त्रुटि: स्मृति पूर्ण")

            return None

        स्थान = self.अगला_स्थान

        self.अगला_स्थान += आकार

        print(f"स्मृति आवंटित: {स्थान} → {स्थान+आकार}")

        return स्थान


    def लिख(self, स्थान, मान):

        if स्थान >= self.आकार:

            print("त्रुटि: अमान्य स्मृति स्थान")
            return

        self.स्मृति[स्थान] = मान

        print(f"स्मृति लिख: [{स्थान}] = {मान}")


    def पढ़(self, स्थान):

        if स्थान >= self.आकार:

            print("त्रुटि: अमान्य स्मृति स्थान")
            return None

        मान = self.स्मृति[स्थान]

        print(f"स्मृति पढ़: [{स्थान}] = {मान}")

        return मान


    def कार्यक्रम_लोड(self, संचिका):

        print("कार्यक्रम RAM में लोड हो रहा है:", संचिका)

        with open(संचिका,"r",encoding="utf-8") as f:

            lines = f.readlines()

        base = self.आवंटन(len(lines))

        if base is None:
            return None

        for i,line in enumerate(lines):

            self.लिख(base+i, line.strip())

        print("कार्यक्रम RAM में लोड पूर्ण")

        return base


    def दिखाओ(self, start=0, end=20):

        print("RAM स्थिति:")

        for i in range(start,end):

            print(i,":",self.स्मृति[i])


# test

if __name__ == "__main__":

    ram = सूत्रRAM()

    base = ram.कार्यक्रम_लोड("test.यन्त्र")

    ram.दिखाओ(base, base+10)
