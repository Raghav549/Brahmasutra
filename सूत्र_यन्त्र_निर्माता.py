# 🕉️ सूत्र यन्त्र निर्माता (Executable Generator)

import os

class यन्त्रनिर्माता:

    def __init__(self):
        print("🕉️ सूत्र यन्त्र निर्माता सक्रिय")

        self.आधार_पथ = os.path.expanduser("~/सूत्र-तंत्र/यन्त्र")

        if not os.path.exists(self.आधार_पथ):
            os.makedirs(self.आधार_पथ)


    def निर्मित(self, नाम, कार्य_संचिका):

        with open(कार्य_संचिका,"r",encoding="utf-8") as f:
            code = f.read()

        output = os.path.join(self.आधार_पथ, नाम + ".यन्त्र")

        with open(output,"w",encoding="utf-8") as f:

            f.write("सूत्रयन्त्रV1\n")

            f.write(code)

        print("यन्त्र निर्मित:", output)

        return output
