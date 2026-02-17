from ब्रह्म_संस्कृत_निष्पादन_इंजन import ब्रह्मसंस्कृतनिष्पादनइंजन


class ब्रह्मसूत्रफाइलनिष्पादन:

    def __init__(self):

        print("🕉️ ब्रह्म सूत्र फाइल निष्पादन प्रणाली सक्रिय")

        self.engine = ब्रह्मसंस्कृतनिष्पादनइंजन()


    def सूत्र_चलाओ(self, path):

        try:

            with open(path, "r", encoding="utf-8") as f:

                code = f.read()

            print(f"सूत्र लोड: {path}")

            result = self.engine.निष्पादित(code)

            return {

                "status": "success",

                "result": result

            }

        except Exception as e:

            return {

                "status": "error",

                "message": str(e)

            }
