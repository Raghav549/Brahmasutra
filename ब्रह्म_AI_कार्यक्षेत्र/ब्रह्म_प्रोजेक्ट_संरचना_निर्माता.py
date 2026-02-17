# ब्रह्म_प्रोजेक्ट_संरचना_निर्माता.py
# BRAHMA PROJECT STRUCTURE GENERATOR
# VERSION 128

import os


class ब्रह्मप्रोजेक्टसंरचनानिर्माता:

    def __init__(self, base_path):

        self.base_path = base_path

        print("ब्रह्म प्रोजेक्ट संरचना निर्माता सक्रिय")


    def निर्माण(self, app_name, architecture):

        project_path = os.path.join(self.base_path, app_name)

        os.makedirs(project_path, exist_ok=True)


        if architecture.get("frontend"):

            os.makedirs(
                os.path.join(project_path, "frontend"),
                exist_ok=True
            )


        if architecture.get("backend"):

            os.makedirs(
                os.path.join(project_path, "backend"),
                exist_ok=True
            )


        if architecture.get("database"):

            os.makedirs(
                os.path.join(project_path, "database"),
                exist_ok=True
            )


        if architecture.get("ai_engine"):

            os.makedirs(
                os.path.join(project_path, "ai"),
                exist_ok=True
            )


        if architecture.get("deployment"):

            os.makedirs(
                os.path.join(project_path, "deployment"),
                exist_ok=True
            )


        os.makedirs(
            os.path.join(project_path, "config"),
            exist_ok=True
        )


        print("प्रोजेक्ट संरचना निर्मित:", project_path)

        return project_path
