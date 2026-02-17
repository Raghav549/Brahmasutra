# ब्रह्म AI DATABASE ENGINE

import os
import json

print("🕉️ ब्रह्म AI Database Engine सक्रिय")


BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_DATABASE")

os.makedirs(BASE, exist_ok=True)



class ब्रह्मडेटाबेस:


    def __init__(self,नाम):

        self.path = f"{BASE}/{नाम}.db"

        if not os.path.exists(self.path):

            with open(self.path,"w",encoding="utf-8") as f:

                json.dump({},f)


    def लिखो(self,key,value):

        with open(self.path,"r",encoding="utf-8") as f:

            data = json.load(f)

        data[key] = value

        with open(self.path,"w",encoding="utf-8") as f:

            json.dump(data,f)

        print(f"संग्रहीत: {key} = {value}")


    def पढ़ो(self,key):

        with open(self.path,"r",encoding="utf-8") as f:

            data = json.load(f)

        if key in data:

            print(f"मान: {key} = {data[key]}")

            return data[key]

        else:

            print("नहीं मिला")

            return None


    def सूची(self):

        with open(self.path,"r",encoding="utf-8") as f:

            data = json.load(f)

        print("डेटाबेस सूची:")

        for k,v in data.items():

            print(k,"=",v)



if __name__ == "__main__":

    db = ब्रह्मडेटाबेस("test")

    db.लिखो("AI","BRAHMA")

    db.पढ़ो("AI")

    db.सूची()
