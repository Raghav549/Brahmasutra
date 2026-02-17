# ब्रह्म अनुप्रयोग पंजी तंत्र
# VERSION 50 FIXED

import json
import os


class ब्रह्मअनुप्रयोगपंजी:

    def __init__(self):

        self.file = os.path.expanduser(
            "~/सूत्र-तंत्र/apps_registry.json"
        )

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump({}, f)

    def पढ़ो(self):

        with open(self.file, "r") as f:
            return json.load(f)

    def लिखो(self, data):

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def पंजीकरण(self, नाम, पथ):

        data = self.पढ़ो()

        data[नाम] = {
            "name": नाम,
            "path": पथ,
            "status": "installed"
        }

        self.लिखो(data)

        return {
            "status": "success",
            "message": f"{नाम} registered"
        }

    def प्राप्त(self, नाम):

        data = self.पढ़ो()

        return data.get(नाम, None)

    def सूची(self):

        return self.पढ़ो()
