# ब्रह्म AI DATABASE तंत्र

import os
import json


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


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global db

    print("🕉️ ब्रह्म AI Database Engine सक्रिय")
    db = ब्रह्मDatabase()

    db.निर्माण("chat")

    db.लिखो("chat","username","raghav")

    db.पढ़ो("chat","username")

    db.सूची("chat")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
