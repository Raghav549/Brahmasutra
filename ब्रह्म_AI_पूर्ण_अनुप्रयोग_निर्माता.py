# 🕉️ ब्रह्म AI पूर्ण अनुप्रयोग निर्माता VERSION 40

import os

class ब्रह्मपूर्णअनुप्रयोगनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म पूर्ण अनुप्रयोग निर्माता सक्रिय")

        self.मूल = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")

        os.makedirs(self.मूल, exist_ok=True)


    def नाम_निर्धारण(self, prompt):

        नाम = prompt.lower().replace(" ", "_")

        return नाम


    def संरचना_निर्माण(self, नाम):

        app_path = os.path.join(self.मूल, नाम)

        backend = os.path.join(app_path, "backend")
        frontend = os.path.join(app_path, "frontend")
        database = os.path.join(app_path, "database")
        auth = os.path.join(app_path, "auth")

        os.makedirs(backend, exist_ok=True)
        os.makedirs(frontend, exist_ok=True)
        os.makedirs(database, exist_ok=True)
        os.makedirs(auth, exist_ok=True)


        with open(os.path.join(backend, "server.ब्रह्म"), "w", encoding="utf-8") as f:

            f.write('दर्शय "बैकएंड सक्रिय"\n')


        with open(os.path.join(frontend, "ui.ब्रह्म"), "w", encoding="utf-8") as f:

            f.write('दर्शय "फ्रंटएंड सक्रिय"\n')


        with open(os.path.join(database, "database.ब्रह्म"), "w", encoding="utf-8") as f:

            f.write('दर्शय "डेटाबेस सक्रिय"\n')


        with open(os.path.join(auth, "auth.ब्रह्म"), "w", encoding="utf-8") as f:

            f.write('दर्शय "लॉगिन सक्रिय"\n')


        return app_path


    def निर्मित(self, prompt):

        नाम = self.नाम_निर्धारण(prompt)

        path = self.संरचना_निर्माण(नाम)

        print("पूर्ण अनुप्रयोग निर्मित:", path)

        return path



# test
if __name__ == "__main__":

    ai = ब्रह्मपूर्णअनुप्रयोगनिर्माता()

    prompt = input("Prompt लिखें: ")

    ai.निर्मित(prompt)
