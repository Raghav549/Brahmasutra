# 🕉️ ब्रह्म AI डेटाबेस निर्माता VERSION 43

import os

class ब्रह्मडेटाबेसनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म डेटाबेस निर्माता सक्रिय")

        self.मूल = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग")


    def डेटाबेस_निर्माण(self, app_name):

        db_path = os.path.join(self.मूल, app_name, "database")

        os.makedirs(db_path, exist_ok=True)

        schema_file = os.path.join(db_path, "संरचना.ब्रह्म")

        schema = """

डेटाबेस प्रारम्भ

तालिका उपयोगकर्ता:

    क्षेत्र id
    क्षेत्र नाम
    क्षेत्र पासवर्ड
    क्षेत्र टोकन

समाप्त

तालिका डेटा:

    क्षेत्र id
    क्षेत्र मान

समाप्त

डेटाबेस समाप्त
"""

        with open(schema_file, "w", encoding="utf-8") as f:

            f.write(schema)

        print("डेटाबेस संरचना निर्मित:", schema_file)

        return schema_file



# test
if __name__ == "__main__":

    निर्माता = ब्रह्मडेटाबेसनिर्माता()

    app = input("App नाम लिखें: ")

    निर्माता.डेटाबेस_निर्माण(app)
