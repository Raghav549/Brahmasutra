import os
import zipfile


class ब्रह्मसंस्कृतपैकस्थापक:


    def __init__(self):

        print("🕉️ ब्रह्म संस्कृत पैक स्थापक सक्रिय")

        self.root = os.getcwd()

        self.install_dir = os.path.join(self.root, "स्थापित")

        os.makedirs(self.install_dir, exist_ok=True)


    def स्थापना(self, pack_file):

        pack_path = os.path.join(self.root, "पैक", pack_file)

        if not os.path.exists(pack_path):

            print("त्रुटि: पैक नहीं मिला")

            return


        app_name = pack_file.replace(".ब्रह्मपैक","")

        dest = os.path.join(self.install_dir, app_name)

        os.makedirs(dest, exist_ok=True)


        with zipfile.ZipFile(pack_path, "r") as z:

            z.extractall(dest)


        print("स्थापना सफल:", dest)

        return dest
