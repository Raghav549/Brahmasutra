# 🕉️ सूत्र Hardware Abstraction Layer


class सूत्रHAL:


    def __init__(self):

        self.हार्डवेयर = {}

        print("🕉️ सूत्र HAL सक्रिय")


    def पंजीकरण(self, नाम, उपकरण):

        self.हार्डवेयर[नाम] = उपकरण

        print("HAL पंजीकृत:", नाम)


    def उपयोग(self, नाम, डेटा=None):

        if नाम not in self.हार्डवेयर:

            print("त्रुटि: HAL उपकरण नहीं मिला")

            return None


        return self.हार्डवेयर[नाम](डेटा)
