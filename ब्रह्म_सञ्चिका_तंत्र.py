import os


class ब्रह्मसञ्चिकातंत्र:


    def __init__(self):

        self.root = "/data/data/com.termux/files/home/सूत्र-तंत्र/ब्रह्म_सञ्चिका"

        os.makedirs(self.root, exist_ok=True)

        print("🕉️ ब्रह्म सञ्चिका तंत्र सक्रिय")



    def पथ(self, नाम):

        return os.path.join(self.root, नाम)



    def निर्माण(self, नाम, data):

        path = self.पथ(नाम)

        with open(path, "w", encoding="utf-8") as f:

            f.write(data)

        print("सञ्चिका निर्मित:", path)

        return path



    def पठन(self, नाम):

        path = self.पथ(नाम)

        if not os.path.exists(path):

            print("त्रुटि: सञ्चिका नहीं मिली")

            return None

        with open(path, "r", encoding="utf-8") as f:

            data = f.read()

        print("सञ्चिका पठन:", path)

        return data



    def सूची(self):

        print("सञ्चिका सूची:")

        for f in os.listdir(self.root):

            print("•", f)



    def हटाओ(self, नाम):

        path = self.पथ(नाम)

        if os.path.exists(path):

            os.remove(path)

            print("सञ्चिका हटाई:", path)
