# ब्रह्म उपकरण प्रबंधक
# VERSION 55

class ब्रह्मउपकरणप्रबंधक:

    def __init__(self):

        self.devices = {}

        print("🕉️ ब्रह्म उपकरण प्रबंधक सक्रिय")


    def पंजीकरण(self, नाम, प्रकार):

        self.devices[नाम] = {
            "type": प्रकार,
            "status": "active"
        }

        return {
            "status": "success",
            "device": नाम
        }


    def हटाएं(self, नाम):

        if नाम in self.devices:

            del self.devices[नाम]

            return {
                "status": "success"
            }

        return {
            "status": "error",
            "message": "device not found"
        }


    def सूची(self):

        return self.devices


    def स्थिति(self, नाम):

        if नाम in self.devices:

            return self.devices[नाम]

        return {
            "status": "error"
        }
