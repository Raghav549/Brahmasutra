# 🕉️ ब्रह्म अनुप्रयोग निर्माण कोर

import os
import uuid

from brahma_paths import data_root
class ब्रह्मअनुप्रयोगनिर्माणकोर:

    def __init__(self):

        print("🕉️ ब्रह्म अनुप्रयोग निर्माण कोर सक्रिय")

        self.base_path = data_root("ब्रह्म_अनुप्रयोग")

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)


    def निर्माण(self, नाम, कोड):

        app_id = str(uuid.uuid4())[:8]

        file_name = f"{नाम}_{app_id}.अनुप्रयोग"

        full_path = os.path.join(self.base_path, file_name)

        content = "ब्रह्मअनुप्रयोगV1\n"
        content += कोड

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("अनुप्रयोग निर्मित:", full_path)

        return full_path


# test run
if __name__ == "__main__":

    builder = ब्रह्मअनुप्रयोगनिर्माणकोर()

    code = """
स्थापित अ 100
दर्शय अ
स्थापित ब 200
योग अ ब
दर्शय अ
"""

    builder.निर्माण("परीक्षण", code)
