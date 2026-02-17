# ब्रह्म उपकरण स्तर

class ब्रह्मउपकरणस्तर:

    def __init__(self):

        self.उपकरण = {}

        print("🔧 ब्रह्म उपकरण स्तर सक्रिय")


    def पंजीकृत_करो(self, नाम, प्रकार):

        self.उपकरण[नाम] = {
            "type": प्रकार,
            "status": "active"
        }

        return {
            "status": "success",
            "device": नाम
        }


    def स्थिति(self, नाम):

        if नाम in self.उपकरण:

            return self.उपकरण[नाम]

        return {
            "status": "not found"
        }


    def सूची(self):

        return self.उपकरण


    def हटाओ(self, नाम):

        if नाम in self.उपकरण:

            del self.उपकरण[नाम]

            return {
                "status": "success"
            }

        return {
            "status": "error"
        }
