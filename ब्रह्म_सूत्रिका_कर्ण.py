print("🕉️ ब्रह्म सूत्रिका कर्ण सक्रिय")


import threading


class ब्रह्मसूत्रिका:


    def __init__(self):

        self.threads = []

        self.counter = 1


    def निर्माण(self, नाम, कार्य):

        print("सूत्रिका निर्मित:", नाम)

        t = threading.Thread(target=self.चलाओ, args=(नाम, कार्य))

        self.threads.append(t)

        return t


    def चलाओ(self, नाम, कार्य):

        print("सूत्रिका प्रारम्भ:", नाम)

        for आदेश in कार्य:

            भाग = आदेश.split()

            if भाग[0] == "स्थापित":

                print("मान:", भाग[1], "=", भाग[2])

            elif भाग[0] == "दर्शय":

                print("दर्शित:", भाग[1])

        print("सूत्रिका समाप्त:", नाम)


    def प्रारम्भ(self):

        print("सभी सूत्रिकाएँ प्रारम्भ")

        for t in self.threads:

            t.start()

        for t in self.threads:

            t.join()

        print("सभी सूत्रिकाएँ पूर्ण")
