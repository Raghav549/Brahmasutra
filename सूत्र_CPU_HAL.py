# 🕉️ CPU HAL


class CPU:


    def __init__(self):

        self.रजिस्टर = {

            "अ":0,
            "ब":0,
            "स":0,
            "द":0

        }

        print("🕉️ CPU HAL सक्रिय")


    def स्थापित(self, नाम, मान):

        self.रजिस्टर[नाम] = मान

        print("CPU स्थापित:", नाम, "=", मान)


    def प्राप्त(self, नाम):

        return self.रजिस्टर.get(नाम,0)
