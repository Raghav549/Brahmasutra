import os
import zipfile


class ब्रह्मसंस्कृतपैकनिर्माता:


    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत पैक निर्माता सक्रिय")

        self.root = os.getcwd()

        self.pack_dir = os.path.join(self.root, "पैक")

        os.makedirs(self.pack_dir, exist_ok=True)


    def निर्माण(self, folder_name):

        folder_path = os.path.join(self.root, folder_name)

        if not os.path.exists(folder_path):

            print("त्रुटि: folder नहीं मिला")

            return


        pack_name = folder_name + ".ब्रह्मपैक"

        pack_path = os.path.join(self.pack_dir, pack_name)


        with zipfile.ZipFile(pack_path, "w") as z:

            for root, dirs, files in os.walk(folder_path):

                for file in files:

                    full_path = os.path.join(root, file)

                    rel_path = os.path.relpath(full_path, folder_path)

                    z.write(full_path, rel_path)


        print("पैक निर्मित:", pack_path)

        return pack_path
