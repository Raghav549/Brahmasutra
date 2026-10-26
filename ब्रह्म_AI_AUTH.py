# ब्रह्म AI AUTH ENGINE

import os
import json
import uuid


class ब्रह्मAuth:


    def __init__(self):

        self.base = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_AUTH")

        os.makedirs(self.base, exist_ok=True)

        self.db = f"{self.base}/users.db"

        if not os.path.exists(self.db):

            with open(self.db,"w",encoding="utf-8") as f:

                json.dump({},f)


    def register(self, username, password):

        with open(self.db,"r",encoding="utf-8") as f:

            users = json.load(f)

        if username in users:

            print("User already exists")

            return

        users[username] = {

            "password": password,

            "token": ""

        }

        with open(self.db,"w",encoding="utf-8") as f:

            json.dump(users,f)

        print("User registered:", username)


    def login(self, username, password):

        with open(self.db,"r",encoding="utf-8") as f:

            users = json.load(f)

        if username not in users:

            print("User not found")

            return

        if users[username]["password"] != password:

            print("Wrong password")

            return

        token = str(uuid.uuid4())

        users[username]["token"] = token

        with open(self.db,"w",encoding="utf-8") as f:

            json.dump(users,f)

        print("Login success")

        print("Token:", token)

        return token


    def verify(self, token):

        with open(self.db,"r",encoding="utf-8") as f:

            users = json.load(f)

        for u in users:

            if users[u]["token"] == token:

                print("Verified:", u)

                return True

        print("Invalid token")

        return False


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global auth, token

    print("🕉️ ब्रह्म AI Auth Engine सक्रिय")
    auth = ब्रह्मAuth()

    auth.register("raghav","123")

    token = auth.login("raghav","123")

    auth.verify(token)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
