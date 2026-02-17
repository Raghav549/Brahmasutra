# ब्रह्म स्थापक v17

import os
import shutil

print("🕉️ ब्रह्म अनुप्रयोग स्थापक सक्रिय")

class ब्रह्मस्थापक:

    def __init__(self):

        self.install_dir = "/data/data/com.termux/files/home/सूत्र-तंत्र/ब्रह्म_स्थापित"

        os.makedirs(self.install_dir, exist_ok=True)

    def स्थापना(self, program_path):

        if not os.path.exists(program_path):

            print("त्रुटि: कार्यक्रम नहीं मिला")
            return

        name = os.path.basename(program_path)

        dest = os.path.join(self.install_dir, name)

        shutil.copy(program_path, dest)

        print("स्थापित:", name)

    def सूची(self):

        files = os.listdir(self.install_dir)

        print("स्थापित अनुप्रयोग:")

        for f in files:

            print("•", f)

    def निष्पादन(self, name):

        path = os.path.join(self.install_dir, name)

        if not os.path.exists(path):

            print("त्रुटि: अनुप्रयोग स्थापित नहीं")
            return

        from ब्रह्म_कार्यक्रम_लोडर import ब्रह्मकार्यक्रमलोडर

        loader = ब्रह्मकार्यक्रमलोडर()

        loader.निष्पादन(path)
