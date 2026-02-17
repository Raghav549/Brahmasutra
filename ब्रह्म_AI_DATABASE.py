# ब्रह्म AI DATABASE तंत्र

import os
import json

print("🕉️ ब्रह्म AI Database Engine सक्रिय")


class ब्रह्मDatabase:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_DATABASE")

        os.makedirs(self.base, exist_ok=True)


    def निर्माण(self, नाम):

        path = f"{self.base}/{नाम}.db"

        if not os.path.exists(path):

            with open(path,"w",encoding="utf-8") as f:

                json.dump({},f)

        print("Database निर्मित:", path)

        return path


    def लिखो(self, नाम, key, value):

        path = f"{self.base}/{नाम}.db"

        with open(path,"r",encoding="utf-8") as f:

            data = json.load(f)

        data[key] = value

        with open(path,"w",encoding="utf-8") as f:

            json.dump(data,f)

        print("Data saved:", key)


    def पढ़ो(self, नाम, key):

        path = f"{self.base}/{नाम}.db"

        with open(path,"r",encoding="utf-8") as f:

            data = json.load(f)

        print("Value:", data.get(key))


    def सूची(self, नाम):

        path = f"{self.base}/{नाम}.db"

        with open(path,"r",encoding="utf-8") as f:

            data = json.load(f)

        print("Database contents:")

        for k,v in data.items():

            print(k,"=",v)



# test

if __name__ == "__main__":

    db = ब्रह्मDatabase()

    db.निर्माण("chat")

    db.लिखो("chat","username","raghav")

    db.पढ़ो("chat","username")

    db.सूची("chat")
