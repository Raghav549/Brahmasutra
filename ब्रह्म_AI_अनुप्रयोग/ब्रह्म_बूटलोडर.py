# ब्रह्म बूटलोडर
# System startup controller

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_कर्नेल import ब्रह्मकर्नेल

class ब्रह्मबूटलोडर:

    def __init__(self):
        print("🕉️ ब्रह्म बूटलोडर प्रारंभ")
        self.kernel = None
        self.booted = False

    def बूट(self):

        if self.booted:
            return {
                "status": "error",
                "message": "already booted"
            }

        try:

            print("⚙️ कर्नेल लोड हो रहा है...")

            self.kernel = ब्रह्मकर्नेल()

            print("🧠 सिस्टम प्रारंभ...")

            self.booted = True

            return {
                "status": "success",
                "message": "BRAHMA SYSTEM BOOTED",
                "kernel": "active"
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

    def स्थिति(self):

        return {
            "booted": self.booted,
            "kernel": self.kernel is not None
        }

    def shutdown(self):

        if not self.booted:
            return {"status": "error"}

        self.kernel = None
        self.booted = False

        return {
            "status": "success",
            "message": "system shutdown"
        }
