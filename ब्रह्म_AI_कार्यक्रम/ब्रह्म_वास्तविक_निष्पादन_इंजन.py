# ब्रह्म वास्तविक निष्पादन इंजन

class ब्रह्मवास्तविकनिष्पादनइंजन:

    def __init__(self):
        self.स्मृति = {}
        print("🕉️ ब्रह्म वास्तविक निष्पादन इंजन सक्रिय")


    def निष्पादन(self, filepath):

        try:

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:

                line = line.strip()

                if not line:
                    continue


                # चर creation
                if line.startswith("चर:"):

                    parts = line.replace("चर:", "").strip().split("=")

                    var = parts[0].strip()
                    value = int(parts[1].strip())

                    self.स्मृति[var] = value

                    print(f"चर संग्रहीत: {var} = {value}")


                # addition
                elif line.startswith("योग:"):

                    parts = line.replace("योग:", "").strip().split()

                    a = parts[0]
                    b = parts[1]

                    result = self.स्मृति[a] + self.स्मृति[b]

                    self.स्मृति["परिणाम"] = result

                    print(f"योग परिणाम: {result}")


                # display
                elif line.startswith("दर्शय:"):

                    msg = line.replace("दर्शय:", "").strip()

                    if msg in self.स्मृति:
                        print(self.स्मृति[msg])
                    else:
                        print(msg)


            return {"status": "success"}

        except Exception as e:

            return {"status": "error", "message": str(e)}
