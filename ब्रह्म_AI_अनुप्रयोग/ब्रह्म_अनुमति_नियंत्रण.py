# ब्रह्म अनुमति नियंत्रण प्रणाली

class ब्रह्मअनुमतिनियंत्रण:

    def __init__(self):
        self.अनुमतियाँ = {}
        print("🔐 ब्रह्म अनुमति नियंत्रण सक्रिय")


    def अनुमति_दो(self, प्रक्रिया_id, संसाधन):

        if प्रक्रिया_id not in self.अनुमतियाँ:
            self.अनुमतियाँ[प्रक्रिया_id] = []

        if संसाधन not in self.अनुमतियाँ[प्रक्रिया_id]:
            self.अनुमतियाँ[प्रक्रिया_id].append(संसाधन)

        return {
            "status": "success",
            "pid": प्रक्रिया_id,
            "permission": संसाधन
        }


    def अनुमति_जांच(self, प्रक्रिया_id, संसाधन):

        if प्रक्रिया_id not in self.अनुमतियाँ:
            return False

        return संसाधन in self.अनुमतियाँ[प्रक्रिया_id]


    def अनुमति_सूची(self, प्रक्रिया_id):

        return self.अनुमतियाँ.get(प्रक्रिया_id, [])


    def अनुमति_हटाओ(self, प्रक्रिया_id, संसाधन):

        if प्रक्रिया_id in self.अनुमतियाँ:

            if संसाधन in self.अनुमतियाँ[प्रक्रिया_id]:

                self.अनुमतियाँ[प्रक्रिया_id].remove(संसाधन)

                return {
                    "status": "success",
                    "removed": संसाधन
                }

        return {
            "status": "error",
            "message": "permission not found"
        }
