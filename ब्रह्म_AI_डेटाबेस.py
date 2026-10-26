# ब्रह्म AI DATABASE ENGINE

import os
import json



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


BASE = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_DATABASE")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global db

    print("🕉️ ब्रह्म AI Database Engine सक्रिय")



    os.makedirs(BASE, exist_ok=True)
    db = ब्रह्मडेटाबेस("test")

    db.लिखो("AI","BRAHMA")

    db.पढ़ो("AI")

    db.सूची()


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
