# 🕉️ ब्रह्म अनुप्रयोग स्थापक

import os
import shutil

from ब्रह्म_अनुप्रयोग_लोडर import ब्रह्मअनुप्रयोगलोडर


class ब्रह्मस्थापक:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग स्थापक सक्रिय")

        self.install_dir = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_स्थापित"
        )

        os.makedirs(self.install_dir, exist_ok=True)

        self.loader = ब्रह्मअनुप्रयोगलोडर()


    def स्थापना(self, path):

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग नहीं मिला")
            return


        name = os.path.basename(path)

        dest = os.path.join(self.install_dir, name)

        shutil.copy(path, dest)

        print("स्थापित:", name)


    def सूची(self):

        print("स्थापित अनुप्रयोग:")

        for f in os.listdir(self.install_dir):

            print("•", f)


    def निष्पादन(self, name):

        path = os.path.join(self.install_dir, name)

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग स्थापित नहीं")
            return


        print("अनुप्रयोग चल रहा है:", name)

        self.loader.निष्पादन(path)
