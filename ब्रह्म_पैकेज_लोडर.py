import os
import zipfile
import shutil

class ब्रह्मपैकेजलोडर:

    def __init__(self):

        self.install_dir = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_स्थापित"
        )

        if not os.path.exists(self.install_dir):
            os.makedirs(self.install_dir)

        print("🕉️ ब्रह्म पैकेज लोडर सक्रिय")


    def स्थापना(self, पैकेज_पथ):

        if not os.path.exists(पैकेज_पथ):
            print("त्रुटि: पैकेज नहीं मिला")
            return

        temp_dir = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_temp_pkg"
        )

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        os.makedirs(temp_dir)

        with zipfile.ZipFile(पैकेज_पथ,"r") as z:
            z.extractall(temp_dir)

        src = os.path.join(temp_dir,"मुख्य.कार्यक्रम")

        name = os.path.basename(पैकेज_पथ).replace(".ब्रह्मपैक",".कार्यक्रम")

        dst = os.path.join(self.install_dir,name)

        shutil.copy(src,dst)

        print("पैकेज स्थापित:", name)
