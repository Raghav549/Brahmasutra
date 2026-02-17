# ब्रह्म स्मृति प्रबंधक

class ब्रह्मस्मृति:

    def __init__(self):

        print("🕉️ ब्रह्म स्मृति सक्रिय")

        self.storage = {}


    # write memory
    def लिखो(self, key, value):

        self.storage[key] = value

        return {
            "status": "success"
        }


    # read memory
    def पढ़ो(self, key):

        if key in self.storage:

            return {
                "status": "success",
                "value": self.storage[key]
            }

        return {
            "status": "error",
            "message": "not found"
        }


    # list memory
    def सूची(self):

        return self.storage
