# ब्रह्म शेड्यूलर

class ब्रह्मशेड्यूलर:

    def __init__(self):
        print("🕉️ ब्रह्म शेड्यूलर सक्रिय")
        self.प्रोसेस = {}

    def जोड़ो(self, pid):
        self.प्रोसेस[pid] = "ready"
        return {"status": "success"}

    def हटाओ(self, pid):
        if pid in self.प्रोसेस:
            del self.प्रोसेस[pid]
            return {"status": "success"}
        return {"status": "error"}

    def सूची(self):
        return self.प्रोसेस
