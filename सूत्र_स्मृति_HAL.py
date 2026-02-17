# 🕉️ Memory HAL


class स्मृति:


    def __init__(self):

        self.स्थान = {}

        print("🕉️ स्मृति HAL सक्रिय")


    def लिख(self, पता, मान):

        self.स्थान[पता] = मान


    def पढ़(self, पता):

        return self.स्थान.get(पता,0)
