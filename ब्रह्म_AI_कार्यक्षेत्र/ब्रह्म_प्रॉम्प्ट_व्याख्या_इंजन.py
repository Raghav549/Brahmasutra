# ब्रह्म प्रॉम्प्ट व्याख्या इंजन
# VERSION 113
# उद्देश्य: उपयोगकर्ता प्रॉम्प्ट → संरचित निर्माण योजना

import os
import json
import datetime


class ब्रह्मप्रॉम्प्टव्याख्याइंजन:

    def __init__(self):
        self.workspace = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र")
        self.output_dir = os.path.join(self.workspace, "generated_apps")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        print("ब्रह्म प्रॉम्प्ट व्याख्या इंजन सक्रिय")

    def व्याख्या(self, prompt_text):

        print("प्रॉम्प्ट प्राप्त:")
        print(prompt_text)

        app_name = self.नाम_निर्माण(prompt_text)

        योजना = {
            "app_name": app_name,
            "prompt": prompt_text,
            "created_at": str(datetime.datetime.now()),
            "frontend": True,
            "backend": True,
            "database": True,
            "deployment": True
        }

        self.सहेजें_योजना(app_name, योजना)

        return योजना

    def नाम_निर्माण(self, prompt):

        words = prompt.lower().split()

        if len(words) == 0:
            return "brahma_app"

        base = "_".join(words[:3])

        clean = "".join(c for c in base if c.isalnum() or c == "_")

        return clean

    def सहेजें_योजना(self, app_name, योजना):

        folder = os.path.join(self.output_dir, app_name)

        if not os.path.exists(folder):
            os.makedirs(folder)

        योजना_file = os.path.join(folder, "build_plan.json")

        with open(योजना_file, "w", encoding="utf-8") as f:
            json.dump(योजना, f, indent=4, ensure_ascii=False)

        print("निर्माण योजना सहेजी गई:")
        print(योजना_file)
